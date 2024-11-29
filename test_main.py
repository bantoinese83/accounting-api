from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from config import engine
from main import app
from models import Transaction

client = TestClient(app)


@pytest.fixture
def sample_job():
    return client.post("/v1/jobs/", json={"name": "Driver", "description": "Experienced driver"}).json()


@pytest.fixture
def sample_transaction(sample_job):
    return client.post("/v1/transactions/", json={
        "job_id": sample_job["id"],
        "account_debit": "DE89370400440532013000",
        "account_credit": "DE89370400440532013001",
        "amount": 100.0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }).json()


@pytest.fixture
def sample_revision(sample_transaction):
    return client.post(f"/v1/transactions/{sample_transaction['id']}/revise/", json={
        "job_id": 1,
        "account_debit": "DE89370400440532013000",
        "account_credit": "DE89370400440532013001",
        "amount": 200.0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }).json()


@pytest.fixture
def no_transactions():
    with Session(engine) as session:
        session.exec(delete(Transaction))
        session.commit()
        yield


def create_sample_sealed_manifest():
    return client.post("/v1/seal-transactions/")


def test_create_job_creates_new_job():
    response = client.post("/v1/jobs/", json={"name": "Driver", "description": "Experienced driver"})
    assert response.status_code == 200
    assert response.json()["name"] == "Driver"


def test_create_job_with_missing_fields():
    response = client.post("/v1/jobs/", json={"name": "Driver"})
    assert response.status_code == 200
    assert response.json()["description"] is None


def test_list_jobs_returns_all_jobs(sample_job):
    response = client.get("/v1/jobs/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_create_transaction_creates_new_transaction(sample_job):
    response = client.post("/v1/transactions/", json={
        "job_id": sample_job["id"],
        "account_debit": "DE89370400440532013000",
        "account_credit": "DE89370400440532013001",
        "amount": 100.0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["job_id"] == sample_job["id"]


def test_create_transaction_with_missing_accounts(sample_job):
    response = client.post("/v1/transactions/", json={
        "job_id": sample_job["id"],
        "amount": 100.0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    assert response.status_code == 400


def test_create_transaction_with_negative_amount(sample_job):
    response = client.post("/v1/transactions/", json={
        "job_id": sample_job["id"],
        "account_debit": "DE89370400440532013000",
        "account_credit": "DE89370400440532013001",
        "amount": -100.0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    assert response.status_code == 400


def test_create_transaction_with_invalid_timestamp(sample_job):
    response = client.post("/v1/transactions/", json={
        "job_id": sample_job["id"],
        "account_debit": "DE89370400440532013000",
        "account_credit": "DE89370400440532013001",
        "amount": 100.0,
        "timestamp": "invalid-timestamp"
    })
    assert response.status_code == 400


def test_list_transactions_returns_all_transactions(sample_transaction):
    response = client.get("/v1/transactions/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_seal_transactions_creates_sealed_manifest(sample_transaction):
    response = create_sample_sealed_manifest()
    assert response.status_code == 200
    response_json = response.json()
    assert response_json != {}
    assert "transaction_count" in response_json
    assert response_json["transaction_count"] > 0
    assert "checksum" in response_json


def test_seal_transactions_with_no_transactions(no_transactions):  # Use the no_transactions fixture
    response = create_sample_sealed_manifest()
    assert response.status_code == 400


def test_revise_transaction_creates_revision(sample_transaction):
    new_transaction_data = {
        "job_id": 1,
        "account_debit": "DE89370400440532013000",
        "account_credit": "DE89370400440532013002",
        "amount": 200.0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    response = client.post(f"/v1/transactions/{sample_transaction['id']}/revise/", json=new_transaction_data)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json != {}
    assert "original_transaction_id" in response_json
    assert response_json["original_transaction_id"] == sample_transaction["id"]
    assert "corrected_transaction_id" in response_json


def test_revise_non_existent_transaction():
    new_transaction_data = {
        "job_id": 1,
        "account_debit": "DE89370400440532013000",
        "account_credit": "DE89370400440532013002",
        "amount": 200.0,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    response = client.post("/v1/transactions/9999/revise/", json=new_transaction_data)
    assert response.status_code == 404


def test_list_revisions_returns_all_revisions(sample_revision):
    response = client.get("/v1/revisions/")
    assert response.status_code == 200
    assert len(response.json()) > 0