# MCP Setup Guide for Windows

## Required API Keys

Add these to your `.env` file:

```env
# Supabase (already configured)
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_DATABASE_URL=postgresql://user:pass@host:port/db

# GitHub Integration
GITHUB_TOKEN=ghp_your_personal_access_token

# Web Search (choose one)
BRAVE_API_KEY=your_brave_search_key
# OR
SERPER_API_KEY=your_serper_key
```

## Installing MCPs on Windows

### Prerequisites
1. Ensure Node.js is installed and added to PATH
2. Open Command Prompt or PowerShell as Administrator (recommended for global installs)

### 1. Supabase MCP
```cmd
# Provides direct Supabase operations
npm install -g @supabase/mcp-server
```

**If you get permission errors, try:**
```cmd
# Alternative: Install without -g flag and use npx
npm install @supabase/mcp-server
# Then use: npx @supabase/mcp-server
```

Benefits:
- Real-time database queries
- Row-level security integration
- Storage and auth operations

### 2. GitHub MCP  
```cmd
# Repository and workflow management
npm install -g @modelcontextprotocol/server-github
```

Benefits:
- Create/manage issues and PRs
- Repository browsing
- CI/CD workflow management

### 3. Web Search MCP
```cmd
# For research agent web search
npm install -g @modelcontextprotocol/server-brave-search
```

Benefits:
- Real-time web research
- Company/prospect intelligence
- News and social signals

### 4. Postgres MCP
```cmd
# Advanced database operations
npm install -g @modelcontextprotocol/server-postgres
```

Benefits:
- Complex analytics queries
- Database performance optimization
- Schema management

## Claude Code Configuration (Windows)

### 1. Locate Claude Code Settings Directory
The Claude Code configuration file location on Windows:
```
%APPDATA%\Claude\claude_desktop_config.json
```

Full path typically:
```
C:\Users\{YourUsername}\AppData\Roaming\Claude\claude_desktop_config.json
```

### 2. Copy MCP Config (Windows Methods)

**Method A: Command Prompt**
```cmd
# Copy our MCP config to Claude Code settings
copy .claude-code\mcp-config.json "%APPDATA%\Claude\claude_desktop_config.json"
```

**Method B: PowerShell**  
```powershell
# Copy using PowerShell
Copy-Item -Path ".claude-code\mcp-config.json" -Destination "$env:APPDATA\Claude\claude_desktop_config.json"
```

**Method C: Windows Explorer**
1. Open Windows Explorer
2. Type `%APPDATA%\Claude` in the address bar
3. Copy `mcp-config.json` from your `.claude-code` folder to this directory
4. Rename it to `claude_desktop_config.json`

### 3. Alternative: Manual Configuration
If the copy doesn't work, manually create the config file:

1. Open Notepad as Administrator
2. Navigate to `%APPDATA%\Claude\`
3. Create new file named `claude_desktop_config.json`
4. Copy the content from `.claude-code\mcp-config.json`

### 4. Restart Claude Code
```cmd
# Close Claude Code completely
# Restart Claude Code application
```

### 3. Verify MCP Connection
Ask Claude Code to:
- Query your Supabase tables
- List GitHub repositories  
- Perform a web search
- Run a database query

## Project-Specific MCP Usage

### Research Workflows
```javascript
// Example: Research a company using web search MCP
const searchResults = await webSearch("OpenAI company funding news 2024");
const companyData = await supabase.table('companies').insert({
  name: 'OpenAI', 
  research_data: searchResults
});
```

### Database Operations
```javascript
// Complex analytics using Postgres MCP
const leadScores = await postgres.query(`
  SELECT company_id, 
         AVG(engagement_score) as avg_engagement,
         COUNT(prospects) as prospect_count
  FROM research_results 
  GROUP BY company_id 
  ORDER BY avg_engagement DESC
`);
```

### Development Automation
```javascript
// GitHub MCP for automated PR creation
await github.createPullRequest({
  title: "Add new research agent",
  body: "Implements LinkedIn prospect research with validation",
  head: "feature/linkedin-agent",
  base: "main"
});
```

## Troubleshooting

### MCP Not Loading
1. Check environment variables are set
2. Verify MCP packages are installed globally
3. Restart Claude Code application
4. Check Claude Code logs for MCP connection errors

### Permissions Issues
- Ensure GitHub token has repo access
- Verify Supabase RLS policies allow operations
- Check API key quotas and limits

### Performance Optimization
- Cache frequent web searches
- Use database connection pooling
- Implement rate limiting for API calls