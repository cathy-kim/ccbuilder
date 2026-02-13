#!/usr/bin/env python3
"""
Claude Code Extension Builder - Evaluation Runner
Purpose: Execute test cases and validate against golden outputs
"""

import json
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Paths
EVAL_DIR = Path(__file__).parent
SKILL_DIR = EVAL_DIR.parent
TEST_CASES_FILE = EVAL_DIR / "test-cases.json"
GOLDEN_DIR = EVAL_DIR / "golden-outputs"
RESULTS_DIR = EVAL_DIR / "eval-results"
TEMP_DIR = Path("/tmp/claude-code-eval")

class SkillEvaluator:
    def __init__(self):
        self.test_cases = self.load_test_cases()
        self.results = []

        # Ensure temp directory exists
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    def load_test_cases(self) -> Dict:
        """Load test cases from JSON"""
        with open(TEST_CASES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def check_yaml_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """Check if file has valid YAML frontmatter"""
        if not file_path.exists():
            return {"valid": False, "error": "File does not exist"}

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for YAML frontmatter
        if not content.startswith('---\n'):
            return {"valid": False, "error": "Missing YAML frontmatter"}

        # Extract frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {"valid": False, "error": "Invalid YAML frontmatter format"}

        frontmatter = match.group(1)

        # Parse fields
        fields = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fields[key.strip()] = value.strip()

        return {
            "valid": True,
            "fields": fields
        }

    def check_file_structure(self, file_path: Path, requirements: Dict) -> Dict[str, Any]:
        """Check if file meets structure requirements"""
        checks = {}

        if not file_path.exists():
            return {"all_passed": False, "error": "File does not exist"}

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Check line count
        if 'line_count_max' in requirements:
            max_lines = requirements['line_count_max']
            actual_lines = len(lines)
            checks['line_count'] = {
                'passed': actual_lines <= max_lines,
                'expected': f"<= {max_lines}",
                'actual': actual_lines
            }

        # Check required sections
        if 'required_sections' in requirements:
            for section in requirements['required_sections']:
                section_found = any(section in line for line in lines)
                checks[f'section_{section}'] = {
                    'passed': section_found,
                    'expected': f'Contains "{section}"',
                    'actual': 'Found' if section_found else 'Not found'
                }

        # Check YAML frontmatter
        if requirements.get('has_yaml_frontmatter'):
            yaml_check = self.check_yaml_frontmatter(file_path)
            checks['yaml_frontmatter'] = {
                'passed': yaml_check['valid'],
                'details': yaml_check
            }

        all_passed = all(check.get('passed', False) for check in checks.values())

        return {
            "all_passed": all_passed,
            "checks": checks
        }

    def compare_with_golden(self, generated_file: Path, golden_file: Path) -> Dict[str, Any]:
        """Compare generated output with golden output"""
        if not generated_file.exists():
            return {
                "match": False,
                "error": "Generated file does not exist"
            }

        if not golden_file.exists():
            return {
                "match": "UNKNOWN",
                "warning": "Golden file does not exist, cannot compare"
            }

        with open(generated_file, 'r', encoding='utf-8') as f:
            generated_content = f.read()

        with open(golden_file, 'r', encoding='utf-8') as f:
            golden_content = f.read()

        # Exact match
        exact_match = generated_content == golden_content

        # Structural similarity (same sections, similar length)
        gen_sections = re.findall(r'^##? (.+)$', generated_content, re.MULTILINE)
        gold_sections = re.findall(r'^##? (.+)$', golden_content, re.MULTILINE)

        sections_match = set(gen_sections) == set(gold_sections)
        length_ratio = len(generated_content) / len(golden_content) if len(golden_content) > 0 else 0

        return {
            "exact_match": exact_match,
            "sections_match": sections_match,
            "length_ratio": length_ratio,
            "similarity_score": 1.0 if exact_match else (0.7 if sections_match else 0.3),
            "generated_sections": gen_sections,
            "golden_sections": gold_sections
        }

    def run_test_case(self, test_case: Dict) -> Dict[str, Any]:
        """Run a single test case"""
        test_id = test_case['id']
        category = test_case['category']

        print(f"\n{'='*60}")
        print(f"Running: {test_id}")
        print(f"Category: {category}")
        print(f"Description: {test_case['description']}")
        print(f"{'='*60}\n")

        result = {
            'test_id': test_id,
            'category': category,
            'description': test_case['description'],
            'status': 'PENDING',
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'notes': []
        }

        # Expected outputs
        expected = test_case['expected_outputs']

        # Manual verification prompt
        print(f"📝 MANUAL STEP REQUIRED:")
        print(f"\nPrompt to use:")
        print(f"  {test_case['input']['prompt']}\n")

        print(f"Expected files to be created:")
        for file_path in expected.get('files_created', []):
            print(f"  - {file_path}")

        print(f"\n⏸️  Please run the skill with the above prompt, then press Enter to continue...")
        input()

        # Check if files were created
        files_check = {}
        for file_path in expected.get('files_created', []):
            full_path = Path.cwd() / ".claude" / file_path
            exists = full_path.exists()
            files_check[file_path] = {
                'exists': exists,
                'path': str(full_path)
            }

            if exists:
                print(f"✅ File created: {file_path}")
            else:
                print(f"❌ File NOT found: {file_path}")

        result['checks']['files_created'] = files_check

        # Check SKILL.md requirements if applicable
        if 'skill_md_requirements' in expected:
            skill_files = [f for f in expected.get('files_created', []) if 'SKILL.md' in f]
            if skill_files:
                skill_path = Path.cwd() / ".claude" / skill_files[0]
                structure_check = self.check_file_structure(
                    skill_path,
                    expected['skill_md_requirements']
                )
                result['checks']['skill_structure'] = structure_check

                # Compare with golden output
                golden_file = GOLDEN_DIR / f"{test_id}-skill-template.md"
                comparison = self.compare_with_golden(skill_path, golden_file)
                result['checks']['golden_comparison'] = comparison

        # Check agent requirements if applicable
        if 'agent_md_requirements' in expected:
            agent_files = [f for f in expected.get('files_created', []) if 'agents/' in f]
            if agent_files:
                agent_path = Path.cwd() / ".claude" / agent_files[0]

                if agent_path.exists():
                    with open(agent_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    agent_reqs = expected['agent_md_requirements']
                    agent_checks = {}

                    if agent_reqs.get('has_role_section'):
                        agent_checks['has_role'] = '## Role' in content or '# Role' in content

                    if agent_reqs.get('has_routing_section'):
                        agent_checks['has_routing'] = '## Routing' in content or 'Route to' in content

                    if 'routing_target' in agent_reqs:
                        target = agent_reqs['routing_target']
                        agent_checks['routes_to_target'] = target in content

                    result['checks']['agent_structure'] = agent_checks

                    # Compare with golden
                    golden_file = GOLDEN_DIR / f"{test_id}-agent-template.md"
                    comparison = self.compare_with_golden(agent_path, golden_file)
                    result['checks']['golden_comparison'] = comparison

        # Determine overall status
        all_files_exist = all(c['exists'] for c in files_check.values())
        structure_passed = result['checks'].get('skill_structure', {}).get('all_passed', True)

        if all_files_exist and structure_passed:
            result['status'] = 'PASS'
        elif all_files_exist:
            result['status'] = 'PARTIAL'
        else:
            result['status'] = 'FAIL'

        print(f"\n{'='*60}")
        print(f"Status: {result['status']}")
        print(f"{'='*60}\n")

        return result

    def generate_report(self):
        """Generate evaluation report"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        report_file = RESULTS_DIR / f"{timestamp}-evaluation.json"
        markdown_file = RESULTS_DIR / f"{timestamp}-evaluation.md"

        # Save JSON
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'total_tests': len(self.results),
                'passed': sum(1 for r in self.results if r['status'] == 'PASS'),
                'failed': sum(1 for r in self.results if r['status'] == 'FAIL'),
                'partial': sum(1 for r in self.results if r['status'] == 'PARTIAL'),
                'results': self.results
            }, f, indent=2)

        # Generate Markdown
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        partial = sum(1 for r in self.results if r['status'] == 'PARTIAL')

        markdown = f"""# Evaluation Report - Claude Code Extension Builder

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Tests | {len(self.results)} | 100% |
| ✅ Passed | {passed} | {passed/len(self.results)*100:.1f}% |
| ⚠️  Partial | {partial} | {partial/len(self.results)*100:.1f}% |
| ❌ Failed | {failed} | {failed/len(self.results)*100:.1f}% |

## Test Results

"""

        for result in self.results:
            status_icon = {"PASS": "✅", "FAIL": "❌", "PARTIAL": "⚠️"}.get(result['status'], "❓")

            markdown += f"""
### {status_icon} {result['test_id']} - {result['status']}

**Category**: {result['category']}
**Description**: {result['description']}

**Checks**:
"""

            # Files created
            if 'files_created' in result['checks']:
                markdown += "\n**Files Created:**\n"
                for file_path, check in result['checks']['files_created'].items():
                    icon = "✅" if check['exists'] else "❌"
                    markdown += f"- {icon} `{file_path}`\n"

            # Structure checks
            if 'skill_structure' in result['checks']:
                structure = result['checks']['skill_structure']
                if 'checks' in structure:
                    markdown += "\n**Structure Checks:**\n"
                    for check_name, check_data in structure['checks'].items():
                        if isinstance(check_data, dict):
                            icon = "✅" if check_data.get('passed') else "❌"
                            markdown += f"- {icon} {check_name}: {check_data.get('expected', 'N/A')}\n"

            # Golden comparison
            if 'golden_comparison' in result['checks']:
                comparison = result['checks']['golden_comparison']
                similarity = comparison.get('similarity_score', 0)
                markdown += f"\n**Golden Output Similarity**: {similarity*100:.0f}%\n"

            markdown += "\n---\n"

        # Add recommendations
        markdown += """
## Recommendations

"""
        if failed > 0:
            markdown += f"- 🔴 **Critical**: Fix {failed} failing test cases\n"
        if partial > 0:
            markdown += f"- 🟡 **Warning**: Review {partial} partial test cases\n"
        if passed == len(self.results):
            markdown += "- ✅ **Excellent**: All tests passed!\n"

        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown)

        print(f"\n📊 Reports generated:")
        print(f"  - JSON: {report_file}")
        print(f"  - Markdown: {markdown_file}")

    def run_all(self):
        """Run all test cases"""
        print("=" * 60)
        print("Claude Code Extension Builder - Evaluation")
        print("=" * 60)

        test_cases = self.test_cases.get('test_cases', [])

        # Ask which tests to run
        print(f"\nFound {len(test_cases)} test cases:")
        for i, tc in enumerate(test_cases, 1):
            print(f"  {i}. [{tc['priority']}] {tc['id']} - {tc['description']}")

        print(f"\nSelect tests to run:")
        print(f"  1. Run all tests")
        print(f"  2. Run P0 tests only")
        print(f"  3. Run specific test")

        choice = input("\nChoice (1-3): ").strip()

        tests_to_run = []
        if choice == '1':
            tests_to_run = test_cases
        elif choice == '2':
            tests_to_run = [tc for tc in test_cases if tc['priority'] == 'P0']
        elif choice == '3':
            test_id = input("Enter test ID (e.g., TC001): ").strip()
            tests_to_run = [tc for tc in test_cases if tc['id'] == test_id]

        print(f"\nRunning {len(tests_to_run)} test(s)...\n")

        for test_case in tests_to_run:
            result = self.run_test_case(test_case)
            self.results.append(result)

        # Generate report
        self.generate_report()

        # Summary
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        print(f"\n{'='*60}")
        print(f"Evaluation Complete")
        print(f"Passed: {passed}/{len(self.results)}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    evaluator = SkillEvaluator()
    evaluator.run_all()
