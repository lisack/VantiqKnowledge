# Client Component Tutorial

## Objectives
Upon completion of this tutorial, a developer will be able to create and use Client Components, which are reusable collections of widgets.

## Tutorial Overview
This tutorial demonstrates how to author Client Components and how to use (or consume) those Components in Clients. A Client Component contains one or more widgets plus optional Data Streams and JavaScript code to provide reusable functionality in other Clients. For example, an author might build a Fahrenheit-to-Celsius conversion Client Component that has input and output display widgets plus a button to perform the conversion. These widgets are combined to form a single Client Component that is used in other Clients that need such conversion functionality.

To get the most from this tutorial, it is highly recommended to complete the short and no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

This tutorial assumes the developer has a working knowledge of the [Vantiq IDE](../../../..). It is recommended that a new developer completes the lessons in the [Introductory Tutorial](tutorial.md) and the [Client Builder Tutorial](client.md) before starting the lessons in this tutorial.

## 1: Creating a Client Component Project
Use the **Projects** button, select **New Project**, which displays the New Project Wizard. Either create a new Namespace (recommended) or add a new project to the current Namespace, select **Empty** as the Project type, and title the project "ProgressComponent":

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ClientProject](../assets/img/intro/EMProject.png "Create Client Project")

The next two lessons take place inside this Project.

## 2: Authoring the Progress Bar Component
This lesson creates a Client Component that implements a progress bar which can be reused in Clients. It uses a StaticHtml widget as a holder for the progress bar plus a little JavaScript code used to drive the progress bar. This lesson uses a simple open-source JavaScript progress bar as an example. However, the steps can easily be adapted to use other third-party JavaScript projects to create other Client Components.

#### a. Download the Progress Bar
Download the [ProgressBar.js](https://github.com/kimmobrunfeldt/progressbar.js) project. The only file necessary for the Client Component is _progressbar.min.js_.

#### b. Create the Client Component
To create a new Client Component, use the **Add** button, select **Client**, then use the **New Component** button to create the _ProgressComponent_ Component:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![CreateComponent](../assets/img/client/CreateComponent.png "Create Client Component")

#### c. Configure the StaticHtml Widget
Once the _ProgressComponent_ Client Component pane appears, drag and drop a StaticHtml widget from the **Add** palette onto the Client Builder canvas. The StaticHtml widget is found in the **Data Display** section and is labeled **HTML**:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![StaticHtmlWidget](../assets/img/client/StaticHtmlWidget.png "StaticHtml Widget")

Click on the newly added StaticHtml widget to display its property sheet:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![StaticHtmlProperties](../assets/img/client/StaticHtmlProperties.png "StaticHtml Properties")

In the **Specific** properties section, click the **Raw** checkbox of the **HTML** property, then click the **Click to Edit** link. In the _Edit Raw HTML_ dialog, replace the default text with the following:
```js
<div id="progressDiv"></div>
```
This _&lt;div&gt;_ is the HTML element that will contain the progress bar in the Client Component.

In the **Layout** properties section, set the following two property values:

* Height: 10
* Width: 150

These properties appropriately size the _&lt;div&gt;_ to display the progress bar.

#### d. Configure the Client Component Properties
Configuring the Client Component properties is where the power of Client Components is exposed. First, add the downloaded _progressbar.min.js_ file from Step (a) to the component. To do so, click the **Edit** tab of the Control Dock (on the left side of the Client Component pane), right-click the **Component** tree entry, then select **Edit Component Properties** to display the _Edit Properties_ dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ComponentProperties](../assets/img/client/ComponentProperties.png "Component Properties")

* In the **Basic** tab, click the **&lt;None&gt;** link under the **Custom Assets** section. Use the **Add an Asset** button in the **JavaScript Assets** section to upload the _progressbar.min.js_ file. Once uploaded, the component uses that code to create and update the actual progress bar.
* In the **Configuration** tab, use the **Add Property** button to add two Client Component configuration properties. Client Component configuration properties are those properties that the Consumer Client may use or change when using the Component.
	* progressBar: change to Type _JSON_ and check its **Hidden** checkbox. _progressBar_ is used internally by the Component to hold a reference to the actual progress bar so is marked _Hidden_ to tell the Consumer Client to not show it as a configuration property.
	* setProgress: change to Type _JavaScript Call-in Function_.
		* Use the **Add JavaScript function parameters** button in the **Actions** section to add a single parameter, _value_, to be used in the _setProgress_ function.
		* Use the **Description** button in the **Actions** section to provide documentation for the use of the _setProgress_ function:
