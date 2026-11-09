# integration
# integration is implemented as MCP

# this script contains functions for testing MCP connections; it requires that API keys are configured
# - local  
# - github
#

mcp-local() {
  npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-everything
}

mcp-github() {
  npx -y @modelcontextprotocol/inspector --config config/mcp.json --server github --header "Authorization: Bearer $MVF_GITHUB"
}