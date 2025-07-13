#!/usr/bin/env python3

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

# Setup GraphQL transport
transport = RequestsHTTPTransport(
    url='http://localhost:8000/graphql',
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# GraphQL query for pending orders in the last 7 days
query = gql(f"""
query {{
  orders(orderDate_Gte: "{seven_days_ago}") {{
    id
    customer {{
      email
    }}
  }}
}}
""")

try:
    result = client.execute(query)
    orders = result.get('orders', [])

    with open('/tmp/order_reminders_log.txt', 'a') as log_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for order in orders:
            log_file.write(f"{timestamp} - Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n")

    print("Order reminders processed!")
except Exception as e:
    print(f"Failed to process order reminders: {e}")
