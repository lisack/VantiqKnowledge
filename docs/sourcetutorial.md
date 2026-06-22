# Source Tutorial

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_PRG](../assets/img/source/128_SourcesTut_PRG.png "Project Resource Graph")

## Purpose

To introduce how to derive and process events from sources outside of Vantiq applications.

## Objectives

Upon completion of the tutorial, a new Vantiq developer should easily be able to:

* Locate the areas of the IDE where sources, rules and procedures are defined
* Populate datatypes with JSON objects to use in applications
* Use rules triggered by incoming data to make changes as needed
* Test source data input functionality with procedures and menu choices

## Tutorial Overview
This tutorial guides a developer through lessons in the use of data sources in Vantiq system. It uses a publicly available weather feed to retrieve a temperature forecast which then triggers a rule to save that temperature value. The temperature value can then be combined with other data in rules to provide temperature-related decisions.

All lessons assume the developer has a working knowledge of the [Vantiq IDE](../../../..). It is recommended that a new developer completes the lessons in the [Introductory Tutorial](tutorial.md) before starting the lessons in this tutorial. 

>Note: if needed, you can import a finished version of this project using the _Projects -> Import_ menu item.  Just select _Tutorials_ for Import Type, then select _Sources_ from the second drop-down, then click _Import_.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

## 1: Creating a Source Project
The first task is to create a project in the IDE to assemble all the source components.

Use the **Projects** button, select **New Project**, which displays the New Project Wizard. Either create a new Namespace (recommended) or add a new project to the current Namespace, select **Empty** as the Project type, and title the project "WeatherSource":

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SourceProject](../assets/img/intro/EMProject.png "Create Weather Source Project")

The rest of the lessons take place inside this Project.

## 2: Creating The Source
A source in Vantiq system allows for the integration of external data sources, both for the retrieval of data and as the recipient of data. For in-depth information about sources, please refer to the [Vantiq Reference Guides](../sources/remote.md).

This tutorial retrieves weather information from [OpenWeatherMap](http://openweathermap.org/), which provides weather forecast data via a REST interface. The first task is to create the source, which defines how to interact with the OpenWeatherMap API. OpenWeatherMap requires the use of a free API key in order to retrieve data. Please visit the [OpenWeatherMap key page](http://openweathermap.org/appid#get) in order to create the key you'll use later in this lesson.

Use the **Add** button to select **Source...** then use the **New Source** button to create our source, and name it _weather_.

Since OpenWeatherMap provides its weather forecast data via a REST interface, select the _REMOTE_ Source Type. Next, switch to the properties tab, where most of the configuration for the source will take place.

There are many options in this tab, but for now we will focus on just a few. Expand the "Polling Properties" section and change the Polling Interval to 15 seconds. This specifies how often the forecast data is retrieved. Select the _application/json_ Content Type since the forecast data is returned in JSON format.

Next, enter _https://api.openweathermap.org/data/2.5/weather_ as the Server URI to define the URI used to retrieve OpenWeatherMap data. This is the base endpoint, but we will want to specify query parameters to fetch the information we need. For this example, the forecast data is retrieved using geographic coordinates (`lat` & `lon`), although forecast data can also be retrieved via city name (using `q`), city id, or a zip code (`zip`).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_weatherSource](../assets/img/source/128_SourcesTut_weatherSource.png "Create Source")

Putting all of the information in the Server URI line will work, but it is better form to set the query parameters.  Within "Request Default Properties", click Query Parameters and enter the following json.
```
{
   "lat": "37.91",
   "lon": "-122.07",
   "APPID": "<YOUR_APP_ID>"
}
```

Make sure you replace "<YOUR_APP_ID\>" with the API token you created.

Once the source has been configured, save the source, then use **Test Data Receipt** to try to retrieve data from the source. A new subscription will appear and display any events received by the source. You can click on any of the events to view its data. For example, here is some sample data from our _weather_ source:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_JSONData](../assets/img/source/128_SourcesTut_JSONData.png "Test Data Receipt")

Click the back button in the top left of the subscription to return to the source. Use the **Save** button in the top left corner to save the project.

## 3: Creating a Data Type
The weather forecast data retrieved from OpenWeatherMap needs to be stored in the Vantiq database so that it can be used with other data to trigger situational-specific rules. You must create a data type to specify that data.

