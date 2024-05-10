from langchain_core.tools import BaseToolkit

from ..tools.base import BaseAgentTool
from ..tools.entity import (
    FollowEntityTool,
    ListFollowsTool,
    ListPopularEntitiesTool,
)


class EntityToolkit(BaseToolkit):
    entity_name: str

    def get_tools(self) -> list[BaseAgentTool]:
        return [
            FollowEntityTool(entity_name=self.entity_name),
            ListFollowsTool(entity_name=self.entity_name),
            ListPopularEntitiesTool(entity_name=self.entity_name),
        ]
