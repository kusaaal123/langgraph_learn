from src.code_review_agent.graph.workflow import create_review_graph


def main():
    print("🚀 Running LangGraph Code Review Workflow (Stage 2)...\n")

    app = create_review_graph()

    initial_state = {
        "repo_path": ".",
        "target_branch": "master",
        "diff": None,
        "review_report": None,
    }
     
    final_state = app.invoke(initial_state)

    report = final_state.get("review_report")

    if report:
        print("--- CODE REVIEW REPORT ---")
        print(f"Passed: {report.passed}")
        print(f"Summary: {report.summary}\n")

        for i, finding in enumerate(report.findings, start=1):
            print(f"Finding #{i}: [{finding.severity.value.upper()}] {finding.category.value}")
            print(f"  File: {finding.file_path}:{finding.line_number}")
            print(f"  Description: {finding.description}")
            print(f"  Suggestion: {finding.suggestion}\n")

if __name__ == "__main__":
    main()