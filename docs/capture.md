# Captures

## Introduction

The goal of any application testing tool is to verify that an application works as expected,
and continues to work correctly over time. The more closely a test can mimic 
real scenarios, the more useful the test becomes. However, real data is complex, and tests that accurately reflect real world data
can be arduous to build. 

Capture simplifies this process, making test writing quick and simple.
Captures allow users to record the events that occur in a Namespace. The Captured events can be
exported to an Integration Tests with one click. This no code approach streamlines the creation process for high quality tests.

Captures may also be exported to Event Generators so that the events can be replayed again in the future.
 
## Defining a Capture

Captures can record all events in the Namespace, or a subset of events specified by the user.

Captures are defined by the following properties:

- **captureId** (String): The unique identifier for the Capture. This is automatically generated when the
Capture begins.
- **startTime** (DateTime): The time the capture began, represented as an ISO DateTime. This is automatically generated when the
Capture begins.
- **endTime** (DateTime):  The time the capture ended, represented as an ISO DateTime. This is automatically generated when the
Capture ends.
- **resources** (List of Strings): List of event paths describing which events should be captured.
- **status** (String): Either *active* if Capture is enabled, or *finished* if the Capture has completed.

As events are captured, they are written as instances of the *ArsCapturedEvent* type.  
An *ArsCapturedEvent* is defined by the following properties:

- **captureId** (String): The unique identifier for the Capture. This will be automatically set to the *captureId* of the 
 active Capture.
- **resource** (String): The event path for the event containing the *resource*, *resourceId*, and *operation*.
- **timestamp** (DateTime): Time at which the event occurred, represented as an ISO DateTime string.
- **event** (Object): Contents of the event message.

**Note**: Vantiq will buffer inserts of *ArsCapturedEvents* during a Capture. Do not expect to see a new *ArsCapturedEvent*
immediately after the event occurred. All events will be written to the database by the time the Capture is complete.

## Start a Capture

A Capture is started by inserting a new instance of the *system.captures* type. The **resources** list is the only property
 that must be specified by the user. All other properties are automatically set at runtime.

The **resources** property of the Capture instance specifies which events should be recorded by the Capture.

It is important to note that a Capture will only remain active for **5 minutes**. After 5 minutes, Vantiq automatically terminates
the Capture. This is to prevent the number of events recorded in one Capture from growing too large, or the
scenario in which a user "forgets" to disable Capture. 

In the IDE, when a Capture is active, a timer and stop icon will appear in the toolbar. This serves as a reminder that Capture
is *active*. The user can see how long
Capture has been enabled, and easily stop Capturing events without having to open a pane.

![Stop Capture List](assets/img/captures/StopCaptureMenu.png "Stop Capture Menu")

Capture may either be *active* or *off* in a Namespace. Attempting to begin a new Capture while one is still *active*
will result in an *io.vantiq.concurrent.captures* error.

### Global Capture

If the **resources** list is empty, the Capture will default to recording all **type**, **topic**, and **source**
events in the Namespace. 

To begin a global capture, insert a new instance of `system.captures` with an empty resource list.

```
Method: POST
URL: /api/v1/resources/captures
Body: { "resources": []}
```

Vantiq will return the new `system.captures` object. The object will contain the **startTime** property
and the **captureId** to uniquely identify the Capture.

To begin a global capture in the IDE, click the **Global Capture** button on the **Captures** pane.

![Global](assets/img/captures/GlobalCapture.png "Global Capture")

### Targeted Capture

To begin a Targeted Capture, users must specify the **resources** list.
Each entry in the **resources** list must be a valid event path in the format: */<resource\>/<resourceId\>/<operation\>*.
The resource may be set to either *types*, *topics*, or *sources*.
Event paths are hierarchical, therefore specifying the resourceId, and operation is not required.
If only the *resource* is specified, all events on the resource will be Captured.  If the *resource* and *resourceId* are specified,
 but not the operation, all operations on that resourceId will be Captured. 

The following are several event paths examples and their scope:

- */types*: All type operations
- */types/myType*: All INSERT, UPDATE, DELETE operations on *myType*
- */types/myType/insert*: All INSERT operations on *myType*
- */topics*: All topic events
- */topics/machines/machine2*: All topic events on the topic */machines/machine2*
- */sources*: All source operations
- */sources/mqttSrc*: All events on the Source *mqttSrc*

