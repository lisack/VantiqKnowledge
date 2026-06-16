#Welcome to the AI Application Developer Foundations Course Labs!<br><br>


![dogs](docs/Lab1/dogs.jpg)<br><br>

##Lab1: Create Supporting Framework for an AI Application<br>

#### Objectives:<br>
* Get comfortable navigating in the IDE<br>
* Gain experience in the Client Builder<br>
* Learn how to make a schema type<br>
* Learn how to create a Service <br><br>

#### Prerequisites:<br>
* You've watched all of the video lectures in the class, up to this point<br>
* You've passed all the quizzes<br><br>

#### Instructions:<br>
####Part 1:  Create a Schema Type and Split the Display _(Hint: Read this whole Part ahead of doing it!)_<br>
0. Take a look at the Project Contents...and notice that there is nothing there, except for documents.  (Don't worry about those yet.)<br>

1. From the Add menu, slide the cursor down to "Type...""<br>

2. In the popup that comes up, choose the ""+ New Type" at the top right<br>

3. Name: _DogSchema_ <br>
   Package: _my.app_  <br>
   Description: _This is the schema for the "dog" entity role_ <br>
   Type: should already be set to "Schema" <br>
   Click "Create"<br>

3. At this point, these instructions disappeared, and the new type pane took up the whole space.  Right-click on the tab for the type at the top, and choose "Split and move right to a new pane".  Now you can see these instructions on the left, and the type pane on the right.<br>

4. Look to the Project Contents again, notice that in the "my.app" package, in the "Type" category, there's your DogSchema.<br>

5. In the DogSchema type window, click on the "Properties" tab, then "+ Add Property"<br>
   Name: _DogId_<br>
   Description: _This will be used to keep track of a collaboration_<br>
   Type: Choose "Integer" from the drop-down<br>
   Click "OK"<br>

6. Oops! It turns out that our DogId would be better as a String!  In the type pane, you'll see your new property.  Under "Actions" in that row, click the little "pen" icon and edit the property to be a "String," clicking "OK" again when finished.  (Now you know how easy it is to change type properties.)<br>

7. At the top right "Save" the type.<br>

####Part 2: Create a Client Page
1. From the Add menu, slide the cursor down to "Client"<br>
2. In the popup that comes up, choose the ""+ New Client" at the top right<br>
3. Name: _DogBehaviorClient_ <br>
   Package: _my.app_  (This is now selectable from the drop-down)<br>
   Template: BrowserEmpty (which is the default)<br>
   Click "Create"<br>
4. Move the Client Builder pane over to the right, so you can keep reading these instructions. ;-) <br>
5. From the "Data Display" category, drag an Image widget to the canvas.<br>
6. Click to select the widget, and open the Specific section of the configuration panel.<br>
7. Click on the blue "cloud" icon to select a new Image.  Choose the "Lab1/dogs.jpg" in the listing.<br>
8. In the Common section, change the name of the image to _Dogs_.<br>
9. In the Layout section, make the image 300 pixels wide by changing the WidthPolicy to Explicit<br>
![](docs/Lab1/width.png)<br>
9. From Data Display, drag a Conversation widget below _Dogs_.  Select it and open Specific.<br>
   Title: _DogTalk_<br>
   In Common, Name: _DogTalk_<br>
10. In Add -> Layout, drag a Vertical layout to the canvas.<br>
11. Drag the top left corner of _Dogs_ to add the image to the layout.<br>
12. Drag _DogTalk_ underneath _Dogs_ so both are in the vertical layout.<br>
13. Select the vertical layout.  In Style, change the Border Radius to 5.<br>
14. Save your Client.<br>
![](docs/Lab1/clientLook.png)  <br>
15. Are you happy with this look?  Check out "Themes" at the top of the Canvas, and the Style and Layout sections for each of the widgets.  Make changes to individualize your Client page.  Fonts, sizes, colors, border types...<br><br>
 

####Part 3: Create a Service<br>
1. From the "Add" menu, choose "Service", then "+ New Service" in the pop-up<br>

   Name: _DogService_<br>
   Package: _my.app_  (This is now selectable from the drop-down)<br>
   _We can ignore the GenAI Agent toggle for now._<br>
   Click "Create"<br><br>
The Service Builder pane will appear, and in the Service category within the my.app package, the Service will be listed in the Project Contents.<br><br>

