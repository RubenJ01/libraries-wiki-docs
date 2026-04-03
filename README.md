# RJDS wiki docs

MkDocs site: mirrors GitHub wikis into `docs/projects/` and regenerates the **home page** with a single **projects table** (GitHub link, wiki docs link, Composer package, install counts, release RSS). No wiki on a repo → no wiki column for that row.

## Local

```text
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python scripts/sync_wikis.py
.venv\Scripts\mkdocs serve
```

`sync_settings.yaml`: `github_user`, `docs_repo` (this repo name, for the clone URL on the home page), `site_name`, `site_url`, `packagist_vendor`, optional `packagist_contact` (email for Packagist’s API user-agent).

Sidebar: **Home** plus **one link per wiki** (home page of that wiki only; deeper pages are linked inside the wiki).

## Pages + the bot commits

GitHub **Settings → Pages → GitHub Actions**. Workflow needs **Workflow permissions → Read and write** so it can commit `docs/projects/`, `docs/index.md`, and `mkdocs.yml`.

Hourly cron + `repository_dispatch` `wikis_updated` + push to `main`.

## Details

Packagist list + stats use the public API. Wiki `[[links]]` are normalized; PHP fences get `<?php` in the **output** only for highlighting.
