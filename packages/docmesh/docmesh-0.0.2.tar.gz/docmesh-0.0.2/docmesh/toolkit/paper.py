from langchain_core.tools import BaseToolkit

from ..tools.base import BaseAgentTool
from ..tools.paper import (
    AddPaperTool,
    GetPaperIdTool,
    MarkPaperReadTool,
    PaperSummaryTool,
    ListLatestPaperTool,
)


class PaperToolkit(BaseToolkit):
    entity_name: str

    def get_tools(self) -> list[BaseAgentTool]:
        return [
            AddPaperTool(entity_name=self.entity_name),
            GetPaperIdTool(entity_name=self.entity_name),
            MarkPaperReadTool(entity_name=self.entity_name),
            PaperSummaryTool(entity_name=self.entity_name),
            ListLatestPaperTool(entity_name=self.entity_name),
        ]