Uncheck *Keep Active* in the source definition window to stop receiving data for now.

Use the **Add** button to select **Type...**:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![AddType](../assets/img/intro/128_IntroTut_BlackTypeScreen.png "Add Weather Type")

Use the **New Type** button to create the forecast reading type:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_weatherReading](../assets/img/source/128_SourcesTut_weatherReading.png "Create Forecast Type")

The _weatherReading_ type contains five properties:

* location: a (required) String property which identifies the city associated with the forecast data
* tempF: a Real property which holds the Fahrenheit value of the temperature forecast
* tempK: a Real property which holds the Kelvin value of the temperature forecast
* windSpeed: a Real property which holds the Kph value of the wind speed forecast
* zipCode: a (required) String property which identifies the zip code associated with the forecast
	
Both _location_ and _zipCode_ are required to make sure OpenWeatherMap sends well-formed data. Once these five User Properties are defined, use the **Save** button to save the _weatherReading_ type.

Use the **Save** button in the top left corner of the IDE to save the project.

## 4: Creating a Data Instance
For our example, we must create an entry in the Vantiq database that defines the city where the forecast data for the specified zip code is stored.

Use the **Show** button to select **Add Record...**, then use the **Type** pull-down menu to create the _weatherReading_ instance:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_addRecordZip](../assets/img/source/128_SourcesTut_addRecordZip.png "Create Weather Reading")

Select the _weatherReading_ Data Type since you are creating a _weatherReading_ entry. Enter the city you specified for the location parameters in the URI as the location property.  In the example shown before, the city associated with the zipcode is Walnut Creek. Enter the corresponding zipcode property; in the example this was _94598_. Use the **Add New Record** button to save the entry. This creates one _weatherReading_ entry to store the weather forecast data by zip code, and ties that zip code to the desired city.

## 5: Creating a Rule
Rules are Vantiq Automation and Integration Language (VAIL) code triggered when data has been added or modified in the Vantiq database, and can specify how to organize that data for further processing. In our example, there is one Rule, which is triggered whenever forecast data is retrieved from the _weather_ source created in Lesson 2.

Use **Add** -> **Advanced** to select **Rule...**:


Use the **New Rule** button to create your weather forecast processing rule:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_weatherSourceRule](../assets/img/source/128_SourcesTut_weatherSourceRule.png "Create Forecast Rule")

The _weatherReading_ rule reads as follows:

```js
RULE weatherReading

WHEN EVENT OCCURS ON "/sources/weather" AS weather
UPDATE weatherReading(tempK:weather.value.main.temp) WHERE location == weather.value.name
```

This rule is triggered whenever forecast data is retrieved from the OpenWeatherMap _weather_ source. The _WHEN EVENT OCCURS ON "/sources/weather" AS weather_ statement specifies the _weather_ source name and subsequent references to _weather_ refer to the data returned by the source.

This rule simply updates the _weatherReading_ current temperature (in Kelvin) for the location associated with the forecast (indicated by the _location_ property). The forecast data is returned in JSON format so the rule uses the _weather_ source variable as the root of the JSON object to retrieve relevant forecast data: weather.value.main.temp is the temperature forecast in Kelvin and weather.value.name is the city location associated with the forecast. Check the **Active** checkbox (next to the **Save** button) to enable the rule then use the **Save** button to save the rule and return to the Project.

Use the **Save** button in the top left corner of the IDE to save the project.

## 6: Verifying and Using The Data
This lesson verifies that weather forecast data is properly retrieved by the _weather_ source and saved by the _weatherReading_ rule. In addition, this lesson also demonstrates how that saved forecast data might be used in other rules.

Since forecast data is retrieved every 15 seconds (the _weather_ source's Polling Interval), no more than 15 seconds will pass after you created the _weatherReading_ rule in Lesson 5 before data is stored in your _weatherReading_ instance. To verify that the source and rule are triggering, use the **Show** button to select **Find Records** to display the _Find Records_ query pane:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![QueryForecast](../assets/img/source/QueryForecast.png "Query Forecast")

Select the _weatherReading_ data type then use the **Run Query** button to retrieve all _weatherReading_ objects from the Vantiq database:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_RecordResult](../assets/img/source/128_SourcesTut_RecordResult.png "Forecast Data")

