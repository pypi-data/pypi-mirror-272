from typing import List

from openapi_client.api.meters_api import MetersApi
from openapi_client.api_client import ApiClient
from openapi_client.models.aggregation_method import AggregationMethod
from openapi_client.models.filter import Filter
from openapi_client.models.update_meter_request_schema import \
    UpdateMeterRequestSchema
from vayu_consts import VAYU_URL


class MetersClient:
    __meters_client: MetersApi = None

    def __init__(self, api_client: ApiClient):
        self.__meters_client = MetersApi(api_client)

    def get(self, meter_id: str):
        return self.__meters_client.get_meter(meter_id)
    
    def list(self, limit: int = None, offset: int = None):
        return self.__meters_client.list_meters(limit=limit, offset=offset)

    def update(
        self,
        id: str,
        name: str = None,
        event_name: str = None,
        aggregation_method: AggregationMethod = None,
        filter: Filter = None,
    ):
        update_meter_request = UpdateMeterRequestSchema(
            name=name,
            eventName=event_name,
            aggregationMethod=aggregation_method,
            filter=filter
        )

        return self.__meters_client.update_meter(id, update_meter_request)

    def delete(self, id: str):
        return self.__meters_client.delete_meter(id)
        






    # name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="The name of the meter")
    # event_name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="The name of the event that the meter is tracking.", alias="eventName")
    # aggregation_method: Optional[EventsDryRunResponseSchemaInnerMeterWithValuesInnerAggregationMethod] = Field(default=None, alias="aggregationMethod")
    # filter: Optional[Filter] = None