Duplicative resources are not allowed within a Capture. Duplicate resources are two event paths that apply to the 
same event. For example */types* and */types/myType* are duplicates because they would both apply to *myType* events.
Similarly */types/myType* and */types/myType/insert* are duplicates because both apply to *myType* insert events.
*/types/myType* and */types/myType2* are not considered duplicates because they Capture distinct, non-overlapping, events.

Targeted captures are recommended over Global captures. They ensure that only the desired events are captured, reducing the 
unnecessary noise as well as performance load of the capture. 

To begin a Targeted capture, insert a new instance of `system.captures` setting the **resource** list to the list of desired
events.

```
Method: POST
URL: /api/v1/resources/captures
Body: { "resources": [<eventPath>, <eventPath>,...]}
```

Vantiq will return the new `system.captures` object. The object will contain the **startTime** property
and the **captureId** to uniquely identify the Capture.

To begin a Targeted capture in the IDE, click the **Targeted Capture** button on the **Captures** pane. 

![Global](assets/img/captures/GlobalCapture.png "Global Capture")

Create a list of event paths and click **Start Capture**.

![Custom Capture List](assets/img/captures/CustomCapture.png "Targeted Capture")

## Stop Capture

To terminate an active Capture, the **status** property of the *captures* instance must be updated from *active*
to *finished*. 

Update *captures* using the *captureId* to uniquely identify the instance.

```
Method: PUT
URL: /api/v1/resources/captures/<captureId>
Body: { "status": "finished"}
```

Stopping a capture will set the **endTime** property of the *captures* instance to the current time and update the **status** to *finished*.
Once the status of a *captures* instance has been updated from *active* to *finished*, the Capture is considered complete
and cannot be re-activated.

To stop a Capture in the IDE, click the **Stop Capture** on the Capture pane of the currently active Capture. 

![Stop Capture List](assets/img/captures/StopCapturePane.png "Stop Capture")

The active Capture may also be stopped by clicking the **Stop Icon** in the toolbar. 

![Stop Capture List](assets/img/captures/StopCaptureMenu.png "Stop Capture Menu")

## Exporting a Capture

Captured events from a completed Capture may be exported to a Test or an Event Generator.
The timing between events is preserved when exporting the Capture.

When exporting a Capture, the user may apply transformations to the Captured events.
This allows users to export the same Captured data into several Tests (or Event Generators), slightly tweaking the data
to produce different scenarios without having to create new Captures.

![Completed](assets/img/captures/CompletedCapture.png "Completed Capture")

### Export Capture to a Test

To create a Test from a Capture, insert a new Test with the following properties:

- **name** (String) *required*: Name of the test to create
- **projectName** (String) *required*: Name of the project. This will become the test resource.
- **capturedInputs** (List of ArsCapturedEvents) *required*: ArsCapturedEvent instances that will be translated into test inputs
- **capturedOutputs** (List of ArsCapturedEvents) *required*: ArsCapturedEvent instances that will be translated into test outputs
- **inputTransformations** (Object) *required*: Transformations to be applied to the Captured event inputs
- **outputTransformations** (Object) *required*: Transformations to be applied to the Captured event outputs

As an example, let's say a Capture recorded one insert on *intType*, one publish to */MyTopic* and one message on *mySource*:

```json
[
    {
        "resource": "/types/intType/insert/5f90beeb90dbd12bf2bb51af",
        "captureId": "1330f103-13f2-11eb-a966-3a525d81d3bc",
        "event": {
            "value": 123,
            "name": "ABC"
        },
           "timestamp": "2020-10-21T23:06:19.510Z"
    },
    {
        "resource": "/topics/MyTopic/publish",
        "captureId": "1330f103-13f2-11eb-a966-3a525d81d3bc",
        "event": {
            "obj": {
                "value": 123,
                "name": "ABC"
            }
       },
       "timestamp": "2020-10-21T23:06:48.811Z"
    },
    {
        "resource": "/sources/mySource/receive",
        "captureId": "1330f103-13f2-11eb-a966-3a525d81d3bc",
        "event": {
            "numList": [1, 2, 3]
        },
        "timestamp": "2020-10-21T23:06:48.817Z"
    }
]
```

We want to create a test named **test1** for **myProject** that uses the insert on *intType* as a test input, and expects 
the publish to */MyTopic* and source message from *mySource* as outputs. We also would like to specify transformations on 
the event objects.
 
