# Vantiq Functionality for React Native Apps
Integrating Vantiq functionality into the [React JavaScript framework](https://react.dev/) is accomplished using the [vantiq-react](https://github.com/Vantiq/vantiq-react) [npm](https://www.npmjs.com/) module. This module for iOS and Android mobile development provides an API to accomplish the following:

* Authentication using either [Keycloak](https://www.keycloak.org/) or Vantiq Internal methods;
* Push Notifications with built-in handling of location tracking;
* Creation of new users using either Keycloak or Internal authentication;
* Execution of streamed Procedures (i.e. executeStreamed);
* Standard CRUD-oriented REST operations (e.g., select, insert, upsert, etc.);
* Vantiq-oriented REST operations (i.e., publish, publishEvent, execute, executePublic)

### Prerequisites
This document assumes that:

* the React Native app already exists, probably created by the CLI command `npx create-expo-app@latest`
* if iOS support is desired, [CocoaPods](https://cocoapods.org/) must be installed on the macOS development machine

### Installation Instructions
* Edit the _package.json_ file at the root of the React Native app to include the following dependencies:
	* `"react-native-root-siblings":"^5.0.1"`
	* `"vantiq-react":"^0.1.9"`
* Execute `npm install` to complete the installations.

### iOS Post-Installation Instructions
* `cd ios`
* edit _Podfile_, including the following in the target section for your app: `pod 'vantiq-ui-ios', :inhibit_warnings => true`. This should be the first line inside the target `do` statement.
* edit _Podfile.properties.json_ to set the `newArchEnabled` property to false: `"newArchEnabled": "false"`. This disables React's new architecture, which is required for Vantiq functionality.
* `pod install`
* `cd ..`
* `npm uninstall react-native-worklets` to regress from React's new architecture.
* `npm install react-native-reanimated@^3.15.0` to regress from React's new architecture.
* `npm install` to update the installations.
* `cd ios`
* `pod deintegrate`
* `pod install`

* The following bullet points make multiple references to edits to the _AppDelegate.m_ file. The AppDelegate.m file edits are complicated so there is a sample of a [complete AppDelegate.m](#sample-ios-appdelegatem-file) file at the bottom of this document.
* If you're using Keycloak-based authentication:
	* Edit the _AppDelegate.m_ file to include the following:
	
		* `#import "VantiqUI.h"`
		* add the following method to handle authorization redirects:
		
```objectivec
(BOOL)application:(UIApplication *)app openURL:(NSURL *)url options:(NSDictionary<NSString *, id> *)options {
	// Sends the URL to the current authorization flow (if any) which will
	// process it if it relates to an authorization response.
	if ([VantiqUIcurrentAuthorizationFlow resumeExternalUserAgentFlowWithURL:url]) {
		VantiqUIcurrentAuthorizationFlow = nil;
		return YES;
	}
		
	// Your additional URL handling (if any) goes here.
	return NO;
}
```

* If you're using Keycloak-based authentication:
	* Edit the _info.plist_ file to include the OAuth URL scheme (see below for more details, e.g. `vantiqreact`) and the iOS app’s Bundle Identifier (e.g. `com.vantiq.reactexample`):

```xml
    <dict> 
        <key>CFBundleSignature</key> 
        <string>????</string> 
        <key>CFBundleURLTypes</key> 
        <array> 
            <dict> 
                <key>CFBundleTypeRole</key> 
                <string>Editor</string> 
                <key>CFBundleURLName</key> 
                <string>com.vantiq.reactexample</string> 
                <key>CFBundleURLSchemes</key> 
                <array> 
                    <string>vantiqreact</string> 
                </array> 
            </dict> 
        </array> 
    </dict> 
```

* If you want to enable APNS Push Notifications:
	* Enable the following Xcode Signing & Capabilities section items for the React Native target:
		*     Privacy - Location Always and When in Use Usage Description = Please allow $(EXECUTABLE_NAME) to report your device's location when required for collaborations.
		*     Privacy - Location When in Use Description = Please allow $(EXECUTABLE_NAME) to report your device's location when required for collaborations.
		*     Privacy - Motion Usage Description = Please allow $(EXECUTABLE_NAME) to detect your device's motion when required for collaborations.
		
	* Edit the _AppDelegate.m_ file to include the following:
		* `#import "LastActive.h"`
		* `#import "VantiqReact.h"`
		* Add following methods which can be found in the [complete AppDelegate.m](#sample-ios-appdelegatem-file) file at the bottom of this document:
			* didRegisterForRemoteNotificationsWithDeviceToken
			* didFailToRegisterForRemoteNotificationsWithError
			* didReceiveRemoteNotification
		* If you want to enable the location tracking features associated with Vantiq push notifications, add the following methods which can be found in the [complete AppDelegate.m](#sample-ios-appdelegatem-file) file at the bottom of this document:
			* performFetchWithCompletionHandler
			* applicationDidEnterBackground
			* applicationWillEnterForeground
		* edit the didFinishLaunchingWithOptions method to include:
	
```objectivec
  // allow the user to select which type of notifications to receive, if any
  UNUserNotificationCenter *center = [UNUserNotificationCenter currentNotificationCenter];
  center.delegate = (id<UNUserNotificationCenterDelegate>)self;
  [center requestAuthorizationWithOptions:(UNAuthorizationOptionSound | UNAuthorizationOptionAlert | UNAuthorizationOptionBadge)
      completionHandler:^(BOOL granted, NSError * _Nullable error){
      if (error) {
          NSLog(@"Error in registering for notifications: %@", [error localizedDescription]);
      } else {
          dispatch_async(dispatch_get_main_queue(), ^ {
              // register for an APNS token
              [[UIApplication sharedApplication] registerForRemoteNotifications];
          });
      };
  }];
```

### Android Post-Installation Instructions

* Set appAuthRedirectScheme
	* Edit the _android/app/build.gradle_ file. You should find an `android` section which contains a `defaultConfig` section that looks similar to the following. Inside the `defaultConfig` section, you must add: `manifestPlaceholders = [appAuthRedirectScheme:"<MyUrlScheme">]`, replacing `MyUrlScheme>` with the same 'urlScheme' parameters you will be passing to the `authWithOAuth` and `createOAuthUser` API calls. This is also known as the 'redirectUrl' for the app.
	
```json
android {  
    namespace 'com.anonymous.testappone' 
    defaultConfig { 
        applicationId 'com.anonymous.testappone' 
        minSdkVersion rootProject.ext.minSdkVersion 
        targetSdkVersion rootProject.ext.targetSdkVersion 
        versionCode 1 
        versionName "1.0.0"
        manifestPlaceholders = [appAuthRedirectScheme:"<MyUrlScheme">]
    }
} 
```

* Configure Firebase
	* If you want to enable Firebase Push Notifications:
		* Use Firebase to generate a google-services.json file for your app and move it to the following directory:  
		android/app
		* To retrieve this file, you need to go to the `Project Settings` page for your Firebase project.
		* Edit the _android/build.gradle_ file. In the `dependencies` section add this line:  
		`classpath 'com.google.gms:google-services:4.3.5'`
		* Edit the _android/app/build.gradle_ file. Add the following line below the other  
		`apply plugins`: `apply plugin: "com.google.gms.google-services"`

* Request Location Permissions
	* If you want to enable the location tracking features associated with Vantiq push notifications, edit the _android/app/src/main/AndroidManifest.xml_ file to add the following permissions:
		* &lt;uses-permission android:name="android.permission.ACCESS\_FINE\_LOCATION"/&gt;
		* &lt;uses-permission android:name="android.permission.ACCESS\_COARSE\_LOCATION"/&gt; 
		* &lt;uses-permission android:name="android.permission.ACCESS\_BACKGROUND\_LOCATION"/&gt;
		
### Vantiq React Module API Reference
#### Authentication Functions
##### init() - initialize the module

```js
init(serverURL:string, namespace:string):Promise<string>
```
* serverURL:string - the fully qualified domain name of the Vantiq server, e.g. https://dev.vantiq.com
* namespace:string - the Vantiq Namespace that contains resources necessary to run the React app

This function must be called before any other module functions in order to establish the Vantiq server and Namespace to be used subsequently by the React app. It determines the type of authentication the server uses (OAuth versus Vantiq Internal) and whether the React app already has valid user authentication credentials. The promise returns a JSON object on success that contains some or all of the following properties:

* serverType:string - will be one of two values, "OAuth" or "Internal". This value can be used to select which authorization function, `authWithOAuth` or `authWithInternal` (see below), is used by the React app to authorize a user.
* authValid:boolean - if true, the React app has valid authentication credentials; if false, the app should use one of `authWithOAuth` or `authWithInternal` to allow the user to authenticate with the Vantiq server.
* username:string - if the user has authenticated, username is the Vantiq username associated with the authentication credentials.
* preferredUsername:string - if the user has authenticated, preferredUsername is the human-readable username associated with the authentication credentials.
* errorStr:string - will contain a human-readable string if any error is encountered while initializing the module.
* statusCode:number - if errorStr is present, statusCode may contain an HTTP response code that might be helpful in determining the nature of the encountered error.

##### serverType() - determine the type of Vantiq server
```js
serverType():Promise<string>
```

This function need not normally be called as it is used by the `init` function to determine the authentication method used by the specified Vantiq server. The promise returns a JSON object on success of the same format as described by the `init` function above.

##### authWithOAuth() - prompt the user for OAuth authentication credentials

```js
authWithOAuth(urlScheme:string, clientId:string):Promise<string>
```

* urlScheme:string - the redirectUrl configured for the React app in the Vantiq server's Keycloak server
* clientId:string - the clientId configured for the React app in the Vantiq server's Keycloak server

This function is called to allow the user to authenticate against the Keycloak OAuth server associated with the Vantiq server. It should be called in either of two circumstances: (1) the `init` function's return object's `authValid` property is false; or (2) any other API returns a reject promise with a statusCode of 401 (HTTP Unauthorized). Use this function when the `init` function's response object's `serverType` is "OAuth".

The promise returns a JSON object on success of the same format as described by the `init` function above.

##### authWithInternal() - prompt the user for Vantiq Internal authentication credentials

```js
authWithInternal(username:string, password:string):Promise<string>
```

* username:string - the user-supplied username
* password:string - the user-supplied password

This function is called after the React app displays a UI to prompt the user for previously established credentials.  It should be called in either of two circumstances: (1) the `init` function's return object's `authValid` property is false; or (2) any other API returns a reject promise with a statusCode of 401 (HTTP Unauthorized). Use this function when the `init` function's response object's `serverType` is "Internal".

The promise returns a JSON object on success of the same format as described by the `init` function above.

#### User Creation Functions
##### createOAuthUser() - create a new user when using an OAuth-based Vantiq Server

```js
createOAuthUser(urlScheme:string, clientId:string):Promise<string>
```
* urlScheme:string - the redirectUrl configured for the React app in the Vantiq server's Keycloak server
* clientId:string - the clientId configured for the React app in the Vantiq server's Keycloak server

This function is called if the React app needs to create a new Vantiq user when using an OAuth-based Vantiq server.

**Important notes:** this function depends on the presence of a Vantiq Service, `com.vantiq.ReactUtilities`, that is present in the Namespace specified when calling the `init` function. Please contact Vantiq support to obtain a Project export that contains the `com.vantiq.ReactUtilities` Service. It is also required that the user that imports this Project export needs to have Namespace Admin privileges.

The promise returns a JSON object on success of the same format as described by the `init` function above.

##### createInternalUser() - create a new user when using an Internal Authorization Vantiq Server

```js
createInternalUser(username:string, password:string):Promise<string>
```
* username:string - the user-supplied username
* password:string - the user-supplied password

This function is called if the React app needs to create a new Vantiq user when using an Internal Authorization-based Vantiq server. It should be called after the React app displays a UI to prompt the user for username and password credentials. 

**Important notes:** this function depends on the presence of a Vantiq Service, `com.vantiq.ReactUtilities`, that is present in the Namespace specified when calling the `init` function. Please contact Vantiq support to obtain a Project export that contains the `com.vantiq.ReactUtilities` Service. It is also required that the user that imports this Project export needs to have Namespace Admin privileges.

The promise returns a JSON object on success of the same format as described by the `init` function above.

#### Database Functions
##### select() - return an array of database records as specified by the parameters

```js
select(type:string, props:string[], where:any, sortSpec:any, limit:number):Promise<string>
```

* type:string - the name of the Vantiq Type for which to return records
* props:string[] - any array of property names associated with the Type to return. May be null if all properties for each record should be returned.
* where:any - a JSON object that contains property name(s) associated with the Type as keys and values for those keys to filter which records are returned. May be null if all records should be returned regardless of the value of its properties. Please consult the [where parameter documentation](api.md#where-parameter) for details as to the format of this JSON object.
* sortSpec:any - a JSON object that contains a property name associated with the Type as a key and either 1 or -1 as the value to determine the sort order of the records returned.
* limit:number - limit the maximum number of records to be returned. Use a value of 0 (zero) to indicate no limit

The promise returns an array of JSON objects on success.

##### selectOne() - return a single database record as specified by the parameters
```js
selectOne(type:string, id:string):Promise<string>
```
* type:string - the name of the Vantiq Type for which to return the record
* id:string - the value of the `_id` property for the desired record of that Type

The promise returns a single JSON object on success.

##### count() - return the number of database records as specified by the parameters
```js
count(type:string, where:any):Promise<string>
```
* type:string - the name of the Vantiq Type for which to return the record count
* where:any - a JSON object that contains property name(s) associated with the Type as keys and values for those keys to filter which records are returned. May be null if all records should be returned regardless of the value of its properties.  Please consult the [where parameter documentation](api.md#where-parameter) for details as to the format of this JSON object.

The promise returns a number of records on success.

##### insert() - creates a new record of the given Type
```js
insert(type:string, object:any):Promise<string>
```
* type:string - the name of the Vantiq Type to insert
* object:any - a JSON object with properties that correspond to Type properties

The promise returns a single JSON object representing the record inserted, including added properties such as `_id`.

##### update() - updates an existing record of the given Type and ID
```js
update(type:string, id:string, object:any):Promise<string>
```
* type:string - the name of the Vantiq Type to update
* id:string - the value of the `_id` property to for the record to be updated
* object:any - a JSON object with properties that correspond to Type properties

This function supports partial updates meaning that only the properties provided are updated. Any properties not specified are not changed in the underlying record.

The promise returns a single JSON object representing the record updated.

##### upsert() - create a new record or update an existing record of the given Type
```js
upsert(type:string, object:any):Promise<string>
```
* type:string - the name of the Vantiq Type to create or update
* object:any - a JSON object with properties that correspond to Type properties

This function either creates or updates a record in the database depending if the record already exists. The method tests for existence by looking at the natural keys defined on the Type. Each natural key property must be present in the `object` parameter.

The promise returns a single JSON object representing the record created or updated.

##### deleteWhere() - removes record(s) of the given Type given a constraint
```js
deleteWhere(type:string, where:any):Promise<string>
```
* type:string - the name of the Vantiq Type to create or update
* where:any - a required JSON object that contains property name(s) associated with the Type as keys and values for those keys to filter which records are deleted.  Please consult the [where parameter documentation](api.md#where-parameter) for details as to the format of this JSON object.

The promise has no return value on success.

##### deleteOne() - removes a record of the given Type with the given ID
```js
deleteOne(type:string, id:string):Promise<string>
```
* type:string - the name of the Vantiq Type to delete
* id:string - the value of the `_id` property to delete

The promise has no return value on success.

#### Procedure Execution Functions

##### executeByPosition() - execute the given Procedure with an array of parameter values
```js
executeByPosition(procedureName:string, params:any[]):Promise<string>
```
* procedureName:string - the name of the Procedure, including its package prefix if there is one
* params:any[] - an array of values corresponding to the parameters of the Procedure. The order of the parameter values in the array must match the order of the parameters in the Procedure declaration. May be null if there are no parameters.

The promise returns the return value of the Procedure on success.

##### executeByName() - execute the given Procedure with an object of parameter values
```js
executeByName(procedureName:string, params:any):Promise<string>
```
* procedureName:string - the name of the Procedure, including its package prefix if there is one
* params:any - a JSON object of keys corresponding to the name of each parameter and values corresponding to the parameter value for each key. May be null if there are no parameters.

The promise returns the return value of the Procedure on success.

##### executePublicByPosition() - execute the given public Procedure with an array of parameter values
```js
executePublicByPosition(namespace:string, procedureName:string, params:any[]):Promise<string>
```
* namespace:string - the Namespace that contains the specified Procedure to execute
* procedureName:string - the name of the Procedure, including its package prefix if there is one
* params:any[] - an array of values corresponding to the parameters of the Procedure. The order of the parameter values in the array must match the order of the parameters in the Procedure declaration. May be null if there are no parameters.

The given Procedure must be marked as a public Procedure.

The promise returns the return value of the Procedure on success.

##### executePublicByName() - execute the given public Procedure with an object of parameter values
```js
executePublicByName(namespace:string, procedureName:string, params:any):Promise<string>
```
* namespace:string - the Namespace that contains the specified Procedure to execute
* procedureName:string - the name of the Procedure, including its package prefix if there is one
* params:any - a JSON object of keys corresponding to the name of each parameter and values corresponding to the parameter value for each key. May be null if there are no parameters.

The given Procedure must be marked as a public Procedure.

The promise returns the return value of the Procedure on success.

##### executeStreamedByPosition() - execute the given streaming Procedure with an array of parameter values
```js
executeStreamedByPosition(procedureName:string, params:any[], progressEvent:string, maxBufferSize:number, maxFlushInterval:number):Promise<string>
```
* procedureName:string - the name of the Procedure, including its package prefix if there is one
* params:any[] - an array of values corresponding to the parameters of the Procedure. The order of the parameter values in the array must match the order of the parameters in the Procedure declaration. May be null if there are no parameters.
* progressEvent:string - the name of a React Event for which a Native Event Emitter call to `addListener` has been made.
* maxBufferSize:number - the maximum size of data (in bytes) produced by the Procedure before a React Event is produced. The default is 512.
* maxFlushInterval:number - the maximum number of milliseconds before a React Event is produced containing the accumulated data produced by the Procedure. The default is 5000 milliseconds.

Intermediate results of Procedure execution are sent to the React Event handler named in the `progressEvent` parameter. The data is a JSON object with some or all of the following properties:

* rawData:string - the data received so far, represented as a string
* data:any - the parsed data received so far, if the data can be parsed. The data may not be parsable because intermediate results may not contain enough information to complete parsing. If this property is not present, it means the data cannot be parsed and the `rawData` property should be consulted instead.
* isComplete:boolean - indicates whether this is an intermediate or a final result
* chunksReceived:number - the number of intermediate results sent
* totalRowsReceived:number - if the data received is an array, the total number of array elements received
* newRowsReceived:number - if the data received is an array, the number of array elements received since the last intermediate result
* firstNewRowIndex:number - if the data received is an array, the index of the first element of the most-recently received data
* error:any - if request returned an error, this JSON object will contain error details

Please reference the `registerSupportedEvents` function below for more information about registering and receiving React Events.

The promise returns a JSON object in the format described for the intermediate results above on success.

##### executeStreamedByName() - execute the given streaming Procedure with an object of parameter values
```js
executeStreamedByName(procedureName:string, params:any, progressEvent:string, maxBufferSize:number, maxFlushInterval:number):Promise<string>
```
* procedureName:string - the name of the Procedure, including its package prefix if there is one
* params:any - a JSON object of keys corresponding to the name of each parameter and values corresponding to the parameter value for each key. May be null if there are no parameters.
* progressEvent:string - the name of a React Event for which a Native Event Emitter call to `addListener` has been made.
* maxBufferSize:number - the maximum size of data (in bytes) produced by the Procedure before a React Event is produced. The default is 512.
* maxFlushInterval:number - the maximum number of milliseconds before a React Event is produced containing the accumulated data produced by the Procedure. The default is 5000 milliseconds.

Intermediate results of Procedure execution are sent as described in the `executeStreamedByPosition` function above.

The promise returns a JSON object in the format described for the intermediate results above on success.

#### Publishing Functions
##### publishEvent() - publish a message to a given resource
```js
publishEvent(resource:string, resourceId:string, message:any):Promise<string>
```
* resource:string - the resource on which to publish, must be one of 'topics', 'sources', or 'services'
* resourceId:string - the resource instance on which to publish. For Topics, it is a slash-delimited string; for Sources, it is the Source name; for Services, it is of the form '&lt;serviceName&gt;/&lt;inboundEventName&gt;'.
* message - a JSON object message to publish

The promise has no return value on success.

##### publish() - publish a message to a Vantiq topic
```js
publish(topic:string, message:any):Promise<string>
```
* topic:string - the topic on which to publish, must start with a '/'.
* message:any - a JSON object message to publish

`publish` is a special case of `publishEvent`.

The promise has no return value on success.

#### Miscellaneous Functions
##### registerForPushNotifications() - register for mobile push notifications
```js
registerForPushNotifications():Promise<string>
```

This function registers a mobile app to receive push notifications using either Apple Push Notification Service (APNS) for iOS or Firebase for Android. It must be called after (1) iOS or Android-specific code is executed to register for APNS or Firebase and (2) the user has valid authentication credentials.

The promise has no return value on success.

##### registerSupportedEvents() - register to receive React Events
```js
registerSupportedEvents(eventNames:string[]):void
```
* eventNames:string[] - a list of the names of React Events expected to be received by the React app

This function is used to register the names of React Events that are used before creating Native Event Emitters. If you are implementing push notifications, one required event name to register is 'pushNotifications'. Here is an example of how to register for and receive push notification events:

```js
VantiqReact.registerSupportedEvents(["pushNotification"]);
let notifyListener = eventEmitter.addListener("pushNotification", event => {
    console.log(JSON.stringify(event,null,3)) 
});
```
The `notifyListener` function will be called whenever a push notification is received that is not already automatically handled. The type of push notification may be found in the `event.type` property, which contains one of four string values when using the Vantiq collaboration tasks in Visual Event Handlers: 'update', 'chat', 'locationTracking' and 'locationRequest'. 'locationTracking' and 'locationRequest' types are automatically handled. 'update' is associated with a Visual Event Handler's Notify task and contains information about a Client associated with the task. 'chat' is associated with a Visual Event Handler's Chat task and contains information about a chat message. It is up to the React app to decide how to handle 'update' and 'chat' push notification types, if at all.

Please note that any listeners created by the `addListener` function must be removed when the React app is closed. Here is an example of how to remove the `notifyListener`:

```js
// Removes the event listeners once unmounted
return () => {
    notifyListener.remove();
};
```

This function has no return.
  
### Sample iOS AppDelegate.m File

```objectivec
#import "AppDelegate.h"
#import <UserNotifications/UserNotifications.h>
#import "VantiqUI.h"
#import "LastActive.h"
#import "VantiqReact.h"

#import <React/RCTBundleURLProvider.h>

// our globally-available Vantiq UI bridge variables
extern VantiqUI *vui;
extern NSString *APNSDeviceToken;

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
  self.moduleName = @"VantiqReactExample";
  // You can add your custom initial props in the dictionary below.
  // They will be passed down to the ViewController used by React Native.
  self.initialProps = @{};
  
  // allow the user to select which type of notifications to receive, if any
  UNUserNotificationCenter *center = [UNUserNotificationCenter currentNotificationCenter];
  center.delegate = (id<UNUserNotificationCenterDelegate>)self;
  [center requestAuthorizationWithOptions:(UNAuthorizationOptionSound | UNAuthorizationOptionAlert | UNAuthorizationOptionBadge)
      completionHandler:^(BOOL granted, NSError * _Nullable error){
      if (error) {
          NSLog(@"Error in registering for notifications: %@", [error localizedDescription]);
      } else {
          dispatch_async(dispatch_get_main_queue(), ^ {
              // register for an APNS token
              [[UIApplication sharedApplication] registerForRemoteNotifications];
          });
      };
  }];

  return [super application:application didFinishLaunchingWithOptions:launchOptions];
}

- (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)deviceToken {
    // remember token for use in registering it with the Vantiq server
    APNSDeviceToken = [VantiqUI convertAPNSToken:deviceToken];
    NSLog(@"APNSDeviceToken = %@", [VantiqUI convertAPNSToken:deviceToken]);
}

- (void)application:(UIApplication *)application didFailToRegisterForRemoteNotificationsWithError:(nonnull NSError *)error {
    NSLog(@"Failed to receive token: %@", [error localizedDescription]);
}

- (void)application:(UIApplication *)application didReceiveRemoteNotification:(nonnull NSDictionary *)userInfo
  fetchCompletionHandler:(void (^)(UIBackgroundFetchResult))fetchCompletionHandler {
  NSLog(@"didReceiveRemoteNotification: userInfo (state = %ld) = %@", application.applicationState, userInfo);
  if (vui) {
      [vui processPushNotification:userInfo completionHandler:^(BOOL notificationHandled) {
          if (notificationHandled) {
              NSLog(@"didReceiveRemoteNotification: calling completion handler.");
              fetchCompletionHandler(UIBackgroundFetchResultNewData);;
          } else {
              // this notification must be handled (or not) by the app
              id notifyData = [userInfo objectForKey:@"data"];
              if (notifyData) {
                  NSString *dataType = [notifyData objectForKey:@"type"];
                  NSLog(@"didReceiveRemoteNotification: unhandled notification type = '%@'.", dataType);
                
                  // forward the notify data to the React Native app
                  // see https://github.com/facebook/react-native/issues/15421
                  VantiqReact *vr = [VantiqReact allocWithZone:nil];
                  [vr sendEventWithName:@"pushNotification" body:notifyData];
              }
              fetchCompletionHandler(UIBackgroundFetchResultNewData);
          }
      }];
  } else {
      // user hasn't logged in so nothing to do yet
      fetchCompletionHandler(UIBackgroundFetchResultNoData);
  }
}

- (void)application:(UIApplication *)application performFetchWithCompletionHandler:(void (^)(UIBackgroundFetchResult))fetchCompletionHandler {
    if (vui) {
        // do our background tasks and call the completion handler when we're finished
        [vui doBFTasksWithCompletionHandler:NO completionHandler:^(BOOL notificationHandled) {
            fetchCompletionHandler(UIBackgroundFetchResultNewData);
        }];
    }
}

- (void)applicationDidEnterBackground:(UIApplication *)application{
    [[LastActive sharedInstance] enterBackground];
}

- (void)applicationWillEnterForeground:(UIApplication *)application{
    [[LastActive sharedInstance] enterForeground];
}

- (NSURL *)sourceURLForBridge:(RCTBridge *)bridge
{
  return [self bundleURL];
}

- (NSURL *)bundleURL
{
#if DEBUG
  return [[RCTBundleURLProvider sharedSettings] jsBundleURLForBundleRoot:@"index"];
#else
  return [[NSBundle mainBundle] URLForResource:@"main" withExtension:@"jsbundle"];
#endif
}

@end
```


