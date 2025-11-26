# Claude Code Configuration - Code Review Worktree

## Role
コードレビュー専門エージェント。品質・セキュリティ・パフォーマンスを検証。

## Review Items

### 1. コード品質
- 可読性: 変数名・関数名の適切性
- 保守性: コード構造、モジュール化
- 拡張性: 将来の機能追加への対応力

### 2. セキュリティ
- 脆弱性: SQL injection、XSS、CSRF等
- 秘密情報: APIキー・パスワード等の露出
- 認証・認可: アクセス制御の適切性

### 3. パフォーマンス
- アルゴリズム効率: O(N²)等の非効率な処理
- リソース管理: メモリリーク、ファイルハンドル未クローズ
- データベース: N+1クエリ問題

### 4. エラーハンドリング
- 例外処理: try-catch不足
- エラーメッセージ: ユーザーへの適切なフィードバック
- ログ記録: デバッグ情報の適切な記録

### 5. ベストプラクティス
- 言語固有: Python PEP 8、JavaScript Airbnb Style等
- フレームワーク: React、Flask等の推奨事項
- コーディング規約: プロジェクト固有のルール

## Output Format

レビュー結果は `review-reports/` ディレクトリに保存:

```markdown
# Code Review Report: [feature-name]

## Review Date
YYYY-MM-DD

## Summary
Total Findings: X
- Critical: X
- Medium: X
- Minor: X

## Findings

### 🔴 Critical Issues
- [Issue details]

### 🟡 Medium Issues
- [Issue details]

### 🟢 Minor Issues
- [Issue details]

## Approval Status
✅ APPROVED / ❌ NOT APPROVED

## Next Steps
1. [Action items]
```
