import json
from urllib.parse import urljoin, urlparse

from typing import List, Dict

from psycopg_pool import AsyncConnectionPool
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent
)

from configs import configs
from models import *
from enums import *
from functions import *
from utils import *

pool = AsyncConnectionPool(
    conninfo=configs.conninfo,
    min_size=1,
    max_size=5,
    open=False,
)


async def serve():
    server = Server("mcp-postgresql")

    @server.list_resources()
    async def list_resources() -> Dict[str, List[Resource]]:
        await pool.open()
        async with pool.connection() as client:
            try:
                async with client.cursor() as cursor:
                    result = await client.execute(
                        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                    )
                    rows = await result.fetchall()
                    resources = []
                    for row in rows:
                        resources.append(
                            Resource(
                                uri=urljoin(configs.conninfo, f"{row[0]}/schema"),
                                mimeType="application/json",
                                name=f'"{row[0]}" database schema',
                            )
                        )
                    return {"resources": resources}
            except Exception as error:
                await pool.close()
                raise error

    @server.read_resource()
    async def read_resource(arguments: dict) -> list[TextContent]:
        await pool.open()
        uri = arguments.get("uri")
        resource_url = urlparse(uri)
        path_components = resource_url.path.split("/")
        if len(path_components) < 2:
            raise ValueError("Invalid resource URI")
        schema = path_components[-1]
        table_name = path_components[-2]
        if schema != "schema":
            raise ValueError("Invalid resource URI")

        async with pool.connection() as client:
            try:
                sql = """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = %s
                """
                async with client.cursor() as cursor:
                    await cursor.execute(sql, (table_name,))
                    result = await cursor.fetchall()
                    return [
                        TextContent(
                            uri=uri,
                            mimeType="application/json",
                            type="text",
                            text=json.dumps(result, indent=2)
                        )
                    ]
            except Exception as e:
                await pool.close()
                raise e

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=PostgreSQLTools.QUERY,
                description="Run a read-only SQL query",
                inputSchema=PostgreSQLQuery.model_json_schema(),
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name == PostgreSQLTools.QUERY:
            await pool.open()
            sql = arguments.get('sql', '')
            async with pool.connection() as client:
                try:
                    async with client.cursor() as cursor:
                        await cursor.execute(sql)
                        result = await cursor.fetchall()
                        return [
                            TextContent(
                                type="text",
                                text=json.dumps(result, indent=2, default=json_serializer)
                            )
                        ]
                except Exception as error:
                    await pool.close()
                    raise error
        else:
            raise ValueError(f"Unknown tool name: {name}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
