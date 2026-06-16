#Welcome to the VAIL AI Class Labs!

### Objectives:
* Reinforce your comfort level navigating in the IDE
* Gain more experience writing VAIL code with AI features
* Learn how to use those AI features

### Prerequisites:
* You've watched all of the video lectures in the VAIL AI class, up to the point of the current lab you're working on
* You've passed all the quizzes up to the point of the lab
* You have an API key from a paid subscription to OpenAI

## Lab 1

### What the Application Will Do by the End of Lab1:
1. The "CEO" enters questions in the "Executive Assistant" conversation 
2. If the question is about his schedule, a Tool is called that gives specific information
3. If the CEO asks about his schedule for Sunday, the Tool functionAuthorizer forces an error
![](docs/Lab1/EAClientScheduleAnswers.png)


### Instructions:
####Part 1:  Check that You Have What You Need to Get Started
0. Check that in your project there is a e.a package with:<br>
* One Client, EAClient<br>
* One Service, EASvc<br>
_Note: There are a few VAIL public procedures in the Service; don't worry about them yet!_<br><br>

#### Part 2:  Integrate a Generative LLM into the Platform<br>

1. From the Add menu, slide the cursor down to "LLM..."<br>

2. In the popup that comes up, choose the ""+ New LLM" at the top right<br>

3. Name: _EALLM_ <br>
   Package: _e.a_ <br>
   Type: Toggle on "Generative"<br>
   Model Name: "openai/gpt-4<x>"<br>
   Description: <whatever will help you remember what it's for><br>
   Secret: Select "Add a New Secret" and enter a new Secret with your OpenAI API key value<br>
   System Prompt: _You are a very helpful Executive Assistant to a CEO.  Always answer courteously and professionally._<br>
   Click to save the LLM, then click to go to the LLM playground.<br>

4. In the LLM playground, enter a simple prompt, like _Why is the sky blue?_ and check that there is an AI response, as if an executive assistant were replying. Now you know that the LLM is working in the platform.<br><br>
       
