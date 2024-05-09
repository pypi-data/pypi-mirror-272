from typing import Optional

from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, MetaData, Table

from langchain_core.tools import BaseTool
from langchain_core.tools import ToolException


class BaseAgentTool(BaseTool):
    entity_name: str

    def _raise_tool_error(self, err_msg: str) -> None:
        raise ToolException(err_msg)
