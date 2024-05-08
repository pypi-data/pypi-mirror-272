import os
from typing import Dict, Optional, Callable

from requests import Response

from ..apiwrappers.httpresponsehandler import HttpResponseHandler
from ..apiwrappers.authenticator import BearerTokenAuth
from ..decorators.ratelimiters import burst_rate_limiter
from ..apiwrappers.dto import RequestConfig
from ..utils.loggers import ConsoleLogger
from ..apiwrappers.restapiwrappers import PaginatedListEntity, RestApiContext, CreateMixin, with_route, \
    ReadMixin, with_id_route, UpdateMixin, DeleteMixin, RestApiClient


class AgendrixHttpResponseHandler(HttpResponseHandler):
    def on_unauthorized(
        self,
        request: RequestConfig,
        response: Response,
        request_method: Callable[[RequestConfig], Response]
    ):
        self.logger.log(f"[401]: Renewing token...")
        self.auth.renew_auth()
        self.logger.log(f"[401]: Token Renewed.")
        self.logger.log(f"Retrying query...")
        new_response = request_method(request)
        new_response.raise_for_status()
        return new_response


class AgendrixPagedEntity(PaginatedListEntity):
    def __init__(self, api_context, base_url):
        self._base_url = base_url
        super().__init__(api_context, self._base_url)
        self._api_context: RestApiContext = api_context

    def _has_next(self, response: dict, current_page: int, end_page: Optional[int] = None) -> bool:
        pagination: dict = response['pagination']
        total_pages = pagination['total_pages']
        next_page = pagination['next_page']

        more_pages_to_get = next_page is not None
        got_all_pages_requested = end_page is not None and (current_page >= end_page or current_page >= total_pages)

        return more_pages_to_get and not got_all_pages_requested

    def _get_next(self, query_params: Dict[str, any] = None):
        return self._api_context.get(self._base_url, query_params=query_params)


class AgendrixAuth(BearerTokenAuth):
    def get_token(self) -> str:
        return os.environ.get("MY_AGENDRIX_TOKEN")

    def get_new_token(self) -> str:
        return "oquaD6vxhs4COxn_zpD9dgVl5-QKKQF9FFhIxP1HggE"
        pass


class AgendrixApiContext(RestApiContext):
    def __init__(self):
        super().__init__(
            rate_limiter=burst_rate_limiter(360, 60),
            authenticator=AgendrixAuth(),
            logger=ConsoleLogger(),
            http_handler=AgendrixHttpResponseHandler()
        )


@with_route("shifts")
class ShiftList(CreateMixin, AgendrixPagedEntity):
    def by_id(self, id: str):
        return ShiftEntity(self._api_context, self._base_url, id=id)


@with_id_route()
class ShiftEntity(ReadMixin, UpdateMixin, DeleteMixin):
    pass


@with_route("sites")
class SiteList(AgendrixPagedEntity):
    def by_id(self, id: str):
        return SiteEntity(self._api_context, self._base_url, id=id)


@with_id_route()
class SiteEntity(ReadMixin):
    pass


@with_route("members")
class MemberList(AgendrixPagedEntity):
    def by_id(self, id: str):
        return MemberEntity(self._api_context, self._base_url, id=id)


@with_id_route()
class MemberEntity(ReadMixin, UpdateMixin):
    pass


@with_route("positions")
class PositionList(AgendrixPagedEntity):
    def by_id(self, id: str):
        return PositionEntity(self._api_context, self._base_url, id=id)


@with_id_route()
class PositionEntity(ReadMixin, UpdateMixin):
    pass


@with_route("time_entries")
class TimeEntryList(CreateMixin, AgendrixPagedEntity):
    def by_id(self, id: str):
        return TimeEntryEntity(self._api_context, self._base_url, id=id)


@with_id_route()
class TimeEntryEntity(ReadMixin, UpdateMixin):
    pass


@with_route("clock_logs")
class ClockLogList(CreateMixin, AgendrixPagedEntity):
    def by_id(self, id: str):
        return ClockLogEntity(self._api_context, self._base_url, id=id)


@with_id_route()
class ClockLogEntity(ReadMixin):
    pass


class AgendrixApiClient(RestApiClient):
    def __init__(self):
        super().__init__(
            base_url="https://api.sandbox.agendrix.net/v1",
            api_context=AgendrixApiContext()
        )

    @property
    def shifts(self):
        return ShiftList(self._api_context, self._base_url)

    @property
    def sites(self):
        return SiteList(self._api_context, self._base_url)

    @property
    def members(self):
        return MemberList(self._api_context, self._base_url)

    @property
    def positions(self):
        return PositionList(self._api_context, self._base_url)

    @property
    def time_entries(self):
        return TimeEntryList(self._api_context, self._base_url)

    @property
    def clock_logs(self):
        return ClockLogList(self._api_context, self._base_url)


api = AgendrixApiClient()
shifts = list(api.shifts.list({"search[from]": "2023-08-20", "search[to]": "2023-08-30"}))
site = api.shifts.by_id('2dea1d3f-4d03-4a51-a902-110d0c1c029b').get()
members = list(api.members.list())
sites = list(api.sites.list())
print()




