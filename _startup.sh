# contains functions for testing MCP connections from github codespaces to:
# local  
# github
#

mcp-local() {
  npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-everything
}

mcp-github() {
  npx -y @modelcontextprotocol/inspector --config mcp.json --server github --header "Authorization: Bearer $MVF_GITHUB"
}