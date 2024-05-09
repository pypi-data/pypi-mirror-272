from openapi_client.api.plans_api import PlansApi
from openapi_client.api_client import ApiClient


class PlansClient:
    __plans_client: PlansApi = None

    def __init__(self, api_client: ApiClient):
        self.__plans_client = PlansApi(api_client)

    def get(self, plan_id: str):
        return self.__plans_client.get_plan(plan_id)
    
    def list(self, limit: int = None, offset: int = None):
        return self.__plans_client.list_plans(limit=limit, offset=offset)

    def delete(self, id: str):
        return self.__plans_client.delete_plan(id)