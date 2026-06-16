## Welcome to the GenAI Builder Labs!

### To Do These Labs, You Will Need:<br>
1. An OpenAI API Key<br>
2. A Tavily API Key<br> _(More about this in Lab #3)_
_Note: To create a Secret with each API key, go to Administer -> Advanced -> Secrets_<br><br>

### Objectives<br>
1. To gain comfort navigating and using the GenAI Builder<br>
2. To see first-hand how many of the GenAI Components behave<br>
3. To successfully build GenAI procedures in the Vantiq platform<br>
4. To learn how to call GenAI procedures from a Visual Event Handler<br>
<br>
### Disclaimer<br>
This lab is just using celebrity names for entertainment value.  In no way should you take any of the "information" about them as truth!  Most of it, like the "food allergies" and "personal conflicts", is pure fiction.<br>
<br>
### Overview <br>
You are an event planner working out a seating chart for three tables of eight places each.  You don't personally know any of the attendees. Fortunately, a friend of a friend who knows them all and gave you some notes on their:<br>
* Personal conflicts with other attendees<br>
* Friends among the other attendees<br>
* Food allergies <br> 

Your job is to write Generative AI Assistance to help you find appropriate seating for all 24 guests.  You want to work interactively with AI to accomplish this, by building:<br>
* One GenAI Procedure to automatically check for food allergies<br>
* One GenAI Procedure to report if there are any personal conflicts at the table where celebrities migh sit<br>
* One GenAI Procedure to carry out an ongoing conversation with you, looking up more about celebrities on-line to answer your questions, and saving what is found to the Semantic Index, for later look-ups.<br><br>

### Step 0.0: The Lab Infrastructure<br>
The w.p.SeatingChart Client comes ready to interact with the w.p.Seating Service.  The schema types are prepared, too.  But now you'll need to build out the Generative AI event logic on the Service to complete the lab.<br>
<br>
### Step 0.1: Set up the Lab<br>
1. Create a Generative LLM of any name in the w.p Package, of the latest model type ChatGPT <br>
2. Create an Embedding LLM of any name in the w.p Package<br>
3. Create a Semantic Index using your new LLMs<br>
<br>
	a. Name: Attendees
    <br>
    b. Package: w.p<br>
4. Run the _BuildSIEntries_ procedure, supplying _w.p.Attendees_ as the Semantic Index name parameter<br>
5. Open your w.p.Attendees Semantic Index and verify that you have 24 index entries; one for each celebrity<br><br>

------------------------------

## Lab 1: Build a GenAI Procedure to Find and Categorize Allergies<br><br>


### Step 1: Find the Start of the VEH That Will Call the GenAI Procedure<br>

1. Verify that you have the w.p.Seating Service already created, with one Public inbound event, _CheckAllergies_, of type CelebNameType<br><br>
    
### Step 2: Create A GenAI Procedure to Check For Food Allergies<br>

1. In the Implement Tab, click on the "+" next to the Public GenAI Procedures Category
2. Call the procedure _CheckForAllergies_<br>
3. Drag a Resources -> PromptFromTemplate component to Input.  Call it _Question_<br>
   a. promptTemplateType: _Template_<br>
   b. promptTemplate: _Does ${Name} have any known food allergies?_ and Save<br> <br>
4. Drag a Primitives -> CodeBlock component to Input.  Call it _KeepName_<br>
   a. Write the VAIL code:  _return input.Name_ & Save <br>  

_Note: We want this procedure to return 4 pieces of vital information:_ <br>
   -  _The celebrity's name_<br>
   -  _What kind of allergy_<br>
   -  _The specific allergy_<br>
   -  _An extra alert if it's a nut allergy_<br><br>
_Notice that the KeepName task has a thick black outline.  This shows that it's part of the return value._<br><br>
5. Drag a Primitives -> CodeBlock component to Question; call it _ConvertToString_<br>
_Note: RAG components can only take string input, so we will need to convert the prompt_<br>
   a. Write the VAIL code: _return toString(input)_  and Save <br>
6. Drag a AI Patterns -> RAG component to ConvertToString, called _SearchAnswer_<br>
   a. Configure with your LLM and the w.p.Attendees Semantic Index<br><br>
7. Drag another CodeBlock to SearchAnswer, called _StripToAnswer_<br>
_Note: RAG components include all the doc references in their response.  To see what was found, click on the RAG task and open the "View Task Input/Output" pane.  The bottom-most task is the last one run, and if you open it, you'll see what the inputs were, what the task outputted, and the types for both.  Make a habit when developing GenAI Procedures, to check the task events often, for information of what's happening in the procedural flow._<br>
<br>_At this point, we just want the answer field, so we're using this latest CodeBlock to get it._<br>
   a. Write the VAIL code: _return input.answer_  and Save <br>
8. Drag a AI Patterns -> Categorize component to StripToAnswer, called _AllergyType_<br>
   a. Set the LLM to your generative LLM<br>
   b. Set the Categories to "has a nut allergy", "has a non-nut allergy", "has no known allergies"<br><br>
9. Drag a PromptFromTemplate component to SearchAnswer, called _PromptEvaluation_<br>
   a. promptTemplateType: _Template Document_<br>
   b. promptTemplate: Choose "prompts/AllergyEvaluationTemplate.txt" from the drop-down list and Save<br>
   _Note: Go to Show -> Documents to see the prompts/AllergyEvaluationTemplate.txt_ to know what was asked.<br><br>
10. Drag a LLM component to PromptEvaluation and call it _EvaluateAllergy_<br>
   a. llm: your generative LLM<br>
   b. outputType: String<br>
11. Save <br>
![](Lab1/GABLab1PreEval.png)
   <br>
### Step 3: Check the Procedure Functionality (So Far)<br>

1. Click on the "Play" button at the top left of the pane.<br>
   a. Make an Object Input:<br>
   ```
   {
      "Name" : "Dwayne Johnson"
   }
   ```<br>
  b. You should see output like:<br>
   ```
{
   "KeepName": "DwayneJohnson",
   "AllergyType": {
      "category": [
         "has a non-nut allergy"
      ],
      "categoryScores": {
         "has no known allergies": 0,
         "has a nut allergy": 0,
         "has a non-nut allergy": 100
      }
   },
   "EvaluateAllergy": "Milk allergy."
}
```
<br><br>

### Step 4: Finish the CheckForAllergies Procedure<br>
_This is good so far, but we want a separate alert in the case of dangerous nut allergies, so let's add a bit more..._<br>
1. Drag a Branch component to AllergyType, called _AllergyFollowUp_<br>
   a. Change "Case" to "RedAlert" and the expression to:<br>
   ```
   input.category[0] == "has a nut allergy"
   ```
   <br>
   b. Leave Default as is <br>
2. Drag an Assign component to the lower leg of the line under RedAlert, called _AssignNutAlert_<br>
   a. Set the property to _NutAlert_<br>
3. Drag a CodeBlock to the lower leg of the line under NutAlert, called _SetNutAlert_<br>
   a. VAIL code: <br>
   ```
   input.NutAlert = true

   return input
   ``` <br>
4. Save the procedure<br>
![](Lab/GABLab1CompleteGAP.png)<br>

### Step 5: Check the Finished Procedure<br>
1. Click the "Play" button, and change the name in the input object to "Lindsay Lohan"<br>
2. Verify that you see output like:<br>
```
{
   "KeepName": "Lindsay Lohan",
   "AllergyFollowUp": {
      "category": [
         "has a nut allergy"
      ],
      "categoryScores": {
         "has a nut allergy": 100,
         "has a non-nut allergy": 0,
         "has no known allergies": 0
      },
      "NutAlert": {
         "category": [
            "has a nut allergy"
         ],
         "categoryScores": {
            "has a nut allergy": 100,
            "has a non-nut allergy": 0,
            "has no known allergies": 0
         },
         "NutAlert": true
      }
   },
   "EvaluateAllergy": "Peanuts"
}
``` 
<br><br>
   
### Step 6: Connect CheckForAllergies Procedure to the Visual Event Handler and Client<br>
1. In the Implement tab, click the CheckAllergies inbound Event to open the Visual Event Handler<br>
2. From the Service Procedures category, drag CheckForAllergies to the CheckAllergies EventStream, and click on the Configuration "Click to Edit" blue lettering.<br>
   a. Set the procedure to: _w.p.Seating.CheckForAllergies_<br>
   a. Set the parameter: input to: _{ Name : event.Name}_ and Save<br>
4. From the Modifier category, drag a Transformation, called _FormatResponse_ to CheckForAllergies<br>

| **Outbound Property** | **Transformation Expression** | <br>
|-----------------------|-------------------------------|
| Allergies             | event.EvaluateAllergy               | <br>
| Category              | event.AllergyFollowUp.category[0]   | <br>
| Name                  | event.KeepName                      | <br>
| NutAlert              | event.AllergyFollowUp.NutAlert ? true : false       


<br>
5. From the Actions category, drag a PublishToService pattern to FormatResponse<br>
   Choose the w.p.Seating/AllergyReport outbound event from the dropdowns and Save<br>
6. From the Actions category, drag a LogStream to FormatResponse (for verifying the VEH function) and Save<br>
7. Verify that this VEH is performing correctly by clicking on CheckAllergies and using the Trigger Event feature to send an event like:<br>
```
{

    "Name": "Taylor Swift"
   
}
```
<br>
You will see Log Message output like: (Make sure you've toggled on Log Messages in the bottom IDE panel to see it.)<br>
```
Level: INFO
Message: Published Logging Event: {Allergies=Shellfish allergy., Category=has a non-nut allergy, Name=Taylor Swift, NutAlert=false} produced by task: FormatResponse in app w.p.Seating.CheckAllergies
```
<br><br>

### Step 7: Run the GenAI Procedure from the Client<br>
1. In the w.p.SeatingChart Client, click the "Play" button at the top right of the frame.<br>
2. Click on a "OPEN" seat anywhere on the chart, and select a name from the "Attendees" drop-down.<br>
3. A row should appear in the data table, reporting allergy information for the selected celebrity.<br>

![](docs/Lab1/GABLab1Client.png)<br>

*Note:  The Client came pre-built with code to send a name to the the w.p.Seating.CheckForAllergies VEH, upon change of the Attendees drop-down.  There is also a pre-configured Datastream called _AllergyStream_ which feeds the published result from the VEH, to which the data table data binds, resulting in the display.* <br>
<br>
### Conclusion<br>
**Congratulations!** You have successfully created a GenAI Procedure in the GenAI Builder.  By now, you should:<br>
- Feel comfortable in the GenAI Builder space<br>
- Know how to use some of the components, having experienced them first-hand<br>
- Have a good sense of how to use GenAI procedures called from a VEH Procedure Activity Task<br>

##### _Did you get stuck?_ <br>
_In the Lab landing page, click on the "W" in Welcome to download a full solution to this lab, including the w.p.Seating.CheckForAllergies GenAI procedure._<br><br>

---------------------------------------------------
<br><br>
## Lab2: Create a GenAI Procedure to Check for Seating Conflicts<br>
_Celebrity feuds have been around as long as there have been celebrities!  You need to make sure you don't accidentally seat two people together who will not get along.  This time, instead of using a RAG component, we'll extract relevant text from the raw Semantic Index findings._<br><br>

### Step 1: Create the Procedure<br>
1. In the w.p.Seating Service, create a new GenAI procedure called _CheckTable_.<br>
2. From the Resources category, drag a PromptFromTemplate component onto Input.  <br>
3. In the configuration, choose a Template Document called _prompts/WholeTableCheckPrompt.txt_ and click OK<br>
4. Drag a CodeBlock to the PromptFromTemplate task.  Change its name to _StringPrompt_<br>
   VAIL Code: _return toString(input)_<br>
_Note:  Just like RAG, SemanticIndex prompts can't be in ChatPrompt format, which is what the PromptFromTemplate task returns, so we're converting it into a String._<br>
5. Drag a SemanticIndex to _StringPrompt_<br>
   Semantic Index: choose _w.p.Attendees_ from the drop-down and click OK<br>
6. Drag a Primitives -> Transform component to both the SemanticIndex and PromptString tasks and call it _SetupRelevanceStructure_.  Configure with a visual transformation:<br>

| **Outbound Property** | **Transformation Expression** | <br>
|-----------------------|-------------------------------|
| query            | input.PromptString               | <br>
| documents              | input.SemanticIndex   | <br>

7. Drag a Document Compressors -> ExtractRelevantContent component to SetUpRelevanceStructure, and configure with your LLM <br>
8. Finally, we'll drag in a CodeBlock to ExtractRelevantContent to convert everything to a String.<br>
  VAIL Code: _return toString(input)_<br><br>
  
![](docs/Lab2/GABLab2CheckTable.png)<br><br>
  
### Step 2: Try the Procedure from the Client <br>
1. Run the Client, and fill up all of the OPEN seating spots of any of the tables with Celebrity names.<br>
2. In the w.p.SeatingChart Client, at the bottom of each table diagram, is a green button labeled "Check Table for Conflicts".  Click it.<br>
_Note:  There is already code in the OnClick handler for the button to directly call the w.p.Seating.CheckTable procedure, sending the names of all 8 of the celebrities seated there.  If there's a conflict, you will first see an Alert for the first one found, at the top of the dashboard, and the same information will appear under the datatable, in a small box._<br>

![](docs/Lab2/GABLab2Conflict.png)<br><br>

### Conclusion<br>
**Congratulations!** You have successfully created a GenAI Procedure and called it directly from the Client<br>
- Feel comfortable converting Component output to String types, as needed <br>
- Know how to use even more of the GenAI Builder components, having experienced them first-hand<br>
- Have a good sense of how to use GenAI procedures directly, or called from a VEH Procedure Activity Task<br>

##### _Did you get stuck?_ <br>
_In the Lab landing page, click on the "W" in Welcome to download a full solution to this lab._<br><br>

---------------------------------------------
<br><br>

## Lab 3: Create a GenAI Procedure to Answer Questions, and Save the Responses<br>
**Note:**  This procedure will not use a managed AI conversation, because you'll do that part in the next lab.

### To Do This Lab, You Will Need:
1. An API Key from [Tavily](https://www.tavily.com/), to use their on-line MCP Server, to do web searches<br>
2. A secret called _w.p.TavilyKey_ holding the value of your API key.  Go to Administer -> Secrets to do this. <br><br>

### Step 1: Use a Tool to Look Up Information in the Internet<br>
1. Create a new GenAI procedure called _CelebNews_<br>
2. Drag a Resources -> PromptFromMessages component to the Input.  Configure the following messages:<br>

| **Type** | **Template or Variable Name** | <br>
|-----------------------|-------------------------------|
|System            |  Template: _You provide helpful and brief celebrity news to the human who asks._ | <br>
|Human             | Template Document: _prompts/CelebNewsPrompt.txt_ | <br> 

<br>


![](docs/Lab3/GABLab3PromptFromMessages.png)<br>

3. Drag a Resources -> Tool component to the PromptFromMessages <br>
  LLM: Choose your LLM from the drop-down <br>
  MCPTools: Paste in the following code:<br>
```
{
   "tavilyServer1": {
      "url": "https://mcp.tavily.com/mcp/?tavilyApiKey=@secrets(w.p.TavilyKey)",
      "transport": "streamable_http"
   }
}
``` 

<br>
_Note:  You might know all about Tools, if you took the [Academy VAIL AI Class.](https://community.vantiq.com/courses/vail-ai/)  In this case, we're going to directly use a MCP Server that is running on the Internet, in order to do an Internet search._<br>
4. What comes out of the Tool task will need to be prepared to be saved to the SemanticIndex.  Drag in a DocumentLoaders -> ParagraphSplit component to the Tool task. The default configuration is fine here.<br>
4. Drag in a Resources -> SemanticIndexStore to the Tool task.<br>
   SemanticIndex: Choose "w.p.Attendees" from the drop-down<br>
_Note: Now the answers to queries about celebrities will be stored in the SemanticIndex_ <br>
5. We also want the answer to display in the Conversation widget back in the Client.  To do this, we'll drag a CodeBlock to both the SemanticIndexStore and the Tool task, and only return the Tool output, not the SemanticIndexStore output. <br>
   Code: _return input.Tool_<br><br>
   ![](docs/Lab3/GABLab2GetCelebNews.png)<br><br>
   
### Step 2: Ask Some Questions About Celebrities, And Get Answers <br>
1. Run the w.p.SeatingChart Client.  This time, choose a celebrity name from the drop-down right above the "Ask Abby" Conversation widget.  Ask a question about this person, and click the "paper airplane" button to send it to your new GenAI procedure.<br>
2. You should get an answer that makes sense. <br>
![](docs/Lab3/GABLab3Conv.png)<br>
<br>
_Note: In the settings for the Conversation widget, the Service and procedure are already selected to connect to the w.p.Seating.GetCelebNews procedure for sending questions and receiving answers_ <br><br>

### Step 3: Verify That Answers are Saved to the Semantic Index<br>
1. Look at the Task Inputs/Outputs from the SemanticIndexStore task in the w.p.Seating.GetCelebNews procedure.  Notice that the output mentions the entry names for successful semantic loads.<br>
2. Open the w.p.Attendees Semantic Index<br>
3. For each question you asked in the "Ask Abby" Conversation widget, there should be a new entry, and they should correspond to the entry names from the task output in the procedure. <br>

![](docs/Lab3/GABLab3NewSIEntries.png)<br><br>

---------------------------------------------
<br><br>

## Lab 4: Manage a Contextual AI Conversation<br>
**Note:**  There are three ways in Vantiq to manage AI conversations so that they are contextual:

* Using the VAIL ConversationMemory Service, which is covered in the [Academy VAIL AI Class.](https://community.vantiq.com/courses/vail-ai/)<br>
* Using a Collaboration through Visual Event Handler Activity Patterns, taught in the [AI in Event-Driven Applications Class.](https://community.vantiq.com/courses/ai-in-event-driven-applications/)<br>
* Using a Collaboration through Service Procedures, taught in this class, and the method you'll be using here.<br><br>

### Step 1: Create a Type to Structure the Conversation<br>
1. Choose Add -> Type, + New Type<br>
  Name: ConvoType<br>
  Package: w.p<br>
Leave the default _schema_ role and click "Create"<br>
2. In the type pane, choose "Add Property"<br><br>
  Name: _id_
 Leave the default type as "String" and click "OK".  We only need the one property.<br>
 SAVE the type.<br><br>
 <br>
### Step 2: Use the Type to Create an Entity Role for a Collaboration, and Generate the Managing Procedures<br>
3. Go to the w.p.Seating service, Implement tab, and click on the State category. Open the Collaboration State category.<br>
![](docs/Lab4/GABLab4_StateProperties.png)<br>
4. _Click to Edit_ the Entity Roles<br>
5. Create a role _CelebConvo_ of type w.p.ConvoType<br>
  
![](docs/Lab4/GABLab4_CelebConvo.png)<br>

6. Save the Service<br>
7. Open the "Generate State/Entity Procedures" category, and select the toggle next to CelebConvo to generate all the procedures in the Service which will help you manage the AI conversation.<br>
![](docs/Lab4/GABLab4_GenerateCelebConvo.png)<br>
You should now see four new public procedures in the Service: "CelebConvoActivate", "CelebConvoClose", "CelebConvoGetActive", "CelebConvoUpdateActive."<br><br>

### Step 3: Set up the Activate Procedure for a default Conversation<br>
1. We need only one default conversation to be set up, so all that is needed is to uncomment the line in the "CelebConvoActivate" procedure right before the return statement, which reads: <br>
```
// To start/resume a conversation for this collaboration, uncomment the following line:
EXECUTE Seating.ActiveCollabsStartConversation(collaborationId) WITH partitionKey = collaborationId
```
<br>
_Note: The conversationId will be the same as a collaborationId here.  If we had more than one conversation, we would need to set variables and call this statement for each of them to get a unique conversationId for each of them_<br>
<br>
### Step 4: Set the CollaborationContext for the Client<br>
_We have a Collaboration all ready to go, but it needs to be activated from the Client, so the Client can use it with the returned collaborationId_<br>
1. In the w.p.SeatingChart Client Edit tab, open the Data Objects, select Add Property(3x) and create three new Data Objects:  _conversationId_ , _collaborationId_, and _entityId_, all of type String<br>
2. In the w.p.SeatingChart client, open the code editor for the On Client Start event in the Start Page section.  Add this code:<br>
```

   client.data.entityId = client.generateUUID();
	let pkg = {
    	"id" : client.data.entityId
	};

    client.execute([pkg.id, pkg, pkg.id], "w.p.Seating.CelebConvoActivate", function(response) {
        client.data.collaborationId = response;
        client.data.conversationId = response;
        
        client.setCollaborationContext({id: response});
    });

    
```
<br>
_As you can see, we're calling the CelebConvoActivate procedure in the w.p.Seating Service, which requires two parameters: an entityId and an entity instance.  What returns will be a single collaborationId, which we'll use for both our conversationId and collaborationId.  Finally, we call client.setCollaborationContext so the Client will be able to get data from the collaboration that was activated._<br>

_Also, check out the onSendRequest handler code for the Conversation widget.  By default, the human entry is a single String value called "input", and a config property is also sent, containing the "conversationId."  Notice that we don't have to send the conversationId, which is done automatically because we set the Collaboration Context, but we're sending "input" as an object with more than just the human entry to the widget.  This will be important to know when we configure the Conversation branch._

3. In the code editor for the On End event in the Client section, be sure to close the collaboration we won't need anymore:<br>
```
client.execute([client.data.entityId, false], "w.p.Seating.CelebConvoClose", function(response) {});
```
_Here, we're closing the collaboration and setting the asFailure property to false_
<br><br>

### Step 5: Make the GenAI Procedure a Collaboration Conversation Response<br>
_If you look at the configuration for the "Ask Abby" Conversation Widget, you'll see that it's set to get its response from the GetCelebNews procedure in the w.p.Seating Service.  Right now, the procedure isn't in a Conversation branch, so the collaboration doesn't have the conversationId needed to make the response part of the managed conversation state. We'll fix that now!_<br>

1. Click and drag the area around all the components in the w.p.Seating.GetCelebNews GenAI procedure.  At the top, you'll see an option to enclose all the now-selected components into a Conversation branch.  Choose this.<br>

![](docs/Lab4/GABLab4_GABEnclose.png)<br>

The Conversation branch will appear above and below all the selected components:<br>
![](docs/Lab4/GABLab4_FullConvoGetCelebNews.png)<br>

2. Click on the top of the Conversation branch and open its configuration.  Type in _Question_ for the "inputMessagesKey" field.<br>

![](docs/Lab4/GABLab4_inputMessagesKey.png)<br>
  
### Step 6: Run the Client and Verify that Your Conversation is Contextual<br>
1. Run the Client, and choose a celebrity, like Orlando Bloom. Ask a question like "What movies has he starred in?"  You'll see an answer like:
```
Orlando Bloom has starred in movies such as:

The Three Musketeers
The Good Doctor
Main Street
Sympathy for Delicious
New York, I Love You
Pirates of the Caribbean.
You can find more information on IMDb.
```
2. Ask a follow-up question that would require the AI to know what was said before, like, "Are there more?"  You should see another answer, in context, like:
```
Orlando Bloom has starred in a variety of movies, including:

The Cut (2024)
Peppa's Cinema Party (2024)
Gran Turismo (2023)
Pirates of the Caribbean: Salazar's Revenge (2017)
Unlocked (2017)
Romans (2017)
The Hobbit: The Battle of the Five Armies (2014)
Broadway's Romeo and Juliet (2014)
The Three Musketeers (2011)
Pirates of the Caribbean: At World's End (2007)
Pirates of the Caribbean: Dead Man's Chest (2006)
Kingdom of Heaven (2005)
Troy (2004)
The Lord of the Rings: Return of the King (2003)
Pirates of the Caribbean: The Curse of the Black Pearl (2003)
The Lord of the Rings: The Two Towers (2002)
The Lord of the Rings: The Fellowship of the Ring (2001)
You can explore more about Orlando Bloom's filmography on this page.
```
<br>


### Conclusion<br><br>
**Congratulations!** You have successfully completed **all** of the labs in the GenAI Builder class(!!) and should: <br>
- Feel comfortable in the GenAI Builder space<br>
- Know how to use most of the components, having experienced them first-hand<br>
- Deftly be able to create GenAI procedures to meet at least your basic AI project needs<br>
- Know how to use the inputs and outputs of the tasks to your advantage<br>
- Be able to connect your GenAI Procedures from Clients and Service Visual Event Handlers<br>
- Manage contextual AI/Human conversations from a Conversation widget in the Client<br>

##### _Did you get stuck?_ <br>
_In the Lab landing page, click on the "W" in Welcome to download a full solution to all these labs, including w.p.Seating.GetCelebNews GenAI procedure._<br>