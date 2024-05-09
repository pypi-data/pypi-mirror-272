import os
import pandas as pd
import networkx as nx

from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from datetime import datetime
from langchain.callbacks.manager import CallbackManagerForToolRun

from .base import BaseAgentTool
from ..db import (
    Paper,
    add_paper,
    get_paper,
    get_latest_papers,
    get_latest_citegraph,
    get_unread_follows_papers,
    get_unread_influential_papers,
)
from ..utils import get_paper_id, get_references, get_paper_details


class PaperIdNotFound(Exception):
    ...


def add_paper_to_neo4j(title: str) -> Paper:
    paper_id = get_paper_id(title)
    if paper_id is None:
        raise PaperIdNotFound(f"Cannot find semantic scholar paper id for {title}.")
    paper = get_paper_details([paper_id])

    references_ids = get_references(paper_id)
    if len(references_ids) == 0:
        references = pd.DataFrame()
    else:
        references = get_paper_details(references_ids)

    neo4j_paper = add_paper(paper, references)
    return neo4j_paper


class AddPaperToolInput(BaseModel):
    title: str = Field(description="paper title")


class AddPaperTool(BaseAgentTool):
    name: str = "add a new paper"
    description: str = "useful when you need to add a paper to neo4j database"
    args_schema: Type[BaseModel] = AddPaperToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        title: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            paper = add_paper_to_neo4j(title)
        except PaperIdNotFound:
            self._raise_tool_error(f"Cannot find paper id for paper {title}, you may end execution.")

        msg = f"Successfully add paper {title} with id {paper.paper_id} into neo4j database."
        return f"\n{msg}\n"


class GetLatestPaperToolInput(BaseModel):
    n: str = Field(description="number of papers")


class GetLatestPaperTool(BaseAgentTool):
    name: str = "get latest paper tool"
    description: str = (
        "useful when you need to find out latest reading papers, "
        "return a list of paper ids and titles for a given number."
    )
    args_schema: Type[BaseModel] = GetLatestPaperToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            n = int(n)
        except Exception:
            self._raise_tool_error(
                "Input argument `n` should be an integer, please check your inputt. "
                "Pay attention that you MUST ONLY input the number, like 1, 3, 5.\n"
            )

        # fetch latest paper
        df = get_latest_papers(name=self.entity_name, n=n)

        papers = "\n".join(
            df.apply(
                lambda x: f"paper id: {x['paper_id']}, paper title: {x['title']}",
                axis=1,
            ),
        )
        return f"\n{papers}\n"


class PaperSummaryToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class PaperSummaryTool(BaseAgentTool):
    name: str = "paper summary tool"
    description: str = (
        "useful when you need to genearte the paper summary, return a short summary for a given paper id."
    )
    args_schema: Type[BaseModel] = PaperSummaryToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        # retrieve paper
        paper = get_paper(paper_id=paper_id)

        return f"\n{paper.summary}\n"


class UnreadFollowsToolInput(BaseModel):
    n: str = Field(description="number of papers")


class UnreadFollowsTool(BaseAgentTool):
    name: str = "recommand papers from follows"
    description: str = "useful when you need to get some recommanded papers from follows"
    args_schema: Type[BaseModel] = UnreadFollowsToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            n = int(n)
        except Exception:
            self._raise_tool_error(
                "Input argument `n` should be an integer, please check your inputt. "
                "Pay attention that you MUST ONLY input the number, like 1, 3, 5.\n"
            )

        # fetch recommandation
        df = get_unread_follows_papers(name=self.entity_name, n=n)

        papers = "\n".join(
            df.apply(
                lambda x: f"paper title: {x['title']}, pdf link: {x['pdf']}",
                axis=1,
            ),
        )
        return f"\n{papers}\n"


class UnreadInfluentialToolInput(BaseModel):
    date_time: str = Field(description="publication date time of papers")


class UnreadInfluentialTool(BaseAgentTool):
    name: str = "recommand latest influential papers"
    description: str = "useful when you need to get some influential papers from a given date"
    args_schema: Type[BaseModel] = UnreadInfluentialToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        date_time: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            datetime.strptime(date_time, "%Y-%m-%d")
        except Exception:
            self._raise_tool_error(
                "Input argument `date_time` should be written in format `YYYY-MM-DD`, "
                "please check your input, valid input can be 1995-03-01, 2024-01-01.\n"
            )

        # fetch recommandation
        df = get_unread_influential_papers(name=self.entity_name, date_time=date_time)

        papers = "\n".join(
            df.apply(
                lambda x: f"paper title: {x['title']}, pdf link: {x['pdf']}",
                axis=1,
            ),
        )
        return f"\n{papers}\n"


class CiteGraphToolInput(BaseModel):
    n: str = Field(description="number of papers")


class CiteGraphTool(BaseAgentTool):
    name: str = "cite graph generation tool"
    description: str = (
        "useful when you need to generate a cite graph from papers, "
        "return a gml format of cite graph for a given number."
    )
    args_schema: Type[BaseModel] = CiteGraphToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        try:
            n = int(n)
        except Exception:
            self._raise_tool_error(
                "Input argument `n` should be an integer, please check your inputt. "
                "You can directly call this function to generate cite graph for latest papers. "
                "Pay attention that you MUST ONLY input the number, like 1, 3, 5.\n"
            )

        # fetch latest citegraph
        df = get_latest_citegraph(name=self.entity_name, n=n)

        G = nx.Graph()
        G.add_edges_from(zip(df["p1_paper_id"], df["p2_paper_id"]))

        # generate gml file
        gml_file = f"{datetime.now().strftime('%Y-%m-%d-%H%M%S')}.gml"
        nx.write_gml(G, gml_file)

        return f"\nCite graph is generate as gml file {gml_file}.\n"
