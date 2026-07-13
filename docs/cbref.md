# Client Builder Reference Guide

This is a "Reference Guide" for the classes that make up the Client Builder API. The User's Guide may be found [here](cbuser.md).


## Client

This section describes the functions and properties of the "Client" object. There is always a single "Client" object available that represents the running Client; it is usually accessible through the "client" argument to event handlers.

### a2aMessageSend()
#### Send a message in Agent2Agent protocol to an Agent

```js
a2aMessageSend(agentName:string,msg:A2AMessage,options:any=null):Promise
```

This method provides a way to send a message to an Agent using the [Agent2Agent (A2A) Protocol](https://a2a-protocol.org).

* agentName:string - The full name of the Agent (Service) to which the message should be sent
* msg:A2AMessage - An object in the [A2AMessage](https://a2a-protocol.org/latest/topics/key-concepts) format that contains the message to be sent.
* options:any - Extra options to be added to the payload

The method returns a Promise since the results are returned asynchronously. Here is an example of using this method:

```js 
  let userMsg = "What is the capital of California?";
  let options = null;
  
  let message = new A2AMessage();
  message.parts.push(new A2ATextPart(userMsg));
  
  console.log("Message=" + userMsg);
  
  client.a2aMessageSend("com.vantiq.MyAgent",message,options).then(
          function(response)
          {
            //
            //  Response from the Agent
            //
            console.log("RESPONSE:" + JSON.stringify(response,null,3));
          },
          function(error)
          {
            console.error("ERROR:" + JSON.stringify(error,null,3));
          }
);
```



### a2aMessageStream()
#### Send a message in Agent2Agent protocol to an Agent and stream the results

```js
a2aMessageStream(agentName:string,msg:A2AMessage,options:any=null,inProgressCallback:Function=null):Promise
```

This method provides a way to send a message to an Agent using the [Agent2Agent (A2A) Protocol](https://a2a-protocol.org). Receives intermediate "streaming" results if the Agent supports it.

* agentName:string - The full name of the Agent (Service) to which the message should be sent
* msg:A2AMessage - An object in the [A2AMessage](https://a2a-protocol.org/latest/topics/key-concepts) format that contains the message to be sent.
* options:any - Extra options to be added to the payload
* inProgressCallback:Function - An optional callback function that receives the results

The method returns a Promise since the results are returned asynchronously. Here is an example of using this method:

```js 
  let userMsg = "What is the capital of California?";
  let options = null;
  
  let message = new A2AMessage();
  message.parts.push(new A2ATextPart(userMsg));
  
  console.log("Message=" + userMsg);
  
  client.a2aMessageStream("com.vantiq.MyStreamingAgent",message,options,function(progress)
  {
    //
    //  Intermediate "progress" messages provided by the Agent
    //
    console.log("PROGRESS:" + JSON.stringify(progress,null,3));
  }).then(
          function(response)
          {
            //
            //  Final response from the Agent
            //
            console.log("RESPONSE:" + JSON.stringify(response,null,3));
          },
          function(error)
          {
            console.error("ERROR:" + JSON.stringify(error,null,3));
          }
  );
);
```

### abort()
#### Abort the Client after trapping an exception

```js
abort(ex:any):string
```

* ex:any - The Exception from a try/catch block




### blockInput()
#### Make the Client temporarily 'modal' by blocking all Client input

```js
blockInput(key:string,title:string):void
```

* key: string - The unique 'key' for this block operation; must be supplied to the matching [client.blockInputCompleted('key')](#blockinputcompleted) call
* title:string - The text that will be displayed to user while the block is active

This function provides a way to block all user input temporarily, making the Client effectively "modal". During the block the user sees some text and a spinner, with the Client obscured by a translucent 'veil'. The intent is to allow you prevent any further user input while some long-running operation is in progress. At some point, whether the operation succeeds or fails, you need to invoke a matching  [client.blockInputCompleted('key')](#blockinputcompleted) call to remove the block.

See [client.blockInputEx()](#blockinputex) for a version of this feature which allows more detailed control. 

This example shows a simple block. (Note that the 'setTimeout' is used to simulate your long-running operation.)

```js
//
//  Example of a simple "block" while some long-running operation is in progress
//
client.blockInput("Simple","Simple Wait in Progress...");

client.setTimeout(function()
{
    client.blockInputCompleted("Simple");
},1000);
```

### blockInputCompleted()
#### Remove a previous modal block placed by client.blockInput()

```js
blockInputCompleted(key:string):void
```

* key: string - The unique 'key' for this block operation; must match the one supplied by a previous call to [client.blockInput()](#blockinput)

This function provides a way to remove a block set by a previous call to [client.blockInput()](#blockinput).




### blockInputEx()
#### Make the Client temporarily 'modal' by blocking all Client input, allowing more options than blockInput

```js
blockInputEx(blockDesc:BlockDescriptor):void
```

* blockDesc: BlockDescriptor - A BlockDescriptor object whose properties allow greater control of the block operation

Like [client.blockInput()](#blockinput) this function provides a way to block all user input temporarily, making the Client effectively "modal". During the block the user sees some text and a spinner, with the Client obscured by a translucent 'veil'. It is more complicated to use than [client.blockInput()](#blockinput) but provides more detailed control of the block that the user sees. 

The BlockDescriptor object has these properties:

```js
class BlockDescriptor
{
    
    delayMS:number;     // Delay in MS until the block takes effect (default = 0)
    title:string;       // Title seen by the user during the block (required)
    subTitle:string;    // Subtitle seen by the user during the block (optional)
    opacity:number;     // Opacity of the "veil" over the blocked Client (default = .5)
    spinner:string;     // Document name containing GIF to show instead of built-in spinner (default = null)
}
```


This example shows a block that has multiple phases where you want to show a "title" and a "subTitle" that can change during the course of the block. (Note that the 'setTimeout' is used to simulate your long-running operation.)


```js  
var block = new BlockDescriptor();
block.title = "Phase One...";
block.subTitle = "Reason One";
block.delayMS = 100;   

client.blockInputEx(block);

client.setTimeout(function()
{
   block.title = "Phase Two...";    // Change the title
   block.subTitle = "Reason Two";   // Change the subTitle

   client.setTimeout(function()
   {
       block.completed();
   },1000);

},1000);

```


Here is a more complex example where there are 2 blocks, with one block nested inside another.

```js  
var outerBlock = new BlockDescriptor();
outerBlock.title = "Blocking Outer Level...";
outerBlock.subTitle = "The Outer Reason";
outerBlock.delayMS = 50;

client.blockInputEx(outerBlock); // Start the "outer" block

client.setTimeout(function()
{
   var innerBlock = new BlockDescriptor();
   innerBlock.title = "Blocking Inner Level...";
   innerBlock.subTitle = "The Inner Reason";
   innerBlock.spinner = "spinner.gif";   //    Your own spinner gif Document

   client.blockInputEx(innerBlock);  // Start the "inner" block

   client.setTimeout(function()
   {
       innerBlock.completed();

       client.setTimeout(function()
       {
           outerBlock.completed(); 
       },1000;

   },1000);

},1000);

```







### cancelSpeaking()
#### Stop the current 'speakText' audio

```js
cancelSpeaking():void
```

Abort the current [speakText()](#speakText) audio clip if there is one in progress. This is a NOP if there is no speech active.



### clearInterval()
#### Cancel a repeating system timer previously created by client.setInterval

```js
clearInterval(handle:number):void
```

* handle: number - The handle of the timer to be canceled (this is the value returned by a previous call to client.setInterval)


This function is used in exactly the same manner as the well-known window.clearInterval() function provided by the 
JavaScript runtime system. It should be used to cancel timers created with the client.setInterval() function.

Note that any outstanding interval timers that are not explicitly canceled will be canceled automatically when the 
Client completes execution. Timers which are created using the system function window.setInterval will **not** be 
canceled automatically, which is why you should use the client.setInterval function instead.

For example:

```js
//
//  Example of a 60-second interval timer
//
var theHandle = client.setInterval(function(a,b)
    {
        console.log("My Interval Timeout: " + a + " " + b);
    },60000,123,456);


...
...

client.clearInterval(theHandle);

```


### clearTimeout()
#### Cancel a one-time system timer event previously created by client.setTimeout

```js
clearTimeout(handle:number):void
```

* handle: number - The handle of the timer to be canceled (this is the value returned by a previous call to client.setTimeout)

This function is used in exactly the same manner as the well-known window.clearTimeout() function provided by the 
JavaScript runtime system. It should be used to cancel timers created with the client.setTimeout() function.

Note that any outstanding un-expired timers that are not explicitly canceled will be canceled automatically when the 
Client completes execution. Outstanding timers which are created using the system function window.setTimeout will **not** be 
canceled automatically, which is why you should use the client.setTimeout function instead.

For example:

```js
//
//  Example of a 60-second one-time timer
//
var theHandle = client.setTimeout(function(a,b)
    {
        console.log("My Timeout: " + a + " " + b);
    },60000,123,456);


...
...

client.clearTimeout(theHandle);

```


### clone()
#### A helper function to make 'clones' of the supplied item

```js
clone(thing: any): any
```

* thing:any - this can be various kinds of values:

    * Any type of JavaScript value such as an object, scalar or null.
    
    * A DataObject (you will get a usable DataObject back).
    
    * A Widget (you will get a duplicate Widget back which could be added to a Page)




### closePopup()
#### Dismiss the currently open popup dialog created with client.popupPage()

```js
closePopup(parameters: any): void
```

* parameters:any - (optional) A data item that will be passed back to the completion callback function supplied in the [client.popupPage()](#popuppage) call.

The popup will be dismissed and the caller's completion callback function will be called (if there was one).

This function can throw an exception in some situations, such as if there is no open popup to close.



### confirmCustom()
#### Pop up a "Confirmation" Dialog prompting the user to make a choice

Pop up a dialog which offers 1 or 2 choices plus a "Cancel" button.

```js
confirmCustom(msg: string, choice1Label: string, choice2Label: string, callback: Function)
```

* msg: string - The text to be displayed in the popup.
* choice1Label: string - The label of the second button in the dialog. If "null" then there will be no button shown.
* choice2Label: string - The label of the third button in the dialog. If "null" then there will be no button shown.
* callback: string - A callback which will be called when a button is clicked. The function has a single argument containing the label of the clicked button or "Cancel";

The dialog is modal; the user must click one of the buttons to dismiss it (at which point the callback function will be called). The string parameters may be supplied as "localization keys" instead of literal text (See [here](cbuser.md#localizing-clients) for a complete discussion of the Client localization process.)

There will always be a "Cancel" button shown; the buttons are shown in the order "cancel", "yes", "no". The "cancel" button has a slightly different appearance which makes it look different from "yes" and "no".

Here is an example showing how confirmCustom() might be used:
 
```js
//
//  Pop-up a "confirmation" Dialog that offers one, two or three "choice" buttons. The first button
//  will always be "Cancel", and either (or both) of the second and third parameters may be "null". In 
//  this example the user will see "Cancel", "Yes", and "No".
//
//  The callback function is driven when the user makes a choice; the function has a single parameter
//  with the text of the selected button or "Cancel".
//
client.confirmCustom("Ask the user to make a choice","Yes","No",function(clicked)
{
    //
    //  "clicked" will have a value of "Yes", "No" or "Cancel" depending on which 
    //  button in the dialog was clicked.
    //
    console.log(clicked);
});
```


### confirmCustomEx()
#### Pop up a "Confirmation" Dialog prompting the user to make a choice

Pop up a confirmation dialog which offers up to 3 choices. This is an extended version of confirmCustom() which provides more control and whose numeric return value makes localization easier. 

```js
confirmCustomEx(title: string, msg: string, cancelLabel: string, yesLabel: string, noLabel: string,  callback: Function)
```

* title: string - The title to be displayed for the popup. If "null" is specified the title will default to "Confirm".
* msg: string - The text to be displayed in the popup.
* cancelLabel: string - The label of the first button in the dialog ("cancel"). If "null" then there will be no button shown.
* yesLabel: string - The label of the second button in the dialog ("yes"). If "null" then there will be no button shown.
* noLabel: string - The label of the third button in the dialog ("no"). If "null" then there will be no button shown.
* callback: string - A callback which will be called when a button is clicked. The function has a single argument containing a number that indicates which button was clicked (Client.CONFIRM_CANCEL, Client.CONFIRM_YES or Client.CONFIRM_NO)

The dialog is modal; the user must click one of the buttons to dismiss it (at which point the callback function will be called). The string parameters may be supplied as "localization keys" instead of literal text (See [here](cbuser.md#localizing-clients) for a complete discussion of the Client localization process.)

The buttons are shown in the order "cancel", "yes", "no". The "cancel" button has a slightly different appearance which makes it look different from "yes" and "no".

Here is an example showing how confirmCustomEx() might be used:
 
```js
//
//  Pop-up a "confirmation" Dialog that offers one, two or three "choice" buttons. Any button is optional but you
//  must specify at least one.
//
//  The callback function is driven when the user makes a choice; the function has a single parameter which 
//  indicates which button was clicked.
//
client.confirmCustomEx("My Title", "Ask the user to make a choice", "Cancel", "Yes", "No", function(clicked)
{
    //
    //  "clicked" will have a value of Client.CONFIRM_CANCEL, Client.CONFIRM_YES or Client.CONFIRM_NO depending on 
    //  which button in the dialog was clicked.
    //
    console.log(clicked);
});
```

### createClientEventDataStream()
#### Dynamically create a "Client Event" DataStream at runtime

```js
createClientEventDataStream(parameters:ClientEventParameters):DataStream
```

* parameters:ClientEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to create.

The properties of the ClientEventParameters object should be set to indicate the parameters of the DataStream you wish to create:

```
class ClientEventParameters
{
    public typeName:string;         
    public dataObjectName:string;   
    public groupBy:string;
}
```

* typeName: The name of a Type which describes the data associated with the Client Event.

* dataObjectName: The name of a DataObject which describes the data associated with the Client Event.

* groupBy:string: The name of the "groupBy" property within the Type or DataObject.

You may set either 'typeName' or 'dataObjectName' but not both.

For example, inside an event handler you might dynamically create a "Client Event" DataStream like this:

```js
	var p = new ClientEventParameters();

	p.typeName = "MyType";

	var ds = client.createClientEventDataStream(p);
```

Note that a unique name for the DataStream will be automatically generated (of the form "DynamicDataStreamNNNNN"). You may access this name (or the DataStream's UUID) using "ds.name" and "ds.uuid")

You may add an "onDataArrived" event handler using the DataStream's [addEventHandler()](#addeventhandler) method.

### createDataChangedDataStream()
#### Dynamically create a "Data Changed" DataStream at runtime

```js
createDataChangedDataStream(parameters:DataChangedParameters):DataStream
```

* parameters:DataChangedParameters - A special object (described below) that contains the parameters of the DataStream you wish to create.

The properties of the DataChangedParameters object should be set to indicate the parameters of the DataStream you wish to create:

```
class DataChangedParameters
{
    public typeName:string;
    public isInsert:boolean;
    public isUpdate:boolean;
    public isDelete:boolean;
    public groupBy:string;
    public eventFilter:any;
}
```

* typeName: The name of a Type which is to be monitored for changes.

* isInsert: Set to "true" if you wish to be notified of "inserts" on the Type.

* isUpdate: Set to "true" if you wish to be notified of "updates" on the Type.

* isDelete: Set to "true" if you wish to be notified of "deletes" on the Type.

* groupBy:string: The name of the "groupBy" property within the Type (may be null).

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).

You may listen for any combination of "inserts", "updates" and "deletes".


For example, inside an event handler you might dynamically create a "Data Changed" DataStream like this:

```js
	var p = new DataChangedParameters();

	p.typeName = "SomeType";
    p.isInsert = true;
    p.isUpdate = true;

	var ds = client.createDataChangedDataStream(p);
```

If the createDataChangedDataStream() is successful you will be subscribed for "insert" and "update" changes on "SomeType".

Note that a unique name for the DataStream will be automatically generated (of the form "DynamicDataStreamNNNNN"). You may access this name (or the DataStream's UUID) using "ds.name" and "ds.uuid")


You may add an "onDataArrived" event handler using the DataStream's [addEventHandler()](#addeventhandler) method.




### createPagedQueryDataStream()
#### Dynamically create a "Paged Query" DataStream at runtime

```js
createPagedQueryDataStream(parameters:PagedQueryParameters):DataStream
```

* parameters:PagedQueryParameters - A special object (described below) that contains the parameters of the DataStream you wish to create.

The properties of the PagedQueryParameters object should be set to indicate the parameters of the DataStream you wish to create:

```
class PagedQueryParameters
{
    public typeName:string;
    public sortByPropertyName:string;
    public sortDescending:boolean;
    public whereClause:object;
}
```

* typeName: The name of the Vantiq Type to be queried.

* sortByPropertyName: The name of a property by which the results should be sorted.

* sortDescending: "true" if you which the sort to be done in ascending order ("false"/ascending is the default).

* whereClause: An object containing the "where" clause for the query. (For details on constructing this object you can consult the [API Reference Guide](api.md#where-parameter))

For example, inside an event handler you might dynamically create a Paged Query DataStream like this:

```js
	var p = new PagedQueryParameters();

	p.whereClause = {
        salary: {
            "$gte": 100000
        }
    };

	var ds = client.createPagedQueryDataStream(p);
	
	//
    //  This type of DataStream is usually bound to a DataTable which could be done like this
    //
    var theDataTable = client.getWidget("MyDataTable");
    theDataTable.dataStreamUUID = ds.uuid;

```

If the createPagedQueryDataStream() is successful the new query will be re-run immediately and the DataTable reset to the first page.

Note that a unique name for the DataStream will be automatically generated (of the form "DynamicDataStreamNNNNN"). You may access this name (or the DataStream's UUID) using "ds.name" and "ds.uuid")


You may add an "onDataArrived" event handler using the DataStream's [addEventHandler()](#addeventhandler) method.


### createPublishEventDataStream()
#### Dynamically create a "Publish Event" DataStream at runtime

```js
createPublishEventDataStream(parameters:PublishEventParameters):DataStream
```

* parameters:PublishEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to create.

The properties of the PublishEventParameters object should be set to indicate the parameters of the DataStream you wish to create:

```
class PublishEventParameters
{
    public topic:string;
    public groupBy:string;
    public eventFilter:any;
}
```

* topic: The topic name you wish to listen for.

* groupBy:string: The name of the "groupBy" property within the message object (may be null).

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).


For example, inside an event handler you might dynamically create a "Publish Event" DataStream like this:

```js
	var p = new PublishEventParameters();

	p.topic = "/my/new/topicname";

    var ds = client.createPublishEventDataStream(p);
```


Note that a unique name for the DataStream will be automatically generated (of the form "DynamicDataStreamNNNNN"). You may access this name (or the DataStream's UUID) using "ds.name" and "ds.uuid")

You may add an "onDataArrived" event handler using the DataStream's [addEventHandler()](#addeventhandler) method.

### createResourceEventDataStream()
#### Dynamically create a  "Resource Event" DataStream at runtime

```js
createResourceEventDataStream(parameters:ResourceEventParameters):DataStream
```

* parameters:ResourceEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to create.

The properties of the ResourceEventParameters object should be set to indicate the parameters of the DataStream you wish to create:

```
class ResourceEventParameters
{
    public eventPath:string;
    public eventFilter:any;
}
```

* eventPath: The event path that you wish to listen for.

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).


For example, inside an event handler you might dynamically create a "Source Event" DataStream like this:

```js
	var p = new ResourceEventParameters();

	p.eventPath = "/topics/my/new/event/path";

    var ds = client.createResourceEventDataStream(p);
```


Note that a unique name for the DataStream will be automatically generated (of the form "DynamicDataStreamNNNNN"). You may access this name (or the DataStream's UUID) using "ds.name" and "ds.uuid")

You may add an "onDataArrived" event handler using the DataStream's [addEventHandler()](#addeventhandler) method.

### createOutboundServiceEventDataStream()
#### Dynamically create a "Service Event" DataStream at runtime

```js
createOutboundServiceEventDataStream(parameters:ServiceEventParameters):DataStream
```

* parameters:ServiceEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to create.

The properties of the ServiceEventParameters object should be set to indicate the parameters of the DataStream you wish to create:

```
class ServiceEventParameters
{
    public service:string;
    public serviceEventName:string;
    public groupBy:string;
    public eventFilter:any;
}
```

* service: The name of the Service whose outbound event you wish to listen for.

* serviceEventName: The name of the "outbound event" of the specified Service you wish to listen for.

* groupBy:string: The name of the "groupBy" property within the message object (may be null).

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).

For example, inside an event handler you might dynamically create a "Service Event" DataStream like this:

```js
	var p = new ServiceEventParameters();

    p.service = "a.b.c.MyService";
    p.serviceEventName = "TheOutboundEventName";

    var ds = client.createOutboundServiceEventDataStream(p);
```


Note that a unique name for the DataStream will be automatically generated (of the form "DynamicDataStreamNNNNN"). You may access this name (or the DataStream's UUID) using "ds.name" and "ds.uuid")

You may add an "onDataArrived" event handler using the DataStream's [addEventHandler()](#addeventhandler) method.

### createSourceEventDataStream()
#### Dynamically create a "Source Event" DataStream at runtime


```js
createSourceEventDataStream(parameters:SourceEventParameters):DataStream
```

* parameters:SourceEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to create.

The properties of the SourceEventParameters object should be set to indicate the parameters of the DataStream you wish to create:

```
class SourceEventParameters
{
    public source:string;
    public groupBy:string;
    public eventFilter:any;
}
```

* source: The name of the Source which you wish to listen for.

* groupBy:string: The name of the "groupBy" property within the message object (may be null).

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).

For example, inside an event handler you might dynamically create a "Source Event" DataStream like this:

```js
	var p = new SourceEventParameters();

	p.source = "ADifferentSource";

    var ds = client.createSourceEventDataStream(p);
```



Note that a unique name for the DataStream will be automatically generated (of the form "DynamicDataStreamNNNNN"). You may access this name (or the DataStream's UUID) using "ds.name" and "ds.uuid")

You may add an "onDataArrived" event handler using the DataStream's [addEventHandler()](#addeventhandler) method.


### createTimedQueryDataStream()
#### Dynamically create a  "Timed Query" DataStream at runtime

```js
createTimedQueryDataStream(parameters:TimedQueryParameters):DataStream
```
* parameters:TimedQueryParameters - A special object (described below) that contains the parameters of the DataStream you wish to create.

The properties of the TimedQueryParameters object should be set to indicate the parameters of the DataStream you wish to create:

```
class TimedQueryParameters
{
    public typeName:string;
    public updateIntervalInSeconds:number;
    public groupByPropertyName:string;
    public maximumRecordsReturned:number;
    public sortByPropertyName:string;
    public sortDescending:boolean;
    public whereClause:object;
}
```

* typeName: The name of the Vantiq Type to be queried.

* updateIntervalInSeconds: The delay in seconds between queries. If this value is "0" the query will be run only once.

* groupByPropertyName: The name of the property used to filter the results; only used by certain Widgets such as the FloorplanViewer.

* maximumRecordsReturned: The maximum number of records to be returned by the query (corresponds to the "limit" option).

* sortByPropertyName: The name of a property by which the results should be sorted.

* sortDescending: "true" if you which the sort to be done in ascending order ("false"/ascending is the default).

* whereClause: An object containing the "where" clause for the query. (For details on constructing this object you can consult the [API Reference Guide](api.md#where-parameter))

For example, inside an event handler you might dynamically create a timed query DataStream like this:

```js
	var p = new TimedQueryParameters();

	p.whereClause = {
        salary: {
            "$gte": 100000
        }
    };

	var ds = client.createTimedQueryDataStream(p);
```


Note that a unique name for the DataStream will be automatically generated (of the form "DynamicDataStreamNNNNN"). You may access this name (or the DataStream's UUID) using "ds.name" and "ds.uuid")

You may add an "onDataArrived" event handler using the DataStream's [addEventHandler()](#addeventhandler) method.





### createResponseObject()
#### Create a "response object" from the contents of the current Page

```js
createResponseObject(submitValue:number):any
```

* submitValue:number - An integer which is to be added to the response object, giving the receiver some information about which button was clicked to produce the response.

This method generates a "response object" by collecting data from all the ControlWidgets on the current Page. In addition it will automatically add some properties to give context:

* responseObject - The default response topic for the current Page.
* submitValue - From the "submitValue" argument.
* values - An object containing all the values extracted from the ControlWidgets on the current Page. (The Widget names are used to set each property.)
* username - The current username.

This method returns null if the response object is not created, usually because a required ControlWidget has not been given a value.


### data
#### "client.data" refers to the "global" DataObject

```js
data: DataObject
```

You can always reach the DataObject for the Client using "client.data".


### deleteOne()
#### Convenience method to issue an asynchronous request to delete a single record from the Vantiq database

```js
deleteOne(typeName:string, resourceId:string, succeed:Function):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#deleteone_1).

* typeName:any - The name of a user-defined Type.
* resourceId:string - The "_id" of the target object.
* succeed:Function - Called when the HTTP status code is 2XX. 

If successful the "succeed" callback is called but there is nothing meaningful in the "response" object. It is important to note that the request will **not** fail if the record does not exist; in that case the request is a NOP.

If the request fails the user will see an error popup that describes what happened.


```js
    //
    //  This _id was probably obtained by a previous "select".
    //
    var theEmployeeId = "59776c4589133374df264357";
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  typeName:        The name of the Type 
    //  resourceId:      The "_id" of the object being deleted
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //
    client.deleteOne("Employee",theEmployeeId,function(response)
    {
        //
        //  The "response" object is meaningless in this case.
        //
        console.log("DELETE SUCCESSFUL");
    });
```




### errorDialog()
#### Pop up an "Error" Dialog with the supplied message.

```js
errorDialog(msg: string. title:string):void
```

* msg: string - The text to be displayed in the popup.
* title: string - The text to be displayed in the popup title bar. (optional)

The dialog is modal; the user must click "OK" to dismiss it. The parameters may be supplied as "localization keys" instead of literal text (See [here](cbuser.md#localizing-clients) for a complete discussion of the Client localization process.)


### execute()
#### Convenience method to asynchronously execute a Procedure in the Vantiq database.


```js
execute(procedureArguments:any, procedureName:string, succeed:Function):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#execute_1).

* procedureArguments:any - An object containing the arguments required by the procedure.
* procedureName:string - The name of the Procedure to execute. (If the Procedure is defined in a service you should supply the "fully qualified" form of the name, i.e. "&lt;service>.&lt;procedurename>".)
* succeed:Function - Called when the HTTP status code is 2XX. 

If successful the "succeed" callback returns the "return" value of the procedure "response". 


If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  Set the Procedure arguments by name. (You may also specify 'args' as an array where the
    //  parameters are given in the same order as in the Procedure definition (e.g. 'args = [10,20];').
    //  'args' must not be null.
    //
    var args = {
        a:1,
        b:2
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  procedureArguments: The procedure arguments.
    //  procedureName:      The fully-qualified name of the Procedure.
    //  successCallback:    A callback function that will be driven when the request completes
    //                      successfully (i.e. a status code of 2XX)
    //
    client.execute(args,"MyService.MyProcedure",function(response)
    {
        //
        //  At this point "response" is results of the Procedure call
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    });
```



### executePublic()
#### Convenience method to asynchronously execute a public Procedure in another namespace.


```js
executePublic(namespace:string, procedureArguments:any, procedureName:string, succeed:Function):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#executepublic_1).

* namespace:string - The namespace where the public Procedure resides
* procedureArguments:any - An object containing the arguments required by the procedure.
* procedureName:string - The name of the Procedure to execute. (If the Procedure is defined in a service you should supply the "fully qualified" form of the name, i.e. "&lt;service>.&lt;procedurename>".)
* succeed:Function - Called when the HTTP status code is 2XX.

Note that in order for a Procedure to be marked "public" you must add "with ars_public=true" to the end of the PROCEDURE definition statement, like this:

```js
PROCEDURE MyService.MyPublicProcedure(a Integer, b Integer) with ars_public=true
```

If successful the "succeed" callback returns the "return" value of the procedure "response".

If the request fails the user will see an error popup that describes what happened.


```js
    //
    //  Set the Procedure arguments by name. (You may also specify 'args' as an array where the
    //  parameters are given in the same order as in the Procedure definition (e.g. 'args = [10,20];').
    //  'args' must not be null.
    //
    var args = {
        a:1,
        b:2
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  namespace:          The target namespace
    //  procedureArguments: The procedure arguments.
    //  procedureName:      The fully-qualified name of the Procedure.
    //  successCallback:    A callback function that will be driven when the request completes
    //                      successfully (i.e. a status code of 2XX)
    //
    client.executePublic("TargetNamespace",args,"MyService.MyPublicProcedure",function(response)
    {
        //
        //  At this point "response" is results of the Procedure call
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    });
```

### executeStreamed()
#### Convenience method to asynchronously execute a Procedure with streamed output in the Vantiq database.


```js
executeStreamed(procedureArguments:any, procedureName:string,
                succeed:Function, progress:Function, failure:Function,
                maxBufferSize:number=null, maxFlushInterval:number=null, options:any=null):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#executestreamed_1).

This function is similar to [client.execute()](#execute) except that it is intended for use when executing Procedures with "streamed output". (This generally means a VAIL Procedure which returns a ["sequence"](rules.md#sequences) rather than an "array".) Rather than waiting for the entire result set to be complete a Procedure with streamed output can deliver the results in "chunks" so you can start receiving results before the Procedures has completed execution. As each additional chunk arrives the "progress" callback will be called with the cumulative results to that point. When the Procedure actually completes (and all the output is available) the "success" callback will be called with the final results.


* procedureArguments:any - An object containing the arguments required by the procedure.
* procedureName:string - The name of the Procedure to execute. (If the Procedure is defined in a service you should supply the "fully qualified" form of the name, i.e. "&lt;service>.&lt;procedurename>".)
* succeed:Function - Called when the Procedure has completed execution and the HTTP status code is 2XX.
* failure:Function - Called if the call fails for some reason
* progress:Function - Called each time another "chunk" of output has arrived
* maxBufferSize:number - The maximum size of the streaming buffer before a "flush" is triggered. Value is in bytes and must be between 512 and 1048576. (Default is 64K)
* maxFlushInterval:number -  The maximum interval between flushes (in milliseconds). A value of 0 means that this feature is disabled and only the buffer size is used to trigger a flush. A negative value means that data will be flushed on every write. Otherwise, a flush will be triggered once the interval is exceeded (regardless of the buffer size). (Default is 5000ms.)
* options:any - An optional object you may use to pass data to the callback methods

Both the "succeed" and "progress" callbacks receive a single object "results" with the following content:

* data - The cumulative data received (so far) as an array
* rawData - The cumulative raw data received for far as a string (this might be parseable as a complete array, but it might be truncated such that the parse would result in an error)
* options - value of the "options" parameter
* isComplete - a boolean set to "true" when no more callbacks are expected
* chunksReceived - (Progress Only) Total "chunks" received so far
* totalRowsReceived - (Progress Only) Total rows received so far
* newRowsReceived -(Progress Only) New rows received with this chunk
* firstNewRowIndex - (Progress Only) The index of the first new row in this chunk

If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  Set the Procedure arguments by name. (You may also specify 'args' as an array where the
    //  parameters are given in the same order as in the Procedure definition (e.g. 'args = [10,20];').
    //  'args' must not be null.
    //
    var args = {
        a:1,
        b:2
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  procedureArguments: The procedure arguments.
    //  procedureName:      The fully-qualified name of the Procedure.
    //  successCallback:    A callback function that will be driven when the request completes
    //                      successfully (i.e. a status code of 2XX)
    //
    client.executeStreamed(args,"MyService.MyStreamedProcedure",
        function(results)
        {
            console.log("SUCCESS: " + JSON.stringify(results));
        },
        function(results)
        {
            console.log("PROGRESS: " + JSON.stringify(results));
        });
```

### executeStreamedPublic()
#### Convenience method to asynchronously execute a public "Streamed" Procedure in another namespace.


```js
executeStreamedPublic(namespace:string, procedureArguments:any, procedureName:string,
                      succeed:Function, progress:Function, failure:Function,
                      maxBufferSize:number=null, maxFlushInterval:number=null, options:any=null):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#executestreamedpublic_1).

This function is similar to [client.executeStreamed()](#executestreamed) except that it is needed to execute a "public" Procedure in a known namespace.

* namespace:string - The namespace where the public Procedure resides
* procedureArguments:any - An object containing the arguments required by the procedure.
* procedureName:string - The name of the Procedure to execute. (If the Procedure is defined in a service you should supply the "fully qualified" form of the name, i.e. "&lt;service>.&lt;procedurename>".)
* succeed:Function - Called when the Procedure has completed execution and the HTTP status code is 2XX.
* progress:Function - Called each time another "chunk" of output has arrived
* failure:Function - Called if the call fails for some reason
* maxBufferSize:number - The maximum size of the streaming buffer before a "flush" is triggered. Value is in bytes and must be between 512 and 1048576. (Default is 64K)
* maxFlushInterval:number -  The maximum interval between flushes (in milliseconds). A value of 0 means that this feature is disabled and only the buffer size is used to trigger a flush. A negative value means that data will be flushed on every write. Otherwise, a flush will be triggered once the interval is exceeded (regardless of the buffer size). (Default is 5000ms.)
* options:any - An optional object you may use to pass data to the callback methods

Both the "succeed" and "progress" callbacks receive a single object "results" with the following content:

* data - The cumulative data received (so far) as an array
* rawData - The cumulative raw data received for far as a string (this might be parseable as a complete array, but it might be truncated such that the parse would result in an error)
* options - value of the "options" parameter
* isComplete - a boolean set to "true" when no more callbacks are expected
* chunksReceived - (Progress Only) Total "chunks" received so far
* totalRowsReceived - (Progress Only) Total rows received so far
* newRowsReceived -(Progress Only) New rows received with this chunk
* firstNewRowIndex - (Progress Only) The index of the first new row in this chunk

If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  Set the Procedure arguments by name. (You may also specify 'args' as an array where the
    //  parameters are given in the same order as in the Procedure definition (e.g. 'args = [10,20];').
    //  'args' must not be null.
    //
    var args = {
        a:1,
        b:2
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  procedureArguments: The procedure arguments.
    //  procedureName:      The fully-qualified name of the Procedure.
    //  successCallback:    A callback function that will be driven when the request completes
    //                      successfully (i.e. a status code of 2XX)
    //
    client.executeStreamedPublic("TheTargetNamesapce", args, "MyService.MyStreamedPublicProcedure",
        function(results)
        {
            console.log("SUCCESS: " + JSON.stringify(results));
        },
        function(results)
        {
            console.log("PROGRESS: " + JSON.stringify(results));
        });
```




### formatMsg()
#### Look up a localization string and substitute the supplied parameters

```js
formatMsg(key:string, ...args:any[]):string
```
* key: string - The 'key' used to look up a locale-specific message

* args: any - An optional set of parameters to be substituted into the message


To localize a Client you may define a set of symbols which will be used to load a locale-specific string at runtime. In most cases these strings can be used in place of a literal value when setting properties on a Widget. However there are also times when you wish to load a localized string at runtime from JavaScript code.

The "formatMsg" method can be used to load a localized message. If you only supply a single argument then "formatMsg" just performs a lookup, returning the message value for the current locale. Additional arguments will be substituted into the message where the special "{n}" expressions are found (where the first argument replaces {0} and so on).


For example, if you have defined these symbols in an event handler you can access their locale-specific values at runtime as shown below:

```js
//$my.text.msg = Hello, World!
//$my.error.msg = The {0} jumped over the {1}.

var cat = "Cat";
var dog = "Dog";
var msg1 = client.formatMsg("$my.text.msg");
var msg2 = client.formatMsg("$my.error.msg", cat, dog);

```

In the example shown above the values of msg1 and msg2 (in the default locale anyway) would be 

```txt
msg1 = Hello, World!
msg2 = The Cat jumped over the Dog.
```

See [here](cbuser.md#localizing-clients) for a complete discussion of the Client localization process.

### generateUUID()
#### Generate a UUID

```js
generateUUID():string
```

This is convenience method that will generate an (effectively unique) UUID string. (For example, something like "1ae40299-4995-4ad8-86d6-e9dbe4363c34".)

### getCollaborationContext()
#### Get the "context" object when running under a Collaboration

```js
getCollaborationContext():any
```
When a Client is running as a result of a Collaboration sending a Notification there is a way to get access to the Collaboration's "context" information.
  
The "context" object will contain these properties:

* "collaboration" - the Collaboration object at the time the Notification was sent (which contains the current "results").
* A property for each collaborator role containing its value.
* A property for each entity, containing the referenced resource object.

You can use the values in the context to dynamically modify the Client and widgets when the Client starts up.

If the Client is **not** running as a result of a Collaboration (for example if it was invoked directly from the mobile devices' "Start" menu) then this method will return "null". (Unless you have explicitly called setCollaborationContext - see below.)


### getCurrentPage()
#### Get the current Page

```js
getCurrentPage():Page
```


### getCurrentPopup()
#### Get the current Page open as a Popup

```js
getCurrentPopup():Page
```



### getDataStreamByName()
#### Get a DataStream by name

```js
getDataStreamByName(name: string): DataStream
```

* name:string - The name of the DataStream to be found.

Returns "null" if the DataStream is not defined.



### getDataStreamByUUID()
#### Get a DataStream by UUID

```js
getDataStreamByUUID(uuid: string): DataStream
```

* uuid:string - The UUID of the DataStream to be found.

Returns "null" if the DataStream is not defined.



### getDocumentAssetLabelList()
#### Get the list of the labels supplied for the Document URLs in the "Document Assets" list

```js
getDocumentAssetLabelList(): string[]
```

If the developer has specified a lists of URLs for "document assets" (see below) they may also have supplied a human-readable "label" for each. This method returns a parallel array that contains those labels. (This list is managed from the Client Properties dialog in the Client Builder.) This might prove useful if the developer wanted to present a list of available document assets to the user and wanted to show a human-readable description instead of the actual URL.

This means that each elements of this array corresponds to the element in the array of URLs returned by client.getDocumentAssetList(). Since these elements contain human-readable text they may be localized in the same way that other Client text may be; see [here](cbuser.md#localizing-clients) for a complete discussion of the Client localization process.



### getDocumentAssetList()
#### Get the list of Document URLs in the "Document Assets" list

```js
getDocumentAssetList(): string[]
```

The method returns an array (which may be empty) that contains the list of URLs for the documents which were included in the Client's list of "Document Assets". (This list is managed from the Client Properties dialog in the Client Builder.) When this Client runs on a mobile app these assets will be loaded into a special cache on the mobile device so they will be available in offline mode. In fact these Document assets are **always** loaded from the Document cache (when present) even in online mode.

If the developer also specified human-readable text for each URL those labels may be retrieved using the client.getDocumentAssetLabelList method described above.


### getRequestParameters()
#### Get all request parameters when a client is started using a direct URL.

```js
getRequestParameters(): any
```

Returns a hash table with request parameter names as keys. The example below assumes this URL was used for the client:  
_http://dev.vantiq.com/ui/mpi/index.html?run=EngineMonitor&startPage=page2&engineId=abc_

```js
    var params = client.getRequestParameters();
    var startpage = params['startPage']; //startpage = 'page2'.
    var engineId = params['engineId']; //engineId = 'abc'.
    var engineLocation = params['engineLocation']; //engineLocation is undefined because it was not found in the URL.
```
 

### getDeviceId()
#### Returns the current "device id" (it if has a value for the current platform).

```js
getDeviceId():string
```

This will generally be the empty string unless this Client is running on a mobile device.

### getDeviceName()
#### Returns the current "device name" (it if has a value for the current platform).

```js
getDeviceName():string
```

This will have the value "Browser" when not running on a mobile device.


### getDocumentUrl()
#### Get the effective url of a document whose name starts with "docs/" or "public/".

```js
getDocumentUrl(docName:string): string
```

A document represents a file stored in the Vantiq Database. All document access require authentication. getDocumentUrl() can be used to generate the full url with authentication info. For example:

* To get the URL of a public document whose name starts with "_public/_", use `getDocumentUrl('public/images/mylogo.jpg')` to get '_/ui/docs/NS/{namespace}/images/mylogo.jpg_' where {namespace} is the current namespace for the logged in user.

* To get the URL of a private document whose name does not start with "public/", add the "_docs/_" prefix to document name, then use `getDocumentUrl('docs/myPrivateInfo.txt')` to get '_/ui/docs/myPrivateInfo.txt?token={access_token}_' where {access_token} is the valid access token for the logged in user.

* If the supplied docName does not start with 'http:', 'https:' or '../' then the method will assume you are just trying to access a private document
and will adjust the URL accordingly. For example, if you supply a docName of '_myImage.png_' the generated name will be '_/ui/docs/myImage.png?token={access_token}_'.


Document URLs are also discussed [here](cbuser.md#accessing-documents).

### getGroupNames()
#### Get a list of the Groups associated with the current User

Every Vantiq user has a "user record" object which contains information about the user and their attributes. This method uses that record to get a list containing the names of all Vantiq 'Groups' of which the user is currently a member.

```js
getGroupNames():string[]
```

### getLocation()
#### Retrieve the current latitude/longitude coordinates of the client.

This function returns a JSON object containing _latitude_ and _longitude_ properties or _null_ if the device's location cannot be determined. This call will work in a mobile device or a browser only if the user has given permission for Location data (or _null_ if not).

```js
getLocation(callback: Function)
```

* callback: Function - (Required) A function called with one parameter, the JSON object or _null_, when the Client either retrieves a GPS location or not.

```js
client.getLocation(function(location) {
    if (location) {
        console.log("location = " + JSON.stringify(location));
    } else {
        console.log("no location!");
    }
});
```



### getName()
#### Get the current Client name

```js
getName():string
```



### getUsername()
#### Get the currently authenticated username

```js
getUsername():string
```




### getProfileNames()
#### Get a list of the Profiles associated with the current User

Every Vantiq user has a "user record" object which contains information about the user and their attributes. This method uses that record to get a list containing the names of all Vantiq 'Profiles' that the user is associated with.

```js
getProfileNames():string[]
```



### getStateObject()
#### Returns the "state object" passed in with the Notification that launched us if there was one.

```js
getStateObject():any
```

### getUserRecord()
#### Get the raw 'user record' object associated with the current User

Every Vantiq user has a "user record" object which contains information about the user and their attributes. This method returns the user record in its raw form. Note that there is a small risk that the contents of this record may change in the future.

```js
getUserRecord():any
```

### getWidget()
#### Get a Widget by name

```js
getWidget(name: string): Widget
```

* name:string - The name of the Widget to be found.

All Widgets have a unique name, so you can use the name to look up the Widget (even if it lives on another page). 


### goToPage()
#### Navigate to the indicated Page

```js
goToPage(pageName: string, parameters: any, transition: string, transitionDuration: number): void
```

* pageName:string - The name of the target page.

* parameters:any - (optional) A data item that will be passed to the target page in its "onStart" handler as the second argument "parameters".

* transition:string - (optional) triggers a one-second transition effect. May be one of the following: fade, slideDown, slideUp, slideRight, slideLeft, highlight or shake. To trigger a transition effect without needing to pass back parameters, simply use an empty JSON object (i.e. {}) as the second argument.

* transitionDuration:number - (optional) supply a specific duration for the transition effect to override the default one second. This value is expressed in milliseconds so to specify a half second transition duration, use 500 as the value.

This function can throw an exception in some situations, such as if the page specified does not exist.



### infoDialog()
#### Pop up an "Info" Dialog with the supplied message.

```js
infoDialog(msg: string, title: string):void
```

* msg: string - The text to be displayed in the popup.
* title: string - The text to be displayed in the popup title bar. (optional)

The dialog is modal; the user must click "OK" to dismiss it. The parameters may be supplied as "localization keys" instead of literal text (See [here](cbuser.md#localizing-clients) for a complete discussion of the Client localization process.)


### insert()
#### Convenience method to issue an asynchronous "insert" to add a single item to the Vantiq database

```js
insert(typeName:string, data:any, parameters:any, succeed:Function):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#insert_1).


* typeName:any - The name of a user-defined Type.
* data:any - The object to be inserted.
* succeed:Function - Called when the HTTP status code is 2XX. 

If successful the "succeed" callback returns the inserted object in "response". 

If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  The object to be inserted
    //
    var aNewEmployee = {
        firstName: "John",
        lastName: "Smith",
        salary: 50000
    };
        
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  typeName:        The name of the Type 
    //  data:            The object being inserted.
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //
    client.insert("Employee", aNewEmployee,function(response)
    {
        //
        //  At this point "response" is the inserted object
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    });
```



### instance
#### Client.instance refers to the current "client" object

```js
Client.instance: Client
```

All event handlers are already given a parameter called "client" which references the current Client instance.

But in "custom code" (which is simply your own JavaScript functions) you do not have access to this parameter. You **could** pass "client" in yourself when you call into these functions but the "Client.instance" property gives you access to the current "client" directly.



### isNetworkActive
#### The current state of the network connection

```js
isNetworkActive: boolean
```

"true" if there is currently a network connection available, and "false" if not. (This property is always "true" when running in a browser since offline mode is only supported in mobile devices.)

See [here](cbuser.md#offline-operation) for a further discussion of running Clients while the device is offline.


### isPublic
#### Check if the current Client is running as "Public"

```js
isPublic: boolean
```

"true" if the Client is running in "Public" mode.

See [here](cbuser.md#public-clients) for a further discussion of Public Clients and how they are used.


### localeCountryCode
#### The "country code" of the current locale

```js
localeCountryCode: string
```

This is usually a two-character code like "us" or "*" is there is no country code specified.

### localeLanguageCode
#### The "language code" of the current locale

```js
localeLanguageCode: string
```

This is usually a two-character code like "en".


### localeVariantCode
#### The "variant code" of the current locale

```js
localeVariantCode: string
```

This code is generally not used by most locales and has a value of "*".



### logout()
#### Terminate the Client the Client and "logout" the current user

```js
logout():boolean
```

For Clients being run from a browser, logout() will only function for Clients started via the Client Launcher. For the iOS and Android mobile apps, the Client will terminate and the user will be returned to the login view.

### markupImage()
#### Ask the user to "mark up" an image and upload it to the server as a Document

```js
markupImage(    responseObjectProperty:string,
                source:string,
                maxWidth:number=null,
                thumbnailSize:number=null,
                groupName:string=null,
                callback:Function):void
```

This API request programmatically simulates the operation of the [ImageMarkup](#imagemarkup) Widget.

* responseObjectProperty:string - The name of the property added to the "response object" which will contain the results of the operation. 

<span style="padding-left:40px;">
This is analogous to the way the name of the [ImageMarkup](#imagemarkup) Widget is used to give a name to the results in the response object.
</span>

* source:string - The source of the image to be offered to the user for markup

<span style="padding-left:40px;">
This may be the string "camera" (if you want the user to snap an image first), the URL of an accessible image from the internet or an image Document in the Vantiq server (e.g. "../../docs/MyDocument.png"). 
</span>

<span style="padding-left:40px;">
The default value is "camera".
</span>

* maxWidth:number - Restrict the size of the captured image (optional)

<span style="padding-left:40px;">
Markup images returned by mobile devices can be quite large so can cause long upload and download times. To restrict the size of the image returned you can supply a non-null value for the _maxWidth_ parameter. If the markup image width is larger than the _maxWidth_ parameter, the image is scaled such that the width matches the _maxWidth_ value and the height is scaled to match the aspect ratio of the markup image. If no value is provided for the _maxWidth_ parameter, the markup image is returned unmodified.
</span>

* thumbnailSize:number - Create a thumbnail image for the captured image (optional)

<span style="padding-left:40px;">
To create a second 'thumbnail' version of the markup image you can supply a non-null value for the _thumbnailSize_ parameter. If the _thumbnailSize_ parameter is specified, an image is created with its width or height, whichever is greater, scaled such that it matches the _thumbnailSize_ value and the lesser of the width or height is scaled to match the aspect ratio of the captured image. If no value is provided for the _thumbnailSize_ parameter, no thumbnail image is created.
</span>

<span style="padding-left:40px;">
The uploaded thumbnail Document will have the same name as the uploaded markup Document with a suffix of "Thumbnail" before the file extension.
</span>

* groupName:string - The name of the Group to which the uploaded Document should be assigned (optional)

<span style="padding-left:40px;">
When this request creates and uploads a Document it will be assigned to the indicated [Group](resourceguide.md#groups). This is useful for controlling which users will have access to the Document.
</span>

* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The function has a single parameter which is an object of type NativeOperationRequest (see below). It contains URLs which may be used to reference the image and thumbnail. Note that when the callback runs, the image has **not** yet been uploaded; it just means the image has been created and temporarily resides on the mobile device. Just like the [ImageMarkup](#imagemarkup) Widget the document won't be created until after a "default Submit" or custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) operation has completed.
</span>


```
class NativeOperationRequest
{
    public responseObjectValueName:string;      //  The 'responseObjectProperty' parameter your specified
    public responseObjectThumbnailName:string;  //  The name of the thumbnail images response object, generated
                                                //  by adding "Thumbnail" to the responseObjectValueName.

    public localDocumentURL:string;             //  A URL which references the temporary local image
    public localThumbnailURL:string;            //  A URL which references the temporary local thumbnail
}
```

Note that these URLs are **local** to the mobile device; they have no meaning externally and can only be used to reference the temporary local copy of the images before they have been uploaded to the server and turned into Documents.

Inside an event handler you might use this API operation like this:

```js
    //
    //  Capture a markup image based on an image from the camera. Create a 150-pixel thumbnail image and
    //  execute the callback when the image is ready for upload.
    //
	client.markupImage("TheMarkupImage","camera", null, 150, null, function(nativeOpRequest)
    	{
        	//
        	//	Use the callback to display a thumbnail of the captured image in a StaticImage widget
        	//	before it is uploaded.
        	//
        	var thumbnailWidget = client.getWidget("TheThumbnailWidget");
        	thumbnailWidget.url = nativeOpRequest.localThumbnailURL;
    	});
```

When the current Page is submitted the captured image markup document will be uploaded along with the rest of the data (and given a property name of "TheMarkupImage" in the response object.) If you are using a custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) you can add this item explicitly using a call like this:

```js
	var uploader = new Uploader(client);

	var nativeOpRequest = uploader.addAPIRequestFor("TheMarkupImage");

```

In the callback of the [Uploader's](cbuser.md#custom-behavior-using-the-uploader) "start" method (which is called after the upload completes) you can extract the actual Document name which was assigned:

```js
    uploader.start(function(theUploader)
	{
        //
        //  The uploaded Image Document name
        //
        var documentName = theUploader.responseObject.values[nativeOpRequest.responseObjectValueName];
        //
        //  The uploaded Thumbnail Document name
        //
        var thumbnailName = theUploader.responseObject.values[nativeOpRequest.responseObjectThumbnailName];
	};

```


### modifyClientEvent()
#### Modify the configuration of a "Client Event" DataStream at runtime

```js
modifyClientEvent(datastream:DataStream, parameters:ClientEventParameters):void
```

* datastream:DataStream - The DataStream object to be modified; this **must** be of type "Client Event" or an exception will be thrown.

* parameters:ClientEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to override.

You must use either [getDataStreamByName()](#getdatastreambyname) or [getDataStreamByUUID()](#getdatastreambyuuid) to look up the DataStream to be modified. The properties of the ClientEventParameters object should be set to indicate the changes you wish to make:

```
class ClientEventParameters
{
    public typeName:string;         
    public dataObjectName:string;   
    public groupBy:string;
}
```

* typeName: The name of a Type which describes the data associated with the Client Event. 

* dataObjectName: The name of a DataObject which describes the data associated with the Client Event.

* groupBy:string: The name of the "groupBy" property within the Type or DataObject.

You may set either 'typeName' or 'dataObjectName' but not both.


For example, inside an event handler you might change the behavior of a "Client Event" DataStream like this:

```js
	var ds = client.getDataStreamByName("MyClientEventDataStream");
	var p = new ClientEventParameters();

	p.typeName = "ADifferentType";

	client.modifyClientEvent(ds,p);
```

If the modifyClientEvent() is successful the ClientEvent will now expect the data associated with the Client Event to be of Type "ADIfferentType".



### modifyDataChanged()
#### Modify the configuration of a "Data Changed" DataStream at runtime

```js
modifyDataChanged(datastream:DataStream, parameters:DataChangedParameters):void
```

* datastream:DataStream - The DataStream object to be modified; this **must** be of type "Data Changed" or an exception will be thrown.

* parameters:DataChangedParameters - A special object (described below) that contains the parameters of the DataStream you wish to override.

You must use either [getDataStreamByName()](#getdatastreambyname) or [getDataStreamByUUID()](#getdatastreambyuuid) to look up the DataStream to be modified. The properties of the DataChangedParameters object should be set to indicate the changes you wish to make:

```
class DataChangedParameters
{
    public typeName:string;
    public isInsert:boolean;
    public isUpdate:boolean;
    public isDelete:boolean;
    public groupBy:string;
    public eventFilter:any;
}
```

* typeName: The name of a Type which is to be monitored for changes.

* isInsert: Set to "true" if you wish to be notified of "inserts" on the Type.

* isUpdate: Set to "true" if you wish to be notified of "updates" on the Type.

* isDelete: Set to "true" if you wish to be notified of "deletes" on the Type.

* groupBy:string: The name of the "groupBy" property within the Type (may be null).

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).

You may listen for any combination of "inserts", "updates" and "deletes".

Note that you must specify all the properties which should be set, even if they are unchanged.

For example, inside an event handler you might change the behavior of a "Data Changed" DataStream like this:

```js
	var ds = client.getDataStreamByName("MyDataChangedDataStream");
	var p = new DataChangedParameters();

	p.typeName = "ADifferentType";
    p.isInsert = true;
    p.isUpdate = true;

	client.modifyDataChanged(ds,p);
```

If the modifyDataChanged() is successful you will be un-subscribed from changes to the old Type and subscribed for "insert" and "update" changes on "ADifferentType".








### modifyPagedQuery()
#### Modify the configuration of a "Paged Query" DataStream at runtime

```js
modifyPagedQuery(datastream:DataStream, parameters:PagedQueryParameters):void
```

* datastream:DataStream - The DataStream object to be modified; this **must** be of type "Paged Query" or an exception will be thrown.

* parameters:PagedQueryParameters - A special object (described below) that contains the parameters of the DataStream you wish to override.

You must use either [getDataStreamByName()](#getdatastreambyname) or [getDataStreamByUUID()](#getdatastreambyuuid) to look up the DataStream to be modified. The properties of the PagedQueryParameters object should be set to indicate the changes you wish to make:

```
class PagedQueryParameters
{
    public typeName:string;
    public sortByPropertyName:string;
    public sortDescending:boolean;
    public whereClause:object;
}
```

* typeName: The name of the Vantiq Type to be queried.

* sortByPropertyName: The name of a property by which the results should be sorted.

* sortDescending: "true" if you which the sort to be done in ascending order ("false"/ascending is the default).

* whereClause: An object containing the "where" clause for the query. (For details on constructing this object you can consult the [API Reference Guide](api.md#where-parameter))

You should only specify those properties whose values you wish to change; all un-specified parameters will be left as they are.

For example, inside an event handler you might change the behavior of a Paged Query DataStream like this:

```js
	var ds = client.getDataStreamByName("MyPagedQueryDataStream");
	var p = new PagedQueryParameters();

	p.whereClause = {
        salary: {
            "$gte": 100000
        }
    };

	client.modifyPagedQuery(ds,p);
```

If the modifyPagedQuery() is successful the new query will be re-run immediately and the DataTable reset to the first page.






### modifyPublishEvent()
#### Modify the configuration of a "Publish Event" DataStream at runtime

```js
modifyPublishEvent(datastream:DataStream, parameters:PublishEventParameters):void
```

* datastream:DataStream - The DataStream object to be modified; this **must** be of type "Publish Event" or an exception will be thrown.

* parameters:PublishEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to override.

You must use either [getDataStreamByName()](#getdatastreambyname) or [getDataStreamByUUID()](#getdatastreambyuuid) to look up the DataStream to be modified. The properties of the PublishEventParameters object should be set to indicate the changes you wish to make:

```
class PublishEventParameters
{
    public topic:string;
    public groupBy:string;
    public eventFilter:any;
}
```

* topic: The topic name you wish to listen for.

* groupBy:string: The name of the "groupBy" property within the message object (may be null).

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).

Note that you must specify all the properties which should be set, even if they are unchanged.

For example, inside an event handler you might change the behavior of a "Publish Event" DataStream like this:

```js
	var ds = client.getDataStreamByName("MyPublishEventDataStream");
	var p = new PublishEventParameters();

	p.topic = "/my/new/topicname";

	client.modifyPublishEvent(ds,p);
```

If the modifyPublishEvent() is successful you will be un-subscribed from the old topic and subscribed to the new one.


### modifyResourceEvent()
#### Modify the configuration of a "Resource Event" DataStream at runtime

```js
modifyResourceEvent(datastream:DataStream, parameters:ResourceEventParameters):void
```

* datastream:DataStream - The DataStream object to be modified; this **must** be of type "Resource Event" or an exception will be thrown.

* parameters:ResourceEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to override.

You must use either [getDataStreamByName()](#getdatastreambyname) or [getDataStreamByUUID()](#getdatastreambyuuid) to look up the DataStream to be modified. The properties of the ResourceEventParameters object should be set to indicate the changes you wish to make:

```
class ResourceEventParameters
{
    public eventPath:string;
    public eventFilter:any;
}
```

* eventPath: The event path that you wish to listen for.

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).

Note that you must specify all the properties which should be set, even if they are unchanged.

For example, inside an event handler you might change the behavior of a "Source Event" DataStream like this:

```js
	var ds = client.getDataStreamByName("MyResourceEventDataStream");
	var p = new ResourceEventParameters();

	p.eventPath = "/topics/my/new/event/path";

	client.modifyResourceEvent(ds,p);
```

If the modifyResourceEvent() is successful you will be un-subscribed from the old event path and subscribed to the new one.



### modifyOutboundServiceEvent()
#### Modify the configuration of a "Service Event" DataStream at runtime

```js
modifyOutboundServiceEvent(datastream:DataStream, parameters:ServiceEventParameters):void
```

* datastream:DataStream - The DataStream object to be modified; this **must** be of type "Service Event" or an exception will be thrown.

* parameters:ServiceEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to override.

You must use either [getDataStreamByName()](#getdatastreambyname) or [getDataStreamByUUID()](#getdatastreambyuuid) to look up the DataStream to be modified. The properties of the ServiceEventParameters object should be set to indicate the changes you wish to make:

```
class ServiceEventParameters
{
    public service:string;
    public serviceEventName:string;
    public groupBy:string;
    public eventFilter:any;
}
```

* service: The name of the Service whose outbound event you wish to listen for.

* serviceEventName: The name of the "outbound event" of the specified Service you wish to listen for.

* groupBy:string: The name of the "groupBy" property within the message object (may be null).

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).

Note that you must specify all the properties which should be set, even if they are unchanged.

For example, inside an event handler you might change the behavior of a "Service Event" DataStream like this:

```js
	var ds = client.getDataStreamByName("MyServiceEventDataStream");
	var p = new ServiceEventParameters();

    p.service = "a.b.c.MyService";
    p.serviceEventName = "TheOutboundEventName";

	client.modifyOutboundServiceEvent(ds,p);
```

If the modifyOutboundServiceEvent() is successful you will be un-subscribed from the old Service Event and subscribed to the new one.





### modifySourceEvent()
#### Modify the configuration of a "Source Event" DataStream at runtime


```js
modifySourceEvent(datastream:DataStream, parameters:SourceEventParameters):void
```

* datastream:DataStream - The DataStream object to be modified; this **must** be of type "Source Event" or an exception will be thrown.

* parameters:SourceEventParameters - A special object (described below) that contains the parameters of the DataStream you wish to override.

You must use either [getDataStreamByName()](#getdatastreambyname) or [getDataStreamByUUID()](#getdatastreambyuuid) to look up the DataStream to be modified. The properties of the SourceEventParameters object should be set to indicate the changes you wish to make:

```
class SourceEventParameters
{
    public source:string;
    public groupBy:string;
    public eventFilter:any;
}
```

* source: The name of the Source which you wish to listen for.

* groupBy:string: The name of the "groupBy" property within the message object (may be null).

* eventFilter:any: Filter out any incoming events which do *not* contain the property and value specified in the object. (may be null).

Note that you must specify all the properties which should be set, even if they are unchanged.

For example, inside an event handler you might change the behavior of a "Source Event" DataStream like this:

```js
	var ds = client.getDataStreamByName("MySourceEventDataStream");
	var p = new SourceEventParameters();

	p.source = "ADifferentSource";

	client.modifySourceEvent(ds,p);
```

If the modifySourceEvent() is successful you will be un-subscribed from changes to the old Source and subscribed to changes from the new one.






### modifyTimedQuery()
#### Modify the configuration of a "Timed Query" DataStream at runtime

```js
modifyTimedQuery(datastream:DataStream, parameters:TimedQueryParameters):void
```

* datastream:DataStream - The DataStream object to be modified; this **must** be of type "Timed Query" or an exception will be thrown.

* parameters:TimedQueryParameters - A special object (described below) that contains the parameters of the DataStream you wish to override.

You must use either [getDataStreamByName()](#getdatastreambyname) or [getDataStreamByUUID()](#getdatastreambyuuid) to look up the DataStream to be modified. The properties of the TimedQueryParameters object should be set to indicate the changes you wish to make:

```
class TimedQueryParameters
{
    public typeName:string;
    public updateIntervalInSeconds:number;
    public groupByPropertyName:string;
    public maximumRecordsReturned:number;
    public sortByPropertyName:string;
    public sortDescending:boolean;
    public whereClause:object;
}
```

* typeName: The name of the Vantiq Type to be queried.

* updateIntervalInSeconds: The delay in seconds between queries. If this value is "0" the query will be run only once.

* groupByPropertyName: The name of the property used to filter the results; only used by certain Widgets such as the FloorplanViewer.

* maximumRecordsReturned: The maximum number of records to be returned by the query (corresponds to the "limit" option).

* sortByPropertyName: The name of a property by which the results should be sorted.

* sortDescending: "true" if you which the sort to be done in ascending order ("false"/ascending is the default).

* whereClause: An object containing the "where" clause for the query. (For details on constructing this object you can consult the [API Reference Guide](api.md#where-parameter))

You should only specify those properties whose values you wish to change; all un-specified parameters will be left as they are. 

For example, inside an event handler you might change the behavior of a timed query DataStream like this:

```js
	var ds = client.getDataStreamByName("MyTimedQueryDataStream");
	var p = new TimedQueryParameters();

	p.whereClause = {
        salary: {
            "$gte": 100000
        }
    };

	client.modifyTimedQuery(ds,p);
```

If the modifyTimedQuery() is successful the new query will be re-run immediately and the delay timer will be reset.









### navBarBackgroundColor
#### The background color of the Client Launcher "navbar"

```js
navBarBackgroundColor: String
```

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".



### navBarForegroundColor
#### The foreground color of the Client Launcher "navbar"

```js
navBarForegroundColor: String
```

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".




### navBarTitleFontFamily
#### The font family of the title in the Client Launcher "navbar"

```js
navBarTitleFontFamily: String
```

This may be any string that will be interpreted by the browser as CSS "font family".

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".




### navBarTitleFontStyle
#### The font style of the title in the Client Launcher "navbar"

```js
navBarTitleFontStyle: String
```

This may be any string that will be interpreted by the browser as a CSS "font style", such as "normal", "italic", etc.

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".






### navBarTitleFontSize
#### The font size of the title in the Client Launcher "navbar"

```js
navBarTitleFontSize: Number
```

This must be a number indicating the size of the title font in pixels. 

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".



### navBarTitleFontWeight
#### The font weight of the title in the Client Launcher "navbar"

```js
navBarTitleFontWeight: String
```

This may be any string that will be interpreted by the browser as a CSS "font weight", such as "normal", "bold", etc.

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".



### navBarIcon
#### The icon shown in the Client Launcher "navbar"

```js
navBarIcon: String
```

This must be the URL of the icon which should be shown in the navbar. Usually it will be a "Document" in the current namespace, which means it should be a relative URL of the form "../../docs/myIcon.png". When overriding the icon you *must* also specify "navBarIconHeight" and "navBarIconWidth".

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".




### navBarIconHeight
#### The height of the icon in the Client Launcher "navbar"

```js
navBarIconHeight: Number
```

This must be a number indicating the height of the "navBarIcon" in pixels.

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".




### navBarIconWidth
#### The width of the icon in the Client Launcher "navbar"

```js
navBarIconWidth: Number
```

This must be a number indicating the width of the "navBarIcon" in pixels.

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".





### navBarShowControls
#### "true" if the controls are shown in Client Launcher "navbar"

```js
navBarShowControls: Boolean
```

This boolean defaults to "true" and determines whether the "controls" should be shown at the right-hand side of the navbar (such as the buttons which allow you to logout or switch namespaces). Setting this value to "false" is not recommended since it can make it awkward for the user to switch to the proper namespace.


See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".




### navBarTitle
#### The title in the Client Launcher "navbar"

```js
navBarTitle: String
```

Normally the runtime system will automatically set the title to the name of the Client; you can override this using "navBarTitle"

See [here](cbuser.md#customizing-the-client-launcher) for an further discussion of customizing the Client Launcher "navbar".











### overrideLocale
#### Changes the effective locale in use at runtime

```js
overrideLocale: String
```

See [here](cbuser.md#changing-locales-at-runtime) for a discussion of what this property means and how to use it.


### playAudio()
#### Play an audio clip previously recorded by 'recordAudio'

```js
playAudio(  localAudioURL:string,
            callback:Function):void
```

This API request programmatically simulates the "playback" operation of the [AudioRecorder](#audiorecorder) Widget.

* localAudioURL:string - The URL that references a local audio file

<span style="padding-left:40px;">
This URL must be the "localDocumentURL" from the NativeOperationRequest of the callback of a previously executed ["client.recordAudio()"](#recordaudio) request. Note that this temporary file is automatically deleted after the Document has been uploaded.
</span>

There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).


* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The callback is only useful for knowing when the audio playback is complete (or was canceled). 
</span>


Inside an event handler you might use this API operation like this:

```js
    //
    //  Play back a short audio clip previously captured by a "recordAudio" call.
    //  "client.data.localAudioURL" must have be set by the "recordAudio" callback.
    //
	client.playAudio(client.data.localAudioURL, function()
    	{
            //  Playback complete
    	});
```



### playVideo()
#### Play a video clip previously recorded by 'recordVideo'

```js
playVideo(  localVideoURL:string,
            callback:Function):void
```

This API request programmatically simulates the "playback" operation of the [VideoRecorder](#videorecorder) Widget.

* localVideoURL:string - The URL that references a local video file

<span style="padding-left:40px;">
This URL must be the "localDocumentURL" from the NativeOperationRequest of the callback of a previously executed ["client.recordVideo()"](#recordvideo) request. Note that this temporary file is automatically deleted after the Document has been uploaded.
</span>

There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).


* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The callback is only useful for knowing when the video playback is complete (or was canceled). 
</span>


Inside an event handler you might use this API operation like this:

```js
    //
    //  Play back a short video clip previously captured by a "recordVideo" call.
    //  "client.data.localVideoURL" must have be set by the "recordVideo" callback.
    //
	client.playVideo(client.data.localVideoURL, function()
    	{
            //  Playback complete
    	});
```







### popupPage()
#### Open a Page as a popup dialog

```js
popupPage(pageName: string, popupTitle: string, parameters: any=null, callback: Function=null, pagePosition:PagePosition=PagePosition.Center, xOffset:number=0, yOffset:number=0): void
```

* pageName:string - The name of the page to be opened as a popup dialog. The page must be in "Browser" layout.

* popupTitle:string - The title to appear on the popup dialog

* parameters:any - (optional) A data item that will be passed to the target page in its "onStart" handler as the second argument "parameters".

* callback:Function - (optional) A callback function that will be invoked when the popup Page exits via [client.closePopup()](#closepopup).

* pagePosition:PagePosition - (optional) Specify where the popup should be positioned relative to the Page area (defaults to PagePosition.Center. Other options are .NW, .N, .NE, .W, .E, .SW, .S and  .SE)

* xOffset:number - (optional) Specify how many horizonal pixels the popup should be offset from the pagePosition.

* yOffset:number - (optional) Specify how many vertical pixels the popup should be offset from the pagePosition.

This function is similar to [client.goToPage()](#gotopage) except that instead of "navigating to" the Page it will be popped up inside a modal dialog. (The popup will be sized so as to "frame" the contents of the Page.)

This function can throw an exception in some situations, such as if there is already a page popped up or the target page is not in "Browser" layout.

The popup will be visible until [client.closePopup()](#closepopup) is called.

Here's an example of how this call might be used, assuming that "MyPopupPage" is the name of a Page.

```js
   var myParameters = {
       "a":1,
       "b":2
   }
   
   client.popupPage("MyPopupPage","A Custom Title",myParameters,function(returnParameters)
   {    
       console.log("The Return Parameters: " + returnParameters);
   });

```

This example shows how to position the popup so it is centered horizontally above the Page and aligned to the top but offset downward by 10 pixels.

```js
   client.popupPage("MyPopupPage","A Custom Title",null,null,PagePosition.N,0,10);
```



### publish()
#### Convenience method to asynchronously "publish" an event on a "topic"

```js
publish(data:any, topic:string, succeed:Function=):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#publish_1).

* data:any - The "message object" to attach to the event
* topic:string - The "topic" for the "publish" (which must be of the form "/a/b/c").
* succeed:Function - Called when the HTTP status code is 2XX. 

If successful the "succeed" callback returns but the "response" object has no meaning.

If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  The "message object" that is to be sent along with the "publish"
    //
    var theMessageObject = {
        a: 1,
        b: 2
    };
    
    //
    //  The name of the "topic" identifying this event
    //
    var topicName = "/a/b/c/d";
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  data:            The "message object" that is to be sent along with the "publish"
    //  topic:           The topic name identifying the event
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //
    client.publish(theMessageObject,topicName,function(response)
    {
        //
        //  "response" is meaningless for a "publish"
        //
    });
```


### publishToServiceEvent()
#### Convenience method to asynchronously "publish" to an inbound event of a Service

```js
publishToServiceEvent(data:any, serviceName:string, eventName:string, successCallback:Function):void
```

Publish directly to the "inbound event" of a Service.

* data:any - The "message object" to attach to the event. This should be compatible with the schema defined on the target event.
* serviceName:string - The full name of the target Service.
* eventName:string - The name of an "inbound event" defined on the Service.
* succeed:Function - Called when the HTTP status code is 2XX.

If successful the "succeed" callback returns but the "response" object has no meaning.

If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  The "message object" that is to be sent along with the "publish"
    //
    var theMessageObject = {
        a: 1,
        b: 2
    };
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  data:            The "message object" that is to be sent along with the "publish"
    //  serviceName:     The full name of the target Service
    //  eventName:       The name of an "inbound event" defined on the Service.
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //
    client.publishToServiceEvent(theMessageObject,"a.b.c.MyService","TheInboundEventName",function(response)
    {
        //
        //  "response" is meaningless for a "publish"
        //
    });
```



### recordAudio()
#### Ask the user to record a short audio clip and upload it to the server as a Document

```js
recordAudio(    responseObjectProperty:string,
                maxDurationInSeconds:number=null,
                maxSizeInK:number=null,
                groupName:string=null,
                callback:Function):void
```

This API request programmatically simulates the operation of the [AudioRecorder](#audiorecorder) Widget.

* responseObjectProperty:string - The name of the property added to the "response object" which will contain the results of the operation. 

<span style="padding-left:40px;">
This is analogous to the way the name of the [AudioRecorder](#audiorecorder) Widget is used to give a name to the results in the response object.
</span>


* maxDurationInSeconds:number - The maximum number of seconds which may be recorded (optional)

<span style="padding-left:40px;">
In order to place a limit of the amount of storage used in your mobile device this setting specifies a maximum number of seconds of audio which you may record. (Default - 10 seconds).
</span>

* maxSizeInK:number - The maximum amount of storage that may be recorded (optional)

<span style="padding-left:40px;">
In order to place a limit of the amount of storage used in your mobile device this setting specifies a maximum size of the clip which may be recorded. (Default - 100K).
</span>


* groupName:string - The name of the Group to which the uploaded Document should be assigned (optional)

<span style="padding-left:40px;">
When this request creates and uploads a Document it will be assigned to the indicated [Group](resourceguide.md#groups). This is useful for controlling which users will have access to the Document.
</span>

* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The function has a single parameter which is an object of type NativeOperationRequest (see below). It contains a URL which may be used to reference the recorded audio clip. Note that when the callback runs, the audio clip has **not** yet been uploaded; it just means the audio file has has been recorded and temporarily resides on the mobile device. Just like the [AudioRecorder](#audiorecorder) Widget the document won't be created until after a "default Submit" or custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) operation has completed.
</span>


```
class NativeOperationRequest
{
    public responseObjectValueName:string;      //  The 'responseObjectProperty' parameter your specified

    public localDocumentURL:string;             //  A URL which references the temporary local audio clip
}
```

Note that the localDocumentURL is **local** to the mobile device; it has no meaning externally and can only be used to reference the temporary local copy of the audio clip before it has been uploaded to the server and turned into a Document.

Inside an event handler you might use this API operation like this:

```js
    //
    //  Capture a short audio clip and execute the callback when the clip is ready for upload.
    //
	client.recordAudio("TheAudioClip", 10, 2000, null, function(nativeOpRequest)
    	{
        	//
        	//	Remember the URL pointing to the local audio clip; this could be used with the "client.playAudio"
            //  API call to allow the user to review the recording before submitting.
        	//
            client.data.localAudioURL = nativeOpRequest.localDocumentURL;
    	});
```

When the current Page is submitted the captured audio Document will be uploaded along with the rest of the data (and given a property name of "TheAudioClip" in the response object.) If you are using a custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) you can add this item explicitly using a call like this:

```js
	var uploader = new Uploader(client);

	var nativeOpRequest = uploader.addAPIRequestFor("TheAudioClip");

```

In the callback of the [Uploader's](cbuser.md#custom-behavior-using-the-uploader) "start" method (which is called after the upload completes) you can extract the actual Document name which was assigned:

```js
    uploader.start(function(theUploader)
	{
        //
        //  The uploaded Audio Document name
        //
        var documentName = theUploader.responseObject.values[nativeOpRequest.responseObjectValueName];
	};

```



### recordVideo()
#### Ask the user to record a short video clip and upload it to the server as a Document

```js
recordVideo(    responseObjectProperty:string,
                maxDurationInSeconds:number=null,
                maxSizeInK:number=null,
                groupName:string=null,
                callback:Function):void
```

This API request programmatically simulates the operation of the [VideoRecorder](#videorecorder) Widget.

* responseObjectProperty:string - The name of the property added to the "response object" which will contain the results of the operation. 

<span style="padding-left:40px;">
This is analogous to the way the name of the [VideoRecorder](#videorecorder) Widget is used to give a name to the results in the response object.
</span>


* maxDurationInSeconds:number - The maximum number of seconds which may be recorded (optional)

<span style="padding-left:40px;">
In order to place a limit of the amount of storage used in your mobile device this setting specifies a maximum number of seconds of video which you may record. (Default - 10 seconds).
</span>

* maxSizeInK:number - The maximum amount of storage that may be recorded (optional)

<span style="padding-left:40px;">
In order to place a limit of the amount of storage used in your mobile device this setting specifies a maximum size of the clip which may be recorded. (Default - 1000K).
</span>


* groupName:string - The name of the Group to which the uploaded Document should be assigned (optional)

<span style="padding-left:40px;">
When this request creates and uploads a Document it will be assigned to the indicated [Group](resourceguide.md#groups). This is useful for controlling which users will have access to the Document.
</span>

* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The function has a single parameter which is an object of type NativeOperationRequest (see below). It contains a URL which may be used to reference the recorded video clip. Note that when the callback runs, the video clip has **not** yet been uploaded; it just means the video file has has been recorded and temporarily resides on the mobile device. Just like the [VideoRecorder](#videorecorder) Widget the document won't be created until after a "default Submit" or custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) operation has completed.
</span>


```
class NativeOperationRequest
{
    public responseObjectValueName:string;      //  The 'responseObjectProperty' parameter your specified

    public localDocumentURL:string;             //  A URL which references the temporary local video clip
}
```

Note that the localDocumentURL is **local** to the mobile device; it has no meaning externally and can only be used to reference the temporary local copy of the video clip before it has been uploaded to the server and turned into a Document.

Inside an event handler you might use this API operation like this:

```js
    //
    //  Capture a short video clip and execute the callback when the clip is ready for upload.
    //
	client.recordVideo("TheVideoClip", 10, 2000, null, function(nativeOpRequest)
    	{
        	//
        	//	Remember the URL pointing to the local video clip; this could be used with the "client.playVideo"
            //  API call to allow the user to review the recording before submitting.
        	//
            client.data.localVideoURL = nativeOpRequest.localDocumentURL;
    	});
```

When the current Page is submitted the captured video Document will be uploaded along with the rest of the data (and given a property name of "TheVideoClip" in the response object.) If you are using a custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) you can add this item explicitly using a call like this:

```js
	var uploader = new Uploader(client);

	var nativeOpRequest = uploader.addAPIRequestFor("TheVideoClip");

```

In the callback of the [Uploader's](cbuser.md#custom-behavior-using-the-uploader) "start" method (which is called after the upload completes) you can extract the actual Document name which was assigned:

```js
    uploader.start(function(theUploader)
	{
        //
        //  The uploaded Audio Document name
        //
        var documentName = theUploader.responseObject.values[nativeOpRequest.responseObjectValueName];
	};

```


### returnToCallingPage()
#### Return to the calling Page

```js
returnToCallingPage(parameters: any, transition: string, transitionDuration: number): void
```

* parameters:any - (optional) A data item that will be passed back to the calling page in its "onStart" handler as the second argument "parameters".

* transition:string - (optional) triggers a one-second transition effect. May be one of the following: fade, slideDown, slideUp, slideRight, slideLeft, highlight or shake. To trigger a transition effect without needing to pass back parameters, simply use an empty JSON object (i.e. {}) as the first argument.

* transitionDuration:number - (optional) supply a specific duration for the transition effect to override the default one second. This value is expressed in milliseconds so to specify a half second transition duration, use 500 as the value.

This method can throw an exception in some situations, such as if there is not currently a "calling" page to return to.

Normally the calling Page will have its "onStart" callback invoked when a called page returns. You may cause this callback to be skipped by using a special value for "parameters" like this:

```js
client.returnToCallingPage(Client.SKIP_ONSTART);
```


### scanBarcode()
#### Allow the user to scan a QR or barcode and read the value

```js
scanBarcode(    responseObjectProperty:string,
                callback:Function):void
```

This API request programmatically simulates the operation of the [BarcodeReader](#barcodereader) Widget.

* responseObjectProperty:string - The name of the property added to the "response object" which will contain the results of the operation. 

<span style="padding-left:40px;">
This is analogous to the way the name of the [BarcodeReader](#barcodereader) Widget is used to give a name to the results in the response object.
</span>


* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The function has a single parameter which is an object of type NativeOperationRequest (see below). If successful it will contain the scanned value.
</span>


```
class NativeOperationRequest
{
    public responseObjectValueName:string;  //  The 'responseObjectProperty' parameter you specified

    public scannedValue:string;             //  The string value read by the barcode scanner
}
```

Inside an event handler you might use this API operation like this:

```js
    //
    //  Scan a barcode and call the callback function when done.
    //
	client.scanBarcode("TheScannedValue", function(nativeOpRequest)
    	{
        	//
        	//	Use the callback to display the scanned value to the user in a StaticText Widget
        	//
            var aTextWidget = client.getWidget("ScannedValue");
            aTextWidget.text = nativeOpRequest.scannedValue;
    	});
```

When the current Page is submitted the scanned value will be uploaded as a property in the response object (and given a property name of "TheScannedValue"). If you are using a custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) you can add this item explicitly using a call like this:

```js
	var uploader = new Uploader(client);

	var nativeOpRequest = uploader.addAPIRequestFor("TheScannedValue");

```







### select()
#### Convenience method to issue an asynchronous "select" to the Vantiq database

```js
select(typeName:string, parameters:any, succeed:Function):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#select_1).

* typeName:any - The name of a user-defined Type.
* parameters:any - "null" or an object containing the "query parameters" for the "select". (See [here](api.md#detail-select) for details.)
* succeed:Function - Called when the HTTP status code is 2XX. 

If successful the "succeed" callback returns a "response" which contains an array with results of the "select".

If the request fails the user will see an error popup that describes what happened.


```js
    //
    //  Specify the (optional) query parameters
    //
    var parameters = {
        where: {salary:{"$gt":50000}}
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  typeName:        The name of the Type  
    //  parameters:      "null" or an object containing the parameters for this request
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //
    client.select("Employee",parameters,function(response)
    {
        //
        //  At this point "response" is an array containing the objects returned for the "select".
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    });
```

### selectOne()
#### Convenience method to issue an asynchronous "select" to read a single item from the Vantiq database

```js
selectOne(typeName:string, resourceId:string, succeed:Function):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#selectone_1).

* typeName:any - The name of a user-defined Type.
* resourceId:string - The "_id" of the target object.
* parameters:any - An object containing any additional "query parameters" for the "select". (Usually null; see [here](api.md#detail-select) for details.)
* succeed:Function - Called when the HTTP status code is 2XX. 

If successful the "succeed" callback returns the selected object in "response". If an object matching the resourceId is not found the request will fail.

If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  This _id was probably obtained by a previous "select".
    //
    var theEmployeeId = "59776c4589133374df264357";
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  typeName:        The name of the Type 
    //  resourceId:      The "_id" of the object being loaded
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //
    client.selectOne("Employee",theEmployeeId,function(response)
    {
        //
        //  At this point "response" is the object found
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    });
```





### sendClientEvent()
#### Fire a "client event" to trigger a DataStream

```js
sendClientEvent(dataStreamName: string, dataObject: any): void
```

* dataStreamName: string - The name of a "Client Event" DataStream.

* dataObject: any - The object or array of objects that is to be emitted by the DataStream. (It must match the schema of the expected Type or DataObject.) 

More details may be found in the User's Guide [here](cbuser.md#data-streams) and [here](cbuser.md#client-event-detail).


### sendLocation()
#### Publish the device's current location data to the location tracking topic.

This function publishes a JSON object containing _latitude_, _longitude_, _altitude_ and other location properties to the well-known location tracking topic, **"/ars_collaboration/location/mc"**. It may be used for testing purposes when the device cannot be easily moved so will not generate location data. This call will publish the current location of a mobile device or a browser only if the user has given permission for location data (or publish simulated data if not). This function does not return a value. Note for Vantiq mobile app users: this function publishes to just the currently authenticated account, whereas the _TrackLocation_ App task publishes to all configured accounts.

```js
client.sendLocation();
```


### setCollaborationContext()
#### Set the "context" object when running under a Collaboration

```js
setCollaborationContext(context:any):any
```

See "getCollaborationContext()" above. When a Client is *not* running as a result of a Notification the Collaboration Context will be "null". But if the Client knows about a related Collaboration by some other mechanism it may call this method to tell the runtime system (and any Conversation Widgets in particular) to use the supplied context object to get the "id" of an active Collaboration. This "id" property may be used to load the active Collaboration, which in turn may contain a Conversation the Conversation Widget should participate in.

The "context" object should just contain a single "id" property.



### setInterval()
#### Create a repeating system timer event
```js
setInterval(callback:Function,milliseconds:number, parm1:any, parm2:any, ...):number
```

* callback: Function - A callback function to be executed when the timer expires

* milliseconds: number - The interval in milliseconds between executions of the callback. 

* parameters: any - An optional set of parameters to be passed to the callback function

This function is used in exactly the same manner as the well-known window.setInterval() function provided by the 
JavaScript runtime system. The only difference is that these interval timers will be automatically cleared when the 
Client terminates (if you haven't already done it yourself).

The timer will continue to fire at the indicated interval and will never stop unless you cancel it explicitly.
The function returns a numeric "handle" which uniquely identifies the timer and can be used 
to cancel it using the client.clearInterval() function.

Note that any outstanding interval timers that are not explicitly canceled will be canceled automatically when the 
Client completes execution. Timers which are created using the system function window.setInterval will **not** be 
canceled automatically, which is why you should use the client.setInterval function instead.

For example:

```js
//
//  Example of a 60-second interval timer
//
var theHandle = client.setInterval(function(a,b)
    {
        console.log("My Interval Timeout: " + a + " " + b);
    },60000,123,456);

```


### setTimeout()
#### Create a one-time system timer event

```js
setTimeout(callback:Function,milliseconds:number, parm1:any, parm2:any, ...):number
```

* callback: Function - A callback function to be executed when the timer expires

* milliseconds: number - The delay in milliseconds before the timer should expire.

* parameters: any - An optional set of parameters to be passed to the callback function

This function is used in exactly the same manner as the well-known window.setTimeout() function provided by the 
JavaScript runtime system. The only difference is that any un-expired timers that are still alive when the
Client terminates will be cleared automatically. 

The timer fires only once. The function returns a numeric "handle" which uniquely identifies the timer and can be used 
to cancel the timer before it expires using the client.clearTimeout() function.

Note that any outstanding un-expired timers that are not explicitly canceled will be canceled automatically when the 
Client completes execution. Outstanding timers which are created using the system function window.setTimeout will **not** be 
canceled automatically, which is why you should use the client.setTimeout function instead.

For example:

```js
//
//  Example of a 60-second one-time timer
//
var theHandle = client.setTimeout(function(a,b)
    {
        console.log("My Timeout: " + a + " " + b);
    },60000,123,456);

```


### showDocument()
#### Display a document (PDF, Audio, Video, Image or HTML)

```js
showDocument(   flavor:string, 
                url:string,
                callback:Function):void
```

This API request programmatically simulates the operation of the [DocumentViewer](#documentviewer) Widget.

* flavor:string - The "flavor" of the document to be displayed

<span style="padding-left:40px;">
The flavor must be one of "html", "pdf", "vaudio", "vimage" or "vvideo".
</span>

* url:string - The URL of the document to be displayed

<span style="padding-left:40px;">
This must either be the URL of a valid resource on the internet or a relative URL to a Document (e.g. "../../docs/manual.pdf").
</span>

There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).

* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The callback is only useful for knowing when the request is complete and the user is no longer viewing the document. 
</span>


Inside an event handler you might use this API operation like this:

```js
    //
    //  Display a document and call the callback function when done.
    //
	client.showDocument("pdf", "https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf", function(nativeOpRequest)
    	{
        	//  Request complete
    	});
```




### showHttpErrors()
#### Pop up a Dialog that reports an error from an Http request

```js
showHttpErrors(errors:any,cause:string):void
```

* errors:any - The "errors" object returned as the argument to the "failure" callback in an Http request.

* cause:any - A short string describing what the request you issued was doing. This will be incorporated into the error dialog to try to assist in debugging by giving some context.

For example, your Http request might look like this:

```js
    http.select(queryParameters,function(response)
    {
        //
        //  At this point "response" is an array containing the objects returned for the "select"
        //
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing a select on 'MyType'");
    });

```



### showMap()
#### Display a map and allow the user to select (tap) a location

```js
showMap(    responseObjectProperty:string,
            defaultLocation:any,
            mapType:string,
            minMapWidth:number,
            markers:any[],
            callback:Function):void
```

This API request programmatically simulates the operation of the [MapViewer](#mapviewer) Widget.

* responseObjectProperty:string - The name of the property added to the "response object" which will contain the results of the operation. 

<span style="padding-left:40px;">
This is analogous to the way the name of the [MapViewer](#mapviewer) Widget is used to give a name to the results in the response object.
</span>


* defaultLocation:any - The default location for the center of the map

<span style="padding-left:40px;">
This allows you to specify the starting location of the center of the map. It may be either a GeoJSON POINT object or
a simple JSON object with the properties "longitude" and "latitude".
</span>

* maptype:string - The map type

<span style="padding-left:40px;">
This value must be a valid map type, one of "Standard", "Hybrid" or "Satellite". (The default is "Standard".) You must specify this value using one of these three constants: MapViewer.MAPTYPE_STANDARD, MapViewer.MAPTYPE_HYBRID, MapViewer.MAPTYPE_SATELLITE.
</span>


* minMapWidthInMeters:number - The minimum map width in meters


* markers:any[] - An array describing markers which are to appear on the map

<span style="padding-left:40px;">
Here is an example of an array which describes two markers:

```
[
   {"label": "Space Mountain", "longitude": -117.917193, "latitude": 33.811379, color:"azure"},
   {"label": "Haunted Mansion", "longitude": -117.922675, "latitude": 33.811530, color:"magenta"}
]
```
</span>


* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The function has a single parameter which is an object of type NativeOperationRequest (see below). If successful it will contain the GeoJSON location value.
</span>


```
class NativeOperationRequest
{
    public responseObjectValueName:string;  //  The 'responseObjectProperty' parameter you specified

    public location:any;                    //  The GeoJSON location where the user tapped
}
```

Inside an event handler you might use this API operation like this:

```js
	var initialLocation = {
        "longitude": -117.917193, 
        "latitude": 33.811379
    };

    //
    //  Scan a barcode and call the callback function when done.
    //
	client.showMap("TheSelectedLocation", initialLocation, MapViewer.MAPTYPE_STANDARD, null, null, function(nativeOpRequest)
    	{
        	//
        	//	Use the callback to display the selected location value to the user in a StaticText Widget
        	//
            var aTextWidget = client.getWidget("Location");
            aTextWidget.text = JSON.stringify(nativeOpRequest.location);
    	});
```

When the current Page is submitted the selected location value will be uploaded as a property in the response object (and given a property name of "TheSelectedLocation"). If you are using a custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) you can add this item explicitly using a call like this:

```js
	var uploader = new Uploader(client);

	var nativeOpRequest = uploader.addAPIRequestFor("TheSelectedLocation");

```


### speakText()
#### Speak the supplied text

```js
speakText(text:string,callback:Function):void
```

* text: string - The text to be rendered as speech.
* callback: Function: - An optional callback function which will be called when the speech has completed.

This method will use Text-to-Speech to speak the supplied text. If spoken audio is in progress it can be aborted with a call to [cancelSpeaking()](#cancelSpeaking).




### startBLEScan()
#### Start scan for a Bluetooth Low Energy (BLE) device
```js
startBLEScan(config:any, success:function, error:function):void
```
This API request is available for Clients running on mobile devices in order to scan for and return BLE device scan data for a given manufacturer ID. The config parameter is a JSON object with three properties:

* manufacturerId (int): the Bluetooth manufacturer ID as found in the [Bluetooth Company Identifier](https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers/) reference page. This must be expressed as a decimal integer.
* timeout (int): amount of time in seconds to wait for a scan to return. When the timeout expires the scan will complete with the "ble.err.scantimeout" error code. If the timeout value is zero the scan will never time out.
* continuous (boolean): If "false" (the default) the BLE scan will automatically stop the first time data is captured from a device with the target manufacturerId. If "true" the scan will not stop until the timeout expires or [stopBLEScan](#stopblescan) is called. In this case the "success" callback will be invoked multiple times, once for each value captured. (Note that in this case data from the same BLE device may be returned multiple times; it is the developer's responsibility to eliminate duplicates.)

The scan will call the _success_ and _error_ functions as appropriate:

* success(result:any): the _success_ function is called when the scan discovers a BLE device advertisement from the specified manufacturer ID. (This will be only called once if "continuous:false" has been set.) The single parameter is a JSON object that contains the following properties:
    * data (string): the Advertising data **without** the first two bytes (the manufacturer/Company ID), returned as a string of hexadecimal digits
    * device (BluetoothDevice): An object which contains information about the responding BLE device. This object can contain these parameters:
        * name (string): the device name, if provided by the device
        * RSSI (int): the [device's power level](https://www.bluetoothle.wiki/rssi) at the receiver
        * macAddress (string): (Android only) the MAC address of the device, returned as a string of hexadecimal digits 
        * type (int): (Android-only) the [Bluetooth device type](https://docs.microsoft.com/en-us/dotnet/api/android.bluetooth.bluetoothdevicetype?view=xamarin-android-sdk-12)
        * deviceClass (int): (Android only) The [device class](https://developer.android.com/reference/android/bluetooth/BluetoothClass.Device) which gives a rough description of the kind of device
	
* error(error:any): the _error_ function is called when the scan either times out or encounters some other Bluetooth-related error. The single parameter is a JSON object that contains two properties:
    * code (string): contains one of the following string error codes:
        * ble.err.notsupported: Bluetooth not supported by this device.
        * ble.err.notenabled: Bluetooth not enabled on this device.
        * ble.err.scanningactive: BLE scanning is already active.
        * ble.err.nomanid: No manufacturerId specified in the configuration.
        * ble.err.scantimeout: BLE scan timed out after {value} seconds.
        * ble.err.browser: Bluetooth is not supported in the browser
        * ble.err.sc.notobj: The scanConfig parameter must contain an object
        * ble.err.sc.missing: The scanConfig object is missing a manufacturerId property
    * message (string): the localized string equivalent of the code value.
	
In "continuous:false" mode the _success_ function will return with data from the **first** device that matches the specified manufacturer ID and the scan will terminate.

In "continuous:true" mode the _success_ function will be called **multiple times** with data from every matching device that responds and the scan will continue until the timeout expires or [stopBLEScan](#stopblescan) is called.

Use the [stopBLEScan](#stopblescan) function to cancel a scan in progress. It is not necessary to call _stopBLEScan_ after the _error_ function from _startBLEScan_ is called.
	
Here is an example of how to use _startBLEScan_ in "continuous:false" mode to return a BLE advertisement from a Hewlett Packard (HP) device, which is Bluetooth Company ID 101:

```js
	var config = {
        manufacturerId: 101,
        timeout: 5,
        continuous: false
    };
    var wdg = client.getWidget("Status");	// text widget displaying scan status
    var rssi = client.getWidget("RSSI");	// text widget displaying device RSSI
    var name = client.getWidget("Name");	// text widget displaying device name
    
    wdg.text = "Scanning...";
    rssi.text = name.text = "";
    
    client.startBLEScan(config,
    	function(result) {
        	wdg.text = "Scan successful: " + result.data;
            var device = results.device;
        	if (device.RSSI) {
                rssi.text = "RSSI: " + result.RSSI;
            }
        	if (device.name) {
                name.text = "Name: " + result.name;
            }
    	},
    	function(error) {
        	wdg.text = "code=" + error.code + " message=" + error.message;
    	}
   );
```


### startGeofencing()
#### Start mobile device tracking for geofence violations

```js
startGeofencing(latitude:float,
	longitude:float,
	radius:float,
	desiredAccuracy:float,
	distanceFilter:float,
	level:string,
	publishTopic:string,
	alertOnExit:boolean,
	alertThreshold:int,
	alertTitle:string,
	alertBody:string):void
```
This API request is available for Clients running on mobile devices similar to how a collaboration [LocationTracking](apps.md#track) task initiates location tracking for the mobile device. Calling this function allows the Client to define a [geofence](https://en.wikipedia.org/wiki/Geo-fence), collect geolocation data when the device running the Client is in violation of the geofence, and display alerts to the user of the device.

* latitude - latitude of center of geofenced area
* longitude - longitude of center of geofenced area
* radius - radius of circular geofenced area, in meters

The _latitude_, _longitude_ and _radius_ parameters define a circular geofenced area.

* desiredAccuracy - desired accuracy of location measurements, in meters
* distanceFilter - minimum distance traveled to produce a new location reading, in meters
* level - granularity of location measurements, may be either 'fine' or 'coarse'

The _desiredAccuracy_, _distanceFilter_ and _level_ parameters indicate the accuracy of location data collected when the device is in violation.

* publishTopic - the topic on which location data are published

The _publishTopic_ parameter defines the Vantiq topic to which collected location data is published.

* alertOnExit - if true, track out-of-bounds violations, otherwise tracking in-bounds violations

The _alertOnExit_ parameter defines whether the geofence violations are determined by moving out-of-bounds, e.g. device moves out of a restricted area, or moving in-bounds, e.g. device moves into a restricted area.

* alertThreshold - time in violation before alert, in seconds

The _alertThreshold_ parameter defines the amount of time a device must be in violation before location data is published to the publishTopic. This allows the device to be in violation for the specified (presumably small) amount of time before the violation is recorded to try to prevent false positives.

* alertTitle - title text of warning presented to user once alertThreshold time reached, may be null for no title
* alertBody - body text of warning presented to user once alertThreshold time reached, may be null for no warning

The _alertTitle_ and _alertBody_ parameters allow the caller to present a UI notification to the device's user to indicate they are in violation of the geofence area. The alertTitle may be null if no notification title is needed. The alertBody is the text of the notification and may be null if no UI notification is needed.

Geolocation data of the format used in the [LocationTracking Collaboration Type Activity Pattern](apps.md#track) is collected starting when the device is in violation. In addition, the _latitude_, _longitude_ and _radius_ properties are added to each data. Once the _alertThreshold_ is reached, the collected data is published to the publishTopic when practicable but no more than once every 10 minutes and for as long as the device is in violation. The published data is an array of objects, with the specified format. Once the device is detected to be out of violation, collection of geolocation data is stopped and any remaining unpublished data is sent when practicable. If the device is returned to an out of violation state before the _alertThreshold_ is exceeded, any collected data is discarded. Please note that a Vantiq Rule must be written to respond to published location data to trigger appropriate responses to geofencing violations.

**Important operational note**: once _startGeofencing_ is called, geofence tracking will remain in effect until:

* a call to the [stopGeofencing](#stopgeofencing) function is made, or
* the Vantiq mobile app is terminated, either by the user or by the Android or iOS OS.

This will be the case even if the Client that makes the _startGeofencing_ call exits. The easiest way to ensure that geofence tracking is disabled is to add a call to _stopGeofencing_ in the **On End** Event Client properties. The **On End** Event definition is found in the Client Properties dialog under the **Events** tab.

### stopAudio()
#### Stop the playback of an in-progress 'playAudio' call

```js
playAudio(  callback:Function):void
```

This API request can be use to interrupt a "playAudio" API call currently in progress (so the user doesn't have to listen to the entire clip.) This is a NOP if there is no audio playback in progress.


* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The callback is only useful for knowing when the "stop audio" request has been processed.
</span>


Inside an event handler you might use this API operation like this:

```js
    //
    //  Cancel an in-progress "playAudio" call.  
    //
	client.stopAudio(function()
    	{
            //  Playback complete
    	});
```

### stopBLEScan()
#### Stop a Bluetooth Low Energy (BLE) scan in progress
```js
stopBLEScan():void;
```
Call the _stopBLEScan_ function to cancel a scan started by the [startBLEScan](#startblescan) function. This is a NOP if there is currently no scan in progress.

### stopGeofencing()
#### Stop mobile device tracking for geofence violations
```js
stopGeofencing():void;
```
Call the _stopGeofencing_ function to cancel geofence tracking started by the [startGeofencing](#startgeofencing) function.

### takePhoto()
#### Ask the user to take a photo and upload it to the server as a Document

```js
takePhoto(  responseObjectProperty:string,
            maxWidth:number=null,
            thumbnailSize:number=null,
            groupName:string=null,
            callback:Function):void
```

This API request programmatically simulates the operation of the [Camera](#camera) Widget.

* responseObjectProperty:string - The name of the property added to the "response object" which will contain the results of the operation. 

<span style="padding-left:40px;">
This is analogous to the way the name of the [Camera](#camera) Widget is used to give a name to the results in the response object.
</span>

* maxWidth:number - Restrict the size of the captured image (optional)

<span style="padding-left:40px;">
Camera images returned by mobile devices can be quite large so can cause long upload and download times. To restrict the size of the image returned you can supply a non-null value for the _maxWidth_ parameter. If the markup image width is larger than the _maxWidth_ parameter, the image is scaled such that the width matches the _maxWidth_ value and the height is scaled to match the aspect ratio of the markup image. If no value is provided for the _maxWidth_ parameter, the image is returned unmodified.
</span>

* thumbnailSize:number - Create a thumbnail image for the captured image (optional)

<span style="padding-left:40px;">
To create a second 'thumbnail' version of the image you can supply a non-null value for the _thumbnailSize_ parameter. If the _thumbnailSize_ parameter is specified, an image is created with its width or height, whichever is greater, scaled such that it matches the _thumbnailSize_ value and the lesser of the width or height is scaled to match the aspect ratio of the captured image. If no value is provided for the _thumbnailSize_ parameter, no thumbnail image is created.
</span>

<span style="padding-left:40px;">
The uploaded thumbnail Document will have the same name as the uploaded image Document with a suffix of "Thumbnail" before the file extension.
</span>

* groupName:string - The name of the Group to which the uploaded Document should be assigned (optional)

<span style="padding-left:40px;">
When this request creates and uploads a Document it will be assigned to the indicated [Group](resourceguide.md#groups). This is useful for controlling which users will have access to the Document.
</span>

* callback - A function which will be called when the operation completes. (optional)

<span style="padding-left:40px;">
The function has a single parameter which is an object of type NativeOperationRequest (see below). It contains URLs which may be used to reference the image and thumbnail. Note that when the callback runs, the image has **not** yet been uploaded; it just means the image has been created and temporarily resides on the mobile device. Just like the [Camera](#camera) Widget the document won't be created until after a "default Submit" or custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) operation has completed.
</span>


```
class NativeOperationRequest
{
    public responseObjectValueName:string;      //  The 'responseObjectProperty' parameter your specified
    public responseObjectThumbnailName:string;  //  The name of the thumbnail images response object, generated
                                                //  by adding "Thumbnail" to the responseObjectValueName.

    public localDocumentURL:string;             //  A URL which references the temporary local image
    public localThumbnailURL:string;            //  A URL which references the temporary local thumbnail
}
```

Note that these URLs are **local** to the mobile device; they have no meaning externally and can only be used to reference the temporary local copy of the images before they have been uploaded to the server and turned into Documents.

Inside an event handler you might use this API operation like this:

```js
    //
    //  Capture an image from the camera. Create a 150-pixel thumbnail image and
    //  execute the callback when the image is ready for upload.
    //
	client.takePhoto("TheCameraImage", null, 150, null, function(nativeOpRequest)
    	{
        	//
        	//	Use the callback to display a thumbnail of the captured image in a StaticImage widget
        	//	before it is uploaded.
        	//
        	var thumbnailWidget = client.getWidget("TheThumbnailWidget");
        	thumbnailWidget.url = nativeOpRequest.localThumbnailURL;
    	});
```

When the current Page is submitted the captured image Document will be uploaded along with the rest of the data (and given a property name of "TheCameraImage" in the response object.) If you are using a custom [Uploader](cbuser.md#custom-behavior-using-the-uploader) you can add this item explicitly using a call like this:

```js
	var uploader = new Uploader(client);

	var nativeOpRequest = uploader.addAPIRequestFor("TheCameraImage");

```

In the callback of the [Uploader's](cbuser.md#custom-behavior-using-the-uploader) "start" method (which is called after the upload completes) you can extract the actual Document name which was assigned:

```js
    uploader.start(function(theUploader)
	{
        //
        //  The uploaded Image Document name
        //
        var documentName = theUploader.responseObject.values[nativeOpRequest.responseObjectValueName];
        //
        //  The uploaded Thumbnail Document name
        //
        var thumbnailName = theUploader.responseObject.values[nativeOpRequest.responseObjectThumbnailName];
	};

```



### terminate()
#### Terminate the current Client


```js
terminate(withResponse:boolean = false): void
```

* withResponse:boolean - (optional) Declares that this Client sent some kind of response before the termination so it 
can be considered "done". If this happens in a Client running in the mobile device which was launched from a Notification 
then the Notification will be removed from the "inbox".

The effect of doing a "terminate" depends on how the Client was launched, but it generally means "go back to where 
you where before the Client started".



### terminateWithDialog()
#### Terminate the current Client after showing a Dialog to the user


```js
terminateWithDialog(withResponse:boolean, msg:string, title:string=null): void
```

* withResponse:boolean - Declares that this Client sent some kind of response before the termination so it 
can be considered "done". If this happens in a Client running in the mobile device which was launched from a Notification 
then the Notification will be removed from the "inbox".
* msg:string - The body of the message to be shown in the dialog.
* title:string - The title of the dialog; this parameter is optional; by default the title will be "CLient Terminating".
 
Terminate the Client after showing a popup dialog to the user so they can be told why the Client is terminating. The string parameters may be supplied as "localization keys" instead of literal text (See [here](cbuser.md#localizing-clients) for a complete discussion of the Client localization process.)

The effect of doing a "terminate" depends on how the Client was launched, but it generally means "go back to where 
you where before the Client started".



### uploadDataURL()
#### Upload a Vantiq Document encoded as a "data URL"

This method uploads the supplied "data URL" to the named Vantiq document. For an explanation of "data URLS" you can read [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs).



```js
uploadDataURL(dataURL:string, documentName:string, callback:Function)
```

* dataURL:string - The "data URL" string that can be turned into a Document object and uploaded.  There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).
* documentName:string - The name of the document 
* callback: Function - (Optional) A function which will be called after the uploaded data has been saved to a document object. The function has two arguments which are described in the example below.

```js
//
//  This function is called when the user clicks the 'Button5' button. (Note
//  that 'this' points to the button itself.)
//
function Client_Start_Button5_onClick(client,page,extra)
{
    	// "Hello, World!" encoded in base64
    	var dataURL = "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==";

    //
    //  "status" contains either "success" or "error".
    //  "detail" contains either the name of the saved document (if "status" == "success") or an
    //  error message (if "status" == "error").
    //
    client.uploadDataURL(dataURL,"MyUploadedDocument.txt",function(status, detail)
    {
        if (status == "success")
        {
            console.log("File has been uploaded to document '" + detail + "'");
        }
        else
        {
            console.log("Upload failed with error: " + detail);
        }     
    });
};
```












### uploadDocument()
#### Upload a file selected by the user to a Vantiq Document.

This function causes the browser to pop up a "file selection dialog" which prompts the user to select a single file that
should be uploaded to a "document". A second popup dialog will prompt for the "name" that should be given to the document.


```js
uploadDocument(callback: Function, useOriginalFileName:boolean, forceOverwrite:boolean, prefix:string)
```

* callback: Function - (Optional) A function which will be called after the uploaded file has been saved to a document object. The function has two arguments which are described in the example below.
* useOriginalFileName: boolean - (Optional) If it is set to true, do not present the document name input dialog, just try to use the original file name as the document name.
* forceOverwrite: boolean - (Optional) if it is set to true, skip the warning message dialog if document with the same name already exists. The new uploaded file will overwrite existing document with the same name.
* prefix: string - (Optional) If it is specified, its value will be prepended to the beginning of document name. To put the new upload document into a folder, includes a "/" in the prefix. E.g. "tickets/".

 
```js
    //
    //  When "false" (the default) the user will be prompted for the document name to use. If "true" the 
    //  original file name will be used to name the document.
    //
    var useOriginalFileName = false;

    //
    //  When "false" (the default) the user will be warned if an existing document will be overwritten. If
    //  "true" the warning message will be skipped.
    //
    var forceOverwrite = false;

    //
    //  When "null" (the default) the document name will be used as specified. Otherwise the string will
    //  be prepended to the the beginning of document name. 
    //
    var prefix = null;

    //
    //  Ask the user to select a file to be uploaded
    //
    client.uploadDocument(function(status, detail)
    {
        //
        //  "status" contains either "success" or "error".
        //  "detail" contains either the name of the saved document (if "status" == "success") or an
        //  error message (if "status" == "error").
        //

        if (status == "success")
        {
            console.log("File has been uploaded to document '" + detail + "'");
        }
        else
        {
            console.log("Upload failed with error: " + detail);
        }
    }, useOriginalFileName, forceOverwrite, prefix);
```

### update()
#### Convenience method to issue an asynchronous "update" to update a single existing item in the Vantiq database

```js
update(typeName:string, data:any, resourceId:string, succeed:Function):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#update_1).

* typeName:any - The name of a user-defined Type.
* data:any - The object to be updated.
* resourceId:string - The "_id" of the object being updated.
* succeed:Function - Called when the HTTP status code is 2XX. 

If successful the "succeed" callback returns the updated object in "response". 

If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  An object which contains only the properties you intend to update
    //
    var updatedEmployeeData = {
        "salary": 50000
    };
    
    //
    //  The "_id" of the record you intend to update (probably obtained from a previous query).
    //
    var theEmployeeId = "59776c4589133374df264357";
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  typeName:        The name of the Type 
    //  data:            The object being updated.
    //  resourceId:      The "_id" of the record being updated
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //
    client.update("Employee",updatedEmployeeData,theEmployeeId,function(response)
    {
        //
        //  At this point "response" is the updated properties of the object
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    });
```






### upsert()
#### Convenience method to issue an asynchronous "upsert" to update or insert an item in the Vantiq database

```js
upsert(typeName:string, data:any, parameters:any, succeed:Function):void
```

The [Http](#http) class provides complete low-level support for interactions with the Vantiq database. In some cases Client convenience methods like this one offer a variation which is simpler to use (but with less complete features). If this method does not support a feature you need you should refer to its [Http equivalent](#upsert_1).


* typeName:any - The name of a user-defined Type.
* data:any - The object to be updated or inserted; "_id" must set set to do an update.
* succeed:Function - Called when the HTTP status code is 2XX. 

If successful the "succeed" callback returns the updated or inserted object in "response". 

If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  A variable which contains the object to be inserted or updated. 
    //
    //  Important! This Type *must* have a naturalKey declared, and the value of the naturalKey must
    //  appear in this object.
    //
    var upsertedEmployee = {
        firstName: "John",
        lastName: "Smith",
        salary: 50000
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  typeName:        The name of the Type 
    //  data:            The object being inserted or updated.
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //
    client.upsert("Employee",upsertedEmployee,function(response)
    {
        //
        //  At this point "response" is the updated object
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    });  
```


### validate()
#### Start validation process on an array of Widgets.

```js
validate(widgets:Widget[]):boolean
```

The process of "validating input data" will automatically be triggered whenever the user does a "submit" for a Page. However you can also validate a specified set of Widgets at a time of your own choosing by calling this method. The "validate()" method will return "true" if all of the Widgets successfully passed all validation tests.

See [here](cbuser.md#field-validation) for a complete discussion of the validation process.

* widgets: Widget[] - You must specify an array of Widgets to be validated.

Validation can also be triggered programmatically by invoking the current Page's "validate()" method; if the method returns "true' then the validation was successful.




### 'On Start' Event

The Client 'On Start' Event is fired when a Client first starts up.

The code will be wrapped in a function with a signature of the form:

```
Client_onStart(client)
```

where both "this" and "client" point to the Client object.

For a discussion of the Client startup process and the sequence in which events are fired see [here](cbuser.md#client-startup).


### 'On End' Event

The Client 'On End' Event is fired right before the Client terminates execution.

The code will be wrapped in a function with a signature of the form:

```
Client_onEnd(client)
```

where both "this" and "client" point to the Client object.

This handler might be used if you need to do any special cleanup before the Client completes.





### 'On Assets Loaded' Event

The Client 'On Assets Loaded' Event is fired after all the CSS and JavaScript assets you have specified (if any) have
completed loading. (This event will not be fired unless you have specified at least one asset.)

The code will be wrapped in a function with a signature of the form:

```
Client_onAssetsLoaded(client)
```

where both "this" and "client" point to the Client object.

Note that since this event is asynchronous it is impossible to know *when* it will fire during startup.
For a discussion of the Client startup process and the sequence in which events are fired see [here](cbuser.md#client-startup).





### 'On Network Status Changed' Event

The Client 'On Network Status Changed' Event is fired when the state of the mobile device's network connection changes. 

The code will be wrapped in a function with a signature of the form:

```
Client_onNetworkStatusChanged(client, extra)
```

where both "this" and "client" point to the Client object. The 'extra' parameter is an object with a single property, 'isNetworkActive', which is 0 when the device is offline and 1 when the device is online.

For a discussion of running Clients in "offline mode"  see [here](cbuser.md#offline-operation).


## DataObject
A description of DataObjects and how they are used can be found [here](cbuser.md#data-objects).

This section describes some useful methods defined on all DataObjects.

### copyMatchingData(obj:any):void
#### Copy any properties from the supplied object which are defined in the DataObject

```js
copyMatchingData(obj:any): void
```

This method can be used to initialize all the properties within a DataObject from a JavaScript object. Any properties defined in the DataObject which are found in the supplied object will be copied. For example:

```js
page.data.MyDataObject.copyMatchingData(myObject);
```


### initializePropertyToDefaultValue(propertyName:string):void
#### Initialize the indicated property to its default value

```js
initializePropertyToDefaultValue(propertyName:string): void
```

This method can be used to initialize a single property within a DataObject to its default value. For example:

```js
page.data.MyDataObject.initializePropertyToDefaultValue("myProperty");

page.data.initializePropertyToDefaultValue("anotherProperty");

```

### initializeToDefaultValues():void
#### Initialize all properties within the DataObject to their default values

```js
initializeToDefaultValues(): void
```

This method can be used to initialize all the properties defined within a DataObject to their default values. For example:


```js
page.data.MyDataObject.initializeToDefaultValues();
```



## DataStream
A description of DataStreams and their uses can be found [here](cbuser.md#data-streams-detail) and [here](cbuser.md#data-streams).

This section describes the properties defined on the DataStream object; these objects are defined in the Client Builder and may not be changed at runtime. 

### addEventHandler()
#### Add an event handler to a dynamically created DataStream


```js
addEventHandler(eventName:string, callback:Function)
```

* eventName: string - The name of the event; at present the only accepted value is "onDataArrived"
* callback: Function - A Javascript function that accepts the standard 2 parameters for a DataStream (client, data)


This is useful if you have dynamically created a DataStream at runtime and you need to add an event handler as well.


```js
    //
    //  Create a dynamic "Publish Event" DataStream
    //
    var pep = new PublishEventParameters();
    pep.topic = "/ADynamicTopic";
    client.data.peds = client.createPublishEventDataStream(pep);

    client.data.peds.addEventHandler("onDataArrived",function(client,data)
    {
      console.log("onDataArrived: data value = ", data.aProperty);
    });
```


### isPaused:boolean
#### Is this DataStream "paused" or "running"?

A DataStream may be "paused" by setting this value to "true" and resumed by setting it to "false". A DataStream which has been "paused" will not receive any events or data.

Note that you should **not** use "isPaused=true" in any of the "On Start" events that get run when the Client starts up. (This means the Client "On Start" event as well as the "On Client Start" and "On Start" events of the "Start" page.) Because of the asynchronous nature of the websocket connections all the DataStreams will be reset to "isPaused=false" automatically at startup.

Instead there is a special boolean property on each DataStream just for this purpose; on the Data Stream property sheet there is a checkbox called "Pause Data Stream at Client start". If you click this checkbox then the DataStream will start up in the "isPaused=true" state and it will be up to your Client to explicitly resume it later using "isPaused=false".

### name:string
#### The unique name of the DataStream


### remove():void
#### Remove a DataStream which has been dynamically created

```js
remove(): void
```

DataStreams which have been dynamically created can be deleted by calling their "remove" method. This method will throw an exception if invoked a "static" DataStream which was not created ar runtime.,

### restart():void
#### Restart a "Timed Query" or "Paged Query" DataStream

```js
restart(): void
```

"Timed Query" Data Streams will wake up at regularly scheduled intervals and re-run their query. You can programmatically cause the timer to pop early, which will re-run the query and schedule the next query after the update interval. This could be used like this:


```js
var ds = client.getDataStreamByName("MyTimedQueryDataStream");
ds.restart();
```

"Paged Query" Data Streams can only be used with the Data Table widget and we used to display Types with a large number of records by querying for only a single page of records at a time. In this case the "restart()" method just reloads the data starting at the first page.

### uuid:string
#### The UUID of the DataStream



### 'On Data Arrived' Event

A DataStream's 'On Data Arrived' Event provides a way to "listen in" and even modify the data that flows into
a DataStream.

The code will be wrapped in a function with a signature of the form:

```
DataStream_<datastreamName_onDataArrived(client,data)
```

where "this" points to the DataStream object and "client" points to the Client object. "data" is the
data which is about to be sent to any Widgets which are bound to the DataStream. This will either be an Object
or an array of Objects depending on the nature of the DataStream.

You are allowed to modify the data before the bound widgets see it as long as you don't change the basic form.


## Http
This section describes the methods defined on the Http object; these are used to make an asychronous request to the Vantiq server. In general you instantiate one Http object for every request.

<a name="common"></a>
#### Basic Information
More detailed information on crafting a REST API request can be found in the [API Reference Guide](api.md).

An Http request to the Vantiq database is always asynchronous and is not complete until it either succeeds or fails, at which time one of the caller-supplied callback functions will be invoked. See callback examples in the sections below.

A request is "successful" if the Http status code is 200 (really 2xx); the "succeed" callback will be called with a single argument whose meaning depends on the type of operation you requested.

A request has "failed" if the Http status code is something other than 2xx; the "failure" callback will be called with an "error object" produced by the server that contains information about why the failure occurred. In general you will want to call the [showHttpErrors](#showhttperrors) method to display the error to the user.



### aggregate()
#### Issue an asynchronous "aggregate" to the Vantiq database

```js
aggregate(pipeline:any[], succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* pipeline:any[] - An array containing the "aggregation operations" for the "aggregate". (See [here](https://docs.mongodb.com/manual/meta/aggregation-quick-reference/) for details.)
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

If successful the "succeed" callback returns a "response" which contains an array with results of the "aggregate".

If the mobile device is currently in "offline mode" (because the network is unavailable) the request will fail with a special HTTP status code of 555.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do a "select" on our Type
    //
    http.setVantiqUrlForResource("Employee");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  Specify the array of aggregation pipeline operations
    //
    var pipeline = [
                       {"$match":{ "salary": { "$gt":  50000 }}},
                       {"$match":{ "salary": { "$lt":  100000 }}}
                   ];

    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  pipeline: An array containing the pipeline operations
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.aggregate(pipeline,function(response)
    {
        //
        //  At this point "response" is an array containing the objects returned for the "select".
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing an aggregation on 'Employee'");
    });
```







### deleteAll()
#### Issue an asynchronous request to delete all the records of a given Type from the Vantiq database

```js
delete(parameters:any, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* parameters:any - An object containing the "query parameters" for the "delete". (See [here](api.md#detail-select) for details.)
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

If successful the "succeed" callback is called but there is nothing meaningful in the "response" object.

If the mobile device is currently in "offline mode" (because the network is unavailable) the operation is considered successful but the request is deferred and added to the Pending Uploads list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. In this case the response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain the deferred request.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do a delete all the records of a Type
    //
    http.setVantiqUrlForResource("Employee");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  parameters: "null" or an object containing the parameters for this request
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.deleteAll(null,function(response)
    {
        //
        //  The "response" object is meaningless in this case.
        //
        console.log("DELETE ALL SUCCESSFUL");
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Deleting all instances of 'Employee'");
    });
```



### deleteOne()
#### Issue an asynchronous request to delete a single record from the Vantiq database

```js
deleteOne(resourceId:string, parameters:any, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* resourceId:string - The "_id" of the target object.
* parameters:any - An object containing any additional "query parameters" for the "delete". (Usually null; see [here](api.md#detail-select) for details.)
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

If successful the "succeed" callback is called but there is nothing meaningful in the "response" object. It is important to note that the request will **not** fail if the record does not exist; in that case the request is a NOP.

If the mobile device is currently in "offline mode" (because the network is unavailable) the operation is considered successful but the request is deferred and added to the Pending Uploads list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. In this case the response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain the deferred request.


```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do a "selectOne" on the specified user Type
    //
    http.setVantiqUrlForResource("Employee");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();

    //
    //  This _id was probably obtained by a previous "select".
    //
    var theEmployeeId = "59776c4589133374df264357";
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  resourceId:      The "_id" of the object being deleted
    //  parameters:      "null" or an object containing the parameters for this request
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.deleteOne(theEmployeeId,null,function(response)
    {
        //
        //  The "response" object is meaningless in this case.
        //
        console.log("DELETE SUCCESSFUL");
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing a delete on a single 'Employee'");
    });
```






### execute()
#### Asynchronously execute a Procedure in the Vantiq database.


```js
execute(procedureArguments:any, procedureName:string, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* procedureArguments:any - An object containing the arguments required by the procedure.
* procedureName:string - The name of the Procedure to execute. (If the Procedure is defined in a service you should supply the "fully qualified" form of the name, i.e. "&lt;service>.&lt;procedurename>".)
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

You must have called setVantiqUrlForSystemResource() with a "resourceName" of "procedures" for this to work.

If successful the "succeed" callback returns the "return" value of the procedure "response". 

If the mobile device is currently in "offline mode" (because the network is unavailable) the operation is considered successful but the request is deferred and added to the Pending Uploads list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. In this case the response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain the deferred request.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do an "execute" of a Procedure
    //
    http.setVantiqUrlForSystemResource("procedures");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  Set the Procedure arguments by name. (You may also specify 'args' as an array where the
    //  parameters are given in the same order as in the Procedure definition (e.g. 'args = [10,20];').
    //  'args' must not be null.
    //
    var args = {
        a:1,
        b:2
    };
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  procedureArguments: The procedure arguments.
    //  procedureName:      The fully-qualified name of the Procedure.
    //  successCallback:    A callback function that will be driven when the request completes
    //                      successfully (i.e. a status code of 2XX)
    //  failureCallback:    A callback function that will be driven when the request does not complete
    //                      successfully.
    //
    http.execute(args,"MyService.MyProcedure",function(response)
    {
        //
        //  At this point "response" is results of the Procedure call
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Executing 'MyService.MyProcedure'");
    });
```



### executePublic()
#### Asynchronously execute a public Procedure in another namespace.


```js
executePublic(namespace:string, procedureArguments:any, procedureName:string, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* namespace:string - The namespace in which the Procedure resides
* procedureArguments:any - An object containing the arguments required by the procedure.
* procedureName:string - The name of the Procedure to execute. (If the Procedure is defined in a service you should supply the "fully qualified" form of the name, i.e. "&lt;service>.&lt;procedurename>".)
* succeed:Function - Called when the HTTP status code is 2XX.
* fail:Function - Called when the HTTP status code is something other than 2XX.

You must have called setVantiqUrlForSystemResource() with a "resourceName" of "public/&lt;namespace>/procedures" for this to work.

Note that in order for a Procedure to be marked "public" you must add "with ars_public=true" to the end of the PROCEDURE definition statement, like this:

```js
PROCEDURE MyService.MyPublicProcedure(a Integer, b Integer) with ars_public=true
```

If successful the "succeed" callback returns the "return" value of the procedure "response".

If the mobile device is currently in "offline mode" (because the network is unavailable) the operation is considered successful but the request is deferred and added to the Pending Uploads list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. In this case the response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain the deferred request.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    var namespace = "TargetNamespace";
    
    //
    //  Build the URL needed to do an "execute" of a Procedure
    //
    http.setVantiqUrlForSystemResource("public/" + namespace + "/procedures");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  Set the Procedure arguments by name. (You may also specify 'args' as an array where the
    //  parameters are given in the same order as in the Procedure definition (e.g. 'args = [10,20];').
    //  'args' must not be null.
    //
    var args = {
        a:1,
        b:2
    };
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  namespace:          The target namespace
    //  procedureArguments: The procedure arguments.
    //  procedureName:      The fully-qualified name of the Procedure.
    //  successCallback:    A callback function that will be driven when the request completes
    //                      successfully (i.e. a status code of 2XX)
    //  failureCallback:    A callback function that will be driven when the request does not complete
    //                      successfully.
    //
    http.executePublic(namespace, args,"MyService.MyPublicProcedure",function(response)
    {
        //
        //  At this point "response" is results of the Procedure call
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Executing 'MyService.MyPublicProcedure'");
    });
```


### executeStreamed()
#### Asynchronously execute a Procedure with streamed output.


```js
executeStreamed(procedureArguments:any, procedureName:string, succeed:Function, progress:Function, failure:Function, maxBufferSize:number=null, maxFlushInterval:number=null, options:any=null):void
```

This function is intended for use when executing Procedures with "streamed output". (This generally means a VAIL Procedure which returns a ["sequence"](rules.md#sequences) rather than an "array".) Rather than waiting for the entire result set to be complete a Procedure with streamed output can deliver the results in "chunks" so you can start receiving results before the Procedures has completed execution. As each additional chunk arrives the "progress" callback will be called with the cumulative results to that point. When the Procedure actually completes (and all the output is available) the "success" callback will be called with the final results.


* procedureArguments:any - An object containing the arguments required by the procedure.
* procedureName:string - The name of the Procedure to execute. (If the Procedure is defined in a service you should supply the "fully qualified" form of the name, i.e. "&lt;service>.&lt;procedurename>".)
* succeed:Function - Called when the Procedure has completed execution and the HTTP status code is 2XX.
* progress:Function - Called each time another "chunk" of output has arrived
* failure:Function - Called if the call fails for some reason
* maxBufferSize:number - The maximum size of the streaming buffer before a "flush" is triggered. Value is in bytes and must be between 512 and 1048576. (Default is 64K)
* maxFlushInterval:number -  The maximum interval between flushes (in milliseconds). A value of 0 means that this feature is disabled and only the buffer size is used to trigger a flush. A negative value means that data will be flushed on every write. Otherwise, a flush will be triggered once the interval is exceeded (regardless of the buffer size). (Default is 5000ms.)
* options:any - An optional object you may use to pass data to the callback methods

Both the "succeed" and "progress" callbacks receive a single object "results" with the following content:

* data - The cumulative data received (so far) as an array
* rawData - The cumulative raw data received for far as a string (this might be parseable as a complete array, but it might be truncated such that the parse would result in an error)
* options - value of the "options" parameter
* isComplete - a boolean set to "true" when no more callbacks are expected
* chunksReceived - (Progress Only) Total "chunks" received so far
* totalRowsReceived - (Progress Only) Total rows received so far
* newRowsReceived -(Progress Only) New rows received with this chunk
* firstNewRowIndex - (Progress Only) The index of the first new row in this chunk


```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do an "execute" of a Procedure
    //
    http.setVantiqUrlForSystemResource("procedures");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  Set the Procedure arguments by name. (You may also specify 'args' as an array where the
    //  parameters are given in the same order as in the Procedure definition (e.g. 'args = [10,20];').
    //  'args' must not be null.
    //
    var args = {
      a:1,
      b:2
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  procedureArguments: The procedure arguments.
    //  procedureName:      The fully-qualified name of the Procedure.
    //  successCallback:    A callback function that will be driven when the request completes
    //                      successfully (i.e. a status code of 2XX)
    //  progressCallback:   A callback function that will be driven when a new chunk has arrived, containing
    //                      the current cumulative output
    //  failureCallback:    A callback function that will be driven when the request does not complete
    //                      successfully.
    //
    client.executeStreamed(args, "MyService.MyStreamedProcedure",
        function(results)
        {
            console.log("SUCCESS: " + JSON.stringify(results));
        },
        function(results)
        {
            console.log("PROGRESS: " + JSON.stringify(results));
        },
        function(errors)
        {
            //
            //  This call will format the error into a popup dialog
            //
            client.showHttpErrors(errors,"Executing 'MyService.MyStreamedProcedure'");
        });
```



### executeStreamedPublic()
#### Asynchronously execute a public Procedure with streamed output in another namespace.

This function is intended for use when executing public Procedures with "streamed output". (This generally means a VAIL Procedure which returns a ["sequence"](rules.md#sequences) rather than an "array".) Rather than waiting for the entire result set to be complete a Procedure with streamed output can deliver the results in "chunks" so you can start receiving results before the Procedures has completed execution. As each additional chunk arrives the "progress" callback will be called with the cumulative results to that point. When the Procedure actually completes (and all the output is available) the "success" callback will be called with the final results.

```js
executeStreamedPublic(namespace:string,procedureArguments:any, procedureName:string, succeed:Function, progress:Function, maxBufferSize:number=null, maxFlushInterval:number=null, options:any=null):void
```

* namespace:string - The namespace where the public Procedure resides
* procedureArguments:any - An object containing the arguments required by the procedure.
* procedureName:string - The name of the Procedure to execute. (If the Procedure is defined in a service you should supply the "fully qualified" form of the name, i.e. "&lt;service>.&lt;procedurename>".)
* succeed:Function - Called when the Procedure has completed execution and the HTTP status code is 2XX.
* progress:Function - Called each time another "chunk" of output has arrived
* maxBufferSize:number - The maximum size of the streaming buffer before a "flush" is triggered. Value is in bytes and must be between 512 and 1048576. (Default is 64K)
* maxFlushInterval:number -  The maximum interval between flushes (in milliseconds). A value of 0 means that this feature is disabled and only the buffer size is used to trigger a flush. A negative value means that data will be flushed on every write. Otherwise, a flush will be triggered once the interval is exceeded (regardless of the buffer size). (Default is 5000ms.)
* options:any - An optional object you may use to pass data to the callback methods

Both the "succeed" and "progress" callbacks receive a single object "results" with the following content:

* data - The cumulative data received (so far) as an array
* rawData - The cumulative raw data received for far as a string (this might be parseable as a complete array, but it might be truncated such that the parse would result in an error)
* options - value of the "options" parameter
* isComplete - a boolean set to "true" when no more callbacks are expected
* chunksReceived - (Progress Only) Total "chunks" received so far
* totalRowsReceived - (Progress Only) Total rows received so far
* newRowsReceived -(Progress Only) New rows received with this chunk
* firstNewRowIndex - (Progress Only) The index of the first new row in this chunk

If the request fails the user will see an error popup that describes what happened.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    var namespace = "TargetNamespace";
    
    //
    //  Build the URL needed to do an "execute" of a Procedure
    //
    http.setVantiqUrlForSystemResource("public/" + namespace + "/procedures");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  Set the Procedure arguments by name. (You may also specify 'args' as an array where the
    //  parameters are given in the same order as in the Procedure definition (e.g. 'args = [10,20];').
    //  'args' must not be null.
    //
    var args = {
      a:1,
      b:2
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  procedureArguments: The procedure arguments.
    //  procedureName:      The fully-qualified name of the Procedure.
    //  successCallback:    A callback function that will be driven when the request completes
    //                      successfully (i.e. a status code of 2XX)
    //  progressCallback:   A callback function that will be driven when a new chunk has arrived, containing
    //                      the current cumulative output
    //  failureCallback:    A callback function that will be driven when the request does not complete
    //                      successfully.
    //
    client.executeStreamedPublic(namespace, args, "MyService.MyStreamedPublicProcedure",
        function(results)
        {
            console.log("SUCCESS: " + JSON.stringify(results));
        },
        function(results)
        {
            console.log("PROGRESS: " + JSON.stringify(results));
        },
        function(errors)
        {
            //
            //  This call will format the error into a popup dialog
            //
            client.showHttpErrors(errors,"Executing 'MyService.MyStreamedPublicProcedure'");
        });
```







### insert()
#### Issue an asynchronous "insert" to add a single item to the Vantiq database

```js
insert(data:any, parameters:any, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* data:any - The object to be inserted.
* parameters:any - An object containing any additional parameters for the "insert". (Usually null; see [here](api.md#detail-insert) for details.)
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

If successful the "succeed" callback returns the inserted object in "response". 

If the mobile device is currently in "offline mode" (because the network is unavailable) the operation is considered successful but the request is deferred and added to the Pending Uploads list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. In this case the response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain the deferred request.


```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do an "insert" on our Type
    //
    http.setVantiqUrlForResource("Employee");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  The object to be inserted
    //
    var aNewEmployee = {
        firstName: "John",
        lastName: "Smith",
        salary: 50000
    };
        
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  data:            The object being inserted.
    //  parameters:      "null" or an object containing the parameters for this request
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.insert(aNewEmployee,null,function(response)
    {
        //
        //  At this point "response" is the inserted object
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing an insert of a new Employee");
    });
```






### patch()
#### Issue an asynchronous request to "patch" a record in the Vantiq database

```js
patch(resourceId:string, patchInstructions:any[], parameters:any, succeed:Function, fail:Function):void;
```

See [above](#common) for details on the common features of Http requests such as this one.

* resourceId:string - The "_id" of the object being patched.
* patchInstructions:any[] - The array containing the patch instruction objects. (See [here](https://tools.ietf.org/html/rfc6902) for a detailed discussion of "patch" operations.)
* parameters:any - An object containing the "parameters" for the "patch". (See [here](api.md#detail-select) for details.)
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

If successful the "succeed" callback returns the updated object in "response". 

If the mobile device is currently in "offline mode" (because the network is unavailable) the operation is considered successful but the request is deferred and added to the Pending Uploads list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. In this case the response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain the deferred request.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do an "update" on our Type
    //
    http.setVantiqUrlForResource("Employee");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    var theEmployeeId = "57e567fe3bdecaa45d7486ba";

    var patchInstructions = [
        {
            op: "replace",
            path: "/salary",
            value: 100000
        }
    ];
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  data: The object being inserted.
    //  parameters: "null" or an object containing the parameters for this request
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.patch(theEmployeeId,patchInstructions,null,function(response)
    {
        //
        //  At this point "response" is the updated object
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing a patch of an existing Employee");
    });
```





### publish()
#### Asynchronously "publish" an event on a "topic" or "source"

```js
publish(data:any, topicOrSource:string, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* data:any - The "message object" to attach to the event
* topicOrSource:string - Either the "topic" for the "publish" (which must be of the form "/a/b/c") or the name of the target Source.
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

You must have called setVantiqUrlForSystemResource() with a "resourceName" of "topics" or "source" for this to work.

If successful the "succeed" callback returns but the "response" object has no meaning.

If the mobile device is currently in "offline mode" (because the network is unavailable) the operation is considered successful but the request is deferred and added to the Pending Uploads list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. In this case the response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain the deferred request.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do a "publish" on a Topic ('topics') or a Source ('sources')
    //
    http.setVantiqUrlForSystemResource("topics");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  The "message object" that is to be sent along with the "publish"
    //
    var theMessageObject = {
        a: 1,
        b: 2
    };
    
    //
    //  The name of the "topic" identifying this event
    //
    var topicName = "/a/b/c/d";
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  data:            The "message object" that is to be sent along with the "publish"
    //  topic:           The topic name identifying the event
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.publish(theMessageObject,topicName,function(response)
    {
        //
        //  "response" is meaningless for a "publish"
        //
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing a publish on a topic");
    });
```




### query()
#### Asynchronously execute a "query" against a Source object


```js
query(parameters:any, resourceId:string, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* parameters:any - An object containing the "query parameters" for the "select". (See [here](api.md#detail-select) for details.)
* resourceId:string - The name of the target "Source" to be queried
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

You must have called setVantiqUrlForSystemResource() with a "resourceName" of "sources" for this to work.

A "query" will only work on Sources which support them; you need to refer to the documentation of the individual Source type for information on the supported parameters.

If successful the "succeed" callback will provide the results of the query in the "response" variable.

If the mobile device is currently in "offline mode" (because the network is unavailable) the request will fail with a special HTTP status code of 555.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do an "query" of a Source
    //
    http.setVantiqUrlForSystemResource("sources");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    var parameters = {
        path: "/api/getData",
        query: {
            xxx: 100
        }
    };
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  parameters: The parameters for the query
    //  resourceId: The name of the target Source
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.query(parameters,"MySource",function(response)
    {
        //
        //  At this point "response" is results of the query
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Executing a query against a Source'");
    });
```





### select()
#### Issue an asynchronous "select" to the Vantiq database

```js
select(parameters:any, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* parameters:any - An object containing the "query parameters" for the "select". (See [here](api.md#detail-select) for details.)
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

If successful the "succeed" callback returns a "response" which contains an array with results of the "select".

If the mobile device is currently in "offline mode" (because the network is unavailable) the request will fail with a special HTTP status code of 555.


```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do a "select" on the specified user Type
    //
    http.setVantiqUrlForResource("Employee");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  Specify the (optional) query parameters
    //
    var parameters = {
        where: {salary:{"$gt":50000}}
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  parameters: "null" or an object containing the parameters for this request
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.select(parameters,function(response)
    {
        //
        //  At this point "response" is an array containing the objects returned for the "select".
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing a select on 'Employee'");
    });
```





### selectOne()
#### Issue an asynchronous "select" to read a single item from the Vantiq database

```js
selectOne(resourceId:string, parameters:any, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* resourceId:string - The "_id" of the target object.
* parameters:any - An object containing any additional "query parameters" for the "select". (Usually null; see [here](api.md#detail-select) for details.)
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

If successful the "succeed" callback returns the selected object in "response". If an object matching the resourceId is not found the request will fail.

If the mobile device is currently in "offline mode" (because the network is unavailable) the request will fail with a special HTTP status code of 555.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do a "selectOne" on the specified user Type
    //
    http.setVantiqUrlForResource("Employee");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();
    
    //
    //  This _id was probably obtained by a previous "select".
    //
    var theEmployeeId = "59776c4589133374df264357";
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  resourceId:      The "_id" of the object being loaded
    //  parameters:      "null" or an object containing the parameters for this request
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.selectOne(theEmployeeId,null,function(response)
    {
        //
        //  At this point "response" is the object found
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing a select on a single 'Employee'");
    });
```

### setVantiqHeaders()
#### Initialize the Http object with required authentication headers

```js
setVantiqHeaders():any
```

The method returns an object containing the HTTP headers which will actually be used in the request. The headers will contain the tokens needed to validate your request with the Vantiq server (acquired the last time you logged in.) 

You can modify these headers before submitting the request.


### setVantiqUrlForResource()
#### Initialize the Http object with the target database Type name

```js
setVantiqUrlForResource(databaseTypeName:string):string
```

* databaseTypeName: string - The name of one of your own existing database Type names. (You can **not** use this method to access system-defined Types or resources)

The method returns the URL which will actually be used in the request, something like:

```js
https://dev.vantiq.com/api/v1/resources/custom/MyType"
```



### setVantiqUrlForSystemResource()
#### Initialize the Http object with the target system resource name

```js
setVantiqUrlForSystemResource(resourceName:string):string
```

* resourceName: string - The resource name of the target resource (e.g. "types", "topics", "sources", etc.) (You can **not** use this method to access one of your own database Types.)

The method returns the URL which will actually be used in the request, something like:

```js
https://dev.vantiq.com/api/v1/resources/sources"
```





### update()
#### Issue an asynchronous "update" to update a single existing item in the Vantiq database

```js
update(data:any, resourceId:string, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* data:any - The object to be updated.
* resourceId:string - The "_id" of the object being updated.
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

If successful the "succeed" callback returns the updated object in "response". 


If the mobile device is currently in "offline mode" (because the network is unavailable) the operation is considered successful but the request is deferred and added to the Pending Uploads list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. In this case the response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain the deferred request.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do an "update" on our Type
    //
    http.setVantiqUrlForResource("Employee");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();

    //
    //  An object which contains only the properties you intend to update
    //
    var updatedEmployeeData = {
        "salary": 50000
    };
    
    //
    //  The "_id" of the record you intend to update (probably obtained from a previous query).
    //
    var theEmployeeId = "59776c4589133374df264357";
    
    //
    //  Execute the asynchronous server request. This expects 4 parameters:
    //
    //  data:            The object being updated.
    //  resourceId:      The "_id" of the record being updated
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.update(updatedEmployeeData,theEmployeeId,function(response)
    {
        //
        //  At this point "response" is the updated properties of the object
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing an update of an existing Employee");
    });
```






### upsert()
#### Issue an asynchronous "upsert" to update or insert an item in the Vantiq database

```js
upsert(data:any, succeed:Function, fail:Function):void
```

See [above](#common) for details on the common features of Http requests such as this one.

* data:any - The object to be updated or inserted; "_id" must set set to do an update.
* succeed:Function - Called when the HTTP status code is 2XX. 
* fail:Function - Called when the HTTP status code is something other than 2XX.

If successful the "succeed" callback returns the updated or inserted object in "response". 

If the mobile device is currently in "offline mode" (because the network is unavailable) the operation is considered successful but the request is deferred and added to the Pending Uploads list. This means that you cannot rely on any returned values in your code since the request will not have happened yet. In this case the response object contains only two properties: "offlineMode" with a boolean value of "true" and "request" which will contain the deferred request.

```js
    //
    //  Create an instance of the Http class to execute our server request
    //
    var http = new Http();
    
    //
    //  Build the URL needed to do an "upsert" on our Type
    //
    http.setVantiqUrlForResource("Employee");
    
    //
    //  Add the Authorization header to the request
    //
    http.setVantiqHeaders();

    //
    //  A variable which contains the object to be inserted or updated. 
    //
    //  Important! This Type *must* have a naturalKey declared, and the value of the naturalKey must
    //  appear in this object.
    //
    var upsertedEmployee = {
        firstName: "John",
        lastName: "Smith",
        salary: 50000
    };
    
    //
    //  Execute the asynchronous server request. This expects 3 parameters:
    //
    //  data:            The object being inserted or updated.
    //  successCallback: A callback function that will be driven when the request completes
    //                   successfully (i.e. a status code of 2XX)
    //  failureCallback: A callback function that will be driven when the request does not complete
    //                   successfully.
    //
    http.upsert(upsertedEmployee,function(response)
    {
        //
        //  At this point "response" is the updated object
        //
        console.log("SUCCESS: " + JSON.stringify(response));
    },
    function(errors)
    {
        //
        //  This call will format the error into a popup dialog
        //
        client.showHttpErrors(errors,"Doing an upsert of an Employee");
    });  
```




## Page

This section describes the functions and properties of the "Page" object. There is always a "Page" object available that represents each of your Pages at runtime; it is usually accessible through the "page" argument of event handlers.


### adjustPopupSizeAndPosition()
#### Adjust size and position of a "popup" page if necessary

Popup pages are automatically sized and centered when opened, even if you have dynamically changed its contents in the "start page" callback. If you change the contents dynamically after the Page is open (such as in response to some event) you can still force it to be re-sized and re-positioned by calling this method.



### children
#### A list of Widgets defined on the Page

```js
children: Widget[]
```

The Widgets in the array are the "top level" Widgets for the Page; if one of these is a WidgetContainer you can drill into **its** list of "children" if necessary.



### clearValidationErrors()
#### Clear any pending validation errors on all widgets on the Page

```js
clearValidationErrors():void
```

This method allows you to reset any pending "validation errors" for all the Widgets on this Page. (The errors will re-appear the next time the Widgets are validated unless the values are changed.)

See [here](cbuser.md#field-validation) for a complete discussion of the validation process.





### data
#### "page.data" refers to the DataObject for a particular Page

```js
data: DataObject
```

In most cases an event handler will pass you a "page" variable that points to the current Page.




### defaultSubmit()
#### Start a "default submit" of the current Page

```js
defaultSubmit(submitValue:number):boolean
```

* submitValue:number - The "submit value" that should be saved in the response object.

If the user clicks a button with no "on click" event handler it starts a process called a "default submit". (This is where all the values from the current page are used to create a "response object" which will be sent to the server via a "publish" on a resource event (usually a topic) using the default "responseResource/responseResourceId" values for the current Page, at which point the Client will terminate.)

This method can be used to programmatically simulate this "default submit" behavior. This might be useful if you wanted a "default submit" but needed to take some action first.




### hideCancelButton()
#### Hide the "X" in the upper-right-hand corner of a popup Page

By default a popup Page will show an "X" button in the upper-right-hand corner of a popup Page which the user can use to dismiss the popup. If for some reason you don't want this to appear you can call this method in the Page's "onStart" handler:

```js
this.hideCancelButton();
```


Note that when the user uses the "X" to dismiss a popup it will be as if you had called

```js
client.closePopup("CANCEL");
```






<!-- Do not document at this time
    //
    //  Return an object that contains the parameters for the Client (if there were any).
    //
    get parameters(): DataObject
    {
        return this.aps.parameters;
    }

    //
    //  Returns the current "device id" (it if has a value for the current platform).
    //
    public getDeviceId():string
    {
        return "";
    }

    //
    //  Returns the current "device name" (it if has a value for the current platform).
    //
    public getDeviceName():string
    {
        return "Browser";
    }

    //
    //  Returns the "state object" passed in with the Notification that launched us if there was one.
    //
    public getStateObject():any
    {
        return null;
    }

    //
    //  Probably don't need to document this since it's an internal function
    //
    public abort(ex:any):void
    {
        this.aps.abort(ex);
    }
    
## DataObject ?


-->

### validate()
#### Start validation process on the current Page

```js
validate():boolean
```

The process of "validating input data" will automatically be triggered whenever the user does a "submit" for a Page. However you can also validate all the widgets on a Page at a time of your own choosing by calling this method. The "validate()" method will return "true" if all of the Widgets successfully passed all validation tests.

See [here](cbuser.md#field-validation) for a complete discussion of the validation process.




### 'On Client Start' Event

The Page's 'On Client Start' Event is fired only once when the Client first starts up.

The code will be wrapped in a function with a signature of the form:

```
Client_Start_onClientStart(client)
```

where "this" points to the Page object and "client" points to the Client object.

For a discussion of the Client startup process and the sequence in which events are fired see [here](cbuser.md#client-startup).


### 'On Start' Event

The Page's 'On Start' Event is fired every time a Page starts executing. (This includes when a Page is restarted after
 calling another Page who returned to it using client.returnToCallingPage().

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_onStart(client,parameters)
```

where "this" points to the Page object and "client" points to the Client object. "parameters" is optional and depends
on the client.goToPage() or client.returnToCallingPage() call responsible to invoking the Page.

For the "Start" page this event will be fired as part of the Client startup process; for a discussion
see [here](cbuser.md#client-startup).

### 'On End' Event

The Page 'On End' Event is fired right before the Page exits

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_onEnd(client)
```

where "this" points to the Page object and "client" points to the Client object.

This handler will be fired every time a Page exits and turns control over to another Page; this also applies when 
the Page is opened as a Popup and then closed. 

When a Client completes execution the last visible Page will have its "On End" handler fired as well, right before
the Client's "On End" handler (if any) is executed.

This handler might be used if you need to do any special cleanup before the Page completes.

### 'On Validation' Event

The Page's 'On Validation' Event is fired as a part of the "Validation" process which is 
described [here](cbuser.md#field-validation).

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_onValidation(client,vco)
```

where "this" points to the Page object and "client" points to the Client object. "vco" is the "Validation Control
Object" which is used to describe the current state of validation and to declare your own validation errors.

### 'On Context Menu'
The Page 'On Context Menu' Event is fired whenever the user selects an item from a page's or widget's optionally defined context menu.

The code will be wrapped in a function with a signature of the form:
```
Client_<page name>_onContextMenu(client,extra)
```

where "this" points to the Page object, "client" points to the Client object, and "extra" which is an object containing the _key_ and _label_ properties of the selected menu item.

Whenever a user selects a context menu item, whether it is associated with the Page-wide or a widget-specific context menu, the **On Context Menu** function is executed and the developer defines the Client interaction based on the _key_ of the "extra" parameter.

### 'On Swipe'
The Page 'On Swipe' Event is fired whenever the user either uses a swipe-left or swipe-right gesture when the Page is run on a mobile device.

The code will be wrapped in a function with a signature of the form:
```
Client_<page name>_onSwipe(client,direction)
```

where "this" points to the Page object, "client" points to the Client object, and "direction" is either _Page.LEFT_ or _Page.RIGHT_.

Use the 'On Swipe' function to provide Page navigation functionality that is natural for user's of mobile apps.








## TreeWidgetObject
These objects are used describe the contents of a [Tree](#tree) Widget. The objects are arranged in a strict hierarchy where each node has a single parent (except for the "root") and each node can have one or more children. Nodes with children may be opened and closed ("isExpanded"). Single nodes may be selected (if "selectableNodes" is set to "true").

For example, you might build a simple tree like this:

```js
var root = new TreeWidgetObject("The Root");

var cats = new TreeWidgetObject("Cats");
var dogs = new TreeWidgetObject("Dogs");

root.addChild(cats);
root.addChild(dogs);

cats.addChild("Miss Kitty Fantastico");
cats.addChild("Spot");

dogs.addChild("Snuff");
dogs.addChild("Zero");

var myTree = client.getWidget("TheTreeWidget");
myTree.root = root;
```
`
This section describes some useful methods and properties defined on all TreeWidgetObjects.

### constructor:(label:string,tooltip:string=null)

When instantiating a TreeWidgetObject you should always supply a "label". This label does not have to be unique, but it should be to avoid user confusion.

### addChild(two:TreeWidgetObject):TreeWidgetObject

Add a node to another (which will become its parent).

### children:TreeWidgetObject[]

A read-only list of the TreeWidgetObject's children.

### icon:string

You may enter a valid icon name such as "glyphicon-asterisk" or "fa-automobile". For a list of valid icons see the Client Builder property sheet.  The default is "null" which means the node has no icon.


### isExpanded:boolean

If the node has children this lets you control whether it is open or closed.

### isSelected:boolean

Only one node may be selected at a time.

### label:string

The TreeWidgetObject's label.

### menuObjects:MenuObject[]

You may specify a context menu for any node - the MenuObjects are the same ones used by the [MenuBar](#menubar) Widget.

### parent:TreeWidgetObject

This node's parent - all nodes have a parent except the root.

### remove():void

Remove this node from its parent.

### removeChild(two:TreeWidgetObject):void

Remove the indicated child from this node.

### sortChildrenByLabel(ascending:boolean=true)

For a node with children this causes them to be sorted by their label.

### tooltip:string

The tooltip which would be displayed when hovering the mouse over the node.


## Uploader

This section describes the Uploader class which allows you to construct a request to upload specific scalar and media data to the Vantiq server. Before reading this section you should refer [here](cbuser.md#uploading-data-to-the-server) which explains what the Uploader does and why you might want to use it.

To use the Uploader you must instantiate an instance like this:

```
var uploader = new Uploader(client);
```

You then tell the Uploader what the responseObject should contain by calling various methods. When ready you call
the "start" method which will begin uploading the data to the server; when the request is done a callback function will be called,


### addAPIRequestFor(responseObjectProperty:string):boolean
#### Add request to upload the "media data" from the indicated native operation request.


```js
uploader.addAPIRequestFor("MyCameraRequest");
```

The "responseObjectProperty" must reference a previously issued API native operation request such as "client.takePhoto".



### addRequestFor(widgetName:string):boolean
#### Add request to upload the "media data" from the indicated widget.


```js
uploader.addRequestFor("MyCameraWidget");
```

The named Widget must be a "media" Widget that captures and uploads binary data (AudioRecorder, Camera, ImageMarkup or VideoRecorder).



### addRequestsForClient():boolean
#### Add request to upload the "media data" from all suitable widgets in the Client

```js
uploader.addRequestsForClient();
```

This tells the Uploader that you want to upload the contents of all the "media" Widgets in your client (AudioRecorder, Camera, ImageMarkup or VideoRecorder).



### addRequestsForCurrentPage():boolean
#### Add request to upload the "media data" from all suitable widgets on the current Page

```js
uploader.addRequestsForCurrentPage();
```


### addRequestForDataURL():void
#### Add request to upload the contents of the "data URL" to a document

```js
uploader.addRequestForDataURL(dataURL:string, documentName:string);
```

"Data URLs" are strings of the form

```
data:[<mediatype>][;base64],<data>
```

The <mediatype\> is a MIME type string, such as 'image/png' for a PNG image file. If omitted, it defaults to "text/plain;charset=US-ASCII". If the data is simply text, you can just it embed directly as the <data\> portion. Otherwise, you can specify ";base64" and embed it as  base64-encoded binary data. For a more complete explanation of "data URLS" you can read [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs).



### addRequestsForPage(pageName:string):boolean
#### Add request to upload the "media data" from all suitable widgets on the indicated Page

```js
uploader.addRequestsForPage("MyPage");
```

### responseObject:any
#### The object which was sent as the "payload" for the "publish"

This property is readonly; it is only useful in the "completed" callback of the start() method, and will contain the payload that was sent along with the "publish". The completed response object will look something like this:

```js
{
    "responseResource": "topics", 
    "responseResourceId": "/capture/payload", 
    "responseTopic": "/capture/payload",       
    "submitValue": 999,
    "state": {},
    "values": {
        "Camera6": "rcs/image/54dc73a8-2030-4706-b9de-d59bd6703cc9.jpg",
        "InputString1": "xxx"
    },
    "arsInfo": {
        "localeLanguage": "en",
        "localeCountry": "us",
        "localeVariant": "*",
        "username": "81a32111-6398-4655-cea2-8f0658525a73",
        "deviceId": "e7ad48993ef11850",
        "deviceName": "Galaxy S9",
        "responseTimestamp": "2019-08-15T11:37:16.725-07:00",
        "responseLocation": {
            "longitude": -122.0660862,
            "latitude": 37.9068591
        },
        "clientName": "MyClient"
    }
}
```

(Note that "responseTopic" is redundant and is included for backwards compatibility; as of R1.34 it has been deprecated and replaced by responseResource and responseResourceId.)

### setResponseObject(responseObject:any=null, responseResource:string=null, responseResourceId:string=null):void
#### Set the "response object", "response resource type" and the "response resource id" to be published to the server

When a mobile client terminates it can publish a "resource event". This is specified by these two parameters:

* responseResource - this must be one of "topics", "services" or "sources"
* responseResourceId - this is the "id" of the resource event.

The most common case is when "responseResource" is set to "topics" and "responseResourceId" is set to the Topic to be published. 

If "responseResource" is set to "services" then "responseResourceId" must be of the form "&lt;serviceName>/&lt;inboundEventName>".

If "responseResource" is set to "sources" then "responseResourceId" must be the name of a Source.

Note that prior to R1.34 Clients could only publish to "topics". For backwards compatibility you may still call this method by only specifying "responseResource" without a "responseResourceId"; in that case it is assumed that you meant "topics" with the supplied name,



```js
var responseObject = {
        "a":1,
        "b":2
    };

uploader.setResponseObject(responseObject,"/the/target/topic");
```

It is recommended that you use setResponseObjectValues() method instead since it creates a complete responseObject which is more consistent with the preferred structure.

### setResponseObjectValues(submitValue:number, responseObjectValues:any, responseResource:string=null, responseResourceId:string=null):void
#### Initialize a "response object" with the submitValue, 'values' object and the "response topic" to be published to the server

When a mobile client terminates it can publish a "resource event". This is specified by these two parameters:

* responseResource - this must be one of "topics", "services" or "sources"
* responseResourceId - this is the "id" of the resource event.

The most common case is when "responseResource" is set to "topics" and "responseResourceId" is set to the Topic to be published. 

If "responseResource" is set to "services" then "responseResourceId" must be of the form "&lt;serviceName>/&lt;inboundEventName>".

If "responseResource" is set to "sources" then "responseResourceId" must be the name of a Source.

Note that prior to R1.34 Clients could only publish to "topics". For backwards compatibility you may still call this method by only specifying "responseResource" without a "responseResourceId"; in that case it is assumed that you meant "topics" with the supplied name,

```js
var responseObjectValues = {
        "a":1,
        "b":2
    };

uploader.setResponseObjectValues(345,responseObjectValues,"topics", "/the/target/topic");
```

This method will create a standard "responseObject" (containing all the standard 'arsInfo' data) and then set the "submitValue", "values" object and "topic" as requested.

Refer [here](cbuser.md#customized-uploads) for an example of using this in the context of a "custom upload".


### start(completedFunction:Function):boolean
#### Start the upload of the requested data and response object

```js
uploader.start(function(theUploader)
    {
        //
        //  Upon completion the Widgets will contain the name of the target Documents where
        //  the media was saved.
        //
        var cameraWidget = client.getWidget("MyCameraWidget");
        client.infoDialog("DocumentName=" + cameraWidget.documentName);
    });
```








# Widget Hierarchy

This section describes the functions and properties of objects in the "Widget" hierarchy. 

In general, the list of properties described here should match those that appear on the "property sheet" for each type of Widget.

The Widgets are arranged in a class hierarchy which is shown below; note that only "leaf" classes can be instantiated.

* [Widget](#widget)
    * [DataStreamWidget](#datastreamwidget)
        * [BarChart](#barchart)
        * [Calendar](#calendar)
        * [ColumnChart](#columnchart)
        * [DataTable](#datatable)
        * [DynamicMapViewer](#dynamicmapviewer)
        * [FloorplanViewer](#floorplanviewer)
        * [Gauge](#gauge)
        * [LineChart](#linechart)
        * [ListViewer](#listviewer)
        * [NumberViewer](#numberviewer)
        * [PieChart](#piechart)
    * [ControlWidget](#controlwidget)
        * [AudioRecorder](#audiorecorder)
        * [BarcodeReader](#barcodereader)
        * [Button](#button)
        * [Camera](#camera)
        * [Chat](#chat)
        * [Checkbox](#checkbox)
        * [ComboBox](#combobox)
        * [Conversation](#conversation)
        * [Discussion](#discussion)
        * [DocumentViewer](#documentviewer)
        * [Droplist](#droplist)
        * [ImageMarkup](#imagemarkup)
        * [ImageViewer](#imageviewer)
        * [InputDate](#inputdate)
        * [InputDateTime](#inputdatetime)
        * [InputNumeric](#inputnumeric)
        * [InputInteger](#inputinteger)
        * [InputReal](#inputreal)
        * [InputObject](#inputobject)
        * [InputString](#inputstring)
        * [Label](#label)
        * [MapViewer](#mapviewer)
        * [MenuBar](#menubar)
        * [MenuButton](#menubutton)
        * [MultilineInput](#multilineinput)
        * [RadioButtons](#radiobuttons)
        * [SectionLabel](#sectionlabel)
        * [Signature](cbref.md#signature)
        * [Tree](#tree)
        * [VideoRecorder](#videorecorder)
    * [StaticHtml](#statichtml)
    * [StaticImage](#staticimage)
    * [StaticMarkdown](#staticmarkdown)
    * [StaticText](#statictext)
    * [WidgetContainer](#widgetcontainer)
        * [AccordionLayout](#accordionlayout)
        * [FixedLayout](#fixedlayout)
        * [FlowLayout](#flowlayout)
        * [GridLayout](#gridlayout)
        * [HorizontalLayout](#horizontallayout)
        * [ScrolledLayout](#scrolledlayout)
        * [TabbedLayout](#tabbedlayout)
        * [VerticalLayout](#verticallayout)




<hr>

## AccordionLayout
<span style="font-style:italic;">[Widget](#widget) &#x2192; [WidgetContainer](#widgetcontainer) &#x2192; AccordionLayout</span>

This is a "container" widget that arranges its visible children into a vertical "stack". The children are arranged from top-to-bottom in the order given by the "children" property. (The index of a child within its parent's "children" array determines its position in the stack.) However this differs from a VerticalLayout in that the container can be "open" or "closed" to control when the children can be seen.

The AccordionLayout is intended for use primarily in a "side bar"; it normally will only contain MenuButtons. You will usually add 2 or more AccordionLayouts to the side bar, each with a set of related MenuButtons. An AccordionLayout will stay closed until clicked at which point it will pop open and reveal the MenuButtons inside. Only 1 AccordionLayout may be open at a time (their siblings will automatically close).

See [here](cbuser.md#accordionlayout) an example.

### closeIcon:string
#### Display a Bootstrap or Font Awesome Icon for the "close" operation

The default is "glyphicon-chevron-up". For a list of valid icons see the Client Builder property sheet.  


### foregroundColor:string
#### The color of the  text

The color of the text is specified using the standard "#RRGGBB" format. 


### fontFace:string
#### The font family of the text

The font family of the text is specified using normal CSS conventions. 


### fontSize:number
#### The font size of the text

The font size is specified in pixels. 


### fontStyle:string
#### The style of the Widget's label text

The style of the text is specified as either "normal" or "italic". 


### fontWeight:string
#### The weight of the Widget's label text

The weight of the text is specified as either "normal" or "bold". 


### isExpanded:Boolean
#### The current 'open' or 'closed' state of the AccordionLayout
This boolean value will tell you if the AccordionLayout is currently 'open' (expanded) or 'closed' (collapsed). This property may be changed to control the state of the AccordionLayout.

### openIcon:string
#### Display a Bootstrap or Font Awesome Icon for the "open" operation

The default is "glyphicon-chevron-down". For a list of valid icons see the Client Builder property sheet.  

### title:string
#### The text appearing in the title area

### titleBarColor:string
#### The background color of the title area

The color is specified using the standard "#RRGGBB" format. If set to "default" the "Title Bar Background Color" Theme color will be used.


### titleForegroundColor:string
#### The color of the text in the title area

The text color is specified using the standard "#RRGGBB" format. If set to "default" the "Title Bar Foreground Color" Theme color will be used. 

### 'On Click' Event

This Widget supports an 'On Click' Event Handler. Note that this event will only be fired if the
AccordionLayout has no children; in that case it acts like a Button itself ather than a container for other
Widgets. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.



<hr>

## AudioRecorder
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; AudioRecorder</span>

This Widget is used to record a short audio clip. The clip may be uploaded into a Document object on the server.


### clearUpload()
#### Reset the recorder to its initial state

```js
clearUpload():void
```

After a clip has been recorder you can call this method to reset it to "empty".

### documentName:string
#### The name of the document to which the clip was uploaded

This property is readonly - it will be null until after a clip has been recorded and uploaded at which time it will
contain the name of the Document where it was saved.

### documentGroupName:string
#### The name of the Group to which the uploaded Document should be assigned

When this Widget creates and uploads a Document is will be assigned to the indicated [Group](resourceguide.md#groups). This is useful for controlling which users will have access to the Document.


### maxDurationInSeconds:number
#### The maximum number of seconds which may be recorded

In order to place a limit of the amount of storage used in your mobile device this setting places a limit on how many
seconds of audio you may record. (Default - 10 seconds).

### maxSizeInK:number
#### The maximum amount of storage that may be recorded

In order to place a limit of the amount of storage used in your mobile device this setting places a limit on the
 maximum size of the clip which may be recorded. (Default - 100K).


### optional:boolean
#### Specify whether a clip must be recorded before a default "submit"

### placeholder:string
#### The optional "placeholder" value

Defaults to "Start Audio Recording".



### 'On Change' Event

This Widget supports an "On Change" Event Handler which fires after the user has successfully recorder an audio clip. 
The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter returns null.

<hr>


## BarChart
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; BarChart</span>

This Widget draws a "bar chart" (where the "histogram" bars grow to the right).

### axisAutoRange:boolean
#### Indicate whether the range of X axis is automatically adjusted.


### bindEvents:any
#### Listen for internal ZingChart events

ZingChart widgets such as this one support a mechanism that allows you to listen for various ZingChart internal [events](https://www.zingchart.com/docs/api/events). This would normally be done through the ZingChart ["bind()"](https://www.zingchart.com/docs/api/events#-bind-) mechanism but in order to be compatible with the Vantiq widgets you need to use the "bindEvents" property instead.

To define the listeners you assign an object to the "bindZEvents" property like this:

```js
var wdg = client.getWidget("LineChart1");
wdg.bindEvents = {
        "setdata":function(e)
        {
            console.log("setdata: " + e.id);
        },
        "node_click":function(e)
        {
            console.log("node_click: " + e.id);
        }
    };
```

### borderThickness:number
#### The thickness of the border in pixels

### chartConfig
#### Access to the [ZingChart Bar Chart](https://www.zingchart.com/docs/chart-types/bar) configuration
Reading from _chartConfig_ returns a JavaScript object which contains the current runtime Bar Chart configuration parameters. Writing to _chartConfig_ allows the user to programmatically change the appearance of the Bar Chart.

For example, the following reads the current configuration and changes the Bar Chart to a line chart with spline plotting:
```js
	var chart = client.getWidget("BarChart1");
	var config = chart.chartConfig;
	config.data.type = "line";
    config.data.plot = {"aspect":"spline"};
	chart.chartConfig = config;
```

Please refer to the ZingChart link above for configuration options available for the Bar Chart.

### chartSeries
#### Access to the [ZingChart Bar Chart](https://www.zingchart.com/docs/chart-types/bar) displayed data
Reading from _chartSeries_ returns a JavaScript object which contains the current runtime Bar Chart data. Writing to _chartSeries_ allows the user to programmatically change the data displayed by the Bar Chart.

For example, the following changes the Bar Chart to contain three data timestamp data points that represent speed:
```js
	var chart = client.getWidget("BarChart1");
	var series = [{"values":[[1420070401000, 100],[1420070402000,30],[1420070403000,90]],"text":"speed"}];
	chart.chartSeries = series;
```

Please refer to the ZingChart link above for the format of series data required for the Bar Chart.

### displayThreshold:string
#### Indicate whether a thresholdline will be drawn across the chart at "thresholdValue"

"displayThreshold" may be set to either "Yes" or "No" (the default is "No"). When "Yes" is specified the value of the "thresholdValue" property is used to draw a "threshold line" across the chart at the indicated point.

### hasGridLines:boolean
#### Indicate whether grid lines should be drawn across the chart



### showIn3D:boolean
#### Indicate the chart should show in 3D


### showTrue3D:boolean
#### Indicate the type of 3D display to use

This property only applies if "showIn3D" is set to "true". It indicates whether to use "true 3D" or an isometric view.



### thresholdValue:number
#### The value where the threshold line should be drawn

Ignored unless "displayThreshold" is set to "Yes".


### title:string
#### Title superimposed on the widget

This property will superimpose a title on the Widget; the title is null by default.

### xAxisProperties:DataStreamListElement[]
#### The properties to be used for the X-Axis

This value must be an array of DataStreamListElement objects; you instantiate them like this:

```js
var dsle = new DataStreamListElement(propertyName:string, label:string);
```

where "propertyName" is the name of a valid property in the incoming DataStream objects and "label" is a human-readable to be label to used when drawing the chart.

### yAxisProperty:string
#### The property to be used for the Y-Axis

This value must either be the name of a valid property in the DataStream objects **or** the special string "-TIMESTAMP-" (which means to use the "arrival time" of the DataStream event).



### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' parameter is an object with 'x' and 'y' properties giving the offset of the click.



### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.



<hr>

## BarcodeReader
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; BarcodeReader</span>

This Widget uses the mobile device's camera to scan a barcode or QR image and convert it into a string.


### defaultValue:string
#### The default result value

This allows you to supply a default value for the result of the scan.


### optional:boolean
#### Specify whether a clip must be recorded before a default "submit"

### placeholder:string
#### The optional "placeholder" value

Defaults to "Scan Barcode".

### scannedValue:string
#### The value of the scanned string

The value of the string scanned by the BarcodeReader. If the user hasn't scanned anything yet the value will be "null".


### 'On Change' Event

This Widget supports an "On Change" Event Handler which fires after the user has successfully scanned a bar code. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains the string that was scanned.




<hr>

## Button
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; Button</span>

This is a classic "push button".

### backgroundColor:string
#### The color of the Button background

The background color is specified using the standard "#RRGGBB" format. ("#d0d0d0" is the default.)


### buttonLabel:string
#### The text of the Button

### buttonLabelColor:string
#### The color of the Button text

The text color is specified using the standard "#RRGGBB" format. ("#000000" is the default.)


### buttonLabelSize:number
#### The font size of the Button text

The font size is specified in pixels. ("18" is the default.)


### buttonLabelStyle:string
#### The style of the Button text

The style of the text may be specified as one of "normal", or "italic".

### glyphIcon:string
#### Display a Bootstrap or Font Awesome Icon to the left of the button text

You may enter a valid icon name such as "glyphicon-asterisk" or "fa-automobile". For a list of valid icons see the Client Builder property sheet.  The default is "null" which omits the icon. 

### isDisabled:boolean
#### Is this button disabled?

By default all buttons are enabled. At runtime you can disable it by setting the value of its “isDisabled” property to “true”.

### submitValue:number
#### A value to identify the button when it is used to submit a default response

For a discussion of how this property is used see [Terminating with default Buttons](cbuser.md#terminating-with-default-buttons).


### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.







<hr>

## Calendar
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; Calendar</span>

This widget is used to present a live calendar of events and is based on the [FullCalendar](https://fullcalendar.io/) JavaScript control.

### borderThickness:number
#### The thickness of the border in pixels

### calendar
#### The JQuery element that references the FullCalendar container

### fullCalendar
#### Reference to the FullCalendar object
Use the _fullCalendar_ accessor to make calls directly to the FullCalendar API. For example:
```
	// retrieve a reference to a calendar widget
	var widget = client.getWidget("Calendar1");
	
	// move to the next month
    widget.fullCalendar.next();
    
    // display the language locale used by FullCalendar
    var locale = widget.fullCalendar.getOption('locale');
    console.log("FullCalendar locale = " + locale);
```


### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.


### Event Handling
The Calendar widget supports many of the FullCalendar event callbacks which are enumerated in the following sections. The widget callbacks are of the form:
```
Client_<page name>_<widget name>_<event name>(client,page,extra)
```
where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself. The "extra" parameter is a JSON object that contains at least two properties:

* **calendar**: a reference to the FullCalendar object. Calls to the FullCalendar API from JavaScript can be made using this element. For example:
```
extra.calendar.changeView('timeGridWeek');
```
changes the current view of the calendar to the weekly view.

* **info**: is the FullCalendar event specific information. Please refer to the FullCalendar [online documentation](https://fullcalendar.io/docs) Events section for details about the event specific information returned for each event. Many of the events return a reference to the event on the calendar which is referenced as follows:
```
extra.info.event.title
```
which returns the title of the event on the calendar.

### 'On Drag Stop' Event
This widget supports the FullCalendar _eventDragStop_ event which is called when an event is dropped or moved.

### 'On Drag Start' Event
This widget supports the FullCalendar _eventDragStart_ event which is called when an event has started to move.

### 'On Event Drop' Event
This widget supports the FullCalendar _eventDrop_ event which is called when an event is dropped.

### 'On Event Resize' Event
This widget supports the FullCalendar _eventResize_ event which is called when an event's duration changes.

### 'On Event Click' Event
This widget supports the FullCalendar _eventClick_ event which is called when an event is clicked.

### 'On Events' Event
This widget supports the FullCalendar _events_ event which is called when the user clicks the Previous or Next buttons or switches calendar views. The "extra" parameter has different properties than all other events for this widget. They are:

* **fetchInfo**: the FullCalendar 'events' event object.
* **successCallback**: a callback JavaScript function. It is essential that the callback function is called with an array of FullCalendar event objects, even if it is empty, when this event is handled. Otherwise, use the 'failureCallback' function.
* **failureCallback**: a callback JavaScript function. Use this callback if there is some sort of failure when attempting to update the calendar view. It accepts a parameter that contains information about the failure.
* **calendar**: a reference to the FullCalendar object.

### 'On Event Render' Event
This widget supports the FullCalendar _eventRender_ event which is called when an event is displayed.

### 'On Drop' Event
This widget supports the FullCalendar _drop_ event which is called when an external draggable element or an event from another calendar is dropped onto the calendar.

### 'On MouseEnter' Event
This widget supports the FullCalendar _eventMouseEnter_ event which is called when the user mouses over a calendar event.

### 'On MouseLeave' Event
This widget supports the FullCalendar _eventMouseLeave_ event which is called when the user mouses out of a calendar event.

<hr>

## Camera
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; Camera</span>

This Widget is used to capture an image using your mobile device's camera. The image may be uploaded into a Document object on the server.


### clearUpload()
#### Reset the camera to its initial state

```js
clearUpload():void
```

After an image has been captured you can call this method to reset it to "empty".

### defaultImageUrl:string
#### The URL of an image will be the default value for the Camera

This defaults to "null", but if set it contains a URL pointing to a default image for the Camera.

There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).

### documentName:string
#### The name of the document to which the image was uploaded

This property is readonly - it will be null until after an image has been captured and uploaded at which time it contains the name of the Document where it was saved.

### documentGroupName:string
#### The name of the Group to which the uploaded Document should be assigned

When this Widget creates and uploads a Document is will be assigned to the indicated [Group](resourceguide.md#groups). This is useful for controlling which users will have access to the Document.

### optional:boolean
#### Specify whether a clip must be recorded before a default "submit"

### maxWidth:number
#### Restrict the size of the captured image
Images returned by mobile devices can be quite large so can cause long upload and download times. To restrict the size of the image returned, enter a value for the _maxWidth_ property. If the captured image width is larger than the _maxWidth_ property, the image is scaled such that the width matches the _maxWidth_ value and the height is scaled to match the aspect ratio of the captured image. If no value is provided for the _maxWidth_ property, the captured image is returned unmodified.

### placeholder:string
#### The optional "placeholder" value

Defaults to "Take Photo".

### thumbnailSize:number
#### Create a thumbnail image for the captured image
To create a second, 'thumbnail' version of the captured image, enter a value for the _thumbnailSize_ property. If the _thumbnailSize_ property is specified, an image is created with its width or height, whichever is greater, scaled such that it matches the _thumbnailSize_ value and the lesser of the width or height is scaled to match the aspect ratio of the captured image. If no value is provided for the _thumbnailSize_ property, no thumbnail image is returned.

The uploaded thumbnail document will have the same name as the uploaded image document with a suffix of "Thumbnail" before the file extension.


### 'On Change' Event

This Widget supports an "On Change" Event Handler which fires after the user has successfully taken a photo. 
The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains null.



<hr>

## Canvas
<span style="font-style:italic;">[Widget](#widget) &#x2192; Canvas</span>

This Widget contains an HTML "canvas" element suitable for drawing custom graphics. You can find a discussion of the "canvas" element [here](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/canvas).


### repaint()
#### Force the canvas to be redrawn

```js
repaint()
```

This method will force the "On Paint" event handler to fire so your code can redraw the graphics area.


### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' is an object with 'x' and 'y' properties giving the offset of the click.)


### 'On Paint' Event

This Widget supports an 'On Paint' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onPaint(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' is an object with the "ctx" property set to the "2D rendering context" for the widget; this is what you should use to make all the canvas API drawing calls.

The context is an instance of the 'CanvasRenderingContext2D' interface and supports a set of drawing methods which are described [here](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D).

The body of an 'On Paint' event might look something like this:

```js
    var ctx = extra.ctx;
    
    ctx.clearRect(0, 0, this.w, this.h);
    
    ctx.beginPath();   
    ctx.strokeStyle = "#ff0000";
    ctx.moveTo(0, 0);    
    ctx.lineTo(this.w, this.h); 
    ctx.moveTo(0, this.h);    
    ctx.lineTo(this.w, 0);  
    ctx.stroke();
   
    ctx.fillStyle = 'rgb(200, 0, 0)';
    ctx.fillRect(10, 10, 50, 50);
    
    ctx.fillStyle = 'rgba(0, 0, 200, 0.5)';
    ctx.fillRect(30, 30, 50, 50);
```




<hr>

## Chat
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; Chat</span>

This Widget is used to facilitate basic chat messaging, similar to the native Chat views found in the Vantiq mobile apps.

### clearText()
#### Clear the current contents of the Widget

```js
clearText()
```



<hr>

## Checkbox
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; Checkbox</span>

This Widget is used to enter boolean value as a standard "checkbox".

### boundValue:Boolean
The value of the checkbox. Will be _undefined_ until the user has changed the value.

### checkboxLabel:string
#### The Checkbox label

This is the text label inside the Checkbox Widget.


### dataBinding:string
#### The name of a Boolean DataObject variable

This Widget can be bound to a DataObject variable of type "Boolean" (e.g. "client.data.myBoolean"). Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.

### isClassic:Boolean
#### Change the Checkbox to a 'classic' display style
By default the Checkbox widget is displayed as a sliding control. If "isClassic" is set to "true" the checkbox will display in the classic style (a small square with a checkmark inside).

### isReadOnly:boolean
#### Disables input into the field

### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.

<hr>

## ComboBox
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; ComboBox</span>

This Widget is used to enter a value either via direct text entry or from a dropdown list of pre-populated values.

### boundValue:any
The value of the combobox. Will be _undefined_ until the user has selected a value.

### dataBinding:string
#### The name of a String, Integer or Real DataObject variable

This Widget can be bound to a DataObject variable of type "String", "Integer" or "Real" (e.g. "client.data.myInteger"). Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.


### enumeratedList:any[]
#### The ComboBox menu definition

When clicked a ComboBox presents a menu of choices based on user-entered values in the text entry field. Each choice in the menu consists of a "label" (the text the user sees) and a "value" (the actual value that is used by the dataBinding). The array must be formed like this:

```js
var enumList = [
    {value:1, label:"One"},
    {value:2, label:"Two"},
    {value:3, label:"Three"}
];
```

In this example the user would see a dropdown menu with the items "One", "Two" and "Three". If the user selected "Two" the bound DataObject variable would be set to the number 2.

### isReadOnly:boolean
#### Disables input into the field

### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.


<hr>

## ColumnChart
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; ColumnChart</span>

This Widget draws a "bar chart" (where the "histogram" bars grow upwards).

### axisAutoRange:boolean
#### Indicate whether the range of Y axis is automatically adjusted.


### bindEvents:any
#### Listen for internal ZingChart events

ZingChart widgets such as this one support a mechanism that allows you to listen for various ZingChart internal [events](https://www.zingchart.com/docs/api/events). This would normally be done through the ZingChart ["bind()"](https://www.zingchart.com/docs/api/events#-bind-) mechanism but in order to be compatible with the Vantiq widgets you need to use the "bindEvents" property instead.

To define the listeners you assign an object to the "bindZEvents" property like this:

```js
var wdg = client.getWidget("LineChart1");
wdg.bindEvents = {
        "setdata":function(e)
        {
            console.log("setdata: " + e.id);
        },
        "node_click":function(e)
        {
            console.log("node_click: " + e.id);
        }
    };
`````

### borderThickness:number
#### The thickness of the border in pixels

### chartConfig
#### Access to the [ZingChart Bar Chart](https://www.zingchart.com/docs/chart-types/bar) configuration
Reading from _chartConfig_ returns a JavaScript object which contains the current runtime Bar Chart configuration parameters. Writing to _chartConfig_ allows the user to programmatically change the appearance of the Bar Chart. A Vantiq ColumnChart is a variation of a ZingChart Bar Chart.

For example, the following reads the current configuration and changes the Bar Chart to a line chart with spline plotting:
```js
	var chart = client.getWidget("ColumnChart1");
	var config = chart.chartConfig;
	config.data.type = "line";
    config.data.plot = {"aspect":"spline"};
	chart.chartConfig = config;
```

Please refer to the ZingChart link above for configuration options available for the Bar Chart.

### chartSeries
#### Access to the [ZingChart Bar Chart](https://www.zingchart.com/docs/chart-types/bar) displayed data
Reading from _chartSeries_ returns a JavaScript object which contains the current runtime chart data. Writing to _chartSeries_ allows the user to programmatically change the data displayed by the chart.

For example, the following changes the Bar Chart to contain three data timestamp data points that represent speed:
```js
	var chart = client.getWidget("ColumnChart1");
	var series = [{"values":[[1420070401000, 100],[1420070402000,30],[1420070403000,90]],"text":"speed"}];
	chart.chartSeries = series;
```

Please refer to the ZingChart link above for the format of series data required for the Bar Chart.


### displayThreshold:string
#### Indicate whether a thresholdline will be drawn across the chart at "thresholdValue"

"displayThreshold" may be set to either "Yes" or "No" (the default is "No"). When "Yes" is specified the value of the "thresholdValue" property is used to draw a "threshold line" across the chart at the indicated point.

### hasGridLines:boolean
#### Indicate whether grid lines should be drawn across the chart




### thresholdValue:number
#### The value where the threshold line should be drawn

Ignored unless "displayThreshold" is set to "Yes".


### title:string
#### Title superimposed on the widget

This property will superimpose a title on the Widget; the title is null by default.

### xAxisProperty:string
#### The property to be used for the X-Axis

This value must either be the name of a valid property in the DataStream objects **or** the special string "-TIMESTAMP-" (which means to use the "arrival time" of the DataStream event).



### yAxisProperties:DataStreamListElement[]
#### The properties to be used for the Y-Axis

This value must be an array of DataStreamListElement objects; you instantiate them like this:

```js
var dsle = new DataStreamListElement(propertyName:string, label:string);
```

where "propertyName" is the name of a valid property in the incoming DataStream objects and "label" is a human-readable to be label to used when drawing the chart.



### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' parameter is an object with 'x' and 'y' properties giving the offset of the click.


### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.


<hr>

## ControlWidget
<span style="font-style:italic;">[Widget](#widget) &#x2192; ControlWidget</span>

This is the superclass of all "control" Widgets. It is a non-leaf class and cannot be instantiated.


### label:string
#### The Widget's label text

All "control" Widgets have an optional label that appears above the main body of the Widget. (This is useful when putting a list of controls into a [VerticalLayout](#verticallayout).) No label will be shown when the value is null or the empty string.

"label" has a default value of "". 

### labelAlign:string
#### The alignment of the Widget's label text

The label alignment may be specified as one of "center", "left" or "right". ("center" is the default.)


### labelColor:string
#### The color of the Widget's label text

The label color may be specified using the standard "#RRGGBB" format. ("#000000" is the default.)

### labelSize:number
#### The font size of the Widget's label text

The label font size may be specified in pixels. ("14" is the default.)

### labelStyle:string
#### The style of the Widget's label text

The style of the label text may be specified as one of "normal", or "italic".




<hr>

## Conversation
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; [Chat](#chat) &#x2192; Conversation</span>

This Widget is used to facilitate a "chat-like" interaction with a [conversation](agents.md#conversations) managed by an [Agent](agents.md).  This allows the user of a Vantiq client to hold a conversation with a designated Agent using either [service events](services.md#event-types) or a [service procedure](services.md#procedures). The Widget is similar in appearance to the [Chat](#chat) Widget. For details on setup, you should refer to the [Conversation Widget Tutorial](tutorials/conversationtutorial.md).


The Conversation widget may interact with a Service in one of two ways:

**Using Service Events**

You must set the "serviceName" and "inboundServiceEvent" properties, and you must associate the widget with a "Service Event" DataStream. The Conversation widget will publish requests to the Service's inboundServiceEvent (with the request in "event.prompt"), and expect responses to appear on the DataStream.

**Using Service Procedures**

You must set the "serviceName" and "procedureName" properties. The conversation widget will invoke the Procedure using these two parameters:

1. "input" - a string that contains what the user typed
2. "config" - an object with the "conversationId" and "collaborationId" properties set (if they are known)



In either case the response returned to the Conversation widget must be in one of three forms:

1. A string
2. An object containing a string in an "llmResponse" or "data" property
3. An object containing an array of strings in an "llmResponse" or "data" property. (The strings will be concatenated together.)

For example, these would all be acceptable responses:

```js
response = "Sacramento is the capital of California."

response = {
  llmResponse: "Sacramento is the capital of California."
}

response = {
  data: "Sacramento is the capital of California."
}

response = {
  llmResponse: ["Sacramento is the capital" + " " + "of California."]
}

response = {
  data: ["Sacramento is the capital" + " " + "of California."]
}
```


### addAIMessage()
#### Simulate a message being received from the system

```js
addAIMessage(text:string, isMarkdown:boolean=false):void
```

* text: string - The text to be added to the left side of the conversation
* isMarkdown: boolean - The text should be formatted as Markdown before being added (optional)

Note that this just affects what is displayed, *not* the contents of the Conversation itself.

### submitHumanMessage()
#### Simulate a message being entered by the user and submitted

```js
submitHumanMessage(text:string, isMarkdown:boolean=false):void
```

* text: string - The text to be added to the right side of the conversation
* isMarkdown: boolean - The text should be formatted as Markdown before being added (optional)

Simulate the user typing input and hitting "send".  This will trigger an interaction with the Agent and will effect the actual conversation.


### addHumanMessage()
#### Add a "user" message to the right side of the conversation without submitting

```js
addHumanMessage(text:string):void
```

* text: string - The text to be added to the right side of the conversation

Add a user message to the right side of the conversation but don't actually submit it.

### clearText()
#### Clear the current contents of the Widget

```js
clearText()
```

Note that this just affects what is displayed, *not* the contents of the Conversation itself.


### conversationId:string
#### The unique id for the Conversation being displayed

### conversationName:string
#### The name of the Conversation being displayed

### getMessages()
#### Get an array containing all the current messages shown in the conversation

```js
getMessages():any[]
```

Returns an array of objects containing all the messages being shown. Each object has these properties:

* msg - The text of the message
* source - The source of the message ("system" or "user")
* msgElement - The JQuery selector for the message.

### isReadOnly:boolean
#### Enable or disable the ability to send messages

Defaults to "false".



### inboundServiceEvent:string
#### The name of the inbound event within the service to which "prompts" are to be sent

### maxFlushInterval:number
#### The maximum interval between flushes (in milliseconds)

This only applies when using a streamed Gen AI Procedure. A value of 0 means that this feature is disabled and only the buffer size is used to trigger a flush. A negative value means that data will be flushed on every write. Otherwise, a flush will be triggered once the interval is exceeded (regardless of the buffer size). (Default is 5000ms.)

### maxBufferSize:number
#### The maximum size of the streaming buffer before a "flush" is triggered

This only applies when using a streamed Gen AI Procedure. Value is in bytes and must be between 512 and 1048576. (Default is 64K)

### procedureName:string
#### The name of the procedure on the service from which the request and responses will be streamed.

### serviceName:string
#### The name of the Service to which "prompts" are to be sent


### title:string
#### The title to appear at the top of the Conversation Widget

### 'On Action Button' Event

In the Client Builder you are able to define 3 different types of "action buttons" which will appear in and around the message area. These are found in the "Specific" area of the property sheet:

* User Message Actions - These are buttons which will appear next to messages entered by the user
* System Message Actions - These are buttons which will appear next to message responses sent by the system
* Latest Message Actions - These are buttons which will only appear next the most recent message response sent by the system

These action buttons are identified by a unique key and have an optional Label, Icon and Tooltip.

The "On Action Button" Event Handler is called whenever one of these buttons is clicked. This call will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onActionButton(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains properties that help identify which button was clicked and which message was associated with it:

* index - the index of the action within its set of action buttons
* message - the text of the message the button is associated with
* key - the unique key that was assigned to the button
* label - the label for the button
* tooltip - the tooltip for the button





### 'On Data Arrived' Event

This Widget supports an "On Data Arrived" Event Handler. This handler will be called whenever new data arrives on the Conversation widget's associated DataStream in response to an input request. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onDataArrived(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains the newly arrived data object. In general it will look something like this:

```js
{
   "prompt": "How big is Mars?",
   "conversationId": "2f71be60-37e4-11f0-9cef-362ce73af82d",
   "collaborationId": "2f71be60-37e4-11f0-9cef-362ce73af82d",
   "myEntityId": "xxxx",
   "llmResponse": "Mars has a diameter of about 6,779 kilometers (4,212 miles), which is roughly half the size of Earth."
}
```

Note that this event will **only** work if you have set the Conversation widget's 'inboundServiceEvent' parameter and have configured a DataStream to listen for a response. (That is, this event will **not** be called if you are configured to use a Procedure rather than an input and output event on the Service.)




### 'On Send Request' Event

This Widget supports an 'On Send Request' Event Handler. It allows your code to see and change any request sent by the user. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onSendRequest(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

When the Conversation widget is configured using the  'inboundServiceEvent' parameter the "extra" object will look like this:

```js
{
   "obj": {
      "prompt": "How big is Mars?"
   }
}
```

When configured to use a Procedure the "extra" object looks like this:


```js
{
   "obj": {
      "input": "How big is the Earth?"
   }
}
```

In either case you may alter the contents of "obj" to override what the user typed and change what is actually sent to the server.



<hr>

## Discussion
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; [Chat](#chat) &#x2192; Discussion</span>


This Widget is similar to the [Conversation](#conversation), but is intended specifically for interaction with Services which are designated as [Agents](agents.md). Any input supplied by the user is sent to the Agent using the streaming Agent-to-Agent (A2A) protocol.

The Discussion Widget manages one or more "InteractionThreads" - each of these represents a dialog the user is having with an Agent. Each thread is represented by a read-only InteractionThread object with properties which contain information about the thread:

* discussion:any - A copy of the last-known state of the corresponding Discussion object
* discussionId:string - The id of the corresponding Discussion object
* isActive:boolean - "true" if this InteractionThread is currently visible in the Discussion Widget
* serviceName:string - The name of the Agent Service that this InteractionThread communicates with
* title:string - The title for the thread, which comes from the "title" property of the Discussion

There are other properties defined by the InteractionThread object but they are for internal use only.

There is only a single InteractionThread visible and usable at a time, known as the "active" thread. The Discussion Widget always contains one special InteractionThread that indicates the "default" thread that is defined in the Client Builder. This InteractionThread does *not* have an actual Discussion associated with it. The discussionId is a special string defined as Discussion.GENERAL.

Typically this "General" thread is used to talk to an Agent whose job it is to analyze requests and send them to other Agents which *do* have a Discussion. In order for the user to see and communicate with these Discussions it is the responsibility of the Client to call the onDiscussionInserted() method, which tells the Widget to create a new InteractionThread to represent the Agent/Discussion. Usually the Client will provide a UI that allows the user to know about (and switch between) the various threads. (You might do this with a List or Tree or even a set of buttons.)



### activeDiscussionId:string
#### Get or Set the id of the currently active Discussion

This contains the Discussion id associated with the currently active InteractionThread. (This will return Discussion.GENERAL for the "default" InteractionThread.)

It can only be set to a Discussion id of one of the currently known InteractionThreads.


### activeInteractionThread:InteractionThread
#### Get or Set the currently active InteractionThread

This contains the currently active InteractionThread. It can only be set to an InteractionThread which is currently known to the Discussion Widget.



### getInteractionThreadByDiscussionId()
#### Get the InteractionThread associated with a Discussion

```js
var it = getInteractionThreadByDiscussionId(discussionId:string):InteractionThread
```
* discussionId: string - The Discussion id

This method returns the InteractionThread associated with the supplied discussion id. If there is no match then "null" will be returned.



### onDiscussionDeleted()
#### Tell the Discussion Widget that a Discussion has been deleted

```js
onDiscussionDeleted(discussion:any)
```
* discussion: any - The Discussion which was deleted

This method tells the Discussion Widget that a Discussion it may know about has been deleted. The Discussion's id will be used to search for a matching InteractionThread and if found it will be discarded. If the InteractionThread happened to be active then the Widget will switch to the default ("General") InteractionThread.

Typically the Client will learn about the creation, update and deletion of Discussions by creating an "On Data Changed" DataStream for the "system.discussions" Type.


### onDiscussionInserted()
#### Tell the Discussion Widget that a new Discussion has been inserted

```js
var it = onDiscussionInserted(discussion:any):InteractionThread
```
* discussion: any - The Discussion which was inserted

This method tells the Discussion Widget that a new Discussion has been created and that a new InteractionThread should be created to represent it.

Typically the Client will learn about the creation, update and deletion of Discussions by creating an "On Data Changed" DataStream for the "system.discussions" Type.



### onDiscussionUpdated()
#### Tell the Discussion Widget that a new Discussion has been updated

```js
onDiscussionUpdated(discussion:any)
```
* discussion: any - The Discussion which was updated

This method tells the Discussion Widget that an existing Discussion has been updated and that the InteractionThread title may need to change to match.

Typically the Client will learn about the creation, update and deletion of Discussions by creating an "On Data Changed" DataStream for the "system.discussions" Type.

### state:DiscussionState
#### Get the current "state" of the Discussion Widget

This is a read-only property that uses a set of possible values to describe the current state of the Discussion Widget:

* DiscussionState.Unrealized - The Widget is not attached to a Page - should never happen
* DiscussionState.Idle - The Widget is idle and waiting for user input
* DiscussionState.InProgress - A request is in progress so new input is not being accepted
* DiscussionState.InputRequested - The Widget is waiting for the user to respond to a request for input

### 'On Action Button' Event

In the Client Builder you are able to define 3 different types of "action buttons" which will appear in and around the message area. These are found in the "Specific" area of the property sheet:

* User Message Actions - These are buttons which will appear next to messages entered by the user
* System Message Actions - These are buttons which will appear next to message responses sent by the system
* Latest Message Actions - These are buttons which will only appear next the most recent message response sent by the system

These action buttons are identified by a unique key and have an optional Label, Icon and Tooltip.

The "On Action Button" Event Handler is called whenever one of these buttons is clicked. This call will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onActionButton(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains properties that help identify which button was clicked and which message was associated with it:

* index - the index of the action within its set of action buttons
* message - the text of the message the button is associated with
* key - the unique key that was assigned to the button
* label - the label for the button
* tooltip - the tooltip for the button




### 'On Data Arrived' Event

This Widget supports an "On Data Arrived" Event Handler. This handler will be called whenever a response to a user's request is sent to the Discussion widget. This call will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onDataArrived(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains two properties:

* response:any - An Agent-to-Agent (A2A) prootcol Task object that contains the complete response. (A description can be found [here](https://agent2agent.info/docs/concepts/task/))
* prompt:string - The previous user input which provoked this response
* isShown:boolean - Your code can set this to "false" if you want this response to be hidden from the user.






### 'On Send Request' Event

This Widget supports an 'On Send Request' Event Handler. It allows your code to see and change any request sent by the user. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onSendRequest(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself. "extra" is an object which contains the "extra.message" property containing the text of the user's input. You may alter the contents of "message" to override what the user typed and change what is actually sent to the server.








<hr>

## DataStreamWidget
<span style="font-style:italic;">[Widget](#widget) &#x2192; DataStreamWidget</span>

This is the superclass of all "Data Stream" Widgets. It is a non-leaf class and cannot be instantiated.

A DataStream can be found using either the [getDataStreamByName()](#getDataStreamByName) or [getDataStreamByUUID()](#getDataStreamByUUID) methods on Client.

These are all the Widgets which inherit from the DataStreamWidget class and can be bound to a DataStream:

* [BarChart](#barchart)
* [DynamicMapViewer](#dynamicmapviewer)
* [FloorplanViewer](#floorplanviewer)
* [ColumnChart](#columnchart)
* [DataTable](#datatable)
* [Gauge](#gauge)
* [LineChart](#linechart)
* [ListViewer](#listviewer)
* [NumberViewer](#numberviewer)
* [PieChart](#piechart)

### clearData()
#### Clear data currently displayed on the widget. 

```
client.getWidget("your_widget_name").clearData();
```

Use this method to clear existing rows in a DataTable, lines on a Chart or markers on a Map.

Use this method to reset Number and Gauge to display the value 0.


### dataStreamUUID:string
#### The UUID of the DataStream to which the Widget is bound

If you have a DataStream object you can get its UUID using "theDataStreamObject.uuid";




<hr>

## DataTable
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; DataTable</span>

This Widget displays a table which contain an array of data rows. Each event from the Data Stream is assumed to carry an array which completely replaces the previous one.

### borderThickness:number
#### The thickness of the border in pixels

### columnDescriptors:DataTableColumn[]
#### An array of objects describing each column

The DataTableColumn object contains these properties which **must** be set:

* propertyName:string - The name of a valid property in the Data Stream object
* title:string - The human-readable title for this column
* dataType:string - The data type of the column value, one of "Currency", "Decimal", "Integer", "Real" or "String"
* format:string - If the data type is numeric or datetime, this format string will be applied to it before it is displayed. (Some examples of valid numeric format strings are found [here](http://numeraljs.com/#format). Examples of valid date time format strings are found  [here](https://momentjs.com/docs/#/parsing/string-format/))

### cellFontColor:string
#### The color of the text in table cell

The text color is specified using the standard "#RRGGBB" format. ("#000000" is the default.)

### cellFontFace:string
#### The font family of the text in table cell

The font family of the text is specified using normal CSS conventions. ("inherit" is the default.)

### cellFontSize:number
#### The font size of the text in table cell

The font size is specified in pixels. ("14" is the default.)

### cellFontStyle:string
#### The style of the text in table cell

The style of the text may be specified as one of "normal", or "italic".


### dataArray:any[]
#### An array of the data objects being displayed in the DataTable

This will be an array of objects; the properties inside must match the columns defined in the DataTable.

You can assign this property to an array of objects and it will completely replace the current contents of fhe DataTable.

### headerFontColor:string
#### The color of the text in table header

The text color is specified using the standard "#RRGGBB" format. ("#000000" is the default.)

### headerFontFace:string
#### The font family of the text in table header

The font family of the text is specified using normal CSS conventions. ("inherit" is the default.)

### headerFontSize:number
#### The font size of the text in table header

The font size is specified in pixels. ("14" is the default.)

### headerFontStyle:string
#### The style of the text in table header

The style of the text may be specified as one of "normal", or "italic".

### rowsPerPage:number
#### The number of rows shown in each "page" of the DataTable

The Data Table only shows "rowsPerPage" rows of data at a time; there is a "paginator" widget shown at the bottom of the table that allows you to page forward and backward through the data.

This property will be ignored if the DataTable's Height Size Policy is set to Explicit or SizeToParent.

### selectedObjectIndex:number
#### Index of the currently selected row object in original data set

If you define a "Select" Event handler then the Data Table will support the selection of rows. This property may be used to programmatically get or set the currently selected row using the index in the current dataArray.  This index starts at 0.

### selectedRowIndex:number
#### Index of the currently selected row on current visible page

If you define a "Select" Event handler then the Data Table will support the selection of rows. This property may be used to programmatically get or set the currently selected row using its row index on current visible page. This index starts at 0 and is less than rowsPerPage.

### selectedRowObject:any
#### The currently selected row object

If you define either a "Select" or "Deselect" Event handler then the Data Table will support the selection and deselection of rows. This property may be used to programmatically get and set the selected row object.

### table:any
#### The DataTable object

This value is the actual DataTable object that gives access to the features of the DataTables API. Documentation can be found [here](https://datatables.net/manual/api). For example, you might use this to remove all rows from a table and cause it to redraw:

```js
var widget = client.getWidget("DataTable1");
widget.table.rows().remove();
widget.table.draw();
```

### 'On Button Click' Event

This event is fired when the user clicks on a "Button" column which has been defined in the DataTable.
The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onButtonClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the click; these properties are defined:

* buttonLabel: The label text of the button that was clicked.
* columnName: The property name that corresponds to the column that was clicked.
* columnSelector: A JQuery selector for the "column" element (td) which contains the clicked button
* columnTitle: The title of the column that was clicked.
* dataColumnIndex: The column number within the DataTable of the button which was clicked (the first column is "0").
* dataObject: The "row object" for the row that was clicked.
* dataRowIndex: The row number within the data array of the button which was clicked (the first row is "0").
* physicalRowIndex: The physical row number containing the button that was clicked (the first row is "0").
* rowSelector: A JQuery selector for the "row" element (tr) which contains the clicked button



### 'On Checkbox Click' Event

This event is fired when the user clicks on a "Checkbox" column which has been defined in the DataTable.
The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onCheckboxClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the click; these properties are defined:

* checkboxLabel: The label text of the checkbox that was clicked.
* columnName: The property name that corresponds to the column that was clicked.
* columnSelector: A JQuery selector for the "column" element (td) which contains the clicked checkbox
* columnTitle: The title of the column that was clicked.
* dataColumnIndex: The column number within the DataTable of the checkbox which was clicked (the first column is "0").
* dataObject: The "row object" for the row that was clicked.
* dataRowIndex: The row number within the data array of the checkbox which was clicked (the first row is "0").
* isChecked: A boolean that represents the current state of the checkbox.
* physicalRowIndex: The physical row number containing the checkbox that was clicked (the first row is "0").
* rowSelector: A JQuery selector for the "row" element (tr) which contains the clicked checkbox


### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.




### 'On Deselect' Event

This Widget supports an "On Deselect" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onDeselect(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains the row object which was deselected.



### 'On Format Cell' Event

This event is fired when a value is about to be displayed within a cell of the DataTable; the handler may be used to change the displayed value. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onFormatCell(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the cell; these properties are defined:

* cellValue: The string that is about to be displayed in this cell.
* columnName: The property name that corresponds to the column being formatted.
* columnTitle: The title of the column being formatted.
* dataColumnIndex: The column number within the DataTable being formatted (the first column is "0").
* dataObject: The "row object" of the row being formatted.
* dataRowIndex: The row number within the data array of the row being formatted(the first row is "0").
* physicalRowIndex: The physical row number containing the row being formatted (the first row is "0").


The string in "extra.cellValue" is about to be displayed in this cell; you may alter this value to change what will actually be displayed.


### 'On Format Cell Background' Event

This event is still defined for backwards compatibility but has been deprecated. Instead you should use the "On Render Cell" event defined below.



### 'On Image Click' Event

This event is fired when the user clicks on an "Image" column which has been defined in the DataTable.
The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onImageClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the click; these properties are defined:

* columnName: The property name that corresponds to the column that was clicked.
* columnSelector: A JQuery selector for the "column" element (td) which contains the clicked image
* columnTitle: The title of the column that was clicked.
* dataColumnIndex: The column number within the DataTable of the image which was clicked (the first column is "0").
* dataObject: The "row object" for the row that was clicked.
* dataRowIndex: The row number within the data array of the image which was clicked (the first row is "0").
* physicalRowIndex: The physical row number containing the image which was clicked (the first row is "0").
* rowSelector: A JQuery selector for the "row" element (tr) which contains the clicked image





### 'On Render Cell' Event

This event is fired when a value is about to be displayed within a cell of the DataTable; the handler may be used to change the CSS style of the various DOM elements that it contains based on the data it displays. (This would allow you to change things such as "font-style".) The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onRenderCell(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the cell; these properties are defined:

* buttonElement: For columns containing "Buttons" this will be a JQuery selector that points to the '&lt;button>' element within the cell.
* columnName: The property name that corresponds to the column being rendered.
* columnTitle: The title of the column being rendered.
* dataColumnIndex: The column number within the DataTable of the cell being rendered (the first column is "0").
* dataRowIndex: The row number within the data array of the cell being rendered (the first row is "0").
* dataObject: The "row object" for the row being rendered.
* imgElement: For columns containing "Images" this will be a JQuery selector that points to the '&lt;img>' element within the cell.
* inputElement: For columns containing "Checkboxes" this will be a JQuery selector that points to the '&lt;input>' element within the cell.
* labelElement: For columns containing "Checkboxes" this will be a JQuery selector that points to the '&lt;label>' element within the cell.
* physicalRowIndex: The physical row number containing the row being rendered (the first row is "0").
* tdElement: A JQuery selector that points to the '&lt;td>' element which contains the cell.
* trElement: A JQuery selector that points to the '&lt;tr>' element which contains the cell.


The JQuery selectors such as "extra.tdElement" can be used to change the CSS styling of this cell. For example,

```
extra.tdElement.css("font-style","italic");
```

### 'On Row Expanded' Event

If this event is defined, then all rows in the DataTable are shown with a "disclosure" button which causes them to expand and contract. When expanded this event can supply a fragment of HTML which will be displayed underneath the open row.

```
Client_<page name>_<widget name>_onRowExpanded(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the row; these properties are defined:

* dataRowIndex: The row number within the data array for the row being expanded (the first row is "0").
* physicalRowIndex: The physical row number within the current page (the first row is "0").
* dataObject: The "row object" for the row being expanded.
* rowSelector: The JQuery selector for the current physical row
* html: A string set by the handler for the HTML to be shown in the expanded area. (defaults to "")

For example, you might use this to add an optional image to an expanded row if the dataObject has one:

```
if (extra.dataObject.employeeImage)
{
    let img = client.getDocumentUrl(extra.dataObject.employeeImage);
    extra.html = "<img src=\"" + img  + "\">";
}
else
{
    extra.html = "No Image";
}
```



### 'On Select' Event

This Widget supports an "On Select" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onSelect(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains the row object which was selected.





<hr>

## Droplist
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; Droplist</span>

This Widget is used to enter a value as a standard "dropdown list".

### allValuesAreStrings
#### Interpret all returned values as strings

When _allValuesAreStrings_ is enabled, the value returned will always be returned as a string or an array of strings, even if the selected list item(s) are numeric.

### boundValue:any
The value of the droplist widget. Will be _undefined_ until the user has selected a value.

### dataBinding:string
#### The name of a String, Integer or Real DataObject variable

This Widget can be bound to a DataObject variable of type "String", "Integer" or "Real" (e.g. "client.data.myInteger"). Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.

### default:string
#### The default selected value for the list

When the Droplist is displayed, the default value, if any, will automatically be selected in the list. Even if the _selectMultiple_ property is enabled, only one value may be selected as the default value.

### enumeratedList:any[]
#### The Droplist menu definition

When clicked a Droplist presents a menu of choices. Each choice consists of a "label" (the text the user sees) and a "value" (the actual value that is used by the dataBinding). The array must be formed like this:

```js
var enumList = [
    {value:1, label:"One"},
    {value:2, label:"Two"},
    {value:3, label:"Three"}
];
```

In this example the user would see a dropdown menu with the items "One", "Two" and "Three". If the user selected "Two" the bound DataObject variable would be set to the number 2.

### isReadOnly:boolean
#### Disables input into the field

### selectMultiple:boolean
#### Allow selection of multiple list items

Allow the user to select multiple list items. When _selectMultiple_ is enabled, the value returned will be an array of values.

### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.

### 'On Validation' Event

The Widget's 'On Validation' Event is fired as a part of the "Validation" process which is
described [here](cbuser.md#field-validation).

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onValidation(client,vco)
```

where "this" points to the Page object and "client" points to the Client object. "vco" is the "Validation Control
Object" which is used to describe the current state of validation and to declare your own validation errors.

Of course in the case of a Droplist all you can do is force the use to select from a subset of the legal values.

<hr>

## DocumentViewer
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; DocumentViewer</span>

This Widget allows you to display a web page or a Vantiq document in another browser tab.

### flavor:string
#### The type of document to be displayed

This property is optional; if supplied it must be one of the following types:

* hmtl (default)
* pdf
* vaudio
* vimage
* vvideo
* deeplink

The "vaudio", "vimage" and "vvideo" flavors are used to listen, view or stream media which have been previously uploaded to a Vantiq document. (This can either be done manually using the Dev Portal or with the Vantiq mobile apps).

The "deeplink" flavor is used by the Vantiq mobile apps to indicate a link to redirect to another mobile app.


### placeholder:string
#### The text that is displayed next to the icon

By default the placeholder says "View the Dashboard" as a hint to the user, suggesting what will happen if they click the icon button. The "placeholder" property allows you to override that string.


### url:string
#### The url of the document to display

For the "html" and "pdf" flavors this must be a complete URL. For the other flavors ("vaudio", "vimage" or "vvideo") this is a fragment that references a Vantiq document. It will look like:

```
"rcs/audio/f9ceddab-add2-4b10-a602-65f82cc0a9da.m4a"
```

There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).


<hr>

## DynamicMapViewer
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; DynamicMapViewer</span>

This Widget shows location points on a map as they arrive from the Data Stream.

*Note that the DynamicMapView uses Google Maps which means the internet must be available at runtime.*

### borderThickness:number
#### The thickness of the border in pixels


### dataStreamProperty:string
#### The property that contains the GeoJSON Location value

This value must contain the name of a valid property in the DataStream objects that contains the GeoJSON location.


### fixedCenter:boolean
#### Indicate if the map should move when new points arrive

If "fixedCenter" is "true" (the default) the map will center on the first point to arrive and not move again unless the user moves it. If "fixedCenter" is "false" then the map will re-center on each new point as it arrives.  Note: to see more than one pin on the map, set the Group By attribute on the data stream used by the map.

### labelProperty:string
#### The property that contains a label for each location

This value must contain the name of a valid property in the DataStream objects that contains a label for the corresponding point in "dataStreamProperty".



### locationHash:any
#### A read-only property containing a hash table that reflects the current displayed location data

This hash table can be used to get information about the current location data being displayed. The 'key' for each item in the hash is the same as the key you have supplied for each location in the incoming data. Each object contains these properties:

The 'dataObject' property contains the most recent data record which was received by the DataStream (which contains the current position.)

The 'gmMarker' property contains the Google Maps "Marker" that represents the point being displayed.

The 'url' property indicates the icon that is being used to display this point.

The 'xc' and 'yc' properties contain the offset in pixels within the icon which indicated the "center-point" of the image.



### map:any
#### The Google 'Map' object

This value is the actual google.maps.Map object that gives access to the features of the Google Maps API. Documentation can be found [here](https://developers.google.com/maps/documentation/javascript/tutorial). For example, you might use this to position the map to a specific location:

```js
var mapWidget = client.getWidget("myMapWidget");
var map = mapWidget.map;

map.setCenter({lat: 33.812093, lng: -117.918973});

```

### maptype:string
#### The map type

This value must be a valid map type, one of "Roadmap", "Hybrid", "Satellite" or "Terrain". (The default is "Roadmap".) You should specify this value using one of these four constants:


* DynamicMapViewer.MAPTYPE_ROADMAP
* DynamicMapViewer.MAPTYPE_HYBRID
* DynamicMapViewer.MAPTYPE_SATELLITE
* DynamicMapViewer.MAPTYPE_TERRAIN



### markerArray:any[]
#### An array containing a pool of icons to be assigned to data points

When a point object arrives from the DataStream it should have a "key" property which uniquely identifies it. In order to decide which icon to use to display it the Widget will first try to look it up in the hash table defined by the "markerHash" property (see below). If the key is not in the hash (or no hash table was defined) then the icon will be assigned from a pool defined by the markerArray. (If markerArray was not defined then a set of builtin icons will be used in its place.)

For example, you might supply a markerArray which looks like this:

```js
[
    {
        url: "firstIcon.png",
        xc: 16,
        yc: 16
    },
    {
        url: "secondIcon.png",
        xc: 10,
        yc: 10
    } 
]

```

The first data point to not have an icon assigned via markerHash will use the next icon in the markerArray list and its key will be bound to that icon from now on (so if later on the point with that key moves the same icon will be used).

The "url" property  must either contain a Document name or a full URL.
The "origin" or "centerpoint" of the
icon will come from the (xc,yc) offsets. (This offset will be used to position to icon relative to the actual point so 
the "center" or "tip" will appear in the right place.)

Each successive point with an unmatched key will use the next icon in the pool, wrapping around back to the beginning if necessary.



### markerHash:any
#### A hash table object defining the icons to be used for a given key

When a point object arrives from the DataStream it should have a "key" property which identifies it. In order to decide
what icon to use to display it, the Widget will first try to look it up in the hash table defined by the "markerHash" 
property.

For example, you might supply a markerHash which looks like this:

```js
{
    "Joe": {
        url: "joesIcon.png",
        xc: 16,
        yc: 16
    },
    "Bob": {
        url: "bobsIcon.png",
        xc: 10,
        yc: 10
    } 
}
```

The data point's key (e.g. "Joe") will be used as the key into the markerHash table. If a matching entry is found it will be assigned the designated icon.

(There are actually two different ways to use the Marker Hash to determine the image used for a data point. See [here](tutorials/imagemaptutorial.md#6-customizing-markers) for details.)

The "url" property  must either contain a Document name or a full URL.
The "origin" or "centerpoint" of the
icon will come from the (xc,yc) offsets. (This offset will be used to position to icon relative to the actual point so 
the "center" or "tip" will appear in the right place.)

If the key is not defined in the hash table then the markerArray (or the builtin defaults) will be used to assign an icon.


### markerHashKeyProperty:string
#### Name of the property containing the "type" of a location marker

This widget allows you to specify a hash table of "marker icons" in the markerHash property so you can identify a separate icon for each different "natural key" in the incoming location data. This would mean a separate icon for each different unique key. This works for some use cases but is awkward for others; sometimes you want to track many different object locations but the marker should be based on the "type" of the object. 

The markerHashKeyProperty is optional but if specified it looks in the indicated property of the data for the object's 'type' and then uses **that** value to look up an icon in the marker hash table.
    
There is a deeper discussion of this issue found [here](tutorials/imagemaptutorial.md#6-customizing-markers).

### showPointsOfInterest:boolean
#### Indicate if the map should show "points of interest"
If "showPointsOfInterest" is "true" the map will show points of interest such as restaurants, gas stations and so forth. If "showPointsOfInterest" is "false" (the default) then these points will not be shown.

### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.



<hr>

## FixedLayout
<span style="font-style:italic;">[Widget](#widget) &#x2192; [WidgetContainer](#widgetcontainer) &#x2192; FixedLayout</span>

This is a "container" widget that (unlike most of the others) does not change the position of its children. You are expected to position children yourself (either using the Client Builder or programmatically at runtime). This means that is possible for children to overlap and obscure each other depending on their "stacking order". (This can be controlled by various Widget methods and properties such as [bringtofront()](#bringtofront)).

This container also duplicates the functionality of the [FloorplanViewer](#floorplanviewer) in that it can be bound to a DataStream and show "markers" based on position data.


### dataStreamProperty:string
#### The property that contains the GeoJSON Location value

This value must contain the name of a valid property in the DataStream objects that contains the GeoJSON location.

### dataStreamUUID:string
#### The UUID of the DataStream to which the Widget is bound

If you have a DataStream object you can get its UUID using "theDataStreamObject.uuid";



### filterObjectString:string
#### String version on a JSON objects containing filtering information

This property is optional; it is the stringified version of a JSON object which contains information on how to filter the incoming data.

The object should look something like this:

```js
var filterObject = {
    floorNumber: 2
}
```

This means that the FloorplanViewer will only use location data from data objects which also contain a property called "floorNumber" with a value of "2". This is useful if you a single Data Stream reporting location data but wish to divide it up into multiple FloorplanViewers which show different floors or areas.


### horizontalOverflow:string
#### Control the horizontal scrolling behavior when the FixedLayout is used as a TabbedLayout page

This property is only meaningful when the FixedLayout is being used as a "page" for a TabbedLayout. It can be set to one of "hidden" (the default), "scroll" or "auto". These settings are used the same way as the CSS "overflow-x" property, controlling if and when a horizontal scrollbar will be displayed.


### imageHeightInLocationUnits:number
#### The height of the image

This describes the height of the image in whatever units the Location data uses.

### imageWidthInLocationUnits:number
#### The width of the image

This describes the width of the image in whatever units the Location data uses.



### labelProperty:string
#### The property that contains a label for each location

This value must contain the name of a valid property in the DataStream objects that contains a label for the corresponding point in "dataStreamProperty".



### locationHash:any
#### A read-only property containing a hash table that reflects the current displayed location data

This hash table can be used to get information about the current location data being displayed. The 'key' for each item in the hash is the same as the key you have supplied for each location in the incoming data. Each object contains these properties:

The 'x' and 'y' properties contain the current location of the item in "location units".

The 'xPixels' and 'yPixels' properties contain the current location of the item in pixels.

The 'dataObject' property contains the most recent data record which was received by the DataStream (which contains the current position.)

The 'element' property contains the JQuery object that describes the icon's "img" DOM element.

The 'url' property indicates the icon that is being used to display this point.

The 'xc' and 'yc' properties contain the offset in pixels within the icon which indicated the "center-point" of the image.



### markerArray:any[]
#### An array containing a pool of icons to be assigned to data points

When a point object arrives from the DataStream it should have a "key" property which uniquely identifies it. In order to decide
which icon to use to display it the Widget will first try to look it up in the hash table defined by the "markerHash" 
property (see below). If the key is not in the hash (or no hash table was defined) then the icon will be assigned
from a pool defined by the markerArray. (If markerArray was not defined then a set of builtin icons will be used in its place.)

For example, you might supply a markerArray which looks like this:

```js
[
    {
        url: "firstIcon.png",
        xc: 16,
        yc: 16
    },
    {
        url: "secondIcon.png",
        xc: 10,
        yc: 10
    } 
]

```

The first data point to not have an icon assigned via markerHash will use the next icon in the markerArray list and its
key will be bound to that icon from now on (so if later on the point with that key moves the same icon will be used).

The "url" property  must either contain a Document name or a full URL.
The "origin" or "centerpoint" of the
icon will come from the (xc,yc) offsets. (This offset will be used to position to icon relative to the actual point so 
the "center" or "tip" will appear in the right place.)

Each successive point with an unmatched key will use the next icon in the pool, wrapping around back to the beginning if necessary.



### markerHash:any
#### A hash table object defining the icons to be used for a given key

When a point object arrives from the DataStream it should have a "key" property which identifies it. In order to decide
what icon to use to display it, the Widget will first try to look it up in the hash table defined by the "markerHash" 
property.

For example, you might supply a markerHash which looks like this:

```js
{
    "Joe": {
        url: "joesIcon.png",
        xc: 16,
        yc: 16
    },
    "Bob": {
        url: "bobsIcon.png",
        xc: 10,
        yc: 10
    } 
}
```

The data point's key (e.g. "Joe") will be used as the key into the markerHash table. If a matching entry is found it
will be assigned the designated icon.

(There are actually two different ways to use the Marker Hash to determine the image used for a data point. See [here](tutorials/imagemaptutorial.md#6-customizing-markers) for details.)

The "url" property  must either contain a Document name or a full URL.
The "origin" or "centerpoint" of the
icon will come from the (xc,yc) offsets. (This offset will be used to position to icon relative to the actual point so 
the "center" or "tip" will appear in the right place.)

If the key is not defined in the hash table then the markerArray (or the builtin defaults) will be used to assign an icon.


### markerHashKeyProperty:string
#### Name of the property containing the "type" of a location marker

This widget allows you to specify a hash table of "marker icons" in the markerHash property so you can identify a separate icon for each different "natural key" in the incoming location data. This would mean a separate icon for each different unique key. This works for some use cases but is awkward for others; sometimes you want to track many different object locations but the marker should be based on the "type" of the object. 

The markerHashKeyProperty is optional but if specified it looks in the indicated property of the data for the object's 'type' and then uses **that** value to look up an icon in the marker hash table.
    
There is a deeper discussion of this issue found [here](tutorials/imagemaptutorial.md#6-customizing-markers).



### removeLocationByKey()
#### Remove the marker icon which corresponds to the supplied key value


```js
removeLocationByKey(locationKey:string)
```

* locationKey: string - The key of the marker to be removed from the display




### removeLocationsByType()
#### Remove the marker icons which corresponds to the supplied type value


```js
removeLocationsByType(typeKey:any)
```

* typeKey: string - The type of the marker to be removed from the display


This method is only relevant if you have set 'markerHashKeyProperty' to identify a property within the data object that contains the "type" of the marker. Calling this method will remove all markers that match the indicated typeKey value.

This method will throw an exception if you call if **without** specifying a 'markerHashKeyProperty'.

### scaledImageHeight:number
#### The current height of the scaled image in pixels

This is a readonly property giving the scaled height of the background image (loaded via the "url" parameter).

### scaledImageWidth:number
#### The current width of the scaled image in pixels

This is a readonly property giving the scaled width of the background image (loaded via the "url" parameter).


### tabIcon:string
#### The Document URL for the icon of this FixedLayout 'page' when it is inside a TabbedLayout

The children of a [TabbedLayout](#tabbedlayout) container are all FixedLayout Widgets. This property defines the icon (if any) that is displayed next to the label for this FixedLayout's 'page' within the [TabbedLayout](#tabbedlayout). This property is ignored for FixedLayouts whose parent is not a [TabbedLayout](#tabbedlayout).

There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).

### tabName:string
#### The label of this FixedLayout 'page' when it is inside a TabbedLayout

The children of a [TabbedLayout](#tabbedlayout) container are all FixedLayout Widgets. This property is the label for this FixedLayout's 'page' within the [TabbedLayout](#tabbedlayout). This property is ignored for FixedLayouts whose parent is not a [TabbedLayout](#tabbedlayout).


### trueImageHeight:number
#### The actual height of the image in pixels

This is a readonly property giving the actual height of the background image (loaded via the "url" parameter).

### trueImageWidth:number
#### The actual width of the image in pixels

This is a readonly property giving the actual width of the background image (loaded via the "url" parameter).


### url:string
#### The URL of a Document containing an image to be shown in the background

This value must contain the name of a valid property in the DataStream objects that contains a label for the corresponding point in "dataStreamProperty".


There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).

### verticalOverflow:string
#### Control the vertical scrolling behavior when the FixedLayout is used as a TabbedLayout page

This property is only meaningful when the FixedLayout is being used as a "page" for a TabbedLayout. It can be set to one of "hidden" (the default), "scroll" or "auto". These settings are used the same way as the CSS "overflow-y" property, controlling if and when a vertical scrollbar will be displayed.


### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' parameter is an object with 'x', 'y', 'floorPlanUnitsX' and 'floorPlanUnitsY' properties giving
the offset of the click. If the click was over a marker icon then 'extra.markerKey' and 'extra.markerDataObject' are 
also set. 'markerKey' holds the value of the key that identifies the clicked marker and
'markerDataObject' is the most recent object which arrived from the DataStream that updated the marker's location.



### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.












<hr>

## FloorplanViewer
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; FloorplanViewer</span>

This Widget shows location points on a fixed image (floorplan) as they arrive from the Data Stream.

### borderThickness:number
#### The thickness of the border in pixels


### clearData()
#### Remove all existing Floorplan markers

To remove any and all Floorplan markers, use the clearData() method. For example:
```js
var fpWidget = client.getWidget("myFloorplanWidget");
fpWidget.clearData();
```

This method used to be called "clearMarkers" but was renamed for consistency. Either "clearData" or "clearMarkers" will work.

### dataStreamProperty:string
#### The property that contains the GeoJSON Location value

This value must contain the name of a valid property in the DataStream objects that contains the GeoJSON location.


### filterObjectString:string
#### String version on a JSON objects containing filtering information

This property is optional; it is the stringified version of a JSON object which contains information on how to filter the incoming data.

The object should look something like this:

```js
var filterObject = {
    floorNumber: 2
}
```

This means that the FloorplanViewer will only use location data from data objects which also contain a property called "floorNumber" with a value of "2". This is useful if you a single Data Stream reporting location data but wish to divide it up into multiple FloorplanViewers which show different floors or areas.


### imageHeightInLocationUnits:number
#### The height of the image

This describes the height of the image in whatever units the Location data uses.

### imageWidthInLocationUnits:number
#### The width of the image

This describes the width of the image in whatever units the Location data uses.

### isScaleable:boolean
#### Indicates whether the image is scaled or shown at its "natural" size

If this property is "false" (the default) the Widget (and the image it contains) are shown at the image's "natural" size. If "true" then the image is scaled to the Widget's width (and the height is scaled to maintain the correct aspect ratio).


### labelProperty:string
#### The property that contains a label for each location

This value must contain the name of a valid property in the DataStream objects that contains a label for the corresponding point in "dataStreamProperty".



### locationHash:any
#### A read-only property containing a hash table that reflects the current displayed location data

This hash table can be used to get information about the current location data being displayed. The 'key' for each item in the hash is the same as the key you have supplied for each location in the incoming data. Each object contains these properties:

The 'x' and 'y' properties contain the current location of the item in "location units".

The 'xPixels' and 'yPixels' properties contain the current location of the item in pixels.

The 'dataObject' property contains the most recent data record which was received by the DataStream (which contains the current position.)

The 'element' property contains the JQuery object that describes the icon's "img" DOM element.

The 'url' property indicates the icon that is being used to display this point.

The 'xc' and 'yc' properties contain the offset in pixels within the icon which indicated the "center-point" of the image.



### markerArray:any[]
#### An array containing a pool of icons to be assigned to data points

When a point object arrives from the DataStream it should have a "key" property which uniquely identifies it. In order to decide
which icon to use to display it the Widget will first try to look it up in the hash table defined by the "markerHash" 
property (see below). If the key is not in the hash (or no hash table was defined) then the icon will be assigned
from a pool defined by the markerArray. (If markerArray was not defined then a set of builtin icons will be used in its place.)

For example, you might supply a markerArray which looks like this:

```js
[
    {
        url: "firstIcon.png",
        xc: 16,
        yc: 16
    },
    {
        url: "secondIcon.png",
        xc: 10,
        yc: 10
    } 
]

```

The first data point to not have an icon assigned via markerHash will use the next icon in the markerArray list and its
key will be bound to that icon from now on (so if later on the point with that key moves the same icon will be used).

The "url" property  must either contain a Document name or a full URL.
The "origin" or "centerpoint" of the
icon will come from the (xc,yc) offsets. (This offset will be used to position to icon relative to the actual point so 
the "center" or "tip" will appear in the right place.)

Each successive point with an unmatched key will use the next icon in the pool, wrapping around back to the beginning if necessary.



### markerHash:any
#### A hash table object defining the icons to be used for a given key

When a point object arrives from the DataStream it should have a "key" property which identifies it. In order to decide
what icon to use to display it, the Widget will first try to look it up in the hash table defined by the "markerHash" 
property.

For example, you might supply a markerHash which looks like this:

```js
{
    "Joe": {
        url: "joesIcon.png",
        xc: 16,
        yc: 16
    },
    "Bob": {
        url: "bobsIcon.png",
        xc: 10,
        yc: 10
    } 
}
```

The data point's key (e.g. "Joe") will be used as the key into the markerHash table. If a matching entry is found it
will be assigned the designated icon.

(There are actually two different ways to use the Marker Hash to determine the image used for a data point. See [here](tutorials/imagemaptutorial.md#6-customizing-markers) for details.)

The "url" property  must either contain a Document name or a full URL.
The "origin" or "centerpoint" of the
icon will come from the (xc,yc) offsets. (This offset will be used to position to icon relative to the actual point so 
the "center" or "tip" will appear in the right place.)

If the key is not defined in the hash table then the markerArray (or the builtin defaults) will be used to assign an icon.


### markerHashKeyProperty:string
#### Name of the property containing the "type" of a location marker

This widget allows you to specify a hash table of "marker icons" in the markerHash property so you can identify a separate icon for each different "natural key" in the incoming location data. This would mean a separate icon for each different unique key. This works for some use cases but is awkward for others; sometimes you want to track many different object locations but the marker should be based on the "type" of the object. 

The markerHashKeyProperty is optional but if specified it looks in the indicated property of the data for the object's 'type' and then uses **that** value to look up an icon in the marker hash table.
    
There is a deeper discussion of this issue found [here](tutorials/imagemaptutorial.md#6-customizing-markers).




### removeLocationByKey()
#### Remove the marker icon which corresponds to the supplied key value


```js
removeLocationByKey(locationKey:string)
```

* locationKey: string - The key of the marker to be removed from the display




### removeLocationsByType()
#### Remove the marker icons which corresponds to the supplied type value


```js
removeLocationsByType(typeKey:any)
```

* typeKey: string - The type of the marker to be removed from the display


This method is only relevant if you have set 'markerHashKeyProperty' to identify a property within the data object that contains the "type" of the marker. Calling this method will remove all markers that match the indicated typeKey value.

This method will throw an exception if you call if **without** specifying a 'markerHashKeyProperty'.



### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' parameter is an object with 'x', 'y', 'floorPlanUnitsX' and 'floorPlanUnitsY' properties giving
the offset of the click. If the click was over a marker icon then 'extra.markerKey' and 'extra.markerDataObject' are 
also set. 'markerKey' holds the value of the key that identifies the clicked marker and
'markerDataObject' is the most recent object which arrived from the DataStream that updated the marker's location.




### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.
















<hr>

## FlowLayout
<span style="font-style:italic;">[Widget](#widget) &#x2192; [WidgetContainer](#widgetcontainer) &#x2192; FlowLayout</span>

This is a "container" widget that arranges its visible children into a "flow" where they arranged left-to-right and top-to-bottom in the same manner that an HTML "div" does. The children are arranged from left-to-right in the order given by the "children" property. (The index of a child within its parent's "children" array determines its position in the flow.)

The width of a FlowLayout determines where the children "wrap"; the height of a FlowLayout grows as necessary to accommodate its children.








<hr>

## Gauge
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; Gauge</span>

This Widget shows a simple "gauge" that displays a single value from the most recent object from the Data Stream.

The range of the Gauge is defined by the "minimum" and "maximum property". Within the range, sections of gauge are designated "low", "medium" and "high". (By
default these are colored "green", "yellow" or "red".) 
If different color zones overlap then "medium" will be drawn on top of "low" and "high" will be drawn on top of "medium".


### borderThickness:number
#### The thickness of the border in pixels

### chartConfig
#### Access to the [ZingChart Gauge](https://www.zingchart.com/docs/chart-types/gauge) configuration
Reading from _chartConfig_ returns a JavaScript object which contains the current runtime Gauge configuration parameters. Writing to _chartConfig_ allows the user to programmatically change the appearance of the Gauge.

For example, the following reads the current configuration and changes the Gauge's background color to _gray_:
```js
	var chart = client.getWidget("Gauge1");
	var config = chart.chartConfig;
	config.data.backgroundColor = "gray";
	chart.chartConfig = config;
```

Please refer to the ZingChart link above for configuration options available for the Gauge.

### chartSeries
#### Access to the [ZingChart Gauge](https://www.zingchart.com/docs/chart-types/gauge) displayed data
Reading from _chartSeries_ returns a JavaScript object which contains the current runtime Gauge data. Writing to _chartSeries_ allows the user to programmatically change the data displayed by the Gauge.

For example, the following changes the Gauge to contain two needles with different values:
```js
	var chart = client.getWidget("Gauge1");
	var series = [{"values":[181]},{"values":[192]}];
	chart.chartSeries = series;
```
Please refer to the ZingChart link above for the format of series data required for the Gauge.

### dataStreamProperty:string
#### The property that contains the GeoJSON Location value

This value must contain the name of a valid property in the DataStream objects that contains the GeoJSON location.


### maximum:number
#### The maximum value displayed by the Gauge


### minimum:number
#### The minimum value displayed by the Gauge

### lowColor:string
#### The color of the "low" zone of the Gauge
Defaults to green.

### lowZones:string
#### "low" zones of gauge (defaults to green)
Zones can be specified as a series of "from:to" ranges separated by a space.  For example, "20:40 80:90". A single value is the equivalent of "value:maximum".

### mediumColor:string
#### The color of the "medium" zone of the Gauge
Defaults to yellow.

### mediumZones:string
#### "medium" zones of gauge (defaults to yellow)

Zones can be specified as a series of "from:to" ranges separated by a space.  For example, "20:40 80:90". A single value is the equivalent of "value:maximum".

### highColor:string
#### The color of the "high" zone of the Gauge
Defaults to yellow.

### highZones:string
#### "high" zones of gauge (defaults to red)

Zones can be specified as a series of "from:to" ranges separated by a space.  For example, "20:40 80:90". A single value is the equivalent of "value:maximum".


### title:string
#### Title superimposed on the widget

This property will superimpose a title on the Widget; the title is null by default.


### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.



<hr>

## GridLayout
<span style="font-style:italic;">[Widget](#widget) &#x2192; [WidgetContainer](#widgetcontainer) &#x2192; GridLayout</span>

This is a "container" widget that arranges its visible children into a "grid" with a fixed number of rows and columns.
 (The index of a child within its parent's "children" array is irrelevant.) A grid "cell" can only contain one child at a time.
 
You can adjust the number of cells in a GridLayout by changing the "rows" and "columns" property, but any cells which would be "lost" must be empty.

### columns:number
#### The number of columns in the Grid

The number of columns must be a positive integer (default is "2").


### rows:number
#### The number of rows in the Grid

The number of rows must be a positive integer (default is "2").




<hr>

## HorizontalLayout
<span style="font-style:italic;">[Widget](#widget) &#x2192; [WidgetContainer](#widgetcontainer) &#x2192; HorizontalLayout</span>

This is a "container" widget that arranges its visible children into a horizontal "stack". The children are arranged from left-to-right in the order given by the "children" property. (The index of a child within its parent's "children" array determines its position in the stack.)



<hr>

## ImageMarkup
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; ImageMarkup</span>

This Widget is used to show an image to the user which can be "marked up" using some simple drawing tools. The image can come from the camera (so the user can snap a picture and then mark it up) or from an image Document or URL.



### clearUpload()
#### Reset the markup image to its initial state

```js
clearUpload():void
```

After an image has been marked up, call this method to reset it to "empty".


### documentName:string
#### The name of the document to which the image was uploaded

This property is readonly - it will be null until after an image has been captured and uploaded at which time it contains the name of the Document where it was saved.

### documentGroupName:string
#### The name of the Group to which the uploaded Document should be assigned

When this Widget creates and uploads a Document it will be assigned to the indicated [Group](resourceguide.md#groups). This is useful for controlling which users will have access to the Document.


### maxWidth:number
#### Restrict the size of the captured image
Markup images returned by mobile devices can be quite large so can cause long upload and download times. To restrict the size of the image returned, enter a value for the _maxWidth_ property. If the markup image width is larger than the _maxWidth_ property, the image is scaled such that the width matches the _maxWidth_ value and the height is scaled to match the aspect ratio of the markup image. If no value is provided for the _maxWidth_ property, the markup image is returned unmodified.

### optional:boolean
#### Specify whether a clip must be recorded before a default "submit"

### placeholder:string
#### The optional "placeholder" value

If "source" has been set to "camera" the placeholder defaults to "Take a photo and mark it up". Otherwise
 the default is "Mark up an image".
 
### source:string
#### The source of the image to be offered to the user for markup

This may be the string "camera" (if you want the user to snap an image first), the URL of an accessible image from the internet
or an image Document in the Vantiq server. (Image Documents must start with "rcs/image/...").

The default value is "camera".

### thumbnailSize:number
#### Create a thumbnail image for the captured image
To create a second, 'thumbnail' version of the markup image, enter a value for the _thumbnailSize_ property. If the _thumbnailSize_ property is specified, an image is created with its width or height, whichever is greater, scaled such that it matches the _thumbnailSize_ value and the lesser of the width or height is scaled to match the aspect ratio of the captured image. If no value is provided for the _thumbnailSize_ property, no thumbnail image is returned.

The uploaded thumbnail document will have the same name as the uploaded markup document with a suffix of "Thumbnail" before the file extension.


### 'On Change' Event

This Widget supports an "On Change" Event Handler which fires after the user has successfully marked up an image. 
The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains null;





<hr>

## InputDate
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; InputDate</span>

This Widget is used to enter or edit only the "date" portion of a DateTime. When clicked the Widget will show an appropriate popup Dialog which will allow the user to enter and edit the bound data.

### boundValue:string
The value of the date. Will be _undefined_ until the user has selected a value.

### dataBinding:string
#### The name of an Object or TypedObject DataObject variable 

This Widget can be bound to a DataObject variable of type "DateTime" (e.g. "client.data.myDate"). The DataObject variable may be marked as an array. Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.

### defaultValue:any
#### The default value for the Widget

If the widget is bound to a DataObject then the DataObject's value overrides this default.

### isReadOnly:boolean
#### Disables input into the field

### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.


### 'On Validation' Event

The Widget's 'On Validation' Event is fired as a part of the "Validation" process which is 
described [here](cbuser.md#field-validation).

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onValidation(client,vco)
```

where "this" points to the Page object and "client" points to the Client object. "vco" is the "Validation Control
Object" which is used to describe the current state of validation and to declare your own validation errors.



## InputDateTime
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; InputDateTime</span>

This Widget is used to enter or edit DateTime values. When clicked the Widget will show an appropriate popup Dialog which will allow the user to enter and edit the bound data.

### boundValue:string
The value of the date/time widget. Will be _undefined_ until the user has selected a value.

### dataBinding:string
#### The name of a DateTime variable 

This Widget can be bound to a DataObject variable of type "DateTime" (e.g. "client.data.myDateTime"). Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.

### defaultValue:any
#### The default value for the Widget

If the widget is bound to a DataObject then the DataObject's value overrides this default.

### isReadOnly:boolean
#### Disables input into the field

### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.


### 'On Validation' Event

The Widget's 'On Validation' Event is fired as a part of the "Validation" process which is 
described [here](cbuser.md#field-validation).

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onValidation(client,vco)
```

where "this" points to the Page object and "client" points to the Client object. "vco" is the "Validation Control
Object" which is used to describe the current state of validation and to declare your own validation errors.



<hr>

## ImageViewer
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; ImageViewer</span>

This Widget allows you to display an image inside a [VerticalLayout](#verticallayout) at a reduced size. (Its width is sized to the width of its parent and the height is scaled to match). When clicked the image displays at full size inside another browser tab.

The [StaticImage](#staticimage) and [ImageViewer](#imageviewer) widgets are very similar widgets. They differ in that the StaticImage is just an image, analogous to the StaticText widget. The ImageViewer supports the optional "label" property and when the image is clicked at runtime it will be displayed in a separate window at full resolution.



### url:string
#### The url of the image to display

There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).


<hr>

## InputInteger
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; [InputNumeric](#inputnumeric) &#x2192; InputInteger</span>

This Widget is used to input an Integer value.

### dataBinding:string
#### The name of an Integer DataObject variable

This Widget can be bound to a DataObject variable of type "Integer" (e.g. "client.data.myInteger"). Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.

### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.


### 'On Validation' Event

The Widget's 'On Validation' Event is fired as a part of the "Validation" process which is 
described [here](cbuser.md#field-validation).

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onValidation(client,vco)
```

where "this" points to the Page object and "client" points to the Client object. "vco" is the "Validation Control
Object" which is used to describe the current state of validation and to declare your own validation errors.



<hr>

## InputNumeric
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; InputNumeric</span>

This is the superclass of the two "numeric input" Widgets [InputInteger](#inputinteger) and [InputReal](#inputreal). It is a non-leaf class and cannot be instantiated.

### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.


### 'On Validation' Event

The Widget's 'On Validation' Event is fired as a part of the "Validation" process which is 
described [here](cbuser.md#field-validation).

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onValidation(client,vco)
```

where "this" points to the Page object and "client" points to the Client object. "vco" is the "Validation Control
Object" which is used to describe the current state of validation and to declare your own validation errors.

### boundValue:number
The value of the widget. Will be _undefined_ until the user has input a value or null if the user clears the value.

### defaultValue:number
#### The default value for the Widget

If the widget is bound to a DataObject then the DataObject's value overrides this default.

### flavor:string
#### The display style of the input control

When editing or displaying numeric input you can specify the "flavor" of the Widget; this must be either "text" or "slider".

### isReadOnly:boolean
#### Disables input into the field

### maxValue:number
#### The maximum value when in "slider" mode

Defaults to "100".

### minValue:number
#### The minimum value when in "slider" mode

Defaults to "0".

### optional:boolean
#### Specify whether a value must be entered before a default "submit"

### placeholder:string
#### The optional "placeholder" value when in "text" mode

Defaults to "".

### units:string
#### The optional "units" text label when in "slider" mode

Defaults to "".



### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.


### 'On Validation' Event

The Widget's 'On Validation' Event is fired as a part of the "Validation" process which is 
described [here](cbuser.md#field-validation).

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onValidation(client,vco)
```

where "this" points to the Page object and "client" points to the Client object. "vco" is the "Validation Control
Object" which is used to describe the current state of validation and to declare your own validation errors.


<hr>

## InputObject
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; InputObject</span>

This Widget is used to enter Objects, arrays of Objects, TypedObjects or arrays of TypedObjects. When clicked the Widget will show an appropriate popup Dialog which will allow the user to enter and edit the bound data.

### dataBinding:string
#### The name of an Object or TypedObject DataObject variable 

This Widget can be bound to a DataObject variable of type "Object" or "TypedObject" (e.g. "client.data.myObject"). The DataObject variable may be marked as an array. Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.

### defaultValue:any
#### The default value for the Widget

If the widget is bound to a DataObject then the DataObject's value overrides this default.

### isReadOnly:boolean
#### Disables input into the field

### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.



<hr>

## InputReal
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; [InputNumeric](#inputnumeric) &#x2192; InputReal</span>

This Widget is used to input a Real value.

### dataBinding:string
#### The name of an Real DataObject variable

This Widget can be bound to a DataObject variable of type "Real" (e.g. "client.data.myReal"). Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.


### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.


### 'On Validation' Event

The Widget's 'On Validation' Event is fired as a part of the "Validation" process which is 
described [here](cbuser.md#field-validation).

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onValidation(client,vco)
```

where "this" points to the Page object and "client" points to the Client object. "vco" is the "Validation Control
Object" which is used to describe the current state of validation and to declare your own validation errors.



<hr>

## InputString
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; InputString</span>

This Widget is used to enter a String value.

### boundValue:string
The value of the string. Will be _undefined_ until the user has input a value.

### dataBinding:string
#### The name of a String DataObject variable

This Widget can be bound to a DataObject variable of type "String" (e.g. "client.data.myString"). Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.

### defaultValue:string
#### The default value for the Widget

If the widget is bound to a DataObject then the DataObject's value overrides this default.

### inputType:string
#### Specify the type of input expected for the data.

Legal values are _text_, _email_, _password_, _telephone_ and _url_. The inputType value signals the browser or mobile app to display appropriate keyboards when data is being entered. For example, _telephone_ signals the mobile app to display a keyboard that is tailored to entering phone numbers.

### isPassword:boolean
#### Specify if this is a "password" field (masking the input)
Deprecated. Use *inputType* instead.

### isReadOnly:boolean
#### Disables input into the field

### optional:boolean
#### Specify whether a value must be entered before a default "submit"

### placeholder:string
#### The optional "placeholder" value

Defaults to "".



### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.


### 'On Validation' Event

The Widget's 'On Validation' Event is fired as a part of the "Validation" process which is 
described [here](cbuser.md#field-validation).

The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onValidation(client,vco)
```

where "this" points to the Page object and "client" points to the Client object. "vco" is the "Validation Control
Object" which is used to describe the current state of validation and to declare your own validation errors.


<hr>

## Label
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; Label</span>

This is a special kind of [ControlWidget](#controlwidget) which contains no active Widget but just the "Label" portion. It is intended for use inside a [VerticalLayout](#verticallayout) with other ControlWidgets. In other cases it is more appropriate to use the [StaticText](#statictext) Widget.


It differs from [SectionLabel](#sectionlabel) in that it has a slightly different appearance making it suitable for labeling a single item rather than an entire "section" in the [VerticalLayout](#verticallayout).


The [Label](#label) and [StaticText](#statictext) widgets are virtually identical; the Label still exists for reasons of backwards compatibility and the StaticText widget is preferred going forward.


<hr>

## LineChart
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; LineChart</span>

This Widget draws a "line chart".

### axisAutoRange:boolean
#### Indicate whether the range of Y axis is automatically adjusted.


### bindEvents:any
#### Listen for internal ZingChart events

ZingChart widgets such as this one support a mechanism that allows you to listen for various ZingChart internal [events](https://www.zingchart.com/docs/api/events). This would normally be done through the ZingChart ["bind()"](https://www.zingchart.com/docs/api/events#-bind-) mechanism but in order to be compatible with the Vantiq widgets you need to use the "bindEvents" property instead.

To define the listeners you assign an object to the "bindZEvents" property like this:

```js
var wdg = client.getWidget("LineChart1");
wdg.bindEvents = {
        "setdata":function(e)
        {
            console.log("setdata: " + e.id);
        },
        "node_click":function(e)
        {
            console.log("node_click: " + e.id);
        }
    };
```


### borderThickness:number
#### The thickness of the border in pixels

### chartConfig
#### Access to the [ZingChart Line Chart](https://www.zingchart.com/docs/chart-types/line) configuration
Reading from _chartConfig_ returns a JavaScript object which contains the current runtime Line Chart configuration parameters. Writing to _chartConfig_ allows the user to programmatically change the appearance of the Line Chart.

For example, the following reads the current configuration and changes the Line Chart to use spline plotting:
```js
	var chart = client.getWidget("LineChart1");
	var config = chart.chartConfig;
    config.data.plot = {"aspect":"spline"};
	chart.chartConfig = config;
```

Please refer to the ZingChart link above for configuration options available for the Line Chart.

### chartSeries
#### Access to the [ZingChart Line Chart](https://www.zingchart.com/docs/chart-types/line) displayed data
Reading from _chartSeries_ returns a JavaScript object which contains the current runtime chart data. Writing to _chartSeries_ allows the user to programmatically change the data displayed by the chart.

For example, the following changes the Line Chart to contain three data timestamp data points that represent speed:
```js
	var chart = client.getWidget("LineChart1");
	var series = [{"values":[[1420070401000, 100],[1420070402000,30],[1420070403000,90]],"text":"speed"}];
	chart.chartSeries = series;
```

Please refer to the ZingChart link above for the format of series data required for the Line Chart.

### displayThreshold:string
#### Indicate whether a thresholdline will be drawn across the chart at "thresholdValue"

"displayThreshold" may be set to either "Yes" or "No" (the default is "No"). When "Yes" is specified the value of the "thresholdValue" property is used to draw a "threshold line" across the chart at the indicated point.

### hasGridLines:boolean
#### Indicate whether grid lines should be drawn across the chart


### showArea:boolean
#### Indicate whether the area should be drawn in under the chart lines


### showPoints:boolean
#### Indicate whether the data points should be draw on the chart lines


### thresholdValue:number
#### The value where the threshold line should be drawn

Ignored unless "displayThreshold" is set to "Yes".


### title:string
#### Title superimposed on the widget

This property will superimpose a title on the Widget; the title is null by default.

### xAxisProperty:string
#### The property to be used for the X-Axis

This value must either be the name of a valid property in the DataStream objects **or** the special string "-TIMESTAMP-" (which means to use the "arrival time" of the DataStream event).



### yAxisProperties:DataStreamListElement[]
#### The properties to be used for the Y-Axis

This value must be an array of DataStreamListElement objects; you instantiate them like this:

```js
var dsle = new DataStreamListElement(propertyName:string, label:string);
```

where "propertyName" is the name of a valid property in the incoming DataStream objects and "label" is a human-readable to be label to used when drawing the chart.


### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' parameter is an object with 'x' and 'y' properties giving the offset of the click.


### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.


<hr>

## ListViewer
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; ListViewer</span>

This Widget shows a single value from the most recent objects to arrive on the Data Stream. Each display row also includes the time that the row arrived.

### borderThickness:number
#### The thickness of the border in pixels

### dataStreamProperty:string
#### The property within the Data Stream object to display in the list


### hasSeparators:boolean
#### Indicates whether to show separators between the rows

### maxRows:number
#### The maximum number of rows the List Viewer should display


### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.




<hr>

## MapViewer
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; MapViewer</span>

This Widget is used to launch a map viewer at a specific location. This is different from the functionality provided by 
[DynamicMapViewer](#dynamicmapviewer) which tracks location data coming in from
a DataStream.

Note that this Widget can be used to collect input as well; the user may click on the map to indicate a location
which will become the "value" of the Widget when results are sent to the server.


### defaultValue:any
#### The default location for the center of the map

This allows you to supply a default value for the center of the map. It may be either a GeoJSON POINT object or
a simple JSON object with the properties "longitude" and "latitude".


### maptype:string
#### The map type

This value must be a valid map type, one of "Standard", "Hybrid" or "Satellite". (The default is "Standard".) You should specify this value using one of these three constants:

* MapViewer.MAPTYPE_STANDARD
* MapViewer.MAPTYPE_HYBRID
* MapViewer.MAPTYPE_SATELLITE


### markers:any[]
#### An array describing markers which are to appear on the map

Here is an example of an array which describes two markers:

```
[
   {"label": "Space Mountain", "longitude": -117.917193, "latitude": 33.811379, color:"azure"},
   {"label": "Haunted Mansion", "longitude": -117.922675, "latitude": 33.811530, color:"magenta"}
]
```

The "color" property is optional and can be one of "azure", "blue", "cyan", "green", "magenta", "orange", 
"red":, "rose", "violet" or "yellow".

### minMapWidthInMeters:number
#### The minimum map width in meters

### optional:boolean
#### Specify whether a clip must be recorded before a default "submit"

### placeholder:string
#### The optional "placeholder" value

Defaults to "Show Map".


### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' parameter is an object with a property 'type' which either has a value of 'Map' or 'Marker' depending on where the user clicked. When the click was on the 'Map' then 'extra' also contains 'mapLatitude', 'mapLongitude', 'mapMouseX' and 'mapMouseY' which describe where the map was clicked. For type 'Marker' the extra properties are 'markerLatitude', 'markerLongitude', 'markerX', 'markerY', 'markerTitle' and 'markerKey' which describe which marker was clicked.












































<hr>

## MenuBar
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; MenuBar</span>

This widget is a classic "menu bar" which supports nested menu buttons. It can be used anywhere, but in general you would add it to the "Top Bar" of a Client so it would be visible on every Page. The structure of the MenuBar is defined by a tree of "MenuObjects". There are four types of MenuObjects:

* MenuItem - A simple menu button which shows a label and an optional icon.
* MenuSeparator - A horizontal line, useful for separating section within a MenuGroup
* MenuGroup - A group of MenuItems, MenuSeparators and MenuGroups
* MenuBarObject - The topmost MenuObject of the MenuBar - it can only appear at the "root" and can only contain MenuGroups

For example, suppose you want to describe a MenuBar which has two MenuGroups called "Operations" and "Views"

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Operations Menu](assets/img/client/Menu1.png "Operations Menu")

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Views Menu](assets/img/client/Menu2.png "Views Menu")


Usually you will build this tree of MenuObjects from the Property Sheet for the MenuBar. The MenuObject tree for the example above would look like this:

* MenuBarObject
    * MenuGroup ("Operations")
        * MenuItem ("New")
        * MenuItem ("Save")
        * MenuItem ("Close")
    * MenuGroup ("Views")
        * MenuItem ("Next")
        * MenuItem ("Previous")
        * MenuSeparator
        * MenuItem ("First")
        * MenuItem ("Last")


All MenuObjects have these properties:

* label:string - The label that should appear for a MenuItem or MenuGroup. This can also be a localization string such as "menu.close = Close"
* glyphIcon:string - A valid icon name such as "glyphicon-asterisk" or "fa-automobile". For a list of valid icons see the Client Builder property sheet.  The default is "null" which omits the icon.
* id:string - A unique identifier that can be used to identify a MenuObject. This is not necessary unless you are localizing the menu item text. In this case the actual text that appear in the menu item would vary depending on the current locale, and you can use the "id" instead (see "getMenuObjectById" below). 
* isHidden:boolean - If "true" this MenuObject (and anything it contains) will be temporarily hidden. Default is "false"
* isDisabled:boolean - If "true" this MenuObject will be temporarily disabled (and greyed out. Default is "false"




### getMenuObjectByLabel()
#### Get the MenuObject associated with the literal label

```js
getMenuObjectByLabel(label: string): MenuObject
```

* label:string - The label of the MenuObject you want to find. If you created localized labels for this menu then this string might be something like "menu.close = Close".

This method returns the corresponding MenuObject.


Here's an example of how this call might be used, assuming the sample MenuBar above:

```js
    var mb = client.getWidget("MenuBar1");
    var mo = mb.getMenuObjectByLabel("New");
    mo.isDisabled = true;
```



### getMenuObjectById()
#### Get the MenuObject associated with the supplied "id"

```js
getMenuObjectById(label: string): MenuObject
```

* id:string - The unique "id" of the MenuObject you want to find. This only works if you supplied unique "id" properties for all your MenuObjects. That's only necessary if you decided to give all your MenuObjects localized labels like "menu.close = Close" instead of just literal labels like "Close".

This method returns the corresponding MenuObject.

Here's an example of how this call might be used, assuming the sample MenuBar above:

```js

    var mb = client.getWidget("MenuBar1");
    var mo = mb.getMenuObjectById("NewCloseID");
    mo.isHidden = true;
```



### getMenuObjectByLocalizedLabel()
#### Get the MenuObject associated with current actual label

```js
getMenuObjectByLocalizedLabel(label: string): MenuObject
```

* label:string - The current actual label of the MenuObject you want to find. This function behaves just like "getMenuObjectByLabel" *unless* you supplied localized labels for your MenuObjects. In that case the "Close" MenuObject might have a localized label of "Cerca" instead of "Close" for the Spanish locale. In this situation you would probably want to use the "getMenuObjectById()" method instead of "getMenuObjectByLocalizedLabel".

This method returns the corresponding MenuObject.

Here's an example of how this call might be used, assuming the sample MenuBar above:

```js

    var mb = client.getWidget("MenuBar1");
    var mo = mb.getMenuObjectByLocalizedLabel("Close");
    mo.isDisabled = true;
```

In this case the returned variable "mo" might be null depending on th current locale.



### children:MenuObject[]
#### The array of child MenuObjects inside a MenuGroup or MenuBarObject

This property only applies to MenuGroups and MenuBarObjects. You may use it to add new MenuObjects to the MenuBar Widget at runtime (which will appear the next time the MenuBar is opened). For example -

```js
    //
    //  First get the "Operations" MenuGroup
    //
    var mb = client.getWidget("MenuBar1");
    var mg = mb.getMenuObjectById("OperationsMenuID");
    
    //
    //  Create a new child MenuItem
    //
    let mi = new MenuItem();
    mi.label = "Another Operation";
    mi.id = "AnotherOperationID";
    mg.children.push(mi);
```




### foregroundColor:string
#### The color of all the text appearing within the MenuBar

The text color is specified using the standard "#RRGGBB" format. (




### fontFace:string
#### The font face of all the text appearing within the MenuBar

The font face of the text is specified using normal CSS conventions.


### fontSize:number
#### The font size of all the text appearing within the MenuBar

The font size is specified in pixels.


### fontStyle:string
#### The style of all the text appearing within the MenuBar

The style of the text may be specified as one of "normal" or "italic".


### fontWeight:string
#### The weight of all the text appearing within the MenuBar

The weight of the text is specified as either "normal" or "bold".


### 'On Click' Event

This Widget supports an "On Click" Event Handler, which will be called when a MenuItem is selected from the MenuBar. (There is a single event handler for the entire MenuBar, so it is your responsibility to determine which MenuItem was clicked.) The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,menuItem)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the MenuBar Widget itself.

The "menuItem" parameter contains the MenuItem object for the item which the user clicked. You will need to examine the "label" or "id" properties to determine *which* MenuItem was clicked (and what should be done about it.) For example -


```js
function Client_Topbar_MenuBar1_onClick(client,page,menuItem)
{

    switch (menuItem.label)
    {
        case "New":
            console.log("New");
            break;
        case "Save":
            console.log("Save");
            break;
        case "Close":
            console.log("Close");
            break;
        case "Next":
            console.log("Next");
            break;
        case "Previous":
            console.log("Previous");
            break;
            
        ...
        ...
        ...
```

<hr>

## MenuButton
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; MenuButton</span>

This is a Button that has been styled to be suitable for use in the TopBar or SideBar of a Client. 



### foregroundColor:string
#### The color of the Button text

The text color is specified using the standard "#RRGGBB" format. 


### fontSize:number
#### The font size of the Button text

The font size is specified in pixels. 


### fontStyle:string
#### The style of the Button text

The style of the text may be specified as one of "normal", or "italic".

### glyphIcon:string
#### Display a Bootstrap or Font Awesome Icon to the left of the button text

You may enter a valid icon name such as "glyphicon-asterisk" or "fa-automobile". For a list of valid icons see the Client Builder property sheet.  The default is "null" which omits the icon. 

### rotationInDegrees:number
#### The angle in degrees by which the Widget should be rotated

A value of "0" (the default) indicates that the widget should not be rotated. "90" means "rotated 90 degrees clockwise" and "-90" means "rotated 90 degrees counter-clockwise."

### text:string
#### The text of the Button


### 'On Click' Event

This Widget supports an "On Click" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.








<hr>

## MultilineInput
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; MultilineInput</span>

This Widget is used to enter a multi-line String value.

### boundValue:string
The value of the text. Will be _undefined_ until the user has input a value.

### dataBinding:string
#### The name of a String DataObject variable

This Widget can be bound to a DataObject variable of type "String" (e.g. "client.data.myString"). Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.

### defaultValue:string
#### The default value for the Widget

If the widget is bound to a DataObject then the DataObject's value overrides this default.

### isReadOnly:boolean
#### Disables input into the field

### optional:boolean
#### Specify whether a value must be entered before a default "submit"

### placeholder:string
#### The optional "placeholder" value

Defaults to "".

### rows:number
#### The number of rows to be displayed.

Defaults to 5.

### wordwrap:boolean
#### Specify whether to wrap text displayed inside the widget.

Defaults to true.


### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.








<hr>

## NumberViewer
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; NumberViewer</span>

This Widget shows a simple "infographic" box that displays a single value from the most recent object from the Data Stream.

### backgroundColor:string
#### The background color 

The color of the background is specified using the standard "#RRGGBB" format. ("#ff9800" is the default.)

### borderThickness:number
#### The thickness of the border in pixels

### dataValue:number
#### The value displayed by the NumberViewer

Normally the NumberViewer gets the data it displays from a DataStream. In some situations (where you just want to compute some number in your code and display it directly) it may be more convenient to use this 'dataValue' property to get and set the number and bypass the need for a DataStream.

### dataStreamProperty:string
#### The property that contains the numeric value




### fontFace:string
#### The font face of the text

The font face of the text is specified using normal CSS conventions. 


### fontSize:number
#### The font size of the text

The font size is specified in pixels. 


### fontStyle:string
#### The style of the Widget's text

The style of the text is specified as either "normal" or "italic".


### fontWeight:string
#### The weight of the Widget's text

The weight of the text is specified as either "normal" or "bold". 





### foregroundColor:string
#### The foreground color 

The color of the foreground is specified using the standard "#RRGGBB" format. 

### format:string
#### An optional string to format the number

Some examples of valid format strings are found [here](http://numeraljs.com/#format).

### icon:string
#### An optional icon to display with the number

This icon string refers to one of the "Font Awesome" icons (such as "fa-circle"). 

A full list of possibilities can be found [here](http://fontawesome.io/icons/).

### units:string
#### An optional short string containing the "units" that should be displayed with the number



### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' parameter is an object with 'x' and 'y' properties giving the offset of the click.


### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.





<hr>

## PieChart
<span style="font-style:italic;">[Widget](#widget) &#x2192; [DataStreamWidget](#datastreamwidget) &#x2192; PieChart</span>

This Widget shows a simple "Pie Chart" by counting up the number of times a certain value appears in the indicated Data Stream object property.


### borderThickness:number
#### The thickness of the border in pixels


### chartConfig
#### Access to the [ZingChart Pie Chart](https://www.zingchart.com/docs/chart-types/pie) configuration
Reading from _chartConfig_ returns a JavaScript object which contains the current runtime Pie Chart configuration parameters. Writing to _chartConfig_ allows the user to programmatically change the appearance of the Pie Chart.

For example, the following reads the current configuration and changes the Pie Chart's type to a 3D Ring:
```js
	var chart = client.getWidget("PieChart1");
	var config = chart.chartConfig;
	config.type = "ring3d";
	chart.chartConfig = config;
```

Please refer to the ZingChart link above for configuration options available for the Pie Chart.

### chartSeries
#### Access to the [ZingChart Pie Chart](https://www.zingchart.com/docs/chart-types/pie) displayed data
Reading from _chartSeries_ returns a JavaScript object which contains the current runtime Pie Chart data. Writing to _chartSeries_ allows the user to programmatically change the data displayed by the Pie Chart.

For example, the following changes the Pie Chart to contain three values for different animal types:
```js
	var chart = client.getWidget("PieChart1");
	var series = [{"values":[50],"text":"Cats"},{"values":[20],"text":"Dogs"},{"values":[30],"text":"Birds"}];
	chart.chartSeries = series;
```
Please refer to the ZingChart link above for the format of series data required for the Pie Chart.


### chartType:string
#### The type of Pie Chart displayed

This property will controls the type of Pie Chart to be displayed; it must be one of "pie", "pie3d", "ring" or "ring3d". 
("pie" is the default".)



### currentValues:any
#### A hash table containing the current contents of the PieChart data (Read only)

For example, you might see a result like this:

```js
{
    "Cat": 12,
    "Dog": 3,
    "Bird": 6
}
```

which indicates that the PieChart currently has 3 segments, each with the associated counts.

### dataStreamProperty:string
#### The property that contains the instances to be counted

For example, the Data Stream property might be "typeOfPet" which would contains such values as "Dog", "Cat" and "Bird". The Pie Chart would display the number of times each of those values appear in the incoming data.


### explodePercentage:number
#### A measure of how "exploded" to make the chart

When set to zero (the default) the chart is displayed with all its segments touching. A positive integer causes the segments to be
"exploded" so they are separate.

### legendLookup:any
#### A hash table containing a lookup table for the PieChart Legend

For example, suppose your PieChart currently contained 3 data segments named "Cat", "Dog" and "Bird". By default those values will be used in the ieChart's legend at the bottom. You could specify a "legendLookup" hash table like this to override any or all of the corresponding legend values displayed:

```js
{
    "Cat": "Meow",
    "Dog": "Woof",
    "Bird": "Tweet"
}
```


### showLegend:boolean
#### Indicates whether to display a legend with the Pie Chart


### title:string
#### Title superimposed on the widget

This property will superimpose a title on the Widget; the title is null by default.


### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' parameter contains the value associated with the segment that was clicked on.

### 'On Data Consumed' Event

This event is fired when data arrives from the bound DataStream and before it has been displayed. This gives you an opportunity to examine and modify the incoming data, or even ignore it altogether.


```
Client_<page name>_<widget name>_onDataConsumed(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the incoming data; these properties are defined:

* dataObject: The incoming data object from the [DataStream](#datastream). You may modify the contents of this object to affect what the widget will display.
* ignore: A boolean value which is initially set to "false". If your code changes this to "true" the object will not be delivered to the widget for display.


<hr>

## RadioButtons
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; RadioButtons</span>

This Widget is used to enter a value as a standard set of "Radio Buttons" where only one buttons may be selected at a time.

### boundValue:any
The value of the radio buttons. Will be _undefined_ until the user has selected a value.

### dataBinding:string
#### The name of a String, Integer or Real DataObject variable

This Widget can be bound to a DataObject variable of type "String", "Integer" or "Real" (e.g. "client.data.myInteger"). Changes to the DataObject variable will be reflected in the Widget, and changes to the Widget will be used to update the DataObject variable.


### enumeratedList:any[]
#### The RadioButton list definition

RadioButtons present the user with a list of buttons, only one of which may be selected at a time. Each choice consists of a "label" (the text the user sees) and a "value" (the actual value that is used by the dataBinding). The array must be formed like this:

```js
var enumList = [
    {value:1, label:"One"},
    {value:2, label:"Two"},
    {value:3, label:"Three"}
];
```

In this example the user would see a set of RadioButtons with the labels "One", "Two" and "Three". If the user selected "Two" the bound DataObject variable would be set to the number 2.


### isHorizontal:boolean
#### Controls the layout direction of the Radio Buttons

If "true" the radio buttons will be laid out left-to-right rather than top-to-bottom. Defaults to "false".

### isReadOnly:boolean
#### Disables input into the field

### 'On Change' Event

This Widget supports an "On Change" Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains no useful information in this case.





<hr>

## VideoRecorder
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; VideoRecorder</span>

This Widget is used to record a short video clip. The clip may be uploaded into a Document object on the server.


### clearUpload()
#### Reset the recorder to its initial state

```js
clearUpload():void
```

After a clip has been recorded you can call this method to reset it to "empty".

### documentName:string
#### The name of the document to which the clip was uploaded

This property is readonly - it will be null until after a clip has been recorded and uploaded at which time it will
contain the name of the Document where it was saved.

### documentGroupName:string
#### The name of the Group to which the uploaded Document should be assigned

When this Widget creates and uploads a Document is will be assigned to the indicated [Group](resourceguide.md#groups). This is useful for controlling which users will have access to the Document.


### maxDurationInSeconds:number
#### The maximum number of seconds which may be recorded

In order to place a limit of the amount of storage used in your mobile device this setting places a limit on how many
seconds of video you may record. (Default - 10 seconds).

### maxSizeInK:number
#### The maximum amount of storage that may be recorded

In order to place a limit of the amount of storage used in your mobile device this setting places a limit on the
 maximum size of the clip which may be recorded. (Default - 1000K).


### optional:boolean
#### Specify whether a clip must be recorded before a default "submit"

### placeholder:string
#### The optional "placeholder" value

Defaults to "Start Video Recording".


### 'On Change' Event

This Widget supports an "On Change" Event Handler which fires after the user has successfully recorded a video. 
The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onChange(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains null.


<hr>




## ScrolledLayout
<span style="font-style:italic;">[Widget](#widget) &#x2192; [WidgetContainer](#widgetcontainer) &#x2192; ScrolledLayout</span>

This is a "container" widget that provides scrollbars for its contents. The ScrolledLayout will only allow a single child.


### allowHorizontalScrolling:Boolean
#### Allow the container to be scrolled horizontally
When "true" (the default) this container will automatically show a horizontal scrollbar when its child is too wide to be completely visible.

### allowVerticalScrolling:Boolean
#### Allow the container to be scrolled vertically
When "true" (the default) this container will automatically show a vertical scrollbar when its child is too tall to be completely visible.

### closeNestedPage()
#### Close the Page that is currently nested within the ScrolledLayout

```js
closeNestedPage(): void
```

This function is similar to [client.closePopup()](#closepopup) except that the currently nested Page will close and be removed from the ScrolledLayout.

This function can throw an exception in some situations, such as if there is not currently a Page nested within the ScrolledLayout.

### openNestedPage()
#### Open a Page nested within the ScrolledLayout

```js
openNestedPage(pageName: string): Page
```

* pageName:string - The name of the Page to be opened within the ScrolledLayout. The Page may be in any layout mode (Browser, Single, or Mobile)

This method returns the Page object for the nested Page.

This function is similar to [client.popupPage()](#popuppage) except that instead of popping it up inside a modal dialog it will be "opened" inside the ScrolledLayout.

This function can throw an exception in some situations, such as if there is already a Page nested within the ScrolledLayout.

The popup will be visible until the Page "closed" in one of several ways. For example, the nested Page can call client.returnToCallingPage() (as a normal popup would) or someone can call [closeNestedPage()](#closenestedpage) on the ScrolledLayout.

Here's an example of how this call might be used, assuming that "openNestedPage" is the name of a Page.

```js

   var myScrolledLayout = client.getWidget("myScrolledLayout");
   var theNestedPage = myScrolledLayout.openNestedPage("openNestedPage");

```

<hr>







## SectionLabel
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; SectionLabel</span>

_This Widget has been deprecated. Please use the [StaticText](#statictext) Widget instead._

This is a special kind of [ControlWidget](#controlwidget) which contains no active Widget but just the "Label" portion. It is intended for use inside a [VerticalLayout](#verticallayout) with other ControlWidgets. In other cases it is more appropriate to use the [StaticText](#statictext) Widget.

It differs from [Label](#label) in that it has a slightly different appearance making it suitable for labeling an entire "section" in the [VerticalLayout](#verticallayout) rather than a single item.


<hr>





## Signature
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; Signature</span>

This Widget allows a user to input a "signature" by drawing into the widget using the mouse or finger. The image is rendered as a PNG which can be uploaded into a Vantiq Document using the standard "upload" mechanism.


### backgroundColor:string
#### The background color of the Signature drawing area

The background color is specified using the standard "#RRGGBB" format. ("#ffffff" is the default.)


### borderThickness:number
#### The thickness of the border in pixels

### dataURL:string (readonly)
#### The current contents of the widget rendered as a "data URL"

For an explanation of "data URLS" you can read [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs).


### documentName:string
#### The name of the document to which the image was uploaded

This property is readonly - it will be null until after a image has been recorded and uploaded at which time it will
contain the name of the Document where it was saved.

### documentGroupName:string
#### The name of the Group to which the uploaded Document should be assigned

When this Widget creates and uploads a Document is will be assigned to the indicated [Group](resourceguide.md#groups). This is useful for controlling which users will have access to the Document.


### foregroundColor:string
#### The 'pen' color used in the Signature drawing area

The foreground color is specified using the standard "#RRGGBB" format. ("#000000" is the default.)


### isReadOnly:boolean
#### Disables input into the field

### optional:boolean
#### Specify whether a clip must be recorded before a default "submit"




<hr>















## StaticHtml
<span style="font-style:italic;">[Widget](#widget) &#x2192; StaticHtml</span>

This Widget displays a fixed fragment of HTML. It would be useful to display a piece of "rich text" or to embed some kind of HTML media viewer.

Since you can add whatever HTML you like StaticHtml can also be used as the basis for your own custom widgets. As a convenience for this feature you can also associate StaticHtml with a DataStream and then define an "On Data Arrived" event which will be called whenever new data appears. Widgets which are bound to DataStreams are generally subclasses of the [DataStreamWidget](#datastreamwidget) class; StaticHtml is an exception.


Here are some examples:


```html
<iframe src="//www.youtube.com/embed/Ki_Af_o9Q9s" width="100%" height="100%" frameborder="0" allowfullscreen="allowfullscreen"></iframe>
```

```html
The quick <span style="color: #993300;">brown</span> <strong><em>fox</em></strong> jumped over the lazy <strong>dog</strong>.
```

### borderThickness:number
#### The thickness of the border in pixels

### dataStreamUUID:string
#### The UUID of the DataStream to which the Widget is associated

If you have a DataStream object you can get its UUID using "theDataStreamObject.uuid";


### html:string
#### The HTML to be be displayed


### horizontalScrollPolicy:number
#### Controls the management of horizontal scrollbars on the StaticHtml Widget

The value must be one of StaticHtml.ScrollPolicyNone, StaticHtml.ScrollPolicyAlways or StaticHtml.ScrollPolicyAuto.

### verticalScrollPolicy:number
#### Controls the management of horizontal scrollbars on the StaticHtml Widget

The value must be one of StaticHtml.ScrollPolicyNone, StaticHtml.ScrollPolicyAlways or StaticHtml.ScrollPolicyAuto.


### 'On Data Arrived' Event

This Widget supports an "On Data Arrived" Event Handler. This handler will be called whenever new data arrives on the widget's associated DataStream. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onDataArrived(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains the newly arrived data, which will be either an Object or and array of Objects depending on the characteristics of the DataStream. 

It is your responsibility to examine this data and extract (and act on) whatever information is appropriate to your custom HTML.

If you need to reference the DataStream object itself you can do it like this:

```js
var theDataStream = client.getDataStreamByUUID(this.dataStreamUUID);
```




<hr>

## StaticIcon
<span style="font-style:italic;">[Widget](#widget) &#x2192; StaticIcon</span>

This Widget displays a single "font glyph" chosen the builtin set of "font-awesome" and "bootstrap" icons.


### backgroundColor:string
#### The color of the StaticIcon background

The background color is specified using the standard "#RRGGBB" format. ("null" is the default, which means the background is transparent.)


### fontSize:number
#### The font size of the glyph

The font size is specified in pixels. ("20" is the default.)

### foregroundColor:string
#### The foreground color 

The color of the glyph is specified using the standard "#RRGGBB" format. 

### glyphIcon:string
#### The name of the glyph to be displayed

These names follow a standard pattern; "font-awesome" icons look like "fa-asterisk", and "bootstrap" icons look like "glyphicon-apple".


### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' is an object with 'x' and 'y' properties giving the offset of the click.)





<hr>

## StaticImage
<span style="font-style:italic;">[Widget](#widget) &#x2192; StaticImage</span>

This Widget displays an loaded from a URL.

The [StaticImage](#staticimage) and [ImageViewer](#imageviewer) widgets are very similar widgets. They differ in that the StaticImage is just an image, analogous to the StaticText widget. The ImageViewer supports the optional "label" property and when the image is clicked at runtime it will be displayed in a separate window at full resolution.

[StaticImages](#staticimage) can be in 4 different states:

* Empty - No URL specified
* Bad - A URL was specified but it could not be loaded
* Loading - A URL was specified but it has not completed loaded yet
* Loaded - A URL was specified and has completed loading (so the natural size of the image is known and the image is displayed)

When editing in the Client Builder the first three states will show as a black, red or grey rectangles respectively. (This makes it easier for the developer to see what state the StaticImage is in while editing.)

When running in a Client the first 3 states will not be obvious to the user; instead of a solid color they will be transparent (clear). When the [StaticImage](#staticimage) is "NaturalSize" it will start as 1x1 and then expand to the proper size once the image is loaded. When the [StaticImage](#staticimage) is sized Explicitly they will start as clear rectangles of the specified size and then the image will appear within the space without causing the [StaticImage](#staticimage) to resize.


### preserveAspectRatio:boolean
#### Indicates whether the image should stretch when not shown at its normal size

If this property is "true" (the default) the image will be scaled to preserve its natural aspect ratio if shown at a size that doesn't match. If 'false' then the image may appear distorted or stretched when forced to appear at a size which is incompatible with the image's height-to-width ratio.

### rotationInDegrees:number
#### The angle in degrees by which the Widget should be rotated

A value of "0" (the default) indicates that the widget should not be rotated. "90" means "rotated 90 degrees clockwise" and "-90" means "rotated 90 degrees counter-clockwise." 

When 'rotationInDegrees' is set to something other than 0 only NaturalSize is allowed in both dimensions.



### url:string
#### The URL of the image to be displayed

There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).


### 'On Click' Event

This Widget supports an 'On Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onClick(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The 'extra' is an object with 'x' and 'y' properties giving the offset of the click.)


<hr>




## StaticMarkdown
<span style="font-style:italic;">[Widget](#widget) &#x2192; StaticMarkdown</span>

This Widget formats and displays a fragment of "Markdown" markup text. 

Normally you would simply use the "markdown" property to set a fixed piece of Markdown text to be displayed at runtime.  You can also associate a StaticMarkdown Widget with a DataStream and then define an "On Data Arrived" event which will be called whenever new data appears. Widgets which are bound to DataStreams are generally subclasses of the [DataStreamWidget](#datastreamwidget) class; StaticMarkdown is an exception.




### borderThickness:number
#### The thickness of the border in pixels

### dataStreamUUID:string
#### The UUID of the DataStream to which the Widget is associated

If you have a DataStream object you can get its UUID using "theDataStreamObject.uuid";


### markdown:string
#### The Markdown text to be formatted and displayed


### horizontalScrollPolicy:number
#### Controls the management of horizontal scrollbars on the StaticMarkdown Widget

The value must be one of StaticMarkdown.ScrollPolicyNone, StaticMarkdown.ScrollPolicyAlways or StaticMarkdown.ScrollPolicyAuto.

### verticalScrollPolicy:number
#### Controls the management of horizontal scrollbars on the StaticMarkdown Widget

The value must be one of StaticMarkdown.ScrollPolicyNone, StaticMarkdown.ScrollPolicyAlways or StaticMarkdown.ScrollPolicyAuto.


### 'On Data Arrived' Event

This Widget supports an "On Data Arrived" Event Handler. This handler will be called whenever new data arrives on the widget's associated DataStream. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onDataArrived(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains the newly arrived data, which will be either an Object or and array of Objects depending on the characteristics of the DataStream.

It is your responsibility to examine this data and extract (and act on) whatever information is appropriate to your custom markdown.

If you need to reference the DataStream object itself you can do it like this:

```js
var theDataStream = client.getDataStreamByUUID(this.dataStreamUUID);
```



<hr>


## StaticText
<span style="font-style:italic;">[Widget](#widget) &#x2192; StaticText</span>

This Widget displays a single list of static text.


The [Label](#label) and [StaticText](#statictext) widgets are virtually identical; the Label still exists for reasons of backwards compatibility and the StaticText widget is preferred going forward.


### foregroundColor:string
#### The color of the  text

The color of the text is specified using the standard "#RRGGBB" format. 


### fontFamily:string
#### The font family of the text

The font family of the text is specified using normal CSS conventions. 


### fontSize:number
#### The font size of the text

The font size is specified in pixels. 


### fontStyle:string
#### The style of the Widget's label text

The style of the text is specified as either "normal" or "italic". 


### fontWeight:string
#### The weight of the Widget's label text

The weight of the text is specified as either "normal" or "bold". 


### isMultiline:Boolean
#### Controls whether more than one line may be displayed
By default the StaticText widget is used to display a single line of text with no line breaks. This property can be used to make the StaticText widget respect "newline" characters ('\n') and display multi-line text.

### rotationInDegrees:number
#### The angle in degrees by which the Widget should be rotated

A value of "0" (the default) indicates that the widget should not be rotated. "90" means "rotated 90 degrees clockwise" and "-90" means "rotated 90 degrees counter-clockwise."


### text:string
#### The text to display





<hr>

## TabbedLayout
<span style="font-style:italic;">[Widget](#widget) &#x2192; [WidgetContainer](#widgetcontainer) &#x2192; TabbedLayout</span>

This is a "container" widget that offer a classic multi-page "tabbed" functionality. The Tabs (and their labels) are settable from the property sheet; each "page" contains a single FixedLayout container where you may place children. 

If you add only single "container" widgets to one of the pages and set both its heightPolicy and widthPolicy to "Size to Parent" then
 the container will be moved and resized so as to fill the entire page. This can be useful if the size of the TabbedLayout will change dynamically and you want the contents of a page to adjust as well.

### activePageIndex:number
#### The index of the currently active Tab page

This property may be used to get or set the index of the currently active tab page (where the leftmost tab is considered page "0").


### fontFamily:string
#### The font family of the tab label text

The font family of the text is specified using normal CSS conventions. ("Arial,Verdana" is the default.)


### fontSize:number
#### The font size of the tab label text

The font size is specified in pixels. ("20" is the default.)


### fontStyle:string
#### The style of the tab label text

The style of the text is specified as either "normal" or "italic". ("normal" is the default.)

### getPageVisibility()
#### Return whether one of the TabbedLayout's pages is shown or hidden

```js
getPageVisibility(index:number):boolean
```

* index: number - The index of the "page" whose visibility you want to access (the indicies start at zero)

Normally all of the "pages" which are defined in a TabbedLayout will be visible at runtime. This method can be used to find out whether a page is currently visible (true) or hidden (false).


### hideTabsAtRuntime:boolean
#### Cause the Tabs to be hidden at runtime

When set to true this causes the tabs defined by the TabbedLayout to be hidden (defaults to "false"). This means it is the Client's responsibilty to provide some alternate programmatic means (using setPageVisibility()) to switch tabs at runtime.

### setPageVisibility()
#### Set one of the TabbedLayout's pages to be shown or hidden

```js
setPageVisibility(index:number,isVisible:boolean):void
```

* index: number - The index of the "page" whose visibility you want to set (the indicies start at zero)
* isVisible: boolean - Set the indicated page to be visible (true) or hidden (false)

Normally all of the "pages" which are defined in a TabbedLayout will be visible at runtime. This method can be used to hide or show a page at runtime. Note that in the property sheet for a TabbedLayout you are allowed to define these pages and their properties (such as name and icon). In that dialog you may also change the default runtime visibility for each page, and then use this method to change its state programmatically.




### 'On Page Changed' Event

This Widget supports an "On Page Changed" Event Handler which fires after the user changes the currently active tab page. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onPageChanged(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself.

The "extra" parameter contains an object with information describing the change; these properties are defined:

* oldTabIndex: The index of the tab which used to be active (starting with "0")
* oldTabLabel: The label of the tab which used to be active (the raw value before localization).
* oldTabLabelLocalized: The label of the tab which used to be active (the actual displayed value after localization)
* newTabIndex: The index of the tab is now active (starting with "0")
* newTabLabel: The label of the tab is now active (the raw value before localization).
* newTabLabelLocalized: The label of the tab which is now active (the actual displayed value after localization).


<hr>

## Tree
<span style="font-style:italic;">[Widget](#widget) &#x2192; [ControlWidget](#controlwidget) &#x2192; Tree</span>

This Widget is used to display a tree of nested items. All of the nodes within the tree are described by a nested hierarchy of TreeWidgetObjects described [TreeWidgetObject](#treewidgetobject).





### getTreeObjectByLabel(label:string):TreeWidgetObject

Return the TreeWidgetObject whose "label" property matches the supplied parameter.

* label: string - The label to search for

This method can return null if the label is not found. If more that one item has the same label if returns the first one found.

### noContentsMessage:string
By default this property is "null" and the Tree will display the text "No Contents". You may set this property to a different value to override that.



### root:TreeWidgetObject
The TreeWidgetObject representing the topmost item in the TreeWidgetObject hierarchy.

### selectableNodes:boolean
Determine whether nodes in the tree should be selectable (The default is "true").

### selectedTreeWidgetObject:TreeWidgetObject
This property may to be used to set or get the currently selected TreeWidgetObject.


### showRoot:boolean
Determine whether the root object is actually shown in the Tree. (The default is "false").






### 'On Node Clicked' Event

This Widget supports an 'On Node Click' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onNodeClicked(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself. 'extra.node' contains the TreeWidgetObject which was clicked.

### 'On Node Expanded Changed' Event

This Widget supports an 'On Node Expanded' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onNodeExpandedChanged(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself. 'extra.node' contains the TreeWidgetObject which changed.


### 'On Node Menu Clicked' Event

This Widget supports an 'On Node Menu Clicked' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onNodeMenuClicked(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself. 'extra.node' is the node whose menu was used, 'extra.key' is the key of the menu item and 'extra.menuItem' is the MenuItem itself.


### 'On Node Selection Changed' Event

This Widget supports an 'On Node Selection Changed' Event Handler. The code will be wrapped in a function with a signature of the form:

```
Client_<page name>_<widget name>_onNodeSelectionChanged(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Widget itself. 'extra.node' contains the TreeWidgetObject which changed.

<hr>

## VerticalLayout
<span style="font-style:italic;">[Widget](#widget) &#x2192; [WidgetContainer](#widgetcontainer) &#x2192; VerticalLayout</span>

This is a "container" widget that arranges its visible children into a vertical "stack". The children are arranged from top-to-bottom in the order given by the "children" property. (The index of a child within its parent's "children" array determines its position in the stack.)


### allowAllAccordionChildrenOpen:Boolean
#### Change the behavior of AccordionLayouts inside the VerticalLayout
You usually place a number of AccordionLayouts inside a VerticalLayout. By default only one AccordionLayout is allowed to be 'open' (expanded) at a time. (Opening one AccordionLayout causes any open one to be closed.) By setting allowAllAccordionChildrenOpen to 'true' you can change this behavior so that any number of the AccordionLayouts may be open at the same time (defaults to 'false').

This property is meaningless unless the VerticalLayout contains more than one AccordionLayout.

<hr>

## Widget
This is the superclass of all Widgets which can be displayed in a Client. It is a non-leaf class and cannot be instantiated.


### addEventHandler()
#### Add an event handler to a Widget


```js
addEventHandler(eventName:string, callback:Function)
```

* eventName: string - The name of the event; this will be something like "onClick" or "onChange"
* callback: Function - A Javascript function that accepts the standard 3 parameters (client, page, extra)


This is useful if you are dynamically adding Widgets to a Page and you need to add an event handler as well. 


```js
    //
    //  Look up an existing container widget to use as a "parent"
    //
    var vc1 = client.getWidget("vc1");

    //
    //  Create a Button and give it a name
    //
    var btn = new Button();
    btn.name = "DynamicButton1";

    //
    //  Add an event handler
    //
    btn.addEventHandler("onClick",function(client,page,extra)
    {
        client.infoDialog("Clicked!","Success");
    });

    //
    //  Add the button to a container so it will become visible and active on the Page
    //
    vc1.addChild(btn);
```


### backgroundImageUrl:string
#### The URL of an image to show in the Widget background

"backgroundImageUrl" is null by default.

There is an explanation of Document URLs found [here](cbuser.md#accessing-documents).

### backgroundImageRepeat:string
#### Set the CSS "background-repeat" property for the background image

This must be set to one of the valid values for
the CSS "background-repeat" property (e.g. "no-repeat", "repeat", "space", etc.) The default is "no-repeat".

This property is ignored unless backgroundImageUrl has been set. 



### backgroundImagePosition:string
#### Set the CSS "background-position" property for the background image

This must be set to one of the valid values for
the CSS "background-position" property (e.g. "center", "left top" etc.) The default is "center".

This property is ignored unless backgroundImageUrl has been set. 



### backgroundImageSize:string
#### Set the CSS "background-size" property for the background image

This must be set to one of the valid values for
the CSS "background-size" property (e.g. "auto", "cover", "contain" etc.) The default is "auto".

This property is ignored unless backgroundImageUrl has been set. 




### bringToFront()
#### Bring a widget "in front" of its sibling Widgets

```js
bringToFront()
```


This method is only useful for Widgets which are parented to a FixedLayout container. It changes a Widget's position in the "stacking order" of its parent's children, making it the "topmost" in the stack so it will not be obscured by any siblings.



### componentContainer:WidgetContainer
#### The topmost "container" Widget of a Component

For any given Widget within a Client Component this value will contain the "topmost" WidgetContainer of the Component. This
value is read-only and be null for Widgets which are not within a Component.

### configuration:Object
#### Configuration Properties for a Component

This property is always null unless the Widget is part of a Component; in that case this is an object which contains the configuration properties defined by the Component author. For a complete explanation see the [Client Component User's Guide](ccug.md).


For example, if your Client contains a Component named "MyComponent" which has a configuration property called "temperature" you can refer to it like this:

```js
    var cmp = client.getWidget("MyComponent");
    console.log(cmp.configuration.temperature);
```

If the Component has a Call-in Function called "add" you can invoke it the same way:


```js
    var cmp = client.getWidget("MyComponent");
    var result = cmp.configuration.add(10,20);
```

### CSSClass:string
#### The CSS class for this Widget
By default widgets have a class assigned to them which is not used by the runtime system but that you can define any way you wish using a "CSS Custom Asset". (Each type of Widget has a different value assigned to CSSClass by default; for example Buttons use "vantiqButton". Look at the CSS Class property in the "Style" section of the Client Builder property sheet to see the default for each type of Widget.) 

You can use the CSSClass property to override this class setting at runtime,

### h:number
#### The height of a Widget in pixels

Note that setting the height of a Widget will be ignored unless it has a height Size Policy of "Explicit".

### heightPolicy:number
#### The 'height' Size Policy of the Widget

Refer to the documentation [here](layout.md#size-policies) for a discussion of Widget Size Policies and how they are used. This must be one of the following constants:


* Widget.SizePolicy_NaturalSize
* Widget.SizePolicy_Explicit
* Widget.SizePolicy_SizeToParent






### horzGravity:number
#### The 'horizontal gravity' of the Widget

Refer to the documentation [here](layout.md#gravity) for a discussion of Gravity and how it is used. This must be one of the following constants:

* Widget.Gravity_Left
* Widget.Gravity_Right
* Widget.Gravity_Center

Note that whether this property is meaningful depends on the Widget's parent [WidgetContainer](#widgetcontainer).


### horzWeight:number
#### The 'horizontal weight' of the Widget

Refer to the documentation [here](layout.md#weight) for a discussion of Weight and how it is used.

Note that whether this property is meaningful depends on the Widget's parent [WidgetContainer](#widgetcontainer) and the horizontal weights of the parent's other children.


### isContainer:boolean
#### Is this a container widget? (readonly)

Returns "true" if this Widget is a subclass of [WidgetContainer](#widgetcontainer).

### isVisible:boolean
#### Is this widget visible? 

By default all Widgets are visible. At runtime you can hide a Widget by setting the value of its "isVisible" property to "true". When a Widget is invisible it is ignored by its parent when doing layout.


### moveAbove()
#### Bring a widget "in front" of the indicated sibling Widget

```js
moveAbove(sibling:Widget)
```

* sibling:Widget - A sibling Widget (i.e. a Widget that shares the same parent container).

This method is only useful for Widgets which are parented to a FixedLayout container. It changes a Widget's position in the "stacking order" of its parent's children, making it immediately above the indicated sibling Widget in the stacking order.


### moveBelow()
#### Send a widget "behind" the indicated sibling Widget

```js
moveBelow(sibling:Widget)
```

* sibling:Widget - A sibling Widget (i.e. a Widget that shares the same parent container).

This method is only useful for Widgets which are parented to a FixedLayout container. It changes a Widget's position in the "stacking order" of its parent's children, making it immediately below the indicated sibling Widget in the stacking order.


### name:string
#### The name of the Widget.

All Widgets must have a name which uniquely identifies it. A Widget can be found using the [getWidget()](#getwidget) method on Client.


### parent:WidgetContainer
#### The parent of the Widget (readonly)

All Widgets (except the topmost) have a parent of class [WidgetContainer](#widgetcontainer).


### sendToBack()
#### Send a widget behind all its sibling Widgets

```js
sendToBack()
```

This method is only useful for Widgets which are parented to a FixedLayout container. It changes a Widget's position in the "stacking order" of its parent's children, making it the "bottommost" in the stack so it will be obscured by any other sibling.





### tooltip:string
#### A message that appears when a cursor is positioned over the Widget.

Tooltips don't work in mobile Clients since there is no "hover" on mobile device.



### vertGravity:number
#### The 'vertical gravity' of the Widget

Refer to the documentation [here](layout.md#gravity) for a discussion of Gravity and how it is used. This must be one of the following constants:

* Widget.Gravity_Top
* Widget.Gravity_Bottom
* Widget.Gravity_Center

Note that whether this property is meaningful depends on the Widget's parent [WidgetContainer](#widgetcontainer).


### vertWeight:number
#### The 'vertical weight' of the Widget

Refer to the documentation [here](layout.md#weight) for a discussion of Weight and how it is used. 

Note that whether this property is meaningful depends on the Widget's parent [WidgetContainer](#widgetcontainer) and the vertical weights of the parent's other children.




### w:number
#### The width of a Widget in pixels


Note that setting the width of a Widget will be ignored unless it has a width Size Policy of "Explicit".


### widthPolicy:number
#### The 'width' Size Policy of the Widget

Refer to the documentation [here](layout.md#size-policies) for a discussion of Widget Size Policies and how they are used. This must be one of the following constants:


* Widget.SizePolicy_NaturalSize
* Widget.SizePolicy_Explicit
* Widget.SizePolicy_SizeToParent


### x:number
#### The X coordinate of a Widget relative to its container



### xc:number
#### The X coordinate of the centerpoint of a Widget relative to its container

### yc:number
#### The Y coordinate of the centerpoint of a Widget relative to its container



### xSync:number
#### The X coordinate of a Widget relative to its container

This property is identical to "x" **except** that changing it will only update the value of the X coordinate in the Widget ("x") but will **not** actually update the position of the underlying DOM element. This is an advanced feature - it should only be used if your code caused the position of this Widget to be changed by some direct manipulation of the DOM; the xSync property would be used keep the actual Widget X coordinate in sync with the true position.

### ySync:number
#### The Y coordinate of a Widget relative to its container

This property is identical to "y" **except** that changing it will only update the value of the Y coordinate in the Widget ("y") but will **not** actually update the position of the underlying DOM element. This is an advanced feature - it should only be used if your code caused the position of this Widget to be changed by some direct manipulation of the DOM; the ySync property would be used keep the actual Widget Y coordinate in sync with the true position.

### y:number
#### The Y coordinate of a Widget relative to its container


### z:number
#### The "stacking order" position of this Widget


This property is only meaningful for Widgets which are parented to a FixedLayout container. It can be used to get or set the Widget's position in the stacking order. (The bottom Widget in the stacking order is position zero.)


### 'On Context Menu' Event
A Widget's 'On Context Menu' Event is fired whenever the user selects an item from the widget's optionally defined context menu.

The code will be wrapped in a function with a signature of the form:
```
Client_<page name>_<widget name>_onContextMenu(client,page,extra)
```

where "this" points to the Widget object, "client" points to the Client object, "page" points to the Page object and "extra" is an object containing the _key_ and _label_ properties of the selected menu item.

Whenever a user selects a Page's context menu item the **On Context Menu** function is executed and the handler make take any appropriate action based on the _key_ of the "extra" parameter.




### 'On Component Start' Event

This Event is **only** defined on a "Component" Widget, and is only available to the author of the Component (it is not visible to the consumer of the Component).

A Component instance may require initialization, analogous to the way a Page can use the "On Page Start" event to initialize the state of Page. After the "On Page Start" for a Page is executed the system will run all the "On Component Start" handlers for any Components on the Page. A common use for this event would be to do any last-minute initialization of the Component instances configuration object.

The code will be wrapped in a function with a signature of the form:

```
Client_Start_<widget name>_onComponentStart(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Component Widget itself.

The "extra" parameter contains no useful information in this case.


### 'On Component End' Event

This Event is **only** defined on a "Component" Widget, and is only available to the author of the Component (it is not visible to the consumer of the Component).

A Component instance may require cleanup, analogous to the way a Page can use the "On Page End" event to finalize the state of Page. Before the "On Page End" handler for a Page is executed the system will run all the "On Component End" handlers for any Components on the Page.

The code will be wrapped in a function with a signature of the form:

```
Client_Start_<widget name>_onComponentEnd(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Component Widget itself.

The "extra" parameter contains no useful information in this case.



### 'On Component Assets Loaded' Event

This Event is **only** defined on a "Component" Widget, and is only available to the author of the Component (it is not visible to the consumer of the Component).

The Client may use the "On Assets Loaded" handler to defer certain initialization until all the JavaScript and CSS assets have completed loading. Some Components my require special processing as well, so after the "On Assets Loaded" handler for a Client is executed the system will run all the "On Component Assets Loaded" handlers for all the Components within the Client.


The code will be wrapped in a function with a signature of the form:

```
Client_Start_<widget name>_onComponentAssetsLoaded(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Component Widget itself.

The "extra" parameter contains no useful information in this case.


### 'On Component Network Status Changed' Event


This Event is **only** defined on a "Component" Widget, and is only available to the author of the Component (it is not visible to the consumer of the Component).

The Client may use the "On Network Status Changed" handler to take action on a mobile device when the status of the network changes. Some Components my require special processing as well, so after the "On Network Status Changed" handler for a Client is executed the system will run all the "On Component Network Status Changed" handlers for all the Components within the Client.

The code will be wrapped in a function with a signature of the form:

```
Client_Start_<widget name>_onComponentNetworkStatusChanged(client,page,extra)
```

where "client" points to the Client object, "page" points to the current Page and "this" points to the Component Widget itself.

The 'extra' parameter is an object with a single property, 'isNetworkActive', which is 0 when the device is offline and 1 when the device is online.

For a discussion of running Clients in "offline mode"  see [here](cbuser.md#offline-operation).


<hr>

## WidgetContainer
<span style="font-style:italic;">[Widget](#widget) &#x2192; WidgetContainer</span>

This is the superclass of all "container" Widgets. It is a non-leaf class and cannot be instantiated.

### addChild()
#### Add a child Widget to a WidgetContainer


```js
addChild(child: Widget, index1: number=-1, index2: number= -2)
```

* child: Widget - The child Widget to be added to this container.
* index1: number - Indicates the index at which the child should be inserted. The default is any negative value such as -1, which means the child should be added "at the end". (This parameter has a slightly different meaning for  [GridLayout](#gridlayout) WidgetContainers; see below.
* index2: number - Only used by [GridLayout](#gridlayout) WidgetContainers at present; see below.


[GridLayout](#gridlayout) WidgetContainers arrange their children in a "grid" where each cell is identified by a "row" and "column". In this case "index1" and "index2" are both required and mean the "row" and "column" of the cell where the child is to be inserted. The cell must be unoccupied or addChild() will throw an exception.


### addComponentChild()
#### Instantiate a Client Component and add it to a WidgetContainer


```js
addComponentChild(componentName:string,widgetName:string,callbackFunction:Function=null,index1: number = -1, index2: number = -1)
```

This method is similar to addChild, except that you do not supply a Widget but the name of a type of Client Component to be instantiated.

* componentName: String - The name of an existing Client Component to be instantiated.
* widgetName:string - The unique name to be given to the Client Component instance
* callbackFunction:Function - a function that will be called after the Client Component is ready for use. You will be passed the Client Component object as a single parameter.
* index1: number - Indicates the index at which the child should be inserted. The default is any negative value such as -1, which means the child should be added "at the end". (This parameter has a slightly different meaning for  [GridLayout](#gridlayout) WidgetContainers; see below.
* index2: number - Only used by [GridLayout](#gridlayout) WidgetContainers at present; see below.


[GridLayout](#gridlayout) WidgetContainers arrange their children in a "grid" where each cell is identified by a "row" and "column". In this case "index1" and "index2" are both required and mean the "row" and "column" of the cell where the child is to be inserted. The cell must be unoccupied or addComponentChild() will throw an exception.

An example is shown below; it assumes you have a VerticalLayout widget called "TheParentWidget" to which we will add a Client Component instance of type "MyComponent". After creating an instance of the Client Component it will be assigned the name "TheComponentName1" (which must be unique).

Because this process is actually asynchronous you can supply a callback function which will be called once the Client Component is ready to use. At that time you can set configuration parameters.
 if required.

```js
var parent = client.getWidget("TheParentWidget");
parent.addComponentChild("MyComponent","TheComponentName1",function(cc)
    {
        //
        //  "cc" is the Client Component widget instance.
        //
        cc.configuration.TheBackGroundColor = "#ff0000";
    });
```

### children:Widget[]
#### The list of "child" Widgets (readonly)

This property contains an array containing all the children of the WidgetContainer.



### horzMargin:number
#### The margin in pixels provided to the left and right of each child

Refer to the documentation [here](layout.md#margins) for a discussion of margins and how they are used.

Note that whether this property is meaningful depends on the type of WidgetContainer and its layout strategy.



### innerMargin:number
#### The margin in pixels provided to the between each child

Refer to the documentation [here](layout.md#margins) for a discussion of margins and how they are used.

Note that whether this property is meaningful depends on the type of WidgetContainer and its layout strategy.









### removeChild()
#### Remove a child Widget to a WidgetContainer


```js
removeChild(child: Widget)
```

* child: Widget - The child Widget to be removed from this container. This throws an exception of "child" is not currently a child of this WidgetContainer.


### vertMargin:number
#### The margin in pixels provided to the top and bottom of each child

Refer to the documentation [here](layout.md#margins) for a discussion of margins and how they are used.

Note that whether this property is meaningful depends on the type of WidgetContainer and its layout strategy.
