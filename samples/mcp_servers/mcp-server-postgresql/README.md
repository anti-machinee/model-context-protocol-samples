# Check list

# Setup project
## uv
```bash
uv init mcp-server-postgresql
uv venv
uv sync
```

# Setup PostgreSQL
- Setup Docker container
```bash
docker pull postgres
docker run --name my-postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase \
  -p 5432:5432 \
  -d postgres
docker exec -it my-postgres /bin/bash
```
- Setup database
```bash
psql -U myuser -d mydatabase
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE providers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users (name, email)
VALUES ('Alice Smith', 'alice@example.com');
INSERT INTO providers (name, email)
VALUES ('David Atton', 'david@example.com');
```

# Deploy with Claude desktop
## Setup
- Edit `claude_desktop_config.json`
    - Windows: `"C:\Users\duong\AppData\Roaming\Claude\claude_desktop_config.json"`
## Python command
- Setup
```bash
{
    "mcpServers": {
        "postgresql": {
            "command": "wsl",
            "args": [
                "/home/duongdq/.local/bin/uv",
                "--directory",
                "/mnt/c/Users/duong/workspace/projects/personal_projects/ai-foundation/model-context-protocol-samples/samples/mcp_servers/mcp-server-postgresql/src/mcp-server-postgresql",
                "run",
                "main.py"
            ]
        }
    }
}
```

## uvx command
## uv Command
## docker command

# Test
## Test from Claude desktop
- Test list_resources
```json
{
    "user": "list schema in this database"
}
I'll help you list the schema information from the database. I'll use the SQL query function to get this information from the system catalog.
[Calling tool query with args {'sql': "SELECT \n    table_schema,\n    table_name,\n    column_name,\n    data_type,\n    character_maximum_length,\n    column_default,\n    is_nullable\nFROM \n    information_schema.columns\nWHERE \n    table_schema NOT IN ('pg_catalog', 'information_schema')\nORDER BY \n    table_schema,\n    table_name,\n    ordinal_position;"}]
From the provided data, there are 3 tables in the public schema:

1. provider
   - id (integer, not null, auto-increment)
   - name (text, not null)
   - email (text, not null)
   - created_at (timestamp, nullable, defaults to CURRENT_TIMESTAMP)

2. providers
   - id (integer, not null, auto-increment)
   - name (text, not null)
   - email (text, not null)
   - created_at (timestamp, nullable, defaults to CURRENT_TIMESTAMP)

3. users
   - id (integer, not null, auto-increment)
   - name (text, not null)
   - email (text, not null)
   - created_at (timestamp, nullable, defaults to CURRENT_TIMESTAMP)

Note: It appears that there might be a redundancy with "provider" and "providers" tables as they have identical structure.
```
- Test read_resource
```json
{
    "user": "read resource given uri mydatabase/users/schema"
}

I'll help you retrieve the schema information for the users table in mydatabase. I can use a SQL query to inspect the table structure.
[Calling tool query with args {'sql': "SELECT \n    column_name, \n    data_type, \n    character_maximum_length,\n    column_default,\n    is_nullable\nFROM information_schema.columns \nWHERE table_name = 'users';"}]
I'll help you understand the schema of the "users" table from the database:

The table has 4 columns:

1. id
   - Type: integer
   - Auto-increment (uses sequence 'users_id_seq')
   - Not nullable (NO)

2. created_at
   - Type: timestamp without time zone
   - Default value: CURRENT_TIMESTAMP
   - Nullable (YES)

3. name
   - Type: text
   - No default value
   - Not nullable (NO)

4. email
   - Type: text
   - No default value
   - Not nullable (NO)

This appears to be a basic users table with an auto-incrementing ID, creation timestamp, and required name and email fields.
```
- Test list_tools
```json
{
    "user": "what functionalities you support"
}

I can help you interact with a PostgreSQL database through SQL queries. Specifically, I can:

1. Execute read-only SQL queries using the `query` function
- This allows us to SELECT data from database tables
- We can perform data analysis, filtering, aggregations, joins, etc.
- The queries must be read-only (no INSERT, UPDATE, DELETE, or other data modifications)

To better assist you, I can first check what tables and schema information are available in the database:
[Calling tool query with args {'sql': "SELECT table_name \nFROM information_schema.tables \nWHERE table_schema = 'public';"}]
Based on the information provided, I understand I can help with functionalities related to:

1. Users
2. Provider 
3. Providers

I can engage in conversations and assist with queries related to these topics. Would you like to know more about any specific functionality or do you have a particular question about any of these areas?
```
- Test call_tool
```json
{
    "user": "query data in users table"
}

I'll help you query the users table. Let me check its contents with a basic SELECT statement.
[Calling tool query with args {'sql': 'SELECT * FROM users;'}]
This appears to be a result from querying a users table with one record. Let me break down the data:

The record contains:
- ID: 1
- Name: "Alice Smith"
- Email: "alice@example.com" 
- Timestamp: "2025-04-18T07:31:24.415137"

The data is structured as a nested array where each inner array represents a row from the users table. In this case, there is only one row.

The format suggests this could be JSON data returned from a database query, with fields that are likely structured as:
- id (integer)
- name (string)
- email (string) 
- created_at/updated_at (datetime)
```
## Test from client
- Same as Test from Claude desktop

# References
- [1] https://github.com/modelcontextprotocol/servers/tree/main/src/postgres
