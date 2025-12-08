import pytest
from fastapi.testclient import TestClient
import os
import sys
from pymongo import MongoClient


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from main import app

client = TestClient(app)

# ---- Helpers ----

def reset_database():
    """Completely deletes and recreates the DB."""
    mongo = MongoClient("mongodb+srv://hamalvolunteers:v96o90K2WbJ@hamalcluster.p2wonhv.mongodb.net/?appName=HamalCluster")
    mongo.drop_database("HamalCluster")
    mongo.close()

def send(action, payload=None):
    """Utility to send API requests using your exact protocol."""
    body = {
        "action": action,
        "payload": payload or {}
    }
    response = client.post("/api", json=body)
    assert response.status_code == 200
    return response.json()


# ---- Test Suite ----

@pytest.fixture(scope="session", autouse=True)
def setup_env():
    """Runs once before test suite: reset DB."""
    reset_database()
    yield
    reset_database()


def test_01_add_user():
    res = send("addUser", {
        "id": 1,
        "name": "Alice",
        "filters": ["music", "sports"]
    })

    assert res["status"] == "ok"
    assert res["data"] is True


def test_02_get_user():
    res = send("getUserById", {"id": 1})

    assert res["status"] == "ok"
    assert res["data"]["name"] == "Alice"
    assert res["data"]["id"] == 1


def test_03_add_filter():
    res = send("addFilterById", {"id": 1, "filter": "volunteer"})
    assert res["status"] == "ok"

    res = send("getFiltersByUserId", {"id": 1})
    assert set(res["data"]) == {"music", "sports", "volunteer"}


def test_04_remove_filter():
    res = send("removeFilterById", {"id": 1, "filter": "sports"})
    assert res["status"] == "ok"

    res = send("getFiltersByUserId", {"id": 1})
    assert set(res["data"]) == {"music", "volunteer"}


def test_05_add_event():
    res = send("addEvent", {
        "eventId": 10,
        "name": "Beach Cleanup",
        "capacity": 3,
        "info": "Help clean the beach",
        "filters": ["volunteer"],
        "location": "Beach",
        "date": "2024-06-01",
        "duration": "3 hours"
    })
    assert res["status"] == "ok"
    mongo = MongoClient("mongodb+srv://hamalvolunteers:v96o90K2WbJ@hamalcluster.p2wonhv.mongodb.net/?appName=HamalCluster")
    event = mongo.HamalCluster.events.find_one({"eventId": 10})
    mongo.close()

    assert event is not None
    assert event["name"] == "Beach Cleanup"
    assert event["capacity"] == 3
    assert event["info"] == "Help clean the beach"
    assert event["filters"] == ["volunteer"]
    assert event["location"] == "Beach"
    assert event["date"] == "2024-06-01"
    assert event["duration"] == "3 hours"

def test_06_get_event_by_filters():
    res = send("getEventByFilters", {"filters": ["volunteer"]})
    assert res["status"] == "ok"
    assert len(res["data"]) == 1
    assert res["data"][0]["eventId"] == 10


def test_07_sign_user_to_event():
    res = send("signUserToEvent", {"id": 1, "eventId": 10})
    assert res["status"] == "ok"

    # Ensure user appears in the event participants
    mongo = MongoClient("mongodb+srv://hamalvolunteers:v96o90K2WbJ@hamalcluster.p2wonhv.mongodb.net/?appName=HamalCluster")
    event = mongo.HamalCluster.events.find_one({"eventId": 10})
    mongo.close()

    assert 1 in event["people"]


def test_08_remove_user_from_event():
    res = send("removeUserFromEvent", {"id": 1, "eventId": 10})
    assert res["status"] == "ok"

    mongo = MongoClient("mongodb+srv://hamalvolunteers:v96o90K2WbJ@hamalcluster.p2wonhv.mongodb.net/?appName=HamalCluster")
    event = mongo.HamalCluster.events.find_one({"eventId": 10})
    mongo.close()

    assert 1 not in event["people"]

def test_09_add_existing_user():
    send("addUser", {"id": 2, "name": "Bob", "filters": ["sports"]})
    res = send("addUser", {"id": 2, "name": "Bob", "filters": ["sports"]})
    assert res["status"] == "ok"
    assert res["data"] is False

def test_10_add_existing_filter():
    send("addUser", {"id": 3, "name": "Charlie", "filters": ["music"]})
    send("addFilterById", {"id": 3, "filter": "music"})  # first add
    res = send("addFilterById", {"id": 3, "filter": "music"})  # duplicate
    assert res["status"] == "ok"
    assert res["data"] is False

def test_11_remove_nonexistent_filter():
    send("addUser", {"id": 4, "name": "Diana", "filters": ["volunteer"]})
    res = send("removeFilterById", {"id": 4, "filter": "nonexistent"})
    assert res["status"] == "ok"
    assert res["data"] is False

def test_12_get_filters_no_user():
    res = send("getFiltersByUserId", {"id": 999})
    assert res["status"] == "ok"
    assert res["data"] == []

def test_13_sign_user_to_full_event():
    send("addUser", {"id": 5, "name": "Eve", "filters": ["volunteer"]})
    send("addEvent", {"eventId": 20, "name": "Full Event", "capacity": 1, "info": "", "filters": ["volunteer"]})
    send("signUserToEvent", {"id": 5, "eventId": 20})  # fills the event
    res = send("signUserToEvent", {"id": 6, "eventId": 20})
    assert res["status"] == "ok"
    assert res["data"] is False

def test_14_remove_user_not_signed():
    send("addUser", {"id": 7, "name": "Frank", "filters": ["volunteer"]})
    send("addEvent", {"eventId": 21, "name": "Empty Event", "capacity": 5, "info": "", "filters": ["volunteer"]})
    res = send("removeUserFromEvent", {"id": 7, "eventId": 21})
    assert res["status"] == "ok"
    assert res["data"] is False

def test_15_get_event_no_matching_filters():
    send("addEvent", {"eventId": 22, "name": "Fun Event", "capacity": 10, "info": "", "filters": ["fun"]})
    res = send("getEventByFilters", {"filters": ["badFilter"]})
    assert res["status"] == "ok"
    assert res["data"] == []

def test_16_get_event_by_id():
    send("addEvent", {"eventId": 30, "name": "Unique Event", "capacity": 15, "info": "Special event", "filters": ["unique"]})
    res = send("getEventById", {"eventId": 30})
    assert res["status"] == "ok"
    assert res["data"]["name"] == "Unique Event"
    assert res["data"]["capacity"] == 15
    assert res["data"]["info"] == "Special event"
    assert res["data"]["filters"] == ["unique"]
