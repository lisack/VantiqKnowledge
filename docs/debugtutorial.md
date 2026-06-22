# Autopsy Debugger Tutorial
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Untriggered](../assets/img/autopsy/Untriggered.png "Untriggered")

## Purpose

To demonstrate how running application components can be traced and autopsied to ensure intended functionality

## Objectives

Developers by the end of this tutorial will be able to:

* Selectively track rules and examine how they ran
* Debug and modify rules as needed
* Turn off tracing and clear autopsies no longer needed

## Tutorial Overview
This tutorial guides a developer through an overview of the capabilities of the "Autopsy Debugger". This is a tool in the [Vantiq IDE](../../../..) that allows you to examine the execution of a Rule in detail after it has completed. It requires the creation of a Type and Rule to put the debugger through its paces.

All lessons assume the developer has a working knowledge of the [Vantiq IDE](../../../..). It is recommended that a new developer completes the lessons in the [Introductory Tutorial](tutorial.md) before starting the lessons in this tutorial. 

>Note: if needed, you can import a finished version of this project using the _Projects -> Import_ menu item.  Just select _Tutorials_ for Import Type, then select _Debugging_ from the second drop-down, then click _Import_.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

## 1: Creating a Debugging Project
The first task in learning about Vantiq debugging is to create a project in the Vantiq IDE to assemble all the debugging components.

Use the **Projects** button, select **New Project**, which displays the New Project Wizard. Either create a new Namespace (recommended) or add a new project to the current Namespace, select **Empty** as the Project type, and title the project "Debugging":

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![DebugProject](../assets/img/intro/EMProject.png "Create Debugging Project")

The rest of the lessons take place inside this Project.

## 2: Creating a Type and Rule
In order to demonstrate the capabilities of the Autopsy Debugger we must first to create a dummy Type and dummy Rule to provide a predictable environment. Neither of these perform any actual function; they will just help you understand the debugger operations.

You will need to create a Type called _TutorialExampleType_. (This procedure is explained in the Introductory Tutorial as [2: Creating Data Types](tutorial.md#2-creating-data-types).) The Type has only two Integer properties, "age" and "weight":

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SourcesTab](../assets/img/autopsy/Type.png "Type")

Next you will need to create a Rule called TutorialExampleRule. Use the **Add / Advanced** menu item to select **Rule...**:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![AddRule](../assets/img/source/AddRule.png "Add Rule")

Use the **New Rule** button to create your sample rule. You can just copy and paste this VAIL language text into the Rule editor:

```js
RULE TutorialExampleRule
WHERE (t.value.age > 5)
WHEN EVENT OCCURS ON "/types/TutorialExampleType/insert" AS t

var ageStatus = "Unknown"

if (t.value.age >= 21) {
   ageStatus = "Adult"
} else {
   ageStatus = "Child"
}

SELECT TutorialExampleType AS allPeople

var total = 0

for (person IN allPeople) {
   total = total + person.weight
}

var averageWeight = total / allPeople.size()
```
Be sure to save your new Rule.

## 3: Turn on Tracing
In production, you want your rules and procedures to execute with minimum overhead. Normally when a rule or procedure executes, it runs as quickly as possible and leaves no traces behind (other than its expected actions and side-effects, of course).

In order to debug a rule, you must turn on "Tracing" for that rule. When Tracing is active for a rule, it causes that rule to create "Rule Snapshots" as it executes. (These correspond to instances of the ArsRuleSnapshot system type.) In general, there is one snapshot generated for every "statement" executed in your Rule. Since Rules can be complicated (containing loops and IF/THEN logic) there are usually many more snapshots produced than the rule has statements. (A FOR loop, for example, could produce thousands.)

After the Rule has completed execution, the Autopsy Debugger will process the snapshots that were produced when the Rule executed, allowing you to investigate the details (after the fact) of the Rule's operation. In this way you can check it for logical flaws and fix possible problems when it doesn't act the way you expect. Note that Procedures can be debugged in the same way.

Because the overhead of producing the snapshots can be substantial, you should *not* leave Tracing on during normal production operation. You should only turn it on to capture one or two autopsies for the target rule or procedure, and then turn it off again. Once you have captured an autopsy, it can be examined at your leisure without impacting normal system performance.

Turning Tracing on and off for a rule (or procedure) is simple. Open the rule or procedure in the IDE, then check the checkbox called **Tracing** so it looks like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SourcesTab](../assets/img/autopsy/Enabled.png "Rule Enabled")

Then click **Save Changes** icon button (the little "floppy disk" icon at the top, right of the _Rule: TutorialExampleRule_ pane). Once enabled, Tracing will stay on for that rule until you edit the rule and turn it off again.

Leave Tracing on now, since we are next going to generate some Rule executions.

## 4: Capture Some Rule Executions

