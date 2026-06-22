# Client Builder Tutorial
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunClient](../assets/img/client/TutRunClient2.png "Run Client")

## Objectives
Upon completion of this tutorial, a new developer will be able to:

* Create a new Client
* Place and configure widgets, either stand-alone or based on data types
* Add event-based functionality to widgets

## Tutorial Overview
This tutorial creates a simple invoicing application which allows a user to enter sales information into a form. The last five transactions will dynamically appear in a table. A gauge will also keep track of the sum of the last five transactions. The basic steps to do this are:

- Create a new project
- Create data types to keep and use sales information
- Build widgets on a new Client, based on the data types already established
- Add Javascript-coded functionality to widgets within the Client

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

All lessons assume the developer has a working knowledge of the [Vantiq IDE](../../../..). It is recommended that a new developer completes the lessons in the [Introductory Tutorial](tutorial.md) before starting the lessons in this tutorial.

>Note: if needed, you can import a finished version of this project using the _Projects -> Import_ menu item. Just select _Tutorials_ for Import Type, then select _Client Builder_ from the second drop-down, then click _Import_.

## 1: Creating a Client Builder Project
The first task is to create a project in the IDE to assemble all the Client components.

Use the **Projects** button, select **New Project**, which displays the New Project Wizard. Either create a new Namespace (recommended) or add a new project to the current Namespace, select **Empty** as the Project type, and title the project "Invoice":

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ClientProject](../assets/img/intro/EMProject.png "Create Client Project")

The rest of the lessons take place inside this Project.

## 2: Creating a Data Type
The invoice Client needs to store invoice data input by the user in the Vantiq system. You must create a data type to specify that data.

Use the **Add** button to select **Type...**:

![BlankTypeScreen](../assets/img/intro/128_IntroTut_BlackTypeScreen.png)

Use the **New Type** button to create the invoice data type:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![CreateInvoice](../assets/img/client/TutCreateInvoice1.PNG "Create Invoice Type")

Use the resulting popup to name your type "Invoice". The description is optional, but you must leave the role as standard. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![CreateInvoice](../assets/img/client/TutCreateInvoice2.PNG "Create Invoice Type")

The _Invoice_ type contains six properties:

* amount: a required Real number which is the total amount of the invoice
* description: an (optional) String property to describe what is being purchased
* firstName: an (optional) String property which holds the first name of the purchaser
* ID: a required unique String property which is used to reference the invoice
* lastName: a required String property which holds the last name of the purchaser
* timestamp: a DateTime property which holds the date and time that the invoice is submitted


The invoice Client creates the _ID_ and _timestamp_ properties using Javascript. The user of the invoice Client will manually enter all other properties.

Once the six properties are defined, save the _Invoice_ type, then save the project.

## 3: Creating the Invoice Client
This lesson uses the IDE's Client Builder feature to create our invoice Client.

Use the **Add** button to select **Client...**, then use the **New Client** button to display the New Client dialog:

![NewClientDialog](../assets/img/cbuser/NewClientDialog.png)

Enter "Invoice" as the Client Name and select the _BrowserEmpty_ Client Template since we'll be running our Client in a browser. Use the **OK** button to display the Client Builder:

![NewCB](../assets/img/client/NewCB.png "New Client Builder") 

The rest of this tutorial takes place inside this Client Builder.
    
## 4: Creating the Client Invoice Form
The next task is to create the invoice data entry form for user input. This is multi-step process and demonstrates concepts of the Client Builder common to many Clients.

First, we'll need to create a new Data Object for the Client. Data Objects define Javascript variables that are referenced by the Client. In this Client, we need to define one Data Object which is used to hold the invoice properties (firstName, lastName, etc.) that the user enters. To create a new Data Object, click the **Edit** tab of the Control Dock (on the left side of the Client pane), open the **Data Objects** tree control, then click **Page 'Start' Data Object (page.data.*)** to open the _Editing Data Object_ dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![DataObjects](../assets/img/client/TutDataObjects.png "Create Data Object")

