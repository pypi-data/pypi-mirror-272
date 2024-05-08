from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanFile
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class KeyValueArguments(TcBaseObj):
    """
    This structure represents the user specified key/value arguments that can be attached to the Dispatcher Request.
    These are translator specific arguments which are handled as inputs by the translators.
    
    :var key: The key of the key/value pair. Example File ticket can be passed as input to translator. In this case,
    key could be "FILE_TICKET"
    :var value: The value of the key/value pair. Example value can be FMS File ticket. This value can be used to
    download a file for translation.
    """
    key: str = ''
    value: str = ''


@dataclass
class CreateDispatcherRequestArgs(TcBaseObj):
    """
    The CreateDispatcherRequestArgs struct is used to pass in multiple sets of data to be used in a single call.  These
    structs are passed in the collection of input arguments to the function createDispatcherRequest.
    
    :var providerName: Name of the provider implementing this Service associated with this request. Example SIEMENS.
    :var serviceName: The service name which is the translator to process when this DispatcherRequest is executed.
    :var type: The type of this request (USER SPECIFIED). Translators could use this option to support additional
    options for a given translator. Example "OnDemand" if created through UI and "OnSave" and translator could choose
    different options based on this type.
    :var primaryObjects: The input primary objects that need to be translated. This usually refers to a dataset to
    translate but can be any component.
    :var secondaryObjects: The input secondary objects for the request. This usually refers to the Item Revision
    containing the primary objects.
    :var priority: The priority to assign to the request. Supported priorities are 1 for low, 2 for medium and 3 for
    high.
    :var startTime: The start time to start the request. Date format is MM/dd/yyyy HH:mm
    :var endTime: The end time at which repeating request should stop processing based on interval setting. Date format
    is MM/dd/yyyy HH:mm. If request is still processing, the request will be completed and will not be stopped.
    :var interval: Repeating request is executed from start time to end time with this interval specified in seconds.
    :var keyValueArgs: User specified key/value arguments for the request. These are translator specific arguments
    which are handled as inputs by the translators.
    :var dataFiles: User specified key/file pairs that can be attached to the Dispatcher Request. These are translator
    specific files which are used as inputs by the translators.
    """
    providerName: str = ''
    serviceName: str = ''
    type: str = ''
    primaryObjects: List[BusinessObject] = ()
    secondaryObjects: List[BusinessObject] = ()
    priority: int = 0
    startTime: str = ''
    endTime: str = ''
    interval: int = 0
    keyValueArgs: List[KeyValueArguments] = ()
    dataFiles: List[DataFiles] = ()


@dataclass
class CreateDispatcherRequestResponse(TcBaseObj):
    """
    The CreateDispatcherRequestResponse struct contains the requests that were created as a result of the inputs
    specified in the CreateDispatcherRequestArgs structure above.
    
    :var requestsCreated: The Dispatcher Request objects created.
    :var svcData: The SOA Service Data.
    """
    requestsCreated: List[BusinessObject] = ()
    svcData: ServiceData = None


@dataclass
class DataFiles(TcBaseObj):
    """
    This structure represents the user specified key/file pairs that can be attached to the Dispatcher Request. These
    are translator specific files which are used as inputs by the translators.
    
    :var key: The key of the key/file pair. Example "CONFIG_FILE" could be a key to identify a configuration file.
    :var file: File which could be the input for translation. Example ImanFile which is the configuration file.
    """
    key: str = ''
    file: ImanFile = None
