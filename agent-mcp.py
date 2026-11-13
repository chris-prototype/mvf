import asyncio
import os
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    client = genai.Client()
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={**os.environ},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents="List my top 3 GitHub repositories.",
                config=types.GenerateContentConfig(tools=[session]),
            )
            print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
