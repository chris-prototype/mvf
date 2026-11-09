# contains script for testing MCP connections from github code spaces

mcp-test() {
  npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-everything
}

mcp-connect() {
  npx -y @modelcontextprotocol/inspector --config mcp.json --server github --header "Authorization: Bearer $MVF_GITHUB"
}