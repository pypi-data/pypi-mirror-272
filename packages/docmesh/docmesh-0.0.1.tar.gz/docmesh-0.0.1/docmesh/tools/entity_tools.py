import os

from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from langchain.callbacks.manager import CallbackManagerForToolRun

from .base import BaseAgentTool
from ..db import follow_entity


class FollowEntityToolInput(BaseModel):
    name: str = Field(description="entity name")


class FollowEntityTool(BaseAgentTool):
    name: str = "follow an entity"
    description: str = "uesful when you need to follow an entity"
    args_schema: Type[BaseModel] = FollowEntityToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        follow_entity(self.entity_name, name)
        return f"\nSuccessfully follow entity {name}\n"
