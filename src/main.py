"""
メインモジュール。
アプリケーションのエントリーポイントです。
"""

import tkinter as tk
import sys
import argparse
import os
from pathlib import Path

# GUI関連のインポート
from . import gui
from . import config

def parse_arguments():
    """
    コマンドライン引数を解析します。
    
    Returns:
        argparse.Namespace: 解析された引数
    """
    parser = argparse.ArgumentParser(description='Claude Desktop 設定エディタ')
    parser.add_argument('--config', type=str, help='設定ファイルのパス')
    parser.add_argument('--no-backup', action='store_true', help='バックアップを作成しない')
    
    return parser.parse_args()


def main():
    """
    アプリケーションのメインエントリーポイント
    """
    # コマンドライン引数の解析
    args = parse_arguments()
    
    # tkinterのルートウィンドウを作成
    root = tk.Tk()
    # アイコンファイルがまだ存在しないためコメントアウト
    # root.iconbitmap(default=os.path.join(os.path.dirname(__file__), '../assets/icon.ico'))
    
    # アプリのインスタンスを作成
    app = gui.ConfigEditorApp(root)
    
    # コマンドライン引数から設定ファイルのパスが指定されている場合
    if args.config:
        app.config_path_var.set(args.config)
        app.load_config()
    
    # メインループの実行
    root.mainloop()


if __name__ == "__main__":
    # モジュールとして実行された場合
    main()
