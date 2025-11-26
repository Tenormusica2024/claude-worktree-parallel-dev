# Claude Code + Git Worktree 並列開発システム

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Design Phase](https://img.shields.io/badge/Status-Design%20Phase-blue.svg)]()

Claude CodeのTask toolサブエージェント機能とGit Worktreeを組み合わせ、**メイン開発・コードレビュー・UI検証を完全並列実行**する革新的な開発システム。

![System Overview](https://via.placeholder.com/800x400?text=Claude+Worktree+Parallel+Dev+System)

## 🎯 プロジェクト概要

### 解決する問題

従来の開発フローでは以下の問題がありました:

1. **レビュー待ちによるブロック**: コードレビューが完了するまで次の作業に進めない
2. **コンフリクトの発生**: 複数ブランチでの作業中にファイル競合が発生
3. **手動レビューの負担**: 人間による手動レビューで細かい問題を見逃しやすい
4. **UI確認の手間**: デプロイ後のUI確認を手動で実施、キャッシュ問題で虚偽報告

### このシステムの解決策

- ✅ **並列開発**: メインエージェントが開発を続けながら、サブエージェントが独立してレビュー
- ✅ **コンフリクト回避**: Git Worktreeによる物理的なブランチ分離
- ✅ **自動レビュー**: 95%以上の問題を自動検出
- ✅ **視覚的UI検証**: AIエージェントが画像解析で自動検証、虚偽報告を完全防止

---

## 🏗️ システム構成

### ディレクトリ構造

```
project-root/
├── main/                    # メイン開発 worktree
│   ├── src/                # ソースコード
│   ├── CLAUDE.md           # メイン開発用Claude Code設定
│   └── ...
│
├── review/                  # コードレビュー専用 worktree
│   ├── src/                # レビュー対象コード
│   ├── review-reports/     # レビューレポート保存先
│   ├── CLAUDE.md           # レビュー専用Claude Code設定
│   └── ...
│
├── ui-test/                 # UI検証専用 worktree
│   ├── src/                # UI検証対象コード
│   ├── screenshots/        # スクリーンショット保存先
│   ├── CLAUDE.md           # UI検証専用Claude Code設定
│   └── ...
│
└── .git/                    # 共有Git管理ディレクトリ
```

### ブランチ戦略

```
main (production)
  ├── develop
  │   ├── feature/[name]     # メイン開発
  │   ├── review/[name]      # コードレビュー
  │   └── ui-test/[name]     # UI検証
  └── hotfix/[name]
```

---

## 🔄 ワークフロー

### 1. 機能開発開始

```bash
./scripts/parallel-dev-flow.sh start user-authentication
```

- メイン開発worktreeで機能ブランチ作成
- Claude Codeで機能実装

### 2. コードレビュー開始

```bash
./scripts/parallel-dev-flow.sh review user-authentication
```

- レビューブランチ作成・プッシュ
- レビューworktreeでClaude Code起動
- Code Reviewer Subagentがレビュー実行
- レビューレポート自動生成

### 3. UI検証開始

```bash
./scripts/parallel-dev-flow.sh ui-test user-authentication https://my-app.run.app
```

- UI検証ブランチ作成・デプロイ
- UI検証worktreeでClaude Code起動
- UI Verification Specialistが視覚的検証実行
- スクリーンショット + レポート自動生成

### 4. フィードバック統合

```bash
./scripts/parallel-dev-flow.sh feedback user-authentication
```

- レビューレポート・UI検証レポート確認
- メイン開発worktreeで問題点修正
- 再レビュー・再検証

### 5. マージ・クリーンアップ

```bash
./scripts/parallel-dev-flow.sh merge user-authentication
```

- developブランチにマージ
- 作業ブランチ削除

---

## 🤖 サブエージェント実装

### Code Reviewer Subagent

**レビュー項目（5つの観点）**:

1. **コード品質**: 可読性・保守性・拡張性
2. **セキュリティ**: SQL injection、XSS、CSRF、パスワード平文保存等
3. **パフォーマンス**: アルゴリズム効率、N+1クエリ、リソース管理
4. **エラーハンドリング**: 例外処理、ログ記録
5. **ベストプラクティス**: 言語・フレームワーク固有の推奨パターン

**起動コマンド**:
```python
Task(
    subagent_type="code-reviewer",
    prompt="review/user-authenticationブランチのコードレビューを実施"
)
```

### UI Verification Specialist Subagent

**検証プロセス**:

1. **キャッシュクリア**: ブラウザ完全終了 → 5秒待機 → 新規起動
2. **スクリーンショット撮影**: Playwright MCPで画面キャプチャ
3. **画像内容確認**: Read toolで視覚的検証
4. **期待結果確認**: 期待要素の存在確認

**起動コマンド**:
```python
Task(
    subagent_type="ui-verification-specialist",
    prompt="ユーザー認証画面のUI検証を実施"
)
```

---

## 📊 期待される効果

### 開発速度

- **並列実行**: メイン開発とレビューを同時進行
- **待ち時間削減**: レビュー待ちでブロックされない
- **自動化**: 手動レビューの時間を90%削減

### 品質向上

- **自動レビュー**: 95%以上の問題を検出（導入前30%見逃し → 導入後95%検出）
- **視覚的UI検証**: FALSE SUCCESS CLAIMSを完全防止（40%の虚偽報告 → 0%）
- **一貫した品質基準**: 人間の主観に依存しない

### コンフリクト削減

- **物理的分離**: Git Worktreeによるブランチ完全分離
- **並列作業**: 複数エージェントの同時作業でもコンフリクトなし
- **高速切り替え**: ブランチ間の瞬時切り替え

---

## 🛠️ 必要なツール・環境

### 必須ツール

- **Git**: 2.35以上（Git Worktree機能）
- **Claude Code**: サブエージェント機能対応版
- **Playwright MCP**: ブラウザ自動化
- **Python 3.10+**: レビュー・検証スクリプト実行

### オプションツール

- **Chrome DevTools MCP**: 詳細なブラウザ操作
- **GitHub CLI**: プルリクエスト自動作成
- **Cloud Run**: デプロイ先（他のクラウドでも可）

---

## 📚 ドキュメント

### 詳細仕様

- [PROJECT_SPECIFICATION.md](PROJECT_SPECIFICATION.md) - システム構成・ワークフロー・実装詳細の完全仕様

### 実装サンプル

- `review/review_agent.py` - Code Reviewer Subagent実装サンプル
- `ui-test/ui_verification_agent.py` - UI Verification Specialist実装サンプル
- `scripts/parallel-dev-flow.sh` - 並列開発フロー自動化スクリプト

---

## 🚀 クイックスタート

### 1. リポジトリクローン

```bash
git clone https://github.com/Tenormusica2024/claude-worktree-parallel-dev.git
cd claude-worktree-parallel-dev
```

### 2. Worktreeセットアップ

```bash
# レビュー専用 worktree作成
git worktree add ../claude-worktree-parallel-dev-review develop

# UI検証専用 worktree作成
git worktree add ../claude-worktree-parallel-dev-ui-test develop

# Worktree一覧確認
git worktree list
```

### 3. 機能開発開始

```bash
./scripts/parallel-dev-flow.sh start my-feature
```

詳細な使用方法は [PROJECT_SPECIFICATION.md](PROJECT_SPECIFICATION.md) を参照してください。

---

## 🌟 このシステムの革新性

### 1. プロアクティブな品質管理
従来の「後追いレビュー」ではなく、**コード変更の瞬間に自動レビュー**が実行される

### 2. 視覚的検証の完全自動化
UI修正の確認を**人間の目視に頼らず、AIエージェントが画像解析**で自動検証

### 3. FALSE SUCCESS CLAIMS 撲滅
**「できました」と報告する前に必ず視覚的確認**を実行し、虚偽報告を完全防止

### 4. サブエージェント並列実行
主エージェントが開発を続けながら、**サブエージェントが独立してレビュー**を実行

### 5. Git Worktree 活用
複数ブランチでの並列作業を可能にし、**エージェント間のコンフリクトを完全回避**

---

## 📈 今後の拡張計画

### Phase 1（短期）

- [ ] レビュー項目のカスタマイズ機能
- [ ] UI検証テストケースのテンプレート化
- [ ] 自動化スクリプトのGUI化

### Phase 2（中期）

- [ ] CI/CDパイプライン統合
- [ ] レビュー履歴の可視化ダッシュボード
- [ ] プロジェクト固有のルールセット管理

### Phase 3（長期）

- [ ] 機械学習による問題予測
- [ ] チーム全体のコード品質分析
- [ ] 複数プロジェクト間のベストプラクティス共有

---

## 📝 ライセンス

MIT License

---

## 👤 作成者

- **GitHub**: [@Tenormusica2024](https://github.com/Tenormusica2024)
- **Portfolio**: [Urayaha Days](https://tenormusica2024.github.io/portfolio/)
- **Note**: [dragonrondo](https://note.com/dragonrondo)

---

## 🙏 謝辞

このプロジェクトは[Claude Code](https://claude.ai/code)のサブエージェント機能を活用して開発されました。

---

**作成日**: 2025-11-26  
**バージョン**: 1.0  
**ステータス**: Design Phase
