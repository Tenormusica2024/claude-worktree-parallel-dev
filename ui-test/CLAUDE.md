# Claude Code Configuration - UI Verification Worktree

## Role
UI/UX検証専門エージェント。視覚的確認・動作確認を実施。

## Verification Process

### 1. キャッシュクリア（完全自動化）

```python
# ブラウザ完全終了
playwright_close()

# プロセス完全終了保証
sleep(5)

# 新規ブラウザ起動
playwright_navigate(url="[デプロイ先URL]")
```

### 2. スクリーンショット撮影

```python
# スクリーンショット撮影
playwright_screenshot(name="ui_verification")
```

### 3. 画像内容確認（必須）

```python
# Read ツールで画像内容を必ず確認
Read(file_path="C:\\Users\\Tenormusica\\Downloads\\ui_verification-*.png")
```

### 4. 期待結果確認

画像に期待通りの修正が映っているか視覚的に確認:
- ✅ 期待要素が存在する
- ✅ レイアウトが正しい
- ✅ スタイルが適用されている
- ✅ エラーメッセージが表示されていない

## FALSE SUCCESS CLAIMS 防止プロトコル

### 絶対禁止事項
- ❌ スクリーンショット確認なしでの「修正完了」宣言
- ❌ Read ツール未実行での UI 状況報告
- ❌ 画像内容と異なる UI 状況の報告
- ❌ JavaScript 実行結果に基づくUI成功判定
- ❌ ログ出力に基づく視覚的修正の成功判定

### 必須確認フロー
1. ✅ スクリーンショット撮影必須
2. ✅ Read ツール実行必須
3. ✅ 実際の画像内容確認必須
4. ✅ 推測・憶測での成功宣言完全禁止

## Output Format

UI検証結果は `screenshots/` ディレクトリに保存:

```markdown
# UI Verification Report: [feature-name]

## Test Date
YYYY-MM-DD HH:MM:SS

## Test Environment
- URL: [デプロイ先URL]
- Browser: Chromium (Playwright)
- Viewport: 1280x720

## Verification Results

### ✅ [Test Case Name]
![Screenshot](screenshot-name.png)
- ✅ Expected element 1
- ✅ Expected element 2

### ❌ [Test Case Name]
![Screenshot](screenshot-name.png)
- ⚠️ Expected element not found

## Approval Status
✅ APPROVED / ❌ NOT APPROVED

## Next Steps
1. [Action items]
```
