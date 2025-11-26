# デモプロジェクト - ユーザー認証システム

このデモプロジェクトは、Claude Code + Git Worktree 並列開発システムの動作確認用です。

## 構成

- `src/user_auth.py`: ユーザー認証クラス実装

## デモワークフロー

### 1. 機能開発開始

```bash
cd C:\Users\Tenormusica\claude-worktree-parallel-dev
./scripts/parallel-dev-flow.sh start user-auth-demo
```

### 2. コードレビュー実行

```bash
./scripts/parallel-dev-flow.sh review user-auth-demo
```

**期待される検出問題:**
- **セキュリティ**: SHA256は推奨されない（bcryptやArgon2を使用すべき）
- **エラーハンドリング**: データベース操作にtry-exceptが不足

### 3. UI検証（Webアプリケーションの場合）

```bash
./scripts/parallel-dev-flow.sh ui-test user-auth-demo https://example.com
```

### 4. フィードバック確認

```bash
./scripts/parallel-dev-flow.sh feedback user-auth-demo
```

レビューレポート・UI検証レポートを確認して問題を修正します。

### 5. マージ

```bash
./scripts/parallel-dev-flow.sh merge user-auth-demo
```

## 検出される問題の例

このデモコードには意図的に以下の問題が含まれています:

1. **セキュリティ**: パスワードハッシュにSHA256を使用（bcryptやArgon2が推奨）
2. **エラーハンドリング**: データベース接続エラーのハンドリング不足
3. **ベストプラクティス**: 接続管理にwith文を使用していない

Code Reviewer Subagentがこれらの問題を自動検出することを確認できます。
