from celery import shared_task
from crm.schema import schema
from datetime import datetime

@shared_task
def generate_crm_report():
    query = """
        query {
            report {
                totalCustomers
                totalOrders
                totalRevenue
            }
        }
    """
    result = schema.execute(query)
    if result.errors:
        with open("/tmp/crm_report_log.txt", "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp} - Error executing query: {result.errors}\n")
        return
    
    data = result.data["report"]
    total_customers = data["totalCustomers"]
    total_orders = data["totalOrders"]
    total_revenue = data["totalRevenue"]
    
    with open("/tmp/crm_report_log.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n")