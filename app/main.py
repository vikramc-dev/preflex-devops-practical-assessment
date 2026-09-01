import json
import os
import urllib.request
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.database import get_connection, initialise_database

VALID_STATUSES = ("planned", "active", "completed")


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    status: Literal["planned", "active", "completed"] = "planned"


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    status: Literal["planned", "active", "completed"] | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialise_database()
    yield


app = FastAPI(title="Project Management Assessment", lifespan=lifespan)


def serialise_project(row):
    return dict(row) if row else None


def send_webhook(project: dict) -> None:
    """Send a best-effort project.created event when WEBHOOK_URL is configured."""
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        return
    payload = json.dumps({"event": "project.created", "project": project}).encode()
    request = urllib.request.Request(webhook_url, data=payload, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(request, timeout=2)
    except OSError:
        # A webhook outage must not prevent the local project from being created.
        pass


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse("app/static.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/projects")
def list_projects(status_filter: str | None = None):
    """List projects. The optional status_filter is intentionally not wired in yet."""
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM projects ORDER BY id").fetchall()
    return [serialise_project(row) for row in rows]


@app.post("/projects", status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate):
    # Intentional assessment issue: whitespace-only names pass validation.
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO projects (name, description, status) VALUES (?, ?, ?)",
            (project.name, project.description, project.status),
        )
        row = connection.execute("SELECT * FROM projects WHERE id = ?", (cursor.lastrowid,)).fetchone()
    result = serialise_project(row)
    send_webhook(result)
    return result


@app.get("/projects/{project_id}")
def get_project(project_id: int):
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    return serialise_project(row)


@app.put("/projects/{project_id}")
def update_project(project_id: int, project: ProjectUpdate):
    """Replace supplied fields. Candidate task: make this endpoint work correctly."""
    with get_connection() as connection:
        existing = connection.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Project not found")
        # Intentional bug: update is calculated but never persisted.
        updated = dict(existing)
        updated.update({key: value for key, value in project.model_dump().items() if value is not None})
    return updated


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    """Candidate task: implement project deletion and correct 404 behavior."""
    return Response(status_code=status.HTTP_204_NO_CONTENT)
