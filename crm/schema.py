import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.db import transaction
import re
from graphene import InputObjectType, Field, List, String, Int, Float, ID, Mutation as GrapheneMutation
from graphene_django.filter import DjangoFilterConnectionField
from .filters import CustomerFilter, ProductFilter, OrderFilter

class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)
        fields = ("id", "name", "email", "phone", "created_at")

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)
        fields = ("id", "name", "price", "stock")

class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)
        fields = ("id", "customer", "products", "total_amount", "order_date")

class Query(graphene.ObjectType):
    hello = graphene.String()
    all_customers = DjangoFilterConnectionField(CustomerNode, order_by=graphene.List(of_type=graphene.String))
    all_products = DjangoFilterConnectionField(ProductNode, order_by=graphene.List(of_type=graphene.String))
    all_orders = DjangoFilterConnectionField(OrderNode, order_by=graphene.List(of_type=graphene.String))

    def resolve_hello(root, info):
        return "Hello, GraphQL!"

    def resolve_all_customers(root, info, **kwargs):
        qs = Customer.objects.all()
        order_by = kwargs.get('order_by')
        if order_by:
            qs = qs.order_by(*order_by)
        return qs

    def resolve_all_products(root, info, **kwargs):
        qs = Product.objects.all()
        order_by = kwargs.get('order_by')
        if order_by:
            qs = qs.order_by(*order_by)
        return qs

    def resolve_all_orders(root, info, **kwargs):
        qs = Order.objects.all()
        order_by = kwargs.get('order_by')
        if order_by:
            qs = qs.order_by(*order_by)
        return qs

class CreateCustomerInput(InputObjectType):
    name = String(required=True)
    email = String(required=True)
    phone = String()

class CreateCustomer(GrapheneMutation):
    class Arguments:
        input = CreateCustomerInput(required=True)
    customer = Field(CustomerNode)
    message = String()
    errors = List(String)

    @staticmethod
    def validate_phone(phone):
        if not phone:
            return True
        pattern = r'^(\\+\\d{10,15}|\\d{3}-\\d{3}-\\d{4})$'
        return re.match(pattern, phone)

    @classmethod
    def mutate(cls, root, info, input):
        errors = []
        if Customer.objects.filter(email=input.email).exists():
            errors.append("Email already exists")
        if not cls.validate_phone(input.phone):
            errors.append("Invalid phone format")
        if errors:
            return CreateCustomer(errors=errors)
        customer = Customer.objects.create(
            name=input.name,
            email=input.email,
            phone=input.phone
        )
        return CreateCustomer(customer=customer, message="Customer created successfully")

class BulkCreateCustomers(GrapheneMutation):
    class Arguments:
        input = List(CreateCustomerInput, required=True)
    customers = List(CustomerNode)
    errors = List(String)

    @classmethod
    def mutate(cls, root, info, input):
        customers = []
        errors = []
        with transaction.atomic():
            for idx, data in enumerate(input):
                if Customer.objects.filter(email=data.email).exists():
                    errors.append(f"Row {idx+1}: Email already exists")
                    continue
                if not CreateCustomer.validate_phone(data.phone):
                    errors.append(f"Row {idx+1}: Invalid phone format")
                    continue
                customer = Customer.objects.create(
                    name=data.name,
                    email=data.email,
                    phone=data.phone
                )
                customers.append(customer)
        return BulkCreateCustomers(customers=customers, errors=errors)

class CreateProductInput(InputObjectType):
    name = String(required=True)
    price = Float(required=True)
    stock = Int(default_value=0)

class CreateProduct(GrapheneMutation):
    class Arguments:
        input = CreateProductInput(required=True)
    product = Field(ProductNode)
    errors = List(String)

    @classmethod
    def mutate(cls, root, info, input):
        errors = []
        if input.price <= 0:
            errors.append("Price must be positive")
        if input.stock is not None and input.stock < 0:
            errors.append("Stock cannot be negative")
        if errors:
            return CreateProduct(errors=errors)
        product = Product.objects.create(
            name=input.name,
            price=input.price,
            stock=input.stock or 0
        )
        return CreateProduct(product=product)

class CreateOrderInput(InputObjectType):
    customer_id = ID(required=True)
    product_ids = List(ID, required=True)
    order_date = String()

class CreateOrder(GrapheneMutation):
    class Arguments:
        input = CreateOrderInput(required=True)
    order = Field(OrderNode)
    errors = List(String)

    @classmethod
    def mutate(cls, root, info, input):
        errors = []
        try:
            customer = Customer.objects.get(pk=input.customer_id)
        except Customer.DoesNotExist:
            errors.append("Invalid customer ID")
            return CreateOrder(errors=errors)
        if not input.product_ids:
            errors.append("At least one product must be selected")
            return CreateOrder(errors=errors)
        products = Product.objects.filter(pk__in=input.product_ids)
        if products.count() != len(input.product_ids):
            errors.append("One or more product IDs are invalid")
            return CreateOrder(errors=errors)
        total_amount = sum([p.price for p in products])
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount
        )
        order.products.set(products)
        return CreateOrder(order=order)

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

# ... existing code ... 