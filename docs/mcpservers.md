# MCP Server Guide

## Introduction

[Model Context Protocol](https://modelcontextprotocol.io/) (MCP) is an open-source standard for connecting AI applications to external systems. Using MCP, AI applications like Claude or ChatGPT can connect to data sources (e.g. local files, databases), tools (e.g. search engines, calculators) and workflows (e.g. specialized prompts). Enabling them to access key information and perform tasks. MCP follows a client-server architecture where an MCP host, an AI application like Claude Code or Codex, establishes connections to one or more MCP servers. The MCP host accomplishes this by creating one MCP client for each MCP server. Each MCP client maintains a dedicated connection with its corresponding MCP server. The [Tool](genaibuilder.md#tool) GenAI Component allows Vantiq applications to act as an MCP client. In this document we will cover how to create an [MCP server](https://modelcontextprotocol.io/docs/learn/server-concepts) hosted by the Vantiq platform.

## Defining an MCP Server

To create an MCP Server, select the "Add...MCP Server" menu item in the Vantiq IDE to bring up the MCP Server editor:

![MCP Server Editor](./assets/img/mcpservers/MCPServerEditor.png)

Here we can provide the basic definition of the server and define its features.

### MCP Server Resource

MCP Servers are a packaged resource, which means that we must provide a resource name and an optional package.  Together these form the server's unique resource id (here that's `com.vantiq.TestMCPServer`).  When defining an MCP Server in an [organization namespace](namespaces.md#organization-administration-tasks), it can be marked as being "organization wide".  This means that it can be used by any namespace that belongs to the organization. Otherwise, the MCP server will only be visible in the namespace in which it was defined.

### MCP Server Info

When an MCP Client connects to an MCP Server, the server responds with a description of its capabilities and general information, including:

* Server Name -- the name of the MCP Server (can be used as a display name by the client).  Defaults to the Vantiq resource id if not specified.
* Version -- the version of the MCP Server.  Note that this is not the MCP protocol version, but a version string that is specific to this MCP Server.
* Instructions -- a context document that can be used by the MCP host/client to understand and guide interactions with the MCP Server. The intent is that they describe the [specifics](https://blog.modelcontextprotocol.io/posts/2025-11-03-using-server-instructions/) of how the MCP server should be used.

All of these are optional, though the use of server instructions is highly recommended.

### MCP Server Features

MCP Servers provide their functionality by defining one or more server features to be used by the MCP client.

#### Tools

Tools enable AI models to perform actions. Each tool defines a specific operation with typed inputs and outputs. The model requests tool execution based on context. Tools are defined by referencing [services](services.md) and/or [procedures](rules.md#procedures):

![Tool Definition](./assets/img/mcpservers/ToolDefinition.png)

When referencing a service, there will be one MCP tool defined for each of the service's public procedures. The description of the tool will be taken from the underlying procedure's description.

#### Resources

Resources expose context to the AI model. Applications can access this information directly and decide how to use it, whether that’s selecting relevant portions, searching with embeddings, or passing it all to the model. Each resource has a unique URI (e.g., `<mcp server>://path/to/document.md`) and declares its MIME type for appropriate content handling. Resources are defined by referencing [documents](resourceguide.md#documents):

![Resource Definition](./assets/img/mcpservers/ResourceDefinition.png)

The resource path and MIME type will be taken from the referenced document. The rest of the resource definition (name, title, and description) are provided by the developer.

#### Resource Templates

Resource templates describe a pattern through which multiple context documents can be accessed. They have dynamic URIs with parameters for flexible queries. For example:

* `travel://activities/{city}/{category}`` - returns activities by city and category
* `travel://activities/barcelona/museums` - returns all museums in Barcelona

Resource Templates include metadata such as title, description, and expected MIME type, making them discoverable and self-documenting.

![Resource Template Definition](./assets/img/mcpservers/ResourceTemplateDefinition.png)

#### Prompts

Prompts provide reusable templates. They allow MCP server authors to provide parameterized prompts for a domain, or showcase how to best use the MCP server. Prompts are defined by referencing a prompt template [document](resourceguide.md#documents):

![Prompt Definition](./assets/img/mcpservers/PromptDefinition.png)

The referenced document is assumed to contain one or more substitution variables which will be exposed as `arguments` in the MCP prompt definition.

## Accessing an MCP Server

Once an MCP Server has been defined, it will be made available at the URI `<vantiqServer>/mcp/<mcpServerResourceId>`. For example, if we assume that the MCP Server shown earlier is defined on the "dev" Vantiq server, then its URI would be: `https://dev.vantiq.com/mcp/com.vantiq.TestMCPServer`. Accessing the MCP Server at this URI requires an access token which grants at least the "user" profile in the current namespace and "expandedUser" in the system namespace.  For example:

![Token Profiles](./assets/img/mcpservers/TokenProfiles.png)

Additional privileges can be provided if they are required by the tool procedures (though care should be taken to minimize the access that is necessary).

> The details of how the MCP Server URI and access token are specified will vary depending on the application being used.  Consult your application's documentation for this information.