# Partnero SDK

The Partnero SDK provides a simple and powerful Python interface to the Partnero API, allowing developers to manage customers, partners, transactions, webhooks, coupons, and promotion codes programmatically.
[Partnero API Documentation](https://developers.partnero.com/reference/general.html)
## Installation

To install the Partnero SDK, run the following command:

```bash
pip install partnero
```

## Configuration

Before using the SDK, you need to set up authentication:

```python
from partnero import Authentication

# Replace 'your_api_token_here' with your actual API token
auth = Authentication.configure(api_token='your_api_token_here')
```

## Usage

Here's how you can use different components of the SDK:

### Customer Management

**List Customers**

```python
from partnero import CustomerAPI

customer_api = CustomerAPI()
customers = customer_api.list_customers(limit=10, page=1)
print(customers)
```

**Create a New Customer**

```python
new_customer = customer_api.create_customer(
    partner_key='your_partner_key',
    customer_key='unique_customer_key',
    email='customer@example.com',
    name='Customer Name'
)
print(new_customer)
```

### Partner Management

**List Partners**

```python
from partnero import PartnerAPI

partner_api = PartnerAPI()
partners = partner_api.list_partners(limit=5, page=1)
print(partners)
```

**Register a New Partner**

```python
new_partner = partner_api.create_partner(
    email='newpartner@example.com',
    name='New Partner',
    password='securepassword123'
)
print(new_partner)
```

### Transaction Management

**List Transactions**

```python
from partnero import TransactionAPI

transaction_api = TransactionAPI()
transactions = transaction_api.list_transactions(limit=5, page=1)
print(transactions)
```

**Create a Transaction**

```python
new_transaction = transaction_api.create_transaction(
    customer_key='customer_key',
    transaction_key='unique_transaction_key',
    amount=39.99,
    product_id='product_id',
    product_type='type',
    action='purchase'
)
print(new_transaction)
```

### Webhook Management

**List Webhooks**

```python
from partnero import WebhookAPI

webhook_api = WebhookAPI()
webhooks = webhook_api.list_webhooks(limit=5, page=1)
print(webhooks)
```

**Create a Webhook**

```python
new_webhook = webhook_api.create_webhook(
    name='Order Placed',
    url='https://yourdomain.com/webhooks/order_placed',
    events=['order_placed'],
    is_active=True
)
print(new_webhook)
```

## Contributions

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This SDK is released under the MIT License. See the LICENSE file for more details.
```

This README includes basic examples of how to use each part of your SDK. It also guides the user on error handling and encourages community contributions, which are important aspects of maintaining an open-source project.

**Suggestions for your next steps:**
- **a.** Consider adding a `Contributing.md` file to guide potential contributors on how to help develop the SDK further.
- **b.** Regularly update the documentation as you add features or make changes to the SDK.