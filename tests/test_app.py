import pytest
from app import create_app
 
 
@pytest.fixture
def client(tmp_path):
    database = tmp_path / "test_aceest.db"
    app = create_app({"TESTING": True, "DATABASE": str(database)})
    with app.test_client() as test_client:
        yield test_client
 
 
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest FUNCTIONAL FITNESS" in response.data
 
 
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "running"
 
 
@pytest.mark.parametrize("program", ["Fat Loss", "Muscle Gain", "Beginner"])
def test_valid_program(client, program):
    response = client.get("/program/" + program.replace(" ", "%20"))
    assert response.status_code == 200
    assert response.json["name"] == program
    assert response.json["workouts"]
    assert response.json["nutrition"]
 
 
def test_unknown_program(client):
    assert client.get("/program/Unknown").status_code == 404
 
 
def test_register_client(client):
    response = client.post("/clients", json={"name": "Alex"})
    assert response.status_code == 201
    assert response.json["client_id"] == 1
 
 
def test_empty_client_name(client):
    assert client.post("/clients", json={"name": " "}).status_code == 400
 
 
def test_missing_json(client):
    assert client.post("/clients", json=None).status_code == 400
 
 
def test_duplicate_client(client):
    client.post("/clients", json={"name": "Alex"})
    response = client.post("/clients", json={"name": "alex"})
    assert response.status_code == 409
 
 
def test_list_clients(client):
    client.post("/clients", json={"name": "Alex"})
    response = client.get("/clients")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Alex"
 
 
def test_add_workout(client):
    registered = client.post("/clients", json={"name": "Alex"})
    response = client.post("/workouts", json={
        "client_id": registered.json["client_id"],
        "workout_type": "Cardio",
        "duration_min": 30
    })
    assert response.status_code == 201
 
 
@pytest.mark.parametrize("duration", [0, -1, "30", True, None])
def test_invalid_workout_duration(client, duration):
    client.post("/clients", json={"name": "Alex"})
    response = client.post("/workouts", json={
        "client_id": 1, "workout_type": "Cardio", "duration_min": duration
    })
    assert response.status_code == 400
 
 
def test_workout_for_missing_client(client):
    response = client.post("/workouts", json={
        "client_id": 999, "workout_type": "Cardio", "duration_min": 30
    })
    assert response.status_code == 404
 
 
def test_list_workouts(client):
    client.post("/clients", json={"name": "Alex"})
    client.post("/workouts", json={
        "client_id": 1, "workout_type": "Yoga", "duration_min": 45
    })
    response = client.get("/workouts")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["workout_type"] == "Yoga"
 
 
def test_update_membership(client):
    client.post("/clients", json={"name": "Alex"})
    response = client.patch("/clients/1/membership", json={"status": "Inactive"})
    assert response.status_code == 200
    assert response.json["status"] == "Inactive"
    assert client.get("/clients").json[0]["membership_status"] == "Inactive"
 
 
def test_invalid_membership_status(client):
    client.post("/clients", json={"name": "Alex"})
    response = client.patch("/clients/1/membership", json={"status": "Unknown"})
    assert response.status_code == 400
 
