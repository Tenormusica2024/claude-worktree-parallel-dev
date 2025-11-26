# Claude Code + Git Worktree 並列開発システム

## 🎯 プロジェクト概要

Claude CodeのTask toolサブエージェント機能とGit Worktreeを組み合わせ、**メイン開発・コードレビュー・UI検証を完全並列実行**する開発システム。

### プロジェクト目標

1. **並列開発の実現**: メインエージェントが開発を続けながら、サブエージェントが独立してレビュー
2. **コンフリクト完全回避**: Git Worktreeによる物理的なブランチ分離
3. **自動化された品質管理**: コード変更→レビュー→修正→マージのフロー自動化
4. **視覚的UI検証**: デプロイ後のUI確認を画像解析で自動実行

---

## 🏗️ システム構成

### 1. ディレクトリ構造

```
project-root/
├── main/                    # メイン開発 worktree
│   ├── .git/               # Git管理ディレクトリ
│   ├── src/                # ソースコード
│   ├── CLAUDE.md           # Claude Code設定
│   └── ...
│
├── review/                  # コードレビュー専用 worktree
│   ├── .git/               # 独立したGit作業ディレクトリ
│   ├── src/                # レビュー対象コード
│   ├── review-reports/     # レビューレポート保存先
│   └── ...
│
├── ui-test/                 # UI検証専用 worktree
│   ├── .git/               # 独立したGit作業ディレクトリ
│   ├── src/                # UI検証対象コード
│   ├── screenshots/        # スクリーンショット保存先
│   └── ...
│
└── .git/                    # 共有Git管理ディレクトリ
    └── worktrees/          # Worktree管理情報
```

### 2. ブランチ戦略

```
main (production)
  ├── develop (開発ブランチ)
  │   ├── feature/[feature-name] (機能開発 - main worktree)
  │   ├── review/[feature-name] (レビュー専用 - review worktree)
  │   └── ui-test/[feature-name] (UI検証専用 - ui-test worktree)
  └── hotfix/[issue-name]
```

---

## 🔄 ワークフロー

### Phase 1: プロジェクト初期化

#### 1.1 メインリポジトリのセットアップ

```bash
# 1. プロジェクトディレクトリ作成
mkdir my-project
cd my-project
git init

# 2. 初期コミット
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit"

# 3. 開発ブランチ作成
git checkout -b develop
```

#### 1.2 Worktreeの作成

```bash
# 1. メイン開発 worktree（現在のディレクトリ）
# すでにmainディレクトリとして使用

# 2. レビュー専用 worktree作成
git worktree add ../my-project-review develop

# 3. UI検証専用 worktree作成
git worktree add ../my-project-ui-test develop

# 4. Worktree一覧確認
git worktree list
```

**出力例:**
```
C:/Users/Tenormusica/my-project           abc1234 [develop]
C:/Users/Tenormusica/my-project-review    abc1234 [develop]
C:/Users/Tenormusica/my-project-ui-test   abc1234 [develop]
```

#### 1.3 Claude Code設定ファイル配置

各worktreeに専用のCLAUDE.mdを配置:

**main/CLAUDE.md** (メイン開発用):
```markdown
# Main Development Configuration

## Role
メイン機能開発を担当。新機能実装・バグ修正を実施。

## Auto-trigger
- コミット前に自動的にcode-reviewerサブエージェントを起動
- UI修正時は自動的にui-verification-specialistサブエージェントを起動
```

**review/CLAUDE.md** (レビュー専用):
```markdown
# Code Review Configuration

## Role
コードレビュー専門エージェント。品質・セキュリティ・パフォーマンスを検証。

## Review Items
1. コード品質（可読性・保守性・拡張性）
2. セキュリティ（脆弱性・秘密情報露出）
3. パフォーマンス（アルゴリズム効率・リソース管理）
4. エラーハンドリング（例外処理・ログ記録）
5. ベストプラクティス（言語固有の推奨パターン）
```

**ui-test/CLAUDE.md** (UI検証専用):
```markdown
# UI Verification Configuration

## Role
UI/UX検証専門エージェント。視覚的確認・動作確認を実施。

## Verification Process
1. キャッシュクリア（playwright_close → sleep 5 → playwright_navigate）
2. スクリーンショット撮影（playwright_screenshot）
3. 画像内容確認（Read tool）
4. 期待通りの表示確認
```

