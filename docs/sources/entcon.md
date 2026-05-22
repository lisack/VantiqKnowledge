<center><h1>Enterprise Connectors Reference Guide</h1></center>

# Introduction

The Vantiq Enterprise Connector capability supports the creation of new Vantiq source types.
Within a Vantiq system, a *source* is the means by which the Vantiq system communicates with other systems.
Each Vantiq source has a *type*.
The source type determines defines the type(s) of system(s) with which the source can communicate.
The Vantiq system has a variety of source types included,
but individual enterprises may require connectivity to other systems.
These other systems may be other commercial or standard systems,
or they may be a *home-grown* system.
In any case,
the set of source types is extensible using **Vantiq Enterprise Connectors**.

Working with the Vantiq system,
a connector (also known as an *extension source*) can be constructed and operated outside the Vantiq installation.
This allows these sources to fully participate in Vantiq edge or full installations.

# Enterprise Connectors Overview

Enterprise Connectors are used to allow Vantiq to communicate with various other systems.
Supported operations include

 - sending a message to the connector (or, more precisely, via the connector to the connected system),
 - having the connector send a message to Vantiq, and
 - querying the connector (or, more precisely, the system being connected).

It is important to understand that the interpretation of these operations
is determined completely by the connector designer/developer.

For example, when sending a message to an enterprise connector,
it might be the case that depending upon some parameter in the message,
the connector might save the data, invoke some operation, or perform some other
action that is appropriate for the data system that connector represents.

# Enterprise Connector Details

Sources developed using the *Enterpise Connector* (*aka* *Extension Source*) capabilities can be developed by Vantiq or by other parties.

Details regarding how to develop, install, and operate these sources can be found in the [Vantiq Extension Source](https://github.com/Vantiq/vantiq-extension-sources) GitHub repository.
This repository also contains the open source source types.

## Managing the Connector

Information regarding lifecycle-managed deployments can be found in the
[External Lifecycle Management Guide](../extlifecycle.md) and
the [Sources](../resourceguide.md#sources) section of the
[Resource Reference Guide](../resourceguide.md).
Specifically, see the [deploy](../resourceguide.md#source-deploy),
[shutdown](../resourceguide.md#source-shutdown),
[restart](../resourceguide.md#source-restart), and
[undeploy](../resourceguide.md#source-undeploy) operations.

## Communicating with an Enterprise Connector

You can send and receive data from an Enterprise Connector using the standard VAIL SELECT and PUBLISH operations, as well as rules involving the receipt of messages from the connector. See the [VAIL Rule and Procedure Reference Guide](../rules.md) for details.

Additionally, some Enterprise Connectors may support operations involving Vantiq Document, Images, or Videos. Please see the individual connector's documentation for details.

### Sending Document, Image, or Video via JSON

There may be cases when you need to embed document, image, or video data in a message to a connector. This may be to send data to some specialized service that includes other information in the JSON body. To do this, we make use of _packaged references_.

Specifically, we can provide a _packaged reference_ as the value for a property in our VAIL message body. For example, to perform a query on a source`entConnSource`, sending the data from the Document _aBeautifulPicture_, we would use the following code.

```js
    var queryDesc = { name: "aBeautifulPicture", 
                        picture: Utils.packageReference("system.documents/aBeautifulPicture")
                    }

    SELECT * FROM SOURCE entConnSource as o WITH
            query = queryDesc {
       // Process response returned in variable 'o'
    }
```

This will send a JSON message with a `name` property set to `aBeautifulPicture` and a `picture` property set to the value of the document _aBeautifulPicture_. If the `fileType` of the referenced document is not text, the value of `picture` will be base64 encoded.  If that document's `fileType` is text, the `picture` value will not be base64 encoded.

If you need to perform base64 encoding regardless of the target's `fileType`, sent the `forceBase64` parameter to `Utils.packageReference()` to `true`. 

```js
    var queryDesc = { name: "aBeautifulPicture", 
                      picture: Utils.packageReference("system.documents/aBeautifulPicture", true)
                    }

    SELECT * FROM SOURCE entConnSource as o WITH
            query = queryDesc {
       // Process response returned in variable 'o'
    }
```

In this case, the `picture` property will be base64 encoded regardless of the `fileType` of the referenced document, image, or video.

Similarly, if you with to PUBLISH data to a enterprise connector source with document, image, or video data in the VAIL message, you would use something like the following.

```js
    var rRef = "system.documents/aBeautifulPicture"
        
    PUBLISH { body: { name: "aBeautifulPicture",
                      picture: { subject: "sunset",
                                 imageContent: Utils.packageReference(rRef)
                               }
                    }
            }
```

This example publishes a message whose body consists of a property `name` with the value _aBeautifulPicture_, and a property `picture` whose value is a nested object with properties `subject` with value _sunset_ and `imageContent` containing the value of the document _aBeautifulPicture_.  As with the previous example, `imageContent`'s value will be base64 encoded if the `fileType` of _aBeautifulPicture_ is not text.  To override this behavior, provide the `forceBase64` parameter to `Utils.packageReference()`.

### Size Limits When Operating on Documents, Images, or Videos

In all of these cases, the documents, images, or videos referenced are expanded in the Vantiq server as required. This expansion is controlled by organization quotas that limit how much memory these document, image, or video expansions can concurrently consume. Should these limits be exceeded, operations will wait until there is sufficient quota available. However, if a particular request would exceed the quota by itself, the request will result in an error.



