"""
設定モジュールのテスト
"""

import unittest
import json
import os
import tempfile
from pathlib import Path
import sys

# モジュールをインポートできるようにシステムパスを調整
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import config


class TestConfig(unittest.TestCase):
    """設定モジュールのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        # テスト用の設定ファイルを作成
        self.test_config = {
            "mcpServers": {
                "filesystem": {
                    "command": "C:\\test\\node.exe",
                    "args": [
                        "C:\\test\\index.js",
                        "C:\\test\\target"
                    ]
                }
            }
        }
        
        # 一時ファイルを作成
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_file = Path(self.temp_dir.name) / 'test_config.json'
        
        with open(self.config_file, 'w') as f:
            json.dump(self.test_config, f)
    
    def tearDown(self):
        """テスト後のクリーンアップ"""
        # 一時ディレクトリを削除
        self.temp_dir.cleanup()
    
    def test_load_config(self):
        """設定読み込み機能のテスト"""
        # 設定を読み込む
        loaded_config = config.load_config(self.config_file)
        
        # 読み込んだ設定が元の設定と一致するか確認
        self.assertEqual(loaded_config, self.test_config)
    
    def test_get_mcp_path(self):
        """パス取得機能のテスト"""
        # 現在のパスを取得
        path = config.get_mcp_path(self.test_config)
        
        # 期待されるパスと一致するか確認
        self.assertEqual(path, "C:\\test\\target")
    
    def test_set_mcp_path(self):
        """パス設定機能のテスト"""
        # 新しいパスを設定
        new_path = "C:\\new\\path"
        updated_config = config.set_mcp_path(self.test_config, new_path)
        
        # 設定が更新されているか確認
        self.assertEqual(updated_config['mcpServers']['filesystem']['args'][2], new_path)
        
        # 元の設定オブジェクトも更新されているか確認（参照渡し）
        self.assertEqual(self.test_config['mcpServers']['filesystem']['args'][2], new_path)
    
    def test_validate_config(self):
        """設定検証機能のテスト"""
        # 有効な設定
        valid_config = {
            "mcpServers": {
                "filesystem": {
                    "args": ["arg1", "arg2", "arg3"]
                }
            }
        }
        self.assertTrue(config.validate_config(valid_config))
        
        # 無効な設定（キーが不足）
        invalid_config1 = {
            "wrongKey": {}
        }
        self.assertFalse(config.validate_config(invalid_config1))
        
        # 無効な設定（argsキーがない）
        invalid_config2 = {
            "mcpServers": {
                "filesystem": {}
            }
        }
        self.assertFalse(config.validate_config(invalid_config2))
        
        # 無効な設定（argsが配列でない）
        invalid_config3 = {
            "mcpServers": {
                "filesystem": {
                    "args": "not an array"
                }
            }
        }
        self.assertFalse(config.validate_config(invalid_config3))
        
        # 無効な設定（argsの要素数が不足）
        invalid_config4 = {
            "mcpServers": {
                "filesystem": {
                    "args": ["arg1", "arg2"]
                }
            }
        }
        self.assertFalse(config.validate_config(invalid_config4))


if __name__ == '__main__':
    unittest.main()
