# Testing the Debugging Tutorial

## Prerequisites
This tutorial assumes you have completed the first 7 steps of the [Debugging Tutorial](debugtutorial.md). 
Please complete the tutorial if you have not done so already, then return to this page in step 8 to learn how to test it.

## Testing The Triggered Rule

Now that we have investigated the Rule and understand it better, it is time to write a few unit tests.

A Vantiq Test is driven by a
sequence of ordered input events and a expects a collection output events. Because Rules do not have return values, the test
requires an output event in order to ensure correctness.
Adding the PUBLISH to the end of the Rule creates the output event necessary to verify that the ageStatus and averageWeight were computed correctly.  

We want to create a Test that 

* INSERTS into the TutorialExampleType
* expects a PUBLISH to "/people/results" with correct ageStatus and averageWeight

Navigate to the `TutorialExampleRule` Rule.  
Edit the Rule and add the following code snippet to the last line at the bottom of the Rule:

```
PUBLISH {ageStatus: ageStatus, averageWeight: averageWeight} TO TOPIC "/people/results"
```

The PUBLISH we added in the Rule will allow us to use that event as an Output event so that we can test and ensure that
the Rule computed the right values.

Navigate back to the Autopsy pane for your successfully triggered Rule and click **Create Test**.

![TestSuiteGeneral](../assets/img/testdebugtutorial/createTestFromAutopsy.png "Test Suite General").

Type `TutorialExampleRule0` as the testName and click OK.

A new **Test** pane will open with all of the General properties on the test already set.
 
![DebugTest](../assets/img/testdebugtutorial/DebugTestGeneral.png "Debug Test General Tab")

Navigate to the **Inputs**
tab and verify that there is one input in the Inputs list.

![DebugTestInputsList](../assets/img/testdebugtutorial/DebugTestInputs.png "Debug Test Inputs Tab")

The Test will expect 1 output: The PUBLISH to the `/people/results` Topic performed by the Rule.

Navigate to the **Outputs** tab and click the **Add Output** Button. 

The `TutorialExampleType` Rule performs a PUBLISH on the `/people/results` that includes the `ageStatus` of the `TutorialExampleType`
and the `averageWeight` of all `TutorialExampleType` instances. The Test will pre-populate the Namespace with 3 instances of the
`TutorialExampleType` (see below) so that the averageWeight is calculated over multiple instances of the Type.

Set *topics* as the Resource, */people/results* as the ResourceId.  
Click on the **Click to Edit** button to open the Event Object Editor and create a JSON Object with the following contents:

```
{
   "ageStatus": "Adult",
   "averageWeight": 126.25
}
```

![DebugTestFirstOutputPopup](../assets/img/testdebugtutorial/DebugTestOutput1.png "First output event")

Click **OK** to close the Event Object Editor.

As mentioned above, the test will pre-populate the Namespace with`TutorialExampleType` instances.

Use the **Add** button in the IDE Navigation Bar to select **Procedures** and then click the **New Procedure** button to create a new Procedure.

Name the Procedure `insertTutorialExampleType`. This Procedure is the Test **Setup** Procedure. The Procedure INSERTS 
3 instances of the `TutorialExampleType` Type.

Copy and paste the following into the new Procedure Pane:

```
PROCEDURE insertTutorialExampleType()
DELETE TutorialExampleType WHERE weight < 300
INSERT TutorialExampleType(age: 10, weight: 60)
INSERT TutorialExampleType(age: 20, weight: 120)
INSERT TutorialExampleType(age: 30, weight: 150)
```

Click **Save** to save the Procedure.

Use the **Add** button again to select **Procedures** and then click the **New Procedure** button to create a new Procedure.

Name the Procedure `deleteTutorialExampleType`. This Procedure is the **Cleanup** Procedure. The Procedure DELETEs
all instances of the `TutorialExampleType` that were INSERTED.
  
Copy and paste the following into the new Procedure Pane:

```
PROCEDURE deleteTutorialExampleType()
DELETE TutorialExampleType WHERE weight < 300
```

Click **Save** to save the Procedure.

The Test requires **Setup** and **Cleanup** Procedures. Navigate back to the **Test** pane in which we were defining the 
`TutorialExampleRule0` test and click on the **General** tab.

Select **insertTutorialExampleType** as the **Setup Procedure** and **deleteTutorialExampleType** as the **Cleanup** Procedure. **Save** the
Test.

![SetupAndCleanupSourceProcs](../assets/img/testdebugtutorial/DebugTestSetupCleanup1.png "Setup and Cleanup Procedures")

