# Vantiq Testing Reference Guide

## Introduction

Testing Applications is a critical step in the Software development lifecycle. The ability to ensure correctness of an Application
throughout its lifetime is key to its success.

Vantiq Applications are event driven and therefore Vantiq Tests must be as well. Vantiq Tests
are capable of simulating and validating every type of event that may occur within the system including
publishes to Topics, interactions with Sources, operations on Types, and executions of Procedures. 

**Note:** This does not include testing Clients or System Models

There are two categories of Vantiq Tests: **Unit Tests** and **Integration Tests**. A Vantiq Unit Test is for testing Procedures,
Rules, and inbound Service Event Types individually. A Vantiq Integration Test is used to test Applications at the Project level. This is targeted towards 
testing Services, Apps, Collaborations and how they interact with each other within an Application/Project. 

## Types of Tests

### Unit Tests
A Unit Test tests an individual Procedure, Rule, or inbound Service Event Type rather than a complete Project. The test is run in the same Namespace
as the Rule, Procedure, or Service is defined.
 At the end of a Test run, a report is
created including which outputs were successful or failed, as well as any errors produced during Test 
execution.

### Integration Tests

Integration Tests are used to test the functionality of entire projects, rather than individual resources. At runtime, a Testing 
Namespace is created. The Project being tested is deployed to the new Namespace. A sequence of ordered input
events described by the Test are generated and the Test waits for the expected outputs. 

At the end of a Test, a report is upserted from the Testing Namespace to the original Namespace. The report includes
which outputs were  successful or failed, as well as any errors produced during Test execution. In the 
event of a successful run, the Namespace is deleted. In the event of a failure, the Testing Namespace is saved
by default for the developer to further investigate what went wrong.

