from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from ..schemas.models import ReviewReport

load_dotenv()

def get_review_chain():
    """
    Build and return an LCEL chain for code review.
    
    Composition: prompt | llm | parser
    """

    # 1. Use a supported model with low temperature for deterministic JSON output
    model_id = "meta/llama-3.3-70b-instruct"

    llm = ChatNVIDIA(
        model=model_id,
        temperature=0.1
    )

    # 2. Use PydanticOutputParser for clean schema instruction injection
    parser = PydanticOutputParser(pydantic_object=ReviewReport)

    # 3. Prompt template formatted with output parser instructions
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert lead software engineer performing code review.\n"
                "Analyze the provided git diff carefully and identify all security issues, bugs, and performance flaws.\n\n"
                "CRITICAL REQUIREMENTS:\n"
                "1. If there are any issues, you MUST add a finding object to the 'findings' array for EVERY issue identified.\n"
                "2. Do NOT leave 'findings' empty if security or logic errors exist in the diff.\n\n"
                "{format_instructions}",
            ),
            (
                "human",
                "Please review the following git diff and output all findings:\n\n```diff\n{diff}\n```",
            ),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | llm | parser
    return chain