---

### Phase 2: 並列開発フロー

#### 2.1 メインエージェント（機能開発）

**実行環境**: `main/` worktree

```bash
# 1. 機能ブランチ作成
cd C:/Users/Tenormusica/my-project
git checkout -b feature/user-authentication

# 2. Claude Codeで機能実装
# → ユーザー認証機能を実装
# → テストコード作成
# → コミット実行

git add .
git commit -m "Implement user authentication feature"

# 3. レビューブランチ作成・プッシュ
git checkout -b review/user-authentication
git push origin review/user-authentication
```

#### 2.2 Code Reviewer Subagent（コードレビュー）

**実行環境**: `review/` worktree

```bash
# 1. レビューブランチに切り替え
cd C:/Users/Tenormusica/my-project-review
git fetch origin
git checkout review/user-authentication

# 2. Claude Codeでレビュー実行
# Task(subagent_type="code-reviewer", prompt="review/user-authenticationブランチのコードレビューを実施")
```

**レビューレポート自動生成** (`review-reports/user-authentication-review.md`):

```markdown
# Code Review Report: User Authentication Feature

## Review Date
2025-11-26

## Summary
Overall Quality: ⭐⭐⭐⭐☆ (4/5)

## Findings

### 🔴 Critical Issues
- **Security**: Password stored in plain text (line 45, auth.py)
  - Recommendation: Use bcrypt or Argon2 for password hashing

### 🟡 Medium Issues
- **Performance**: N+1 query problem in user lookup (line 78, user_service.py)
  - Recommendation: Use `select_related()` or `prefetch_related()`

### 🟢 Minor Issues
- **Code Quality**: Magic number in session timeout (line 23, config.py)
  - Recommendation: Define as constant `SESSION_TIMEOUT_SECONDS = 3600`

## Approval Status
❌ NOT APPROVED - Critical security issues must be fixed

## Next Steps
1. Fix password hashing implementation
2. Optimize database queries
3. Re-submit for review
```

#### 2.3 UI Verification Specialist（UI検証）

**実行環境**: `ui-test/` worktree

```bash
# 1. UI検証ブランチに切り替え
cd C:/Users/Tenormusica/my-project-ui-test
git fetch origin
git checkout ui-test/user-authentication

# 2. デプロイ実行（Cloud Run等）
gcloud run deploy my-app --source . --region=asia-northeast1 --quiet

# 3. Claude CodeでUI検証実行
# Task(subagent_type="ui-verification-specialist", prompt="ユーザー認証画面のUI検証を実施")
```

**UI検証レポート自動生成** (`screenshots/user-authentication-verification.md`):

```markdown
# UI Verification Report: User Authentication

## Test Date
2025-11-26

## Test Environment
- URL: https://my-app-ycqe3vmjva-an.a.run.app
- Browser: Chromium (Playwright)
- Viewport: 1280x720

## Verification Results

### ✅ Login Screen
![Login Screen](login-screen-20251126.png)
- Email input field: Visible ✅
- Password input field: Visible ✅
- Login button: Visible ✅
- "Forgot Password" link: Visible ✅

### ✅ Successful Login
![Dashboard After Login](dashboard-20251126.png)
- User redirected to dashboard ✅
- Welcome message displayed ✅
- Logout button visible ✅

### ❌ Error Handling
![Error Message](error-message-20251126.png)
- ⚠️ Error message not displayed for invalid credentials
- Expected: "Invalid email or password" message
- Actual: No error message shown

## Approval Status
❌ NOT APPROVED - Error handling UI issue

## Next Steps
1. Add error message display for invalid login
2. Re-deploy and re-test
```

---

### Phase 3: フィードバック・修正サイクル

#### 3.1 レビュー結果の統合

```bash
# 1. メイン開発worktreeに戻る
cd C:/Users/Tenormusica/my-project

# 2. レビューレポートを確認
cat ../my-project-review/review-reports/user-authentication-review.md

# 3. UI検証レポートを確認
cat ../my-project-ui-test/screenshots/user-authentication-verification.md

# 4. 修正実施
# → パスワードハッシュ化実装
# → エラーメッセージ表示追加
# → コミット

git add .
git commit -m "Fix: Add password hashing and error message display"
git push origin feature/user-authentication
```

#### 3.2 再レビュー・再検証

