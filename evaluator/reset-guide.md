# Reset Guide

## Reset a local working copy

From the repository root, remove candidate changes and untracked runtime files:

```bash
git fetch origin
git switch main
git reset --hard origin/main
git clean -fdx
docker compose down -v --remove-orphans
```

If this assessment is distributed without a remote, replace `origin/main` with the known baseline commit or recreate the clone:

```bash
git reset --hard <baseline-commit>
git clean -fdx
docker compose down -v --remove-orphans
```

## Verify the reset

```bash
pip install -r requirements.txt
pytest -q
DATABASE_PATH=data/projects.db uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal, `curl http://127.0.0.1:8000/health` should return `{"status":"ok"}`. Stop the server, then remove `data/projects.db` if a truly empty local database is required.

## Reset Docker state only

```bash
docker compose down -v --remove-orphans
docker compose up --build -d
docker compose logs --tail=50
docker compose down -v
```
