import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from langchain.callbacks.manager import CallbackManagerForToolRun

from .base import BaseAgentTool
from ..utils.graph_utils import find_max_degree_nodes


class CiteGraphVisualizeToolInput(BaseModel):
    gml_file: str = Field(description="gml file to visualize")


class CiteGraphVisualizeTool(BaseAgentTool):
    name: str = "cite graph visualize tool"
    description: str = (
        "useful when you need to visualize a cite graph, return a png file for a given gml format cite graph. "
    )
    args_schema: Type[BaseModel] = CiteGraphVisualizeToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        gml_file: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        if not os.path.exists(gml_file):
            self._raise_tool_error(f"Cannot find gml file {gml_file}, please check your provided file name.")

        # read gml file
        G = nx.read_gml(gml_file)
        # draw networkx
        nx.draw_networkx(G, width=0.1, with_labels=False, node_size=1)

        # generate png file
        png_file = f"{os.path.splitext(gml_file)[0]}.png"
        # save png file
        plt.savefig(png_file, dpi=200)

        return f"\nCite graph visualized plot is saved to {png_file}.\n"


class PopularPaperToolInput(BaseModel):
    gml_file: str = Field(description="gml file to analyze")


class PopularPaperTool(BaseAgentTool):
    name: str = "popluar paper analysis tool"
    description: str = (
        "useful when you need to find out the popluar paper, "
        "return a list of paper ids for a given gml format cite graph. "
    )
    args_schema: Type[BaseModel] = PopularPaperToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        gml_file: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        if not os.path.exists(gml_file):
            self._raise_tool_error(f"Cannot find gml file {gml_file}, please check your provided file name.")

        # read gml file
        G = nx.read_gml(gml_file)
        # convert G to adj_mat
        A = nx.adjacency_matrix(G, G.nodes)
        # find max degree nodes
        node_indices = find_max_degree_nodes(A)
        nodes = np.array(G.nodes)[node_indices]
        nodes_repr = ", ".join(nodes)

        return f"\n{nodes_repr}\n"