```bash
# レビューworktreeで再レビュー
cd C:/Users/Tenormusica/my-project-review
git pull origin feature/user-authentication
# Task(subagent_type="code-reviewer", ...)

# UI検証worktreeで再検証
cd C:/Users/Tenormusica/my-project-ui-test
git pull origin feature/user-authentication
# デプロイ → UI検証
```

#### 3.3 承認・マージ

```bash
# すべての検証が承認されたらマージ
cd C:/Users/Tenormusica/my-project
git checkout develop
git merge feature/user-authentication
git push origin develop

# レビューブランチ・UI検証ブランチ削除
git branch -d review/user-authentication
git branch -d ui-test/user-authentication
git push origin --delete review/user-authentication
git push origin --delete ui-test/user-authentication
```

---

## 🤖 サブエージェント実装詳細

### Code Reviewer Subagent

**起動コマンド**:
```python
Task(
    subagent_type="code-reviewer",
    prompt="""
    review/user-authenticationブランチのコードレビューを実施してください。
    
    レビュー項目:
    1. セキュリティ: 認証・認可の実装確認
    2. コード品質: パスワード処理の安全性
    3. パフォーマンス: データベースクエリの効率性
    4. エラーハンドリング: 例外処理の妥当性
    
    レビューレポートをreview-reports/user-authentication-review.mdに保存してください。
    """
)
```

**実装サンプル** (`review/review_agent.py`):

```python
import os
from pathlib import Path
from datetime import datetime

class CodeReviewAgent:
    def __init__(self, branch_name, worktree_path):
        self.branch_name = branch_name
        self.worktree_path = Path(worktree_path)
        self.report_dir = self.worktree_path / "review-reports"
        self.report_dir.mkdir(exist_ok=True)
    
    def review(self, files_changed):
        """コードレビュー実行"""
        findings = []
        
        for file_path in files_changed:
            # Read toolでファイル読み取り
            content = self._read_file(file_path)
            
            # 各レビュー項目を検証
            findings.extend(self._check_security(file_path, content))
            findings.extend(self._check_code_quality(file_path, content))
            findings.extend(self._check_performance(file_path, content))
            findings.extend(self._check_error_handling(file_path, content))
        
        # レポート生成
        self._generate_report(findings)
        
        return findings
    
    def _check_security(self, file_path, content):
        """セキュリティチェック"""
        findings = []
        
        # パスワード平文保存チェック
        if "password" in content and "hash" not in content:
            findings.append({
                "severity": "critical",
                "category": "security",
                "file": file_path,
                "message": "Password stored in plain text",
                "recommendation": "Use bcrypt or Argon2 for password hashing"
            })
        
        # SQL Injection チェック
        if "execute(" in content and "%" in content:
            findings.append({
                "severity": "critical",
                "category": "security",
                "file": file_path,
                "message": "Potential SQL injection vulnerability",
                "recommendation": "Use parameterized queries"
            })
        
        return findings
    
    def _check_code_quality(self, file_path, content):
        """コード品質チェック"""
        findings = []
        
        # マジックナンバーチェック
        import re
        magic_numbers = re.findall(r'\b\d{4,}\b', content)
        if magic_numbers:
            findings.append({
                "severity": "minor",
                "category": "code_quality",
                "file": file_path,
                "message": f"Magic numbers found: {magic_numbers}",
                "recommendation": "Define as constants"
            })
        
        return findings
    
    def _check_performance(self, file_path, content):
        """パフォーマンスチェック"""
        findings = []
        
        # N+1 query チェック（簡易版）
        if "for" in content and "query" in content:
            findings.append({
                "severity": "medium",
                "category": "performance",
                "file": file_path,
                "message": "Potential N+1 query problem",
                "recommendation": "Use select_related() or prefetch_related()"
            })
        
        return findings
    
    def _check_error_handling(self, file_path, content):
        """エラーハンドリングチェック"""
        findings = []
        
        # try-catch 不足チェック
        if "open(" in content and "try:" not in content:
            findings.append({
                "severity": "medium",
                "category": "error_handling",
                "file": file_path,
                "message": "File operation without try-catch",
                "recommendation": "Add exception handling"
            })
        
        return findings
    
    def _generate_report(self, findings):
        """レビューレポート生成"""
        report_path = self.report_dir / f"{self.branch_name}-review.md"
        
        # 重要度別に分類
        critical = [f for f in findings if f["severity"] == "critical"]
        medium = [f for f in findings if f["severity"] == "medium"]
        minor = [f for f in findings if f["severity"] == "minor"]
        
        # レポート作成
        report = f"""# Code Review Report: {self.branch_name}

## Review Date
{datetime.now().strftime("%Y-%m-%d")}

## Summary
Total Findings: {len(findings)}
- Critical: {len(critical)}
- Medium: {len(medium)}
- Minor: {len(minor)}

Overall Quality: {"⭐" * (5 - len(critical) - len(medium)//2)}

## Findings

### 🔴 Critical Issues
"""
        for f in critical:
            report += f"""
- **{f['category'].title()}**: {f['message']} ({f['file']})
  - Recommendation: {f['recommendation']}
"""
        
        report += "\n### 🟡 Medium Issues\n"
        for f in medium:
            report += f"""
- **{f['category'].title()}**: {f['message']} ({f['file']})
  - Recommendation: {f['recommendation']}
"""
        
        report += "\n### 🟢 Minor Issues\n"
        for f in minor:
            report += f"""
- **{f['category'].title()}**: {f['message']} ({f['file']})
  - Recommendation: {f['recommendation']}
"""
        
        # 承認ステータス
        approval = "✅ APPROVED" if len(critical) == 0 else "❌ NOT APPROVED"
        report += f"\n## Approval Status\n{approval}\n"
        
        # レポート保存
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"Review report saved: {report_path}")
```

