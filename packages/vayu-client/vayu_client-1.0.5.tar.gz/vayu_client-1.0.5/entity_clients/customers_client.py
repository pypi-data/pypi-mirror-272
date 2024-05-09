from typing import List

from openapi_client.api.customers_api import CustomersApi
from openapi_client.api_client import ApiClient
from openapi_client.models.create_customer_request_schema import \
    CreateCustomerRequestSchema
from openapi_client.models.update_customer_request_schema import \
    UpdateCustomerRequestSchema


class CustomersClient:
    __customers_client: CustomersApi = None

    def __init__(self, api_client: ApiClient):
        self.__customers_client = CustomersApi(api_client)

    def get(self, customer_id: str):
        return self.__customers_client.get_customer(customer_id)
    
    def list(self, limit: int = None, offset: int = None):
        return self.__customers_client.list_customers(limit=limit, offset=offset)

    def create(self, name: str, alias: str):
        create_customer_request = CreateCustomerRequestSchema(name=name, alias=alias)
        return self.__customers_client.create_customer(create_customer_request)

    def update(self, id: str, name: str = None, alias: str = None):
        update_customer_request = UpdateCustomerRequestSchema(name=name, alias=alias)
        return self.__customers_client.update_customer(id, update_customer_request)

    def delete(self, id: str):
        return self.__customers_client.delete_customer(id)