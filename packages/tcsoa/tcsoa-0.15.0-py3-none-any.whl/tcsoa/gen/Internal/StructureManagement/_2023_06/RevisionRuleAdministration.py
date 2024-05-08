from __future__ import annotations

from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RevRuleEntryInfo2(TcBaseObj):
    """
    Structure representing an entry or clause in a RevisionRule.
    
    :var entryType: Indicates type of the rule entry of a RevisionRule. A RevisionRule is made up of a sequential list
    of entries. Evaluation of the rule involves evaluating each of the entries, in order, until a configured revision
    of the Item is successfully obtained. A rule is made up of  following "EntryType".
    0 - Working
    1 - Status
    2 - Override
    3 - Date
    4 - Unit No.
    5 - Group
    6 - Precise
    7 - Latest
    8 - End Item
    9 - GroupByItemType
    10 - Branch.
    :var displayText: Display text of the entry.
    :var revRuleEntryKeyToValue: A map (string, string) of entry name-value pairs. Following are the allowed key-value
    pair as per "EntryType".
    "Working":
        "user" &ndash; UID of User
        "group" &ndash; UID of Group
        "current_user" &ndash; "true"
        "current_group" &ndash; "true"
    "Status":
        "status_type" &ndash; UID of status (TaskType) or "Any"
        "config_type" &ndash; "0" (configured using released date) or
                                   "1" (configured using effective date) or
                                   "2" (configured using unit no.)
    "Override":
        "folder" &ndash; UID of Folder.
    "Date":
        "date" &ndash; date in format "yyyy-mm-ddThh:mm:ss"
        "today" &ndash; "true"
    "Unit No.":
        "unit_no" &ndash; number
    "Latest":
        "latest" &ndash; "0" (latest by creation date) or
                        "1" (latest by alphanumeric rev id) or
                        "2" (latest by numeric rev id) or
                        "3" (latest by alpha plus number rev id)
    "End Item":
        "end_item" &ndash; UID of Item.
        "end_item_rev" &ndash; UID of ItemRevision.
    "Branch":
        "branch" &ndash; UID of Fnd0Branch.
    :var groupEntryInfo: Information about group entry. This structure is populated only in case of entry type being
    any of the supported group type entries. For example: CFMGroupEntry, CFMGroupItemTypeEntry and
    Fnd0CFMGroupOccTypeEntry.
    """
    entryType: int = 0
    displayText: str = ''
    revRuleEntryKeyToValue: MapOfRevRuleEntryKeyToValue2 = None
    groupEntryInfo: RevRuleGroupEntryInfo2 = None


@dataclass
class RevRuleGroupEntryInfo2(TcBaseObj):
    """
    Structure to hold an information about group entry.
    
    :var groupByTypes: A list containing display names of types of Item or PSOccurrence on which this rule entry is to
    be evaluated. This will be populated in cases of entry type being CFMGroupItemTypeEntry or
    Fnd0CFMGroupOccTypeEntry. For example: If CFMGroupItemTypeEntry, the list can contain display names of item types:
    AllocationMap, CAEBCItem, CAEConnItem, and CAEItem.
    :var listOfSubEntries: A list of entries that are grouped together.
    """
    groupByTypes: List[str] = ()
    listOfSubEntries: List[RevRuleEntryInfo2] = ()


@dataclass
class RevRuleInfoResponse2(TcBaseObj):
    """
    This structure contains all information about a RevisionRule.
    
    :var revisionRuleInfo: Information about revision rule.
    """
    revisionRuleInfo: RevisionRuleInfo2 = None


@dataclass
class RevisionRuleInfo2(TcBaseObj):
    """
    Structure with information about RevisionRule such as name, description, rule entries, etc.
    
    :var uid: Unique Identifier (UID) of a RevisionRule to be created or updated.
    :var name: Name of the RevisionRule.
    :var description: Description of a RevisionRule.
    :var entriesInfo: A list containing entries in a RevisionRule.
    :var nestedEffectivity: If true, nested effectivity is added to RevisionRule. If nested effectivity is added,
    Teamcenter evaluates nested effectivities as per EffectivityMapping on ItemRevision.
    :var isPrivate: If true, RevisionRule is available only to the user who has created it. In this case, a runtime
    property suppressed on a RevisionRule will be set. A combination of properties suppressed and owning user will be
    used to decide if a RevisionRule is available to the user or not.
    """
    uid: str = ''
    name: str = ''
    description: str = ''
    entriesInfo: List[RevRuleEntryInfo2] = ()
    nestedEffectivity: bool = False
    isPrivate: bool = False


@dataclass
class CreateOrUpdateRevRuleInput2(TcBaseObj):
    """
    Input structure required to create or update RevisionRule.
    
    :var updateExisting: If true, an existing RevisionRule will be updated else a new RevisionRule will be created.
    :var revisionRuleInfo: Information on RevisionRule to be created or updated.
    """
    updateExisting: bool = False
    revisionRuleInfo: RevisionRuleInfo2 = None


@dataclass
class CreateOrUpdateRevRuleResp2(TcBaseObj):
    """
    Returns information on created or updated RevisionRule along with service data containing created or updated
    objects.
    
    :var revisionRuleInfo: Information about created or updated RevisionRule.
    :var serviceData: ServiceData with created or updated objects and partial errors.
    """
    revisionRuleInfo: RevisionRuleInfo2 = None
    serviceData: ServiceData = None


"""
A map (string, string) of entry name-value pairs. 
For example,
1: For entry type "Working", the map will contain "user", and "group" as keys and UIDs of User and Group as values respectively.
2: For entry type "Status", the map will contain "status_type" as key and UID of attached status  (TaskType). 
3: For entry type "Override", the map will contain "folder" as key and UID of the Folder object.
"""
MapOfRevRuleEntryKeyToValue2 = Dict[str, str]
