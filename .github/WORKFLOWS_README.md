# GitHub Actions ワークフロー

このディレクトリには、並列開発システムのCI/CD統合のためのGitHub Actionsワークフローが含まれています。

## 📋 ワークフロー一覧

### 1. code-review.yml - 自動コードレビュー

**トリガー:**
- Pull Request作成時
- Pull Requestへのコミット追加時

**処理内容:**
1. 変更ファイルの検出（.py, .js, .html, .css, .sh）
2. Code Reviewerサブエージェント実行
3. レビューレポート生成・アップロード
4. Critical問題がある場合はPRをfailにする
5. レビュー結果をPRにコメント

**成果物:**
- `code-review-report` - レビューレポート（30日間保持）

**使用例:**
```yaml
# PR作成時に自動実行
# 手動実行は不要
```

### 2. auto-fix.yml - Critical問題の自動修正

**トリガー:**
- code-review.ymlワークフローが失敗した時

**処理内容:**
1. レビューレポートをダウンロード
2. Auto Fixerサブエージェント実行
3. 修正をコミット・プッシュ
4. 修正内容をPRにコメント

**自動修正される問題:**
- SHA256/MD5パスワードハッシュ → bcrypt
- ハードコードされたAPIキー → 環境変数
- SQL Injection → パラメータ化クエリ
- eval()使用 → 削除＋FIXME注釈

**使用例:**
```yaml
# code-review.ymlが失敗すると自動実行
# 手動実行は不要
```

### 3. ui-verification.yml - UI検証

**トリガー:**
- Pull Request作成時
- 手動実行（workflow_dispatch）

**処理内容:**
1. Playwright環境セットアップ
2. デプロイ先URLでスクリーンショット撮影
3. UI検証レポート生成
4. スクリーンショットをアーティファクトにアップロード
5. 検証結果をPRにコメント

**成果物:**
- `ui-verification-results` - スクリーンショット（30日間保持）

**手動実行:**
```bash
# GitHub UIから手動実行
# Actions > UI Verification > Run workflow
# Deployment URLを入力
```

---

## 🚀 セットアップ

### 1. GitHub Actionsの有効化

リポジトリ設定で以下を確認:
- Settings > Actions > General
- "Allow all actions and reusable workflows" を選択

### 2. 必要な権限設定

リポジトリ設定で以下を確認:
- Settings > Actions > General > Workflow permissions
- "Read and write permissions" を選択
- "Allow GitHub Actions to create and approve pull requests" をチェック

### 3. Secretsの設定（オプション）

外部サービス連携が必要な場合:
- Settings > Secrets and variables > Actions
- 必要なSecretsを追加

---

## 📊 ワークフロー実行結果の確認

### PRでの確認

Pull Requestページで以下を確認できます:

**Checksタブ:**
- 各ワークフローの実行状態
- エラーログ
- 実行時間

**Conversationタブ:**
- 自動レビュー結果のコメント
- 自動修正結果のコメント
- UI検証結果のコメント

**Files changedタブ:**
- 自動修正された変更内容

### Actionsタブでの確認

リポジトリのActionsタブで以下を確認できます:

- 全ワークフローの実行履歴
- 実行ログの詳細
- アーティファクトのダウンロード

---

## 🔧 カスタマイズ

### レビュー対象ファイルの変更

`.github/workflows/code-review.yml` の `files` セクションを編集:

```yaml
- name: Get changed files
  id: changed-files
  uses: tj-actions/changed-files@v39
  with:
    files: |
      **/*.py
      **/*.js
      **/*.ts     # TypeScript追加
      **/*.jsx    # React追加
```

### デプロイURLの設定

`.github/workflows/ui-verification.yml` のデフォルトURLを変更:

```yaml
- name: Determine deployment URL
  id: deploy-url
  run: |
    echo "url=https://your-production-url.com" >> $GITHUB_OUTPUT
```

### レビュールールのカスタマイズ

プロジェクトルートに `.reviewrc.json` を作成:

```json
{
  "rules": {
    "security": {
      "password_hash": {
        "severity": "critical",
        "allowed": ["bcrypt", "argon2"]
      }
    }
  }
}
```

---

## 🐛 トラブルシューティング

### ワークフローが実行されない

**原因:** GitHub Actionsが無効化されている

**解決策:**
1. Settings > Actions > General
2. "Allow all actions and reusable workflows" を選択

### 自動コミットが失敗する

**原因:** Workflow permissionsが不足

**解決策:**
1. Settings > Actions > General > Workflow permissions
2. "Read and write permissions" を選択

### PRコメントが投稿されない

**原因:** "Allow GitHub Actions to create and approve pull requests" が無効

**解決策:**
1. Settings > Actions > General
2. "Allow GitHub Actions to create and approve pull requests" をチェック

### レビューレポートが生成されない

**原因:** Pythonスクリプトのパスエラー

**解決策:**
ワークフローログを確認し、パスを修正:
```yaml
run: python review/code_reviewer.py ...
```

---

## 📚 参考リンク

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [tj-actions/changed-files](https://github.com/tj-actions/changed-files)
- [Playwright Documentation](https://playwright.dev/)

---

**作成日**: 2025-11-26  
**バージョン**: 1.0