Input and Output transformations are applied on a per resource level. **inputTransformations** and **outputTransformations**
are Objects in which the key is the ResourceReference of the resource whose events should be transformed, and the value
is a nested object describing the transformations to each property within the resource. Each key in the nested transformation
object is the name of the property in the resource that the transformation should apply to. 
Each value in the nested transformation object is a VAIL expression defining the transformation.

The transformation will first copy the event exactly it was captured, and then modify the properties specified by the 
transformation. Any properties not specified by the transformation will remain unchanged in the event object.
 
For example, to create a transformation on all *intType* events that multiplies the *value* property by 10, and sets
the name property to lowercase, the `inputTransformations`  would be: 
 
```json
{
    "/types/intType": {
        "value": "event.value * 10",
        "name": "event.name.toLowerCase()"
    }
}
```

We want to apply the same transformation to the the */MyTopic* event in the outputs. 
 
```json
{
    "/topics/MyTopic": {
        "obj.value": "event.obj.value * 10",
        "obj.name": "event.obj.value.toLowerCase()"
    }
}
```

Note that in the case of the events on */MyTopic*, the *name* and *value* properties are nested under the *obj* property.
The transformation keys and values both reflect this in the transformation object, separating the nested properties with periods.

We want to multiply each value in *mySource* event's numList by 10. The `outputTransformations` would be: 

```json
{
    "/sources/mySource": {
        "numList": "[event.numList[0] * 10, event.numList[1] * 10, event.numList[2] * 10]"
    }
}
```

Putting this all together, to create the test described above with the transformations:

```json
 Method: POST
 URL: /api/v1/resources/tests
 Body: { 
    "name": "test1",
    "projectName": "myProject",
    "capturedInputs": [
        {
            "resource": "/types/intType/insert/5f90beeb90dbd12bf2bb51af",
            "captureId": "03aa2df1-13f2-11eb-a966-3a525d81d3bc",
            "event": {
                "value": 123,
                "name": "ABC"
            },
            "timestamp": "2020-10-21T23:06:19.510Z"
        }
    ],
    "capturedOutputs": [
        {
            "resource": "/topics/MyTopic/publish",
            "captureId": "1330f103-13f2-11eb-a966-3a525d81d3bc",
            "event": {
                "obj": {
                    "value": 123,
                    "name": "ABC"
                }
            },
            "timestamp": "2020-10-21T23:06:48.811Z"
        },
        {
            "resource": "/sources/mySource/receive",
            "captureId": "1330f103-13f2-11eb-a966-3a525d81d3bc",
            "event": {
                "numList": [1, 2, 3]
            },
            "timestamp": "2020-10-21T23:06:48.817Z"
        }
    ],
    "inputTransformations": {
        "/types/intType": {
            "value": "event.value * 10",
            "name": "event.name.toLowerCase()"
        }
    },
    "outputTransformations": {
        "/topics/MyTopic": {
            "obj.value": "event.obj.value * 10",
            "obj.name": "event.obj.value.toLowerCase()"
        },
        "/sources/mySource": {
            "numList": "[event.numList[0] * 10, event.numList[1] * 10, event.numList[2] * 10]"
        }
    } 
}
```
To remove a property from all events on a particular resource, set the property transformation to `"${REMOVE_KEY}"`.
The test will no longer include that property on all events generated on the selected resource. This is particularly useful
for removing id or timestamp properties from output objects so that they are not considered at output validation time.

To create a Test from a Capture in the IDE, click the **Create Test From Capture** button on the Capture Pane. Use the
checkboxes next to each event to mark whether the event should be included as a test input or output. Individual event messages
may be edited by clicking the **JSON** button.

![Completed](assets/img/captures/ExportToTest.png "Export Capture To Test")

To apply transformations, select either **Input Transformations** or **Output Transformations**. Use the droplist to select
a resource, and add transformations as desired.

![Completed](assets/img/captures/TestInputTransformation.png "TestInputTransformation")

### Export Capture to an Event Generator
 
To create an Event Generator from a Capture, insert a new Event Generator with the following properties:

- **name** (String) *required*: Name of the event generator to create
- **capturedEvents**  (List of ArsCapturedEvents) *required*: ArsCapturedEvent instances that will be translated into 
event descriptors for the Event Generator
- **transformationRules** (Object) *required*: Transformations to be applied to the Captured events

 Transformations are applied on a per resource level. **transformationRules** is an object
  in which the key is the ResourceReference of the resource whose events should be transformed, and the value
 is a nested object describing the transformations to each property within the resource. Each key in the nested transformation
 object is the name of the property in the resource. 
 Each value in the nested transformation object is a VAIL expression defining the transformation on that property.

