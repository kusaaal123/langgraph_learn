import subprocess
from typing import Optional
from langchain_core.tools import tool

@tool
def read_git_diff(repo_path: str = ".", target_branch: Optional[str] = None) -> str:
   """
    Reads the git diff of the specified repository path against the target branch.

    Args:
        repo_path (str): The path to the git repository. Defaults to the current directory.
        target_branch: Optional target branch or commit to diff against (e.g., 'main' or 'HEAD~1').
                      If omitted, returns unstaged changes or HEAD diff.

    Returns:
        str: The git diff output as a string.
    """

   try:
      cmd = ["git" , "diff"]
      if target_branch:
         cmd.append(target_branch)

      result = subprocess.run(
         cmd,
         cwd=repo_path,
         capture_output=True,
         text=True,
         check=True
      )

      diff_text = result.stdout.strip()
      if not diff_text:
        return "No differences found."

      return diff_text
   except subprocess.CalledProcessError as e:
        return f"Error reading git diff: {e.stderr.strip()}"
   except Exception as e:
      return f"An unexpected error occurred: {str(e)}"