# Testing the Introductory Tutorial

## 1. Prerequisites
This tutorial assumes you have completed the entirety of the [Introductory Tutorial](tutorial.md). Please complete the tutorial if you have not
done so already, then return to this page to learn how to test it.

## 2. Overview
Create an Integration Test to ensure the _EngineMonitor_ Service always works as expected. 

A Vantiq Test is driven by a sequence of ordered input events and a collection of expected output events.
You want to create a Test that sends *SpeedEvent* and *TemperatureEvent* Inbound Event Type events as inputs and verify that the correct
*EngineStatus* alert events are produced.

The following cases will produce a *EngineStatus* Outbound Event with an *alertMsg*. You want to make sure the Test covers all three cases the Service may encounter:

1. The engine is running fine
2. The engine temperature is above 210 and the engine speed below 45
3. The engine temperature is above 210 and the engine speed is above or equal to 45

For a detailed explanation of the Vantiq testing system, please refer to the [Vantiq Testing Reference Guide](../tests.md).

## 3. Creating a Test

Using the **Add** button, select **Service** and open the *com.vantiq.engines.EngineMonitor* Service.

Navigate to the Service's **Test** tab using the tabs in the upper left-hand corner of the pane. Click the **+** button on the 
_Integration Test_ section header to create a new Service Integration Test.

Service Integration Tests are designed to test one Service
in complete isolation from the rest of the Project or Namespace. This means that only Procedure execution
and Inbound Service Event Types may be inputs and only Outbound Service Event Types may be outputs.

![EngineMonitorTest](../assets/img/introTest/133_CreateNewIntgTest.png "EngineMonitor New Test")

Enter *EngineMonitorTest* as the name and *com.vantiq.engines* as the package name. 
Set the description to _Tests The Engine Monitor Tutorial_. Set the Timeout to *30 seconds*.

Click **Save** to save the Service.
Notice that saving the Service creates the Integration Test and add it to the list of Integration Tests in the left-hand Project Contents tree.

![EngineMonitorTest](../assets/img/introTest/133_EngineMonitorTestGeneral.png "EngineMonitor Test General Tab")


## 4. Test Inputs

In this section, five test inputs are defined that will exercise the EngineMonitor Service. Test inputs are events
produced at test time which are processed by the Service.

Navigate to the **Inputs** tab and click the **Add Input** Button. 

![AddInput](../assets/img/introTest/133_FirstInput.png "First input")

For the first input, create an engine speed event. 

- Resource: *Service Events*
- ResourceId: _com.vantiq.engines.EngineMonitor/SpeedEvent_
- Delay: _1 Second_


Click on the **Click to Edit** button to open the Event Object Editor and create a JSON Object:

```json
{
    "systemId": "123",
    "speed": 50
} 
```

Click **OK** to close the JSON Editor and then click **OK and Add Another** to add another Input. 

Now create an input for the case in which the engine is overheating (the temperature is greater than or equal to 210).

![Second](../assets/img/introTest/133_TestIntroTut_SecondInput.png "second input")


- Resource: _Service Events_
- ResourceId: _com.vantiq.engines.EngineMonitor/TemperatureEvent_
- Delay: _3 Seconds_


Click on the **Click to Edit** button to open the Event Object Editor and create a JSON Object:

```json
{
  "systemId": "123",
  "temperature": 220
}
```

Click **OK** to close the JSON Editor and then click **OK and Add Another** to add another Input.

The two inputs above test one of the malfunction cases. Next, you want to ensure that if the Service receives temperature events below the overheating threshold, the alert message is cleared.

Create a new input with the temperature *below* the malfunction threshold.

- Resource: _Service Events_
- ResourceId: _com.vantiq.engines.EngineMonitor/TemperatureEvent_
- Delay: _3 Seconds_

The **Delay** value for this and the previous test input is artificially high (3 seconds) because these events are used to trigger a Visual Event Handler in a new Namespace created when a test is run. The tasks of a Visual Event Handler are compiled once as the first event is received for that task. That one-time compilation introduces a delay in event processing. By setting an artificially high delay value for the test input event generation, the testing process is compensating for the one-time compilation delay.

Click on the **Click to Edit** button to open the Event Object Editor and create a JSON Object:

