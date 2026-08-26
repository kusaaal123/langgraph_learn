from src.code_review_agent.chains.review_chain import run_react_agent
import json

def main():
    print("Starting ReAct Code Review Agent...\n")

    # Prompt user query (letting agent decide to run tools)
    query = "Please fetch the latest git diff for the target branch 'master' and review the code for issues."
    
    review_report = run_react_agent(query)
    
    print("\n--- CODE REVIEW REPORT ---")
    print(f"Passed: {review_report.passed}")
    print(f"Summary: {review_report.summary}\n")

    for i, finding in enumerate(review_report.findings, start=1):
        print(f"Finding #{i}: [{finding.severity.value.upper()}] {finding.category.value}")
        print(f"  File: {finding.file_path}:{finding.line_number}")
        print(f"  Description: {finding.description}")
        print(f"  Suggestion: {finding.suggestion}\n")

if __name__ == "__main__":
    main()