Use the **Add a 'Typed Object'** button to add the new _Invoice_ property to the list of Data Objects. By creating the _Invoice_ property, any Javascript may now reference the _Invoice_ variable using the following syntax: _page.data.Invoice_. (_page.data_ is the Client's syntax prefix to reference the data object associated with the Client.)

Second, we'll use the Client Builder to automatically create a data entry form based on the _Invoice_ properties. Use the **Generate Widgets** icon, which is an **Actions** choice and looks like a small lightning bolt. The Generate Widgets process creates a contained form with labeled data entry widgets.

Use the **Save and Exit** button to save the new _Invoice_ Data Object.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![InvoiceForm](../assets/img/client/TutInvoiceForm.png "Create Invoice Form")

Third, we'll edit the data entry form to make it a little more user-friendly. Since we'll use be using Javascript later to generate the invoice _ID_ and _timestamp_ properties, delete those widgets from the Client display. Select the _timestamp_ title widget, then use the **Delete** button just above the palette of widgets to delete the title. In the same manner, select and delete the _timestamp_ data entry widget, the _ID_ title widget, and the _ID_ data entry widget. 

Next, change the titles of the remaining widgets. To change the title of the _amount_ widget, select it, then edit the _Text_ property in the _Specific_ menu to "Amount". In the same manner, change the titles of the _description_, _firstName_, and _lastName_ title widgets to "Description", "First Name" and "Last Name". 

Finally, drag and drop the _Last Name_ title widget and its data entry widget so they are directly under the _First Name_ widgets. The data entry form should now look like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![InvoiceFormEdit](../assets/img/client/TutInvoiceFormEdit.png "Create Invoice Form Edited")

Fourth, add a button to the form to submit the invoice data. To add the **Submit** button, click the **Edit** tab of the Control Dock then drag the **Inline** widget palette tile (under _Buttons_) and drop it just under the _Last Name_ title in the form. By default, the button is titled 'Click Me'. Click the 'Click Me' button to display its property sheet:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SubmitButton](../assets/img/client/TutSubmitButton.png "Create Submit Button")

Change the _Button Label_ field in **Specific** property category to "Submit". Next, select the **Event** property category then click the **<None\>** field titled _On Click_ to display the 'Edit Javascript' dock:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SubmitJavascript](../assets/img/client/TutSubmitJavascript.png "Submit Javascript")

This editor is where we enter Javascript that is executed whenever the user clicks the **Submit** button. For our invoice Client, we want to generate values for the _ID_ and _timestamp_ properties, validate some user-provided invoice properties, and submit the invoice data to the Vantiq system:

```js
	// generateUUID is used to create a unique ID to use as the invoice ID
	generateUUID = function() {
        // http://www.ietf.org/rfc/rfc4122.txt
        var s = [];
        var hexDigits = "0123456789abcdef";
        for (var i = 0; i < 36; i++)
        {
            s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
        }
        s[14] = "4";  // bits 12-15 of the time_hi_and_version field to 0010
        s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);  // bits 6-7 of the clock_seq_hi_and_reserved to 01
        s[8] = s[13] = s[18] = s[23] = "-";

        var uuid = s.join("");
        return uuid;
    };

	if (!page.data.Invoice.lastName || (page.data.Invoice.amount === 0)) {
        client.errorDialog("Please enter Last Name and Amount values!");
    } else {
        // programatically generate a timestamp and ID for our invoice
        page.data.Invoice.timestamp = new Date().toISOString();
        page.data.Invoice.ID = generateUUID();

        // create a Vantiq database connection to insert our new invoice
        var http = new Http();
        http.setVantiqUrlForResource("Invoice");
        http.setVantiqHeaders();
        http.insert(page.data.Invoice, null, function(response) {
            client.infoDialog("Invoice " + page.data.Invoice.ID + " submitted.");            
        }, function(errors) {
            client.errorDialog("Submit fails: " + JSON.stringify(errors));
        });
    }
```

