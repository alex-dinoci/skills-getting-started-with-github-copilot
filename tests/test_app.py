from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def setup_function():
    # Reset activity participants before each test.
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
    activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    activities["Soccer Team"]["participants"] = ["ryan@mergington.edu", "hannah@mergington.edu"]
    activities["Swimming Club"]["participants"] = ["lisa@mergington.edu", "chris@mergington.edu"]
    activities["Art Club"]["participants"] = ["ava@mergington.edu", "mason@mergington.edu"]
    activities["Drama Club"]["participants"] = ["sophia@mergington.edu", "jack@mergington.edu"]
    activities["Debate Team"]["participants"] = ["grace@mergington.edu", "liam@mergington.edu"]
    activities["Science Olympiad"]["participants"] = ["nina@mergington.edu", "alex@mergington.edu"]


def test_get_activities_returns_all_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity_adds_participant():
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup?email={email}".format(email=email))

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_signup_for_activity_rejects_duplicate():
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant_from_activity():
    email = "daniel@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in activities["Chess Club"]["participants"]


def test_remove_nonexistent_participant_returns_404():
    email = "ghost@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/participants?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
