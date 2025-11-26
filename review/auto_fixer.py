#!/usr/bin/env python3
import os
import sys
import re
from pathlib import Path


class AutoFixer:
    def __init__(self, report_path):
        self.report_path = report_path
        self.fixes_applied = []
        
    def run(self):
        print(f"🔧 自動修正を開始: {self.report_path}")
        
        if not os.path.exists(self.report_path):
            print(f"❌ レポートが見つかりません: {self.report_path}")
            return False
        
        with open(self.report_path, 'r', encoding='utf-8') as f:
            report_content = f.read()
        
        critical_issues = self._extract_critical_issues(report_content)
        
        if not critical_issues:
            print("✅ Critical問題なし。修正不要です。")
            return True
        
        print(f"🔍 {len(critical_issues)}件のCritical問題を検出")
        
        for issue in critical_issues:
            self._fix_issue(issue)
        
        if self.fixes_applied:
            print(f"\n✅ {len(self.fixes_applied)}件の修正を適用しました:")
            for fix in self.fixes_applied:
                print(f"  - {fix}")
            return True
        else:
            print("\n⚠️ 自動修正可能な問題がありませんでした")
            return False
    
    def _extract_critical_issues(self, report_content):
        issues = []
        
        critical_section = re.search(
            r'### 🔴 Critical Issues\n\n(.*?)(?=###|\Z)',
            report_content,
            re.DOTALL
        )
        
        if not critical_section:
            return issues
        
        critical_text = critical_section.group(1)
        
        issue_blocks = re.findall(
            r'\*\*(\w+)\*\* - (.+?)\n- 問題: (.+?)\n- 推奨: (.+?)\n',
            critical_text,
            re.DOTALL
        )
        
        for category, file_path, message, recommendation in issue_blocks:
            issues.append({
                "category": category,
                "file": file_path.strip(),
                "message": message.strip(),
                "recommendation": recommendation.strip()
            })
        
        return issues
    
    def _fix_issue(self, issue):
        file_path = issue["file"]
        
        if not os.path.exists(file_path):
            print(f"  ⚠️ ファイルが見つかりません: {file_path}")
            return
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        if "パスワードが平文で保存" in issue["message"]:
            content = self._fix_plain_password(content, file_path)
        
        elif "eval()の使用" in issue["message"]:
            content = self._fix_eval_usage(content, file_path)
        
        elif "SQL Injection" in issue["message"]:
            content = self._fix_sql_injection(content, file_path)
        
        elif "APIキーがハードコード" in issue["message"]:
            content = self._fix_hardcoded_api_key(content, file_path)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixes_applied.append(f"{issue['category']}: {file_path}")
            print(f"  ✅ 修正適用: {file_path} - {issue['message']}")
        else:
            print(f"  ⚠️ 自動修正不可: {file_path} - {issue['message']}")
    
    def _fix_plain_password(self, content, file_path):
        if file_path.endswith('.py'):
            if 'import hashlib' not in content and 'import bcrypt' not in content:
                import_section = re.search(r'^(import .*?\n)+', content, re.MULTILINE)
                if import_section:
                    last_import = import_section.group(0)
                    content = content.replace(
                        last_import,
                        last_import + 'import bcrypt\n'
                    )
            
            content = re.sub(
                r'password\s*=\s*["\'](.+?)["\']',
                r'password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())',
                content
            )
        
        return content
    
    def _fix_eval_usage(self, content, file_path):
        content = re.sub(
            r'eval\s*\(',
            r'# FIXME: eval() removed for security - use ast.literal_eval() or json.loads()\n# eval(',
            content
        )
        
        return content
    
    def _fix_sql_injection(self, content, file_path):
        sql_patterns = [
            (r'["\']SELECT\s+(.+?)\s+FROM\s+(.+?)["\'].*?\+\s*(\w+)',
             r'"SELECT \1 FROM \2 WHERE field = ?", (\3,)'),
            (r'cursor\.execute\s*\(\s*["\'](.+?)["\'].*?\+\s*(.+?)\)',
             r'cursor.execute("\1 ?", (\2,))')
        ]
        
        for pattern, replacement in sql_patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content
    
    def _fix_hardcoded_api_key(self, content, file_path):
        api_key_pattern = r'(api[_-]?key\s*=\s*)["\']([^"\']+)["\']'
        
        if re.search(api_key_pattern, content, re.IGNORECASE):
            if 'import os' not in content:
                import_section = re.search(r'^(import .*?\n)+', content, re.MULTILINE)
                if import_section:
                    last_import = import_section.group(0)
                    content = content.replace(
                        last_import,
                        last_import + 'import os\n'
                    )
            
            content = re.sub(
                api_key_pattern,
                r'\1os.environ.get("API_KEY")',
                content,
                flags=re.IGNORECASE
            )
        
        return content


def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_fixer.py <review-report-path>")
        sys.exit(1)
    
    report_path = sys.argv[1]
    
    fixer = AutoFixer(report_path)
    success = fixer.run()
    
    if success and fixer.fixes_applied:
        print("\n📝 修正を反映するため、変更をステージングしてください:")
        print("  git add -u")
        print("  git commit --amend --no-edit")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