Copy the lines of code above and paste them between the curly braces within the ..._onClick_ function. Now, when the user clicks the **Submit** button after entering invoice data on our form, the program will do the following:

* First, check that the user entered at least the Last Name and Amount on the form, generating an error message and terminating further action if not
* Next, populate the _timestamp_ property for the current Invoice by generating a timestamp and converting it to a string
* Likewise, populate the transaction _ID_ property for the current Invoice by calling the function _generateUUID_ (which is defined in the first part of the code) to return a large randomized number formated as a string with dashes 
* Connect to the Vantiq database to insert the entire record, both from the user's input on the form and from what the code generated
* If the insert succeeds, create an _Info_ pop-up to confirm; in the case of failure, an _Error_ pop-up alerts the user

Use the **Save** button to save the code.

Fifth, add a button to the form to reset the invoice data. To add the **Reset Form** button, drag the **Inline** widget palette tile and drop it to the right of the **Submit** button. Click the new 'Click Me' button to display its property sheet:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SubmitButton](../assets/img/client/TutResetButton.png "Create Reset Button")

Change the _Button Label_ field to "Reset Form". Next, select the **Event** property category then click the **<None\>** field titled _On Click_ to display the 'Edit Javascript' dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SubmitJavascript](../assets/img/client/TutResetJavascript.png "Submit Javascript")

This editor is where we enter Javascript that is executed whenever the user clicks the **Reset Form** button. For our invoice Client, we want to return the data field in the form to blank:

```js
	page.data.Invoice.firstName = page.data.Invoice.lastName = page.data.Invoice.description = "";
	page.data.Invoice.amount = null;
```

Just as before, copy and paste the code above to between the function curly braces, and use the **Save** button to save the Javascript.

The data entry form should now look like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![InvoiceFormEdit](../assets/img/client/TutInvoiceFormEdit2.png "Create Invoice Form Edited")

Save the Client and the Project, then run the Client by clicking the small triangle that looks like a small **Play** button at the top right corner of the Client. Input some data in the fields and see for yourself how the Client behaves. When you're finished, you can return to edit the Client by clicking the same button again, which now looks like a small square within a square.

## 5: Creating a Recent Invoices Table
The next task is to create a table that displays the last five entered invoices. This is a two step process: (1) creating a Data Stream which is used to retrieve invoice data and (2) creating a table to display the data.

First, create a Data Stream. Click the **Edit** tab of the Control Dock then right-click on the **Data Streams** tree control, then select **Add 'Timed Query'** from the menu to create the new Data Stream:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![InvoiceDataModel](../assets/img/client/TutInvoiceDataModel.png "Create Invoice Data Stream")

Title the Data Stream "Invoice Queryable". A Timed Query Data Stream means that the Client will retrieve data from the Vantiq database on a periodic basis. Select _Invoice_ as the 'Data Type' since we want to retrieve invoice data. Enter 15 as the 'Update Interval' to retrieve the invoice data every 15 seconds. Since the goal is to create a table that displays the last five entered invoices, enable the **Limit maximum number of records to return** and enter '5'. Then select _timestamp_ as the 'Sort By' property (since we want to sort by when the invoice was created) and, finally, enable **Sort Descending** so the top entry in the table will be the most recent invoice. Use the **Save** button to save the Data Stream.

Second, create a table to hold the recent invoice data. To add the table, click the **Add** tab of the Control Dock then drag the **Table** widget palette tile (under _Data Display_) and drop it to the right of the data entry form. Click the new table to display its property sheet:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Table](../assets/img/client/TutTable.png "Create Table")

Select the **Data** property category then use the **Data Stream** pull-down menu to select _Invoice Queryable_, our recently created Data Stream. Use the **Columns** property to display the 'Edit Columns' dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ConfigureTable](../assets/img/client/TutEditColumns.png "Configure Table")

