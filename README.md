# Claude Desktop 設定変更プログラム

このプログラムは、Claude Desktopの設定ファイル `claude_desktop_config.json` 内のパス設定を簡単に変更するためのGUIツールです。

## 概要

Claude Desktopの設定ファイル内の `mcpServers.filesystem.args` パス設定を視覚的に簡単に変更できるようにするツールです。特に、ファイルシステムのパス設定を頻繁に変更する必要がある場合に便利です。

## 機能

- 設定ファイルの読み込みと表示
- パス設定の視覚的な編集
- ディレクトリブラウザによる簡単なパス選択
- 設定の保存と自動バックアップ
- プロファイル管理機能
- エラーハンドリングとユーザーフィードバック

## 技術スタック

- Python 3.8+
- tkinter (GUI)
- JSON処理
- 仮想環境 (venv)
- PyInstaller (パッケージング)

## 簡単な使い方

1. プログラムを起動します
2. 現在のClaude Desktop設定ファイルが自動的に読み込まれ、現在のパスが表示されます
3. 新しいパスを直接入力するか、「参照」ボタンをクリックしてディレクトリを選択します
4. 「保存」ボタンをクリックして設定を保存します
5. 元の設定ファイルは自動的にバックアップされます

## インストール方法

### 方法1: 実行ファイル（.exe）を使用する

1. リリースページから最新の `.exe` ファイルをダウンロードします
2. ダウンロードしたファイルをダブルクリックして実行します

### 方法2: ソースコードから実行する

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/claude-config-editor.git
cd claude-config-editor

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化（Windows）
venv\Scripts\activate

# 必要なパッケージをインストール
pip install -r requirements.txt

# プログラムを実行
python -m src.main
```

詳細な情報については、以下のドキュメントを参照してください：

- [インストール方法](INSTALL.md)
- [使用方法](USAGE.md)
- [開発者向け情報](DEVELOPMENT.md)

## ライセンス

MITライセンスの下で公開されています。詳細については [LICENSE](LICENSE) ファイルを参照してください。
