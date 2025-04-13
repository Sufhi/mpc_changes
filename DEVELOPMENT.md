# 開発者向けドキュメント

## プロジェクト構造

```
claude-config-editor/
├── src/                  # ソースコード
│   ├── __init__.py       # パッケージ初期化
│   ├── main.py           # メインエントリーポイント
│   ├── config.py         # 設定処理モジュール
│   ├── gui.py            # GUIモジュール
│   └── utils.py          # ユーティリティ関数
├── tests/                # テストコード
├── venv/                 # 仮想環境（gitignore対象）
├── requirements.txt      # 依存関係
├── setup.py              # パッケージング設定
├── README.md             # プロジェクト概要
└── LICENSE               # ライセンス情報
```

## 開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/claude-config-editor.git
cd claude-config-editor

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化（Windows）
venv\Scripts\activate

# 開発用の依存関係をインストール
pip install -r requirements-dev.txt
```

## 主要モジュールの説明

### config.py

設定ファイルの読み込み、解析、書き込みを担当します。

主な機能:
- `load_config()`: 設定ファイルを読み込む
- `save_config()`: 設定を保存する
- `backup_config()`: 設定のバックアップを作成する
- `validate_config()`: 設定の検証を行う

### gui.py

グラフィカルユーザーインターフェースを提供します。

主な機能:
- `ConfigEditorApp`: メインのGUIアプリケーションクラス
- `show_error()`: エラーメッセージを表示する
- `show_success()`: 成功メッセージを表示する

### utils.py

ユーティリティ関数を提供します。

主な機能:
- `find_config_file()`: 設定ファイルを探す
- `create_backup_dir()`: バックアップディレクトリを作成する
- `get_timestamp()`: タイムスタンプを生成する

## テスト

```bash
# 全テストを実行
pytest

# 特定のテストを実行
pytest tests/test_config.py
```

## パッケージング

```bash
# PyInstallerでexeを作成
pyinstaller --onefile --windowed src/main.py --name claude-config-editor

# pipパッケージを作成
python setup.py sdist bdist_wheel
```

## コーディング規約

- PEP 8に従ってください
- ドキュメント文字列はGoogle styleで記述してください
- すべての関数とクラスにドキュメント文字列を追加してください
- コミットメッセージは明確で簡潔にしてください

## 貢献方法

1. フォークを作成
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## リリースプロセス

1. バージョン番号を更新 (`setup.py`)
2. CHANGELOGを更新
3. テストを実行して問題がないことを確認
4. リリースブランチを作成 (`release/vX.Y.Z`)
5. パッケージをビルド
6. リリースをタグ付け
7. リリースをアップロード
