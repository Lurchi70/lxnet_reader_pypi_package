
from lxnet_reader_dev.lxnet_reader import LXNetReader

import pprint

class LocalDemo:    
    def __init__(self, host:str):
        self.host = host
        self.remote = LXNetReader(host, "", "")


    def ShowSystemInfo(self):
        pprint.pprint("System Info ---------------------------")
        pprint.pprint("""   Location: {0}""".format(self.remote.data["location"]["Value"]))
        pprint.pprint("""   Operator: {0}""".format(self.remote.data["operator"]["Value"]))

    def ShowTank1Info(self):
        pprint.pprint("Tank 1 Info ---------------------------")
        pprint.pprint("""   Name: {0}""".format(self.remote.data["tank_name"]["Value"]))
        pprint.pprint("""   Size: {0}""".format(self.remote.data["tank_size"]["Value"]))
        pprint.pprint("""   Level: {0}""".format(self.remote.data["tank_level"]["Value"]))
        pprint.pprint("""   Clearance: {0}""".format(self.remote.data["tank_clearance"]["Value"]))
        pprint.pprint("""   Level Percent: {0}""".format(self.remote.data["tank_level_percent"]["Value"]))
        pprint.pprint("""   Alarm: {0}""".format(self.remote.data["tank_alarm"]["Value"]))

if __name__ == '__main__':
    o = LocalDemo('192.168.100.82')

    o.ShowSystemInfo()
    o.ShowTank1Info()
