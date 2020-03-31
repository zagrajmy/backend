from typing import Dict

from aiographql.client.client import GraphQLClient, GraphQLRequest  # type: ignore


class HasuraClient:
    """GraphQL connection client."""

    INSERT_GUILD = """
mutation insert_default_guild {
  insert_guild(
    objects: {description: "%s", name: "%s"}
  ) {
    returning {
      id
    }
  }
}
"""

    def __init__(self, url: str, auth: Dict[str, str]) -> None:
        """Create graphQL client for chosen url and credentials."""
        self._client = GraphQLClient(endpoint=url, headers=auth)

    async def _query(self, query: str) -> None:
        """Query GraphQL endpoint."""
        request = GraphQLRequest(query=query)
        await self._client.post(request)

    async def insert_guild(self, name: str, description: str) -> None:
        """Create a new guild with chosen name and description."""
        await self._query(self.INSERT_GUILD % (name, description))
