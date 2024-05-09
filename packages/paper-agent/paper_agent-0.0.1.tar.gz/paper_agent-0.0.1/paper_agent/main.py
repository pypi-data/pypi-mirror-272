import os
import uuid

from typing import Any
from pydantic import BaseModel

from fastapi import status, FastAPI, Response
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from paper_agent.db import get_entity
from paper_agent.tools import (
    FollowEntityTool,
    AddPaperTool,
    GetLatestPaperTool,
    PaperSummaryTool,
    UnreadFollowsTool,
    UnreadInfluentialTool,
    CiteGraphTool,
    CiteGraphVisualizeTool,
    PopularPaperTool,
)
from paper_agent.prompt import MEMORY_REACT_PROMPT

AVAILABLE_TOOLS = [
    FollowEntityTool,
    AddPaperTool,
    GetLatestPaperTool,
    PaperSummaryTool,
    UnreadFollowsTool,
    UnreadInfluentialTool,
    CiteGraphTool,
    CiteGraphVisualizeTool,
    PopularPaperTool,
]


app = FastAPI()


class LoginBody(BaseModel):
    entity_name: str


class AgentBody(BaseModel):
    entity_name: str
    session_id: str
    query: str


@app.post("/login")
def entity_login(body: LoginBody, response: Response) -> dict[str, Any]:
    try:
        get_entity(name=body.entity_name)

        session_id = str(uuid.uuid4())
        data = {
            "msg": "Successfully to get a session id.",
            "session_id": session_id,
        }
    except Exception:
        session_id = None
        data = {
            "msg": "Failed to get a session id, since you are not registered.",
            "session_id": session_id,
        }
        response.status_code = status.HTTP_401_UNAUTHORIZED

    return {"data": data}


@app.post("/agent")
def agent_execution(body: AgentBody, response: Response) -> dict[str, Any]:
    # setup react prompt
    prompt = MEMORY_REACT_PROMPT
    # setup llm
    llm = ChatOpenAI(model="gpt-4-0125-preview")
    # set up all tools
    tools = [tool(entity_name=body.entity_name) for tool in AVAILABLE_TOOLS]
    # setup ReAct agent
    agent = create_react_agent(llm, tools, prompt)
    # setup agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    # setup memory database
    memory_store = os.getenv("MYSQL_URL")
    # bind agent and memory
    agent_with_memory = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: SQLChatMessageHistory(
            session_id=session_id,
            connection_string=memory_store,
        ),
        input_messages_key="input",
        history_messages_key="chat_history",
    )
    # run the agent!
    try:
        result = agent_with_memory.invoke(
            {"input": body.query},
            config={"configurable": {"session_id": body.session_id}},
        )
        data = {"input": body.query, "output": result["output"]}
    except Exception as e:
        data = {"input": body.query, "output": f"Failed to answer with error: {e}."}
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": data}
