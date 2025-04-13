"""
ユーティリティモジュールのテスト
"""

import unittest
import os
import sys
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

# モジュールをインポートできるようにシステムパスを調整
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import utils


class TestUtils(unittest.TestCase):
    """ユーティリティモジュールのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        # 一時ディレクトリを作成
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
    
    def tearDown(self):
        """テスト後のクリーンアップ"""
        # 一時ディレクトリを削除
        self.temp_dir.cleanup()
    
    def test_get_timestamp(self):
        """タイムスタンプ生成機能のテスト"""
        # タイムスタンプを取得
        timestamp = utils.get_timestamp()
        
        # フォーマットが正しいか確認（14桁の数字）
        self.assertTrue(timestamp.isdigit())
        self.assertEqual(len(timestamp), 14)
    
    def test_generate_backup_filename(self):
        """バックアップファイル名生成機能のテスト"""
        # 元のファイル名
        original_filename = "C:\\test\\config.json"
        
        # 生成されたバックアップファイル名
        with patch('src.utils.get_timestamp', return_value="20251231235959"):
            backup_filename = utils.generate_backup_filename(original_filename)
        
        # 期待されるファイル名と一致するか確認
        self.assertEqual(backup_filename, "config_backup_20251231235959.json")
    
    def test_ensure_directory_exists(self):
        """ディレクトリ存在確認機能のテスト"""
        # 存在するディレクトリ
        self.assertTrue(utils.ensure_directory_exists(self.temp_path))
        
        # 存在しないディレクトリを作成
        new_dir = self.temp_path / "new_dir"
        self.assertTrue(utils.ensure_directory_exists(new_dir))
        self.assertTrue(new_dir.exists())
    
    def test_is_valid_directory(self):
        """ディレクトリ検証機能のテスト"""
        # 有効なディレクトリ
        self.assertTrue(utils.is_valid_directory(self.temp_path))
        
        # 存在しないディレクトリ
        self.assertFalse(utils.is_valid_directory(self.temp_path / "nonexistent"))
        
        # ファイル（ディレクトリではない）
        file_path = self.temp_path / "test_file.txt"
        with open(file_path, 'w') as f:
            f.write("test")
        self.assertFalse(utils.is_valid_directory(file_path))
    
    def test_is_valid_json_file(self):
        """JSONファイル検証機能のテスト"""
        # 有効なJSONファイル
        valid_json_path = self.temp_path / "valid.json"
        with open(valid_json_path, 'w') as f:
            json.dump({"key": "value"}, f)
        self.assertTrue(utils.is_valid_json_file(valid_json_path))
        
        # 無効なJSONファイル
        invalid_json_path = self.temp_path / "invalid.json"
        with open(invalid_json_path, 'w') as f:
            f.write("This is not a valid JSON")
        self.assertFalse(utils.is_valid_json_file(invalid_json_path))
        
        # 存在しないファイル
        self.assertFalse(utils.is_valid_json_file(self.temp_path / "nonexistent.json"))


if __name__ == '__main__':
    unittest.main()
