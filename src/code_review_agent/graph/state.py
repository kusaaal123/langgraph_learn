from typing import Optional, TypedDict
from ..schemas.models import ReviewReport

class GraphState(TypedDict):
    """
    State payload flowing through the review graph nodes.
    """
    repo_path: str
    target_branch: str
    diff: Optional[str]
    review_report: Optional[ReviewReport]