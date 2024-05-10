from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from datetime import datetime
from langchain.callbacks.manager import CallbackManagerForToolRun

from .base import BaseAgentTool
from ..db.neo import (
    list_unread_follows_papers,
    list_unread_influential_papers,
)


class UnreadFollowsToolInput(BaseModel):
    n: str = Field(description="number of papers")


class UnreadFollowsTool(BaseAgentTool):
    name: str = "recommand_papers_from_follows"
    description: str = "useful when you need to get some recommanded papers from follows"
    args_schema: Optional[Type[BaseModel]] = UnreadFollowsToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        n = self._preporcess_input(n)
        try:
            n = int(n)
        except Exception:
            self._raise_tool_error(
                "Input argument `n` should be an integer, please check your inputt. "
                "Pay attention that you MUST ONLY input the number, like 1, 3, 5.\n"
            )

        df = list_unread_follows_papers(entity_name=self.entity_name, n=n)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class UnreadInfluentialToolInput(BaseModel):
    date_time: str = Field(description="publication date time of papers")


class UnreadInfluentialTool(BaseAgentTool):
    name: str = "recommand_latest_influential_papers"
    description: str = "useful when you need to get some influential papers from a given date"
    args_schema: Optional[Type[BaseModel]] = UnreadInfluentialToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        date_time: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        date_time = self._preporcess_input(date_time)
        try:
            datetime.strptime(date_time, "%Y-%m-%d")
        except Exception:
            self._raise_tool_error(
                "Input argument `date_time` should be written in format `YYYY-MM-DD`, "
                "please check your input, valid input can be 1995-03-01, 2024-01-01.\n"
            )

        df = list_unread_influential_papers(entity_name=self.entity_name, date_time=date_time)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"
