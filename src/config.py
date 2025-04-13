"""
設定ファイルを処理するモジュール。
JSON設定ファイルの読み込み、解析、書き込みを担当します。
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime


def get_default_config_path():
    """
    デフォルトの設定ファイルパスを取得します。
    
    Returns:
        Path: デフォルトの設定ファイルパス
    """
    # デフォルトの場所を調べる（Windows環境を想定）
    app_data = os.environ.get('APPDATA', '')
    return Path(app_data) / 'Claude Desktop' / 'claude_desktop_config.json'


def load_config(config_path=None):
    """
    設定ファイルを読み込みます。
    
    Args:
        config_path (Path, optional): 設定ファイルのパス。Noneの場合はデフォルトパスを使用。
    
    Returns:
        dict: 設定データ
        
    Raises:
        FileNotFoundError: 設定ファイルが見つからない場合
        json.JSONDecodeError: JSONの解析エラーがある場合
    """
    if config_path is None:
        config_path = get_default_config_path()
    
    with open(config_path, 'r') as file:
        config = json.load(file)
    
    return config


def save_config(config, config_path=None):
    """
    設定ファイルを保存します。
    
    Args:
        config (dict): 保存する設定データ
        config_path (Path, optional): 設定ファイルのパス。Noneの場合はデフォルトパスを使用。
    
    Returns:
        bool: 保存が成功したかどうか
        
    Raises:
        PermissionError: ファイルへの書き込み権限がない場合
    """
    if config_path is None:
        config_path = get_default_config_path()
    
    # バックアップを作成
    backup_config(config_path)
    
    with open(config_path, 'w') as file:
        json.dump(config, file, indent=4)
    
    return True


def backup_config(config_path):
    """
    設定ファイルのバックアップを作成します。
    
    Args:
        config_path (Path): 設定ファイルのパス
    
    Returns:
        Path: バックアップファイルのパス
    """
    if not os.path.exists(config_path):
        return None
    
    # バックアップディレクトリ
    backup_dir = Path(config_path).parent / 'backup'
    os.makedirs(backup_dir, exist_ok=True)
    
    # タイムスタンプ付きのバックアップファイル名
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = backup_dir / f'claude_desktop_config_backup_{timestamp}.json'
    
    # バックアップをコピー
    shutil.copy2(config_path, backup_file)
    
    return backup_file


def get_mcp_path(config):
    """
    mcpServers.filesystem.argsの最後の要素（パス）を取得します。
    
    Args:
        config (dict): 設定データ
    
    Returns:
        str: 現在設定されているパス
        
    Raises:
        KeyError: 必要なキーが存在しない場合
    """
    try:
        return config['mcpServers']['filesystem']['args'][2]
    except (KeyError, IndexError):
        raise KeyError("設定ファイルに必要なキーが存在しません")


def set_mcp_path(config, new_path):
    """
    mcpServers.filesystem.argsの最後の要素（パス）を変更します。
    
    Args:
        config (dict): 設定データ
        new_path (str): 新しいパス
    
    Returns:
        dict: 更新された設定データ
        
    Raises:
        KeyError: 必要なキーが存在しない場合
    """
    try:
        config['mcpServers']['filesystem']['args'][2] = new_path
        return config
    except (KeyError, IndexError):
        raise KeyError("設定ファイルに必要なキーが存在しません")


def validate_config(config):
    """
    設定が必要な構造を持っているか検証します。
    
    Args:
        config (dict): 設定データ
    
    Returns:
        bool: 有効な設定かどうか
    """
    try:
        # 必要なキーが存在するか確認
        if 'mcpServers' not in config:
            return False
        if 'filesystem' not in config['mcpServers']:
            return False
        if 'args' not in config['mcpServers']['filesystem']:
            return False
        if not isinstance(config['mcpServers']['filesystem']['args'], list):
            return False
        if len(config['mcpServers']['filesystem']['args']) < 3:
            return False
        
        return True
    except Exception:
        return False