The simple dummy rule we created watches for records to be inserted into the _TutorialExampleType_. This makes it easy to cause the Rule to execute; we simply insert some data into the Type. The IDE provides an easy way to do this manually. Use the **Show** button to select **Add Record...**, then use the **Type** pull-down menu to create two _TutorialExampleType_ records.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![AddRecord](../assets/img/autopsy/InsertObject.png "Add Record")

For the purposes of this tutorial we need to insert two _TutorialExampleType_ records. First fill in the fields like this and click the **Add New Record** button:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![AddRecord1](../assets/img/autopsy/InsertObject1.png "Add Record 1")

Now create a second one with these values:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![AddRecord2](../assets/img/autopsy/InsertObject2.png "Add Record 2")

To verify that the two records have been saved, use the **Show** button to select **Find Records** to display the Find Records query pane:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![FindRecords](../assets/img/autopsy/FindRecords.png "Find Records")

Select _TutorialExampleType_ from the **Type** menu, then use the **Run Query** button to display the list of _TutorialExampleType_ records:

![FindRecordsResults](../assets/img/autopsy/FindRecordsResults.png "Record List")

Since we inserted two _TutorialExampleType_ records, we expect that two Autopsies were created. Let's go see what they look like.

## 5: The Captured Autopsies
Use the **Test** button to select **Autopsies**, then use the **Run Query** button:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![AutopsiesQuery](../assets/img/autopsy/AutopsiesQuery.png "Autopsies Query")

The "Autopsy Query Results" pane will display like this:

![AutopsiesResults](../assets/img/autopsy/AutopsiesResults.png "Autopsies") 

You should see two Autopsies for the _TutorialExampleRule_ in the list, created by the inserts we did in Lesson 4. They are displayed in reverse time order, so the ones that executed most recently are at the top. The "Start Time" column tells you when that particular Rule execution started.

Notice that in the "Triggered" column they look different. Why is that? Let's find out.

You can click in the "Name" column of this table to open the Autopsy for a particular Rule execution; click the older of the two (the one that contains the little red "Not" icon in the "Triggered" column). This should cause the Autopsy Debugger to open, letting us see what happened during this execution.


## 6: Untriggered Rules
Here is what you should be seeing:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Untriggered](../assets/img/autopsy/Untriggered.png "Untriggered")

At the top of the page is general information about this particular execution of _TutorialExampleRule_. Of most interest is the line in red which says, "The WHERE clause prevented the WHEN from triggering the rule." That's why the two rule executions were different; although this Rule executed it didn't actually "trigger". (That is, it didn't actually run the Rule.) Let's look further to see why.

The page is divided into two columns; in the left hand column is the text of the rule itself. On the right (called "the display area") is a tree that displays the current values of various variables, objects and lists being manipulated by the Rule. 

Note that the "WHEN" for this Rule is preceded by a WHERE clause that says, "the rule should only trigger if the inserted object had an 'age' field greater than 5". Did it?

Look at the top item in the display area; it tells us the current contents of the object referenced by the "t" correlation variable. If you open it we can see that the "t.value.age" property was "4" so in fact this rule did exactly what we asked it to do.

That's all this autopsy has to tell us; the Rule didn't fully trigger because the WHERE clause told it not to.

Now return to the "Autopsy Query Results" list by clicking "back" arrow in the upper-left hand corner of the window.

**A little digression for advanced users**

You can skip this section if you don't care about some subtle points concerning how rules get triggered.

We **could** have described the triggering condition for the rule like this instead, specifying the WHERE as part of the WHEN clause:

```js
WHEN EVENT OCCURS ON "/types/TutorialExampleType/insert" AS t WHERE (t.value.age > 5)
```

When the WHERE clause is attached to the WHEN like this, it means that the "filtering" happens much earlier, such that this rule never even starts at all. If we did it that way there would have been no snapshot generated unless _t.value.age_ was greater than 5. This would be more efficient and generate less "noise". For this tutorial we did it a different way:

```js
WHERE (t.value.age > 5)
WHEN EVENT OCCURS ON "/types/TutorialExampleType/insert" AS t
```

This distinction becomes important when using advanced "compound condition" rules in which the WHEN clauses can get much more complex; for the purposes of this tutorial we wanted to force a "non-triggered" snapshot.


## 7: Debugging a Rule
Once you have returned to the "Autopsy Query Results" list, we can select the other autopsy, which (as we can tell by the green check in the "Triggered" column) actually did something. The debugger display for this Rule execution should look more interesting:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Triggered](../assets/img/autopsy/Step1.png "Triggered")

There is more to see now. First notice that there are 4 buttons at the top of the display; and there is the legend "Step 1 of 12". This tells us that this Rule execution produced 12 Snapshots, each representing the execution of a statement in the Rule.

