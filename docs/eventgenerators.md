# Event Generators

## Introduction

 Event Generators simulate real world data coming into a Vantiq system. They are tools for creating and replaying Events
 within a namespace. Users can flexibly describe events that will be produced on any Vantiq resource with
  little to no code. 
 
 Event Generators can be used for manual testing to visualize data
 and trouble shoot during Application Development. They can act as test inputs for Integration
 or Unit tests to avoid redundant event definitions. Event Generators may even be used for Performance
 testing to guarantee your system works correctly under load.
 
## Defining an Event Generator
 
Event Generators are defined by a name and a set of Event Descriptors.  

**Note**: All event Types, Topics, and Sources used by Event Generator must have a defined schema or messageType.
 
 ![Event Generator Pane](assets/img/eventgenerators/eventGenerator.png "Event Generator Detail")

 
### Defining an Event Descriptor
 
An Event Descriptor defines one or more events that will occur on a specified resource, and how each events message will be generated. 
Each Event Descriptor defines:

 - **resource** (ResourceReference) *required*: Reference to the resource that will generate the event 
 - **op** (String) *required for type resources*: Type of operation (INSERT, UPDATE, DELETE) of the event if applicable
 - **ruleList** (List of Objects) *required*: List of Generator Rules (see below) that will determine how each event message is constructed
 - **qual** (Object) *required for update/delete events*: Qualifier object describing which instances should be updated or deleted  
  For Example: *{name: "abc"}* would apply to all instances where name == "abc"
 - **startAfter** (Integer): Duration (milliseconds) before this descriptor begins producing events (after Event Generator begins running).
 - **duration** (Integer): Duration (milliseconds) that this event descriptor should actively produce events. The total number of produced
  events will be equal to *duration/interval*.
 - **iterations** (Integer): Number of events that this Event Descriptor will produce
 - **interval** (Integer) *required if periodic*: Duration (milliseconds) between periodic events produced by the Event Generator.  
    *Note*: Either the Duration or Iterations property may be set but not both. If either is set, the interval property is required.
   
   To edit an Event Descriptor in the IDE, click the *Edit* button in the Actions menu for the Event Descriptor.

![Event Generator Pane](assets/img/eventgenerators/eventDescriptor.png "Event Descriptor")
 
### Defining Generator Rules
  The ruleList property of an Event Descriptor determines the message for each event generated. The ruleList is a list
   containing one entry per property in the event resource schema. Each entry is an Object containing the name 
  of the property, and a Generator Rule for determining its value in the event message. An entry is not required for every
   property in the schema, but only properties contained within the ruleList will be present in the event message. 
  
```
{
    "name": <propertyName>,
    "rule": {
        <ruleType> : <ruleValue>
    }
}
```
  
  The following is the complete list of available Generator Rule Types:
  
- **randomRange**: Selects a random number in the specified range. This is only available for properties of type Integer,
  Real, Decimal, DateTime, and Currency. The rule value is a list with 2 entries, defining the minimum and maximum values in the range.    
  Example: `{"rule": {"randomRange": [0, 10]}}` randomly selects a number between 0 and 10.
- **range**: Steps through a specified range given a step size. This is only available for properties of type Integer,
    Real, Decimal, DateTime, and Currency. The rule value is a list with 3 entries. The first entry is the minimum value 
    in the range, the second value is the maximum value in the range, and the third value is the step size. Once the range
    hits the maximum, it will begin again at the minimum.   
    Example: `{"rule": {"range": [0, 10, 2]}}` will step through the range 0 to 10 incrementing by 2 at each iteration.
    Note: For DateTime ranges, an interval string such as *1 minute* must be used as the step size.
- **randomSet**: Selects a random element from a specified set.  The rule value is a list of values.
  A random entry from the list will be selected as the value of the specified property in the message.    
     Example: `{"rule": {"randomSet": ["abc", "def", "ghi"]}}` randomly selects either "abc" or "def" or "ghi" as the property value.  
- **step**: Steps through the values in the specified set. The rule value is a list of values. Once the last entry in the list is reached,
the Event Generator will begin again the first entry.  
       Example: `{"rule": {"step": ["abc", "def"]}}` will alternate between "abc" and "def".
- **value**: Sets the property to a constant value. Rule Value may be set to any legal value for the property.  
              Example: `{"rule": {"value": "abc"}}` will always set the property value to `"abc"`.
- **UUID**: Generates a new UUID for each event. This is only available for String type properties. The Rule value is ignored.  
              Example: `{"rule": {"UUID": null}}`.
- **NOW**: Generates an ISO Date String representing the current time when the event was produced.
 This is only available for String and DateTime type properties. The Rule value is ignored.  
Example: `{"rule": {"NOW": null}}`.
- **NULL**: Sets the property value to null for every message. The Rule value is ignored.  
Example: `{"rule": {"NULL": null}}`.

As an example, the Event Generator below will create events on the `MachineTemperature` type which contains following properties:

- **name** (String) name of the warehouse
- **machineId** (String) unique id of the machine
- **temperature** (Integer) temperature of the machine
- **timestamp** (DateTime) time of the temperature reading