`Use setProgress(value) to update the progress bar's value. Value must be a number between 0 and 1.`

		* Use the **Click to Edit** link to add the JavaScript code for the _setProgress_ function. This code calls the _ProgressBar.js_ API to change the value of the progress bar:
```js
// the component runtime configuration contains a reference to the
// progress bar
configuration.progressBar.animate(value, {
	duration: 100
});
```

* In the **Events** tab, click the **&lt;None&gt;** link under the **On Component Start** section. In the _Edit JavaScript_ dialog, enter the following code:
```js
	// retrieve a reference to the StaticHtml widget that will contain the progress bar
    var progressWidget = client.getWidget("StaticHtml1");
    if (progressWidget) {
        // retrieve a reference to the div in the widget
        var progressDiv = progressWidget.find("#progressDiv");
        if (progressDiv) {
            // change the ID of the div so it will be unique, in case there are
            // multiple copies of the component
            var pbName = this.name + "_progressDiv";
            progressDiv.attr("id", pbName);
            
            // retrieve a reference to this component's runtime configuration
    		var config = this.configuration;
            // create a progress bar and store its reference in the runtime configuration
            config.progressBar = new ProgressBar.Line("#"+pbName, {
                strokeWidth:5
            });
        }
    }
```
This code is run when the Client consuming the Component starts up. It remaps the &lt;div&gt; ID so that the Component can be used multiple times then creates the progress bar by calling the _ProgressBar.js_ API _new_ function. Note the call to _client.getWidget_. The identifier passed as a parameter (in the example this is _"StaticHtml1"_) will have to match the ID of the StaticHtml widget from Step c above. The ID for any widget is in quotes at the top of the property sheet shown when clicking on that widget in the Client Builder canvas.

Use the **Save Changes** button in the Client Component pane to save the _ProgressComponent_ Component.

## 3: Consuming the Progress Bar Component
Now that the Progress Bar Component is complete, Clients may use the Component like any other widget. This lesson creates a new Client which contains the ProgressBar Component and a slider widget to show how to change the value of the progress bar.

#### a. Create the Client
To create a new Client, use the **Add** button, select **Client**, then use the **New Client** button to create the _ProgressDemo_ Client.

#### b. Add Client Widgets
Once the _ProgressDemo_ Client pane appears, drag and drop a ProgressComponent widget from the **Add** palette onto the Client Builder canvas. The ProgressComponent widget is found in the **Components** section and is labeled **ProgressComponent**. (Whenever a Client pane is displayed, all Client Components in the current Namespace are displayed in the **Components** section of the **Add** palette.)

Next, drag and drop an InputInteger widget from the **Add** palette onto the Client Builder canvas. The InputInteger widget is found in the **Data Input** section and is labeled **Integer**.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ProgressDemo](../assets/img/client/ProgressDemo.png "Progress Demo")

#### c. Configure the Client Widgets
 Any non-hidden Component Configuration properties are always found in the Component's property sheet **Specific** section when used in a Consumer Client.

There is nothing to configure for the ProgressComponent since there were only two Component Configuration properties defined during the authoring process:

* setProgress: is a read-only property for the Component and is the single JavaScript function that the Consumer Client may call to set the value of the progress bar.
* progressBar: is a hidden property used internally by the ProgressComponent so does not appear in the property sheet.

There are two properties to configure in the InputInteger widget:

* In the **Specific** section, the _Input_ property should be changed to _As Slider_.
* In the **Event** section, click the **&lt;None&gt;** link for the **On Change** property. In the _Edit JavaScript_ dialog, enter the following code:

```js
// retrieve a reference to the progress bar component
var pb = client.getWidget("ProgressComponent");
if (pb) {
	// retrieve a reference to the component's runtime configuration
	var config = pb.configuration;
	config.setProgress(this.boundValue/100);
}
```
The **On Change** event function is called whenever the value of the slider changes. In this example, a reference to the ProgressComponent's widget is retrieved then a reference to the _setProgress_ exposed property is retrieved. Using that reference (the _config_ variable), the value of the slider, _this.boundValue_, is converted from a 0 to 100 based value to a 0 to 1 based value (which is used by the progress bar) and passed to the _setProgress_ function.

Use the **Save Changes** button in the Client pane to save the _ProgressDemo_ Client.

#### d. Run the Client
Use the **Run** button at the top, right of the _ProgressDemo_ Client pane to start running the Client:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunProgressDemo](../assets/img/client/RunProgressDemo.png "Run Progress Demo")

When moving the slider widget left and right, the progress bar exactly tracks the value of the slider position. This is a simple example of how calls to the _setProgress_ JavaScript function property of the _ProgressComponent_ are used in other Clients that would like to display the progress of Client operations.

