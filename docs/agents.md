# GenAI Agent Building Guide

## Introduction

GenAI Agents (hereafter simply Agents) are [Services](services.md) which combine application logic with the use of a large language model ([LLM](resourceguide.md#llms)), either directly or via other resources such as [Semantic Indexes](resourceguide.md#semantic-indexes).  When it comes to their basic implementation including issues such as [state management](servicestatemgmt.md), Agents are just standard services.  However, the use of LLMs and the nature of the functionality they typically provide, present some unique issues.  That is what we will be focusing on in this document.

### Related Documentation

When it comes to leveraging an LLM you may be interested in the [SubmitPrompt](apps.md#submit-prompt), [AnswerQuestion](apps.md#answer-question), and [GenAIFlow](apps.md#genai-flow) activity patterns in the [Visual Event Handler Guide](apps.md). You will also want to know about [GenAI Procedures](services.md#genai-procedures) and the [GenAI Builder](genaibuilder.md). For practice adding GenAI functionality to your services see the [GenAI Builder Tutorial](tutorials/genaibuilder.md).

## Trip Planner Contribution

The *Trip Planner* project provides a skeletal example of a multi-agent system. This can be imported using the **Project...Import...Contributions** menu in the IDE:

![Trip Planner Import](./assets/img/agents/TripPlannerImport.png)

The project demonstrates some of the key elements of this document:

* Defining [Agent Skills](#agent-skills)
* [Discovering agents](#discovering-and-describing-agents)
* Applying the ReWOO [planning algorithm](#planning-agents)
* Managing client state with [discussions](#discussions)
* [Requesting user input](#agent-to-human-interaction)

We will be drawing on this application for examples throughout this document.

## Defining Agents

To create an Agent you start by creating a [Service](services.md) and check the "GenAI Agent" checkbox as shown here:

![Create Agent](./assets/img/agents/CreateAgent.png)

This triggers generation of an [A2A](https://a2a-protocol.org/latest/specification/) compliant framework which allows Agents to receive and process requests through a standard interface. See the [A2A Service](rules.md#a2a) for more details. The framework also provides a standard way for agents to request [user input](rules.md#agent) and obtain [context](rules.md#agent) related to the current request. We will see examples of all of these in the sections that follow.

### Agent Prerequisites

Implementation of the Agent's request dispatching framework requires the use of an LLM.  The generated implementation uses the LLM *io.vantiq.a2a.agentDispatch* which will be automatically defined if it does not exist in the current namespace.  The LLM is configured to use the model `openai/gpt-4.1`. It gets its OpenAI API key from the secret *VANTIQ_A2A_SECRET*. The system will create an empty instance of this secret if it does not already exist and it must be populated with a valid OpenAI API key in order for the agent framework to operate properly.

> The LLM used for request dispatching can be reconfigured if needed. See [Agent Extension Configuration](#agent-extension-configuration) for details.

### Agent Skills

As part of its definition, an Agent must declare one or more "skills".  Each skill represents a unique function or capability that the agent provides. Skills are implemented as procedures, so the IDE provides a way to indicate which of an Agent's public procedures should be treated as skills:

![Agent Skill](./assets/img/agents/AgentSkill.png)

Skills are invoked by the agent framework in response to the requests the Agent receives. Typically this involves matching input from the user to the skill or skills that can perform the request action. This is something LLMs are very good at, when they have access to the appropriate context. 

Here that context consists of the description of the skill's associated procedure and its parameters.  Therefore, it is very important to provide as complete a description as possible, both of the procedure and its parameters. Testing request dispatching and adjusting these descriptions to improve accuracy is an important part of building an Agent.

For example, the Trip Planner's `FlightAgent` declares its `searchFlights` skill as follows:

```
// Search for available flights based on the given criteria
package com.vantiq.trip.agents
stateless PROCEDURE FlightAgent.searchFlights(
    originAirport String Required Description "The IATA 3-letter code for the originating airport."
    ,destinationAirport String Required Description "The IATA 3-letter code for the destination airport."
    ,startTime String Description "The earliest date and time for the flight in ISO8601 format."
    ,endTime String Description "The latest date and time for the flight in ISO8601 format."
    ,airline String Description "The name of the airline."
    ,seatClassification String Description "The type of seat desired, e.g. 'First-Class', 'Economy Plus'"
): Object Array
```

The top-level comment becomes the procedure's description -- this is what the dispatching LLM consults to decide whether `searchFlights` is the right skill for an incoming request. Each parameter's `Description "..."` clause is surfaced as parameter-level context so the dispatcher can populate it correctly when invoking the skill.

### Discovering and Describing Agents

Explicitly declaring agents means that it is possible to query the system's metadata and determine what agents are available.  The following query selects the names of all agents:

```
var agentNames = SELECT name FROM system.services WHERE isAgent == true
```

Agents also support the notion of "tags" which can be used to form groups of related agents which can be determined dynamically.  For example, this query will find all agents tagged as "travel":

```
var qual = {
	isAgent: true,
	"ars_properties.tags": "travel"
}
var travelAgents = SELECT name FROM system.services WHERE qual
```

Once the appropriate agents are selected, you may need to determine exactly what the agent can do. To that end, all agents automatically provide an [Agent Card](https://a2a-protocol.org/latest/specification/#5-agent-discovery-the-agent-card) which provides a standard description of their functionality. An agent's "card" can be obtained either via the REST endpoint `/api/v1/resources/services/<agentName>/_agentCard` or by invoking the built-in procedure [*io.vantiq.ai.A2A.getAgentCard*](rules.md#a2a).

For example, the Trip Planner wraps the tag-based query shown above in a helper `TripPlanner.selectAgents()` which extracts just the names. It then fetches each agent's card and assembles a `{name, desc}` list which a [text template](rules.md#template) renders into a string suitable for embedding in the planning prompt:

```
var agentNames = TripPlanner.selectAgents()
var agentsWithDesc = []
for (name in agentNames) {
    var card = io.vantiq.ai.A2A.getAgentCard(name)
    agentsWithDesc.add({name: name, desc: card.description})
}

var template = "@repeat(agents)* ${name}[input] - ${desc}
@endrepeat"
var availableAgents = io.vantiq.text.Template.format(template, {agents: agentsWithDesc})
```

This is another instance where we are leaning heavily on the descriptions provided (here of each agent's overall capabilities) in order to perform accurate matching.

## Agent State Management

Agents are implemented as [stateful Vantiq Services](servicestatemgmt.md#stateful-services). All agents are automatically declared as managing [collaborations](servicestatemgmt.md#collaborations) which means that they have [partitioned state](servicestatemgmt.md#partitioned-state). This is used to manage both per-Agent state (including local LLM state via [conversations](#conversations)) and broader [discussion state](#discussions) which can span multiple requests and capture interactions in a multi-agent system (MAS). Agents also have more specialized state management requirements, which are explored in the sections below.

### Tasks

Agents use [tasks](https://agent2agent.info/docs/concepts/task/) to keep track of user requests as they are processed. Each task represents a single user request which concludes either with the production of one or more [artifacts](https://agent2agent.info/docs/concepts/artifact/) or a failure. Tasks record both the current processing state and maintain a history of all messages sent during their processing (indicated by the task id stored in each message).

For example, an agent skill can retrieve the currently active task using [`io.vantiq.ai.Agent.getCurrentTask`](rules.md#agent) to access its `contextId` (e.g. to propagate to a downstream A2A call) or to inspect the message history:

```
var task = io.vantiq.ai.Agent.getCurrentTask()
log.info("Processing task {} (context {}) with {} prior messages",
    [task.id, task.contextId, task.history.size()])
```

Task state is stored in-memory and is discarded upon task completion. It will also be lost if an agent is terminated or restarted for any reason. The agent framework also exposes the following [A2A](https://a2a-protocol.org/latest/specification) operations on each agent's service interface, intended for external callers (other agents, REST clients, administrative tooling) inspecting the agent's in-flight work:

* `tasks/get(taskId String): io.vantiq.a2a.Task` -- return the task with the given id.
* `tasks/list(): io.vantiq.a2a.Task[]` -- return a list of all currently active tasks.

### Discussions

In most applications, achieving the user's ultimate objective is not simply a matter of sending one request to an agent and waiting for it to be done. More often it involves multiple requests over some period of time to reach the final goal. Keeping track of these requests and their outcomes, visualizing them to the user so they can see what they've done and decide what they might do next, allowing agents to access this data so they can use it to inform later actions, these are all core capabilities of most agentic applications. Rather than require developers to repeatedly "roll their own" solution we have introduced the concept of "discussions".

Discussions record the results of a sequence of tasks related to a larger, overall goal (as determined by the application). This is done automatically by the agent framework, once the application has declared that it wishes to enable the feature. This provides a persistent record of all client to agent interactions which can be accessed for a variety of purposes:

* On the client side, the discussion messages can be used to reconstruct the complete exchange between the user and the agent (note that this differs from a [conversation](#conversations) since it is unbound from any specific LLM interaction).
* Agents can use task history to extract context they might use as they process any active user requests.
* Discussions can be used to audit actions taken by both the user and the agent.

Discussions are implemented as an [A2A extension](https://a2a-protocol.org/latest/topics/extensions/) which requires opt-in by both the agent and any client (this includes both user facing applications and other agents). All Vantiq agents have the discussion extension enabled by default. If you want to disable this for any agent, you must uncheck the "Discussion Creation" checkbox in the IDE:

![Discussion Creation](./assets/img/agents/DiscussionCreation.png)

> You can also disable this directly using the agent's [extension configuration](#agent-extension-configuration).

Discussions leverage the agent's collaboration management facilities to manage persistence. As a result, each discussion instance is "owned" by a specific agent, which is solely responsible for state recording and lifecycle management. When communicating with an agent, there are two message properties that directly influence what the framework does (see the [io.vantiq.a2a.Message](rules.md#message) type for more details):

* **extensions** -- in order to enable the use of discussions, the client must include the extension URI `https://vantiq.com/agents/discussion`.
* **contextId** -- if no value is provided and discussions are enabled, then the framework will create a new discussion containing the resulting task. If a value is provided and discussions are enabled (by both the client and agent), the value is treated as a discussion id. The referenced discussion must exist, be active, and be owned by the agent receiving the message.

For Vantiq clients, the easiest way to use discussions is through the [Discussion Widget](cbref.md#discussion). This will automatically set the necessary extension in the messages it sends and also make sure to send the appropriate context on each message. Clients invoking an agent directly (using the JavaScript procedures) will need to include the information outlined above in the messages that they send (assuming they want discussions).

#### Discussion Management API

When an Agent supports discussion creation, the following discussion management procedures will be automatically generated:

* `discussionsDelete(discussionId String REQUIRED): Boolean` -- Deletes the specified discussion (as long as it is owned by this agent). Returns `true` if the discussion was deleted and `false` otherwise.
* `discussionsGetById(discussionId String REQUIRED, required Boolean, options Object): ArsDiscussion` -- Return the specified discussion instance. The discussion must be owned by the current agent. If `required` is `true` (the default), then an exception is raised if the discussion cannot be found. The properties of the `options` parameter influence the returned discussion properties as follows:
    * **includeMessages** (Boolean) -- when set to `true` (the default), the discussion returned will include the recorded messages.
    * **includeArtifacts** (Boolean) -- when set to `true` (the default), the discussion returned will include the recorded artifacts.
    * **includeSystemProperties** -- when set to `true` (the default is `false`), the discussion returned will include the system properties.
* `discussionsList(): ArsDiscussion Array` -- Return all active discussions owned by this agent.
* `discussionsUpdateStatus(discussionId String REQUIRED, status String REQUIRED): ArsDiscussion` -- Closes the specified discussion and updates its status to either `completed` or `failed`.

These procedures are public and can be used by both the agent and its clients to interact with the discussions owned by the agent.

#### Multi-Agent Discussions

Although each discussion is owned by a single agent (typically the initial agent contact by the client), it is still possible for downstream agents to leverage the discussion for their own state management. These agents are said to be "participants" in the discussion. Agent to agent communication propagates the current task's `contextId` (if any), but does not automatically propagate the extension. The intent is to communicate the id of the current discussion to the participating agents without asking them to create their own discussion. If an agent needs to manage state for the discussion, the recommended approach is to establish a collaboration and associate it with the discussion. The best way to do this depends on whether or not the agent is managing its own persistent entities.  If it is, then the discussion id can be used as a foreign key to find the entity and then the entity's id can be used to establish the collaboration instance (likely using the generated [entity role procedures](servicestatemgmt.md#entity-role-procedures)). Otherwise, the agent can establish a collaboration using the discussion id as the collaboration id. This provides a direct mapping from the overall discussion to the agent's local state. The Trip Planner's FlightAgent demonstrates the use of this technique.

Of course, it is also possible for agents to initiate their own discussions by altering the information that is propagated on downstream messages. See the [`io.vantiq.ai.Agent`](rules.md#agent) service procedures for details on how to accomplish this.

### Domain Specific State

Agents often need to manage application/domain specific state (aka "entity") as part of their operation. For example, a trip planning agent may need to manage instances of a "Trip" resource. Since agents are services, this can be done using the standard service [state management](servicestatemgmt.md) features. One common approach is to leverage the [entity role procedures](servicestatemgmt.md#entity-role-procedures) to bind the resource instances to a collaboration (and optionally a [persistent conversation](#persistent-conversations)). 

Alternatively, [discussions](#discussions) offer another, more agent-centric, approach to managing this state. The Trip Planner's `TripPlanner.processRequest` binds its `Trip` resource to the current discussion via collaboration management -- see the contribution for the full pattern.

### Conversations

LLM interactions are stateless.  This means that for every request, the LLM only has access to its own "knowledge" and the information in the current request.  If you want the LLM to know about previous requests and its responses to them, this information must be presented as part of the current request.  Doing this is the role of a *conversation*.  

> The word "conversation" gets used in a variety of contexts when talking about GenAI applications.  This isn't surprising given that LLMs appear to "converse" with users and it is a convenient word to describe many application behaviors.  However, in the Vantiq platform the term has a very specific meaning and anytime you see it in relation to Vantiq Agents and GenAI Applications, this is what we mean.

A conversation consists of an ordered sequence of [*chat messages*](rules.md#chatmessage) which capture the history of an interaction between an Agent and an LLM.  The messages in a conversation have a *type* and associated *content*.  A message's type tells the LLM how to interpret the content and must be one of the following:

* **system** -- Instructions to the LLM about how to interpret the conversation or "behave" in general.  Typically there is only a single system message which is added automatically by the application.  Vantiq supports including a system message as part of an [LLM](resourceguide.md#llms) definition to ensure that it is always present.
* **human** -- Content provided by the user/client.
* **ai** -- Content generated by the LLM in response to a request.  Maybe a direct response or instructions for some further action (e.g. the invocation of an LLM "tool").
* **tool** -- Content produced by the execution of an LLM tool.

The structure of a message's content depends on its type.  See [ChatMessage](rules.md#chatmessage) for more details.

#### Transient Conversations

Conversations are managed using the [Conversation Memory](rules.md#conversationmemory) service which supports creation and manipulation of conversations.  The conversations managed by this service can be referenced when sending an LLM request via the built-in [submitPrompt](rules.md#llm) and [answerQuestion](rules.md#semanticsearch) procedures or when invoking a [GenAI procedure](services.md#genai-procedures).  Doing so causes the conversation to be automatically updated based on the underlying LLM interactions.

As its name implies, the resulting conversation state is stored in memory.  This means that it has a limited lifetime and can be subject to loss in certain failure cases.  We refer to these as "transient" conversations.  Transient conversations are suitable for interactions that will last minutes to maybe an hour or so and which do not need to be saved for any reason (such as auditing).

For example, an agent may need to "iterate" on a request in order to arrive at the appropriate result. This involves multiple LLM invocations (aka "turns") where information from previous turns is needed to direct the current one (perhaps to avoid making the same mistake repeatedly). This state can be stored in a conversation, which can be safely discarded, once the final result is reached. Since this all occurs while processing a single request, there is no need for long term storage of the conversation.

#### Persistent Conversations

For cases where a conversation must be available over much longer time frames (days or even weeks) or when it needs to be recorded for some reason, conversations can be persisted as part of a [collaboration](servicestatemgmt.md#collaborations) managed by the Agent.  This can be accomplished in a variety of ways.  Using the [SubmitPrompt](apps.md#submit-prompt), [AnswerQuestion](apps.md#answer-question), or [GenAIFlow](apps.md#genai-flow) activity patterns in a [visual event handler](apps.md) will automatically bind a conversation to the current collaboration instance (or create one as needed).  The Agent may also choose to manage its collaborations more explicitly.  If the conversation is associated with some application "entity", then the [entity role procedures](servicestatemgmt.md#entity-role-procedures) are a natural fit.  Alternatively, the Agent can directly manage one or more persistent conversations using the [collaboration management procedures](servicestatemgmt.md#procedures).

In either case, once bound to a collaboration instance, persistent conversations are automatically saved along with their associated collaboration instance and loaded into memory when the collaboration instance is retrieved. Once loaded, they can be accessed through the [Conversation Memory](rules.md#conversationmemory) service as described above.  This is all done using standard [partitioned state](servicestatemgmt.md#partitioned-state) and fully supports [service replication](servicestatemgmt.md#service-replication) for stricter reliability guarantees.

## Communicating with Agents

### Agent Messages

The standard way to send a request to an agent is by sending it a [message](rules.md#message) to be processed. Messages are processed by the generated agent framework and provide a standard way of interacting with any agent. This is what allows agents to be invoked during [plan execution](#planning-agents) without having to worry about the details of how the requests will be processed. It also supports an architecture where [discovered](#discovering-and-describing-agents) agents can be used without prior knowledge of their API. Messages are sent using the following [A2A](https://a2a-protocol.org/latest/specification) operations (the caller chooses which one to use based on how it wants to process the result(s)):

* `message/send` -- each message sent to the agent results in exactly one response, which will be an instance of a [Task](rules.md#task) representing the current state of the request processing.
* `message/stream` -- each message results in a sequence of responses (minimum of 2) which communicate the incremental state of the request as it is processed.

Either of these can be used to send messages to an agent either from a [Vantiq Client](cbuser.md) or from another VAIL Service.

#### Sending from Vantiq Clients

Clients send messages to an agent using one of two JavaScript functions:

* `client.a2aMessageSend(agentName:string,msg:A2AMessage,options:any=null):Promise`

For example:

```typescript
let userMsg = "What is the capital of California?";
let options = null;

let message = new A2AMessage();
message.parts.push(new A2ATextPart(userMsg));

console.log("Message=" + userMsg);

client.a2aMessageSend("io.vantiq.via.RoutingAgent",message,options).then(
    function(response)
    {
        console.log("RESPONSE:" + JSON.stringify(response,null,3));
    },
    function(error)
    {
        console.error("ERROR:" + JSON.stringify(error,null,3));
    }
);
```

* `client.a2aMessageStream(agentName:string,msg:A2AMessage,options:any=null,inProgressCallback:Function=null):Promise`

For example:

```typescript
let userMsg = "What is the capital of California?";
let options = null;

let message = new A2AMessage();
message.parts.push(new A2ATextPart(userMsg));

console.log("Message=" + userMsg);

client.a2aMessageStream("io.vantiq.via.RoutingAgent",message,options,function(progress)
{
    console.log("PROGRESS:" + JSON.stringify(progress,null,3));
}).then(
    function(response)
    {
        console.log("RESPONSE:" + JSON.stringify(response,null,3));
    },
    function(error)
    {
        console.error("ERROR:" + JSON.stringify(error,null,3));
    }
);
```

Using these functions allows the client to precisely control how messages are sent and how the subsequent responses are processed and displayed.

One common pattern is for a client to interact with an agent as part of a [discussion](#discussions). While this can be done using the above methods, Vantiq also provides a [Discussion Widget](cbref.md#discussion) to simplify this process. The widget encapsulates the sending of messages (using `message/stream`), processing and displaying the results, and managing agent discussions all in a single UI element. The widget's configuration options let you select the agent you will be communicating with, as well as pre and post-processing options.

#### Sending from VAIL

VAIL also offers built-in procedures which can be used to send messages to an agent which are defined as follows (full details can be found in the [A2A Service](rules.md#a2a)):

* `io.vantiq.ai.A2A.messageSend(agentName String Required, message io.vantiq.a2a.Message Required, options Object): io.vantiq.a2a.Task`

For example:

```
var userMsg = "What is the capital of California?"

var message = {
    role: "user",
    messageId: uuid(),
    parts: [
        {kind: "text", text: userMsg}
    ]
}

var task = io.vantiq.ai.A2A.messageSend("io.vantiq.via.RoutingAgent", message)
if (task.getStateValue() == "completed") {
    log.info("RESPONSE: {}", [task.status.message.value])
} else {
    log.error("Request did not complete: {}", [task])
}
```

* `io.vantiq.ai.A2A.messageStream(agentName String Required, message io.vantiq.a2a.Message Required, options Object): Sequence`

For example:

```
var userMsg = "What is the capital of California?"
var message = io.vantiq.a2a.Message.forValue(userMsg)

var eventStream = io.vantiq.ai.A2A.messageStream("io.vantiq.via.RoutingAgent", message)
for (event in eventStream) {
    if (event.kind == "artifact-update" && event.lastChunk) {
        log.info("ARTIFACT: {}", [event.artifact.value])
    } else if (event.kind == "status-update") {
        if (event.isFinal) {
            log.info("FINAL: {}", [event.status.message.value])
        } else {
            log.info("PROGRESS: {}", [event.status])
        }
    }
}
```

The shortcut `io.vantiq.a2a.Message.forValue(...)` shown above produces an equivalent message to the explicit form used in the `messageSend` example, and can be used in either procedure.

These procedures can be used from any Vantiq service (whether or not it is an Agent). As with the client side procedures, they provide precise control over the sending of messages and processing of the subsequent results.

One common scenario in which one agent will call another is as part of a [planning algorithm](#planning-agents). In this case, the execution of the plan may result in messages being sent to an agent that has been made available to the planner. Whether this is done using `message/send` or `message/stream` depends on how the plan itself is being executed.  See the [Agent](rules.md#agent) built-in service for more details. Note that plan execution can only be done by an Agent, not a vanilla Vantiq service.

## Agent to Human Interaction

The use of an LLM can make Agents very powerful, allowing them to make decisions much more dynamically instead of relying solely on predetermined pathways.  To help mitigate against the Agent doing something not just unexpected, but inappropriate, it can be necessary to keep the "human in the loop", requiring that it obtain permission prior to acting.  This requires that the Agent be able to initiate an interaction with the user.  This mechanism can also be used for other purposes, such as allowing the Agent to gather additional information it might need to complete its task. In a multi-agent system (MAS) it must be possible for "downstream" agents (those which were not directly called by the client) to perform these actions.

In addition to providing a common entry point through which all agents receive requests, the generated agent framework also includes a standard way of requesting input from the user using the built-in procedure [io.vantiq.ai.Agent.requestUserInput](rules.md#agent).  This procedure can be called at any point and will instruct the framework to contact the caller to obtain the requested information. This works through multiple invocations to ensure that the request ends up with the original requester.  For example, suppose a client sends a request to an agent and that agent sends a request to a second agent (one that is unknown to the client).  If this second agent wants to obtain user input, we want that request to be forwarded back to the client. Using `io.vantiq.ai.Agent.requestUserInput` triggers exactly this behavior.

For example, the [Trip Planner contribution](#trip-planner-contribution)'s `CarRentalAgent` uses this to ask the user what kind of car they want before returning results. Because the car rental agent is invoked downstream of the Trip Planner (which is the agent the client originally called), the request is automatically forwarded back to that client:

```
// Search for available rental cars
package com.vantiq.trip.agents
stateless PROCEDURE CarRentalAgent.searchCars(
    rentalAirport String Required Description "The IATA 3-letter code for the airport at which we will be renting the car."
)

var answer = io.vantiq.ai.Agent.requestUserInput("What kind of car do you want?")
log.info("User input: {}", [answer])

// ... use answer to filter rental cars ...
```

The call blocks until the user responds, and the response is returned as the procedure's result. The forwarding flow is shown below:

![Agent Request Input](./assets/img/agents/A2AUserInputRequest.png)

## Planning Agents

One popular agent architecture is known as "plan and execute".  The idea is that you start by asking the LLM to formulate a step-wise plan to address a given request.  The LLM is typically given a collection of "tools" which it can use when building its plan (note that these are distinct from [LLM Tools](genaibuilder.md#tool)).  Once the plan is created, it is executed, step by step.  This may or may not involve calling the LLM.  Once the plan has been executed, the results are analyzed and a result is provided.  Some algorithms introduce the notion of "re-planning" which may cause the agent to repeat the execution phase on a new set of tasks (until a final state is reached). Some common algorithms are:

* [Plan and Execute](https://blog.langchain.com/planning-agents/#plan-and-execute) -- this is the most basic form which constructs a linear sequence of tasks and uses re-planning to refine the results.  It performs re-planning after each step, so it can be quite expensive in terms of the number of LLM interactions. This approach does not enumerate the available tools to the planner, relying instead on native LLM capabilities augmented with standard LLM tool calling (which is implicit and therefore unknown to the planner).
* [Reasoning Without Observations](https://blog.langchain.com/planning-agents/#reasoning-without-observations) (ReWOO) -- attempts to improve on the basic plan-execute approach in order to reduce the number of LLM calls required. It explicitly enumerates the available tools so the planner can decide when to leverage them and it uses "variables" to pass information from one step to another. The individual tools may or may not use an LLM to do their work and can often use a smaller, cheaper LLM than the one used to construct the plan. The resulting plan can be represented as a directed, acyclic graph. Plan execution occurs once, with no re-planning.
* [LLMCompiler](https://blog.langchain.com/planning-agents/#llmcompiler) -- similar to ReWOO in that information can flow from one task to another.  Tasks are "streamed" and executed as they are produced (assuming all dependencies are available).  Incorporates continuous re-planning in order to continue task generation until final result is reached.

Each of these uses different prompts to build the plan and process task results, but what they all have in common is the need to execute a sequence of tasks and report their results.  We refer to this as "plan execution" and we have provided the built-in procedures [io.vantiq.ai.Agent.executePlan](rules.md#agent) and [io.vantiq.ai.Agent.executePlanAsSequence](rules.md#agent) to manage this process. 

> Since the "Plan and Execute" algorithm executes its tasks one at a time, it actually doesn't need to use the plan execution facility.  We've included it in this section for completeness (since it is a well-known architecture for planning agents).

The primary input to these procedures is a DAG where each node represents a task to perform and the edges represent the flow of information from one task to another. The result is an `Object` whose `evidence` property carries one entry per node (with that node's computed value) and -- when a user request is provided -- whose `response` property carries the user-facing answer assembled by the algorithm's solver step. See [io.vantiq.ai.Agent.executePlan](rules.md#agent) for the full schema.

For example, once `availableAgents` has been [built up from the discovered agents](#discovering-and-describing-agents), the Trip Planner constructs and executes a plan:

```
// Construct the plan via the planner's GenAI procedure
var planInput = {task: userRequest, availableAgents: availableAgents}
var plan = TripPlanner.planTripRequest(planInput, {})

// Execute the plan and return the user-facing response
var result = io.vantiq.ai.Agent.executePlan(plan, userRequest)
return result.response
```

The plan itself is built by `TripPlanner.planTripRequest`, a [GenAI procedure](services.md#genai-procedures) whose prompt encodes the planning algorithm (ReWOO, here) -- the choice of algorithm lives in the prompt rather than in the execution call.

The streaming variant, `executePlanAsSequence`, returns the plan's progress as a [Sequence](rules.md#sequences) of events. This lets the calling agent forward downstream status updates back to its own client as they happen, instead of waiting for the whole plan to finish:

```
var curTask = io.vantiq.ai.Agent.getCurrentTask()

var planStream = io.vantiq.ai.Agent.executePlanAsSequence(plan, userRequest)
var lastItem
for (item in planStream) {
    lastItem = item

    // Forward intermediate status updates from downstream agents, re-tagging the
    // message to our own task id so the client sees a single coherent stream.
    if (item.kind == "status-update" && !item.isFinal) {
        var src = item.status.message
        var fwd = io.vantiq.a2a.Message.build(parts: src.parts,
            taskId: curTask.id, contextId: src.contextId, role: src.role,
            metadata: src.metadata, extensions: src.extensions,
            referenceTaskIds: src.referenceTaskIds)
        io.vantiq.ai.Agent.sendTaskStatusUpdate(fwd)
    }
}

// The final item is the same Object executePlan returns.
if (lastItem.evidence) {
    for (r in lastItem.evidence) {
        // ...consume per-node results from lastItem.evidence[r.key]...
    }
}
```

Intermediate items use the same event shapes as [`messageStream`](#sending-from-vail). The forwarding loop re-tags each downstream status update with the current agent's task id (`curTask.id`) before re-emitting it via `sendTaskStatusUpdate`, so the original client sees one stream of updates against the task it originally created. See [io.vantiq.ai.Agent.executePlanAsSequence](rules.md#agent) for the supported event types.

## Advanced Topics

### Agent Extension Configuration

The behavior and implementation of the agent's framework can be altered through the use of advanced configuration options. Typically it is not necessary to use these, but they are available should the need arise. The structure of the configuration is a two-level JSON Object where the outer properties are extension URIs and the sub-properties are the available configuration options relating to that extension. The supported values are:

* `https://vantiq.com/agents/discussion` -- configures discussion processing.
    * **creationDisabled** (Boolean) -- if set to `true` then the agent will not perform discussion processing.  The default value is `false`.
* `https://vantiq.com/agents/requestDispatch` -- configures the agent's request dispatch processing.
    * **algorithm** (String) -- specifies the dispatching algorithm to be used. Legal values are:
        * `planning` (default) -- use a planning algorithm to process requests using the available skills.
        * `tools` -- use LLM tool calling to map the request to the available skill procedures.
    * **llm** (String) -- the name of the Vantiq LLM to use for request dispatching.
    * **prompts** (Object) -- specifies the prompts to use at various points (varies based on the dispatching algorithm). The legal values are:
        * **planner** -- the prompt used to construct the dispatch plan. Must be the name of a Vantiq document instance. Only used by the `planning` dispatch algorithm.
        * **solver** -- the prompt used to construct the final "solution" to the dispatch plan. Only used by the `planning` dispatch algorithm.
        * **formatting** -- the prompt used when formatting a request to the user for additional input.
        * **skill** -- the prompt used when performing an LLM tool call to one or more skill procedures.

### Legacy Applications

> Only relevant when considering how to maintain pre 1.44 Vantiq applications.

While we strongly encourage using A2A operations when [communicating with agents](#communicating-with-agents), it is still possible to treat an agent as a standard Vantiq [service](services.md). When processing requests received through the Agent's service interface (either via a procedure invocation or processing an inbound event), the Agent no longer has access to the facilities provided by the agent framework. This includes [tasks](#tasks), [discussions](#discussions), and the automatic forwarding of [user input requests](#agent-to-human-interaction). However, the agent can send downstream requests using [A2A messages](#agent-messages) and can make use of a user request bridge procedure to help it communicate with legacy clients. 

#### User Request Bridge Procedure

The user request bridge procedure (hereafter simply "the bridge") should be implemented by any agent which will be receiving requests through its service interface and wants to support use of the built-in procedure `io.vantiq.ai.Agent.requestUserInput`.  The bridge has the following definition:

```
PRIVATE STATELESS PROCEDURE <AgentService>.a2a_requestUserInput(userRequest Any, requestContext Any): Any 
```

The parameters are:

* **userRequest** -- the value provided to the invocation of `io.vantiq.ai.Agent.requestUserInput`.  It describes what is being requested from the user.
* **requestContext** -- the value provided to the invocation of `io.vantiq.ai.Agent.requestUserInput`. This is an opaque value that the agent should use to establish the proper communication context.

The return value of the procedure will be returned to the caller of `io.vantiq.ai.Agent.requestUserInput`.  The procedure's implementation should leverage the techniques described in the next sections.

##### Direct Communication

The direct communication model requires that the agent and the user be actively engaged in a conversation via the [Conversation Widget](cbref.md#conversation).  Whenever the conversation widget loads a conversation (either directly or via an enclosing collaboration instance), it will register a "callback" with the [Callback service](rules.md#callback).  The id of the current conversation is used as the *callbackId*.  This allows the Agent to contact the user using the `io.vantiq.Callback.invoke` procedure like this:

```
var userPrompt = "I'm about to withdraw money from your account, is that OK?"
var userResponse = io.vantiq.Callback.invoke(conversationId, userPrompt, 5 minutes)
... do something with the response ...
```

The data sent will be displayed to the user in the conversation widget and then the user's response will be returned as the result of the invocation (unless the user takes longer than *5 minutes* to respond).  The advantage of this approach is that the Agent's communication will appear to the user where they are likely already engaged.  This avoids the need to pop up additional UI elements or distract them from the current task.  The disadvantage is that it won't work if the user isn't actively using a client with a conversation widget.

##### Notification

If the user cannot be reached directly, then the Agent must instead use a notification based approach to contact them.  The [Notify](apps.md#notify) activity pattern already provides robust support for sending a notification to one or more users and then managing their responses.  The primary limitation is that it works in the context of a [visual event handler](apps.md), which typically operate asynchronously and do not provide a means to produce a result.  Rather than invent an alternate notification mechanism, we instead chose to address this limitation.

To do this we added the ability to "invoke" a service event handler.  The VAIL [`PUBLISH`](rules.md#event-sending) statement can obviously be used to trigger a handler, but it assumes a fully asynchronous execution model, so it cannot "wait" for a reply.  Therefore, we have added the `Event.request` procedure to the built-in [event processing](rules.md#event-processing) service.  This procedure triggers the handler for a specified [service event](services.md#event-types).  It must be called from a [service procedure](rules.md#service-procedures) belonging to the same service as the target event type.  The behavior of the handler is unrestricted, but it is assumed that at some point it will provide a response using the [Reply](apps.md#reply) activity pattern. The net result is a request/response execution model which uses an event handler as its implementation.

For example, suppose we have the following event handler:

![Notify Handler](assets/img/agents/NotifyHandler.png)

We can "invoke" it from the Agent using code like this:

```
var event = {collaborationId: collaborationId}
var userResponse = Event.request("NotifySessionEVT", event, 5 minutes)
... do something with the response ...
```

When run, the target user will receive the notification and be presented with the associated client.  Once the user provided the requested input, the result from the client would be sent back to the Agent as the return from `Event.request` and processing would continue from that point.  The advantage of this approach is that it allows the agent to contact users on an "interrupt" basis, not just when they are actively in a conversation.  The disadvantage is that the Vantiq Notify pattern is limited to use on a mobile device.  So this approach isn't appropriate for browser only applications.
