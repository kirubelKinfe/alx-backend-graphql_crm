import graphene
from graphene_django import DjangoObjectType
from crm.models import Product, Customer, Order
from django.db.models import Sum

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class ReportType(graphene.ObjectType):
    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Float()

class Query(graphene.ObjectType):
    report = graphene.Field(ReportType)

    def resolve_report(self, info):
        total_customers = Customer.objects.count()
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0.0
        return ReportType(
            total_customers=total_customers,
            total_orders=total_orders,
            total_revenue=total_revenue
        )

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []
        
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)
        
        message = f"Updated {len(updated_products)} products with low stock."
        return UpdateLowStockProducts(updated_products=updated_products, message=message)

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)