This Event Generator will generate 5 INSERT events on the `MachineTemperature` type over 10 seconds. Each instance will
randomly set the name to either "warehouse1", "warehouse2", or "warehouse3". Each instance will have a
unique id as the machineId and set the timestamp property to the current time. The temperature property will increase from 
100 to 200 over the course of the 5 events, increasing by 20 degrees with each event.

The following Event Generator is defined:

![Event Generator Pane](assets/img/eventgenerators/machineTempEventDescriptor.png "Event Descriptor with properties")

The full JSON representation of the Event Generator is:

```json
{
    "name": "machineTemperatureGenerator",
    "events": [
        {
            "resource": "/types/MachineTemperature",
            "op": "INSERT"
            "iterations": 5,
            "interval": 2000,
            "ruleList": [
                {
                    "name": "name",
                    "rule": {
                        "randomSet": ["warehouse1", "warehouse2", "warehouse3"]
                    }
                },
                {
                    "name": "machineId",
                    "rule": {
                        "UUID": null
                    }
                },
                {
                    "name": "timestamp",
                    "rule": {
                        "NOW": null
                    }
                },
                {
                    "name": "temperature",
                    "rule": {
                        "range": [100, 200, 20]
                    }
                }
            ]
        }
    ]
}
```


The following is an example of the events generated by running `machineTemperatureGenerator`.

```json
   {
      "machineId": "f5abed80-0ffd-11eb-8fda-de54736504e9",
      "name": "warehouse1",
      "temperature": 100,
      "timestamp": "2020-10-16T22:21:38.724Z"
   },
   {
      "machineId": "f5acb0d1-0ffd-11eb-8fda-de54736504e9",
      "name": "warehouse3",
      "temperature": 120,
      "timestamp": "2020-10-16T22:21:40.724Z"
   },
   {
      "machineId": "f5acb0d3-0ffd-11eb-8fda-de54736504e9",
      "name": "warehouse2",
      "temperature": 140,
      "timestamp": "2020-10-16T22:21:42.724Z"
   },
   {
      "machineId": "f5acb0d5-0ffd-11eb-8fda-de54736504e9",
      "name": "warehouse1",
      "temperature": 160,
      "timestamp": "2020-10-16T22:21:44.724Z"
   },
   {
      "machineId": "f5acd7e1-0ffd-11eb-8fda-de54736504e9",
      "name": "warehouse3",
      "temperature": 180,
      "timestamp": "2020-10-16T22:21:46.724Z"
   }
```

#### Generator Rules for List Properties

For Properties marked as `multi`, the Generator Rule must have a different structure.
 Instead of containing a single `rule` property, a `ruleList` property will contain a list of Generator Rules. 
 The *i*th entry in the nested ruleList determines how the *i*th entry in the value list must
be generated. 

The following is an example of an Event Generator that will generate topic events on a topic `/listTopic`.
The Topic's messageType is a Schema Type called `listType` with a single Integer List property called `listProp`.


The Event Generator will generate 5 events on `/listTopic`. For each event message, `listProp` will contain three values.
The first value is a random number between 0 and 5. The second value will step through the values 5 to 10 with a step size 
of 1. The third value will be a random number in between 10 and 15.


![Event Generator Pane](assets/img/eventgenerators/arrayEventDescriptor.png "Array Event Descriptor")

To configure the nested ruleList, click *Configure Array of Integers*

![Event Generator Pane](assets/img/eventgenerators/arrayRules.png "Array Event Descriptor")

The full JSON representation of the Event Generator is:

```json
{
    "name": "listPropertyGenerator",
    "events": [
        {
            "resource": "/topics/listTopic",
            "duration": 5000,
            "interval": 1000,
            "ruleList": [
                {
                    "name": "listProp",
                    "ruleList": [
                        {
                            "rule": {
                                "randomRange": [0, 5]
                            }
                        },
                        {
                            "rule": {
                                "range": [5, 10, 1]
                            }
                        },
                        {
                            "rule": {
                                "randomRange": [10, 15]
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

The following is an example of events generated by running the `listPropertyGenerator`.

```json
   {
      "listProp": [1, 5, 10]
   },
   {
      "listProp": [1, 6, 10]
   },
   {
      "listProp": [4, 7, 14]
   },
   {
      "listProp": [0, 8, 10]
   },
   {
      "listProp": [4, 9, 14]
   }
