#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
from pathlib import Path
import subprocess
import re


class CodeReviewAgent:
    def __init__(self, branch_name, target_files=None):
        self.branch_name = branch_name
        self.target_files = target_files or []
        self.findings = {
            "critical": [],
            "medium": [],
            "minor": []
        }
        
    def run_review(self):
        print(f"🔍 Starting code review for branch: {self.branch_name}")
        
        if not self.target_files:
            self.target_files = self._get_changed_files()
        
        for file_path in self.target_files:
            if not os.path.exists(file_path):
                continue
            
            print(f"  Reviewing: {file_path}")
            content = self._read_file(file_path)
            
            self._check_code_quality(file_path, content)
            self._check_security(file_path, content)
            self._check_performance(file_path, content)
            self._check_error_handling(file_path, content)
            self._check_best_practices(file_path, content)
        
        self._generate_report()
        
    def _get_changed_files(self):
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", "develop"],
                capture_output=True,
                text=True,
                check=True
            )
            files = result.stdout.strip().split("\n")
            return [f for f in files if f.endswith(('.py', '.js', '.html', '.css'))]
        except subprocess.CalledProcessError:
            return []
    
    def _read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"  ⚠️ Failed to read {file_path}: {e}")
            return ""
    
    def _check_code_quality(self, file_path, content):
        findings = []
        
        if file_path.endswith('.py'):
            if re.search(r'\bdef\s+[a-z]{1,2}\b', content):
                findings.append({
                    "severity": "minor",
                    "category": "code_quality",
                    "file": file_path,
                    "message": "関数名が短すぎます（2文字以下）",
                    "recommendation": "意味のある関数名を使用してください"
                })
            
            if len(content.split('\n')) > 500:
                findings.append({
                    "severity": "medium",
                    "category": "code_quality",
                    "file": file_path,
                    "message": "ファイルが500行を超えています",
                    "recommendation": "モジュールを分割してください"
                })
        
        for finding in findings:
            self._add_finding(finding)
    
    def _check_security(self, file_path, content):
        findings = []
        
        if "password" in content.lower() and "hash" not in content.lower():
            findings.append({
                "severity": "critical",
                "category": "security",
                "file": file_path,
                "message": "パスワードが平文で保存されている可能性",
                "recommendation": "bcryptやArgon2でハッシュ化してください"
            })
        
        if re.search(r'eval\s*\(', content):
            findings.append({
                "severity": "critical",
                "category": "security",
                "file": file_path,
                "message": "eval()の使用を検出（Code Injection リスク）",
                "recommendation": "eval()を使用せず、安全な方法で実装してください"
            })
        
        if re.search(r'["\']SELECT\s+.*\s+FROM\s+.*["\'].*\+', content, re.IGNORECASE):
            findings.append({
                "severity": "critical",
                "category": "security",
                "file": file_path,
                "message": "SQL Injection の可能性（文字列連結でSQL構築）",
                "recommendation": "プリペアドステートメント・パラメータ化クエリを使用してください"
            })
        
        if re.search(r'api[_-]?key\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
            findings.append({
                "severity": "critical",
                "category": "security",
                "file": file_path,
                "message": "APIキーがハードコードされています",
                "recommendation": "環境変数や設定ファイルで管理してください"
            })
        
        for finding in findings:
            self._add_finding(finding)
    
    def _check_performance(self, file_path, content):
        findings = []
        
        if file_path.endswith('.py'):
            nested_loops = re.findall(r'for\s+.*:\s*\n\s+for\s+.*:', content)
            if len(nested_loops) > 0:
                findings.append({
                    "severity": "medium",
                    "category": "performance",
                    "file": file_path,
                    "message": "ネストしたループを検出（O(N²)の可能性）",
                    "recommendation": "アルゴリズムの最適化を検討してください"
                })
        
        if re.search(r'for\s+.*\s+in\s+.*\.query\(', content):
            findings.append({
                "severity": "medium",
                "category": "performance",
                "file": file_path,
                "message": "N+1クエリ問題の可能性",
                "recommendation": "join()やselect_related()を使用してください"
            })
        
        for finding in findings:
            self._add_finding(finding)
    
    def _check_error_handling(self, file_path, content):
        findings = []
        
        if file_path.endswith('.py'):
            try_count = len(re.findall(r'\btry\s*:', content))
            except_count = len(re.findall(r'\bexcept\s+', content))
            
            if except_count > 0 and 'except:' in content:
                findings.append({
                    "severity": "medium",
                    "category": "error_handling",
                    "file": file_path,
                    "message": "汎用的なexceptを使用しています",
                    "recommendation": "具体的な例外クラスを指定してください"
                })
            
            if 'open(' in content and try_count == 0:
                findings.append({
                    "severity": "minor",
                    "category": "error_handling",
                    "file": file_path,
                    "message": "ファイル操作にtry-exceptがありません",
                    "recommendation": "with文またはtry-exceptでエラーハンドリングしてください"
                })
        
        for finding in findings:
            self._add_finding(finding)
    
    def _check_best_practices(self, file_path, content):
        findings = []
        
        if file_path.endswith('.py'):
            if 'import *' in content:
                findings.append({
                    "severity": "minor",
                    "category": "best_practices",
                    "file": file_path,
                    "message": "import *を使用しています",
                    "recommendation": "必要なモジュールのみを明示的にimportしてください"
                })
            
            if re.search(r'class\s+[a-z]', content):
                findings.append({
                    "severity": "minor",
                    "category": "best_practices",
                    "file": file_path,
                    "message": "クラス名がPascalCaseになっていません",
                    "recommendation": "PEP 8に従い、クラス名はPascalCaseで記述してください"
                })
        
        for finding in findings:
            self._add_finding(finding)
    
    def _add_finding(self, finding):
        severity = finding["severity"]
        self.findings[severity].append(finding)
    
    def _generate_report(self):
        report_dir = Path("review-reports")
        report_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d")
        report_path = report_dir / f"review-{self.branch_name}-{timestamp}.md"
        
        total_findings = sum(len(v) for v in self.findings.values())
        approval_status = "✅ APPROVED" if len(self.findings["critical"]) == 0 else "❌ NOT APPROVED"
        
        report_content = f"""# Code Review Report: {self.branch_name}

## Review Date
{timestamp}

## Summary
Total Findings: {total_findings}
- Critical: {len(self.findings["critical"])}
- Medium: {len(self.findings["medium"])}
- Minor: {len(self.findings["minor"])}

## Findings

"""
        
        if self.findings["critical"]:
            report_content += "### 🔴 Critical Issues\n\n"
            for finding in self.findings["critical"]:
                report_content += f"""**{finding['category'].upper()}** - {finding['file']}
- 問題: {finding['message']}
- 推奨: {finding['recommendation']}

"""
        
        if self.findings["medium"]:
            report_content += "### 🟡 Medium Issues\n\n"
            for finding in self.findings["medium"]:
                report_content += f"""**{finding['category'].upper()}** - {finding['file']}
- 問題: {finding['message']}
- 推奨: {finding['recommendation']}

"""
        
        if self.findings["minor"]:
            report_content += "### 🟢 Minor Issues\n\n"
            for finding in self.findings["minor"]:
                report_content += f"""**{finding['category'].upper()}** - {finding['file']}
- 問題: {finding['message']}
- 推奨: {finding['recommendation']}

"""
        
        if total_findings == 0:
            report_content += "問題は検出されませんでした。\n\n"
        
        report_content += f"""## Approval Status
{approval_status}

## Next Steps
"""
        
        if len(self.findings["critical"]) > 0:
            report_content += "1. Critical問題を優先的に修正してください\n"
        if len(self.findings["medium"]) > 0:
            report_content += "2. Medium問題の修正を検討してください\n"
        if len(self.findings["minor"]) > 0:
            report_content += "3. Minor問題は時間があれば修正してください\n"
        if total_findings == 0:
            report_content += "1. developブランチへのマージ準備完了\n"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n📊 レビューレポート作成完了: {report_path}")
        print(f"   Total Findings: {total_findings}")
        print(f"   Status: {approval_status}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python code_reviewer.py <branch-name> [file1] [file2] ...")
        sys.exit(1)
    
    branch_name = sys.argv[1]
    target_files = sys.argv[2:] if len(sys.argv) > 2 else None
    
    agent = CodeReviewAgent(branch_name, target_files)
    agent.run_review()


if __name__ == "__main__":
    main()
