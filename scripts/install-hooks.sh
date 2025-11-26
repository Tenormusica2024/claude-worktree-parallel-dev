#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
HOOKS_SOURCE_DIR="$PROJECT_ROOT/hooks"
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"

COLOR_RESET="\033[0m"
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
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

echo ""
log_info "============================================="
log_info "Git Hooks インストーラー"
log_info "============================================="
echo ""

if [ ! -d "$GIT_HOOKS_DIR" ]; then
    log_warning ".git/hooksディレクトリが見つかりません"
    log_info "Gitリポジトリを初期化してください: git init"
    exit 1
fi

log_info "インストール元: $HOOKS_SOURCE_DIR"
log_info "インストール先: $GIT_HOOKS_DIR"
echo ""

HOOKS=("pre-commit" "post-commit" "pre-push")

for hook in "${HOOKS[@]}"; do
    SOURCE_FILE="$HOOKS_SOURCE_DIR/$hook"
    TARGET_FILE="$GIT_HOOKS_DIR/$hook"
    
    if [ ! -f "$SOURCE_FILE" ]; then
        log_warning "$hook: ソースファイルが見つかりません"
        continue
    fi
    
    if [ -f "$TARGET_FILE" ]; then
        log_warning "$hook: 既存のhookファイルが存在します"
        log_info "上書きしますか? (y/n)"
        read -r answer
        
        if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
            log_info "$hook: スキップします"
            continue
        fi
        
        cp "$TARGET_FILE" "$TARGET_FILE.backup"
        log_info "$hook: バックアップを作成しました (.backup)"
    fi
    
    cp "$SOURCE_FILE" "$TARGET_FILE"
    chmod +x "$TARGET_FILE"
    
    log_success "$hook: インストール完了"
done

echo ""
log_success "============================================="
log_success "Git Hooks インストール完了"
log_success "============================================="
echo ""

log_info "インストールされたhooks:"
for hook in "${HOOKS[@]}"; do
    if [ -f "$GIT_HOOKS_DIR/$hook" ]; then
        echo "  ✅ $hook"
    fi
done

echo ""
log_info "使い方:"
echo ""
echo "1. 通常通りコミット:"
echo "   git add ."
echo "   git commit -m \"Your message\""
echo "   → pre-commitが自動実行されます"
echo ""
echo "2. コミット後:"
echo "   → post-commitが自動実行されます"
echo ""
echo "3. プッシュ前:"
echo "   git push"
echo "   → pre-pushが自動実行されます"
echo ""

log_info "Hookを無効化する場合:"
echo "   git commit --no-verify"
echo "   git push --no-verify"
echo ""

log_warning "注意事項:"
echo "  - pre-commitでCritical問題が検出された場合、コミットが中断されます"
echo "  - 自動修正を選択すると、auto_fixer.pyが実行されます"
echo "  - pre-pushでレビュー未実施の場合、警告が表示されます"
echo ""

log_success "セットアップ完了！"
