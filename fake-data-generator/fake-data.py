import pandas as pd
import random
from faker import Faker
import numpy as np

# Initialize Faker for generating synthetic data
fake = Faker()

# Create Products Data
products_data = {
    "ProductID": range(1, 101),
    "ProductName": [fake.word().capitalize() for _ in range(100)],
    "Category": random.choices(["Electronics", "Furniture", "Clothing", "Beauty", "Books"], k=100),
    "UnitPrice": [round(random.randint(1, 100) + random.choice([0, 0.05, 0.99]), 2) for _ in range(100)],
    "StockQuantity": [random.randint(10, 500) for _ in range(100)],
    "SupplierID": random.choices(range(101, 121), k=100),
    "ProductCreationDate": [fake.date_between(start_date='-3y', end_date='today') for _ in range(100)]
}
products_df = pd.DataFrame(products_data)

# Create Suppliers Data
suppliers_data = {
    "SupplierID": range(101, 121),
    "SupplierName": [fake.company() for _ in range(20)],
    "ContactEmail": [fake.email() for _ in range(20)],
    "Phone": [fake.phone_number() for _ in range(20)],
    "Address": [fake.address().replace('\n', ', ') for _ in range(20)],
    "SupplierCreationDate": [fake.date_between(start_date='-3y', end_date='today') for _ in range(20)]
}
suppliers_df = pd.DataFrame(suppliers_data)

# Create Customers Data
customers_data = {
    "CustomerID": range(201, 301),
    "CustomerName": [fake.name() for _ in range(100)],
    "Email": [fake.email() for _ in range(100)],
    "Phone": [fake.phone_number() for _ in range(100)],
    "Address": [fake.address().replace('\n', ', ') for _ in range(100)],
    "RegistrationDate": [fake.date_between(start_date='-3y', end_date='today') for _ in range(100)]
}
customers_df = pd.DataFrame(customers_data)

# Create initial Orders Data
orders_data = []
for i in range(100):
    order_purchase_timestamp = fake.date_time_between(start_date='-1m', end_date='now')
    order_approved_at = order_purchase_timestamp + pd.Timedelta(hours=random.randint(0, 12))  # Approved within 0 to 3 days
    order_delivered_carrier_date = order_approved_at + pd.Timedelta(days=random.randint(1, 3))  # Delivered to carrier within 1 to 3 days
    order_delivered_customer_date = order_delivered_carrier_date + pd.Timedelta(days=random.randint(1, 5))  # Customer delivery within 1 to 5 days
    order_estimated_delivery_date = order_delivered_customer_date + pd.Timedelta(days=random.randint(1, 7))  # Estimated delivery within 1 week

    orders_data.append({
        "OrderID": 1001 + i,
        "CustomerID": random.choice(range(201, 301)),
        "OrderStatus": random.choice(["Pending", "Shipped", "Delivered"]),
        "OrderPurchaseTimestamp": order_purchase_timestamp,
        "OrderApprovedAt": order_approved_at,
        "OrderDeliveredCarrierDate": order_delivered_carrier_date,
        "OrderDeliveredCustomerDate": order_delivered_customer_date,
        "OrderEstimatedDeliveryDate": order_estimated_delivery_date,
        "TotalAmount": round(random.uniform(50, 2000), 2)
    })
orders_df = pd.DataFrame(orders_data)

# Add validity dates for slow changing dimensions
current_date = pd.Timestamp.now()
orders_df['DateValidFrom'] = orders_df['OrderPurchaseTimestamp'].apply(lambda x: x.floor('D'))
orders_df['DateValidTo'] = current_date + pd.DateOffset(years=1)  # Valid for 1 year

# Create OrderDetails Data
order_details_data = {
    "OrderID": random.choices(range(1001, 1101), k=300),
    "ProductID": random.choices(range(1, 101), k=300),
    "QuantityOrdered": [random.randint(1, 10) for _ in range(300)],
    "UnitPrice": [round(random.randint(1, 100) + random.choice([0, 0.05, 0.99]), 2) for _ in range(300)]
}
order_details_df = pd.DataFrame(order_details_data)
order_details_df["TotalPrice"] = round(order_details_df["QuantityOrdered"] * order_details_df["UnitPrice"],2)

# Save all DataFrames to CSV files
products_df.to_csv('./fake_data/products.csv', index=False)
suppliers_df.to_csv('./fake_data/suppliers.csv', index=False)
customers_df.to_csv('./fake_data/customers.csv', index=False)
orders_df.to_csv('./fake_data/orders_with_validity.csv', index=False)
order_details_df.to_csv('./fake_data/order_details.csv', index=False)
