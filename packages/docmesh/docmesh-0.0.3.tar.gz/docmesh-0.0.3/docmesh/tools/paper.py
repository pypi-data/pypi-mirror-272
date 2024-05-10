from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from langchain.callbacks.manager import CallbackManagerForToolRun

from .base import BaseAgentTool
from ..utils.semantic_scholar import PaperIdNotFound
from ..db.neo import (
    add_paper,
    read_paper,
    get_paper_from_id,
    get_paper_from_title,
    list_latest_papers,
)


class AddPaperToolInput(BaseModel):
    title: str = Field(description="paper title")


class AddPaperTool(BaseAgentTool):
    name: str = "add_paper"
    description: str = "useful when you need to add a paper to database"
    args_schema: Optional[Type[BaseModel]] = AddPaperToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        title: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        title = self._preporcess_input(title)
        try:
            paper = add_paper(title)
        except PaperIdNotFound:
            self._raise_tool_error(f"Cannot find paper id for paper {title}, you may end execution.")

        msg = f"Successfully add paper {title} with id {paper.paper_id} into neo4j database."
        return f"\n{msg}\n"


class GetPaperIdToolInput(BaseModel):
    title: str = Field(description="paper title")


class GetPaperIdTool(BaseAgentTool):
    name: str = "get_paper_id"
    description: str = "useful when you need to find a paper id"
    args_schema: Optional[Type[BaseModel]] = GetPaperIdToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        title: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        title = self._preporcess_input(title)
        paper_id = get_paper_from_title(title=title).paper_id
        msg = f"Successfully find paper id {paper_id} for {title}."
        return f"\n{msg}\n"


class MarkPaperReadToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class MarkPaperReadTool(BaseAgentTool):
    name: str = "mark_paper_read"
    description: str = "useful when you need to mark a paper be read"
    args_schema: Optional[Type[BaseModel]] = MarkPaperReadToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)
        read_paper(entity_name=self.entity_name, paper_id=paper_id)
        msg = f"Successfully mark paper {paper_id} read."
        return f"\n{msg}\n"


class PaperSummaryToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class PaperSummaryTool(BaseAgentTool):
    name: str = "paper_summary"
    description: str = (
        "useful when you need to genearte the paper summary, return a short summary for a given paper id."
    )
    args_schema: Optional[Type[BaseModel]] = PaperSummaryToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)
        paper = get_paper_from_id(paper_id=paper_id)
        msg = paper.summary
        return f"\n{msg}\n"


class ListLatestPaperToolInput(BaseModel):
    n: str = Field(description="number of papers")


class ListLatestPaperTool(BaseAgentTool):
    name: str = "list_latest_papers"
    description: str = (
        "useful when you need to find out latest reading papers, "
        "return a list of paper ids and titles for a given number."
    )
    args_schema: Optional[Type[BaseModel]] = ListLatestPaperToolInput
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

        df = list_latest_papers(entity_name=self.entity_name, n=n)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"
