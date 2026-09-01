# Fresher DevOps Engineer Practical Assessment

**Timebox:** 120 minutes. Work in this repository and commit your work to a branch.

## Starting the application

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the app with `uvicorn app.main:app --reload`.
4. Open `http://localhost:8000` and API documentation at `http://localhost:8000/docs`.
5. Run the existing checks with `pytest -q`.

## Tasks

### 1. Programming and debugging (25 points)

1. Investigate and correct the project update behaviour. A successful update must persist to SQLite, return the updated JSON document, and return JSON `404` for a nonexistent ID.
2. Implement project deletion. It must delete an existing project, return `204 No Content`, and return `404` when the project does not exist.
3. Reject project names that are empty after leading/trailing whitespace is removed. Return a useful `4xx` JSON validation response.
4. Add focused automated tests for the behaviours you change.

### 2. REST API and database (20 points)

1. Make `GET /projects?status_filter=active` return only projects with that valid status.
2. Invalid filter values must return a clear `4xx` response instead of silently returning an unexpected result.
3. Use parameterised SQL and retain the existing JSON response fields.
4. Use SQLite directly to inspect the `projects` table. Add a short SQL query and its output to your commit message or submission notes.

### 3. Git (10 points)

1. Create a feature branch.
2. Make at least two meaningful, well-described commits.
3. Show the final `git log --oneline -5` and `git diff`/merge-request summary in your submission notes.

### 4. Linux and Docker (15 points)

1. Use Linux commands to identify the process listening on port 8000 and to inspect the application logs.
2. Build and run the supplied Docker image or Compose service.
3. Verify `/health` from the host using `curl`.
4. Ensure SQLite data survives a container restart using the configured volume.
5. Add the commands and observed output to submission notes.

### 5. GitLab CI/CD (15 points)

1. Read `.gitlab-ci.yml` and explain the purpose of its stages/jobs in submission notes.
2. Make the pipeline run the automated tests and build the image.
3. Improve it so a failed test prevents the image build.
4. Add one useful CI improvement, such as dependency caching, a test report, or a clear image tag.

### 6. Webhook integration and troubleshooting (10 points)

1. Configure `WEBHOOK_URL` to a test endpoint you control.
2. Create a project and verify that a JSON `project.created` event is sent.
3. Demonstrate that an unavailable webhook does not stop the project from being created.
4. Diagnose one issue you encounter using logs, HTTP status codes, or Docker/GitLab job output; document the symptom, command used, cause, and fix.

### 7. Problem solving (5 points)

Keep the changes small, readable, and appropriate for the timebox. Include concise submission notes describing assumptions and trade-offs.
