import hashlib
import json
from datetime import datetime, timezone
from typing import Sequence

from fastapi import HTTPException
from kafka import KafkaProducer
from sqlmodel import select, Session

from models import Job, Transaction, Revision, SealedManifest

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def create_job(job: Job, session: Session) -> Job:
    session.add(job)
    session.commit()
    session.refresh(job)
    return job


def list_jobs(session: Session) -> Sequence[Job]:
    return session.exec(select(Job)).all()


def create_transaction(transaction: Transaction, session: Session) -> Transaction:
    # Validate debit and credit accounts
    if not transaction.account_debit or not transaction.account_credit:
        raise HTTPException(status_code=400, detail="Both debit and credit accounts are required.")
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Transaction amount must be positive.")

    # Ensure timestamp is a datetime object
    if isinstance(transaction.timestamp, str):
        try:
            transaction.timestamp = datetime.fromisoformat(transaction.timestamp.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid timestamp format.")

    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    # Convert datetime to string for JSON serialization
    transaction_data = transaction.model_dump()
    transaction_data['timestamp'] = transaction_data['timestamp'].isoformat()

    # Publish transaction to Kafka
    producer.send("transactions", transaction_data)
    return transaction


def list_transactions(session: Session) -> Sequence[Transaction]:
    return session.exec(select(Transaction)).all()


def seal_transactions(session: Session) -> SealedManifest:
    # Fetch all unsealed transactions
    transactions = session.exec(select(Transaction)).all()
    if not transactions:
        raise HTTPException(status_code=400, detail="No transactions to seal.")

    # Generate checksum
    transactions_data = "".join([str(txn.id) for txn in transactions])
    checksum = hashlib.sha256(transactions_data.encode()).hexdigest()

    # Create sealed manifest
    manifest = SealedManifest(transaction_count=len(transactions), checksum=checksum)
    session.add(manifest)
    session.commit()
    session.refresh(manifest)
    return manifest


def revise_transaction(transaction_id: int, new_transaction: Transaction, session: Session) -> Revision:
    # Find original transaction
    original_transaction = session.get(Transaction, transaction_id)
    if not original_transaction:
        raise HTTPException(status_code=404, detail="Original transaction not found.")

    # Ensure timestamp is a datetime object
    if isinstance(new_transaction.timestamp, str):
        new_transaction.timestamp = datetime.fromisoformat(new_transaction.timestamp.replace("Z", "+00:00"))

    # Save the new transaction
    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)

    # Log the revision
    revision = Revision(
        original_transaction_id=original_transaction.id,
        corrected_transaction_id=new_transaction.id,
        reason="Correction",
        timestamp=datetime.now(timezone.utc)
    )
    session.add(revision)
    session.commit()
    session.refresh(revision)
    return revision


def list_revisions(session: Session) -> Sequence[Revision]:
    return session.exec(select(Revision)).all()
