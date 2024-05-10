# File: test_asset_manager.py

import unittest
import unittest.mock as mock
import sys
sys.path.append('/Users/redpist/dev/perso/sweb/sweb')
from asset_manager import AssetManager


class TestAssetManager(unittest.TestCase):

    @mock.patch('shutil.copytree')
    @mock.patch('shutil.rmtree')
    @mock.patch('os.path.exists', return_value=True)
    def test_copy_assets(self, mock_exists, mock_rmtree, mock_copytree):
        src = "/path/to/source"
        dst = "/path/to/destination"

        manager = AssetManager(src, dst)
        manager.copy_assets()

        mock_exists.assert_called_once_with(dst)
        mock_rmtree.assert_called_once_with(dst)
        mock_copytree.assert_called_once_with(src, dst)

if __name__ == '__main__':
    unittest.main()
