from __future__ import annotations

from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def refreshPOMCachePerRequestDeprecated(cls, refresh: bool) -> bool:
        """
        By Default the service operations will retrieve property value data straight from the POM. When 'refresh' is
        set to true, a refresh will be done on business objects before getting any property data. This will update the
        POM with fresh data from the database. The refresh is only applied to business objects that are actually being
        returned by a service operation. This applies only to database objects, and is not applied to runtime objects. 
        This is applied to all subsequent service requests from the same client. If multiple clients are sharing the
        same Teamcenter server session the refresh POM state is applied per client. Setting this to true will have a
        performance impact but will grantee all property values returned are up-to-date.
        """
        return cls.execute_soa_method(
            method_name='refreshPOMCachePerRequestDeprecated',
            library='Internal-Core',
            service_date='2007_05',
            service_name='Session',
            params={'refresh': refresh},
            response_cls=bool,
        )
