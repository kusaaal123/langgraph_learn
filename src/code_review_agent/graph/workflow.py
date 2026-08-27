from langgraph.graph import START, END, StateGraph
from .state import GraphState
from .nodes import (
    fetch_diff_node,
    classify_diff_node,
    generate_review_node,
    fast_path_docs_node,
    format_output_node,
)

def route_diff(state: GraphState) -> str:
    """Routing function for conditional edge after diff classification."""
    if state.get("is_docs_only"):
        return "fast_path"
    return "full_review"

def create_review_graph():
    workflow = StateGraph(GraphState)

    # 1. Add nodes
    workflow.add_node("fetch_diff", fetch_diff_node)
    workflow.add_node("classify_diff", classify_diff_node)
    workflow.add_node("generate_review", generate_review_node)
    workflow.add_node("fast_path_docs", fast_path_docs_node)
    workflow.add_node("format_output", format_output_node)

    # 2. Add fixed linear edges
    workflow.add_edge(START, "fetch_diff")
    workflow.add_edge("fetch_diff", "classify_diff")

    # 3. Add conditional edge
    workflow.add_conditional_edges(
        "classify_diff",
        route_diff,
        {
            "fast_path": "fast_path_docs",
            "full_review": "generate_review",
        },
    )

    # 4. Fan back in to format output
    workflow.add_edge("fast_path_docs", "format_output")
    workflow.add_edge("generate_review", "format_output")
    workflow.add_edge("format_output", END)

    return workflow.compile()