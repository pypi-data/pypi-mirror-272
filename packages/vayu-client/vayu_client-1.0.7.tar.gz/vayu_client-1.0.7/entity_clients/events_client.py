from datetime import datetime
from typing import List

from openapi_client.api.events_api import EventsApi
from openapi_client.api_client import ApiClient
from openapi_client.models.event import Event
from openapi_client.models.send_events_request_schema import \
    SendEventsRequestSchema


class EventsClient:
    __events_client: EventsApi = None

    def __init__(self, api_client: ApiClient):
        self.__events_client = EventsApi(api_client)

    def query(
        self,
        start_time: datetime,
        end_time: datetime,
        event_name: str,
        cursor: str = None,
        limit: int = None
    ):
        return self.__events_client.query_events(
            start_time=start_time,
            end_time=end_time,
            event_name=event_name,
            cursor=cursor,
            limit=limit
        )

    def get(self, ref: str):
        return self.__events_client.get_event_by_ref_id(ref)

    def delete(self, ref: str):
        return self.__events_client.delete_event_by_ref_id(ref)

    def send(self, events: List[Event]):
        send_events_request_schema = SendEventsRequestSchema(events)

        return self.__events_client.send_events(send_events_request_schema)

    def dry_run(self, events: List[Event]):
        send_events_request_schema = SendEventsRequestSchema(events)

        return self.__events_client.send_events_dry_run(send_events_request_schema)