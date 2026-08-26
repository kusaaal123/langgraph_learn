from src.code_review_agent.tools.git_tools import read_git_diff
from src.code_review_agent.chains.review_chain import get_review_chain
import json

def main():
    print("Initializing LCEL review chain...")
    review_chain = get_review_chain()

    print("Running code review on diff...\n")

    git_diff = read_git_diff.invoke({"repo_path": ".", "target_branch": "master"})

    if git_diff == "No differences found." or git_diff.startswith("Error reading git diff:") or git_diff.startswith("An unexpected error occurred:"):
        print(f"Git diff result: {git_diff}")
        return

    review_report = review_chain.invoke({"diff": git_diff})
    
    # 3. Print the structured review report
    print("Code Review Report:")
    print(f"Passed: {review_report.passed}")
    print(f"Summary: {review_report.summary}\n")

    print("--- FINDINGS ---")
    for i, finding in enumerate(review_report.findings, start=1):
        print(f"Finding #{i}: [{finding.severity.value.upper()}] {finding.category.value}")
        print(f"  File: {finding.file_path}:{finding.line_number}")
        print(f"  Description: {finding.description}")
        print(f"  Suggestion: {finding.suggestion}\n")

    # # Optional: Display raw JSON output
    print("--- RAW JSON OUTPUT ---")
    print(json.dumps(review_report.model_dump(), indent=2))

if __name__ == "__main__":
    main()