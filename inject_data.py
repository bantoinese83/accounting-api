import hashlib
import logging
from datetime import datetime, timezone

from faker import Faker
from sqlmodel import Session
from tqdm import tqdm

from config import engine
from models import Job, Transaction, Revision, SealedManifest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker()


def inject_data():
    with Session(engine) as session:
        # Create sample jobs (drivers)
        jobs = []
        logger.info("Creating sample drivers...")
        for _ in tqdm(range(1000), desc="Drivers"):
            job = Job(name=fake.name(), description=f"Driver with {fake.random_int(min=1, max=20)} years of experience.")
            jobs.append(job)
        session.add_all(jobs)
        session.commit()
        for job in jobs:
            session.refresh(job)  # Refresh to get IDs
        logger.info("Sample drivers created.")

        job_ids = [job.id for job in jobs]

        # Create sample transactions (rides) and revisions
        transactions = []
        revisions = []
        logger.info("Creating sample rides and revisions...")
        for _ in tqdm(range(1000), desc="Rides and Revisions"):
            transaction = Transaction(
                job_id=fake.random_element(elements=job_ids),
                account_debit=fake.iban(),
                account_credit=fake.iban(),
                amount=round(fake.random_number(digits=2) + fake.random.random(), 2),  # Ride fare
                timestamp=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc),
            )
            session.add(transaction)
            session.flush()  # Crucial: Get the transaction ID
            transactions.append(transaction)

            if fake.boolean(chance_of_getting_true=10):  # 10% chance of revision
                corrected_transaction = fake.random_element(elements=transactions)
                revision = Revision(
                    original_transaction_id=transaction.id,
                    corrected_transaction_id=corrected_transaction.id,
                    reason=fake.sentence(),
                    timestamp=datetime.now(timezone.utc),
                )
                revisions.append(revision)

        session.add_all(revisions)
        session.commit()
        logger.info("Sample rides and revisions created.")

        # Create sample sealed manifest
        logger.info("Creating sample sealed manifest...")
        transactions_data = "".join([str(txn.id) for txn in transactions])
        checksum = hashlib.sha256(transactions_data.encode()).hexdigest()
        manifest = SealedManifest(
            transaction_count=len(transactions),
            checksum=checksum,
            sealed_at=datetime.now(timezone.utc),
        )
        session.add(manifest)
        session.commit()
        logger.info("Sample sealed manifest created.")


if __name__ == "__main__":
    inject_data()