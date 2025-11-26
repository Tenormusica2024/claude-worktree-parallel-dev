#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
from pathlib import Path
import subprocess


class UIVerificationAgent:
    def __init__(self, feature_name, url, viewport_width=1280, viewport_height=720):
        self.feature_name = feature_name
        self.url = url
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.test_results = []
        
    def run_verification(self):
        print(f"🔍 Starting UI verification for: {self.feature_name}")
        print(f"   URL: {self.url}")
        print(f"   Viewport: {self.viewport_width}x{self.viewport_height}")
        
        print("\n📸 スクリーンショット撮影の準備...")
        print("   ⚠️ このスクリプトはClaude Codeのコンテキストで実行してください")
        print("   ⚠️ 以下のPlaywright MCPコマンドを手動で実行する必要があります:")
        print("")
        print(f"   1. playwright_close()")
        print(f"   2. sleep 5")
        print(f"   3. playwright_navigate(url=\"{self.url}\", width={self.viewport_width}, height={self.viewport_height})")
        print(f"   4. playwright_screenshot(name=\"ui_verification_{self.feature_name}\")")
        print(f"   5. Read(file_path=\"C:\\\\Users\\\\Tenormusica\\\\Downloads\\\\ui_verification_{self.feature_name}-*.png\")")
        print("")
        print("📝 スクリーンショット撮影後、以下の項目を確認してください:")
        
        self._define_test_cases()
        self._generate_report_template()
        
    def _define_test_cases(self):
        print("\n✅ 確認項目:")
        print("   1. 期待される要素が存在するか")
        print("   2. レイアウトが正しいか")
        print("   3. スタイルが適用されているか")
        print("   4. エラーメッセージが表示されていないか")
        print("   5. コンソールエラーがないか")
    
    def _generate_report_template(self):
        report_dir = Path("screenshots")
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_path = report_dir / f"ui-verification-{self.feature_name}-{datetime.now().strftime('%Y%m%d')}.md"
        
        report_content = f"""# UI Verification Report: {self.feature_name}

## Test Date
{timestamp}

## Test Environment
- URL: {self.url}
- Browser: Chromium (Playwright)
- Viewport: {self.viewport_width}x{self.viewport_height}

## Verification Results

### ⏳ Test Case 1: [テストケース名を記入]
![Screenshot](ui_verification_{self.feature_name}-[タイムスタンプ].png)

**確認項目:**
- [ ] 期待される要素が存在する
- [ ] レイアウトが正しい
- [ ] スタイルが適用されている
- [ ] エラーメッセージが表示されていない
- [ ] コンソールエラーがない

**結果:**
[✅ PASS / ❌ FAIL を記入]

**備考:**
[気づいた点があれば記入]

---

### ⏳ Test Case 2: [テストケース名を記入]
![Screenshot](ui_verification_{self.feature_name}-[タイムスタンプ].png)

**確認項目:**
- [ ] 期待される要素が存在する
- [ ] レイアウトが正しい
- [ ] スタイルが適用されている
- [ ] エラーメッセージが表示されていない
- [ ] コンソールエラーがない

**結果:**
[✅ PASS / ❌ FAIL を記入]

**備考:**
[気づいた点があれば記入]

---

## Approval Status
⏳ PENDING VERIFICATION

## Next Steps
1. 上記のPlaywright MCPコマンドを実行
2. スクリーンショットをRead toolで確認
3. 各テストケースの結果を記入
4. 最終的なApproval Statusを更新（✅ APPROVED / ❌ NOT APPROVED）

---

## FALSE SUCCESS CLAIMS Prevention Checklist

- [ ] スクリーンショット撮影完了
- [ ] Read ツールで画像内容確認完了
- [ ] 実際の画像内容に基づいて結果を記入
- [ ] 推測・憶測での成功判定を避けた
- [ ] JavaScript実行結果ではなく視覚的確認に基づく
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n📊 UI検証レポートテンプレート作成完了: {report_path}")
        print(f"   スクリーンショット撮影後、このファイルに結果を記入してください")


def main():
    if len(sys.argv) < 3:
        print("Usage: python ui_verifier.py <feature-name> <url> [width] [height]")
        print("Example: python ui_verifier.py user-auth https://my-app.run.app 1280 720")
        sys.exit(1)
    
    feature_name = sys.argv[1]
    url = sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1280
    height = int(sys.argv[4]) if len(sys.argv) > 4 else 720
    
    agent = UIVerificationAgent(feature_name, url, width, height)
    agent.run_verification()


if __name__ == "__main__":
    main()
