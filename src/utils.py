"""
ユーティリティモジュール。
様々なヘルパー関数を提供します。
"""

import os
import datetime
import platform
import json
from pathlib import Path


def find_config_file():
    """
    デフォルトの場所から設定ファイルを探します。
    
    Returns:
        Path: 見つかった設定ファイルのパス、見つからない場合はNone
    """
    # OS別のデフォルトパスを確認
    if platform.system() == 'Windows':
        # Windows
        appdata = os.environ.get('APPDATA', '')
        paths = [
            Path(appdata) / 'Claude Desktop' / 'claude_desktop_config.json',
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Claude Desktop' / 'claude_desktop_config.json',
        ]
    elif platform.system() == 'Darwin':
        # macOS
        paths = [
            Path.home() / 'Library' / 'Application Support' / 'Claude Desktop' / 'claude_desktop_config.json',
        ]
    else:
        # Linux/その他
        paths = [
            Path.home() / '.config' / 'Claude Desktop' / 'claude_desktop_config.json',
        ]
    
    # 存在するパスを返す
    for path in paths:
        if path.exists():
            return path
    
    return None


def create_backup_dir(base_dir):
    """
    バックアップディレクトリを作成します。
    
    Args:
        base_dir (Path): 基本ディレクトリ
    
    Returns:
        Path: バックアップディレクトリのパス
    """
    backup_dir = base_dir / 'backup'
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def get_timestamp():
    """
    現在の日時からタイムスタンプ文字列を生成します。
    
    Returns:
        str: タイムスタンプ文字列（YYYYMMDDHHMMSS形式）
    """
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def generate_backup_filename(original_filename):
    """
    オリジナルのファイル名からバックアップファイル名を生成します。
    
    Args:
        original_filename (str): オリジナルのファイル名
    
    Returns:
        str: バックアップファイル名
    """
    base_name = Path(original_filename).stem
    timestamp = get_timestamp()
    return f"{base_name}_backup_{timestamp}.json"


def ensure_directory_exists(directory_path):
    """
    ディレクトリが存在することを確認し、存在しない場合は作成します。
    
    Args:
        directory_path (str or Path): 確認するディレクトリのパス
    
    Returns:
        bool: ディレクトリが存在するか作成されたかどうか
    """
    path = Path(directory_path)
    if not path.exists():
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception:
            return False
    return True


def is_valid_directory(path):
    """
    指定されたパスが有効なディレクトリかどうかを確認します。
    
    Args:
        path (str): 確認するパス
    
    Returns:
        bool: 有効なディレクトリであるかどうか
    """
    try:
        return os.path.isdir(path)
    except Exception:
        return False


def is_valid_json_file(path):
    """
    指定されたパスが有効なJSONファイルかどうかを確認します。
    
    Args:
        path (str): 確認するパス
    
    Returns:
        bool: 有効なJSONファイルであるかどうか
    """
    try:
        with open(path, 'r') as f:
            json.load(f)
        return True
    except Exception:
        return False
