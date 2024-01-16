import pytest
import json
import requests
import subprocess

from src.misc import read_json


URL = "http://127.0.0.1:5000/"


@pytest.fixture()
def start_requests():
    return read_json("tests/resources/start.jsonl")

@pytest.fixture()
def stop_requests():
    return read_json("tests/resources/stop.jsonl")

@pytest.fixture()
def retrieve_requests():
    return read_json("tests/resources/retrieve.jsonl")

def test_liveness():
    response = requests.get(f"{URL}/health/liveness")
    assert response.status_code == 200
    
def test_start_activity(start_requests):
    for request in start_requests:
        response = requests.post(f"{URL}/start", json=request)
        assert response.status_code == 200
        
def test_stop_activity(stop_requests):
    for request in stop_requests:
        response = requests.post(f"{URL}/stop", json=request)
        assert response.status_code == 200
        
def test_retrieve_activity(retrieve_requests):
    for request in retrieve_requests:
        response = requests.get(f"{URL}/retrieve", json=request)
        assert response.status_code == 200
        assert len(response.json()) > 0