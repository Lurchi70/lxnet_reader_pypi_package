import unittest
from unittest import mock

from unittest.mock import MagicMock, patch
from lxnet_reader.lxnet_reader import LXNetReader

def mocked_socket(*args, **kwargs):
    class MockSocket:
        recv_data : str
        def __init__(self):
            self.recv_data = "abc"

        def connect(self, connectTo):
            return

        def close(self):
            return
            
        def send(self, sendData):
            return
        
        def recv(self):
            return "abc"

    return MockSocket


class TestValidator(unittest.TestCase):
    @patch("socket.socket", side_effect=mocked_socket)
    def test_query_host_negative(self, mock_socket):
        """Test host validator with a not existing host"""

        testPassed = False
        try:
            o = LXNetReader("4.3.2.1", "", "")
        except:
            testPassed = True

        self.assertFalse(testPassed)

#    @mock.patch('requests.get', side_effect=mocked_requests_get)
#    @mock.patch('defusedxml.ElementTree.parse', side_effect=mocked_elementtree_parse)
#    def test_check_data_elements(self, mock_get, mock_parse):
#        """Test is all supported data element are in the dictionary"""        
#        o = SC2XMLReader("http://existing_device.local", DEFAULT_USERNAME, DEFAULT_PASSWORD)

#        for value in o.MAP_SOLVIS_TO_NAME.values():
#            self.assertIsNotNone(o.data[value])


