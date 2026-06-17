# Releasing

Releases are automated via `.github/workflows/publish.yml`. Pushing a version
tag (`vX.Y.Z`) builds and publishes the package to PyPI.

## One-time setup (PyPI Trusted Publishing)

This repo uses [Trusted Publishing](https://docs.pypi.org/trusted-publishers/),
so no API token is stored in GitHub. Configure it once:

1. Go to https://pypi.org/manage/project/llm-promptlint/settings/publishing/
2. Add a new **GitHub** trusted publisher:
   - **Owner:** `pop123-ux`
   - **Repository:** `promptlint`
   - **Workflow name:** `publish.yml`
   - **Environment:** `pypi`
3. In the GitHub repo: **Settings → Environments → New environment → `pypi`**
   (optionally add required reviewers for a manual approval gate before publish).

## Cutting a release

```bash
# 1. Bump the version in pyproject.toml (e.g. 0.1.0 -> 0.1.1)
# 2. Commit it
git commit -am "Release v0.1.1"

# 3. Tag and push
git tag v0.1.1
git push origin main --tags
```

The workflow builds, runs `twine check`, and publishes to PyPI automatically.
Create a GitHub Release from the tag for nicer changelogs (optional).

## Manual fallback

```bash
python -m build
python -m twine upload dist/*
```
