# GitHubリポジトリ手動セットアップ手順

GitHub CLI認証問題により、手動でリポジトリを作成・プッシュする手順を記載します。

---

## 📝 手順

### 1. GitHubでリポジトリ作成

1. ブラウザで [GitHub](https://github.com) にアクセス
2. 右上の「+」→「New repository」をクリック
3. 以下の情報を入力:

   - **Repository name**: `claude-worktree-parallel-dev`
   - **Description**: `Claude Code + Git Worktree 並列開発システム: メイン開発・コードレビュー・UI検証を完全並列実行する革新的な開発フロー`
   - **Visibility**: Public
   - **Initialize this repository with**: チェックなし（既存のローカルリポジトリをプッシュするため）

4. 「Create repository」をクリック

### 2. リモートリポジトリ追加・プッシュ

GitHubリポジトリ作成後、以下のコマンドを実行:

```bash
# リモートリポジトリ追加
cd "C:\Users\Tenormusica\claude-worktree-parallel-dev"
git remote add origin https://github.com/Tenormusica2024/claude-worktree-parallel-dev.git

# ブランチ名をmasterからmainに変更（GitHub標準）
git branch -M main

# 初回プッシュ
git push -u origin main
```

### 3. 確認

ブラウザでリポジトリURLにアクセスして確認:
```
https://github.com/Tenormusica2024/claude-worktree-parallel-dev
```

以下のファイルが表示されていればOK:
- ✅ README.md
- ✅ PROJECT_SPECIFICATION.md
- ✅ MANUAL_GITHUB_SETUP.md

---

## 🔐 認証問題の解決（オプション）

今後GitHub CLIを使用する場合、以下の手順で認証を再設定:

```bash
# 既存の認証をクリア
"C:\Program Files\GitHub CLI\gh.exe" auth logout

# 再度ログイン
"C:\Program Files\GitHub CLI\gh.exe" auth login

# プロンプトに従って設定:
# - GitHub.com
# - HTTPS
# - Authenticate Git with your GitHub credentials: Yes
# - Login with a web browser
```

---

## 📚 参考

- [GitHub公式: リポジトリ作成](https://docs.github.com/ja/get-started/quickstart/create-a-repo)
- [GitHub CLI公式: 認証](https://cli.github.com/manual/gh_auth_login)

---

**作成日**: 2025-11-26