```json
{
    "systemId": "123",
    "temperature": 200
} 
```

Click **OK** to close the JSON Editor and then click **OK and Add Another** to add another Input. Create a new input with the speed *below* the malfunction threshold.

- Resource: _Service Events_
- ResourceId: _com.vantiq.engines.EngineMonitor/SpeedEvent_
- Delay: _1 Second_

Click on the **Click to Edit** button to open the Event Object Editor and create a JSON Object:

```json
{
    "systemId": "123",
    "speed": 40
} 
```

Click **OK** to close the JSON Editor and then click **OK and Add Another** to add another Input. Create a new input with the temperature *above* the malfunction threshold.

- Resource: _Service Events_
- ResourceId: _com.vantiq.engines.EngineMonitor/TemperatureEvent_
- Delay: _1 Second_

Click on the **Click to Edit** button to open the Event Object Editor and create a JSON Object:

```json
{
    "systemId": "123",
    "temperature": 230
} 
```

Click **OK** to close the JSON Editor and then click **OK** to create the last input. 
Once all the inputs have been created, click the **Save Changes** icon in the top right corner to save the test.

![TestInputList](../assets/img/introTest/133_InputList.png "Input List")

## 5. Test Outputs

The Test expects three Outputs, one for each of the possible cases described above. 

The first Test Output expects the *EngineStatus* Outbound event produced by the Service when the engine is overheating and the speed is above 45.
Navigate to the **Outputs** tab of the test and click **Add Outputs**.

![133_FirstOutput](../assets/img/introTest/133_FirstOutput.png "First output")

- Resource: _Service Events_
- ResourceId: _com.vantiq.engines.EngineMonitor/EngineStatus_

Click on the **Click to Edit** button to open the Event Object Editor and create a JSON Object:

```json
{
    "systemId": "123",
    "alertMsg": "Your engine is overheating: please reduce your speed.",
    "temperature": 220,
    "speed": 50
} 
```

Click **OK** to close the JSON Editor. Then click **OK and Add Another**.

The next Test Output expects the *EngineStatus* Outbound event produced by the Service when the engine is no longer overheating.

- Resource: _Service Events_
- ResourceId: _com.vantiq.engines.EngineMonitor/EngineStatus_

Click on the **Click to Edit** button to open the Event Object Editor and create a JSON Object:

```json
{
    "systemId": "123",
    "alertMsg": "",
    "temperature": 200
} 
```

Click **OK** to close the JSON Editor. Then click **OK and Add Another**.

The last Test Output tests that an *EngineStatus* Outbound event is produced if the engine is overheating but the speed is less than 45.

- Resource: _Service Events_
- ResourceId: _com.vantiq.engines.EngineMonitor/EngineStatus_

Click on the **Click to Edit** button to open the Event Object Editor and create a JSON Object:

```json
{
    "systemId": "123",
    "alertMsg": "Your engine is overheating: check for a malfunctioning fan or a coolant leak.",
    "temperature": 230,
    "speed": 40
} 
```

Click **OK** to close the JSON Editor. Then click **OK** and save the Service.

![TestOutputList](../assets/img/introTest/133_OutputsList.png "Output list")

## 6. Running The Test

Click **Run Test** to run the Test. Click **Run Test** to confirm for the pop-up.

Click on the **Show Test History** button to see the list of Test Reports associated with this Test. 
Wait until the blue spinner becomes a green checkmark.

![TestReportCleaned](../assets/img/introTest/TestReportSpinner.png "Test report list")

This means that the test was a success and therefore cleaned up after itself, tearing down the associated testing namespace.

![TestReportCleaned](../assets/img/introTest/TestReportClean.png "Test report list")

Click on the *Test Run Id* for the Test run to open the Test Report.

![TestReportGeneral](../assets/img/introTest/TestReportGeneral.png "Test report general")


Navigate to the *Successes* tab, You should see all three of your defined Outputs listed.
 
![TestReportSuccesses](../assets/img/introTest/TestReportSuccesses.png "Test report successes")

Navigate to the **Errors** tab and ensure there were no errors during test execution.

![TestReportErrors](../assets/img/introTest/TestReportErrors.png "Test report errors")

### Conclusion

Users who have successfully completed this tutorial can comfortably create and run Service Integration tests!