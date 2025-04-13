"""
GUIモジュールのテスト
"""

import unittest
import os
import sys
import tkinter as tk
from unittest.mock import MagicMock, patch

# モジュールをインポートできるようにシステムパスを調整
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import gui


class TestGUI(unittest.TestCase):
    """GUIモジュールのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        # rootウィンドウをモック化
        self.root = MagicMock()
        
        # configモジュールをパッチ
        self.config_patcher = patch('src.config')
        self.mock_config = self.config_patcher.start()
        
        # デフォルトの設定パスを返すモック
        self.mock_config.get_default_config_path.return_value = "C:\\test\\config.json"
        
        # 設定読み込みのモック
        self.mock_config.load_config.return_value = {
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
        
        # 設定検証のモック
        self.mock_config.validate_config.return_value = True
        
        # パス取得のモック
        self.mock_config.get_mcp_path.return_value = "C:\\test\\target"
    
    def tearDown(self):
        """テスト後のクリーンアップ"""
        # パッチを停止
        self.config_patcher.stop()
    
    @patch('tkinter.messagebox.showerror')
    def test_load_config(self, mock_showerror):
        """設定読み込み機能のテスト"""
        # GUIアプリケーションのインスタンス作成
        app = gui.ConfigEditorApp(self.root)
        
        # 初期化時に自動的に設定が読み込まれるので、モックが呼び出されたか確認
        self.mock_config.load_config.assert_called_once()
        self.mock_config.get_mcp_path.assert_called_once()
        
        # 現在のパスが正しく設定されているか確認
        self.assertEqual(app.current_path_var.get(), "C:\\test\\target")
        
        # エラーメッセージが表示されていないことを確認
        mock_showerror.assert_not_called()
    
    @patch('tkinter.messagebox.showerror')
    def test_load_config_error(self, mock_showerror):
        """設定読み込みエラーのテスト"""
        # 設定読み込み時にエラーを発生させる
        self.mock_config.load_config.side_effect = FileNotFoundError("ファイルが見つかりません")
        
        # GUIアプリケーションのインスタンス作成
        app = gui.ConfigEditorApp(self.root)
        
        # エラーメッセージが表示されたことを確認
        mock_showerror.assert_called_once()
    
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.askyesno')
    def test_save_config(self, mock_askyesno, mock_showinfo):
        """設定保存機能のテスト"""
        # ディレクトリが存在するように設定
        with patch('os.path.exists', return_value=True):
            # GUIアプリケーションのインスタンス作成
            app = gui.ConfigEditorApp(self.root)
            
            # 新しいパスを設定
            app.new_path_var.set("C:\\new\\path")
            
            # 設定を保存
            app.save_config()
            
            # 設定の更新と保存が呼び出されたことを確認
            self.mock_config.set_mcp_path.assert_called_once()
            self.mock_config.save_config.assert_called_once()
            
            # 成功メッセージが表示されたことを確認
            mock_showinfo.assert_called_once()
    
    @patch('tkinter.messagebox.askyesno', return_value=True)
    def test_save_config_with_confirmation(self, mock_askyesno):
        """存在しないパスの場合の確認ダイアログテスト"""
        # ディレクトリが存在しないように設定
        with patch('os.path.exists', return_value=False):
            # GUIアプリケーションのインスタンス作成
            app = gui.ConfigEditorApp(self.root)
            
            # 新しいパスを設定
            app.new_path_var.set("C:\\nonexistent\\path")
            
            # 設定を保存
            app.save_config()
            
            # 確認ダイアログが表示されたことを確認
            mock_askyesno.assert_called_once()
            
            # ユーザーが確認したので、設定の更新と保存が呼び出されたことを確認
            self.mock_config.set_mcp_path.assert_called_once()
            self.mock_config.save_config.assert_called_once()
    
    @patch('tkinter.filedialog.askdirectory', return_value="/test/dir")
    def test_browse_directory(self, mock_askdirectory):
        """ディレクトリ参照機能のテスト"""
        # GUIアプリケーションのインスタンス作成
        app = gui.ConfigEditorApp(self.root)
        
        # 参照ダイアログを呼び出す
        app._browse_directory()
        
        # パスがWindowsフォーマットで設定されたか確認
        self.assertEqual(app.new_path_var.get(), "\\test\\dir")


if __name__ == '__main__':
    unittest.main()
