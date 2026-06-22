# Testing the Source Tutorial

## Prerequisites
This tutorial assumes you have completed the entirety of the [Source Tutorial](sourcetutorial.md). 
Please complete the tutorial if you have not done so already, then return to this page to learn how to test it.

## Testing Sources Rules

We will now create a Unit Test to ensure that our Rule always works as we expect. A Unit Test is preferable to an Integration
Test for this case because we are only testing the functionality of a single Rule rather than of a whole Project or App.

A Vantiq Test is driven by a
sequence of ordered input events and expects a collection of output events.
We want to create a Test that 

* creates a Source event from the Weather Source as an input and 
* expects an UPDATE on the `weatherReading` Type as an output.

Navigate to the `weatherReading` Rule and click the **Create Test** button.

![CreateTest](../assets/img/testsource/CreateTestBtn.png "Create Test")

Set the name of the test to `weatherReading0`.

![CreateTestPopup](../assets/img/testsource/CreateTestPopup.png "Create Test Popup")

Click on the pencil button to edit the Event Object. The event object is the message that will arrive from the Source
to trigger the Rule during the Test run. 
The following JSON Object is a sample event received from the `weather` Source. It was captured and copied during step 2
of the [Source Tutorial](sourcetutorial.md) using the Test Data Receipt feature. It is important for the Test data to resemble
real data as closely as possible, to accurately test the system under the correct conditions.

Copy and paste the following Source message into the JSON editor and then click **OK**.
```
{
   "coord": {
      "lon": -122.12,
      "lat": 37.89
   },
   "weather": [
      {
         "id": 800,
         "main": "Clear",
         "description": "clear sky",
         "icon": "01d"
      }
   ],
   "base": "stations",
   "main": {
      "temp": 294.78,
      "feels_like": 290.57,
      "temp_min": 292.59,
      "temp_max": 297.15,
      "pressure": 1023,
      "humidity": 23
   },
   "visibility": 16093,
   "wind": {
      "speed": 3.1,
      "deg": 80
   },
   "clouds": {
      "all": 1
   },
   "dt": 1582680753,
   "sys": {
      "type": 1,
      "id": 3581,
      "country": "US",
      "sunrise": 1582641979,
      "sunset": 1582682233
   },
   "timezone": -28800,
   "id": 5364226,
   "name": "My Address",
   "cod": 200
}
```

A new **Test** pane opens with all of the General properties on the test already set.

![SourceTest](../assets/img/testsource/SourceTestGeneral.png "Source Test General Tab")

Navigate to the **Inputs**
tab and verify that there is one input in the Inputs list.

![SourceTestInputsList](../assets/img/testsource/SourceTestInputsList.png "Source Test Inputs Tab")

The Test expects one output: The UPDATE to the `weatherReading` Type performed by the Rule.
To accomplish this, navigate to the **Outputs** tab and click the **Add Output** Button. 

The `weather` Rule performs an UPDATE on the *weatherReading* with the matching location. 
It is assumed that the Test pre-populates the Namespace with an instance of *weatherReading* to be UPDATED. We will include this later using a **Setup** Procedure.
The existing instance includes the *zipCode* and *location* properties. The Rule updates the instance to include 
the *tempK* property.

Set *types* as the Resource, *weatherReading* as the ResourceId and *UPDATE* as the Operation.

![SourceTestFirstOutputPopup](../assets/img/testsource/SourceTestFirstOutputPopup.png "First output event")

Click on the **Click to Edit** button to open the Expected Object Editor and create a JSON Object with the following contents:

```
{
   "location": "My Address",
   "tempK": 294.78,
   "zipCode": "94609"
}
```
Click **OK** to close the Event Object Editor, then **OK** again to save exit the Edit Output popup.

Because one of the Test outputs is an expected UPDATE event, it is implied that there will already be an existing instance
of the `weatherReading` Type to be UPDATED. The Test therefore requires **Setup** and **Cleanup** Procedures.

Use the **Add** button in the IDE Navigation Bar, hover over **Advanced**, and select **Procedures**. Click the **New Procedure** button to create a new Procedure.

Name the Procedure `createWeatherData`. This Procedure is the Test **Setup** Procedure. The Procedure sets the `weather` Source into Mock Mode and 
INSERTS the necessary instance of the `weatherReading` Type. 

