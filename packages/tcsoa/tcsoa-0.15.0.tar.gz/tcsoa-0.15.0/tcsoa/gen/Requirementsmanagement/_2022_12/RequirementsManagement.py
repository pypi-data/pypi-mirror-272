from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from enum import Enum
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SetContentInput2(TcBaseObj):
    """
    The SetContentInput2 structure represents the input required to set the contents on the FullText object.
    
    :var objectToProcess: FullText object or any BusinessObject with a FullText, attached via an IMAN_Specification
    relation, where FullText is a secondary object.
    :var transientFileWriteTicket: An FMS ticket of a Microsoft Word file to be uploaded to Teamcenter.
    :var contentType: Type of content to be set on the FullText. Supported values are: REQ_HTML, REQ_PLAINTEXT or
    REQ_RICHTEXT
    :var contents: The actual content to be set on the FullText object.
    """
    objectToProcess: BusinessObject = None
    transientFileWriteTicket: str = ''
    contentType: ContentTypes = None
    contents: str = ''


class ContentTypes(Enum):
    """
    Defines the valid content types of the FullText object.
    """
    REQ_HTML = 'REQ_HTML'
    REQ_PLAINTEXT = 'REQ_PLAINTEXT'
    REQ_RICHTEXT = 'REQ_RICHTEXT'
