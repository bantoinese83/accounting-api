from sqlalchemy import create_engine
from sqlmodel import Session, select
from models import Job, Transaction, Revision, SealedManifest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def shadow_migration(old_db_engine, new_db_engine):
    with Session(old_db_engine) as old_session, Session(new_db_engine) as new_session:
        try:
            # Start a transaction
            new_session.begin()

            # Fetch all records from the old database
            old_transactions = old_session.exec(select(Transaction)).all()
            old_jobs = old_session.exec(select(Job)).all()
            old_revisions = old_session.exec(select(Revision)).all()
            old_manifests = old_session.exec(select(SealedManifest)).all()

            # Insert or update records in the new database
            for job in old_jobs:
                if not new_session.get(Job, job.id):
                    new_session.add(job)
                else:
                    new_session.merge(job)

            for transaction in old_transactions:
                if not new_session.get(Transaction, transaction.id):
                    new_session.add(transaction)
                else:
                    new_session.merge(transaction)

            for revision in old_revisions:
                if not new_session.get(Revision, revision.id):
                    new_session.add(revision)
                else:
                    new_session.merge(revision)

            for manifest in old_manifests:
                if not new_session.get(SealedManifest, manifest.id):
                    new_session.add(manifest)
                else:
                    new_session.merge(manifest)

            # Commit the transaction
            new_session.commit()
            logger.info("Migration completed successfully.")
        except Exception as e:
            # Rollback in case of error
            new_session.rollback()
            logger.error(f"Migration failed: {e}")
        finally:
            new_session.close()

# Example usage
old_engine = create_engine("sqlite:///database.db")
new_engine = create_engine("sqlite:///new_database.db")
shadow_migration(old_engine, new_engine)