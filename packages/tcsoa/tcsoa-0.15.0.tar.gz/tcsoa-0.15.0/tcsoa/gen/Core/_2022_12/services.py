from __future__ import annotations

from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def tcServerSleep(cls, seconds: int) -> str:
        """
        A no-op serivce operation that puts the TcServer in a wait/sleep for the requested amount of time before
        returning.
        This can be used to simulate long running service requests.
        """
        return cls.execute_soa_method(
            method_name='tcServerSleep',
            library='Core',
            service_date='2022_12',
            service_name='Session',
            params={'seconds': seconds},
            response_cls=str,
        )
