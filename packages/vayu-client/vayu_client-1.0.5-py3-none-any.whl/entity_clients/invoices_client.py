from openapi_client.api.invoices_api import InvoicesApi
from openapi_client.api_client import ApiClient


class InvoicesClient:
    __invoices_client: InvoicesApi = None

    def __init__(self, api_client: ApiClient):
        self.__invoices_client = InvoicesApi(api_client)

    def get(self, invoice_id: str):
        return self.__invoices_client.get_invoice(invoice_id)
    
    def list(self, limit: int = None, offset: int = None):
        return self.__invoices_client.list_invoices(limit=limit, offset=offset)