```

#### Generator Rules for Nested Schema Properties


For properties that are typed as a User (or System) Defined Type rather than a Built-in Property Type (String, Integer, etc), users must define a nested
ruleList to define the nested properties of the event object. Each entry in the nested ruleList contains the nested
property name and a Generator Rule.

For the generated event message to contain a nested object, the resource schema must define the nested schema as an existing Type.
Any property typed as a plain *Object* will only produce an empty object at generation time.


As an example, we will reference a type called `machineDefType` with 2 properties:

- id (String): unique machine id
- temperature (tempType): nested object that contains the machine temperature

`tempType` has 2 properties:

- value (Integer): temperature of the machine   
- timestamp (DateTime): time at which the reading occurred
 
 The following Event Generator will create 5 INSERTS on the `machineDefType` type. Each instance will contain a unique value
 for the *id* property. Each instance will contain a nested *temperature* property that will contain a timestamp
 of the current time of the event. The *value* of the *temperature* property will increase from 100 to 200 by steps of 20 over the 5 instances.
 
![Event Generator Pane](assets/img/eventgenerators/nestedSchemaEventDescriptor.png "Array Event Descriptor")

To configure the nested ruleList, click *Configure 'tempType' Object*

![Event Generator Pane](assets/img/eventgenerators/nestedSchema.png "Array Event Descriptor")

The full JSON representation of the Event Generator is:

```json
{
      "name": "nestedEventGenerator",
      "events": [
         {
            "resource": "/types/machineDefType",
            "iterations": 5,
            "op": "INSERT",
            "interval": 1000,
            "ruleList": [
               {
                  "name": "id",
                  "rule": {
                     "UUID": null
                  }
               },
               {
                  "name": "temperature",
                  "ruleList": [
                     {
                        "name": "timestamp",
                        "rule": {
                           "NOW": null
                        }
                     },
                     {
                        "name": "value",
                        "rule": {
                           "range": [100, 200, 20]
                        }
                     }
                  ]
               }
            ]
         }
      ]
   }
```

The following are events from running the `nestedEventGenerator` Generator.

```json
 {
      "id": "96205d80-1000-11eb-8fda-de54736504e9",
      "temperature": {
         "timestamp": "2020-10-16T22:40:26.964Z",
         "value": 100
      }
   },
   {
      "id": "9620d2b1-1000-11eb-8fda-de54736504e9",
      "temperature": {
         "timestamp": "2020-10-16T22:40:27.964Z",
         "value": 120
      }
   },
   {
      "id": "9620d2b4-1000-11eb-8fda-de54736504e9",
      "temperature": {
         "timestamp": "2020-10-16T22:40:28.964Z",
         "value": 140
      }
   },
   {
      "id": "9620d2b7-1000-11eb-8fda-de54736504e9",
      "temperature": {
         "timestamp": "2020-10-16T22:40:29.964Z",
         "value": 160
      }
   },
   {
      "id": "9620d2ba-1000-11eb-8fda-de54736504e9",
      "temperature": {
         "timestamp": "2020-10-16T22:40:30.964Z",
         "value": 180
      }
   }
```

## Running an Event Generator

To run an Event Generator, *POST* to the *eventgenerators* resource using the Event Generator's name as the *resourceId*.  
Send *{ "op": "runGenerator"}* as the Message Body and the Event Generator will begin.

```
Method: POST
URL: /api/v1/resources/eventgenerators/<GeneratorName>
Body: { "op": "runGenerator"}
```

Event Generator's may be run in the IDE by clicking on the *Run Generator* button on the Event Generator's Pane.
 ![Event Generator Pane](assets/img/eventgenerators/eventGenerator.png "Event Generator Detail")

It is important to note that 2 parallel runs of the same Event Generator is not allowed. If the specified Event Generator
 is already actively running, you must wait for it to complete, or terminate it manually, before restarting. 
 However, two different Event Generators may be run in parallel.

Running an Event Generator will return an ArsRunningGenerator instance. The ArsRunningGenerator instance contains the 
name of the running Event Generator, the start time for the run, and the unique *_id* to identify the Event Generator Run.

## Status of an Event Generator
To check whether a given Event Generator is currently running, use the *status* operator. 

```
Method: GET
URL: /api/v1/resources/eventgenerators/<GeneratorName>/_status
Body: {}
```

If the Event Generator is currently running, the status operation will return an object of the form:

```
{
    <GeneratorName>: [
        {
            _id: <runningGeneratorId>,
            startTime: <runningGeneratorStartTime>
        }
    ]
}
```
The *_id* is the same *_id* that was returned when the Event Generator began its run.

 
If there is not an active run of the Event Generator, the *status* operation will return:

```
{
    <GeneratorName>: []
}
```

In the IDE, the status of the Event Generator is automatically fetched every 10 seconds. If the Event Generator is 
not currently running, the Event Generator Pane will present a blue *Run Generator* button. However, if the Event
Generator is currently running, the Pane will instead show a red *Stop Generator* button.

## Stopping an Event Generator

To stop an Event Generator Run before it has completed, *POST* to the *eventgenerators* resource.
Use the *_id* of the ArsRunningGenerator as the *resourceId*.  

The *_id* for the currently active Event Generator is returned when the Event Generator run begins, and may be found again
by running a *status* operation on the Event Generator.

The message body must contain *{ "op": "stopGenerator"}*.

```
Method: POST
URL: /api/v1/resources/eventgenerators/<ArsRunningGeneratorId>
Body: { "op": "stopGenerator"}
```
The server will return a 1 if successful, and an error otherwise.

Event Generator's may be stopped in the IDE by clicking on the *Stop Generator* button on the Event Generator's Pane.

![Event Generator Pane](assets/img/eventgenerators/stopGenerator.png "Stop Generator")