####Congratulations!  You have completed the Lab, and learned:<br>
* How to navigate in the IDE<br>
* How to create a basic schema type, and edit properties<br>
* How to create a Client page with widgets and layout<br>
* How to create a Service<br><br>

We now have the main framework of our project in place.  Over the course of the next few labs, we will build more functionality into it to make it a full AI application.<br><br>

##### Did you get stuck?<br>
Don't worry, there's a full solution project zip file that you can download by clicking on the "W" in the Welcome title word in the class Lab page!<br>

_______________________________
________________________________
<br><br>

## Lab 2: Build Your First AI Application<br>
(Work on this lab after you've watched the videos and taken the quizzes after the first lab.)<br><br>

### Objectives:<br>
* Learn how to create a Secret<br>
* Gain experience integrating LLMs to the project<br>
* Build a basic GenAI procedure<br>
* Connect a Conversation widget to a GenAI procedure<br><br>


### Prerequisites:<br>
1. Have your OpenAI key ready; you'll need it for this lab!<br><br>

### What the Application Will Do:<br>
1. We're starting off where we left off in the last lab<br>
2. We'll create a GenAI procedure for our Large Language Model to create responses to questions posed in the Conversation widget in the Client<br>
3. We'll use a Prompt Template to keep the LLM on track with our intentions for the application<br><br>

### Instructions:<br><br>

#### Part 1:  Make a Secret for Your OpenAI API Key<br>

1. From the Administer menu, slide to Advanced, then to Secrets.<br>

2. In the Secrets Pane, click the "+ Secret"<br>

3. In the Popup:<br>
   Name: my.app._OpenAISecret_ <br>
   Description: <whatever you want><br>
   Secret: <paste in your OpenAI API Key><br>
Click "Save"<br><br>

#### Part 2:  Integrate a Generative LLM into the Platform<br>

1. From the Add menu, slide the cursor down to "LLM..."<br>

2. In the popup that comes up, choose the ""+ New LLM" at the top right<br>

3. Name: _ChatGPT4_ <br>
   Package: _my.app_ <br>
   Type: Toggle on "Generative"<br>
   Model Name: "openai/gpt-4<x>"<br>
   Description: <whatever will help you remember what it's for><br>
   Secret: Select your OpenAISecret from the drop-down<br>
   System Prompt: _Answer all queries with as much sarcasm as you can muster_<br>
   Click to save the LLM, then click to go to the LLM playground.<br>

4. In the LLM playground, enter a simple prompt, like _Why is the sky blue?_ and check that there is a response, and that it's sarcastic. Now you know that the LLM is working in the platform.<br>
                          
5. Go back to the ChatGPT4 LLM page and remove the System Prompt, so that the field is blank.  (This isn't the only place to enter system instructions; we'll create a prompt template later.)<br>
       
6. Save the LLM.<br><br>
       
#### Part 3: Build a Simple GenAI Procedure with the LLM<br>
                          
1. Go to your my.app.DogService Service<br>
2. In the GenAI Procedures, click on the "+" next to "Public" and "Add Public GenAI Procedure"<br>
![](docs/Lab2/AddGenAIProc.jpeg) <br>
   Name: _DogTalk_<br>
3. From the Resources section, drag a LLM task to Input.<br>
4. Click on the LLM task to select it.  Change the LLM task name to _DogExpert_<br>
5. "Click to Edit" the Configuration.  Select the _my.app.ChatGPT4_ LLM from the drop-down.<br>
6. Click "OK"<br>
7. Save the Service with the blue Save button at the top<br><br>
                          
#### Part 4:  Connect your Client to the GenAI Procedure<br>
1. In the _my.app.DogBehaviorClient,_ select the Conversation Widget to bring out the configuration pane.<br>
2. In Specific:<br>
   Service: <Select _my.app.DogService from the drop-down><br>
   Procedure: <Select _DogTalk_ from the drop-down><br>
3. Save the Client<br><br>
    
#### Part 5: Run the Simple AI Application<br>
1. At the top-right of the Client page, click on the "Play" icon button<br>
2. Where is says "Type your message," ask a dog-related question.<br>
3. In the Service, if you're watchin the _DogTalk_ procedure, you'll see red badges appear on the Input and DogExpert tasks.<br>
3. In the Client, you should see a response appear in the Conversation widget.<br>
    ![Conversation Widget](docs/Lab2/ConversationWidget.png)<br>
4. Great, but now ask a follow-up without providing any context.  It will be obvious from the response that the AI has no idea what the earlier query was about.<br>
5. Now ask a question about anything, like why the sky is blue.  Notice that the LLM is just as willing to give a response about something completely off-topic.<br>
6. You can stop the Client by click the "Stop" icon that used to be the "Play" icon at the top right of the Client window.<br>

####Part 6: Create a Prompt Template<br>
_By adding a prompt, we're giving the LLM more guidance about its core mission._<br>
1. Go to Show -> Documents, and click "+ Document".<br>
2. Copy and paste the following in the pop-up window:<br>
```
You are an expert in canine behavior. Answer all questions honestly and always in regard to dogs.
The question: ${input}
```<br>
3. Choose "Save As..." and call it _templates/DogDocPrompt.txt_<br><br>


####Part 7: Add the Prompt Template to the GenAI Procedure<br>
                          
1. In the DogTalk procedure, from Resources, drag a PromptFromTemplate component to the line between the Input and DogExpert.  When the line turns green, let go.  <br>
2. Click on the PromptFromTemplate task.  Rename it _DogDocPrompt_, and in the configuration for the promptTemplate, choose the Template Document of _templates/DogDocPrompt.txt_ from the drop-down.  Click OK.<br>
3. Toggle on "isSystemPrompt", then click "OK"<br>
4. Save the Service.<br><br>
    
####Part 8: Run the Application Again, and See What's Changed<br>
1. Ask a new question in the Conversation widget.  If it's about dogs, the changes might not be obvious.<br>
2. If you ask a follow-up question, notice that the LLM still doesn't keep track of what was said before.<br>
3. Be sure to ask a random question unrelated to dogs.  Notice how the LLM responds in a way that the subject matter returns to dogs.  This is, of course, thanks to our prompt template.<br><br>
    
   
####Congratulations!  You have completed the Lab, and learned:<br>
* How to create a Secret<br>
* How to add a Generative LLM<br>
* How to check that the LLM is working from the LLM Playground<br>
* How to create a simple GenAI procedure<br>
* How to connect that procedure to your Client<br>
* How to create and add a prompt template to the application.<br><br>

##### Did you get stuck?<br>
Don't worry, there's a full solution project zip file that you can download by clicking on the "2" in the  title word "2nd" in the class Lab page!<br>
_______________________________
________________________________<br><br>


## Lab 3: Build Retrieval-Augmented Generative AI into Your Application<br>
(Work on this lab after you've watched the videos and taken the quizzes after the second lab.)<br><br>

### Objectives:<br>
* Learn how to integrate an Embedding LLM<br>
* Learn how to create a Semantic Index<br>
* Learn how to add entries to the Semantic Index<br>
* Adjust LLM settings in the LLM Playground<br>
* Add RAG to a GenAI procedure<br><br>

### What the Application Will Do:<br>
1. We'll add more dog behavior knowledge for the LLM to look up and use to answer.<br>
2. Our GenAI Procedure will be modified to perform a search of this new material when prompted.<br><br>

### Instructions:<br>

#### Part 1:  Add an Embedding LLM to the Project<br>
1. From the Add menu, choose LLM, then click "+ New LLM"<br>
   Name: _EmbLLMMini12_<br>
   Package: my.app<br>
   Type: Embedding<br>
   Model: "all-MiniLM-L12-v2"<br>
   Description: <your choice><br>
   API Key Secret: _my.app.OpenAISecret_<br>
   (ignore the other settings)<br>
2. Save the new LLM<br><br>
   
#### Part 2: Create a New Semantic Index and Add an Entry<br>
1. From the Add menu, choose Semantic Index, then click "+ New Semantic Index"<br>
   Name: _DogDocs_<br>
   Package: _my.app_<br>
   Embedding LLM: _EmbLLMMini12_<br>
   Default...LLM: _my.app.ChatGPT4x<br>
   (ignore the other settings)<br>
2. Save the Semantic Index<br>
3. At the bottom is a new area for Semantic Index Entries.  Click "+ Index" to add an entry<br>
   Entry Type: "Resource"<br>
   Resource Reference: _Select "Lab3/DogBehavior.txt" from the Documents_<br>
   Id: _DogBehavior_<br>
    ![](docs/Lab3/SIEntry.png)<br>
4. Click "Create"<br>
5. You should briefly see that the Status is "Loading... " followed by "Loaded" in the Index entry listing<br>
6. Take a moment to read the DogBehavior.txt document from Show -> Documents.  Notice that it lists various dog behaviors and what they might mean.<br><br>
    
#### Part 3: Check Out RAG Changes in the LLM Playground<br><br>
1. From the Text menu, choose "LLM Playground"<br>
2. You should see that your Generative LLM is the default choice at the top.<br>
3. Enter the prompt: _Why does my dog tilt his head?_ and note the response.<br>
4. At the bottom of the Playground, toggle on RAG and notice that your Embedding LLM is the default choice.<br>
5. Enter the same prompt, and this time, notice that the response included information from the DogBehavior.txt file.<br>
6. Change various LLM settings in the Playground to get a feel for how they affect LLM responses.<br><br>
    
#### Part 4: Add RAG to the GenAI Procedure<br>
1. In the DogTalk GenAI Procedure, choose a CodeBlock from the Primitives category, and drag it to the line between DogDocPrompt and DogExpert<br>
    Name: _PromptString_<br>
    codeBlock: _return toString(input)_ (VAIL) <br>
    _We're doing this because the next task requires a String, and what comes out of a PromptFromTemplate is a "PromptValue" in Python, so we need to convert it back to a String_<br>
2. From Resources, choose a SemanticIndex and drag it to the line between PromptString and DogExpert<br>
   Name: _DogDocs_<br>
   Semantic Index: my.app.DogDocs<br>
   (click OK)<br>
   contentOnly: (toggle this on!)<br>
   minSimilarity: _0.5_<br>
   (click OK again)<br>
3. Save the Service<br>
_Are you wondering why we don't use a RAG component? We could, but the output format is different, and we'd have to alter it to be displayable in the Conversation widget._<br><br>
    
#### Part 5: Run the Application with RAG<br>
1. Start the Client, and ask a dog behavior-related question.  Notice that the response references the DogBehavior document in the Semantic Index.<br><br>


#### Part 6: Learn More about GenAI Procedures<br>
1. In the DogTalk procedure, click on DogDocs and open the View Task Input/Output section of the configuration pane.<br>
2. Open the last task run at the bottom of the list.  Notice that you can view both the input and output from this task, and any other task.<br>
3. At the top right of the GenAI Builder pane, look for the "gear" icon and "Properties".  Click on this.
4. Click to view the Generated Script.  This is the Python code generated to create this procedure.  It is read-only, and very informative of what is going on.<br><br>
    
####Congratulations!  You have completed the Lab, and learned:<br>
* How to work with Semantic Indexes<br>
* How to add RAG capabilities to GenAI Procedures<br>
* How to navigate and learn more about GenAI Procedures<br><br>

##### Did you get stuck?<br>
Don't worry, there's a full solution project zip file that you can download by clicking on the "b" in the Lab title word in the class Lab page!
<br>
_______________________________
________________________________<br><br>
    
## Lab 4: Using a Collaboration to Manage a Conversation<br>
(Work on this lab after you've watched the videos and taken the quizzes after the second lab.)<br><br>

### Objectives:<br>
* Learn how to set up and entity role and procedures for a Collaboration<br>
* Learn how to initiate the Collaboration from the Client<br>
* Learn an alternative RAG method in a GenAI Procedure<br>
* Learn how to add Conversation capabilities to a GenAI procedure<br><br>

### What the Application Will Do:<br>
1. Finally, you'll be able to have a real, contextual, managed AI conversation between Client and Service!<br><br>

### Instructions:<br><br>

#### Part 1:  Set Up the Collaboration in the Service<br>
1. In the my.app.DogTalk Service, go to the Implement tab and click "State" next to the gear icon.<br>
2. Open the Collaboration State Properties drop-down, and click to edit an Entity Role<br>
3. Click "+ Add an Entity Role"<br>
   Value: _Dog_ (Really, this could be anything)<br>
   OfType: "my.app.DogSchema"<br>
   OK<br>
   Save the Service<br>
4. (We'll leave the Named Conversations alone, and just use the default.) Take note of the "Close all active collaborations" blue words. _During the course of development, if you suspect that your application didn't property close a Collaboration, click on those words to clear the memory._ Now open the "Generate State/Entity Procedures"<br>
5. Toggle on all the procedures for the "Dog" entity role.<br>
6. Verify that you can now see the Dog procedures in the Public Procedures area of the Service Implement tab.<br>
    ![CollabProcedures](docs/Lab4/CollabProcedures.png)<br>
7. While still in the Implement tab, click on the DogActivate procedure.<br>
8. Uncomment the line near the very bottom, to start the default conversation for this collaboration<br>
    ![UncommentConvoLine](docs/Lab4/UncommentConvoLine.png)<br>

#### Part 2: Set Up the Collaboration in the Client<br>
1. In the Edit tab, open Data Objects, and choose Client Data<br>
2. Click "+ Add Property"<br>
   Name: _collaborationId_<br>
   Data Type: String<br>
   ("Save & Exit")<br>
3. In the Edit tab for the my.app.DogBehaviorClient, click on the "</>" symbol near the top of the left panel, just under the tabs.  (This shows events where code is and could be added.)<br>
4. Under Start, click on "On Client Start".  In the editor, paste the following code:<br>
```
var DogEntity = {
    ID : "woof"
};
 
client.execute([DogEntity.ID, DogEntity], "my.app.DogService.DogActivate", (collaborationId) => {
    client.data.collaborationId = collaborationId;
    client.setCollaborationContext(collaborationId);
 
});
```<br>
_This is activating the Collaboration in the Service by calling the DogActivate procedure, and setting up the Client to get the Collaboration information, too._
5. In the Edit tab, under Client, click on "On End". In the editor, past the following code:<br>
```
var quitPkg = {
    "entityId" : "woof",
    "asFailure" : false
};
    
client.execute(quitPkg, "my.app.DogService.DogClose", () => {});
```<br>
    
_It's important to clean up Collaborations when we're finished with them_<br><br>

#### Part 3:  Make the AI Response Part of the Collaboration Conversation<br>
1. In the my.app.DogService Implement tab, click on the DogTalk GenAI procedure.<br>
2. In the procedure flow, shift-click on DogDocPrompt, PromptString, DogDocs and DogExpert, so that all four tasks are outlined in blue.<br>
3. At the top of the pane, click on "Enclose In" and then click "Conversation"<br>
    ![EncloseInConversation](docs/Lab4/EncloseInConversation.png)<br>
4. "Cancel" the "Select" message at the top, for creating a Component<br>
5. Click on the top of the Conversation branch:
   inputMessagesKey: _request_<br>
   historyMessagesKey: _history_<br>
6. Save the Service.<br>

#### Part 4: Try Another RAG Solution in the GenAI Procedure<br><br>
1. Click on the DogDocs task to select it, then press the Delete key on your keyboard to Delete it without affecting the rest of the procedure flow.<br>
2. Delete the DogExpert task, too.<br>
3. In the AI Patterns category, find RAG and drag it to the line under PromptString.<br>
   Name: _DogDocsRAG_<br>
   SemanticIndex: (the only one we have)<br>
   qaLLM: (the only one we have)<br>
   useConversation: (toggle ON)<br>
_What comes out of the RAG task is a whole structure; we just want the answer, so we'll write a task to do that._<br>
4. From Primitives, drag in a CodeBlock to the line under DogDocRAG.<br>
   Name: _Answer_<br>
   Code: _return input.answer_<br>
   (OK)<br>
5. Save the Service.<br>
    
#### Part 5: Make some Adjustments to the Conversation<br><br>
_If we try to run the application now, it will fail because the Conversation needs two pieces of information: input, which is a String; and conversationId, which is a property in the config structure.  The Conversation widget automatically sends both, but now that the whole object is considered input.  We now have to call the String value something else, which is why the Conversation is expecting "request"._<br>
1. In Show -> Documents, edit your template/DogDocPrompt.txt to:<br>
```
You are an expert in canine behavior.  Be sure to keep the conversation history in mind when you answer the human's question succinctly and always in regard to dogs.
 
The question: ${request}
 
The conversation history: ${history}
```  <br>
    
4. In the my.app.DogBehaviorClient, click on the Conversation widget, and open the Event section.
5. Click to edit the On Send Request, and paste in:
```
var orig = extra.obj.input;
var modern = {"request" : orig};
extra.obj.input = modern;
```
_This code just takes the expected "input" string and renames it "request" so there is no confusion with the now-object "input" that the Conversation expects._<br><br>
    
#### Part 6: Run the Application and Verify Full Conversations<br>
1. Run the Client, and ask a dog-related question.<br>
2. Notice that the response should still be informed by the Semantic Index search.<br>
3. Ask a follow-up question that depends on the earlier conversation.<br>
4. The LLM should be able to respond, because now the whole conversation is managed in the Collaboration.<br><br>

#### Part 7: View the Tasks in the GenAI Procedure<br>
1. If you haven't tried this already, select each task in the GenAI flow, and open the View Task Input/Output to see the list of executions done on the task.  View the inputs and outputs so you can see and understand what the GenAI procedure is really doing.<br><br>
    
####Congratulations!  You have completed the Lab, and learned:<br>
* How to set up a Collaboration to manage AI conversation history<br>
* How to add Conversation capabilities to a GenAI procedure<br>
* How to instantiate a Collaboration from the Client<br>
* How to get Collaboration context for the Client<br>
* How to close a Collaboration from the Client<br>
* A Second way to do RAG in a GenAI Procedure.<br>
    

##### Did you get stuck?<br>
Don't worry, there's a full solution project zip file that you can download by clicking on the second "e" in the Welcome title word in the class Lab page!<br>

_______________________________
________________________________

    
## Lab 5: Using a Catalog Namespace to Distribute an Application<br><br>
(Work on this lab after you've watched the videos and taken the quizzes after the second lab.)<br><br>

### Objectives:<br>
* Learn How to Create a Catalog<br>
* Learn Two Ways to Connect a Catalog to a Namespace<br>
* Learn How to Publish Resources and Subscribe to Them with a Catalog<br>
* Learn How to Make Clients Launchable in the Mobile App<br>
* Use Subscription Resources<br><br>

### What the Application Will Do:<br>
1. You'll have a Client interface in another Namespace, but you'll still be able to access resources in your original Namespace.<br><br>

### Instructions:<br><br>

#### Part 1:  Create a Catalog Namespace<br>
1. Go to Administer in the Nav Bar and choose "Namespaces."<br>
2. In the Namespaces pane, choose "+ Namespace"<br>
   Name: _DogCatalog\_<your initials>_<br>
  Save<br>
3. Click on the "globe" icon next to your current Namespace name.  In the popup, choose your "DogCatalog"<br>
_Make sure your current project is saved!_<br>
4. In the New Project popup, choose Empty and click "Continue", then "Finish"<br>
5. Choose Administer -> Advanced -> Catalog<br>
6. Click "Create Catalog" confirm in the pop-up, and click "Create Catalog" again in the optional name popup<br>
7. In the Manage Catalog pane, click "New Token"<br>
   Name: _DogCatalog_<br>
   _Nothing else needs changing_ Click "Create"<br>
_The new token is in your computer clipboard._<br><br>
   
#### Part 2: Connect your Catalog to Other Namespaces<br>
1. Switch back to your previous Namespace by clicking on the Globe icon and selecting it from the list.<br>
2. Go to Show -> Catalogs and click "Connect"<br>
3. Paste in the new access token and make sure the URL is the server location of the Catalog<br>
4. Click "Connect"<br>
_In the Catalogs pane, you will see your Catalog listed._<br>
5. From Administer -> Namespaces, create a new Namespace<br>
   Name: _DogAdvisorRemote\_<your initials>_<br>
   Connect to Catalog: _choose your Catalog from the drop-down_<br>
   Save<br>
6. Verify that the Catalog is now listed in the Catalogs pane. <br><br>

#### Part 3: Publish Resources to your Catalog<br>
1. Go to your my.app.DogService Interface tab.<br>
2. Click on "General."  Publish the Service to your Catalog by clicking on the "cloud" icon next to the catalog name. Click "Publish" in the Confirm pop-up.<br>
3. Open your my.app.DogDocs Semantic Index.  Publish the Semantic Index to the Catalog; it's below the entries pane.  Confirm.<br>
4. Back in the Show -> Catalogs window, click on the Catalog and verify that you can see your Service and your Semantic Index listed by resource type.<br>
_Good job!  You've successfully published from this Namespace._<br>
    
#### Part 4: Download the Dog Image for Use in the other Namespace<br>
1. Go to Show -> Documents<br>
2. Find the document named _Lab5/dogs.jpg_ and right-click on it to download to your local filesystem.<br><br>
    
#### Part 5: Subscribe to Resources from the Catalog.<br>
1. Switch to the DogAdvisorRemote Namespace. _Hint: The "Globe" icon, then select from the list._<br>
2. In the New Project pop-up, choose Empty, then Finish in the next pop-up.<br>
_The Namespace should be completely empty, with nothing listed in the Project Contents._<br>
3. Go to Show -> Catalogs.  You should see the Catalog listed there.<br>
4. Click on the Catalog name, and then on Services.  <br>
_If you click on the my.app.DogService listing, you'll see it (ReadOnly) but you won't be subscribed to it._<br>
5. Right-click on "my.app.DogService" and choose "Subscribe", then "Subscribe" again in the pop-up.<br>
6. Look at the Project Contents now.  In the my.app package, you'll see the Service and the schema type.<br>
7. Subscribe to the my.app.DogDocs Semantic Index, and verify that it turns up in the Project Contents.<br><br>
   
#### Part 6: Create a Mobile Client Page<br>
1. From the Add menu, create a new Client<br>
   Name: _DogMobile_<br>
   Package: _far.away_<br>
   Template: "MobileEmpty"<br>
2. From the Edit tab, right-click on the "Client" and choose "Edit Client Properties..."<br>
   ![EditClientProperties2](docs/Lab5/EditClientProperties2.png)<br>
3. Go to the Advanced Tab, and toggle on "Mark as Launchable", then click the OK button, and Save the Client.<br>
4. From the Data Display category, drag in an Image and a Conversation widget below the Image<br>
5. Select the Conversation, changing the Title to _Dog Talk_<br>
   Service: my.app.DogService<br>
   Procedure: _DogTalk_<br>
   Conversation Name: (leave default)<br><br>
  
#### Part 7: Code the Mobile Client<br>
_Remember that our other Client had code in three places, and a Client data object?  We need to set up the same here._<br>
1. In the Client Edit tab, open Data Objects and choose Client Data Object.<br>
2. Click the "+ Add Property"<br>
   Name: collaborationId<br>
   Data Type: (leave as String)<br>
3. Create another property, _dogEntityId_ also of type String<br>
   (Save and Exit)<br>
4. In the Client Edit tab, under the Start page, choose "On Client Start"<br>
5. Paste in this code:<br>
```
var DogEntity = {
    ID : Math.floor(Math.random() * 10000)
};
 
 
client.execute([DogEntity.ID, DogEntity], "my.app.DogService.DogActivate", (collaborationId) => {
    client.data.collaborationId = collaborationId;
    client.data.dogEntityId = DogEntity.ID;
 
});
```<br>
_It's better to make a unique Entity ID to avoid name collisions, but otherwise, this is identical to what you coded before in your other Client._<br>
6. In the Start page "On End" code area, paste in:<br>
```
client.execute(client.data.dogEntityId, "my.app.DogService.DogClose", () => {});    
```<br>
7. After saving the code, select the Conversation widget and in the Event section, click on "On Send Request"<br>
8. Paste in:<br>
```
var orig = extra.obj.input;
var modern = {"request" : orig};
extra.obj.input = modern;
```<br>

_Notice(!) we did not need to create any LLMs or Semantic Indexes; didn't set up any Collaborations either.  All that is already done in the publisher namespace; we just interface with what we subscribed to._<br><br>
    
#### Part 8: Run the Application from the Mobile App<br>
1. If you haven't already, download the Vantiq Mobile App from the app store corresponding to your phone.
2. Open the app and sign in to your server, using your credentials.<br>
3. Type in your server url (Example: _https://dev.vantiq.com_) and look for your _DogAdvisorRemote\_<your initials>_ Namespace.<br>
4. Once in the Namespace, you should be able to click "Run" at the bottom of the screen to see your Client<br>
    ![DogMobile1](docs/Lab5/DogMobile1.jpeg)<br>
    and then click on the Client to start the application.  Ask a question about dogs and you should see your AI response!<br>
    ![DogMobile2](docs/Lab5/DogMobile2.jpeg)<br>

####Congratulations!  You have completed all of the labs(!), and learned:<br>
* How to create a full Client - Service AI Conversation<br>
* How to set up a Collaboration to manage that conversation<br>
* How to make resources available remotely via the Catalog<br>
* How to use the Vantiq Mobile App<br>
* How to generally navigate the IDE and get to the tools you need.<br>
    

##### Did you get stuck?<br>
Don't worry, there's a full solution project zip file that you can download by clicking on the word "last" in the class Lab page!<br>