"""requesting and decode Remote Data. """
from __future__ import absolute_import

import logging

from defusedxml import ElementTree
from io import BytesIO, StringIO

from datetime import datetime
import socket
import time

from .const import DEFAULT_MODEL

_LOGGER = logging.getLogger(__name__)

class LXNetReader:
    """interface class for LX-NET."""

    def __init__(self, host: str, username: str, password: str) -> None:
        """Initialize the data interpreter."""
        self.data = {}

        responseData = ''
        try:
            s = socket.socket()
            s.connect((host, 80))
            s.send(b"GET /xml\r\n")

            chunk = b''
            t_end = time.time() + 5
            while time.time() < t_end:            
                chunk = s.recv(2096)
                if chunk:
                    responseData += chunk.decode()
                if responseData.find("</seqSmartbox>") >= 0:
                    break
                time.sleep(1)
            s.close()
        except Exception as err:
            if responseData:
                pass
            else:
                _LOGGER.info(f"LX-NetReader Exception: {err}")
                return

        it = ElementTree.iterparse(StringIO(responseData))
        for _, el in it:
            if "}" in el.tag:
                el.tag = el.tag.split("}", 1)[1]  # strip all namespaces
            for at in list(el.attrib.keys()):  # strip namespaces of attributes too
                if "}" in at:
                    newat = at.split("}", 1)[1]
                    el.attrib[newat] = el.attrib[at]
                    del el.attrib[at]
        root = it.root

        val1 = self.create_data_entry("time", "", datetime.now(), "")
        self.data["last_update"] = val1

        self.addStringDataFromXML(
            root, "seqHeader/devLocation", "location", "location", ""
        )
        self.addStringDataFromXML(
            root, "seqHeader/devOperator", "operator", "operator", ""
        )
        self.addIntDataFromXML(
            root, "seqPara/para2", "", "alarm_treshold", "alarm_treshold"
        )
        alarm_treshold = self.get_value("alarm_treshold")

        node = root.findall("seqData/seqTanks")
        for subnode in node:
            self.addStringDataFromXML(subnode, "tankName", "tank_name", "tank_name", "")
            self.addIntDataFromXML(
                subnode,
                "seqTankLevel/tankLevel",
                "seqTankLevel/tankUnit",
                "tank_level",
                "tank_level",
            )
            self.addIntDataFromXML(
                subnode,
                "tankPercent",
                "tankPercentUnit",
                "tank_level_percent",
                "tank_level_percent",
            )
            self.addIntDataFromXML(
                subnode,
                "seqTankSize/tankSize",
                "seqTankSize/tankUnit",
                "tank_size",
                "tank_size",
            )
            self.addIntDataFromXML(
                subnode,
                "seqTankClear/tankClearance",
                "seqTankClear/tankUnit",
                "tank_clearance",
                "tank_clearance",
            )
            tank_level_percent = self.get_value("tank_level_percent")
            alarm_treshold = self.get_value("alarm_treshold")
            alarm = False
            if tank_level_percent <= alarm_treshold:
                alarm = True
            value = self.create_data_entry("tank_alarm", "tank_alarm", alarm, "")
            self.data["tank_alarm"] = value

    def addStringDataFromXML(
        self, node: any, tag: str, key: str, name: str, unit: str
    ) -> None:
        node = node.find(tag)
        if node != None:
            value = self.create_data_entry(key, name, node.text, unit)
            self.data[key] = value

    def addIntDataFromXML(
        self, node: any, tagValue: str, tagUnit: str, key: str, name: str
    ) -> None:
        unit = ""
        if len(tagUnit):
            nodeUnit = node.find(tagUnit)
            if nodeUnit != None:
                unit = nodeUnit.text

        nodeValue = node.find(tagValue)
        if nodeValue != None:
            value = self.create_data_entry(key, name, int(nodeValue.text), unit)
            self.data[key] = value

    def get_value(self, element: str) -> int | float | str | datetime | None:
        if element in self.data:
            return self.data[element]["Value"]
        return None

    def get_data(self, element: str) -> dict | None:
        if element in self.data:
            return self.data
        return None

    def get_model(self) -> str:
        return DEFAULT_MODEL

    def create_data_entry(
        self, the_key=None, the_name=None, the_value=None, the_unit=None
    ) -> dict:
        """Return dictionary entry."""
        data_entry = {}
        data_entry["Key"] = the_key
        data_entry["Name"] = the_name
        data_entry["Value"] = the_value
        data_entry["Unit"] = the_unit
        return data_entry