The transformation will first copy the event exactly it was captured, and then modify the properties specified by the
transformation. Any properties not specified by the transformation will remain unchanged in the event object.

 Refer to the Captured data in the above section for the example below.
 
To create a transformation on all *intType* events that multiplies the *value* property by 10, and sets the name property to lowercase,
 the `transformationRules` would be: 
 
```json
{
    "/types/intType": {
        "value": "event.value * 10",
        "name": "event.name.toLowerCase()"
    }
}
```

To apply the same transformation to the events on */myTopic*, the `transformationRules` would be: 

```json
{
    "/topics/MyTopic": {
        "obj": {
            "value": "event.value * 10",
            "name":  "event.name.toLowerCase()"
        } 
    }
}
```

Note that in the case of the events on */MyTopic*, the *name* and *value* properties are nested under the *obj* property.
The transformation object is deeply nested by property. The VAIL expression that represents the transformation only refers
to the innermost property which is actually being transformed, rather than the fully qualified property. 

To apply a transformation to the events on */mySource* where each element in the values list is incremented by 10,
 the `transformationRules` is: 
 
```json
{
    "/sources/mySource": {
        "numList": "event.value + 10" 
    }
}
```

The transformation `event.value + 10` is applied to each element in the *numList* property. 
The transformation VAIL expression must refer `event.value` access the list element being transformed. 

Putting this all together, to create an Event Generator from the Captured events and applying all of the transformations described above.
 
```json
 Method: POST
 URL: /api/v1/resources/eventgenerators/
 Body: { 
    "name": "myGenerator",
    "capturedEvents": [
        {
            "resource": "/types/intType/insert/5f90beeb90dbd12bf2bb51af",
            "captureId": "03aa2df1-13f2-11eb-a966-3a525d81d3bc",
            "event": {
                "value": 123,
                "name": "ABC"
            },
            "timestamp": "2020-10-21T23:06:19.510Z"
        },
        {
            "resource": "/topics/MyTopic/publish",
            "captureId": "1330f103-13f2-11eb-a966-3a525d81d3bc",
            "event": {
                "obj": {
                    "value": 123,
                    "name": "ABC"
                }
            },
            "timestamp": "2020-10-21T23:06:48.811Z"
        },
        {
            "resource": "/sources/mySource/receive",
            "captureId": "1330f103-13f2-11eb-a966-3a525d81d3bc",
            "event": {
                "value": 123,
                "name": "ABC"
            },
            "timestamp": "2020-10-21T23:06:48.817Z"
        }
    ],
    "transformationRules": {
        "/types/intType": {
            "value": "event.value * 10",
            "name": "event.name.toLowerCase()"
        },
        "/topics/MyTopic": {
            "obj": {
                "value": "event.value * 10",
                "obj.name": "event.value.toLowerCase()"
            } 
        },
        "/sources/mySource": {
            "numList": "event.value + 10" 
        }
    } 
}
```

Instead of applying values known at Generation creation time, we support some runtime variations that provide dynamic information 
at Generator runtime. This is accomplished by setting the variation type on the property rather than a constant
transformed value. 

To replace a timestamp property with the current time at Generator runtime, set the property transformation to `"${NOW}"`.
This will set the variation type of the property to `NOW`, allowing the desired behavior.

```json
{
    "/resource/resourceId": {
        "property": "${NOW}"
    }
}
```

Similarly, to replace an id property with a new UUID at Generator runtime, set the property transformation to `"${UUID}"`
This will set the variation type of the property to `UUID`, allowing the desired behavior.

```json
{
    "/resource/resourceId": {
        "property": "${UUID}"
    }
}
```

To remove a property from all events on a particular resource, set the property transformation to `"${REMOVE_KEY}"`.
The event generator will no longer include that property on all events generated on the selected resource.

To create an Event Generator from a Capture in the IDE, click the **Create Generator From Capture** button on the Capture Pane. Use the
checkboxes next to each event to mark whether the event should be included in the Event Generator. Individual event messages
may be editted by clicking the **JSON** button.

![Completed](assets/img/captures/ExportToGenerator.png "Export Capture To Generator")

To apply transformations, select either **Add Transformations**. Use the droplist to select
a resource, and add transformations as desired.

![Completed](assets/img/captures/EventGeneratorTransformation.png "Transformation for To Generator")