Because this is an "autopsy" debugger we already know the entire execution history of the Rule. That means we can step forwards *and backwards* to examine the Rule execution. We can fast-forward all the way to the end (by clicking the "End" button) and then step backwards or click "Start" and "rewind" all the way to the initial state. This ability can be helpful when trying to understand what your rule did (and where it may have gone wrong).

The text of your rule is displayed on the left-hand side of the window. The statements which are executable (and not just part of the statement syntax, like "ELSE" and "END") have two little icons to their left:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Statement](../assets/img/autopsy/statement1.png "Statement 1")

The rightwards-pointing arrow tells us where we are in the execution flow. The statement that is about to be executed (but hasn't executed yet) has a green arrow, and the background of the rule is pale green. For other rules, the arrow is grey and the background is white. (Note that just because a statement is executable does not mean it will have an arrow; arrows only appear on statements which were actually "visited" during the captured execution.)

The greyed-out star represents a breakpoint; you can toggle it to indicate that the debugger should stop at that point. (This is irrelevant if you are just "single-stepping" through the Rule, but if you click "Start" or "End" these breakpoints will take effect.)

This first statement sets the value of a variable called "ageStatus" to "Unknown". But it hasn't executed yet; you will notice that it doesn't appear in the display area because the variable hasn't been assigned a value yet. If you click the "Forward" button at the top of the display you should see several things happen.

* The legend will change to "Step 2 of 12"
* The "current statement" pointer will move to the next statement ("IF (t.age >= 21) THEN")
* The "ageStatus" will now appear in the display area with a value of "Unknown", as expected

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Statement](../assets/img/autopsy/Step2.png "Step 2")

Remember that you can always click the "Step Back" button and you will see things go back to where you started. Then hit "Step Forward" again, so the current statement point is on the "IF" statement.

What should happen next? Since _t.value.age_ is "35" (as we can see from the "t" section of the display area) we would expect the expression to be "true". Click "Step Forward" again and let's see.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Statement](../assets/img/autopsy/Step3.png "Step 3")


Note that we have stepped into the first clause of the "IF" statement since the expression was true, as expected.

Okay, let's jump ahead. Scroll down to line 17 to find the FOR statement and toggle its breakpoint icon so it looks like this:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ForLoop](../assets/img/autopsy/ForLoop.png "For Loop")

Now click the "End" button at the top of the page. This would normally let the rule run all the way to the "Execution Completed" point at the bottom, but because we set a breakpoint it will stop at the "FOR" (Step 6).

A few statements before, the Rule loaded all the instances of _TutorialExampleType_ into the "allPeople" list using a SELECT. You should now be able to see those in the display area on the right:


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Statement](../assets/img/autopsy/Step6.png "Step 6")


We have clicked the "allPeople" variable to open it and reveal the contents. Notice that it says that "allPeople" is an array with 2 elements, and each element can be opened to see inside,

Now we can iterate through these two _TutorialExampleType_ instances in the FOR loop using the "person" variable.

Since the "person" variable only has meaning inside the FOR loop it doesn't appear in the display area until we step in. Do that now by clicking once on the "Step Forward" button and you will see the value of _person.weight_ change as you step through the loop. As you keep clicking the "Step Forward" button you will eventually exit the FOR loop.

Of course, at any time you can click the "End" button and zip all the way to the "Execution Completed" point. This means the Rule has completed executing all statements and is about to exit.

## 8: Testing the Rule

Congratulations! You've just learned how to debug in Vantiq. However, there is an important piece missing.
How can you ensure your Rule works, and will always work as you expect?

Learn how to test the Rule you just built by clicking here: [Testing the Debug Tutorial](testdebugtutorial.md)

## 9: Cleaning up Autopsies
In the process of debugging a Rule, you may capture many execution instances. As you work with more than one rule, the list can get rather long. After you are done with a debugging session you will probably want to clean up the ones you no longer need.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Autopsies](../assets/img/autopsy/Autopsies.png "Autopsies")

You can delete individual autopsies by checking the checkbox to the left of the autopsy name, then using the **Delete** icon button (small trashcan at the top, right of the pane). This can get tedious if you have more than a handful to delete, so a more efficient way has been provided.
You can delete *all* these at once by using the **Delete All** button in the "Autopsies Query" pane, using the **Name Containing** and **Filter** fields to select exactly which autopsy records to delete.

Note: there is also an *Errors* pane in the IDE that shows errors that have occurred in rules, procedures, or sources run by the system. These errors are collected and saved whether Tracing is enabled or not. To retrieve existing errors, use the **Test** button to select **Errors**, then use the "Errors Query" pane to select which errors to display:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Errors](../assets/img/autopsy/Errors.png "Errors Query")

## Conclusion

Developers creating applications should now be able to effortlessly:

* Trace through parts of their code step-by-step to see how rules and procedures are functioning with sample input
* Create tests from autopsies of rules and procedures
* Clean up the output they no longer need 