Use the right arrows to add all six properties of the _Invoice_ type as table columns. If you want to change the column titles to be more human-readable, edit them by using the pencil icon for each column, then **Save**. Use the **OK** button to save the column configuration.

Finally, check **Clear on Data Arrival** so the table only displays the latest result from the Timed Query. Uncheck **Show Paging** to hide the paging buttons since the table will always be a fixed size.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ConfigureTable](../assets/img/client/TutTableProp.png "Configure Table Display")

Save the Client and the Project. Try running the Client again, entering data in your Invoice form and seeing the table periodically update to show the input of the last five records.
 
## 6: Creating a Recent Invoices Gauge
The next task is to create a gauge that displays the sum of the last five entered invoices. This is a four step process: (1) creating a new Data Object to hold the sum, (2) creating a new Data Stream that uses the Data Object, (3) creating the gauge to display the data and (4) adding Javascript to compute the sum.

First, create a Data Object. To create a new Data Object, click the **Edit** tab of the Control Dock (on the left side of the Client pane), open the **Data Objects** tree control, then click **Client Data Object (client.data.*)** to open the _Editing Data Object_ dialog. We select _client.data_ because our upcoming Data Stream may only reference _client.data_ Data Objects.

Use the **Add a Property** button to add the new Data Object: enter _sumLastFive_ as the Property Name, select _Typed Object_ from the **DataType** pull-down menu, and enter _sumLastFive_ as the Default Label. (Please refer to the [Client Builder User's Guide](../cbuser.md#models) for more information about Typed Objects.) The _sumLastFive_ Data Object is now present but we need to add one field to hold the actual invoice sum. Use the **Edit Typed Object** icon, which is found under the **Actions** menu heading and looks like a small pencil:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![InvoiceDOSum](../assets/img/client/TutDOSum.png "Create Invoice Data Object")

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![InvoiceDOSumProperty](../assets/img/client/TutDOSumProperty.png "Create Invoice Data Object Property")

Use the **Add a Property** button to add the new Typed Object property: enter _value_ as the Property Name, select _Real_ from the **DataType** pull-down menu, and enter _value_ as the Default Label. The _value_ property of the _sumLastFive_ Data Object will be used to hold the sum of the recent invoices. Use the **OK** button to save the _value_ property, then use the **Save and Exit** button to save the _sumLastFive_ Data Object.

Second, create a Data Stream which is used to send data events to the gauge. To create a new Data Stream, click the **Edit** tab of the Control Dock then right-click on the **Data Streams** tree control, then select **Add 'On Client Event'** from the menu to create the new Data Stream:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![InvoiceDSSum](../assets/img/client/128_ClientBuilderTut_NewDataStream.png "Create Invoice Data Stream")

Title the Data Stream “Invoice Sum”. Select **Get schema from client.data.object** then select _client.data.sumLastFive_ from the **Data Object** pull-down menu. This data stream now references the _sumLastFive_ Data Object we created in the previous step. Use the **Save** button to save the Data Stream.

Third, create a gauge to display the invoice sum. To add the gauge, click the **Add** tab of the Control Dock then drag the **Gauge** widget palette tile (under _Data Display_) and drop it under the invoice table. Click the new gauge to display its property sheet:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Gauge](../assets/img/client/TutGauge.png "Create Gauge")

Select the **Data** property category then use the **Data Stream** pull-down menu to select _Invoice Sum_, our recently created Data Stream. Use the **Data Stream Property** pull-down men to select _value_. Since we're anticipating high-value invoices, select the **Specific** property category then enter the following property values:
```text
 Low Range Zones: 0:700
 Medium Range Zones 700:900
 High Range: 900:1000
 Maximum: 1000
```
Fourth, we will modify our submit Javascript to sum the recent invoices, then send the Client Event to update the Data Stream. Click the **Submit** button in the data entry form. Next, click the **Click to Edit** field titled _On Click_ to display the 'Edit Javascript' dialog.

Here is the modified Javascript which includes summing the recent invoice values and sending the Client event to the _Invoice Sum_ Data Stream:

```js
	// generateUUID is used to create a unique ID to use as the invoice ID
    generateUUID = function() {
        // http://www.ietf.org/rfc/rfc4122.txt
        var s = [];
        var hexDigits = "0123456789abcdef";
        for (var i = 0; i < 36; i++)
        {
            s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
        }
        s[14] = "4";  // bits 12-15 of the time_hi_and_version field to 0010
        s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1);  // bits 6-7 of the clock_seq_hi_and_reserved to 01
        s[8] = s[13] = s[18] = s[23] = "-";

        var uuid = s.join("");
        return uuid;
    };

    if (!page.data.Invoice.lastName || (page.data.Invoice.amount === 0)) {
        client.errorDialog("Please enter Last Name and Amount values!");
    } else {
        // programatically generate a timestamp and ID for our invoice
        page.data.Invoice.timestamp = new Date().toISOString();
        page.data.Invoice.ID = generateUUID();

        // create a Vantiq database connection to insert our new invoice
        var http = new Http();
        http.setVantiqUrlForResource("Invoice");
        http.setVantiqHeaders();
        http.insert(page.data.Invoice.values, null, function(response) {
            // the invoice was saved, now query for the last five invoices based on timestamp
            client.infoDialog("Invoice " + page.data.Invoice.ID + " submitted.");
            var parameters = {
                "limit":5,
                "sort":{"timestamp":-1}
            };
            http.select(parameters, function(response) {
                // sum the amounts of the last five invoices
                client.data.sumLastFive.value = 0;
                for (var i = 0; i < response.length; i++) {
                    client.data.sumLastFive.value += response[i].amount;
                }
                // create a client event for widgets listening on the Invoice Sum data stream
                client.sendClientEvent("Invoice Sum", client.data.sumLastFive);
            }, function(errors) {
                client.errorDialog("Select fails: " + JSON.stringify(errors));
            });
        }, function(errors) {
            client.errorDialog("Submit fails: " + JSON.stringify(errors));
        });
    }
```

It's simplest to copy all of the above and replace the previous event code for the button. You will notice that most of the code from before is still here, but some new functionality has been added:

* After submitting the latest invoice record to the database, a SELECT operation is queried against the database to collect and sum the value amounts from the last five transactions
* The code then triggers an Event for the _Invoice Sum_ data stream, which we created earlier, sending the lastSumFive data out to the stream
* The user is notified in the event of errors in connecting to the database, either in the insertion (as was the case before) or selection of data

Use the **Save** button after adding the modifications to save the Javascript.

Our simple invoice Client is complete and should look like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![FinalClient](../assets/img/client/TutRunClient.png "Final Client")

## 7: Running the Client
The last lesson of this tutorial is to run the Client, entering sample invoices and watching the invoice table update. Use the **Run** icon button of the _Client: Invoice_ pane (small triangle in a square at the top, right of the pane):

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunClient](../assets/img/client/TutRunClient.png "Run Client")

To create a new invoice, add values to the _Amount_, _Description_, _First Name_, and _Last Name_ fields, then use the **Submit** button to submit the invoice. After entering several invoices, the Client display will look similar to this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunClient](../assets/img/client/TutRunClient2.png "Run Client")

Use the **Stop Running** icon button of the _Client: Invoice_ pane (small square in a square at the top, right of the pane) to end the Client session.

# Conclusion
Users who have successfully completed this tutorial should now be able to confidently:

* Create new Clients and arrange widgets in the workspace
* Create and edit forms based on datatypes
* Set up Data Objects, both based on datatypes and independently
* Establish Data Streams and configure widgets to interact with the data
* Know where Javascript code can be inserted for widget events

More information on Clients can be found in the [Client Builder User's Guide](../cbuser.md) and the [Client Builder Reference Guide](../cbref.md), where there is also more detail on HTTP requests to the Vantiq database.

