def test_health(client):
    assert client.get('/health').json() == {'status': 'ok'}


def test_create_and_get_project(client):
    created = client.post('/projects', json={'name': 'Assessment', 'description': 'Practice API', 'status': 'active'})
    assert created.status_code == 201
    project = created.json()
    assert project['name'] == 'Assessment'
    assert client.get(f"/projects/{project['id']}").json()['status'] == 'active'


def test_unknown_project_is_404(client):
    assert client.get('/projects/999').status_code == 404
