from langgraph.graph import START, END, StateGraph
from .state import GraphState

from .nodes import fetch_diff_node, generate_review_node, format_output_node

def create_review_graph():
    """
    Create a graph of nodes for the code review process.
    Nodes:
        1. fetch_diff_node: Fetches the git diff for the repo path and target branch.
        2. generate_review_node: Runs LLM analysis on the fetched diff.
        3. format_output_node: Formats and logs the final review report.
    """
    
    workflow = StateGraph(GraphState)

    #1. Add nodes to the graph
    workflow.add_node("fetch_diff", fetch_diff_node)
    workflow.add_node("generate_review", generate_review_node)
    workflow.add_node("format_output", format_output_node)

    #2. Add Linear edges 
    workflow.add_edge(START, "fetch_diff")
    workflow.add_edge("fetch_diff", "generate_review")
    workflow.add_edge("generate_review", "format_output")
    workflow.add_edge("format_output", END)

    return workflow.compile()