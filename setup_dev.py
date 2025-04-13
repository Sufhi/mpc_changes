#!/usr/bin/env python
"""
開発環境のセットアップスクリプト
"""

import os
import subprocess
import sys
import platform
from pathlib import Path


def setup_venv():
    """
    仮想環境をセットアップする
    """
    print("仮想環境をセットアップしています...")
    
    # 仮想環境のディレクトリ
    venv_dir = "venv"
    
    # 仮想環境が存在するか確認
    if os.path.exists(venv_dir):
        print(f"仮想環境が既に存在します: {venv_dir}")
        return venv_dir
    
    try:
        # 仮想環境を作成
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        print(f"仮想環境を作成しました: {venv_dir}")
        return venv_dir
    except subprocess.CalledProcessError as e:
        print(f"仮想環境の作成に失敗しました: {e}")
        sys.exit(1)


def install_dependencies(venv_dir):
    """
    依存パッケージをインストールする
    
    Args:
        venv_dir (str): 仮想環境のディレクトリ
    """
    print("依存パッケージをインストールしています...")
    
    # OSに応じたpipのパス
    if platform.system() == "Windows":
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
    else:
        pip_path = os.path.join(venv_dir, "bin", "pip")
    
    try:
        # pipをアップグレード
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("pipをアップグレードしました")
        
        # 開発用の依存パッケージをインストール
        subprocess.run([pip_path, "install", "-r", "requirements-dev.txt"], check=True)
        print("開発用の依存パッケージをインストールしました")
    except subprocess.CalledProcessError as e:
        print(f"依存パッケージのインストールに失敗しました: {e}")
        sys.exit(1)


def setup_assets():
    """
    アセットディレクトリをセットアップする
    """
    print("アセットをセットアップしています...")
    
    # アセットディレクトリ
    assets_dir = "assets"
    
    # ディレクトリが存在するか確認
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"アセットディレクトリを作成しました: {assets_dir}")


def main():
    """
    メイン関数
    """
    print("Claude Desktop設定エディタ - 開発環境セットアップ")
    
    # 仮想環境をセットアップ
    venv_dir = setup_venv()
    
    # 依存パッケージをインストール
    install_dependencies(venv_dir)
    
    # アセットをセットアップ
    setup_assets()
    
    print("\n開発環境のセットアップが完了しました！")
    
    # 仮想環境の有効化方法を表示
    if platform.system() == "Windows":
        print("\n仮想環境を有効化するには、以下のコマンドを実行してください:")
        print(f"{venv_dir}\\Scripts\\activate")
    else:
        print("\n仮想環境を有効化するには、以下のコマンドを実行してください:")
        print(f"source {venv_dir}/bin/activate")
    
    print("\nアプリケーションを実行するには、以下のコマンドを実行してください:")
    print("python run.py")


if __name__ == "__main__":
    main()
