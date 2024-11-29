from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from sqlmodel import Session

from dependencies import get_session, lifespan
from models import Job, Transaction, Revision, SealedManifest
import services

# FastAPI App Initialization
app = FastAPI(
    lifespan=lifespan,
    title="Accounting API 💼",
    version="0.1.0",
    description="API for accounting operations.",
    docs_url="/"
)


# API Routes
@app.post("/v1/jobs/", response_model=Job, tags=["Jobs 📝"], description="Create a new job 🆕")
async def create_job(job: Job, session: Session = Depends(get_session)):
    return services.create_job(job, session)


@app.get("/v1/jobs/", response_model=List[Job], tags=["Jobs 📝"], description="List all jobs 📋")
async def list_jobs(session: Session = Depends(get_session)):
    return services.list_jobs(session)


@app.post("/v1/transactions/", response_model=Transaction, tags=["Transactions 💸"],
          description="Create a new transaction 🆕")
async def create_transaction(transaction: Transaction, session: Session = Depends(get_session)):
    return services.create_transaction(transaction, session)


@app.get("/v1/transactions/", response_model=List[Transaction], tags=["Transactions 💸"],
         description="List all transactions 📋")
async def list_transactions(session: Session = Depends(get_session)):
    return services.list_transactions(session)


@app.post("/v1/seal-transactions/", response_model=SealedManifest, tags=["Transactions 💸"],
          description="Seal all transactions 🔒")
async def seal_transactions(session: Session = Depends(get_session)):
    return services.seal_transactions(session)


@app.post("/v1/transactions/{transaction_id}/revise/", response_model=Revision, tags=["Transactions 💸"],
          description="Revise a transaction ✏️")
async def revise_transaction(
        transaction_id: int, new_transaction: Transaction, session: Session = Depends(get_session)
):
    return services.revise_transaction(transaction_id, new_transaction, session)


@app.get("/v1/revisions/", response_model=List[Revision], tags=["Revisions 📝"], description="List all revisions 📋")
async def list_revisions(session: Session = Depends(get_session)):
    return services.list_revisions(session)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=120)
