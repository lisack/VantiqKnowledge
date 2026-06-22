# VIDEO Source Integration

A VIDEO source represents a source of image data. This may be an online camera or a file. A video source can supply data.  Sending data to a video source is not supported.

A video source implements one or more of the following capabilities:

* Stream data from the origination of the video. A request is issued to the video service periodically with the results producing an event which will be delivered to any subscribing rules or clients (thus simulating a stream).
* Query the video service for data. The video service is asked for content data and returns an image.

The operation of the video source is enabled through the _video assistant_ service connector.  If you are using the video source, your administrator will need to configure your organization with the VideoAssistantServiceConnector. Information about how to do this can be found in the [Administrators Reference Guide](../namespaces.md#depVidAssistant) and, for Vantiq edge installations, the [Vantiq Edge Reference Guide](../vantiqedge.md), specifically [running the Video Assistant server](../vantiqedge.md#runVideoAssistant) and [creating the Video Assistant Service Connector](../vantiqedge.md#createVideoAssistantSC).

Images returned by a video source are, by default, placed in memory (as a [`TempBlob`](./../resourceguide.md#tempblobs)) -- they are not saved to a document resource ([unless specifically requested](#saveAs)). Any use of a video source requires some organization-wide quota.  See [Size Limits](#sizeLimits) for more information.

## Defining a Video Source

A video source is usually defined in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**. A video source may also be defined by creating a source resource that represents the definition of the video source and submitting the definition to the Vantiq server for registration. The source object is submitted using a **POST** request. 

An example:

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "VIDEOCameraSource",
    "type": "VIDEO",
    "config": {
        "ipCamera": "http://online.camera.address:9900/aDemo/add/demoData"
    }
}
```

Creates a video source that can be queried to obtain data from the camera at the specified network address. This example does not define a stream for automatically querying the camera periodically for data.

Once registered, the video source will immediately begin reading and processing images if a stream is configured and will also immediately be available for query operations.

The relevant source properties are as follows:

* **name** The name given the video source by the user. The name must be unique among all sources.
* **type** The string **VIDEO** to indicate this is a video source.
* **config** A JSON object containing additional VIDEO configuration parameters:
    * Exactly one of the following:
        * **ipCamera** An endpoint representing a camera on network.  This is a `String` containing the URI supported by the camera in question.
        * **directCamera** An address of a camera available to the server (that is, on the same machine).  Direct camera addresses are environment specific and rarely used.
        * **videoFile** A fully specified file path and name, again available to the server.  This is expected to be used primarily for testing.
    * **rtspTransport** An optional value of 'udp', 'tcp', 'udp_multicast', or 'http'. If specified, this value overrides the default RTSP transport negotiation and forces the use of the selected transport.
	* **pollingInterval** The interval at which the video service is polled. Unlike the REMOTE source, this value is specified as a VAIL duration (_e.g._, `3 seconds`). If a value of 0 or no value is provided then no polling occurs.
	* **requestDefaults** A collection of defaults to use in making requests
	    * **query** A set of parameters defining defaults when fetching images.  These are used for polling or direct queries. 
	        * **contentType** is used to specify the desired MIME type to return. The source assumes a default content type `image/jpeg`.  The supported response type values are:
	            * `image/jpeg` -- return a JPEG image.
	            * `image/png` -- return a PNG image.
	        * **requestTimeout** is used to specify the time to wait for the query.If no data is received in the specified amount of time, a timeout occurs, and the request is closed. The value must be specified as a VAIL duration, not exceeding the request [execution time](../workloadmanagement.md#default-quotas) which defaults to 2 minutes. If this limit is exceeded, the request times out. 
	        * **resize** is used to specify the image size of the result. It is specified as a JSON object containing the following:
	            * **maxHeight** and **maxWidth** -- integers specifying the maximum height and width of the resulting image. If the image returned from the camera or file is smaller than what's specified, no resizing will be done.
	            * **maxLongEdge** -- an integer specifying the size of the long edge of the resulting image.  The shorter edge will be adjusted proportionally.  As above, if the long edge is shorter than this value, no resizing is done.
	            * Note that the **resize** member can have either **maxHeight** and **maxWidth** OR **maxLongEdge** but not both.


## Making a Request to a Video Source

When making a request to a video source (via polling, or SELECT) you can provide a JSON document which fully describes the request. This document can have the following properties:

* **contentType** The MIME content type to process the response. The property defaults to the content type supplied by the video service in its response, so most of the time it will not need to be set. The supported response type values are:
    * `image/jpeg` -- return a JPEG image.
    * `image/png` -- return a PNG image.
* **requestTimeout** The amount of time the request has to receive any data. If no data is received in the specified amount of time, a timeout occurs, and the request is closed. The value must be specified as a VAIL duration, not exceeding the request [execution time](../workloadmanagement.md#default-quotas) which defaults to 2 minutes. If this limit is exceeded, the request times out. 
* **resize** is used to specify the image size of the result. It is specified as a JSON object containing the following:
    * **maxHeight** and **maxWidth** -- integers specifying the maximum height and width of the resulting image. If the image returned from the camera or file is smaller than what's specified, no resizing will be done.
    * **maxLongEdge** -- an integer specifying the size of the long edge of the resulting image.  The shorter edge will be adjusted proportionally.  As above, if the long edge is shorter than this value, no resizing is done.
    * Note that the **resize** member can have either **maxHeight** and **maxWidth** OR **maxLongEdge** but not both.

In all of these cases, the values given at the time of the query override those specified in the source definition.


If your query values contain sensitive data, you can store them as Vantiq Secrets and reference them in your code using the `@secrets` [syntax](source.md#using-secrets).

The following REST requests are used to manage video sources:

## Create a VIDEO Source

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "VIDEOCameraSource",
    "type": "VIDEO",
    "config": {
        "ipCamera": "http://online.camera.address:9900/aDemo/add/demoData"
    }
}
```

Creates a REST source with the video service responding at the URI specified.

To define a video source that reads from a file, use the following.

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "VIDEOFileSource",
    "type": "VIDEO",
    "config": {
        "videoFile": "/some/file/location/sample.mov"
    }
}
```

To define a video source that reads from a file, resizing the result, use the following.

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "VIDEOFileSource",
    "type": "VIDEO",
    "config": {
        "videoFile": "/some/file/location/sample.mov"
        "requestDefaults": {
            "query": {
                "resize": {
                    "maxWidth": 400,
                    "maxHeight": 300
                }
            }
        }
    }
}
```


## Delete a VIDEO Source

```json
DELETE https://dev.vantiq.com/api/v1/resources/sources/VIDEOCameraSource
```
      
Deletes the source created in the previous example.

## Stream Data from VIDEO Service

A stream sourced from the video service is defined by setting the pollingInterval.

A request will be issued every **pollingInterval** seconds. The response to the request generates an event which is delivered to any subscribing rules.

An example definition of a streaming REST source:

```json
{
     "name": "RESTServiceName",
	 "type": "REMOTE",
     "config": {
        "ipCamera": "http://online.camera.address:9900/aDemo/add/demoData"
        "pollingInterval": "1 minute"
    }
}
```

This source will fetch a new image from the camera at the specified URI every minute.


## Read from Video service

The video service can respond to queries when **SELECT** is issued on the video source. The **WITH** clause of the SELECT is used to specify the request document to use when the select is performed.

The body of the response carries the results of the query that will be delivered to the caller of **SELECT**. For example:

```js
var someData = SELECT FROM SOURCE videoSource WITH contentType="image/png"
```

Will override the content type of the camera or source.

```js
var someData = SELECT FROM SOURCE videoSource WITH contentType = "image/png", 
                resize = { maxHeight: 300, maxWidth: 400 }
```

Will override the content type and the image size.  

<a name="docImgVidOps"></a>
## Image Operations

A VIDEO source is used to download (_i.e._, receive) images. These are returned as a Object containing the following properties:

* **fileType** -- the MIME type of the image entity
* **contentSize** -- the size (in bytes) of the image entity
* **contentRef** -- a ResourceReference to the `TempBlob` holding the entity contents

The [`TempBlob`](./../resourceguide.md#tempblobs) has a defined expiration time (defaulting to 2 minutes).  If not saved by that time, the data is lost.

<a name="saveAs"></a>
### Saving an Image as a Document

To save the result of a query against a video source as a Vantiq Document, provide a `saveAs` parameter to the `WITH` clause of the SELECT statement. The value of the `saveAs` parameter should be a `ResourceReference` identifying the where to save the result.

For example, the following VAIL code will fetch an image from a video source (here, called `imageSource`), saving it into a VAIL document named `myImage`.

```js
var imageRef = "system.documents/myImage"
var fetchedImg = SELECT ONE FROM SOURCE imageSource WITH saveAs = imageRef
```

The return value of the SELECT statement (here, stored in the `fetchedImg` variable), will be the resource reference into which the image was saved.

<a name="processWith"></a>
#### Dynamically Determining Whether to Save the Document

As noted above, when the `saveAs` parameter is provided, the Document is saved as specified.  However, it is sometimes desired to fetch entities, then determine whether to save them based on some criteria. Rather than always saving then having to remove unwanted things, we can use the `processWith` parameter.

The `processWith` parameter can optionally be provided in addition to the `saveAs` parameter. The `processWith` parameter should specify the name of a procedure that will be called to determine whether to save the received entity or to discard it.

The procedure (which can be in a package and/or service) must have the following signature.

```js
//
// Process/Filter document references
//
// @param targetContent String Document content, encoded as base64 if necessary
// @param targetSize Integer Size of targetContent string
// @param isBase64Encoded Boolean Is the string passed along the entity value or the base64-encoded entity value
// @param fileType String MIME content type of target/entity
// @param entitySize Integer The size of the entity to be saved
// @param entityRef ResourceReference to the entity to be saved
// @return Boolean true if resource is to be saved, false to discard it.

PROCEDURE someProcedureName(targetContent String,
                            targetSize Integer,
                            isBase64Encoded Boolean,
                            fileType String,
                            entitySize Integer,
                            entityRef String): Boolean
```

where

* **targetContent** -- the content to be saved, represented as a String.  It may be base64 encoded if the MIME type is not text.
* **targetSize** -- the size of the `targetContent` as an Integer
* **isBase64Encoded** -- is the `targetContent` value base64 encoded
* **fileType** -- the MIME type of the document presented, as a String
* **entitySize** -- the size of the entity as it will be saved, as an Integer.  This may be different from `targetSize` if the `targetContent` is base64 encoded.
* **entityRef** -- Resource Reference of the entity to be saved.

The procedure must return a Boolean value -- _true_ to save the entity as specified, _false_ to discard the entity without saving it.
 
Size limits are enforced as described [here](#sizeLimits).

As an example, the following procedure will save a document if it is a JPEG image (based on its MIME type), discarding it otherwise.

```js
package doc.example

PROCEDURE ExampleService.filter(targetContent String,
                               targetSize Integer,
                               isBase64Encoded Boolean,
                               fileType String,
                               entitySize Integer,
                               entityRef String): Boolean
if (fileType == "image/jpeg") {
    return true
} else {
    return false
}
```

To use the procedure, we might extend our previous example as follows:

```js
var imageRef = "system.documents/myImage"
var fetchedImg = SELECT ONE FROM SOURCE imageSource WITH saveAs = imageRef,
    processWith = "doc.example.ExampleService.filter"
```


<a name="sizeLimits"></a>
### Size Limits When Operating on Images

Use of a video source requires the organization to have quota for `documentExpansion`. Details on the `documentExpansion` quota can be found in the [Administrators Reference Guide](../namespaces.md#quotas).

The images returned are stored in the Vantiq server. This storage is controlled by organization quotas that limit how much memory these document, image, or video expansions can concurrently consume. Should these limits be exceeded, the request will result in an error.

