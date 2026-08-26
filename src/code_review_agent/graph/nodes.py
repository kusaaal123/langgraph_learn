from ..graph.state import GraphState
from ..tools.git_tools import read_git_diff
from typing import Dict, Any
from ..chains.review_chain import get_review_chain

def fetch_diff_node(state: GraphState) -> Dict[str, Any]:
    """Node: Fetches the git diff for the repo path and target branch."""
    print("🔹 [Node: fetch_diff] Fetching git diff...")
    repo_path = state.get("repo_path", ".")
    target_branch = state.get("target_branch", "master")
    
    diff_content = read_git_diff.invoke({"repo_path": repo_path, "target_branch": target_branch})
    return {"diff": diff_content}

def generate_review_node(state: GraphState) -> Dict[str, Any]:
    """Node: Runs LLM analysis on the fetched diff."""
    print("🔹 [Node: generate_review] Analyzing code diff...")
    diff = state.get("diff", "")
    
    if not diff or diff.startswith("No differences found") or diff.startswith("Error"):
        return {"review_report": None}

    chain = get_review_chain()
    report = chain.invoke({"diff": diff})
    return {"review_report": report}

def format_output_node(state: GraphState) -> Dict[str, Any]:
    """Node: Formats and logs the final review report."""
    print("🔹 [Node: format_output] Finalizing results...\n")
    report = state.get("review_report")
    if not report:
        print("No review report generated (no changes or git error).")
    return {}