## 4: Authoring a Configurable Data Stream Component
This lesson creates a Client Component that implements a Gauge widget that can easily adapt to a new source of data to display sensor readings. The lesson also shows how to expose widget properties for use in the Consumer Client so that the Client may configure how the Component is used. To start, create a new project in a new or current Namespace, as explained in Lesson 1 above. Title this project "SensorComponent".

#### a. Create the Client Component
To create a new Client Component, use the **Add** button, select **Client**, then use the **New Component** button to create the _SensorComponent_ Component.

#### b. Create a Data Object to Test the Component
To initially run the Gauge widget, the Component uses a Client Data Object, which is a convenient place to define 'global variables'. See the [Data Objects](../cbuser.md#data-objects) section of the Client Builder User's Guide for more details about Data Objects. To create a new Data Object, click the **Edit** tab of the Control Dock (on the left side of the Client Component pane), open the **Data Objects** tree entry,  then click **Client Data Object** tree entry. This displays the _Editing Data Object_ dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SensorDataObject](../assets/img/client/SensorDataObject.png "Sensor Data Object")

Use the **Add Property** button to add a new Data Object. Enter _sensor_ as the Name, select _Typed Object_ as the Data Type, then click the **Edit Typed Object** icon from the **Actions** menu. This displays the _client.data.sensor_ dialog. Click the **Add Property** button to add a single property, which will be used to store the value of a simulated sensor. Enter _n_ as the Name and select _Real_ as the Data Type, then click the **OK** button. The value _n_ will be referenced in the next section as the sensor value. Use the **Save and Exit** button to save the Data Object.

#### c. Create a Data Stream
Data Streams are used to feed data to Data Display widgets, such as the Gauge. See the [Data Streams](../cbuser.md#data-streams) section of the Client Builder User's Guide for more details about Data Streams. To create a new Data Stream, in the **Edit** tab of the Control Dock right-click the **Data Streams** tree entry, then select **Add 'On Client Event'** to display the _Edit Data Stream_ dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SensorDataStream](../assets/img/client/SensorDataStream.png "Sensor Data Stream")

This Data Stream uses the Data Object, _client.data.sensor_, created in the previous section. Enter _SampleSensor_ as the Data Stream Name, select _Get schema from client.data.object_ as the Client Event, and select _client.data.sensor_ as the Data Object. Use the **Save** button to save the new _SampleSensor_ Data Stream.

#### d. Add and Configure the Gauge Widget
Drag and drop a Gauge widget from the **Add** palette onto the Client Builder canvas. The Gauge widget is found in the **Data Display** section and is labeled **Gauge**. Click on the newly added Gauge widget to display its property sheet:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![GaugePropertySheet](../assets/img/client/GaugePropertySheet.png "Gauge Property Sheet")

* In the **Specific** properties section, click the **Expose Property** (small **+** icon) button to the right of the **Minimum** property and do the same for all properties through the **Title** property. The **Expose Property** button adds Component Configuration properties to the Component, which allow the Consumer Client to change each of those properties. In addition, enter _Sensor Readings_ for the **Title** property to change the title of the Gauge.

* In the **Data** properties section, click the **Expose Property** button for each of the **Data Stream** and **Data Stream Property** properties. These two Component Configuration properties allow the Consumer Client to use a different Data Stream, which is the objective of this section. In addition, select _SampleSensor_ for the **Data Stream** property and _n_ for the **Data Stream Property** property. These two values use the Data Stream and Data Objects from the previous two sections to display data in the Gauge widget.

Use the **Save Changes** button in the Client Component pane to save the _SensorComponent_ Client Component.

## 5: Consuming the Sensor Component
Now that the Sensor Component is complete, Clients may use the Component like any other widget. This lesson creates a new Client which contains the Sensor Component, a button to test the sensor gauge, and substitutes a new Data Stream to drive the gauge.

#### a. Create the Client
To create a new Client, use the **Add** button, select **Client**, then use the **New Client** button to create the _SensorDemo_ Client.

#### b. Create a Data Object
Follow the instructions from Lesson 4, section b (Create a Data Object to Test the Component) above. This Data Object is necessary in this Consumer Client to match that found in the _SensorComponent_ so the Gauge widget can be tested.

#### c. Add Client Widgets
Drag and drop a SensorComponent widget from the **Add** palette onto the Client Builder canvas. The SensorComponent widget is found in the **Components** section and is labeled **SensorComponent**.

Next, drag and drop an Inline Button widget from the **Add** palette onto the Client Builder canvas. The Inline Button widget is found in the **Buttons** section and is labeled **Inline**.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SensorDemoClient](../assets/img/client/SensorDemoClient.png "Sensor Demo Client")

#### d. Configure the Client Widgets
Click on the _SensorComponent_ widget to configure its properties.

* In the **Specific** section:
	* **Title**: enter _My Sensor_.
	* **Data Stream Property**: enter _n_, which is the sensor value configured in the Data Object.

Click on the Inline Button widget to configure its properties.

* In the **Specific** section:
	* **Button Label**: enter _Sensor Sample_.
* In the **Event** section:
	* **On Click**: enter the following code:
	
```js
	// set the Data Object sensor data
    client.data.sensor.n = 50.0;
    
    // retrieve a reference to the Sensor Component
    var gauge = client.getWidget("SensorComponent");
    if (gauge) {
        // find the Data Stream property of the Component's configuration
        var dataStream = gauge.configuration["Data Stream"];
        if (dataStream) {
            // send a Client Event to the Data Stream to set its value
            client.sendClientEvent(dataStream, client.data.sensor);
        }
    }
```

Use the **Save Changes** button in the Client pane to save the _SensorDemo_ Client.

#### e. Run the Client
Use the **Run** button at the top, right of the _SensorDemo_ Client pane to start running the Client:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SensorDemoRun](../assets/img/client/SensorDemoRun.png "Sensor Demo Run")

