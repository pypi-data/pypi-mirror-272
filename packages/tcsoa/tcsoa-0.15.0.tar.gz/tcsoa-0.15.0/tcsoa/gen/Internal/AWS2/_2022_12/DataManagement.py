from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2018_05.DataManagement import TileIcons, Action, ContentEntry
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetCurrentUserGateway3Response(TcBaseObj):
    """
    GetCurrentUserGateway2Response view model to be presented by the client. The response consists of TileGroup2
    objects which contain Tile2 objects in the order they should be presented in the Gateway. Each Tile2 object
    contains a reference to the Awp0GatewayTileRel so the Tile2 may be operated on.
    
    :var serviceData: Contains partial error information.
    :var tileGroups: List of TileGroup2 to be presented in the Gateway.
    """
    serviceData: ServiceData = None
    tileGroups: List[TileGroup2] = ()


@dataclass
class Tile2(TcBaseObj):
    """
    Contains all the information relevant to presenting and operating on the Tile2 object in the UI.
    
    :var action: The action to execute when the Tile2 is clicked.
    :var icons: Defines the primary and secondary icons to be presented in the Gateway.
    :var themeIndex: The integer that indicates the theme for color of the Tile2. Valid values are 0: light, 1 medium,
    2: highlight, 3: alternate.
    :var isProtected: Indicates whether a Tile2 may be removed from a TileGroup2. If true, a Tile2 object cannot be
    removed from a TileGroup2. If false, a Tile2 object can be removed from a TileGroup2.
    :var content: Defines the live content to be displayed on a Tile2. Each entry is a line on the Tile2.
    :var validSizes: A list of sizes of the Tile2 that this template supports. Can be used to limit available sizes for
    a tile type - if blank, all sizes are allowed. Valid values are 0: small, 1: wide, 2: large.
    :var displayName: The display name of the Tile2 object.
    :var styleOverride: This property indicates any CSS classes to override the default styling of the Tile2.
    :var relUID: The UID of the Awp0GatewayTileRel object which describes the Tile2 or TileGroup2 information.
    :var tileID: The unique ID of the Tile2 object.
    :var tileSize: Size of the Tile2. Valid values are 0, 1, or 2 (small, wide, or large).Null value not allowed.
    :var orderNumber: The order number for which this Tile2 should be presented in the Gateway.
    """
    action: Action = None
    icons: TileIcons = None
    themeIndex: int = 0
    isProtected: bool = False
    content: List[ContentEntry] = ()
    validSizes: List[int] = ()
    displayName: str = ''
    styleOverride: str = ''
    relUID: str = ''
    tileID: str = ''
    tileSize: int = 0
    orderNumber: int = 0


@dataclass
class TileGroup2(TcBaseObj):
    """
    Contains the group name to be presented in the UI, as well as the vector of Tile2 objects to be presented in the
    UI. The Tile2 objects are ordered based on awp0OrderNo property on the Awp0GatewayTileRel object.
    
    :var tiles: The Tile2 objects to be presented in the TileGroup2.
    :var groupName: The name of the TileGroup2.
    """
    tiles: List[Tile2] = ()
    groupName: str = ''
