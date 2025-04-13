"""
GUIモジュール。
tkinterを使用したグラフィカルユーザーインターフェースを提供します。
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from pathlib import Path

# 自作モジュールのインポート
from . import config


class ConfigEditorApp:
    """Claude Desktop設定エディタのメインGUIクラス"""
    
    def __init__(self, root):
        """
        初期化メソッド
        
        Args:
            root (tk.Tk): tkinterのルートウィンドウ
        """
        self.root = root
        self.root.title("Claude Desktop 設定エディタ")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # スタイル設定
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc")
        self.style.configure("TLabel", padding=6)
        self.style.configure("TEntry", padding=6)
        
        # 変数
        self.config_path_var = tk.StringVar()
        self.current_path_var = tk.StringVar()
        self.new_path_var = tk.StringVar()
        self.profile_name_var = tk.StringVar()
        self.status_var = tk.StringVar()
        
        # 設定ファイルのパスをデフォルト値に設定
        self.config_path_var.set(str(config.get_default_config_path()))
        
        # プロファイルリスト
        self.profiles = {}
        
        # UIの作成
        self._create_widgets()
        
        # 初期設定の読み込み
        self.load_config()
    
    def _create_widgets(self):
        """ウィジェットを作成してレイアウトします"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 設定ファイルパス
        path_frame = ttk.LabelFrame(main_frame, text="設定ファイルの場所", padding="10")
        path_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Entry(path_frame, textvariable=self.config_path_var, width=50).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(path_frame, text="参照", command=self._browse_config).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(path_frame, text="読み込み", command=self.load_config).grid(row=0, column=2, padx=5, pady=5)
        
        # 現在のパス
        current_frame = ttk.LabelFrame(main_frame, text="現在のパス設定", padding="10")
        current_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Entry(current_frame, textvariable=self.current_path_var, state="readonly", width=60).pack(fill=tk.X, padx=5, pady=5)
        
        # 新しいパス
        new_frame = ttk.LabelFrame(main_frame, text="新しいパス設定", padding="10")
        new_frame.pack(fill=tk.X, padx=5, pady=5)
        
        entry_frame = ttk.Frame(new_frame)
        entry_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Entry(entry_frame, textvariable=self.new_path_var, width=50).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(entry_frame, text="参照", command=self._browse_directory).grid(row=0, column=1, padx=5, pady=5)
        
        # プロファイル管理（オプション機能）
        profile_frame = ttk.LabelFrame(main_frame, text="プロファイル管理", padding="10")
        profile_frame.pack(fill=tk.X, padx=5, pady=5)
        
        profile_entry_frame = ttk.Frame(profile_frame)
        profile_entry_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(profile_entry_frame, text="プロファイル名:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(profile_entry_frame, textvariable=self.profile_name_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(profile_entry_frame, text="保存", command=self._save_profile).grid(row=0, column=2, padx=5, pady=5)
        
        # プロファイル選択
        self.profile_combobox = ttk.Combobox(profile_entry_frame, state="readonly", width=20)
        self.profile_combobox.grid(row=0, column=3, padx=5, pady=5)
        self.profile_combobox.bind("<<ComboboxSelected>>", self._load_profile)
        
        # アクションボタン
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(button_frame, text="保存", command=self.save_config).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="キャンセル", command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        
        # ステータスバー
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 初期ステータス
        self.status_var.set("準備完了")
        
        # フレームの伸縮設定
        main_frame.columnconfigure(0, weight=1)
        path_frame.columnconfigure(0, weight=1)
        entry_frame.columnconfigure(0, weight=1)
    
    def _browse_config(self):
        """設定ファイルの参照ダイアログを表示"""
        file_path = filedialog.askopenfilename(
            title="設定ファイルを選択",
            filetypes=[("JSON ファイル", "*.json"), ("すべてのファイル", "*.*")]
        )
        if file_path:
            self.config_path_var.set(file_path)
            self.load_config()
    
    def _browse_directory(self):
        """ディレクトリ参照ダイアログを表示"""
        dir_path = filedialog.askdirectory(
            title="ディレクトリを選択"
        )
        if dir_path:
            # Windowsパス形式に変換
            dir_path = Path(dir_path).as_posix().replace('/', '\\')
            self.new_path_var.set(dir_path)
    
    def _save_profile(self):
        """現在のパス設定をプロファイルとして保存"""
        name = self.profile_name_var.get()
        if not name:
            messagebox.showerror("エラー", "プロファイル名を入力してください。")
            return
        
        path = self.new_path_var.get()
        if not path:
            messagebox.showerror("エラー", "新しいパスを設定してください。")
            return
        
        # プロファイルを保存
        self.profiles[name] = path
        self._update_profile_list()
        messagebox.showinfo("成功", f"プロファイル '{name}' を保存しました。")
    
    def _load_profile(self, event=None):
        """選択されたプロファイルを読み込む"""
        name = self.profile_combobox.get()
        if name in self.profiles:
            self.new_path_var.set(self.profiles[name])
            self.status_var.set(f"プロファイル '{name}' を読み込みました。")
    
    def _update_profile_list(self):
        """プロファイルリストを更新"""
        self.profile_combobox['values'] = list(self.profiles.keys())
    
    def load_config(self):
        """設定ファイルを読み込む"""
        try:
            # 設定ファイルのパスを取得
            config_path = self.config_path_var.get()
            if not config_path:
                raise ValueError("設定ファイルのパスが指定されていません。")
            
            # 設定を読み込む
            self.config_data = config.load_config(config_path)
            
            # 設定を検証
            if not config.validate_config(self.config_data):
                raise ValueError("設定ファイルの形式が正しくありません。")
            
            # 現在のパスを取得して表示
            current_path = config.get_mcp_path(self.config_data)
            self.current_path_var.set(current_path)
            
            # 新しいパスの初期値を現在の値に設定
            self.new_path_var.set(current_path)
            
            self.status_var.set("設定を読み込みました。")
        except FileNotFoundError:
            messagebox.showerror("エラー", "設定ファイルが見つかりません。")
            self.status_var.set("エラー: ファイルが見つかりません。")
        except json.JSONDecodeError:
            messagebox.showerror("エラー", "設定ファイルの形式が正しくありません。")
            self.status_var.set("エラー: JSONの形式が不正です。")
        except ValueError as e:
            messagebox.showerror("エラー", str(e))
            self.status_var.set(f"エラー: {str(e)}")
        except Exception as e:
            messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {str(e)}")
            self.status_var.set(f"エラー: {str(e)}")
    
    def save_config(self):
        """設定ファイルを保存する"""
        try:
            # 新しいパスを取得
            new_path = self.new_path_var.get()
            if not new_path:
                raise ValueError("新しいパスが指定されていません。")
            
            # パスが存在するか確認
            if not os.path.exists(new_path):
                if not messagebox.askyesno("警告", f"パス '{new_path}' は存在しません。続行しますか？"):
                    return
            
            # 設定を更新
            updated_config = config.set_mcp_path(self.config_data, new_path)
            
            # 設定を保存
            config_path = self.config_path_var.get()
            config.save_config(updated_config, config_path)
            
            # 現在の設定を更新
            self.current_path_var.set(new_path)
            
            # 成功メッセージ
            messagebox.showinfo("成功", "設定を保存しました。")
            self.status_var.set("設定を保存しました。")
        except KeyError:
            messagebox.showerror("エラー", "設定ファイルの形式が正しくありません。")
            self.status_var.set("エラー: 設定ファイルの形式が不正です。")
        except PermissionError:
            messagebox.showerror("エラー", "ファイルに書き込む権限がありません。")
            self.status_var.set("エラー: 権限がありません。")
        except Exception as e:
            messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {str(e)}")
            self.status_var.set(f"エラー: {str(e)}")


def show_error(title, message):
    """エラーメッセージを表示"""
    messagebox.showerror(title, message)


def show_success(title, message):
    """成功メッセージを表示"""
    messagebox.showinfo(title, message)
