"""Expose general-purpose and asset helpers as MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from mcp.types import ImageContent

from tools import assets, general


def register(mcp: FastMCP) -> None:
    """Register general-purpose tools."""

    @mcp.tool(enabled=False)
    def greet(name: str) -> str:
        return general.greet(name)

    @mcp.tool()
    def get_time() -> str:
        return general.get_time()

    @mcp.tool()
    def health() -> dict:
        return general.health()

    @mcp.tool(enabled=False)
    def search(query: str) -> dict:
        return general.search(query)

    @mcp.tool(enabled=False)
    def fetch(id: str) -> dict:
        return general.fetch(id)

    @mcp.tool(enabled=False)
    def get_star() -> ImageContent:
        data = assets.fetch_star_image()
        return Image(data=data, format="png").to_image_content()

    @mcp.tool(enabled=False)
    def get_star_link() -> str:
        return assets.get_star_link()

    @mcp.tool()
    def cdbai_chat(chat: str) -> dict:
        """
        Send a request to cdbai_chat that searches the CellMinerCDB cancer cell line pharmacogenomics database. It normalizes the data by converting cell line and drug names to standard identfiers (i.e., Cellosaurus and PubChem, respectively). Generates and SQL query to retrieve relevant data then generates and executes Python code to respond to the user question.

        Args:
            chat (str): The user’s chat message or prompt to send to the CellMinerCDB AI chat service.

        Returns:
            dict: A dictionary representing the service’s response. The reponse will include
                Example structure:
                [
                    {
                        "type": "text",
                        "text": "{\"type\":\"plot\",\"value\":\"https://s3.us-east-1.amazonaws.com/lunean.mcp/tmp_20251121T142531.png\",\"svg\":\"https://s3.us-east-1.amazonaws.com/lunean.mcp/tmp_20251121T142531.svg\",\"normalized_prompt\":\"create violin plots of rna-seq expression for the genes twist1 and foxc2 across ccle cell lines. use python to load the ccle expression data if available, and produce a multi-panel figure with one violin plot per gene (consistent y-axis range). add clear axis labels and titles. return the result as markdown that embeds the generated plot image.\",\"code\":\"https://s3.us-east-1.amazonaws.com/lunean.mcp/tmp_20251121T142531.py\",\"csv\":\"https://s3.us-east-1.amazonaws.com/lunean.mcp/tmp_20251121T142531_01.csv\",\"original_prompt\":\"Create violin plots of RNA-seq expression for the genes TWIST1 and FOXC2 across CCLE cell lines. Use Python to load the CCLE expression data if available, and produce a multi-panel figure with one violin plot per gene (consistent y-axis range). Add clear axis labels and titles. Return the result as Markdown that embeds the generated plot image.\"}"
                    }
                ]

        Notes:
            - The data is limited is row limited; make sure the user is aware
            - For queries requesting a plot  will return a link to a PNG image that should be embedded; results should be returned as Markdown that embeds the plot image
            - Other links to CSV data, SVG image, and Python code be returned as part of the answer to increase scientific transparency
            - This would not be appropriate if the user requests patient data
            - Attempt to be descriptive as possible for debugging if an error occurs; example return SQL used in the answer when an error occurs
            - Do not assume units of measurement (e.g., meters) unless a unit is clearly indicated or mentioned by the user
        """
        return general.cdbai_chat(chat)
