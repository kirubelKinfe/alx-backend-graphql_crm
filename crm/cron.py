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