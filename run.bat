@echo off
REM Claude Desktop設定エディタの起動スクリプト

REM 仮想環境が存在するか確認
if exist venv\Scripts\activate (
    REM 仮想環境を有効化して実行
    call venv\Scripts\activate
    python run.py
    call venv\Scripts\deactivate
) else (
    REM 仮想環境がない場合は直接実行
    python run.py
)