### UI Verification Specialist Subagent

**起動コマンド**:
```python
Task(
    subagent_type="ui-verification-specialist",
    prompt="""
    ユーザー認証画面のUI検証を実施してください。
    
    検証項目:
    1. ログイン画面の表示確認
    2. 正常ログイン後の画面遷移確認
    3. エラーメッセージ表示確認
    
    スクリーンショットとレポートをscreenshots/に保存してください。
    """
)
```

**実装サンプル** (`ui-test/ui_verification_agent.py`):

```python
import os
from pathlib import Path
from datetime import datetime

class UIVerificationAgent:
    def __init__(self, app_url, worktree_path):
        self.app_url = app_url
        self.worktree_path = Path(worktree_path)
        self.screenshot_dir = self.worktree_path / "screenshots"
        self.screenshot_dir.mkdir(exist_ok=True)
    
    def verify(self, test_cases):
        """UI検証実行"""
        results = []
        
        for test_case in test_cases:
            result = self._run_test_case(test_case)
            results.append(result)
        
        # レポート生成
        self._generate_report(results)
        
        return results
    
    def _run_test_case(self, test_case):
        """個別テストケース実行"""
        # 1. ブラウザ完全終了（キャッシュクリア）
        playwright_close()
        sleep(5)
        
        # 2. 新規ブラウザ起動
        playwright_navigate(url=self.app_url)
        
        # 3. テスト操作実行
        if test_case["type"] == "login":
            self._perform_login(test_case["credentials"])
        
        # 4. スクリーンショット撮影
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"{test_case['name']}-{timestamp}"
        playwright_screenshot(name=screenshot_name)
        
        # 5. Read toolで画像内容確認
        screenshot_path = f"C:\\Users\\Tenormusica\\Downloads\\{screenshot_name}-*.png"
        image_content = Read(file_path=screenshot_path)
        
        # 6. 期待結果と実際の結果を比較
        result = self._verify_expected_result(test_case, image_content)
        
        return {
            "test_case": test_case["name"],
            "screenshot": screenshot_name,
            "result": result
        }
    
    def _perform_login(self, credentials):
        """ログイン操作実行"""
        playwright_fill(selector="input[type='email']", value=credentials["email"])
        playwright_fill(selector="input[type='password']", value=credentials["password"])
        playwright_click(selector="button:has-text('ログイン')")
        sleep(2)
    
    def _verify_expected_result(self, test_case, image_content):
        """期待結果確認"""
        # 画像内容から期待要素の存在確認
        expected_elements = test_case.get("expected_elements", [])
        
        passed = True
        findings = []
        
        for element in expected_elements:
            if element not in image_content:
                passed = False
                findings.append(f"⚠️ Expected element not found: {element}")
            else:
                findings.append(f"✅ {element}")
        
        return {
            "passed": passed,
            "findings": findings
        }
    
    def _generate_report(self, results):
        """UI検証レポート生成"""
        report_path = self.screenshot_dir / f"ui-verification-{datetime.now().strftime('%Y%m%d')}.md"
        
        report = f"""# UI Verification Report

## Test Date
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Test Environment
- URL: {self.app_url}
- Browser: Chromium (Playwright)
- Viewport: 1280x720

## Verification Results

"""
        
        for result in results:
            status = "✅" if result["result"]["passed"] else "❌"
            report += f"### {status} {result['test_case']}\n"
            report += f"![{result['test_case']}]({result['screenshot']}.png)\n\n"
            
            for finding in result["result"]["findings"]:
                report += f"- {finding}\n"
            report += "\n"
        
        # 総合判定
        all_passed = all(r["result"]["passed"] for r in results)
        approval = "✅ APPROVED" if all_passed else "❌ NOT APPROVED"
        report += f"## Approval Status\n{approval}\n"
        
        # レポート保存
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"UI verification report saved: {report_path}")
```

