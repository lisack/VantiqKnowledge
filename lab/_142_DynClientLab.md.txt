# Welcome to the Dynamic Client Content Labs!

### Purpose:
Learning is best accomplished by doing.  After watching the videos about how to create dynamic Client content, and taking the quizzes to ensure reasonable comprehension of the material, this is your chance to convert that basic understanding into actual experience.

### Objectives:
By the end of these labs, you will have had hands-on experience building the following knowledge and skills:
	• Creating widgets dynamically in a Client page
    • Configuring widget properties in code
    • Creating dynamic event handlers
    • Creating dynamic datastreams for use by the dynamic content in the Client page
    
### Overview:
This project description is divided into instructions for two labs, separated by several video lectures.

#### Lab 1: (Estimated time to complete: 1 hour)
In this first lab, you will create, position and alter several widgets for display on a Client page.
Under a title, there will be a DataTable for displaying visitor information.  Under the table, within a horizontal layout, will be two buttons.

#### Lab 2: (Estimated time to complete: 45 minutes)
In the second lab, you will code event handlers and a datastream for widget display.  
	• One of the buttons will be coded such that a click will close the Client.
    • The other button will start a timed query that populates the DataTable
    • Upon clicking a row of the DataTable, a popup page will appear with more details about the visitor in the row.

At the end of this lab, you will have built a basic Client application that queries a standard type and displays the data in different ways.  The project supplies a "starter Client page", data and the popup page, but it will be up to you to follow these instructions to build the main page at run-time and program the event handlers so others can use the application.

### Instructions for Lab 1:
#### Step 1: Build & Display Static Text
1. On the Client page, you'll see one sad, empty VerticalLayout widget, called _FormVert_.  Go to Help -> Developer Guides -> Client Builder -> Client Builder Reference Guide, and keep it open.  You will need to refer to it often to see how to set widgets properties in code.  _Hint:  Don't forget to look up the widget hierarchy to see all the possible properties that can be set!_<br>
2. In the Client Start event handler, create a new StaticText to be a title for the small form you'll be building:
	• Give it the name _titleText_
    • Font size: 24
    • Font weight: bold
    • Text color: <your pick!>
    • Title: "Visitor Data Logs" <br>
3. Put the new StaticText widget into the FormVert.  Run the Client and verify that you can see the text there.<br>
#### Step 2: Create and place a new Data Table
1. Now code for a new DataTable:
	• Name: _visTable_
2. Put the DataTable into the bottom of the FormVert.  Run the Client and verify that the title text is at the top of FormVert, and the DataTable is below it.<br>
#### Step 3: Build another Layout and Buttons to Go Into It
1. Code for a new HorizontalLayout:
	• Name: _btnLO_
    • height & width policies set to SizeToParent _Hint: Check Client Builder Reference Guide to get the exact setting structure_<br>
2. Put the new HorizontalLayout into the bottom of the FormVert then run the Client to check that it's there.<br>
3. Create a new Button:<br>
	• Name: "refreshBtn"<br>
    • Label : "Refresh Table"<br>
    • Height & Width policies: SizeToParent <br>
4. Clone your new Button: _Hint: Look in the docs for client.clone()_<br>
	• Name: "closeBtn"<br>
    • Label: "Close"<br>
    • Label Color: <your choice!> _Hint: foregroundColor_ <br>
    • Button Color: <your choice!> <br>
5. Change the foregroundColor and backgroundColor of at least one of the buttons.<br>
6. Add both buttons to the btnLO layout.  Again, check how the Client looks when run.<br>

#### Step 4: Position the Outermost Layout
1. Set FormVert's top-left corner to appear at position 10,20 on the page.<br>

### Congratulations!  You've Completed Lab #1
You've successfully <br>
	• Created and set some properties of several widgets<br>
    • Parented widgets into layouts to appear on the page<br>
    • Set a layout position on the page<br>
And no doubt, you've learned to find what you need in the _Client Builder Reference Guide_<br>

_Did you get stuck?  Look into the lab.solutions package and read the code in the Lab1Client_<br>

-----------------------------------
### Instructions for Lab 2:

This lab starts where you left off in Lab 1.  If your Lab 1 is not in the state you'd like, you can duplicate the Lab1ClientSolution in the lab.solutions package and start from there.

#### Step 1: Write Event Handlers 
1. Client Start event handler, where all your other code is, create an event handler for when someone clicks the _closeBtn_.  It should close the Client.  _Hint:  Look up client.terminate()_<br>
<br>
2. Write another event handler for when someone clicks on a row in _visTable_, that opens the _RowDets_ page as a pop-up. <br>
	• This won't be an onClick handler - look up what would work for DataTables<br>
    • The _RowDets_ page should be a popup. Look up _client.popupPage()_<br>
    • Pass the selectedRowObject to the popup page<br>
<br>
#### Step 2: Create a Datastream
1. Within a "onClick" event handler for the _refreshBtn_, set up and create a TimedQueryParameters instance to query the _com.acme.VisitorRecords_Small_ type every 10 seconds.<br>
2. Create a TimedQueryDataStream using the parameters, still in the "click" handler.<br>
3. At the end of the "onClick" event, we should make the _refreshBtn_ disappear, because now that the timed query is set in motion, it doesn't need to be done again.<br>

#### Step 3:  Ensure that Datastream Messages Display in the DataTable
1. Set the dataStreamUUID of _visTbl_ to the uuid of the Datastream, which is binding the DataTable display to messages in the stream. _Hint: This has to be done in the _refreshBtn_ "onClick" handler_<br>
2. Set the columnDescriptors for _visTbl_ to match the first and last names of visitors in the _com.acme.VisitorRecords_Small_ standard type.  _Hint:  No need to do this in the _refreshBtn_ event handler!_<br>

#### Step 4: Run the Completed Client Application
Now for the moment of truth!<br>
1. Put the Client into Run Mode.<br>
2. Click the Refresh Table button.  You should see:<br>
	• The DataTable now has rows of first and last names <br>
    • The Refresh Table button has disappeared. (The Close button will by default stretch across the space now.) <br>
3. Click on a row in the DataTable. 
	• A popup page should appear, with the same first and lastname, as well as a picture, phone and email information.
    • When you close the popup page and click a new row, you should see the popup page return with new data.
4. Close the popup page.
5. Click on the Close button to stop the Client.

### Congratulations!  You've Completed Lab #2!!!
You've successfully <br>
	• Written a few event handlers for dynamic widgets.<br>
    • Created a datastream.<br>
    • Used that datastream to bind to a dynamic DataTable display.<br>

_Did you get stuck?  Look into the lab.solutions package and read the code in the Lab2Client_<br>