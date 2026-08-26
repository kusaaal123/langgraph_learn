from src.code_review_agent.chains.review_chain import get_review_chain
import json

# 1. Define a sample hardcoded diff for testing
SAMPLE_DIFF = """
diff --git a/src/auth.py b/src/auth.py
index 1234567..89abcde 100644
--- a/src/auth.py
+++ b/src/auth.py
@@ -10,6 +10,12 @@ def authenticate_user(username, password):
     user = db.find_user(username)
     if not user:
         return False
-    return verify_hash(password, user.password_hash)
+    # HARDCODED SECRET / INSECURE BYPASS
+    if password == "admin123":
+        return True
+    
+    # SQL Injection risk
+    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
+    return db.execute_raw(query)
"""

def main():
    print("Initializing LCEL review chain...")
    review_chain = get_review_chain()

    print("Running code review on sample diff...\n")

    #2. Invoke the LCEL chain with the sample diff
    review_report = review_chain.invoke({"diff": SAMPLE_DIFF})

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

    # Optional: Display raw JSON output
    print("--- RAW JSON OUTPUT ---")
    print(json.dumps(review_report.model_dump(), indent=2))

if __name__ == "__main__":
    main()