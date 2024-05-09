from entity_clients.events_client import EventsClient
from openapi_client.api.auth_api import AuthApi
from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
from openapi_client.models.aggregation_method import AggregationMethod
from openapi_client.models.event import Event
from openapi_client.models.login_request_schema import LoginRequestSchema
from vayu_consts import VAYU_URL

from .entity_clients.contracts_client import ContractsClient
from .entity_clients.customers_client import CustomersClient
from .entity_clients.invoices_client import InvoicesClient
from .entity_clients.meters_client import MetersClient
from .entity_clients.plans_client import PlansClient


class Vayu:
    __api_key: str = None

    @property
    def __private_api_client(self):
        configuration = Configuration(host=VAYU_URL, api_key=self.__api_key)
        
        return ApiClient(configuration)

    @property
    def __public_api_client(self):
        configuration = Configuration(host=VAYU_URL)
        
        return ApiClient(configuration)

    @property
    def customers(self)->CustomersClient:
        return CustomersClient(self.__private_api_client)

    @property
    def plans(self)->PlansClient:
        return PlansClient(self.__private_api_client)


    @property
    def contracts(self)->ContractsClient:
        return ContractsClient(self.__private_api_client)


    @property
    def meters(self)->MetersClient:
        return MetersClient(self.__private_api_client)


    @property
    def invoices(self)->InvoicesClient:
        return InvoicesClient(self.__private_api_client)

    @property
    def events(self)->EventsClient:
        return EventsClient(self.__private_api_client)

    def __init__(self, api_key: str):
        self.__login(api_key)
    

    def __login(self, refresh_token: str):
        auth_api = AuthApi(self.__public_api_client)
        login_request = LoginRequestSchema(refresh_token)
        refresh_response = auth_api.login(login_request)

        self.__api_key = refresh_response.access_token