Click the **Sensor Sample** button. The **Sensor Readings** gauge will change to display a value of 50, which is the value entered in the Client Data Object code. This is a simple example to test that the _SensorComponent_ works with the default Data Stream.

Use the **Stop Running** button at the top, right of the _SensorDemo_ Client pane to stop running the Client.

#### f. Create an MQTT Source
This section creates an MQTT Source which will be used to drive the _SensorComponent_ Component in the _SensorDemo_ Client. Use the **Add** button, select **Source**, then use the **New Source** button to create the New Source pane.

* In the **General** tab, name the Source _Sensor_ and select _MQTT_ as the Source Type.
* In the **Server URI** tab, use the **Add Server URI** button to add a new server URI with the value of _tcp://public.vantiq.com:1883_. This references a publicly available Vantiq MQTT server which generates sample data.
* In the **Topic** tab, use the **Add Topic** button to add a new MQTT topic with a value of _com.vantiq.sensor.sample_.

Save the new source, then click the **Test Data Receipt** button in the pane to display realtime data from the MQTT server. A _Subscription_ pane will appear and data of the form shown below will be displayed:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SensorData](../assets/img/client/SensorData.png "Sensor Data")

Notice there are three property values returned by the MQTT topic. The last property is _vl_, which represents a voltage between 0 and 2.5 volts. Notice also data is delivered at one second intervals. Close the _Subscription_ pane after seeing the source data displayed.

#### g. Create a New Client Data Stream
Now that the _Sensor_ MQTT Source is active, it can be used in the _SensorDemo_ Client. In the **Edit** tab of the Control Dock, right-click the **Data Streams** tree entry, then select **Add 'On Source Event'** to display the _Edit Data Stream_ dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![MQTTDataStream](../assets/img/client/MQTTDataStream.png "MQTT Data Stream")

Enter _SensorSource_ as the Data Stream Name and select _Sensor_ as the Source. Use the **Save** button to save the new _SensorSource_ Data Stream.

#### h. Reconfigure the SensorComponent Widget
The _SensorComponent_ widget can now use the _SensorSource_ source sample voltage values to drive its gauge. Click on the _SensorComponent_ widget to display its property sheet:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![MQTTDataSource](../assets/img/client/MQTTDataSource.png "MQTT Data Source")

In the **Specifics** section, configure the following Component properties:

* **Low Range Zones**: _0:1.5_
* **Medium Range Zones**: _1.5:2.0_
* **High Range Zones**: _2.0:3.0_
* **Maximum**: _3.0_
* **Data Stream**: _SensorSource_
* **Data Stream Property**: _vl_, which is the voltage property value seen in the sample MQTT data

Use the **Save Changes** button in the Client pane to save the _SensorDemo_ Client.

#### i. Run the Client Using MQTT Data
Use the **Run** button to start running the Client:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SensorSourceRun](../assets/img/client/SensorSourceRun.png "Sensor Source Run")

The **Sensor Readings** gauge changes to display values between 0 and 2.5 volts at one second intervals, as retrieved by the _Sensor_ MQTT source.

So, by creating new Sources which retrieve at least one numeric value, the _SensorComponent_ can easily be reconfigured to display the data from those new Sources.

Now that this lesson is complete, please disable the _Sensor_ source by clicking the **Toggle Keep Active Off** button at the top, right of the _Sensor_ Source pane, then save the Source. Disabling the source will reduce the load on the publicly available Vantiq MQTT server.
