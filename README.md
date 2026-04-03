# RJDS wiki docs

One MkDocs site for all the wikis on my public GitHub repos (RJDS stuff — PHP libs, Magento modules, whatever else has a wiki). It clones each `something.wiki.git`, dumps the markdown into `docs/projects/`, and builds with Material.

No wiki on a repo = it doesn’t show up. 

## Local

```text
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python scripts/sync_wikis.py
.venv\Scripts\mkdocs serve
```

(Fix the path to `pip`/`python` if you’re not on Windows.)

`sync_settings.yaml` has `github_user`, `site_name`, and `site_url` if you care about canonical URLs.

## Pages + the bot commits

Point GitHub Pages at **Actions** under Settings. The workflow syncs, builds, deploys. It also **commits** `docs/projects/` and `mkdocs.yml` when they change, so the tree isn’t only updated on your laptop.

You need **Workflow permissions → Read and write** or the push step dies. Protected `main` means you have to let Actions push or swap in a PAT — that’s on you.

Wiki edits don’t trigger Actions on those other repos, so there’s an hourly cron. Bored waiting? `repository_dispatch` with `wikis_updated` or hit “Run workflow”.

## Random details

Unauthenticated API is fine for a few repos. The sync script fixes wiki `[[links]]` and adds `<?php` to fenced PHP blocks in the **built** output only so highlighting works.
