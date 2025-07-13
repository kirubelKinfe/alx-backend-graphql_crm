# CRM Project Scheduled Tasks & Automation

## Setup Instructions

### 1. Install Dependencies

```
pip install -r requirements.txt
```

### 2. Install and Start Redis

- Download and install Redis from https://redis.io/download
- Start the Redis server:
  ```
  redis-server
  ```

### 3. Run Django Migrations

```
python manage.py migrate
```

### 4. Start Django Server

```
python manage.py runserver
```

### 5. Start Celery Worker

```
celery -A crm worker -l info
```

### 6. Start Celery Beat Scheduler

```
celery -A crm beat -l info
```

### 7. Verify Logs

- **CRM Report Log:** `/tmp/crm_report_log.txt`
- **Order Reminders Log:** `/tmp/order_reminders_log.txt`
- **Customer Cleanup Log:** `/tmp/customer_cleanup_log.txt`
- **Low Stock Updates Log:** `/tmp/low_stock_updates_log.txt`
- **Heartbeat Log:** `/tmp/crm_heartbeat_log.txt`

---

## Crontab Setup

- Use the provided crontab files in `crm/cron_jobs/` to schedule shell and Python scripts as required.
- Make sure all scripts are executable (`chmod +x script.sh`).