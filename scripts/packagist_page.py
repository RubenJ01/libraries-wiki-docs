import json
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
INDEX_MD = DOCS / "index.md"
LEGACY_PACKAGES = DOCS / "packages.md"


def _ua(settings: dict) -> str:
    m = settings.get("packagist_contact") or "RubenJ01"
    if "@" in m:
        return f"rjds-docs-sync (mailto:{m})"
    return f"rjds-docs-sync (+https://github.com/{m})"


def _http_json(url: str, settings: dict) -> dict | None:
    req = urllib.request.Request(url, headers={"User-Agent": _ua(settings), "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, TimeoutError):
        return None


def _repo_slug(repo_url: str, github_user: str) -> str | None:
    if not repo_url:
        return None
    u = repo_url.rstrip("/").removesuffix(".git")
    m = re.match(rf"https?://github\.com/{re.escape(github_user)}/([^/]+)$", u, re.I)
    return m.group(1) if m else None


def _format_release_date(iso_time: str) -> str:
    if not iso_time:
        return "—"
    try:
        dt = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return iso_time[:10] if len(iso_time) >= 10 else "—"


def _latest_stable_release(versions: object) -> tuple[str, str]:
    if not isinstance(versions, dict):
        return ("—", "—")
    candidates: list[tuple[str, str, str]] = []
    for _key, meta in versions.items():
        if not isinstance(meta, dict):
            continue
        vn = str(meta.get("version_normalized") or "")
        if vn.startswith("dev-") or vn in ("dev-main", ""):
            continue
        disp = str(meta.get("version") or "").strip()
        if not disp or disp.startswith("dev-"):
            continue
        if disp.startswith("v") and len(disp) > 1 and disp[1].isdigit():
            disp = disp[1:]
        sort_key = str(meta.get("time") or "")
        iso = sort_key
        candidates.append((sort_key, disp, iso))
    if not candidates:
        return ("—", "—")
    candidates.sort(key=lambda x: x[0], reverse=True)
    _sk, disp, iso = candidates[0]
    return (disp, _format_release_date(iso))


def _fetch_packages(vendor: str, settings: dict, gh: str) -> list[dict]:
    data = _http_json(f"https://packagist.org/packages/list.json?vendor={urllib.parse.quote(vendor)}", settings)
    if not data or "packageNames" not in data:
        return []

    packages: list[dict] = []
    for full_name in sorted(data["packageNames"]):
        slug_path = urllib.parse.quote(full_name, safe="")
        j = _http_json(f"https://packagist.org/packages/{slug_path}.json", settings)
        if not j or "package" not in j:
            continue
        p = j["package"]
        dl = p.get("downloads") or {}
        latest, updated = _latest_stable_release(p.get("versions"))
        packages.append(
            {
                "name": p.get("name", full_name),
                "repository": (p.get("repository") or "").strip(),
                "url": f"https://packagist.org/packages/{slug_path}",
                "total": int(dl.get("total") or 0),
                "monthly": int(dl.get("monthly") or 0),
                "latest": latest,
                "updated": updated,
            }
        )
    packages.sort(key=lambda x: (-x["total"], x["name"].lower()))
    return packages


def write_home_md(settings: dict, wiki_repo_names: list[str]) -> None:
    if LEGACY_PACKAGES.exists():
        LEGACY_PACKAGES.unlink()

    gh = settings.get("github_user") or "RubenJ01"
    title = (settings.get("site_name") or "Documentation").strip()
    vendor = (settings.get("packagist_vendor") or "").strip()
    wiki_set = set(wiki_repo_names)

    pkg_by_slug: dict[str, dict] = {}
    if vendor:
        for pkg in _fetch_packages(vendor, settings, gh):
            slug = _repo_slug(pkg["repository"], gh)
            if slug:
                pkg_by_slug[slug] = pkg

    slugs = sorted(wiki_set | set(pkg_by_slug.keys()), key=str.lower)
    if pkg_by_slug:
        top_slug = max(pkg_by_slug, key=lambda s: pkg_by_slug[s]["total"])
        example_pkg = pkg_by_slug[top_slug]["name"]
    elif vendor:
        example_pkg = f"{vendor}/your-package"
    else:
        example_pkg = "vendor/package"

    lines: list[str] = [
        f"# {title}",
        "",
        "Documentation for RJDS PHP packages: install via Composer, then use **docs** for usage and API notes (mirrored from GitHub wikis).",
        "",
        "## Composer",
        "",
        "```bash",
        f"composer require {example_pkg}",
        "```",
        "",
        "Pick the package name from the table below. Constraint examples: `^3.0`, `^1.1`.",
        "",
    ]

    if vendor:
        lines.append(
            f"All listed packages: [`{vendor}/…` on Packagist](https://packagist.org/search/?q={urllib.parse.quote(vendor + '/')})."
        )
        lines.append("")

    lines.append("## Projects")
    lines.append("")
    lines.append("| Project | Latest | Updated | Installs (total / mo) | Composer | Wiki |")
    lines.append("| --- | --- | --- | ---: | --- | :---: |")

    if not slugs:
        lines.append("| — | — | — | — | — | — |")
    else:
        for slug in slugs:
            gh_url = f"https://github.com/{gh}/{slug}"
            wiki_cell = f"[docs](projects/{slug}/index.md)" if slug in wiki_set else "—"
            pkg = pkg_by_slug.get(slug)
            if pkg:
                comp = f"[`{pkg['name']}`]({pkg['url']})"
                ins = f"{pkg['total']:,} / {pkg['monthly']:,}"
                ver = f"`{pkg['latest']}`" if pkg["latest"] != "—" else "—"
                upd = pkg["updated"] if pkg["updated"] != "—" else "—"
            else:
                comp = "—"
                ins = "—"
                ver = "—"
                upd = "—"
            lines.append(f"| [`{slug}`]({gh_url}) | {ver} | {upd} | {ins} | {comp} | {wiki_cell} |")

    lines.append("")

    INDEX_MD.write_text("\n".join(lines), encoding="utf-8")
