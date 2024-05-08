from __future__ import annotations

from tcsoa.gen.Markup._2022_06.Markup import MarkupResponse
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class MarkupService(TcService):

    @classmethod
    def processMarkups(cls, baseObject: WorkspaceObject, action: str, version: str, message: str, markups: str) -> MarkupResponse:
        """
        This operation processes (load or save) the markups or stamps on the server.
        
        Use cases:
        - Load all the existing markups from the server.
        - Save the user created or modified markups to the server and load updated markups.
        - Load all the existing stamps from the server.
        - Save the user created or modified stamps to the server and load updated stamps.
        
        """
        return cls.execute_soa_method(
            method_name='processMarkups',
            library='Markup',
            service_date='2022_06',
            service_name='Markup',
            params={'baseObject': baseObject, 'action': action, 'version': version, 'message': message, 'markups': markups},
            response_cls=MarkupResponse,
        )
