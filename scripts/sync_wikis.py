#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

import yaml

from packagist_page import write_home_md

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PROJECTS = DOCS / "projects"
SETTINGS_PATH = ROOT / "sync_settings.yaml"
MKDOCS_PATH = ROOT / "mkdocs.yml"


def load_settings() -> dict:
    if not SETTINGS_PATH.is_file():
        print(f"Missing {SETTINGS_PATH}", file=sys.stderr)
        sys.exit(1)
    with SETTINGS_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def github_public_repos(username: str) -> list[dict]:
    repos: list[dict] = []
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    while url:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "rjds-wiki-docs-sync",
            },
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            link = resp.headers.get("Link", "")
        data = json.loads(raw)
        repos.extend(data)
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                m = re.search(r"<([^>]+)>", part)
                if m:
                    url = m.group(1)
                break
    out = [r for r in repos if not r.get("private") and not r.get("fork")]
    out.sort(key=lambda r: r["name"].lower())
    return out


def clone_wiki(wiki_url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    r = subprocess.run(
        ["git", "clone", "--depth", "1", wiki_url, str(dest)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return False
    return True


def transform_wiki_links(text: str) -> str:
    def to_md_file(stem_or_name: str) -> str:
        s = stem_or_name.strip()
        if not s.lower().endswith(".md"):
            s = f"{s}.md"
        if Path(s).stem.lower() == "home":
            return "index.md"
        return s

    def pipe_link(m: re.Match) -> str:
        label = m.group(1).strip()
        target = to_md_file(m.group(2).strip())
        return f"[{label}]({target})"

    def bare_link(m: re.Match) -> str:
        label = m.group(1).strip()
        slug = "-".join(label.split())
        target = to_md_file(slug)
        return f"[{label}]({target})"

    def fix_slug_md_links(chunk: str) -> str:
        def repl(m: re.Match) -> str:
            label = m.group(1)
            target = m.group(2)
            if target.startswith("#") or "/" in target or ":" in target:
                return m.group(0)
            low = target.lower()
            if low.endswith((".md", ".html", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
                return m.group(0)
            if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9\-]{0,240}", target):
                if target.lower() == "home":
                    return f"[{label}](index.md)"
                return f"[{label}]({target}.md)"
            return m.group(0)

        return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", repl, chunk)

    def wiki_brackets(chunk: str) -> str:
        chunk = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", pipe_link, chunk)
        chunk = re.sub(r"\[\[([^\]|]+)\]\]", bare_link, chunk)
        chunk = fix_slug_md_links(chunk)
        return chunk

    parts = re.split(r"(```[\s\S]*?```)", text)
    for i in range(0, len(parts), 2):
        parts[i] = wiki_brackets(parts[i])
    return "".join(parts)


def ensure_php_open_tag_for_highlight(text: str) -> str:
    def repl(m: re.Match) -> str:
        opener, body, closer = m.group(1), m.group(2), m.group(3)
        if body.lstrip().startswith("<?"):
            return m.group(0)
        return f"{opener}<?php\n\n{body}{closer}"

    return re.sub(r"(```php\s*\n)([\s\S]*?)(```)", repl, text, flags=re.IGNORECASE)


def wiki_md_files(wiki_dir: Path) -> list[Path]:
    return sorted(
        (p for p in wiki_dir.glob("*.md") if not p.name.startswith("_")),
        key=lambda p: p.name.lower(),
    )


def copy_wiki_to_docs(wiki_dir: Path, target: Path) -> list[str]:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    has_home = any(p.name.lower() == "home.md" for p in wiki_md_files(wiki_dir))

    rel_paths: list[str] = []
    for src in wiki_md_files(wiki_dir):
        if has_home and src.name.lower() == "readme.md":
            continue
        name = src.name
        if name.lower() == "home.md":
            dst = target / "index.md"
        else:
            dst = target / name
        body = src.read_text(encoding="utf-8")
        body = transform_wiki_links(body)
        body = ensure_php_open_tag_for_highlight(body)
        dst.write_text(body, encoding="utf-8")
        rel_paths.append(str(dst.relative_to(DOCS)).replace("\\", "/"))

    index = target / "index.md"
    if not index.is_file():
        pages = [p for p in sorted(target.glob("*.md"))]
        if not pages:
            return []
        if len(pages) == 1:
            only = pages[0]
            if only.name.lower() != "index.md":
                only.rename(index)
            rel_paths = [str(index.relative_to(DOCS)).replace("\\", "/")]
        else:
            lines = ["# Wiki\n", "\n"]
            for p in pages:
                title = p.stem.replace("-", " ")
                lines.append(f"- [{title}]({p.name})\n")
            index.write_text("".join(lines), encoding="utf-8")
            rel_paths.insert(0, str(index.relative_to(DOCS)).replace("\\", "/"))

    return sorted(set(rel_paths), key=lambda s: (0 if s.endswith("/index.md") or s.endswith("index.md") else 1, s))


def _nav_page_title(rel_path: str) -> str:
    stem = Path(rel_path).stem
    if stem.lower() == "index":
        return "Home"
    return stem.replace("-", " ")


def nav_entry_for_repo(slug: str, doc_paths: list[str]) -> dict:
    prefix = f"projects/{slug}/"
    pages = sorted(
        [p for p in doc_paths if p.startswith(prefix) and p.lower().endswith(".md")],
        key=lambda p: (0 if Path(p).stem.lower() == "index" else 1, p.lower()),
    )
    index_path = f"{prefix}index.md"
    if not pages:
        return {slug: index_path}
    if len(pages) == 1:
        return {slug: pages[0]}
    children: list = []
    if index_path in pages:
        children.append(index_path)
        rest = [p for p in pages if p != index_path]
    else:
        rest = list(pages)
    children.extend({_nav_page_title(p): p} for p in rest)
    return {slug: children}


def write_mkdocs(settings: dict, nav_projects: list) -> None:
    site_name = settings.get("site_name") or "RJDS — Documentation"
    site_url = settings.get("site_url") or ""

    nav: list = [{"Home": "index.md"}]
    nav.extend(sorted(nav_projects, key=lambda d: next(iter(d)).lower()))

    cfg: dict = {
        "site_name": site_name,
        "theme": {
            "name": "material",
            "palette": [
                {"scheme": "default", "primary": "indigo", "toggle": {"icon": "material/brightness-7", "name": "Switch to dark"}},
                {"scheme": "slate", "primary": "indigo", "toggle": {"icon": "material/brightness-4", "name": "Switch to light"}},
            ],
            "features": [
                "content.code.copy",
                "navigation.indexes",
            ],
        },
        "markdown_extensions": [
            {
                "pymdownx.highlight": {
                    "anchor_linenums": True,
                    "line_spans": "__span",
                    "pygments_lang_class": True,
                }
            },
            {"pymdownx.superfences": {}},
            "tables",
        ],
        "nav": nav,
    }
    gh_user = settings.get("github_user") or "RubenJ01"
    docs_repo = (settings.get("docs_repo") or "").strip()
    repo_url = (settings.get("repo_url") or "").strip()
    repo_name = (settings.get("repo_name") or "").strip()
    if not repo_url and docs_repo:
        repo_url = f"https://github.com/{gh_user}/{docs_repo}"
    if repo_url:
        cfg["repo_url"] = repo_url
        cfg["repo_name"] = repo_name or (f"{gh_user}/{docs_repo}" if docs_repo else "GitHub")
    if site_url:
        cfg["site_url"] = site_url

    with MKDOCS_PATH.open("w", encoding="utf-8") as f:
        yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main() -> None:
    settings = load_settings()
    user = settings.get("github_user") or "RubenJ01"

    PROJECTS.mkdir(parents=True, exist_ok=True)
    for child in PROJECTS.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        elif child.is_file():
            child.unlink()

    repos = github_public_repos(user)
    nav_projects: list = []
    synced = 0
    synced_repo_names: list[str] = []

    for repo in repos:
        name = repo["name"]
        wiki_url = f"https://github.com/{user}/{name}.wiki.git"
        with tempfile.TemporaryDirectory(prefix="wiki-") as tmp:
            tmp_path = Path(tmp) / "wiki"
            if not clone_wiki(wiki_url, tmp_path):
                print(f"skip (no wiki): {name}")
                continue
            md = wiki_md_files(tmp_path)
            if not md:
                print(f"skip (empty wiki): {name}")
                continue
            target = PROJECTS / name
            paths = copy_wiki_to_docs(tmp_path, target)
            if not paths:
                print(f"skip (no pages): {name}")
                continue
            nav_projects.append(nav_entry_for_repo(name, paths))
            synced_repo_names.append(name)
            synced += 1
            print(f"synced: {name} ({len(paths)} page(s))")

    write_home_md(settings, synced_repo_names)
    write_mkdocs(settings, nav_projects)
    print(f"\nWrote {MKDOCS_PATH} ({synced} wiki(s)).")


if __name__ == "__main__":
    main()
