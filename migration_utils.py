from sqlalchemy import create_engine
from sqlmodel import Session
from sqlmodel import select

from models import Job, Transaction, Revision, SealedManifest


def shadow_migration(old_db_engine, new_db_engine):
    with Session(old_db_engine) as old_session, Session(new_db_engine) as new_session:
        # Fetch all records from the old database
        old_transactions = old_session.exec(select(Transaction)).all()
        old_jobs = old_session.exec(select(Job)).all()
        old_revisions = old_session.exec(select(Revision)).all()
        old_manifests = old_session.exec(select(SealedManifest)).all()

        # Insert records into the new database
        new_session.bulk_save_objects(old_transactions)
        new_session.bulk_save_objects(old_jobs)
        new_session.bulk_save_objects(old_revisions)
        new_session.bulk_save_objects(old_manifests)
        new_session.commit()


# Example usage
old_engine = create_engine("sqlite:///database.db")
new_engine = create_engine("sqlite:///new_database.db")
shadow_migration(old_engine, new_engine)