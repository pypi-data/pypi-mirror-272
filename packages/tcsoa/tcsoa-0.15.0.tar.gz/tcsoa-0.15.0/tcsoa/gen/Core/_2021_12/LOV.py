from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2013_05.LOV import LOVValueRow
from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ValidateLOVPropertyData(TcBaseObj):
    """
    The ValidateLOVPropertyData structure contains LOV property value validadity, dependentPropNames and updated
    property values.
    
    :var propName: Input Property name to which the LOV is attached.
    :var propHasValidValues: Names of dependent properties server modified to be updated by client as a results of
    dependency with input property selection. This can be empty.
    :var dependentPropNames: Names of dependent properties server modified to be updated by client as a results of
    dependency with input property selection. This can be empty.
    :var updatedPropValues: Updated property values. It contains both internal and display values of the updated
    properties. It can be empty.
    """
    propName: str = ''
    propHasValidValues: bool = False
    dependentPropNames: List[str] = ()
    updatedPropValues: LOVValueRow = None


@dataclass
class ValidatePropertyValuesForLOVInBulkInputData(TcBaseObj):
    """
    This represents the LOV property value validation input for the Business Object(s).
    
    :var clientID: A unique string used to identify return data elements with this input structure.
    :var owningObject: Object for which this operation being invoked. 
    a. Edit operation - Object to be edited. 
    b. Save operation - Object to be saved. 
    c. Revise operation - Object to be revised. 
    d. SaveAs operation - Object to be copied. 
    e. Search operation - Saved Query Object for searching. 
    If an operation does not have an object, specify the value as null and ensure boName is not empty. 
    For example, during creation, client does not have an object. Therefore specify the business object name of the
    object being created. For example, if Item object is being created, specify the boName as "Item" and operationName
    as "Create".
    :var boName: Name of the source business object. For example, Item is the source business object for Item
    Descriptors. If the owningObject is not null, then boName can be empty. Server can determine the business object
    name from the owningObject. It is mandatory for Create operation where owningObject is null.
    :var operationName: Name of the business object operation like "Create", "SaveAs" etc. to be performed. Valid
    operation names supported by this service operation are: "Create", "Revise", "SaveAs", "Edit", "Search", "Save".
    :var propNames: Name of the properties for which LOV validation being done. If no properties are specified then no
    validation happens and partial error will be returned.
    :var propValues: A map (string, list) of property names and values that are being edited by User. The client is
    responsible for converting the values of the different property types (int, float, date .etc) to a string using the
    appropriate toXXXString functions in the service operation client framework's Property class. Single valued
    properties will have a single value in the value list while Multi-valued properties will have multiple values in
    the value list.
    """
    clientID: str = ''
    owningObject: BusinessObject = None
    boName: str = ''
    operationName: str = ''
    propNames: List[str] = ()
    propValues: PropertyValuesMap = None


@dataclass
class ValidatePropertyValuesForLOVInBulkOutput(TcBaseObj):
    """
    The ValidatePropertyValuesForLOVInBulkOutput contains clientID and LOV property value validation output.
    
    :var clientID: The unmodified value from the input clientId. This can be used by the caller to indentify this data
    structure with the source input.
    :var validateLOVPropertyOutput: A list containing property names with list of ValidateLOVPropertyData.
    """
    clientID: str = ''
    validateLOVPropertyOutput: List[ValidateLOVPropertyData] = ()


@dataclass
class ValidatePropertyValuesForLOVInBulkResponse(TcBaseObj):
    """
    The ValidatePropertyValuesForLOVInBulkResponse contains the output response structure for
    validatePropertyValuesForLOVInBulk service operation.
    
    :var output: A list containing the clientID and list of ValidatePropertyValuesForLOVInBulkOutput. For each input,
    one ValidatePropertyValuesForLOVInBulkOutput will be returned.
    :var serviceData: Service data object associated with the operation.
    """
    output: List[ValidatePropertyValuesForLOVInBulkOutput] = ()
    serviceData: ServiceData = None


"""
Map (string, vector) that is a generic container that represents property values. The key is the property name and the value is the string representation of the property value.
"""
PropertyValuesMap = Dict[str, List[str]]
