from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class FindingCategory(str, Enum):
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    BUG = "bug"
    ARCHITECTURE = "architecture"

class SeverityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ReviewFinding(BaseModel):
    """An individual finding identified during code review."""
    
    file_path: str = Field(description="Path to the file being reviewed.")
    line_number: Optional[int] = Field(default=None, description="Line number relevant to the finding, if applicable.")
    category: FindingCategory = Field(description="Category of the finding.")
    severity: SeverityLevel = Field(description="Severity level of the issue.")
    description: str = Field(description="Detailed explanation of the issue.")
    suggestion: str = Field(description="Recommended fix or code refactoring snippet.")


class ReviewReport(BaseModel):
    """Complete code review report containing summary and findings."""

    summary: str = Field(
        description="High-level summary of the code review."
    )
    findings: List[ReviewFinding] = Field(
        description="List of specific findings. You MUST populate this array with an item for each bug, security issue, or design issue found."
    )
    passed: bool = Field(
        description="Whether the code passes review criteria without critical issues."
    )