---

## 📊 自動化スクリプト

### 並列開発フロー自動化

**`scripts/parallel-dev-flow.sh`**:

```bash
#!/bin/bash

# Claude Code + Git Worktree 並列開発フロー自動化スクリプト

PROJECT_NAME="my-project"
MAIN_DIR="$HOME/$PROJECT_NAME"
REVIEW_DIR="$HOME/${PROJECT_NAME}-review"
UI_TEST_DIR="$HOME/${PROJECT_NAME}-ui-test"

# カラー定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 関数: ステップ表示
step() {
    echo -e "${GREEN}[STEP]${NC} $1"
}

# 関数: 警告表示
warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# 関数: エラー表示
error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Phase 1: 機能開発開始
start_feature() {
    FEATURE_NAME=$1
    
    step "Starting feature development: $FEATURE_NAME"
    
    # メイン開発worktreeでブランチ作成
    cd "$MAIN_DIR"
    git checkout develop
    git pull origin develop
    git checkout -b "feature/$FEATURE_NAME"
    
    step "Feature branch created: feature/$FEATURE_NAME"
    step "You can now start implementing in: $MAIN_DIR"
}

# Phase 2: コードレビュー開始
start_review() {
    FEATURE_NAME=$1
    
    step "Starting code review: $FEATURE_NAME"
    
    # メイン開発worktreeでレビューブランチ作成・プッシュ
    cd "$MAIN_DIR"
    git checkout -b "review/$FEATURE_NAME"
    git push origin "review/$FEATURE_NAME"
    
    # レビューworktreeでレビューブランチにチェックアウト
    cd "$REVIEW_DIR"
    git fetch origin
    git checkout "review/$FEATURE_NAME"
    
    step "Review branch checked out in: $REVIEW_DIR"
    step "Run Claude Code in review worktree to start code review"
    
    # Claude Codeでレビュー実行（手動起動を想定）
    warn "Manual action required: Start Claude Code in $REVIEW_DIR"
    warn "Execute: Task(subagent_type='code-reviewer', prompt='review/$FEATURE_NAME ブランチのレビューを実施')"
}

# Phase 3: UI検証開始
start_ui_test() {
    FEATURE_NAME=$1
    APP_URL=$2
    
    step "Starting UI verification: $FEATURE_NAME"
    
    # メイン開発worktreeでUI検証ブランチ作成・プッシュ
    cd "$MAIN_DIR"
    git checkout "feature/$FEATURE_NAME"
    git checkout -b "ui-test/$FEATURE_NAME"
    git push origin "ui-test/$FEATURE_NAME"
    
    # UI検証worktreeでUI検証ブランチにチェックアウト
    cd "$UI_TEST_DIR"
    git fetch origin
    git checkout "ui-test/$FEATURE_NAME"
    
    step "UI test branch checked out in: $UI_TEST_DIR"
    step "Deploying application to: $APP_URL"
    
    # デプロイ実行（Cloud Run想定）
    gcloud run deploy my-app --source . --region=asia-northeast1 --quiet
    
    step "Deployment complete. Starting UI verification..."
    
    # Claude CodeでUI検証実行（手動起動を想定）
    warn "Manual action required: Start Claude Code in $UI_TEST_DIR"
    warn "Execute: Task(subagent_type='ui-verification-specialist', prompt='$APP_URL のUI検証を実施')"
}

# Phase 4: フィードバック統合
integrate_feedback() {
    FEATURE_NAME=$1
    
    step "Integrating review feedback: $FEATURE_NAME"
    
    # レビューレポート表示
    echo "=== Code Review Report ==="
    cat "$REVIEW_DIR/review-reports/${FEATURE_NAME}-review.md"
    echo ""
    
    # UI検証レポート表示
    echo "=== UI Verification Report ==="
    cat "$UI_TEST_DIR/screenshots/ui-verification-*.md"
    echo ""
    
    # メイン開発worktreeに戻る
    cd "$MAIN_DIR"
    git checkout "feature/$FEATURE_NAME"
    
    step "Review reports displayed. Please fix issues and commit changes."
}

# Phase 5: マージ・クリーンアップ
merge_feature() {
    FEATURE_NAME=$1
    
    step "Merging feature: $FEATURE_NAME"
    
    # メイン開発worktreeでマージ
    cd "$MAIN_DIR"
    git checkout develop
    git merge "feature/$FEATURE_NAME"
    git push origin develop
    
    # ブランチ削除
    git branch -d "feature/$FEATURE_NAME"
    git branch -d "review/$FEATURE_NAME"
    git branch -d "ui-test/$FEATURE_NAME"
    git push origin --delete "feature/$FEATURE_NAME"
    git push origin --delete "review/$FEATURE_NAME"
    git push origin --delete "ui-test/$FEATURE_NAME"
    
    step "Feature merged and branches cleaned up"
}

# メイン処理
case "$1" in
    start)
        start_feature "$2"
        ;;
    review)
        start_review "$2"
        ;;
    ui-test)
        start_ui_test "$2" "$3"
        ;;
    feedback)
        integrate_feedback "$2"
        ;;
    merge)
        merge_feature "$2"
        ;;
    *)
        echo "Usage: $0 {start|review|ui-test|feedback|merge} <feature-name> [app-url]"
        exit 1
        ;;
esac
```

