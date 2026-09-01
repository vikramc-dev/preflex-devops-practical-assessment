# Evaluator Guide

Use this repository to assess debugging and delivery skills rather than greenfield development. The candidate begins with a runnable FastAPI/SQLite project whose update, delete, validation, and filtering behaviours are incomplete or defective.

## Evaluation flow

1. Give the candidate `candidate/README.md` and a clean copy/branch of the repository.
2. Allow 120 minutes and normal local command-line documentation.
3. Ask for their branch/commits and submission notes.
4. Run `pytest -q`, start the service, and exercise the API using `/docs` or `curl`.
5. Score using `evaluator/scoring.md`; compare behaviour with `evaluator/solutions.md` only after assessing the candidate's work.

## What to look for

- They read existing code and make targeted changes rather than replacing the application.
- They use HTTP status codes and JSON responses correctly.
- SQL is parameterised and database changes are verified.
- Tests prove fixes, including success and error paths.
- Docker and CI commands are understood, not merely copied.
- The webhook is treated as a best-effort external dependency.

## Suggested verification commands

```bash
pytest -q
uvicorn app.main:app --host 127.0.0.1 --port 8000
curl -i http://127.0.0.1:8000/health
curl -i -X POST http://127.0.0.1:8000/projects -H 'content-type: application/json' -d '{"name":"Demo","status":"active"}'
docker compose up --build -d
curl -i http://127.0.0.1:8000/health
docker compose down
```

See `solutions.md` for expected implementation details, `scoring.md` for the rubric, and `reset-guide.md` to restore a clean assessment.
