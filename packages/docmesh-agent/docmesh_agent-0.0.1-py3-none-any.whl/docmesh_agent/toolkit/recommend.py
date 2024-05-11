from langchain_core.tools import BaseToolkit

from docmesh_agent.tools.base import BaseAgentTool
from docmesh_agent.tools.recommend import (
    UnreadFollowsTool,
    UnreadInfluentialTool,
)


class RecommendToolkit(BaseToolkit):
    entity_name: str

    def get_tools(self) -> list[BaseAgentTool]:
        return [
            UnreadFollowsTool(entity_name=self.entity_name),
            UnreadInfluentialTool(entity_name=self.entity_name),
        ]
