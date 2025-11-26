#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MAIN_WORKTREE="$PROJECT_ROOT"
REVIEW_WORKTREE="${PROJECT_ROOT}-review"
UI_TEST_WORKTREE="${PROJECT_ROOT}-ui-test"

COLOR_RESET="\033[0m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_RED="\033[0;31m"
COLOR_BLUE="\033[0;34m"

log_info() {
    echo -e "${COLOR_BLUE}ℹ️  $1${COLOR_RESET}"
}

log_success() {
    echo -e "${COLOR_GREEN}✅ $1${COLOR_RESET}"
}

log_warning() {
    echo -e "${COLOR_YELLOW}⚠️  $1${COLOR_RESET}"
}

log_error() {
    echo -e "${COLOR_RED}❌ $1${COLOR_RESET}"
}

show_usage() {
    cat << EOF
Usage: $0 <command> [options]

Commands:
    start <feature-name>              機能開発開始
    review <feature-name>             コードレビュー開始
    ui-test <feature-name> <url>      UI検証開始
    feedback <feature-name>           フィードバック確認
    merge <feature-name>              developにマージ

Examples:
    $0 start user-authentication
    $0 review user-authentication
    $0 ui-test user-authentication https://my-app.run.app
    $0 feedback user-authentication
    $0 merge user-authentication
EOF
}

cmd_start() {
    local feature_name="$1"
    
    if [ -z "$feature_name" ]; then
        log_error "Feature name is required"
        show_usage
        exit 1
    fi
    
    log_info "機能開発を開始: $feature_name"
    
    cd "$MAIN_WORKTREE"
    
    git checkout develop
    git pull origin develop
    
    local branch_name="feature/$feature_name"
    git checkout -b "$branch_name"
    
    log_success "ブランチ作成完了: $branch_name"
    log_info "Claude Codeでメイン開発worktreeを開いて実装を開始してください"
    log_info "  cd $MAIN_WORKTREE"
}

cmd_review() {
    local feature_name="$1"
    
    if [ -z "$feature_name" ]; then
        log_error "Feature name is required"
        show_usage
        exit 1
    fi
    
    log_info "コードレビューを開始: $feature_name"
    
    if [ ! -d "$REVIEW_WORKTREE" ]; then
        log_info "レビュー用worktreeを作成中..."
        cd "$MAIN_WORKTREE"
        git worktree add "$REVIEW_WORKTREE" develop
    fi
    
    cd "$REVIEW_WORKTREE"
    
    local review_branch="review/$feature_name"
    git checkout -b "$review_branch" "origin/feature/$feature_name" 2>/dev/null || \
        git checkout -b "$review_branch" "feature/$feature_name"
    
    log_success "レビューブランチ作成完了: $review_branch"
    
    if [ -f "review/code_reviewer.py" ]; then
        log_info "コードレビュー実行中..."
        python3 review/code_reviewer.py "$feature_name"
    else
        log_warning "code_reviewer.pyが見つかりません"
        log_info "Claude Codeでレビューworktreeを開いてcode-reviewerサブエージェントを起動してください"
        log_info "  cd $REVIEW_WORKTREE"
    fi
}

cmd_ui_test() {
    local feature_name="$1"
    local url="$2"
    
    if [ -z "$feature_name" ] || [ -z "$url" ]; then
        log_error "Feature name and URL are required"
        show_usage
        exit 1
    fi
    
    log_info "UI検証を開始: $feature_name"
    log_info "  URL: $url"
    
    if [ ! -d "$UI_TEST_WORKTREE" ]; then
        log_info "UI検証用worktreeを作成中..."
        cd "$MAIN_WORKTREE"
        git worktree add "$UI_TEST_WORKTREE" develop
    fi
    
    cd "$UI_TEST_WORKTREE"
    
    local ui_test_branch="ui-test/$feature_name"
    git checkout -b "$ui_test_branch" "origin/feature/$feature_name" 2>/dev/null || \
        git checkout -b "$ui_test_branch" "feature/$feature_name"
    
    log_success "UI検証ブランチ作成完了: $ui_test_branch"
    
    if [ -f "ui-test/ui_verifier.py" ]; then
        log_info "UI検証レポートテンプレート作成中..."
        python3 ui-test/ui_verifier.py "$feature_name" "$url"
    else
        log_warning "ui_verifier.pyが見つかりません"
        log_info "Claude Codeでui-testworktreeを開いてui-verification-specialistサブエージェントを起動してください"
        log_info "  cd $UI_TEST_WORKTREE"
    fi
}

cmd_feedback() {
    local feature_name="$1"
    
    if [ -z "$feature_name" ]; then
        log_error "Feature name is required"
        show_usage
        exit 1
    fi
    
    log_info "フィードバック確認: $feature_name"
    
    local review_report=""
    local ui_report=""
    
    if [ -d "$REVIEW_WORKTREE/review-reports" ]; then
        review_report=$(find "$REVIEW_WORKTREE/review-reports" -name "review-$feature_name-*.md" | head -1)
    fi
    
    if [ -d "$UI_TEST_WORKTREE/screenshots" ]; then
        ui_report=$(find "$UI_TEST_WORKTREE/screenshots" -name "ui-verification-$feature_name-*.md" | head -1)
    fi
    
    echo ""
    log_info "=== レビューレポート ==="
    if [ -n "$review_report" ] && [ -f "$review_report" ]; then
        cat "$review_report"
    else
        log_warning "レビューレポートが見つかりません"
    fi
    
    echo ""
    log_info "=== UI検証レポート ==="
    if [ -n "$ui_report" ] && [ -f "$ui_report" ]; then
        cat "$ui_report"
    else
        log_warning "UI検証レポートが見つかりません"
    fi
    
    echo ""
    log_info "問題があれば、メイン開発worktreeで修正してください:"
    log_info "  cd $MAIN_WORKTREE"
}

cmd_merge() {
    local feature_name="$1"
    
    if [ -z "$feature_name" ]; then
        log_error "Feature name is required"
        show_usage
        exit 1
    fi
    
    log_info "developブランチへのマージを開始: $feature_name"
    
    cd "$MAIN_WORKTREE"
    
    local feature_branch="feature/$feature_name"
    git checkout "$feature_branch"
    
    log_info "最新のdevelopを取得中..."
    git checkout develop
    git pull origin develop
    
    log_info "マージ実行中..."
    git merge --no-ff "$feature_branch" -m "Merge $feature_branch into develop"
    
    log_success "マージ完了"
    
    log_info "作業ブランチを削除しますか？ (y/n)"
    read -r answer
    
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        git branch -d "$feature_branch"
        
        if [ -d "$REVIEW_WORKTREE" ]; then
            cd "$REVIEW_WORKTREE"
            git branch -d "review/$feature_name" 2>/dev/null || true
        fi
        
        if [ -d "$UI_TEST_WORKTREE" ]; then
            cd "$UI_TEST_WORKTREE"
            git branch -d "ui-test/$feature_name" 2>/dev/null || true
        fi
        
        log_success "ブランチ削除完了"
    fi
    
    log_info "developブランチをプッシュ: git push origin develop"
}

main() {
    local command="$1"
    shift
    
    case "$command" in
        start)
            cmd_start "$@"
            ;;
        review)
            cmd_review "$@"
            ;;
        ui-test)
            cmd_ui_test "$@"
            ;;
        feedback)
            cmd_feedback "$@"
            ;;
        merge)
            cmd_merge "$@"
            ;;
        *)
            log_error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

main "$@"
