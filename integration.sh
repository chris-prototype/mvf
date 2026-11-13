# integration
# integration is implemented as MCP

# this script contains functions for testing MCP connections
# - mock  
# - github
#

# mock server
mcp-local() {
  npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-everything
}

# MVF_GITHUB holds the Personal Access Token used to interact with github; currently saved as a secret
mcp-github() {
  npx -y @modelcontextprotocol/inspector --config config/mcp.json --server github --header "Authorization: Bearer $MVF_GITHUB"
}

mcp-linear() {
  npx -y @modelcontextprotocol/inspector --config config/mcp.json --server linear --header "Authorization: Bearer $MVF_LINEAR"
}
