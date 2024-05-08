from __future__ import annotations

from tcsoa.gen.Administration._2012_09.PreferenceManagement import GetPreferencesResponse
from typing import List
from tcsoa.base import TcService


class PreferenceManagementService(TcService):

    @classmethod
    def refreshPreferences2(cls, preferenceNames: List[str], includePreferenceDescriptions: bool) -> GetPreferencesResponse:
        """
        Refresh the specified prefences and then retrieve the values for the preferences specified in the list of
        names, as seen by the current user, based on current application context. If there are no values in current
        application context, values that exist in the default application context are retrieved. 
        If the list is empty or its first value is equal to "*", all the preferences as seen by the logged-in user will
        be refreshed and returned (not only the preference instances created by the logged-in user).
        """
        return cls.execute_soa_method(
            method_name='refreshPreferences2',
            library='Administration',
            service_date='2020_12',
            service_name='PreferenceManagement',
            params={'preferenceNames': preferenceNames, 'includePreferenceDescriptions': includePreferenceDescriptions},
            response_cls=GetPreferencesResponse,
        )
