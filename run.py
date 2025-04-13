#!/usr/bin/env python
"""
Claude Desktop設定エディタの単独実行スクリプト
"""

import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# メイン関数をインポート
from src.main import main

if __name__ == "__main__":
    # アプリケーションを起動
    main()
