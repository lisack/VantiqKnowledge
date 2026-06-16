### Assembly Class Lab – Creating and Consuming an Assembly

#### Objectives:
By the time you complete this lab, you should: <br>
•	Be able to make a simple Assembly<br>
•	Identify ways to make the Assembly more flexible<br>
•	Configure variables that Consumers can set to their needs<br>
•	Become adept at consuming App Components<br>
•	Feel comfortable making changes and doing updates<br>
 
#### Overview:
In this lab, you’ll:
<br>
•	Start with a basic project<br>
•	Convert the project to an Assembly<br>
•	Publish the Assembly to a Catalog<br>
•	Install and run the Assembly from a Consumer NS<br>
•	Change the Assembly, and update to the Catalog<br>
•	From the Consumer NS, update the Assembly to see the changes<br>

##### Step 1: See the Application in the Namespace

**The Project:** Run the PicWorks Client and click the “paw print” button.  You should see an image display in window.  In the multiline widget next to it, you'll see an AI's guess of the breed shown. (If the picture is a gif, this might not show up!)

**How the Application Works:**  
1. The button click is sending the inbound Service Event called PicRequest to the pic.news.PicSvc Service, which calls the _fetch_ procedure and then publishes to the Service ClientDisplay output event.

2. The same PicRequest Event also calls the _askAboutPic_ procedure which prompts the multi-modal AI about the dog breed in the picture.

3. The pic.news.PicWorks Client listens for two Service Event Datastreans, one called _ClientDisplay_ which sets the url for the “CatPic” FixedLayout field within the PicFetchDisplayComponent on the page, and one called _PicDescStream_ which sets the client data property called _desc_ to the AI response to the prompt.  The multiline widget on the page is bound to that data, so the "AI Analysis" appears.


##### Step 2: Create the Assembly
 
1. Study the Project <br>
a.	Read all the code and follow what the Service is doing

2. Make an Assembly <br>
a.	From the Projects menu, choose “Convert to Assembly”<br>
b.	Go through the tabs, choosing the Service to define the Interface, what resources you want to make visible.<br> 
_(**Hints:** <br>Interface: This project doesn't have any expected inputs/outputs. <br>Visible Resources: You'll at least need the Client to be visible so the Consumer can interact with it.)_ <br>
c. Ignore the Configuration tab for now<br>

##### Step 3: Publish the Assembly to the Catalog
 
1.	Create a new empty Namespace and make it a Catalog  _(Hint: Administer -> Catalog)_
2.	Make an access token to the Catalog and connect your Project Namespace to the Catalog
3.	Create another Namespace and connect it to the Catalog.  This will be your Consumer Namespace.  _(Don't switch to it yet.)_
4.	Publish your Assembly to the Catalog

***Hint:**  Make sure it’s the Assembly that you are publishing, and not the Service!* <br>

##### Step 4: Consume the Assembly

1.	Switch to the Consumer Namespace, access and install the Assembly<br>
***Hint:** From Show->Catalogs, choose the Catalog, then find the Assembly.*<br>
2.  Create a Secret called _pic.news.OpenAISecret_ with your OpenAI API key.<br>
3.  In Show -> Documents, you'll find the downloaded Client color themes.  Select them and make them part of the project in order to see them as options in the Configuration. (Select Assembly from Project Contents to see.)
4.	Run the Client and verify that the Application is still running as expected.<br>
***Hint:** You may have to press the button again if the HTTP response errors with 400 status, bad format.*<br>

##### Step 5: Make Configuration Changes to the Assembly

1.	This project is ok as-is, but wouldn’t it be even better if subscribers could change a few things for their needs?  Ideas: <br>
• The Client color theme (Get more from the Add -> Assembly menu)<br>
• The pic.news.OpenAI Secret API key<br>
• The prompt question about the picture.<br> _(Right now it just asks for the dog breed.)_
    
2.	In the Assembly pane of the Project NS, open the Configurations tab<br>
3.  Make the Client theme changeable for the pic.news.PicWork Client.<br>

***Hint:**  The View by Resource drop-down in the Configuration tab is helpful here.  Select the Client and provide a Config Property Name for the options.themeName*<br>

4.  Create a String configuration property called _dogPrompt_ and map it to the corresponding prompt property in the _pic.news.PicSvc.askAboutPic_ procedure.<br>
5.  Create a Secret and map it to _pic.news.OpenAISecret_.  Mark it required.<br>

##### Step 6: Test How Subscribing Works Locally<br>

1.	Switch to “Edit as Consumer” in the Assembly pane, change the Client theme and the prompt to something like "What is the dog doing?", choose your Secret from the configuration drop-down and run the Client.  Do you see the corresponding changes in behavior?<br>

##### Step 7: Update the Assembly<br>
1.	From the General tab, click on the blue "recycle" icon next to the correct Catalog.<br>

##### Step 8: Change the Configuations as a True Subscriber<br>
1.	In the Subscriber NS, refresh the browser window.<br><br>
2.	Click on the badged "book" icon in the Nav bar.<br>
3.	Click to update.  Change all the configurable properties to your new preferences.<br>
4.	Run the Client.  Do you see the expected behavior?

##### Congratulations!  

You have created your first Assembly, made it more flexible with Configurations, and then used it as a Consumer.
From now on, as you build Projects, be looking for opportunities to make more Assemblies, to save yourself future time and effort!

*Did you get stuck?*  Review the videos of the class, where the demonstrations are nearly identical to the lab!