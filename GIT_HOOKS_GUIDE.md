# Git Hooks 統合ガイド

Git Hook統合により、コミット・プッシュ時に自動的にコードレビュー・UI検証が実行されます。

---

## 🚀 クイックスタート

### 1. Git Hooksインストール

```bash
cd C:\Users\Tenormusica\claude-worktree-parallel-dev
./scripts/install-hooks.sh
```

これで以下のhooksが自動的にインストールされます:
- `pre-commit`: コミット前に自動レビュー実行
- `post-commit`: コミット後にレビューサブエージェント起動提案
- `pre-push`: プッシュ前にレビュー状態確認

### 2. 通常通り開発

```bash
# 機能開発
git checkout -b feature/my-feature

# コード編集
vim src/my_code.py

# コミット（自動レビューが実行される）
git add .
git commit -m "Add new feature"

# プッシュ（レビュー状態を確認）
git push origin feature/my-feature
```

---

## 📋 各Hookの動作詳細

### pre-commit（コミット前チェック）

**実行タイミング:** `git commit` 実行時

**処理フロー:**
1. 変更ファイルの検出
2. コードファイル（.py, .js, .html, .css, .sh）のみレビュー実行
3. `review/code_reviewer.py` で自動レビュー
4. Critical問題検出時:
   - ✅ **自動修正を提案** (y/n/skip)
   - `y` → 自動修正実行 → コミット中断（修正後に再コミット）
   - `n` → コミット中断
   - `skip` → レビューをスキップしてコミット続行

**出力例:**
```
🔍 [pre-commit] コミット前レビューを開始...
🔍 [pre-commit] 変更ファイル:
  - src/user_auth.py
🔍 [pre-commit] コードレビューを実行中...
❌ [pre-commit] Critical問題が検出されました
⚠️  [pre-commit] 自動修正を試行しますか? (y/n/skip)
```

### post-commit（コミット後処理）

**実行タイミング:** `git commit` 完了後

**処理フロー:**
1. コミット情報の表示（ブランチ名・コミットハッシュ）
2. `feature/*` ブランチの場合:
   - 詳細レビューの提案（Code Reviewerサブエージェント起動コマンド表示）
3. GitHub Issueへの自動報告提案

**出力例:**
```
📝 [post-commit] コミット後処理を開始...
📝 [post-commit] ブランチ: feature/user-auth
📝 [post-commit] コミット: a1b2c3d
📝 [post-commit] 詳細レビューを実行しますか? (y/n)
```

### pre-push（プッシュ前チェック）

**実行タイミング:** `git push` 実行時

**処理フロー:**
1. 最近のレビューレポート確認（過去24時間以内）
2. レビューレポートがない場合:
   - レビュー実行を推奨
   - レビューなしでプッシュ続行の確認
3. 未承認レビューがある場合:
   - Critical問題の修正を推奨
   - 強制プッシュの確認
4. UI検証の実施確認

**出力例:**
```
🚀 [pre-push] プッシュ前チェックを開始...
🚀 [pre-push] ブランチ: feature/user-auth
⚠️  [pre-push] 最近のレビューレポートが見つかりません
⚠️  [pre-push] レビューなしでプッシュを続行しますか? (y/n)
```

---

## 🔧 自動修正機能

`review/auto_fixer.py` が以下の問題を自動修正します:

### 修正可能な問題

1. **パスワード平文保存**
   - SHA256 → bcrypt自動変換
   - `import bcrypt` 自動追加

2. **eval()使用**
   - `eval()` をコメントアウト
   - FIXME注釈追加

3. **SQL Injection**
   - 文字列連結 → プリペアドステートメント変換

4. **APIキーハードコード**
   - ハードコード → `os.environ.get("API_KEY")` 変換
   - `import os` 自動追加

### 使い方

```bash
# 手動実行（レビューレポートを指定）
python review/auto_fixer.py review-reports/review-feature-name-2025-11-26.md

# 自動実行（pre-commitで自動的に実行される）
git commit -m "Your message"
# → Critical問題検出 → 自動修正提案 → y を選択
```

---

## ⚙️ カスタマイズ

### Hookを無効化

一時的にhookをスキップする場合:

```bash
# pre-commitをスキップ
git commit --no-verify -m "Skip pre-commit hook"

# pre-pushをスキップ
git push --no-verify
```

### Hookのアンインストール

```bash
rm .git/hooks/pre-commit
rm .git/hooks/post-commit
rm .git/hooks/pre-push
```

バックアップから復元:

```bash
mv .git/hooks/pre-commit.backup .git/hooks/pre-commit
```

### タイムアウト調整

各hookでユーザー入力を待つタイムアウトはデフォルト10秒です。

変更する場合、各hookファイルの `read -t 10` を編集:

```bash
# タイムアウトを30秒に変更
read -t 30 -r answer || answer="n"
```

---

## 🎯 推奨ワークフロー

### 標準的な開発フロー

```bash
# 1. 機能ブランチ作成
git checkout -b feature/user-authentication

# 2. コード編集・実装
vim src/user_auth.py

# 3. コミット（自動レビューが実行される）
git add .
git commit -m "Add user authentication"
# → pre-commit: 自動レビュー実行
# → Critical問題検出時は自動修正提案
# → post-commit: 詳細レビュー提案

# 4. 詳細レビュー（オプション）
./scripts/parallel-dev-flow.sh review user-authentication

# 5. プッシュ（レビュー状態確認）
git push origin feature/user-authentication
# → pre-push: レビューレポート確認
# → 未承認レポートがあれば警告

# 6. UI検証（Webアプリの場合）
./scripts/parallel-dev-flow.sh ui-test user-authentication https://my-app.run.app

# 7. マージ
./scripts/parallel-dev-flow.sh merge user-authentication
```

---

## 🐛 トラブルシューティング

### Hookが実行されない

**原因:** 実行権限がない

**解決策:**
```bash
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/post-commit
chmod +x .git/hooks/pre-push
```

### code_reviewer.pyが見つからない

**原因:** Worktree構造が正しくない

**解決策:**
```bash
# プロジェクトルートで実行
ls review/code_reviewer.py

# 存在しない場合
git checkout implementation/minimal-setup
```

### 自動修正が動作しない

**原因:** Pythonパスが正しくない

**解決策:**
```bash
# Python 3が正しくインストールされているか確認
python3 --version

# auto_fixer.pyに実行権限があるか確認
chmod +x review/auto_fixer.py
```

---

## 📚 関連ドキュメント

- [README.md](README.md) - プロジェクト全体概要
- [PROJECT_SPECIFICATION.md](PROJECT_SPECIFICATION.md) - 詳細仕様
- [demo-project/README.md](demo-project/README.md) - デモプロジェクト使用方法

---

**作成日**: 2025-11-26  
**バージョン**: 1.0
