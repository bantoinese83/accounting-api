# Accounting API 💼

This robust API, built with FastAPI, provides comprehensive endpoints for managing accounting data, including jobs,
transactions, revisions, and sealed manifests. It leverages a modern tech stack including SQLModel, SQLite, Kafka, and
robust testing with Pytest and Locust.

## ✨ Key Features

* **Job Management:** Create, retrieve, and manage job records.
* **Transaction Handling:** Create, list, revise, and seal financial transactions.
* **Revision Tracking:** Maintain a complete audit trail of transaction revisions with detailed reasons.
* **Data Integrity:** Securely seal transactions with checksum verification.
* **Asynchronous Communication:** Utilizes Kafka for reliable and scalable event streaming.
* **Thorough Testing:**  Includes comprehensive test suites using Pytest and performance testing with Locust.

## 🚀 Technologies

<img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
<img src="https://img.shields.io/badge/FastAPI-0.115.5-green.svg" alt="FastAPI ">  
<img src="https://img.shields.io/badge/SQLModel-latest-orange.svg" alt="SQLModel">
<img src="https://img.shields.io/badge/SQLite-latest-blueviolet.svg" alt="SQLite">
<img src="https://img.shields.io/badge/Kafka-latest-red.svg" alt="Kafka">
<img src="https://img.shields.io/badge/Pytest-latest-brightgreen.svg" alt="Pytest">
<img src="https://img.shields.io/badge/Locust-latest-yellow.svg" alt="Locust">

## 🛠️ Installation

1. **Prerequisites:**
    * Python 3.8+
    * Kafka
    * Zookeeper (for Kafka)

2. **Clone:**

```bash
   git clone https://github.com/bantoinese83/accounting-api.git
   cd accounting-api
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

### Set Environment Variables

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Start Zookeeper and Kafka

```sh
./start_services.sh
```

### Run the Application

```sh
uvicorn app.main:app --reload
```

### Run Tests

```sh
pytest
```

### Run Locust

```sh
locust -f locustfile.py
```

## Configuration

Configuration settings are managed in `config.py`. The default database is SQLite, but you can change the `DATABASE_URL`
environment variable to use a different database.

## API Endpoints

| **Endpoint**                                | **Method** | **Description**                       |
|---------------------------------------------|------------|---------------------------------------|
| `/v1/jobs/`                                 | `POST`     | Create a new job record.              |
| `/v1/jobs/`                                 | `GET`      | List all job records.                 |
| `/v1/transactions/`                         | `POST`     | Create a new transaction.             |
| `/v1/transactions/`                         | `GET`      | List all transactions.                |
| `/v1/transactions/{transaction_id}/revise/` | `POST`     | Revise an existing transaction.       |
| `/v1/seal-transactions/`                    | `POST`     | Seal transactions for data integrity. |
| `/v1/revisions/`                            | `GET`      | List all transaction revisions.       |

## 📊 GitHub Profile Insights

### 🚀 My GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=bantoinese83&show_icons=true&theme=radical)

---

### 💻 Top Languages

![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=bantoinese83&layout=compact&theme=radical)

---

### 🌟 Contribution Graph

![Contribution Graph](https://github-readme-activity-graph.vercel.app/graph?username=bantoinese83&theme=radical)

---

### 🏆 GitHub Achievements

![GitHub Achievements](https://github-profile-trophy.vercel.app/?username=bantoinese83&theme=radical)

---

### 🐙 Streak Stats

![GitHub Streak Stats](https://streak-stats.demolab.com?user=bantoinese83&theme=radical&date_format=M%20j%5B%2C%20Y%5D)

---

Feel free to explore my repositories and projects to see what I've been working on. 🚀
