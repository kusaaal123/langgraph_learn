from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from ..schemas.models import ReviewReport
from ..tools.git_tools import read_git_diff

load_dotenv()

def get_tool_bound_model():
    """
    Returns ChatNVIDIA model with read_git_diff tool bound.
    """

    model_id = "minimaxai/minimax-m3"
    # model_id = "minimaxai/minimax-m3"
    llm = ChatNVIDIA(
        model=model_id,
        temperature=0.1,
        timeout=200,
        max_completion_tokens=16384
    )

    return llm.bind_tools([read_git_diff])

def run_react_agent(user_query: str) -> ReviewReport:
    """
    Executes a manual ReAct loop:
    1. Sends initial query to LLM with tools bound.
    2. While LLM requests tool execution:
       - Runs the requested tool (e.g., read_git_diff)
       - Appends ToolMessage output to message history
       - Re-invokes model with updated history
    3. Parses final response into structured ReviewReport.
    """
    llm_with_tools = get_tool_bound_model()
    
    # Tool registry map for dynamic lookup
    tools_by_name = {read_git_diff.name: read_git_diff}
    
    parser = PydanticOutputParser(pydantic_object=ReviewReport)
    
    messages = [
        SystemMessage(content=(
            "You are an expert lead software engineer performing code review.\n"
            "You have access to git tools. Call `read_git_diff` to inspect repository changes before analyzing.\n"
            "Output your final findings adhering strictly to the structured schema format.\n\n"
            f"{parser.get_format_instructions()}"
        )),
        HumanMessage(content=user_query)
    ]

    # ReAct Loop
    while True:
        response = llm_with_tools.invoke(messages)
        print(f"🤖 [ReAct Agent] Model Response:\n{response.content}\n")
        messages.append(response)

        # Check if the model called any tools
        if not response.tool_calls:
            # Final output reached; parse structured result
            return parser.parse(response.content)

        # Execute all requested tool calls
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            print(f"🔧 [ReAct Agent] Calling Tool: `{tool_name}` with args: {tool_args}")
            
            tool_to_call = tools_by_name.get(tool_name)
            if tool_to_call:
                output = tool_to_call.invoke(tool_args)
            else:
                output = f"Error: Tool '{tool_name}' not found."

            # Append ToolMessage with exact matching tool_call_id
            messages.append(ToolMessage(content=str(output), tool_call_id=tool_id))

# def get_review_chain():
#    """
#    Build and return an LCEL chain for code review.
#    
#    Composition: prompt | llm | parser
#    """

    # 1. Use a supported model with low temperature for deterministic JSON output

    #model_id = "meta/llama-3.3-70b-instruct"
    model_id = "minimaxai/minimax-m3"

    llm = ChatNVIDIA(
        model=model_id,
        temperature=0.1,
        timeout=200,
        max_completion_tokens=16384
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