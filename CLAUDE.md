# Claude Code Configuration - Main Development Worktree

## Role
メイン機能開発を担当。新機能実装・バグ修正を実施。

## Auto-trigger Protocols

### Code Review Auto-Trigger
重要なコード変更完了後、自動的にcode-reviewerサブエージェントを起動:

```python
Task(
    subagent_type="code-reviewer",
    prompt="最新のコミットに含まれるコードのレビューを実施してください"
)
```

### UI Verification Auto-Trigger
UI/フロントエンド修正完了後、自動的にui-verification-specialistサブエージェントを起動:

```python
Task(
    subagent_type="ui-verification-specialist",
    prompt="デプロイ後のUI修正内容を視覚的に検証してください"
)
```

## Development Guidelines

1. **コミット前チェック**: 重要な変更は必ずレビューサブエージェントを起動
2. **UI修正時**: デプロイ後に必ずUI検証サブエージェントを起動
3. **並列作業**: レビュー・UI検証は別のworktreeで実行（コンフリクト回避）

## Worktree Structure

```
main/           # このworktree（メイン開発）
review/         # コードレビュー専用worktree
ui-test/        # UI検証専用worktree
```
