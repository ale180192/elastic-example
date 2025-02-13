from elasticsearch import Elasticsearch
import datetime
# Reemplaza con la URL de tu cluster en Elastic Cloud
CLOUD_ID = "d1615ca690f34e65b4f7bb55b11431ba:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQwNGRmZWI2MTcyOGY0NzlkOWI5YTE3YjA1MWZiMWM3YSQwOTQ4MjBiZjE1OTQ0NzRmOTdmOWJiYWZlZWI0Y2ZmMg=="
API_KEY = "ekZaaV9KUUJxOGNuTW9LMDlEVlg6blZkRlcyMlBTbkdkSXRCZnFlRklSQQ=="

# Conectar a Elasticsearch en Elastic Cloud con API Key
es = Elasticsearch(
    cloud_id=CLOUD_ID,
    api_key=API_KEY
)


# Documento de ejemplo
doc = {
    "transaction_id": "abc123",
    "customer_id": "user_456",
    "customer_name": "John Doe",
    "total_amount": 199.99,
    "payment_method": "credit_card",
    "products": [
        {"product_id": "p001", "product_name": "Laptop",
            "category": "Electronics", "price": 999.99, "quantity": 1},
        {"product_id": "p002", "product_name": "Mouse",
            "category": "Accessories", "price": 19.99, "quantity": 2}
    ],
    "purchase_date": datetime.datetime.utcnow().isoformat(),
    "location": {"lat": 19.4326, "lon": -99.1332}
}

# Indexar documento en Elasticsearch
es.index(index="transactions", document=doc)

print("Documento insertado correctamente")
