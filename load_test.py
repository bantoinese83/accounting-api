from locust import HttpUser, task, between

class AccountingApiUser(HttpUser):
    wait_time = between(1, 5)
    connection_timeout = 120.0
    network_timeout = 120.0

    @task
    def create_job(self):
        self.client.post("/v1/jobs/create", json={
            "name": "Software Developer",
            "description": "Develops software applications."
        })

    @task
    def list_jobs(self):
        self.client.get("/v1/jobs/list")

    @task
    def create_transaction(self):
        self.client.post("/v1/transactions/create", json={
            "job_id": 1,
            "account_debit": "DE89370400440532013000",
            "account_credit": "DE89370400440532013001",
            "amount": 1000.0,
            "timestamp": "2023-10-10T10:00:00Z"
        })

    @task
    def list_transactions(self):
        self.client.get("/v1/transactions/list")

    @task
    def seal_transactions(self):
        self.client.post("/v1/transactions/seal")

    @task
    def revise_transaction(self):
        self.client.post("/v1/transactions/1/revise", json={
            "job_id": 1,
            "account_debit": "DE89370400440532013000",
            "account_credit": "DE89370400440532013001",
            "amount": 2000.0,
            "timestamp": "2023-10-10T10:00:00Z"
        })

    @task
    def list_revisions(self):
        self.client.get("/v1/revisions/list")