#### Part 3: Create a Procedure to Use the LLM<br>
1. In the EASvc Implement Tab, click on the "+" next to Public in the Procedures section to create a new VAIL public procedure.  Change its name to _requestHandler_, with a single parameter _input_ of type String<br>
2. Write a single line of code to make a response variable equal to the command to submit the input parameter as a prompt to your e.a.EALLM.  <br>
_Hint: Refer to the proper syntax [here](https://dev.vantiq.com/docs/system/rules/#llm) to figure this out._<br>
3. Write code to return the response variable.<br><br>

#### Part 4: Connect the Conversation Widget to the Procedure, and Run the Application<br>
1. In the Client, click on the Conversation Widget to bring up the configuration pane<br>
   Service: "e.a.EASvc"<br>
   Procedure: "e.a.EASvc.requestHandler"<br>
   Save the Client<br>
2. Click on the "play" button to run the Client. Type in a question, and make sure the procedure is responding.
       
#### Part 5: Add a Tool to Report A Schedule<br>
1. In the e.a.EASvc.requestHandler, add a variable called "ToolProcedures" set to an empty array<br>
2. Add another line that sets the first element of the ToolProcedures to the mySchedule procedure in the same Service.<br>
_Hint: ToolProcedures[0] = "procedures/e.a.EASvc.mySchedule"_<br>
3. In the submitPrompt command, add ToolProcedures as the tool parameter<br>
4. Be sure to read through the mySchedule procedure so you see what the tool is about.<br>
5. Save the Service.
6. Run the Client again, and ask questions about what you're doing on a given day, when you're seeing someone, if you're going to be doing some activity, etc.  You should see log messages about "checking the schedule" so you know the tool procedure was involved.<br><br>
                          
#### Part 6: Add a Tool functionAuthorizer<br>
1. In the Service, create another public procedure called "BossBlock"<br>
2. The procedure should have two parameters: _name_ of type _String_, and _arguments_ of type _Object_<br>
3. Write a simple _if_ statement that checks if "arguments.subject" is equal to Sunday.  If so, return _false_.  Otherwise, return _true_.
4. Save the Service.<br>
5. Back in the "requestHandler" procedure, update the submitPrompt command to include a functionAuthorizer.<br>
6. Save the Service again.<br>
7. Run the Client again.  Ask a question about any day but Sunday, and you should get a good response from using the tool.  Now ask a question about Sunday.  The Client should stop running and an error should pop up:<br>
    ![](docs/Lab1/BlockBossError.png)<br>
    
#### OPTIONAL: Try a Sequenced Response
1. Change the submitPrompt command in the requestHandler procedure to the one that returns a sequenced response, then run the Client and ask for a 1,000 word story.  (Notice that the response will come in pieces, rather than all at once.)
    
#### Congratulations!  You have successfully:<br>
* Integrated a LLM to the project<br>
* Created a simple VAIL procedure to submit a question to a LLM and return the response<br>
* Connected the Client Conversation widget to the procedure<br>
* Added and used a Tool to be called in certain circumstances<br>
* Created a functionAuthorizer procedure to prevent the Tool from running if the CEO asks a question about Sunday's schedule.<br>

_Did you get stuck?  You can download a completed project by clicking on the "o" in "You" in the Lab page title!_<br><br>
    
-----------------------------
    
-----------------------------
## Lab 2<br><br>
![](docs/Lab2/EAClientLab2.png)<br>
### What the Application Will Do by the End of Lab2:<br>
1. The "CEO" enters questions in the "Executive Assistant" conversation <br>
2. Now there're some better prompts, so the AI is better instructed and informed about what to do
3. The mySchedule tool will be strengthened with a prompt template and system information to be even more helpful.<br><br>

### Instructions:<br>
####Part 1:  Add more System Instruction<br>

1. Consider what the AI already knows about itself, which is that it's a professional assistant.  Now add more information to the EALLM prompt description that tells the AI more about the CEO - name (John Smith), company name (Megacorp Conglomerated), family members (Katie, grandaughter; Alice, wife; Bill, son; Anna, daughter-in-law). Feel free to add any number of finer details to help the AI understand its circumstances.<br>
2. Run the EAClient and ask pertinent questions about 'yourself' as the CEO and the company.  The AI response should include what you've put into the prompt.<br><br>
    
#### Part 2: Create a Prompt Template<br>
_Remember how the mySchedule tool put the weekly schedule into a JSON format for reading?  Let's make this easier by just listing the schedule in a document template, then referencing it in the mySchedule procedure for use._<br>
1. Go to Show -> Documents and right-click to Edit "WeeklySchedule"<br>
2. At the top are three lines ending in a colon.  Create a variable for each of them, called _DayOfWeek_, _TimeOfDay_ and _TodayDate_ respectively.<br>
_Hint: Click [here](https://dev.vantiq.com/docs/system/rules/#template) for help._<br><br>

#### Part 3:  Change the mySchedule Tool to Reference the Template<br>
1. In the e.a.EASvc, open the mySchedule procedure<br>
2. Remove every line after the "Checking the schedule" log.info line.  _This would include the variable set to the JSON structure detailing the week's schedule._<br>
3. Create a variable, _input_ and set it equal to a JSON structure.  The first propery should be _DayOfWeek_ set to a procedure call to "e.a.EASvc.getDayOfWeek".<br>
   Make the second property _TimeOfDay_ set to a procedure call to "e.a.EASvc.GetTimeOfDay"<br>
   Finally, make the third property _TodayDate_ for a procedure call to "e.a.EASvc.getTodayDate"<br>
4. Now, write a line to format the documentReference to "WeeklySchedule", using the _input_ variable for the formatting.  Make sure that value is what the procedure returns.<br><br>
    
#### Part 4: Give more Examples in the Procedure Declaration<br>
1. Try to run the Client now, and ask the assistant about the current time or today's date.  Notice that the AI doesn't give the correct answer.  Now check the Log Messages.  Was the mySchedule tool involved?<br>
2. Add description to the procedure comments at the top, and/or example questions in the parameter description to include extra questions that might be asked, like 'What day is it?,  'What time is it?'', 'What's the day of the week?'<br>
3. Run the Client again, and verify that now the tool is being called, and the responses are more correct.<br><br>
    
#### Part 5: Make a New Tool Using the @repeat to Template Array Elements<br>
1. In the Procedures area of the EASvc, find and open the GoodMorningEve procedure.<br>
2. Read what's there, and how this tool will be called.  Notice we have an array with three elements; messages that came in for the 'CEO'.<br>
3. Create a template variable set to a string using @repeat to define how the properties within each array element should be displayed, followed by @endrepeat.<br>
4. Write a return statement that uses the Template service procedure to format the template and set the array element as coming from the array.<br>
5. Run the Client again, this time wishing the assistant a good morning.  Make sure the response is a professional recounting of the messages.<br><br>
    
#### Congratulations!  You have successfully:<br>
* Used templates two different ways, within two tools<br>
* Strengthened your application by improving the initial prompt and adding more tool functionality<br>

_Did you get stuck?  You can download a completed project by clicking on the "2" in the Lab page title!_<br>
    <br>
-----------------------------
    
-----------------------------
## Lab 3<br><br>
![](docs/Lab3/EAClientLab3.png)<br>
### What the Application Will Do by the End of Lab3:<br>
_Currently, our 'Assistant' only answers the questions it is asked, and has no memory of what came before. We're now going to build in some conversation managment so the AI conversation will maintain context!_  
1. Conversations with the AI Assistant will now be contextual, full conversations.<br><br>
### Instructions:<br>
####Part 1: Create a Unique ID for the Conversation<br>
1. In the Edit tab of the Client, open the Data Objects and click on "Client Data"<br>
2. Create a new property, called "ConvoID" of type String and then OK<br>
3. In the Edit tab, click on the "\<\/\>" icon, and then on the "On Client Start"<br>
4. In the code editor, uncomment the following line:<br>
```<br>
client.data.convoID = String(Math.floor(Math.random() * 1000));
```<br>
5. Save the code, and the Client<br>
6. Click on the Conversation widget<br>
7. In the Event section, click the "On Send Request"<br>
8. In the code editor, uncomment the following line:<br>
```<br>
extra.obj.convoID = client.data.convoID;
```<br>
_This conversation id number will be sent every time the human sends a message in the Conversation widget._<br><br>

####Part 2:  Add code to Create and Maintain a Conversation<br>

1. Open the handleRequest procedure in the EASvc Service.  Add the following code:
    * Builds a human-type ChatMessage from the input parameter.<br>
    _Hint:  Relevant documentation is [here.](https://dev.vantiq.com/docs/system/rules/#chatmessage)_<br>
    * Checks if it's possible to add the new ChatMessage to an existing conversation.  If not, then start one. <br>
    _Hint:  If it can't add to an existing conversation, an error is thrown, so put this attempt into a [try/catch statement](https://dev.vantiq.com/docs/system/rules/#try).  Also, [here](https://dev.vantiq.com/docs/system/rules/#conversationmemory) is the pertinent documentation for adding/starting conversations.<br>
       
2. Add the LLM response to the conversation. _Hint: Look [here](https://dev.vantiq.com/docs/system/rules/#llm) for the documentation._ <br>
3. (Optional) Build in a mechanism for ending the conversation, probably with a tool and a phrase from the human, _but the conversation will automatically disappear after half an hour of inactivity, so this is not vital for our purposes._<br><br>
   
####Part 3: Run the Application Again<br>
1. Run the Client, and this time, be sure to ask follow-up questions that wouldn't make sense out of context.  Verify that the AI doesn't lose the thread of what you're asking.<br><br>
    
#### Congratulations!  You have successfully:<br>
* Learned to manage an AI conversation, using the appropriate Vantiq services.<br>
* Learned how to use a conversationId that identifies the conversation for the life of the interaction.<br>

_Did you get stuck?  You can download a completed project by clicking on the "L" in the Lab page title!_<br><br>
    
-----------------------------
    
-----------------------------
## Lab 4<br><br>
![](docs/Lab4/EAClientCoffee.png)<br>
### What the Application Will Do by the End of Lab4:<br>
1. You'll be able to ask for coffee, and your assistant will verify how you like it before sending the order.<br><br>
### Instructions:<br>
####Part 1: Set the conversationId for the Conversation Widget<br>
1. In the Edit tab of the EAClient, go to the code for the onStart of the Start page, and uncomment the line  there.<br><br>

####Part 2: Create a try/catch for a "coffee" reply<br>
1. In the EASvc Service "requestHandler" procedure, after the LLM.submitPrompt call, add the following _if_ statement:<br>
```
if (match(reply, regExp("coffee"))) {

	var p = "How will you take it today?"

	try {
		var response = XXXXX
		reply = toString(response) + ", coming right up!"
	
	
	} catch(error) {
		reply = "I'll assume you'd like it black."
		
	}
} 
```<br>
2. Where the XXXX's are, supply the proper Callback Service procedure call to invoke a callback message asking the CEO how he takes his coffee, and waiting a minute for the response.  <br><br>

####Part 3: Run your Client and ask for coffee<br>
1. Run the Client.  Type in a request for coffee. Does the Assistant ask how you like it?  Does it wait a whole minute for your response?  Verify that the behavior is as you expect!<br><br>
    
#### Congratulations!  You have successfully:<br>
* Learned to peform a Callback invocation to a Conversation widget, and react to what comes back.<br>
<br>

_Did you get stuck?  You can download a completed project by clicking on the "4" in the Lab page title!_<br><br>
    

-----------------------------
    
-----------------------------
    
## Lab 5<br><br>
![](docs/Lab5/EAClientLab5.png)<br>
### What the Application Will Do by the End of Lab5:<br>
1. The AI will now have knowledge of Employee Policies specific to Megacorp Conglomerated.<br><br>
### Instructions:<br>
####Part 1: Integrate an Embedding LLM<br>
1. From Add->LLMs, choose "+ New LLM"<br>
   Name: _EAEmbedding_<br>
   Package: _e.a_<br>
   Type: Embedding (should be the default)<br>
   Model: "all-MiniLM-L6-v2"<br>
   Description: (Your choice)<br>
   Secret: "e.a.EASecret"<br>
   (Leave the rest to defaults, and SAVE)<br><br>

####Part 2: Create an Populate a Semantic Index<br>
1. From Add->Semantic Index, choose "+ New Semantic Index"<br>
   Name: _EmployeeSI_<br>
   Package: _e.a_<br>
   (Select your Embedding and Q\&A LLMs from the drop-downs)
   Description: _For employee-related subjects_<br>
   (Leave the rest to defaults, and SAVE)<br>
    ![](docs/Lab5/EASI.png)<br>
2. Click on "+ Index" and choose "Resource" from the drop-down<br>
3. Click on the "none"" next to "Resource Reference" and select "Megacorp Conglomerated Employee Handbook.pdf" from the list.<br>
   ID: "EmployeeHandbook"<br>
4. Verify that the Handbook loaded into the Semantic Index successfully.<br>
    ![](docs/Lab5/EASILoad.png)<br><br>
####Part 3:  Write a Tool to Search the Index for Personnel Questions<br>
_By now, you are familiar with the process of writing a tool, so instructions will be minimized!_<br>
1. Call your new tool procedure _EmployeePolicies_<br>
2. Be sure to write lots of procedure descriptions, both in the top comment section and for the expected parameters.<br>
3. You will need to perform a semantic search to get the answers requested.  Look [here](https://dev.vantiq.com/docs/system/rules/#semanticsearch) for the relevant documentation.<br>
4. Don't forget to add this tool to the ToolProcedures array in the requestHandler procedure!<br><br>
    
####Part 4: Run Your Completed Application<br>
1. In the Client, ask employee-related questions.  Verify that the responses are consistent with what is in the Employee Handbook.<br><br>
    
## Congratulations!  You have successfully completed all of the Labs!<br>
* In the process, you've created a useful application, using VAIL procedures as tools, which the AI LLM will evaluate to respond appropriately to real-time conditions!<br><br>

_Did you get stuck?  You can download a completed project by clicking on the "L" in "Last" in the Lab page title!_<br><br>