A specialized version of Integration Tests exists for [Services](services.md#integration-tests). Service Integration Tests define a 
Service as the test resource rather than a Project. At runtime, a Service Integration Test
will generate a Project that contains only the Service and its implementing resources. That project will be deployed to a 
Testing namespace so that it can be tested in isolation from the rest of the Project. 

**Note**: Unit Tests are much faster than Integration
Tests because they are run in the same namespace as the defined Rule or Procedure. They do not require
generating a new namespace and deploying the Project first. 

Test Reports for Test runs are found by clicking `View Test History` in the `Test` Pane or in the actions menu on the `Tests` Pane.

![Test Report Detail](assets/img/tests/TestReportGeneral.png "Test Report General")

Developers can find all of the Testing Namespaces associated with failed Tests under the Testing Namespaces section of 
the `Switch Namespaces` pop-up. A developer may also navigate to a Testing Namespace for a particular Test run by clicking 
the `Switch to Testing Namespace` button within the `Test Report` Pane.

![Switch Namespaces Popup](assets/img/tests/SwitchNSPopup.png "Switch Namespace Popup")

  
## Defining a Test 
Tests are defined by the following properties:

* **name** (String, _required_): Name of the Test 
* **description** (String): Description of the Test 
* **resource** (ResourceReference, _required_): If the Test is an Integration Test, then the resource associated with the Test is a Project or Service.
  If the Test is a Unit Test, then it is the Procedure, Rule, or Service with a unitReference defined (ex: `/projects/myProject` or `/rules/MyRule`)
* **unitReference** (Object, _required for service unit tests_): For Service Unit Tests, this property is required to specify which piece of the Service is being tested. This is an Object 
with the format *{type: <unit type\>, name: <unit name\>}* where type is either *eventTypes* or *procedures* and the unit name is the name of the Event Type or Procedure being tested.
* **inputs** (Array of Objects): The list of input objects (see below for how to define inputs)
* **outputs** (Array of Objects): The list of outputs objects (see below for how to define outputs)
* **timeoutTime** (String, _required_): Global timeout time before the Test terminates. An interval string that limits how
 long the test is allowed to run (ex: `1 minute`).
The Test terminates after the time interval and all unseen outputs at this point are recorded as failures.
* **saveNamespace** (Boolean): In the event of an Integration Test failure, this toggles whether or not the Testing namespace should be
  saved or deleted. This defaults to true in the IDE so that if a Test fails, the developer may inspect what went wrong.
* **runPolicies** (Array of Objects): Array of run policy descriptors.  Run Policies define a time interval for how frequently an automatic Test run will be triggered.
(See below for how to define a run policy descriptor).
* **setup** (String):  The name of a zero-parameter Procedure which is executed before the Test begins running.
  Use a setup procedure to prime the testing environment so that the Test may run correctly.  
* **cleanup** (String): Name of a zero-parameter Cleanup Procedure which runs just after the
Test completes. The Procedure will run whether or not the Test is successful. This is most useful for Unit Tests which run in 
the local Namespace. If the Test has any side-effects, the developer 
may want to clean-up their Namespace after the Test has completed.
* **unitAutopsy** (Boolean): If set to true, this will turn on Tracing for the test resource during the test run.  
 Note: this applies to Unit Tests only. Global tracing is automatically
enabled for Integration Tests.
* **unitLogLevel** (String): The log level set on the test resource during the test run.  
Note: this applies to Unit Tests only. A global "DEBUG" log level is automatically set for Integration Tests.    

![Test Definition](assets/img/tests/VantiqTestGeneral.png "Test General")


### Defining an Input
A Test's ordered inputs list describes inputs that are generated at Test time. Each input may contain the 
following properties:

* **resource** (String, _required_): Resource associated with the event: "procedures", "types", "topics",  "sources", "eventtypes", "services", or "eventgenerators"
* **resourceId** (String, _required_): Unique name of the resource on which the event is created
* **op** (String, _Type event only_,  _required_): Operation associated with the Type event: INSERT, UPDATE, or DELETE 
* **qual** (String, _UPDATE/DELETE only_, _required_): The associated WHERE clause for the UPDATE or DELETE operation required
to qualify the operation to the targeted instances. `(ex: name == “ABC”)`
* **Event Object** (Object): The message associated with the event. 
    * Type events: Object that is INSERTED or UPDATED. 
    * Source events: Message that will arrive from the Source. 
    * Topic events: Message that is published to the given Topic. 
    * Procedure execution: Object describing parameters passed into the Procedure.
* **returnValue** (Object, _Procedures only_): The expected return value of a Procedure call. If this is not set, the returnValue
for the Procedure will be ignored. The returnValue will be compared with the Procedure's actual return value to validate the received return value.
The defined returnValue will be cross-checked key by key with the received return value. Keys that are not specified in the returnValue object will
not be used for validation and will be ignored. This allows variable properties, such as timestamps, to be omitted from the validation 
process.
* **periodic** (Boolean): Whether or not the input should repeat periodically
* **periodInterval** (String, _Periodic inputs only_): The interval between each periodic input event of this type (ex: `1 minute`)
* **delay** (String): The time interval before the following event occurs after this one (ex: `1 minute`)

![Input Definition](assets/img/tests/EditInputsPopup.png "Input Popup")

### Defining an Output
The outputs list of a Test defines a list of outputs that are expected by the Test. Each output may contain the 
following properties:

* **resource** (String, _required_): Resource associated with the event:  "types", "topics", "sources", "eventtypes", or "services"
* **resourceId** (String, _required_): Unique name of the resource on which the event is created
* **op** (String, _Type event only_, _required_): Operation associated with the Type event: INSERT, UPDATE, or DELETE 
* **Missing** (Boolean): The Test should not receive an output on this _/resource/resourceId_ event path with the specified event value. If an output event
marked as missing is received during Test execution, an error is logged and the Test fails.   
* **validationMethod** (String, _required_): The method which is used to check if the received output was valid.
This property may be set to either: "Event Object", "Validation Procedure", or "Validation Procedure With Expected Object". Depending
on the validationMethod chosen, the following 2 properties will have to be specified.
* **eventObj** (Object) : The event object description to be compared with the received event to validate the received output event.
The defined eventObj will be cross-checked key by key with the received event. Keys that are not specified in the eventObj will
not be used for validation and will be ignored. This allows variable properties, such as timestamps, to be omitted from the validation 
process.
* **validationProcedure** (String): The name of a user-defined Procedure used to validate the event. If no event object is specified,
the Procedure must take in one parameter: the received event. If an event object
  is specified, the procedure must take two parameters: the received event as the first parameter, and the expected event (eventObj) as the second parameter.
The procedure must return _true_ if the event was valid and _false_ otherwise.
* **repeat** (Object) : A bounded range of the number of events of this type that should be expected by the Test.
If this property is not set, the output validation will default to expecting one or more events.
If the number of received outputs of this type does not match what is expected, the Test fails.
The repeat Object requires two keys:
    * *op* (String): This is the operator that defines the bounded range. Must be either "<", "<=", "==", ">=", or ">"
    * *value* (Integer): The value that defines the bounded range
(ex: `{"op": "<", "value": 10}`)
* **error** (Boolean): Set to true if this output represents an expected error. For an error output set the 
resource to *types* and the resourceId to *ArsRuleSnapshot*. Error outputs require *eventObj* validation where the eventObj 
specifies the `message`, `errorCode`, and `name` of the error producing resource.
* **timeoutTime** (String): Amount of time after the timeout event (see below) that this output must occur in order to be considered 
valid. If no timeout event is specified then the event must occur within the _timeoutTime_ of the global start time of the Test. (ex: `1 minute`)
* **timeoutEvent** (Integer): The index of a specified input event within the inputs list. This output event must occur within _timeoutTime_ 
of the specified input event to be considered valid. 
* **prereqEvent** (Object): An input event that must occur before this output occurs in order for this output to be
considered valid. The input may be required to occur a specified number of times as a compound prerequisite event.
The prereqEvent Object requires two keys:
    * *event* (Integer): The index of a specified input event within the inputs list
    * *num* (Integer): The number of times the prerequisite event must occur for the output to be considered valid

![Output Definition](assets/img/tests/EditOutputsPopup.png "Output Popup")

### Defining a Run Policy

Run Policies define how frequently an automatic run of the Test should be triggered.
For example, this allows developers to run the Tests every hour or every night automatically. 

The `runPolicies` property of a Test is a list of Objects. A run policy object for a Scheduled run policy includes the following properties:

* *type* (String, _required_): This must be set to "scheduled"
* *intervalAsText* (String, _required_): The frequency that the Test should be run (ex: `1 hour`)
* *occursAt* (DateTime): The time to begin the scheduled testing. Defaults to `Starting Now`.

**Note**: The minimum frequency that may be set is *1 hour*. Tests may not be scheduled to run automatically more frequently 
than once an hour. Also, only one test may be run at a time. Make sure that scheduled test runs will not conflict and begin
trying to run at the same time.

![Run Policies](assets/img/tests/RunPolicies.png "Run Policies")

### Populate Testing Namespace With Data

Tests may specify a `setup` Procedure which will run after the test Project has been deployed to the testing Namespace but
before the test begins running. The `setup` Procedure may take whatever actions required to prepare the testing Namespace for
the test to be run.
 
This might involve setting a Source's Mock Procedures (see below). This might also involve pulling data from the originating
Namespace into the Testing Namespace. By default, the Testing Namespace will contain a Node that connects back to the originating
Namespace. The Node's name is the name of the Testing Namespace. To pull all of the records of a given Type from the originating
Namespace to the testing Namespace, use the following skeleton code: 

```js
PROCEDURE setupProcedure()
var namespaceName = Context.nampesace()
SELECT * FROM <typeName> as instance PROCESSED BY name == namespaceName {
    INSERT <typeName>(instance)
}
```

## Defining a Test Suite
Test Suites are a way of collecting multiple Tests that test the same resource. By running the Test Suite, each of the Tests
defined within the Suite are run sequentially. A Test Suite run creates individual Test Reports for each Test
within the Suite, as well as a composite report for the whole Suite.


### Properties
 * **name** (String, _required_): Name of the Test Suite
 * **description** (String): Description of the Test Suite
 * **resource** (ResourceReference, _required_):  If the Test Suite is an Integration Test, then the resource associated with the Test Suite is a Project or Service.
   If the Test is a Unit Test, then it is the Procedure, Rule, or Service with a unitReference defined (ex: `/projects/myProject` or `/rules/MyRule`)
* **unitReference** (Object, _required for service unit tests_): For Service Unit Test Suites, this property is required to specify which piece of the Service is being tested. This is an Object
  with the format *{type: <unit type\>, name: <unit name\>}* where type is either *eventTypes* or *procedures* and the unit name is the name of the Event Type or Procedure being tested.
 * **tests** (Array of Strings, _required_): List of Test names that are run sequentially as part of the Suite 
 * **runPolicies** (Array of Objects): Array of run policy descriptors. Run Policies define a time interval for how frequently an automatic Test Suite run will be triggered.
 (See above for how to define a run policy descriptor).
 
 ![Test Suite](assets/img/tests/TestSuiteGeneral.png "Test Suite")
 
 ![Test Suite Tests](assets/img/tests/TestSuiteTests.png "Test Suite Tests")


When a Unit Test is defined on a Procedure or Rule, a Test Suite for that resource is automatically generated named _<resourceName\>_UnitTestSuite_. 
This Test Suite automatically contains all of the Unit Tests for that resource at run time. This allows the developer to execute the full 
Test Suite defined for that resource within the Rule or Procedure pane.

Another Test Suite is automatically generated named _<projectName\>_UnitTestSuite_. 
This Test Suite automatically contains all of the Unit Tests that test a Rule or Procedure in the Project.

## Source Mocking For Tests

Deterministic Source messages are critical to defining a repeatable Test that does not produce undesired side effects. 
When an Integration Test is deployed into a Testing Namespace, all of the Sources are automatically placed in Mock Mode.
This means that if the Test expects Source messages, mock Procedures must be defined on the Source. Otherwise, the Source
will not be able to produce any messages.

Please see the [External Source Reference Guide](sources/source.md#source-mocking) for more information about Mock Mode.

When running a Unit Test, Sources are not automatically set into Mock Mode so as to not disrupt the development Namespace where
the Unit Test is run. However, a developer may use the `Setup` and `Cleanup` Procedures in the Test definition to set 
their Sources into Mock Mode for Unit Tests.

Developers may use built-in Procedures to turn Mock Mode on and off. 
`Test.startSourceMocking(sourceName, mockQueryProcedure, mockPublishProcedure)` turns on Source Mocking for the source _sourceName_ and `Test.stopSourceMocking(sourceName)`  turns it off. For more information, please see the [VAIL Rule and Procedure Reference Guide](rules.md#source-mocking).

To Mock a source event use the procedure [`Test.sendMockSourceEvent()`](rules.md#test).

For example, assuming a source named `MySource` receiving XML data, the following VAIL procedure would publish a Mocked message as produced by `MySource`:

```
PROCEDURE mockSourceEvent()
var xml = "<message><city state=\"ca\">oakland</city></message>"
var message = parseXml(xml)
Test.sendMockSourceEvent("MySource", message)
```

## Shortcuts to Building Tests in the IDE

### Procedure Pane
By selecting the `Create Unit Test` button when Executing a Procedure, a new Unit Test is created with a single input
and no outputs. The input includes the Procedure that was run, the parameters it was run with, and the return value 
that was returned. A new Test Pane opens and displays the newly created Test.

![Procedures Pane](assets/img/tests/CreateTestFromExecute.png "Procedure Pane create a test")

A new Test may also be created by clicking the `Create Test` button.
You will be prompted to set the parameters that the Procedure will be called with in the Test. Clicking `OK` will prompt you 
to name the Test. Then, a new Test will be created and open a new Test pane.

Existing Tests can be run within the Procedure pane by selecting the Test in the Execution dropdown menu and then clicking `Run`.  
 The `Test Suite`
 option in the Execution dropdown menu runs
the generated Test Suite which includes all of the Unit Tests for that Procedure.

![Procedures Pane](assets/img/tests/ProceduresPane.png "Procedures Pane run a test")


### Rule Pane

A new Test can be made in the Rule Pane by clicking the `Create Test` button.
 You will be prompted to specify the event
message for the Rule triggering event that drives the Unit Test. If the triggering condition for the Rule is an UPDATE or DELETE event, then
the developer also specifies the WHERE clause for that event (ex: `name == “ABC”`).

![Rules Pane](assets/img/tests/CreateTestFromRule.png "Rules Pane run a test")

When “OK” is clicked, a new Unit Test is created with a single input and no outputs. The input includes the Rule 
triggering event that was described. The developer may then specify the expected output events that the Rule may produce.

Existing Tests can be run within the Rule pane by selecting them in the Execution dropdown menu and clicking `Run`.  
  The ` Test Suite` option
 in the Execution dropdown menu runs
the generated Test Suite which includes all of the Unit Tests for that Rule.

![Rules Pane](assets/img/tests/RulesPane.png "Rules Pane run a test")

### Autopsies

Clicking on the `Create Test` button in the upper-right hand corner of an Autopsy creates a new Unit Test with a single
input and no outputs.  

If the Autopsy was of a **Rule** then the input includes the Rule triggering event. For an UPDATE or DELETE
Rule, the user must later edit the Test Input in the new Test Pane to include the WHEN clause qualifier.

If the Autopsy was
of a **Procedure**, the input includes the Procedure that was run, the parameters it was run with, and the return value.
A new Test Pane opens and displays the newly created Test.

### Error Pane
Clicking on the `Create Test` button in the upper-right hand corner creates a new Unit Test. A new Test with a single input 
is created. 

If the Error was from a **Rule** then the input includes the Rule triggering event. For an UPDATE or DELETE Rule, the user must later edit the Test Input
in the new Test Pane to include the WHEN clause qualifier. 

If the Error was
from a **Procedure**, the input includes the Procedure that was run and the parameters it was run with. 

The developer may then select either `Create Test` or `Create Test and Include Error`. If `Create Test` 
is selected, the Test includes the single input and no outputs. However, if `Create Test and Include Error`
is selected, then the Test includes the single input and the error produced is added as an expected output for the Test.

![Error Pane](assets/img/tests/ErrorsPane.png "ErrorsPane")

### App Pane
Clicking on the `Create Test` button in the upper-right hand corner creates a new Integration Test skeleton. The test will have 
an input event for each App triggering event. The test will contain one output for each outbound App event:

- SaveToType
- PublishToTopic
- PublishToSource
- StartCollaboration

The developer may then provide a name and description for the Test and a new Test will be opened. Note that none of the
auto-generated inputs or outputs will have event objects set. It is expected the user will fill in the details before
running the test.

![Error Pane](assets/img/tests/ErrorsPane.png "ErrorsPane")


## Running a Test

### Running a Test in the IDE

Tests can be run in The IDE by clicking `Run Test` in the `Test` pane or clicking  `Run Test` in the actions menu of the
`Tests` pane. Test Suites can be run in the IDE by clicking `Run Test` in the `Test Suite` pane or clicking  `Run Test` in the actions menu of the
`Test Suites` pane. Unit Tests and Unit Test Suites  may also be run in the Procedures and Rule pane (see above) for the resource they test.

![Test Definition](assets/img/tests/VantiqTestGeneral.png "Test General")


### Running a Test through the REST Interface

Test execution is triggered by performing an insert operation on the system resource `system.testreports`. To begin a Test run of a Unit or Integration Test, 
INSERT into the Type `system.testreports` with the `name` property set to the name of the Test. For example,
to run a Test called `MyProcedureTest`:

```
Method: POST
URL: /api/v1/resources/system.testreports
Body: { "name": "MyProcedureTest"}
```

To run a Unit or Integration Test Suite set the `name` property to the name of the first Test in the Test Suite
and set the `testSuiteName` property to the name of the Test Suite. For example, to run a Test Suite called
`MyTestSuite` which consists of `Test1`, `Test2`, and `Test3`:

```
Method: POST
URL: /api/v1/resources/system.testreports
Body: { "name": "Test1", "testSuiteName": "MyTestSuite"}
```

Posting the `testSuiteName` with any other test name other than the first Test in the Test Suite will cause the Test Suite
to run in the specified order starting at the name specified.

To run an auto-generated resource or project Test Suite, post an object that contains only the testSuiteName and no Test Name.
The server will automatically select all of the Tests associated with the automatically generated Test Suite at run time.

```
Method: POST
URL: /api/v1/resources/system.testreports
Body: { "name": null, "testSuiteName": "myRule__UnitTestSuite"}
```
