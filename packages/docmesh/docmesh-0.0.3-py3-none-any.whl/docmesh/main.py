import os
import uuid

from typing import Any
from pydantic import BaseModel

from fastapi import status, Depends, HTTPException, Response, FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from docmesh.prompt import MEMORY_REACT_PROMPT
from docmesh.db.auth import get_entity_from_auth
from docmesh.toolkit import EntityToolkit, PaperToolkit, RecommendToolkit

app = FastAPI()
auth_scheme = HTTPBearer()


class AgentBody(BaseModel):
    session_id: str
    query: str


def _check_access_token(access_token: str) -> str:
    if (entity_name := get_entity_from_auth(access_token)) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return entity_name


@app.post("/login")
def login(
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    entity_name = _check_access_token(token.credentials)
    session_id = str(uuid.uuid4())
    data = {"entity_name": entity_name, "session_id": session_id}

    return {"data": data}


def _execute_agent(entity_name: str, query: str, session_id: str) -> str:
    # setup react prompt
    prompt = MEMORY_REACT_PROMPT
    # setup llm
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
    # set up all tools
    tools = [
        *EntityToolkit(entity_name=entity_name).get_tools(),
        *PaperToolkit(entity_name=entity_name).get_tools(),
        *RecommendToolkit(entity_name=entity_name).get_tools(),
    ]
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
    result = agent_with_memory.invoke(
        {"input": query},
        config={"configurable": {"session_id": session_id}},
    )
    # retrieve output
    output = result["output"]

    return output


@app.post("/agent")
def agent(
    body: AgentBody,
    response: Response,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> dict[str, Any]:
    entity_name = _check_access_token(token.credentials)

    try:
        output = _execute_agent(entity_name, body.query, body.session_id)
        data = {"input": body.query, "output": output}
    except Exception as e:
        output = f"Failed to answer with error:\n{e}"
        data = {"input": body.query, "output": output}

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return {"data": data}
