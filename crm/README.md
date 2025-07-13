# CRM GraphQL Project Setup

This project implements a CRM system with GraphQL and Celery for automated tasks.

## Prerequisites

- Python 3.x
- Redis server
- Django project (`alx-backend-graphql_crm`)

## Installation

1. **Install Dependencies**:
   Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Redis**:
   - On Ubuntu:
     ```bash
     sudo apt-get install redis-server
     ```
   - On macOS:
     ```bash
     brew install redis
     ```
   - Start Redis:
     ```bash
     redis-server
     ```

3. **Run Migrations**:
   Apply database migrations:
   ```bash
   python manage.py migrate
   ```

## Running Celery

1. **Start Celery Worker**:
   Run the Celery worker to process tasks:
   ```bash
   celery -A crm worker -l info
   ```

2. **Start Celery Beat**:
   Run Celery Beat to schedule tasks:
   ```bash
   celery -A crm beat -l info
   ```

## Verifying Logs

- Check the CRM report logs:
  ```bash
  cat /tmp/crm_report_log.txt
  ```
  Expected output format:
  ```
  2025-07-14 06:00:00 - Report: X customers, Y orders, Z revenue
  ```

## Notes

- Ensure Redis is running on `redis://localhost:6379/0`.
- The weekly CRM report runs every Monday at 6:00 AM.