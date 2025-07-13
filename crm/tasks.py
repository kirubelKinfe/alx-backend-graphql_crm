from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    query = '''
    { report { totalCustomers totalOrders totalRevenue } }
    '''
    response = requests.post('http://127.0.0.1:8000/graphql', json={'query': query})
    data = response.json().get('data', {}).get('report', {})
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('/tmp/crm_report_log.txt', 'a') as f:
        f.write(f"{now} - Report: {data.get('totalCustomers', 0)} customers, {data.get('totalOrders', 0)} orders, {data.get('totalRevenue', 0.0)} revenue\n")