To learn more about Source Mock Mode, reference the [Testing Reference Guide](../tests.md#source-mocking-for-tests).

Copy and paste the following into the new Procedure Pane:

```
PROCEDURE createWeatherData()
Test.startSourceMocking("weather", null, null)
INSERT weatherReading(location:"My Address", zipCode:"94609")
```

Click **Save** to save the Procedure.

Add a second procedure, and name it `deleteWeatherData`. This Procedure is the **Cleanup** Procedure. The Procedure turns off Mock Mode on the `weather` Source and DELETES
 the created instance of the `weatherReading` Type.
  
Copy and paste the following into the new Procedure Pane:

```
PROCEDURE deleteWeatherData()
DELETE weatherReading WHERE zipCode == "94609"
Test.stopSourceMocking("weather")
```

Click **Save** to save the Procedure.

Navigate back to the **Test** pane in which we were defining the `weatherReading0` test and click on the **General**
tab.

Select **createWeatherData** as the **Setup Procedure** and **deleteWeatherData** as the **Cleanup** Procedure. **Save** the
Test.

![SetupAndCleanupSourceProcs](../assets/img/testsource/SetupAndCleanupSourceProcs.png "Setup and Cleanup Procedures")

Navigate back to the `weatherReading` Rule. Select the new test `weatherReading0` from the Execute droplist and then
click **Run**.

![ExecuteTest](../assets/img/testsource/ExecuteTest.png)

Navigate back to the Test pane for `weatherReading0` and click **Show Test History**.
 
 ![TestHistory](../assets/img/testsource/ShowTestHistory.png)

Expect one entry with a green check showing that the test run was a success.

 ![SuccessfulTest](../assets/img/testsource/SuccessfulSourceTest.png)

## Adding Source Query Mocking
You can also use a Procedure to supply test data for the Source when running the test.  This is called _mocking_ the Source.
In this section, we will add a Procedure `querySourceAndInsert` that uses our Source, and then add a Procedure to supply mock data for that source, which will be used in testing the `querySourceAndInsert` Procedure.

First, let's create the Procedure `querySourceAndInsert`.
Click the **Add** button, hover over **Advanced**, and click  **Procedure...** Click the **New Procedure** button to create a new Procedure.

The `querySourceAndInsert` Procedure queries the `weather` Source and then INSERTS an instance of the `weatherReading` Type.
We will use this Procedure in our Test to show Mocking a query to a Source.

Copy and paste the following into the new Procedure Pane:

```
PROCEDURE querySourceAndInsert()
var weatherReading = SELECT FROM SOURCE weather 
weatherReading = weatherReading[0]
INSERT weatherReading(tempK:weatherReading.main.temp, location: weatherReading.name, zipCode = "94609")
```

Click **Save** to save the Procedure.

Now let's create our Mocking Procedure. Click the **Add** button, hover over **Advanced**, and click  **Procedure...** Click the **New Procedure** button to create a new Procedure.

The `queryProcedureOverride` Procedure mocks the `weather` Source's *query* functionality by always returning the same object.

```
Procedure queryProcedureOverride(queryDesc)
return {
   "coord": {
      "lon": -122.12,
      "lat": 37.89
   },
   "weather": [
      {
         "id": 800,
         "main": "Clear",
         "description": "clear sky",
         "icon": "01d"
      }
   ],
   "base": "stations",
   "main": {
      "temp": 75,
      "feels_like": 290.57,
      "temp_min": 292.59,
      "temp_max": 297.15,
      "pressure": 1023,
      "humidity": 23
   },
   "visibility": 16093,
   "wind": {
      "speed": 3.1,
      "deg": 80
   },
   "clouds": {
      "all": 1
   },
   "dt": 1582680753,
   "sys": {
      "type": 1,
      "id": 3581,
      "country": "US",
      "sunrise": 1582641979,
      "sunset": 1582682233
   },
   "timezone": -28800,
   "id": 5364226,
   "name": "Walnut Creek",
   "cod": 200
}
```

Click **Save** to save the Procedure.

Navigate back to the  `createWeatherData` Procedure and update the `Test.startSourceMocking` Procedure to set the **Query
Mock Procedure** to the new Procedure we just created.

```
PROCEDURE createWeatherData()
Test.startSourceMocking("weather", "queryProcedureOverride", null)
INSERT weatherReading(location:"My Address", zipCode:"94609")
```

Click **Save** to save the Procedure.

Navigate back to the `querySourceAndInsert` Procedure. Click the **Create Test** button. Confirm by clicking `Create Unit Test` 
then type _querySourceAndInsert0_ as the test name and click **OK**.


A new Test called `querySourceAndInsert0` opens. 
 
![CreateTest](../assets/img/testsource/querySourceTestGeneral.png "Create Test")

 
Navigate to the **Inputs** tab and you will see this test has a single input, running the `querySourceAndInsert` Procedure.

![CreateTest](../assets/img/testsource/querySourceTestInput.png "Create Test")

Right click this input and click **Edit**. 

![CreateTest](../assets/img/testsource/querySourceInputPopup.png "Create Test")

In the test input, an expected Return Value is automatically generated. This is normally quite helpful, but in this case we want to override the return value with the mock data we created in the `queryProcedureOverride` Procedure. Therefore, open the **Expected Return Value** editor by clicking the **Click to Edit** button, and delete the contents of the editor. This will cause the test to ignore the return value of the Procedure. Close Event Object Editor by clicking **OK**, then exit the Edit Test Input popup by clicking **OK**.

Click on the **Outputs** tab. Click the **Add Output** Button. 

For the output, set *types* as the Resource, *weatherReading* as the ResourceId and *INSERT* as the Operation.
This captures the INSERT produced by the *querySourceAndInsert* Procedure.

![SourceTestSecondOutputPopup](../assets/img/testsource/SourceTestSecondOutputPopup.png "Second output event")

Click on the **Click to Edit** button to open the Expected Object Editor and create a JSON Object with the following contents:

```
{
   "location": "Walnut Creek",
   "tempK": 75,
   "zipCode": "94609"
}
```
Click **OK** to close the Event Object Editor.

Navigate to the **General** Tab. Select **createWeatherData** as the **Setup Procedure** and **deleteWeatherData** as the **Cleanup** Procedure. **Save** the
Test.

![SetupAndCleanupSourceProcs](../assets/img/testsource/querySourceGeneralWithSetup.png "Setup and Cleanup Procedures")

Navigate back to the `querySourceAndInsert` Procedure. Select the new test `querySourceAndInsert0` from the Execute droplist and then
click **Run**.

Navigate back to the Test pane for `querySourceAndInsert0` and click `Show Test History`.

Expect one entry with a green check showing that the test run was a success.

 ![SuccessfulTest](../assets/img/testsource/SuccessfulQueryTest.png)

## Conclusion ##

After successfully navigating through this tutorial, the user should be familiar with:

* Creating Unit Tests for Rules and Procedures
* Running Unit Tests from the Rule/Procedure Pane
* Setting a Source to Mock Mode and overriding Source behavior with Mock Procedures

