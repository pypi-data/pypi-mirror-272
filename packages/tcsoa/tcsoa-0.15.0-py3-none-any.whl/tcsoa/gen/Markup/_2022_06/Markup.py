from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class MarkupResponse(TcBaseObj):
    """
    This MarkupResponse structure is for the response of all processMarkups operations.
    
    :var baseObject: The base object after process markups.
    :var version: The version of the markups, set by the server and opaque to the client. Client always include the
    version in the request to the server. The server use it to determine if the content on the client is up to date. If
    so, the server responds with a message "up-to-date"; otherwise the server sends the latest markups to the client.
    :var message: The supplement message from server to the client.
    Values can be:
    - "author"
    - "reviewer" 
    - "reader"
    - "admin"
    - "up-to-date"
    
    
    :var markups: The current markups from the server in JSON format.
    - It will be "[]" if there is no markups on the server.
    - It will be empty string if the message is "up-to-date".
    - It will be empty string if error occcured.
    
    
    :var serviceData: The service data contains any partial errors which may have been encountered during processing.
    """
    baseObject: WorkspaceObject = None
    version: str = ''
    message: str = ''
    markups: str = ''
    serviceData: ServiceData = None
