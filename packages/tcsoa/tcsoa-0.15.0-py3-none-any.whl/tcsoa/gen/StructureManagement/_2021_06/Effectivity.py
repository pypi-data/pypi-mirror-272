from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetEffectivitiesResponse(TcBaseObj):
    """
    Holds the Effectivity data associated with the input objects.
    
    :var effectivitiesInfo: A list of effectivities info structures per input object.
    :var serviceData: The service data contains partial errors, if there are any errors during the operation.
    """
    effectivitiesInfo: List[EffectivitiesInfo] = ()
    serviceData: ServiceData = None


@dataclass
class EffectivitiesInfo(TcBaseObj):
    """
    Holds effectivity data for each input object. The effectivity data can be either in the form of list of
    Teamcenter::Effectivity objects or a list of effectivity expression information. If the input object holds the
    effectivity expression, it will be broken into expression data structure which contains unit ranges, date ranges,
    end item along with respective formula.
    Note: 
    The operation will either populate effectivityExprData with formula or effectivityObjects depending on the
    underlying effectivity storage model.
    
    :var inputObjectIndex: The index of input BusinessObject to which effectivity information is associated.
    :var effectivityExprData: A list of Effectivity for an inputObject.
    :var effectivityExprFormula: The effectivity formula for the inputObject. For example, for unit range 1-10 the
    corresponding formula is ([Teamcenter::]Unit >= 1 &amp; [Teamcenter::]Unit < 11 ) &amp; [Teamcenter::]EndItem =
    "HDD-Top"
    :var effectivityObjects: A list of Effectivity objects with specified effectivity data.
    """
    inputObjectIndex: int = 0
    effectivityExprData: List[EffectivityExpressionData] = ()
    effectivityExprFormula: str = ''
    effectivityObjects: List[BusinessObject] = ()


@dataclass
class EffectivityExpressionData(TcBaseObj):
    """
    The EffectivityExpressionData represents a validity range. The following constants have special meaning:
    &bull;    January 2, 1900 12:00 AM UTC: Open Start Date.
    &bull;    December 30, 9999 12:00 AM UTC: Open End Date.
    &bull;    December 26, 9999 12:00 AM UTC: Stock Out.
    &bull;    1: Open Start Unit.
    &bull;    2147483647: Open End Unit.
    &bull;    2147483646: Stock Out.
    Effect in as well as effect out points may have NULL values, which indicate no value assigned:
    &bull;    -1: no unit value assigned.
    &bull;    NULL date: no date value assigned.
    
    :var unitStart: The unit at which validity range starts.
    :var unitEnd: The unit at which validity range ends.
    :var dateStart: The date at which validity range starts.
    :var dateEnd: The date at which validity range ends.
    :var endItemObject: The effectivity end Item or ItemRevision.
    :var expressionEffFormula: Expression Effectivity clause Formula.
    :var effectivityOptions: A list of EffectivityOption for which the effectivity range is valid (optional). The valid
    effectivity options are available on the effectivity context associated with product Item with relation
    Fnd0ProductEffConfigCxtRel.
    For example, effectivity context with item id EFFCTX001 is associated with product Item. It has option families
    defined with names Maturity Intent and Module Intent. Maturity Intent has values Design and Production. Module
    Intent has values Kit and Modkit.  The effectivity options can be specified as: 
    &bull;    familyNamespace=EFFCTX001, familyName=Maturity Intent, optionValue=Design, opCode=5
    &bull;    familyNamespace=EFFCTX001, familyName=Module Intent, optionValue=Kit, opCode=5
    """
    unitStart: int = 0
    unitEnd: int = 0
    dateStart: datetime = None
    dateEnd: datetime = None
    endItemObject: BusinessObject = None
    expressionEffFormula: str = ''
    effectivityOptions: List[EffectivityOption] = ()


@dataclass
class EffectivityOption(TcBaseObj):
    """
    For example, if expression formula is like :([Teamcenter::]Unit >= 10 &amp; [Teamcenter::]Unit <= 50 ) &amp;
    [Teamcenter::]EndItem = "Engine" &amp; [EFFCTX001]MaturityIntent = "Design" &amp; [EFFCTX001]ModuleIntent = "Kit",
    then Effectivity expression data will be as below:
    
    UnitStart: 10, UnitEnd: 50, endItemObject: "Engine",
    effectivityOptions: [
    {familyNamespace:"EFFCTX001", familyName:"MaturityIntent", opCode: 5, optionValue: "Design"},
    {familyNamespace:"EFFCTX001",    familyName:" ModuleIntent", opCode: 5, optionValue: "Kit"}],
    expressionEffFormula: 
    ([Teamcenter::]Unit >= 10 &amp; [Teamcenter::]Unit <= 50 ) &amp; [Teamcenter::]EndItem = "Engine" &amp;
    [EFFCTX001]MaturityIntent = "Design" &amp; [EFFCTX001]ModuleIntent = "Kit"
    
    :var familyNamespace: The namespace by which the effectivity option family is uniquely identified. The
    familyNamespace is the item id of effectivity context associated with product Item with relation
    Fnd0ProductEffConfigCxtRel.
    For example, effectivity context with item id EFFCTX001 is associated with product Item. It has option families
    defined with names Maturity Intent and Module Intent. Maturity Intent has values Design and Production. Module
    Intent has values Kit and Modkit. The familyNamespace can be EFFCTX001.
    :var familyName: The name of the effectivity option family. Valid option family names are available on the
    effectivity context associated with product Item with relation Fnd0ProductEffConfigCxtRel.
    For example, effectivity context with item id EFFCTX001 is associated with product Item. It has option families
    defined with names Maturity Intent and Module Intent. Maturity Intent has values Design and Production. Module
    Intent has values Kit and Modkit. The familyNamespace is set as EFFCTX001. The familyName can be either Maturity
    Intent or Module Intent.
    :var opCode: The operator to be used for the optionValue. 
    The valid values are:
    &bull;    5 &ndash; Equals
    &bull;    6 &ndash; Not Equals
    :var optionValue: The value for the effectivity option. Valid option values for given familyNamespace  and
    familyName are available on the effectivity context associated with product Item with relation
    Fnd0ProductEffConfigCxtRel.
    For example, effectivity context with item id EFFCTX001 is associated with product Item. It has option families
    defined with names Maturity Intent and Module Intent. Maturity Intent has values Design and Production. Module
    Intent has values Kit and Modkit. The familyNamespace is set as EFFCTX001. The familyName is set Maturity Intent.
    The optionValue can be either Design or Production.
    """
    familyNamespace: str = ''
    familyName: str = ''
    opCode: int = 0
    optionValue: str = ''
