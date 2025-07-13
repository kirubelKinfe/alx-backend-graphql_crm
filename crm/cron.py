import requests
from datetime import datetime

LOG_FILE = '/tmp/low_stock_updates_log.txt'
GRAPHQL_URL = 'http://127.0.0.1:8000/graphql'

MUTATION = '''
mutation {
  updateLowStockProducts {
    updatedProducts {
      name
      stock
    }
    message
  }
}
'''

def log_crm_heartbeat():
    now = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{now} CRM is alive\n")
    # Optionally, check GraphQL hello
    try:
        hello_query = '{ hello }'
        resp = requests.post(GRAPHQL_URL, json={'query': hello_query})
        if resp.status_code == 200 and resp.json().get('data', {}).get('hello'):
            pass  # Endpoint is responsive
    except Exception:
        pass

def update_low_stock():
    try:
        response = requests.post(GRAPHQL_URL, json={'query': MUTATION})
        data = response.json()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a') as f:
            f.write(f"\n[{now}] Low Stock Update:\n")
            if 'data' in data and data['data']['updateLowStockProducts']:
                msg = data['data']['updateLowStockProducts']['message']
                f.write(msg + '\n')
                for prod in data['data']['updateLowStockProducts']['updatedProducts']:
                    f.write(f"  - {prod['name']}: {prod['stock']}\n")
            else:
                f.write(f"No products updated or error: {data}\n")
    except Exception as e:
        with open(LOG_FILE, 'a') as f:
            f.write(f"\n[{now}] Exception: {e}\n")