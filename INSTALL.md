# インストール方法

## 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

## 方法1: 実行ファイルを使用する（推奨）

1. リリースページから最新の`.exe`ファイルをダウンロードします
2. ダウンロードしたファイルをダブルクリックして実行します

## 方法2: ソースコードから実行する

### 仮想環境のセットアップ

```bash
# プロジェクトディレクトリに移動
cd path/to/claude-config-editor

# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化（Windows）
venv\Scripts\activate

# 必要なパッケージをインストール
pip install -r requirements.txt
```

### プログラムの実行

```bash
# 仮想環境が有効化されていることを確認
python src/main.py
```

## 方法3: pipを使用してインストール

```bash
# インストール
pip install claude-config-editor

# 実行
claude-config-editor
```

## トラブルシューティング

- **エラー: tkinterが見つかりません** - Pythonインストール時にtkinterモジュールが含まれていることを確認してください
- **設定ファイルにアクセスできません** - 適切な権限があることを確認してください
- **その他の問題** - Issueを作成してサポートを求めてください
