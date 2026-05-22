# Remote Source Integration

To implement HTTP or REST calls in Vantiq, you use a Remote source. A Remote source is the standard mechanism for 
interacting with external HTTP or RESTful services in Vantiq. It enables developers to define and manage outbound HTTP 
requests directly within the platform.

Remote sources provide a structured interface for configuring request details, sending data, and handling responses 
from external APIs. As the primary and supported integration method for HTTP-based communication, Remote sources are 
the appropriate way to connect to web services from within Vantiq applications.

A remote source implements one or more of the following capabilities:

* Stream data from the REST service. A request is issued to the REST service periodically with the results producing an event which will be delivered to any subscribing rules or clients (thus simulating a stream).
* Query the REST service for data. The REST service receives a standard REST query as documented in the REST API Reference Guide and returns a set of objects in one of the supported content types.
* Send a request to the REST service.

## Defining a Remote Source

A remote source is usually defined in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**. A remote source may also be defined by creating a source resource that represents the definition of the remote source and submitting the definition to the Vantiq server for registration. The source object is submitted using a **POST** request. 

An example:

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "RESTServiceName",
    "type": "REMOTE",
    "config": {
        "uri": "http://sub.domain.vantiq:9900/aDemo/add/demoData",
        "username": "vantiq",
        "password": "vantiq",
    }
}
```

Creates a REST source that can be queried to obtain data from the REST service or notified to send data to the REST service. Notifications are issued via the **PUBLISH** action in a rule. The above example does not define a stream for automatically querying the REST service periodically for data.

Once registered the remote source will immediately begin reading and processing messages if a stream is configured and will also immediately be available for query and notify operations.

The relevant source properties are as follows:

* **name** The name given the remote source by the user. The name must be unique among all sources.
* **type** The string **REMOTE** to indicate this is a REST source.
* **config** A JSON object containing additional REMOTE configuration parameters:
	* **uri** The endpoint for the REST service. This is a `String` containing the URI supported by the REST service.  The form of this URI is important when considering how it may be *resolved* against the *path* of any requests.  See [URI.resolve](https://docs.oracle.com/javase/8/docs/api/java/net/URI.html) for more complete details.  For example, during resolution any trailing path element (such as `demoData` in the above example) will be removed.  To prevent this you would need to use the URI `"http://sub.domain.vantiq:9900/aDemo/add/demoData/"` (note the terminating slash (`/`)).
	* **username** If basic auth is supported by the REST service, the username with which the REST service will be accessed.
	* **password** If basic auth is supported by the REST service, the password with which the REST service is accessed.
	* **accessToken** If the user is authenticated using an accessToken rather than basic auth, the accessToken to be presented to the service. See also the [Fetching Access Tokens on Demand](#fetching-access-tokens-on-demand) section.
    * **realm** The authentication realm to use if an accessToken is specified. Defaults to `Bearer`.
	* **requestDefaults** A request document which provides default values to use when issuing a request to the source (including a polling request). See request document schema for details on the expected contents.
	* **pollingInterval** The interval at which the REST service is polled, in seconds. If a value of 0 is provided then no polling occurs.
	* **query** A request document which describes the query to perform when polling (see request document schema for details on the expected contents). If a query isn’t provided then the source defaults to performing a GET operation on the base URI with no authentication and assumes content type JSON.
	* **clientOptions** The JSON object form of [Vert.x HTTP Client Options](<https://vertx.io/docs/4.5.12/apidocs/io/vertx/core/http/HttpClientOptions.html>) used to configure the client when connecting to the REST service.

### Fetching Access Tokens on Demand

For some sources, the **accessToken** outlined above can be part of the configuration. This works well when that access token is long-lived. However, there are times when that token has a short lifetime -- a few minutes to a matter of hours. Rather than reconfigure the source constantly, you can configure the source so that it can fetch a new token on demand. To do so, you will need to have another REMOTE source (aka _the OAuth source_) defined that represents an [OAuth (Open Authentication)](https://tools.ietf.org/html/rfc6749) authorization server.

The configuration properties described below instruct the Vantiq system to perform the following actions when a request is made on a REMOTE source so configured.

* Check to see that a valid access token for the source is known.  _Valid_ here means that the access token has been obtained, and that it has not expired.
* If not, based on the configuration described below, make a request to the OAuth authentication server to obtain a new access token.
* When the access token is obtained, associate it with the source, and use that access token to interact with the REMOTE source.

The properties defined below can be part of the REMOTE source's configuration. 
If it is more convenient (say, because there are a number of sources that may use the same property values to obtain an access token), these configuration properties may be provided as part of the configuration of the source used to obtain the access token.  Any of the configuration properties described EXCEPT for the **oauthSourceName** property can be included in the OAuth source's configuration.  Since this property tells the remote source which other source to employ to fetch the access token, this must be provided as part of the REMOTE source's configuration. If one of these properties is found in both the REMOTE source's configuration _and_ the OAuth source's configuration, the value from the REMOTE source will be used.

The following outlines the configuration properties required to dynamically obtain the access token. 
These properties are under the **config** property outlined in the section above.

* **config** The following properties are in addition to those defined above.
    * **oauthSourceName** The name of the source to use to fetch the access token
    * **oauthGrantType** The type of request flow to make to get the token.  Choices are `client_credentials` or `refresh_token`.
    * **oauthClientId** The client_id supplied to the user (if any)
    * **oauthClientSecret** The client_secret supplied to the user (if any)
    * **oauthRefreshToken** The refresh token supplied to the user. This is used when the `oauthGrantType` is `refresh_token`. In this case, the **oauthClientId** and **oauthClientSecret** may be required as well.
    * **oauthScope** The scope defined for the token.  This is usually not required
    * **oauthAudience** The audience for the token. While non-standard, this is sometimes used by authorization servers.
    * **oauthUseBasicAuth** Tells Vantiq to package the client_id & client_secret into a BasicAuth credential, and use that to access the authorization server. 
    * **oauthContentType** This allows the user to override the content type used in the authorization server request.  The default value is `application/x-www-form-urlencoded`; this should be overridden only when required.

The **oauthSourceName** indicates that another source, representing the authorization server, is to be used to get an access token.  This source needs to exist and be active at the time a request is made.

OAuth defines a number of grant type flows, two of which are appropriate for our case.  The client_credentials flow, indicated by setting **oauthGrantType** to `client_credentials`, uses the **oauthClientId** and **oauthClientSecret** (often in conjunction with the **oauthScope** and/or **oauthAudience**) to request an access token from the authorization server.  

The refresh token flow, indicated by setting **oauthGrantType** to `refresh_token`, uses the **oauthRefreshToken** in association with **oauthClientId** and **oauthClientSecret** (and often in conjunction with the **oauthScope** and/or **oauthAudience**) to request an access token from the authorization server. The **oauthRefreshToken** is usually a long-lived token that can be used, with the other properties, to obtain an access token.

The **oauthUseBasicAuth** and **oauthContentType** properties do not affect the content of the request; rather, they affect the form the requests take. Some authorization servers will want the **oauthClientId** and **oauthClientSecret** packaged in a Basic Auth and placed in the `Authorization` HTTP header. If your server requires that, set the **oauthUseBasicAuth** property to `true`.

The **oauthContentType** property allows you to use `application/json` instead of the default `application/x-www-form-urlencoded`. This is rarely required.

Note that **oauthClientSecret** and **oauthRefreshToken** properties should be considered sensitive data and, thus, should probably be stored as Vantiq Secrets. This should be done by [referencing the secret in the configuration](source.md#using-secrets).


## Making a Request to a Remote Source

When making a request to a remote source (via polling, SELECT, or PUBLISH) you provide a JSON document which fully describes the request. This is known as a request document and has the following properties:

* **method** The HTTP method to use when issuing the query. The default is GET for query and POST for publish.
* **path** The path to use when issuing the query. If none is provided then the query is performed using just the base URI. The path provided will be *resolved* against the source's base URI. This means that if it is a relative path it may be appended to that URI whereas if it is an absolute path it may replace portions of the URI (depending on whether or not the base URI includes a path segment).
* **query** An object containing name/value pairs which are added to the request as URL query parameters. Supports the `@secrets` notation.
* **fragment** The fragment property, if defined, contains a URI fragment to be added to the URI for the remote source.		
* **headers** An object containing a set of name/value pairs which will be added to the request as HTTP headers. Supports the `@secrets` notation.
* **body** or **parts** The content to send.  Either **body** or **parts** is permitted, not both.
    * **body** An object containing the body content to provide with the request (if any).
    * **parts** A list/array of objects where each item in the list (part description) consists of the following properties. This is used to send a _multipart/form-data_ message.
        * **content** or **ref** The content to be included in this part.  Either **content** OR **ref** must be provided, but not both.
            * **content** The content to be included in this part.
            * **ref** A resource reference to a document.
        * **filename** [Optional] The name to be sent as the _filename_ parameter.  If absent, _filename_ will be set to the name of the document referenced.  If no such name is available, the _filename_ will not be set.
        * **name** The name of the part.  If **content** is provided, this is required.  If **ref** is provided, this will default to the name of the referenced entity.
        * **contentType** The MIME type for the part.  If **content** is provided, this will default to `text/plain`. If **ref** is provided, this will default to the `fileType` of the referenced entity.
* **contentType** The MIME content type used to process both the body and, if the **responseType** property is not defined, the response if it does not contain a content type header. Default is `application/json` if **body** is provided, `multipart/form-data` if **parts** is provided.
* **acceptType** The MIME content type sent as the ACCEPT header in the HTTP request. Either **acceptType** or **responseType** may be specified, but not both.
* **responseType** The MIME content type used to process the response. The property defaults to the content type supplied by the remote source in its response, so most of the time it will not need to be set. However, if that type is not one of the ones recognized by Vantiq, then it may be necessary to provide an explicit value. This value is also sent as the ACCEPT header in the HTTP request otherwise the value of the **contentType** property is sent, although not all remote sources honor this header. The supported response type values are:
	* `*/json` -- parse the content as JSON.
	* `*/xml` -- parse the content as XML. Given precedence this will match `text/xml` before it gets treated as plain text.
	* `text/*` -- convert the content to a string, but otherwise leave unprocessed.
* **requestTimeout** The amount of time the request has to receive any data. If no data is received in the specified amount of time, a timeout occurs and the request is closed. The value must be specified as a VAIL duration, not exceeding the request [execution time](../workloadmanagement.md#default-quotas) which defaults to 2 minutes. If this limit is exceeded, the request times out. 

As noted above, when the **path** of a REST request is used, it is *resolved* against the source's base URI.  If the source URI contains only a schema, host, and port (such as `https://myRestService`) then this distinction won't matter.  However, when the base URI includes a path, it becomes very important.  For example, assume we have a base server URI of `http://some.server.com:8777/api/v1/`.  Resolving the path `info/getStatus` will result in a final URI of `http://some.server.com:8777/api/v1/info/getStatus`.  However, resolving the path `/info/getStatus` results in `http://some.server.com:8777/info/getStatus`.  As you can see, when resolved the relative path *appends* to the existing path, while the absolute path *replaces* it.  For a more detailed description of the resolution process see the [Java URI](<https://docs.oracle.com/javase/7/docs/api/java/net/URI.html>) documentation.

If your query or header values contain sensitive data, you can store them as Vantiq Secrets and reference them in your code using the `@secrets` [syntax](source.md#using-secrets).

The following REST requests are used to manage remote sources:

## Create a REMOTE Source

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "RESTServiceName",
    "type": "REMOTE",
    "config": {
        "uri": "http://sub.domain.vantiq:9900/aDemo/add/demoData",
        "username": "vantiq",
        "password": "vantiq",
         "requestDefaults": {
            "requestTimeout": "30 seconds"
         }
    }
}
``` 

Creates a REST source with the remote service responding at the URI specified.

Alternatively, to use a secret password named "MySecret", change the password property to a reference and specify 'secret' as the passwordType like this:


```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "RESTServiceName",
    "type": "REMOTE",
    "config": {
        "uri": "http://sub.domain.vantiq:9900/aDemo/add/demoData",
        "username": "vantiq",
        "password": "/system.secrets/MySecret",
        "passwordType": "secret"
    }
}
```

It's also possible to use a secret to reference an accessToken instead of configuring the source with a username and password:

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "RESTServiceName",
    "type": "REMOTE",
    "config": {
        "uri": "http://sub.domain.vantiq:9900/aDemo/add/demoData",
        "accessToken": "/system.secrets/MySecret",
        "accessTokenType": "secret"
    }
}
```

To configure the client connection used to communicate with the REST service, you can include a `clientOptions` document.  Common uses of this are:

```json
Disable the SSL trust check:

"config": {
    "uri": "https://sub.domain.vantiq:4443",
    "clientOptions": {
        "trustAll": true
    }
}
```

```json
Enable the use of an HTTP proxy:

"config": {
    "uri": "http://sub.domain.vantiq:9900",
    "clientOptions": {
        "proxyOptions" : {
            "host": "hostABC",
            "port": 8080,
            "password": "pwd123",
            "username": "uuuu"
        }
    }
}
```

### Create a REMOTE Source that uses OAuth to obtain an Access Token

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "OAuthAuthenticatedRESTServiceName",
    "type": "REMOTE",
    "config": {
        "uri": "http://sub.domain.vantiq:9900/aDemo/add/demoData",
         "oauthSourceName": "authSource",
         "oauthGrantType": "client_credentials",
         "oauthClientId": "myClientIdentifier",
         "oauthClientSecret": "@secret(myClientSecret)",
         "requestDefaults": {
            "requestTimeout": "30 seconds"
         }
    }
}
``` 

This request creates a REMOTE source named _OAuthAuthenticatedRESTServiceName_. This source uses another source named _authSource_ to obtain an access token using the `client_credentials` flow, and using the _myClientIdentifer_ as the client id, and the value contained in the Vantiq secret _myClientSecret_ as the client secret.

The source _AuthSource_ would be defined as follows:

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "authSource",
    "type": "REMOTE",
    "config": {
        "uri": "http://some.oauthserver.com/
    }
}
``` 

## Delete a REMOTE Source

```json
DELETE https://dev.vantiq.com/api/v1/resources/sources/RESTServiceName
```
      
Deletes the source created in the previous example.

## Stream Data from REST Service

A stream sourced from the REST service is defined by setting the pollingInterval.

A request will be issued every **pollingInterval** seconds. The response to the request generates an event which is delivered to any subscribing rules.

An example definition of a streaming REST source:

```json
{
     "name": "RESTServiceName",
	 "type": "REMOTE",
     "config": {
        "uri": "http://sub.domain.vantiq/streaming/source",
        "username": "vantiq",
        "password": "vantiq",
        "pollingInterval": 60
    }
}
```

This source will issue a GET (the default HTTP method) on the URI every 60 seconds.

An example definition with optional clientOptions:

```json
{
     "name": "RESTServiceName",
     "type": "REMOTE",
     "config": {
        "uri": "https://sub.domain.vantiq/streaming/source",
        "username": "vantiq",
        "password": "vantiq",
        "pollingInterval": 60
        "clientOptions": {
            "trustAll": true,
            "connectTimeout": 120,
            "proxyOptions" :    {
               "host": "hostABC",
               "port": 8080,
               "password": "pwd123",
               "username": "uuuu"
            }
        }
    }
}
```

## Read from REST service

The REST service can respond to queries when **SELECT** is issued on the remote source. The **WITH** clause of the SELECT is used to specify the request document to use when the select is performed. The request will also incorporate any defaults provided as part of the source definition.

The body of the response carries the results of the query that will be delivered to the caller of **SELECT**. For example:

```js
var someData = SELECT FROM SOURCE someSource WITH path = "/api/getData", method = "GET"
```
     
## Publish Notifications to REST Service

The **PUBLISH** request for remote sources takes three parameters: the source to which the publish is sent and the body and publish parameters object. The message body and any publish parameters are combined with any request defaults provided by the source to form the final request document which is used to perform the PUBLISH.

For example:
	
```js
PUBLISH { body: { data: "somedata" } } TO SOURCE someRemoteSource USING { path: "/submit" }
```

## Form encoding

If the content type of a request is `x-www-form-urlencoded`, and the request body consists of key-value pairs represented 
as a VAIL object, each key and value is URL-encoded. The resulting key-value pairs are then combined into a single 
string and sent as the request body. If the body is already a string, it is sent as-is without additional encoding.

## JSON Results

If the remote source declares a content type of **json**, results of polling and query operations are returned as JSON objects and JSON arrays. The results can be manipulated in rules using the standard notations of accessing lists, objects, properties.

## XML Results
If a remote source declares a content type of **xml**, results of polling and query operations are returned using an internal representation of the XML element structure. If the result is used in a rule, the rule author must take care to properly navigate the XML structure. The following summarizes the most important access rules using the example XML:

```xml
<houses>
    <house bedrooms="2", bathrooms="2">
    	<address>25 Main Street, Anywhere CA</address>
    	<color>green</color>
    </house>
     <house bedrooms="3", bathrooms="3">
    	<address>50 Main Street, Anywhere CA</address>
    	<color>blue</color>
    </house>
</houses>
```

An XML document may be received by invoking a query using the **SELECT** operation to query the remote source for the list of houses:

```js
var query = SELECT FROM SOURCE "someRemoteSource" WITH parm = 1
```
    
When the query returns the XML document is assigned to the variable **query**. The XML document can then be examined by navigating using element names and attribute names. The set of houses can be obtained via the navigation expression:

```js
houseList = query.house
```

Note that **house** returns the array of houses that are children of the houses element. The array of houses is assigned to the variable **houseList**.

A single house within the list of houses can be reference by the house's index in the house array:

```
firstHouse = query.house[0]
```

returns the first house in the array of houses while:

```
secondHouse = query.house[1]
```

returns the second house in the array of houses.

An attribute can be referenced using the XPath syntax ["@<attributeName>"]. Note the use of double quotes to identify the attribute name:

```
bedrooms = query.house[0]["@bedrooms"]
```

will return an XML element that contains the number of bedrooms. However, the returned value is an element. In order to obtain the actual value of the element (the value: "2") the reference must explicitly request the text value of the attribute as follows:

```
bedroomsAsText = query.house[0]["@bedrooms"].text()
```

Nested elements can be referenced using the dot (.) notation to navigate the hierarchical structure of the XML document. For example, to obtain the address of the second house in the list:

```
query.house[1].address.text()
```

will return the value:

```text
50 Main Street, Anywhere CA
```
In the example above all the sub-elements of **houses** are elements named **house**. In XML the sub-elements may be of multiple types. The sub-elements can be directly referenced by their element names. A more general example:

```xml
<places>
    <house bedrooms="2", bathrooms="2">
    	<address>25 Main Street, Anywhere CA</address>
    	<color>green</color>
    </house>
     <house bedrooms="3", bathrooms="3">
    	<address>50 Main Street, Anywhere CA</address>
    	<color>blue</color>
    </house>
    <office floor="2", size="2000">
    	<address>75 Main Street, Anywhere CA</address>
    	<color>green</color>
    </office>
     <office floor="3", size="10000">
    	<address>100 Main Street, Anywhere CA</address>
    	<color>blue</color>
    </house>
</places>
```

In this example the first house can be referenced with the following expression:

```js
var query = SELECT FROM SOURCE "someRemoteSource" WITH parm=1
firstHouse = query.house[0]
```
    
This is exactly the same syntax as in the previous example. In detail it asks the system to find the first element of type **house** that is a sub-element of the root of the XML document (the **places** element).

The second office in the list can be obtained in a similar fashion.

```
secondOffice = query.office[1]
```    
interpreted as find the second element of type **office** that is a sub-element of the root of the XML document.

## Gzip Content Encoding

A REMOTE source can transparently decompress gzip-encoded HTTP responses from a remote service. To enable this, set `clientOptions.decompressionSupported` to true, as shown below:

```json
{
  "uri": "https://remoteSite:4443",
  "clientOptions": {
    "decompressionSupported": true
  }
}
```

With this option enabled, the REMOTE source sends `Accept-Encoding: gzip, deflate` on outbound requests and automatically decompresses any response that arrives with `Content-Encoding: gzip` (or `deflate`). This setting applies only to response handling; it does not compress request bodies.

## Document Operations<a name="documentOps"></a>

A REMOTE source can be used to upload or download (_i.e._, send or receive, respectively) Vantiq Documents.

### Receiving a Document

To receive a Vantiq Document from a REMOTE source, provide a `saveAs` parameter to the `WITH` clause of the SELECT statement. The value of the `saveAs` parameter should be a `ResourceReference` identifying the where to save the result.

For example, the following VAIL code will fetch an image from a REMOTE source (here, called `imageSource`), saving it into a VAIL document named `myImage`.

```js
var imageRef = "system.documents/myImage"
var fetchedImg = SELECT ONE FROM SOURCE imageSource WITH saveAs = imageRef
```

The return value of the SELECT statement (here, stored in the `fetchedImg` variable), will be the resource reference into which the image was saved.

#### Saving Content to a Temp Blob

Additionally, you can save the result to a [Temp Blob](./../resourceguide.md#tempblobs). To perform this action, the value of the `saveAs` parameter should be a [`ResourceReference`](./../rules.md#resourcereference) to a temp blob.  For Temp Blobs, the `resourceId` portion must be included, but will be ignored because Temp Blob resource ids are assigned by the system. 

In this case, the Temp Blob will be returned by the SELECT statement used to query the source.

For example,

```js
// 'any' will be ignored - the Temp Blob resource id will be assigned by the system
var imageRef = "/system.tempblobs/any"
var fetchedImg = SELECT ONE FROM SOURCE imageSource WITH saveAs = imageRef
```

and `fetchedImg` would be something like,

```json
{
   "fileType": "image/jpeg",
   "contentSize": 53860,
   "contentRef": "/system.tempblobs/b64ba680-7885-11f0-8a86-f27cd3919e31__94456d6f-6a78-43bb-bed7-81e6d9e62f67"
}
```

#### Dynamically Determining Whether to Save the Document

As noted above, when the `saveAs` parameter is provided, the Document is saved as specified.  However, it is sometimes desired to fetch entities, then determine whether to save them based on some criteria. Rather than always saving then having to remove unwanted things, we can use the `processWith` parameter.

The `processWith` parameter can optionally be provided in addition to the `saveAs` parameter. The `processWith` parameter should specify the name of a procedure that will be called to determine whether to save the received entity or to discard it.

The procedure (which can be in a package and/or service) must have the following signature.

```js
//
// Process/Filter document reference
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


### Sending a Document Using PUBLISH

Sending a Vantiq Document is done using the PUBLISH statement. Vantiq supports sending such data as the _directly embedded_ content of the PUBLISH message or via `multipart/form-data`.  These two types are the most common upload formats for large data elements.

Both forms of upload involve the use of a _packaged reference_.  A _packaged reference_ allows us to optionally encode the data as Base64 when required.  When uploading data to a REMOTE source directly, this will rarely be required (_i.e._, only if the REMOTE source itself requires it). A
_packaged reference_ is generated using the VAIL procedure `Utils.packageReference(rRef)` where `rRef` is a ResourceReference for the Vantiq document to upload.

#### Embedding the Data Directly

To upload a Vantiq document directly, PUBLISH to the source in question, setting the `body` of the message to the _packaged reference_ of the data required.  For example, to upload a Vantiq document named _aBeautifulPicture_, we would use the following VAIL code

```js
    var path = ...
    var rRef = "system.documents/aBeautifulPicture"
                
    PUBLISH { body: Utils.packageReference(rRef) } TO SOURCE imageSource USING {
                    path: path
    }

```

where `path` is set to the path required by the server to which you are uploading. The `method` parameter can be set to override the default of `POST`. For example, to upload the same document using the HTTP PUT method, use

```js
    var path = ...
    var rRef = "system.documents/aBeautifulPicture"
                
    PUBLISH { body: Utils.packageReference(rRef) } TO SOURCE imageSource USING {
                    method: "PUT",
                    path: path
    }

```

The `contentType` will be set to the fileType of the Vantiq Document if not specified.  If a value is provided, it will be used (except for the special case of `multipart/form-data` outlined below).


#### Using Content-Type multipart/form-data

##### **Sending a single entity**

A common case for uploading large binary data is to send it using the HTTP content type `multipart/form-data`.  The Vantiq REMOTE source is capable of utilizing this format.

To upload data in such a way, you will set the `contentType` parameter to `multipart/form-data; boundary=...` as shown below.  The value of `boundary` must be a value known not to be found in the data being uploaded. A common case is some random string of characters, but you can use any value you find appropriate.  The `boundary` value is used in the HTTP message to delimit the uploaded content.

```js
    var rRef = "system.documents/testVideo.mp4"
    var boundary = "lkadifuloiuwrnkcnpow983lsl8sla"
    
    PUBLISH { body: Utils.packageReference(rRef) } TO SOURCE imageSource USING {
        path: path,
        contentType: "multipart/form-data; boundary=" + boundary
    }

```

##### **Sending multiple parts**

Sometimes, it is desirable to send a multipart message where the sender and receiver are aware of the parts.  To do this, we use the **parts** property to specify the content. The **parts** property is used instead of the **body** property.

For example, to send a multipart message containing some object in a part named _specification_ and an image showing the part, we could use

```js
PUBLISH { parts: [ { name: "specification",
                     contentType: "application/json",
                     content: { specName: "partSpec", 
                                specId: "someSpecificationId",
                                partName: "widget 42",
                                specDescription: "This describes widget 42." }},
                   { ref: "system.documents/widget42Image.jpg" }
                 ] } TO SOURCE mySource
```

Alternatively, if we expect some response, we can use the SELECT form:

```js
SELECT ONE FROM SOURCE mySource WITH
                method: "POST",
                parts: [ { name: "specification",
                           contentType: "application/json",
                           content: { specName: "partSpec", 
                                      specId: "someSpecificationId",
                                      partName: "widget 42",
                                      specDescription: "This describes widget 42." }},
                         { ref: "system.documents/widget42Image.jpg" }
                       ]
```


As with the direct upload above, the `method` parameter can be set to the appropriate HTTP Method name, overriding the default value of `POST`.

Note that this form can be used to send a single entity as a single part as well.

### Sending a Document via JSON

It is likely to be quite rare, but there may be cases when you need to embed document data in a JSON message. This may be to send data to some specialized service that includes other information in the JSON body. To do this, we again make use of the _packaged references_ outlined above.

Specifically, we can provide the _packaged reference_ as the value for a property in our VAIL message body. For example, to perform a query on our `imageSource`, sending the data from the Document _aBeautifulPicture_, we would use the following code.

```js
    var rRef = "system.documents/aBeautifulPicture"
        
    var fetchEnt = SELECT ONE FROM SOURCE imageSource WITH
            method = "POST",
            body = { name: "myPicture",
                     picture: Utils.packageReference(rRef) }
```

This will send a JSON message with a `name` property set to `myPicture` and a `picture` property set to the value of the document _aBeautifulPicture_. If the `fileType` of the referenced document is not text, the value of `picture` will be base64 encoded.  If that document's `fileType` is text, the `picture` value will not be base64 encoded.

If you need to perform base64 encoding regardless of the target's `fileType`, set the `forceBase64` parameter to `Utils.packageReference()` to `true`. 

```js
    var rRef = "system.documents/aBeautifulPicture"
        
    var fetchEnt = SELECT ONE FROM SOURCE imageSource WITH
            method = "POST",
            body = { name: "myPicture",
                     picture: Utils.packageReference(rRef, true) }
```

In this case, the `picture` property will be base64 encoded regardless of the `fileType` of the referenced document.

Similarly, if you wish to PUBLISH data to a REMOTE source with document data in the VAIL message, you would use something like the following.

```js
    var rRef = "system.documents/aBeautifulPicture"
        
    PUBLISH { body: { name: "myPicture",
                      picture: { subject: "sunset",
                                 imageContent: Utils.packageReference(rRef)
                               }
                    }
            }
```

This example publishes a message whose body consists of a property `name` with the value _myPicture_, and a property `picture` whose value is a nested object with properties `subject` with value _sunset_ and `imageContent` containing the value of the document _aBeautifulPicture_.  As with the previous example, `imageContent`'s value will be base64 encoded if the `fileType` of _aBeautifulPicture_ is not text.  To override this behavior, provide the `forceBase64` parameter to `Utils.packageReference()`.

<a name="sizeLimits"></a>
### Size Limits When Operating on Documents

In all of these cases, the documents referenced are expanded in the Vantiq server as required. This expansion is controlled by [organization quotas](../namespaces.md#quotas) that limit how much memory these document expansions can concurrently consume. Should these limits be exceeded, operations will wait until there is sufficient quota available. However, if a particular request would exceed the quota by itself, the request will result in an error.


## Receiving the full response

When performing a SELECT, the caller may request that the source return the entire response document instead of just the content in the body of the response. This is done by setting the `asFullResponse` property to `true` in the WITH clause of the select. When this is done, the result will be a JSON object with the following properties:

* **status** The HTTP status code of the response.
* **headers** The HTTP headers returned in the response. If a header has multiple values then it is returned as an array of strings.
* **cookies** The cookies contained in the response as an array of strings.
* **body** The body of the response (what would normally be returned by the SELECT).

To additionally treat HTTP redirect responses (status codes in the 300 range) as failures without triggering exceptions, also set the `includeRedirect` property to `true`.

## Receiving the full exchange

To troubleshoot a REST request during a SELECT operation, the caller can ask for a JSON document containing `request` and `response` properties that give detailed insights into the HTTP exchange. When this feature is enabled, a response error (status code >= 400) does not trigger an exception. Instead, failure information is available in the `response` section.

If there is a request body and its size is smaller than 4096 bytes, the `request` property also includes a `bodyHex`  attribute that shows the request's byte content. This is meant to display the exact payload as it is sent. The request body itself is a string representation of the buffer sent, and the response body is the payload as received and parsed by the remote source.

Receiving a full exchange is enabled by setting the `asFullExchange` property to `true` in the WITH clause of the select. 

To also receive failure information for HTTP status codes in the 300 range (redirect responses) without triggering an exception, set the `includeRedirect` property to `true`.

## Response error

If a request response status code is an error, an exception is thrown. In that case, the exception object `params` property
contains the following information:

- source name
- status message
- response message
- status code

## SSL Setup

A Remote Source can be configured for either one-way or two-way SSL communication using the optional `clientOptions`
configuration property. This property is the JSON object form of the
[Vert.x HTTP Client Options](<https://vertx.io/docs/4.5.12/apidocs/io/vertx/core/http/HttpClientOptions.html>).
Below are some usage examples of this configuration option.

### One-way SSL

This section's examples assume that a remote site certificate has been signed by a CA, CA certificate
added to a trust store named `sourceTrustStore.jks`. A Remote Source is configured to access the remote site
and the user configuring the Source has access to the trust store.

If the trust store is accessible on a file system readable by the Vantiq server (e.g., an edge installation),

```json
{
    "uri": "https://remoteSite:4443",
    "clientOptions": {
        "trustStoreOptions": {
            "path": "/path/to/sourceTrustStore.jks",
            "password": "my_store_password"
        }
    }
}
```

If the trust store is not accessible by the server in which the remote source is being defined, the trust store content
can be specified as a base64 encoded value,

```json
# Copy/paste the following output to the value property below
$ cat /path/to/sourceTrustStore.jks | base64

{
    "uri": "https://remoteSite:4443",
    "clientOptions": {
        "trustStoreOptions": {
            "value": "/u3+7QAAAAIAAAABAAAAAgAGY2F........SzpeAUc7WXDK1HOg==",
            "password": "my_store_password"
        }
    }
}
```

The value can also be stored as a Secret and [referenced in the configuration](source.md#using-secrets),

```json
# Copy/paste the following output to a Secret named SourceTrustStore
$ cat /path/to/sourceTrustStore.jks | base64

{
    "uri": "https://remoteSite:4443",
    "clientOptions": {
        "trustStoreOptions": {
            "value": "@secrets(SourceTrustStore)",
            "password": "my_store_password"
        }
    }
}
```

Note that the store password can also be defined as a Secret using the same `@secrets()` syntax.

For example,

```json
# Also define a Secret named SourceTrustStorePassword containing the trust store password

{
    "uri": "https://remoteSite:4443",
    "clientOptions": {
        "trustStoreOptions": {
            "value": "@secrets(SourceTrustStore)",
            "password": "@secrets(SourceTrustStorePassword)"
        }
    }
}
```

Assuming that the CA certificate is also accessible from a file named `ca-cert` in PEM format,

```json
{
    "uri": "https://remoteSite:4443",
    "clientOptions": {
        "pemTrustOptions": {
            "certPaths": ["/path/to/ca-cert"],
            "password": "my_store_password"
        }
    }
}
```

This configuration can also be expressed using a base64 value,

```json
# Copy/paste the following output as one String entry in the certValues array below
$ cat /path/to/ca-cert | base64

{
    "uri": "https://remoteSite:4443",
    "clientOptions": {
        "pemTrustOptions": {
            "certValues": ["LS0tLS1CRU.........0FURS0tLS0tCg=="]
        }
    }
}
```

The above example could also be defined using a Secret. Assuming two certificates `ca-cert-1` and `ca-cert-2`
both in PEM format,

```json
# Copy/paste the following output to a Secret named CertAuthority1
$ cat /path/to/ca-cert-1 | base64
# Copy/paste the following output to a Secret named CertAuthority2
$ cat /path/to/ca-cert-2 | base64

{
    "uri": "https://remoteSite:4443",
    "clientOptions": {
        "pemTrustOptions": {
            "certValues": ["@secrets(CertAuthority1)", "@secrets(CertAuthority2)"]
        }
    }
}
```

### SSL Client Authentication

In addition to specifying a trust store, a source configuration can also specify a client certificate.
This is necessary if the server requires the client to authenticate with a certificate.

The examples below assume a key store named `sourceKeyStore.jks` containing the client certificate
signed by the CA.

If the key store is accessible on a file system readable by the Vantiq server,

```json
{
    "uri": "https://remoteSite:4443",
    "clientOptions": {
        "trustStoreOptions": {
            "path": "/path/to/sourceTrustStore.jks",
            "password": "my_store_password"
        },
        "keyStoreOptions": {
            "path": "/path/to/sourceKeyStore.jks",
            "password": "my_keystore_password"
        }
    }
}
```

Similarly to the trust store examples, any keystore specified using the path syntax can be specified as a base64
encoded value.

For example using Secret definitions,

```json
# Copy/paste the following output to a Secret named SourceTrustStore
$ cat /path/to/sourceTrustStore.jks | base64
# Copy/paste the following output to a Secret named SourceKeyStore
$ cat /path/to/sourceKeyStore.jks | base64

{
    "uri": "https://remoteSite:4443",
    "clientOptions": {
        "trustStoreOptions": {
            "value": "@secrets(SourceTrustStore)",
            "password": "my_store_password"
        },
        "keyStoreOptions": {
            "value": "@secrets(SourceKeyStore)",
            "password": "my_keystore_password"
        }
    }
}
```

Note that if a keystore contains several keys you can specify which key to use by providing the `alias`
[store options](https://vertx.io/docs/4.5.12/apidocs/io/vertx/core/net/JksOptions.html) property.

Refer to the [Vert.x HTTP Client Options](<https://vertx.io/docs/4.5.12/apidocs/io/vertx/core/http/HttpClientOptions.html>)
document for a complete list of configuration options. Note: in that document, reference to `Buffer`
means that a base64 encoded value can be specified (e.g., trustStoreOptions). Any `add` method translates into an array
(e.g., pemTrustOptions) and any `set` method translates into a single property setting (e.g., path or value).

## Realm Authentication

Some REST APIs can use an API key as a means of authentication. An API Key is a Token and must always be
specified with a realm value. Although the realm value for API keys is often `Bearer`, the value might differ
based on the REST APIs that you are accessing. Make sure to check the REST APIs documentation for the proper
realm value to specify.

The below example configures a Remote Source to send heartbeats to an Opsgenie heartbeat endpoint. The API Key
is stored as a Secret named HeartbeatAccessKey and the REST documentation instructs to use the realm GenieKey.

```json
{
    "name": "HeartbeatSource",
    "type": "REMOTE",
    "config": {
        "accessToken": "/system.secrets/HeartbeatAccessKey",
        "accessTokenType": "secret",
        "realm": "GenieKey",
        "uri": "https://api.opsgenie.com/v2/heartbeats/"
    }
}
```

With the following Procedure sending heartbeats,

```js
PROCEDURE sendHeartbeat(heartbeatName String)
    var pingPath = heartbeatName + "/ping"
    select from source HeartbeatSource with path = pingPath
```

## JWT Authentication

If a REST API requires to authenticate with a JWT token, you can use the
[JWT service procedures](./../rules.md#jwt-procedures) and include the token in the Authorization header.

For example, assuming a remote source named `RemoteAPI` and a signing key `MyPrivateKey` configured 
as a [secret](./../resourceguide.md#secrets),

```
// Claims to be included in the JWT token
var claims = {
  "iat": 1686095226,
  "exp": 1686116826,
  ...
}

// Create the JWT token using the RS256 algorithm
var jwt_token = JWT.createTokenUsingResource("RS256", claims, "system.secrets", "MyPrivateKey")

// Access the Remote API authenticating with the JWT token
var response = select from source RemoteAPI with headers = {Authorization: jwt_token}
```

## Open Inference Protocol

The [Open Inference Protocol](https://github.com/kserve/open-inference-protocol) (OIP) is built on standard HTTP/REST communication, making the Remote source a natural integration point for connecting to OIP endpoints.

A Remote source can be explicitly configured to take advantage of OIP extensions by setting the `openInference` configuration property to true. Enabling this property activates support for the OIP binary data extension, which allows efficient transfer of large tensors, such as images.

For more information on using Remote sources with OIP endpoints, refer to the [Open Inference Guide](../openinference.md).
