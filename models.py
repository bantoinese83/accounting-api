from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Relationship
from sqlmodel import SQLModel, Field, Index


class Job(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    transactions: List["Transaction"] = Relationship(back_populates="job")

    __table_args__ = (
        Index("idx_job_name", "name"),
    )

class Transaction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    job_id: int = Field(foreign_key="job.id")
    account_debit: str
    account_credit: str
    amount: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    job: Job = Relationship(back_populates="transactions")

    __table_args__ = (
        Index("idx_transaction_job_id", "job_id"),
        Index("idx_transaction_timestamp", "timestamp"),
    )

class Revision(SQLModel, table=True):
    id: int = Field(primary_key=True)
    original_transaction_id: int = Field(foreign_key="transaction.id")
    corrected_transaction_id: int = Field(foreign_key="transaction.id")
    reason: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index("idx_revision_original_transaction_id", "original_transaction_id"),
        Index("idx_revision_corrected_transaction_id", "corrected_transaction_id"),
    )

class SealedManifest(SQLModel, table=True):
    id: int = Field(primary_key=True)
    sealed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    transaction_count: int
    checksum: str

    __table_args__ = (
        Index("idx_sealed_manifest_sealed_at", "sealed_at"),
    )