Click the **Show Test History** button to watch the test run in real time when the **Run Test** button is clicked next.

![ShowHistory](../assets/img/testdebugtutorial/ShowHistory.png "ShowHistory")

Navigate back to the `TutorialExampleRule` Rule. Select the new test `TutorialExampleRule0` from the Execute droplist and then
click **Run**. 

Wait for the Test History List to show one entry with a green check showing a successful test run.

![SuccessTest1](../assets/img/testdebugtutorial/SuccessTest1.png "SuccessTest1")


## Testing The Untriggered Rule

We want to now create a second Test that tests the case where the INSERT on the `TutorialExampleType` Type has *age < 5*
which should not trigger the Rule.

Navigate back to the Autopsy pane for your untriggered Rule and click **Create Test**.

![CreateTest](../assets/img/testdebugtutorial/createTestFromAutopsy.png "Debug Test General Tab")

Name the test `TutorialExampleRule1` and click OK.

A new **Test** pane opens with all of the General properties on the test already set.   
Change the *Timeout Time* for the test to **10 seconds**.
 
 ![DebugTest](../assets/img/testdebugtutorial/DebugTestGeneral2.png "Debug Test General Tab")

 Navigate to the **Inputs** tab and verify that there is one input in the Inputs list.

![DebugTestInputsList](../assets/img/testdebugtutorial/DebugTestInputs2.png "Debug Test Inputs Tab")

Navigate to the Outputs Tab and click **Add Output**.

Set *topics* as the Resource, */people/results* as the ResourceId.
Because the Rule should not be triggered, there should be no PUBLISHES to the */people/results* Topic.
Set the Validation Method to *Missing*. This means that the Test expects **no PUBLISHES** on the */people/results* Topic, and 
if one is received within the *Timeout Time* period, the Test fails.

![DebugTestFirstOutputPopup](../assets/img/testdebugtutorial/DebugTestOutput2.png "First output event")

Navigate to the **General** tab.

![SetupAndCleanupSourceProcs](../assets/img/testdebugtutorial/DebugTestSetupCleanup2.png "Setup and Cleanup Procedures")

Because the Rule is not triggered and the averageWeight is not calculated, a Setup Procedure is not required.
However, this Test performs an INSERT on the `TutorialExampleType` Type which should be cleaned up. 
Select **deleteTutorialExampleType** as the **Cleanup** Procedure. **Save** the Test.

Click on the Show History button to watch the test run in real time.

![SHowHistory](../assets/img/testdebugtutorial/ShowHistory.png "SHowHistory")

Navigate back to the `TutorialExampleRule` Rule. Select the new test `TutorialExampleRule1` from the Execute droplist and then
click **Run**. 

Wait for the Test History List to show one entry with a green check showing a successful test run.

![SuccessTest2](../assets/img/testdebugtutorial/SuccessTest2.png "SuccessTest2")

## Running the Test Suite

Navigate to the **Test Suite List** by selecting **Test Suites** under the **Test** tab. There should be one entry called
`TutorialExampleRule_UnitTestSuite`. This is the auto-generated Test Suite for all Unit Tests that test the `TutorialExampleRule`.
This Test Suite will always keep itself up to date with all the Unit Tests that test this Rule.

![TestSuiteList](../assets/img/testdebugtutorial/TestSuiteList.png "Test Suite List")

Click on the Test Suite to open up the Test Suite Pane.

![TestSuiteGeneral](../assets/img/testdebugtutorial/TestSuiteGeneral.png "Test Suite General")

Navigate to the Tests tab to see the list of all the Tests for this Rule. You should see both Tests that you defined.

![TestSuiteTests](../assets/img/testdebugtutorial/TestSuiteTests.png "Test Suite Tests")


Click **Run Test** to run the Test Suite.

Click **Show Test History** and wait until a green check appears showing that the Test Suite has completed successfully.
This should take a little over 10 seconds since this is the timeout period.

![TestSuiteReportList](../assets/img/testdebugtutorial/TestSuiteReportList.png "Test Suite Report List")

Click on the report to see the breakdown of each test within the Test Suite. 

![TestSuiteReport](../assets/img/testdebugtutorial/TestSuiteReport.png "Test Suite Report")

## Conclusion

Developers creating applications should now be able to effortlessly:

* Trace through parts of their code step-by-step to see how rules and procedures are functioning with sample input
* Create tests from autopsies of rules and procedures
* Create setup and cleanup Procedures for Tests
* Run a Test Suite