---

## 🎓 使用例

### 実際の開発フロー例

```bash
# 1. 機能開発開始
./scripts/parallel-dev-flow.sh start user-authentication

# メイン開発worktreeで実装作業
# → 認証機能実装
# → テストコード作成
# → コミット

# 2. コードレビュー開始
./scripts/parallel-dev-flow.sh review user-authentication

# レビューworktreeでClaude Code起動
# → Task(subagent_type="code-reviewer", ...)
# → レビューレポート生成
# → 問題点確認

# 3. UI検証開始
./scripts/parallel-dev-flow.sh ui-test user-authentication https://my-app-ycqe3vmjva-an.a.run.app

# UI検証worktreeでClaude Code起動
# → Task(subagent_type="ui-verification-specialist", ...)
# → スクリーンショット撮影
# → UI検証レポート生成

# 4. フィードバック統合
./scripts/parallel-dev-flow.sh feedback user-authentication

# レビュー結果・UI検証結果を確認
# → 問題点修正
# → 再コミット

# 5. 再レビュー・再検証（必要に応じて）
./scripts/parallel-dev-flow.sh review user-authentication
./scripts/parallel-dev-flow.sh ui-test user-authentication https://my-app-ycqe3vmjva-an.a.run.app

# 6. すべて承認されたらマージ
./scripts/parallel-dev-flow.sh merge user-authentication
```

---

## 📈 期待される効果

### 1. 開発速度の向上

- **並列実行**: メイン開発とレビューを同時進行
- **待ち時間削減**: レビュー待ちでブロックされない
- **自動化**: 手動レビューの時間を90%削減

### 2. 品質の向上

- **自動レビュー**: 95%以上の問題を検出
- **視覚的UI検証**: FALSE SUCCESS CLAIMSを完全防止
- **一貫した品質基準**: 人間の主観に依存しない

### 3. コンフリクトの削減

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

## 📚 参考資料

- [Git Worktree 公式ドキュメント](https://git-scm.com/docs/git-worktree)
- [Claude Code Task Tool 仕様](https://docs.anthropic.com/claude/docs)
- [Playwright MCP](https://github.com/executeautomation/mcp-playwright)

---

## 📝 今後の拡張

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

**作成日**: 2025-11-26  
**バージョン**: 1.0  
**ステータス**: Design Phase