There should only be one instance for the zip code you created in Lesson 4. The only _weatherReading_ property updated by the _weatherReading_ rule is tempK, which is set to 301.55 in the example above. This indicates that _weather_ source has retrieved data, which triggered the _weatherReading_ rule, which updated the _weatherReading_ data type for the Walnut Creek location.

Now that the forecast data is available, you can use it for other purposes. For example, if you want to offer a special sale to customers located where there's a heat wave, the following rule could be defined:

```js
WHEN EVENT OCCURS ON "/types/Customer/update" AS Customer
SELECT UNIQUE weatherReading:wr WHERE zipCode EQ Customer.value.location

if (wr.tempK >= 300) {
    UPDATE Offer(offerMessage: "Buy a fan") WHERE (customerId == Customer.value.id)
}
```

Here is a breakdown of this example rule, starting with:

```js
WHEN EVENT OCCURS ON "/types/Customer/update" AS Customer
SELECT UNIQUE weatherReading:wr WHERE zipCode EQ Customer.value.location
```

This rule is triggered whenever a customer (defined by a _Customer_ data type) instance is updated, for example, when the customer enters a store in a particular zip code. The SELECT UNIQUE statement instructs the rule to find the weather forecast (the _weatherReading_ data type) entry for the customer location by referencing the zipCode.

Next is the `if` statement which evaluates whether the outside temperature forecast for the store's zip code is equal to or greater than about 80F/27C (300K):

```js
if (wr.tempK >= 300) {
```
    
and, if so, updates the Offer data type associated with the customer's ID:

```js
	UPDATE Offer(offerMessage: "Buy a fan") WHERE (customerId == Customer.value.id)
}
```
## 7: Using Secrets In Sources

Often, you won't want all the information in a source to be visible to anyone who can access the source.
In the OpenWeatherMap source, you may not want to expose your API key to anyone who can access the source.
To address this, Vantiq provides a mechanism for storing secrets in the Vantiq system.

To add a secret, click **Administer**, hover **Advanced**, and then click **Secrets** to open the **Secrets** pane.
Click the **New** button in the **Secrets** pane to create a new secret. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_PRG](../assets/img/source/newSecret.png "Add New Secret")

Name the secret `apiKey` and give it a description.
For the "Secret" field, paste your API key from OpenWeatherMap.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_PRG](../assets/img/source/secretField.png "Create New Secret")

Save the secret. Next, open your source and reopen the Query Parameters popup. Replace your api key with `"@secrets(apiKey)"`. 
This will cause the source to use the secret you created to look up your api key, without the key being visible to anyone who can access the source.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_PRG](../assets/img/source/secretParam.png "Add New Secret to Source")

## 8: Deactivating or Deleting a Source

When you are finished with this tutorial, you should either (1) deactivate the source or (2) delete the source so that data from OpenWeatherMap doesn't continue to be collected. At this point, the IDE's _Project Resource Graph_ pane should look similar to this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_PRG](../assets/img/source/128_SourcesTut_PRG.png "Project Resource Graph")

To deactivate the source, click the _Source: weatherSource_ oval in the _Project Resource Graph_ to display the _Source: weatherSource_ pane:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![128_SourcesTut_weatherSource](../assets/img/source/128_SourcesTut_weatherSource.png "Create Source")

Select the **Properties** tab then uncheck the **Keep Active** checkbox of the _Source: weather_ pane, then use the **Save Changes** icon button in the pane (down arrow at the top, right of the pane) to save the source.

To delete the source, right-click on the _Source: weatherSource_ oval in the _Project Resource Graph_ and select _Remove from Project and Delete_ from the menu.

## 9: Testing The App

Congratulations! You just built your first Vantiq application using Sources. However, there is an important piece missing.
How can you ensure your Rule works, and will always work as you expect?

Learn how to test the App you just built by clicking here: [Testing the Source Tutorial](testsourcetutorial.md)

## Conclusion ##

After successfully navigating through this tutorial, the user should be familiar with:

* How to create and configure sources from URIs
* Polling the data from the source
* Populating datatypes with the source data
* Creating rules to manipulate data in records
* Test that the data is consistent with procedures that anticipate inputs and outputs
