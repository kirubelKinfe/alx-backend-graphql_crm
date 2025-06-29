import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

from crm.models import Customer, Product, Order
from decimal import Decimal

def seed_database():
    print("Seeding database...")
    
    # Clear existing data
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()
    
    # Create customers
    customers = [
        Customer.objects.create(
            name="Alice Johnson",
            email="alice@example.com",
            phone="+1234567890"
        ),
        Customer.objects.create(
            name="Bob Smith",
            email="bob@example.com",
            phone="123-456-7890"
        ),
        Customer.objects.create(
            name="Carol Davis",
            email="carol@example.com"
        )
    ]
    print(f"Created {len(customers)} customers")
    
    # Create products
    products = [
        Product.objects.create(
            name="Laptop",
            price=Decimal('999.99'),
            stock=10
        ),
        Product.objects.create(
            name="Mouse",
            price=Decimal('29.99'),
            stock=50
        ),
        Product.objects.create(
            name="Keyboard",
            price=Decimal('79.99'),
            stock=25
        ),
        Product.objects.create(
            name="Monitor",
            price=Decimal('299.99'),
            stock=5
        )
    ]
    print(f"Created {len(products)} products")
    
    # Create orders
    orders = [
        Order.objects.create(
            customer=customers[0],
            total_amount=Decimal('1029.98')
        ),
        Order.objects.create(
            customer=customers[1],
            total_amount=Decimal('109.98')
        ),
        Order.objects.create(
            customer=customers[2],
            total_amount=Decimal('379.98')
        )
    ]
    
    # Add products to orders
    orders[0].products.add(products[0], products[1])  # Laptop + Mouse
    orders[1].products.add(products[1], products[2])  # Mouse + Keyboard
    orders[2].products.add(products[2], products[3])  # Keyboard + Monitor
    
    print(f"Created {len(orders)} orders")
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database() 