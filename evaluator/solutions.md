# Expected Solutions and Common Mistakes

## Programming (25)

**Expected:** `PUT /projects/{id}` finds the project, merges only supplied model fields, trims/validates a supplied name, executes a parameterised `UPDATE`, reads back the row, and returns it. `DELETE` checks the affected row count and returns `204` only after deletion. Blank/whitespace names are rejected with a 422 or 400 JSON response. Tests cover update persistence, missing update/delete, delete persistence, and blank names.

**Look for:** updates visible to a fresh request; no false `204`; appropriate status and JSON body; concise tests.

**Common mistakes:** mutating an in-memory dict only, using string interpolation in SQL, accepting `"   "`, returning a JSON body with 204, or testing only happy paths.

## API and database (20)

**Expected:** list endpoint accepts only `planned`, `active`, or `completed`, uses `WHERE status = ?` when provided, and returns all rows without a filter. Invalid values return 400/422 with a clear detail. Candidate demonstrates a SQLite query such as `sqlite3 data/projects.db 'SELECT id,name,status FROM projects;'`.

**Look for:** stable response schema, parameter binding, valid HTTP response semantics, and an actual database inspection.

**Common mistakes:** filtering in Python unnecessarily, passing invalid values silently, SQL injection-prone f-strings, or changing field names without reason.

## Git (10)

**Expected:** feature branch, two or more logical commits, clear imperative messages, and concise notes with log/diff summary.

**Common mistakes:** one giant commit, committing generated database/venv files, or vague messages such as `changes`.

## Docker and Linux (15)

**Expected:** image builds, Compose starts on port 8000, health works from host, named volume preserves `/data/projects.db`, and candidate can use commands such as `ss -ltnp`, `ps`, `docker compose logs`, and `curl`.

**Look for:** command output matches claimed diagnosis; volume path agrees with `DATABASE_PATH`.

**Common mistakes:** relying on a bind mount that does not persist as claimed, publishing the wrong port, or checking a container-only health URL from host.

## GitLab CI/CD (15)

**Expected:** `test` runs before `build`; a failed test prevents build by stage dependency; jobs install dependencies/build the Docker image. Credit an appropriate small improvement such as pip cache, JUnit report, or sensible image tag.

**Look for:** valid YAML, correct indentation, noninteractive scripts, and candidate can explain dind/image build constraints.

**Common mistakes:** placing build before test, invalid YAML, assuming an image survives between jobs without pushing/saving it, or a cache that caches only a virtualenv from another image.

## Integration and troubleshooting (10)

**Expected:** with `WEBHOOK_URL`, a create emits JSON containing `event: project.created` and the project. A failed webhook is logged or handled without rolling back local creation. Notes document a reproducible symptom, diagnostic command/output, cause, and corrective change.

**Common mistakes:** making project creation fail on timeout, sending form data rather than JSON, no timeout, exposing webhook secrets, or claiming a diagnosis without evidence.

## Problem solving (5)

**Expected:** modest scope, readable code, tests, assumptions/trade-offs, and sensible time management.
