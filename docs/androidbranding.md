#Branding the Vantiq Android Mobile App

This document provides guidance to a developer interested in customizing or rebranding the Vantiq Android app. The following sections discuss likely operations necessary to develop a new Android app based on the Vantiq version with the goal of submitting the new app to the Google Play Store.

Please note: this document assumes the reader is an experienced Android developer. Additionally, if customizing more than just images, the developer should be comfortable developing in Java and the Android SDK.


## Fork the Vantiq Android App Repository
The Vantiq Android app GitHub repository may be found [here](https://github.com/Vantiq/android). In order to maintain the ability to track changes in the Vantiq-maintained app version, the developer should fork the repository. There are many sources of information for learning how to keep a forked repository up to date with the original. Here is [one summary](https://stackoverflow.com/a/3903835/6309).

## Choose an Application Id (appId)

Before you begin you must choose a unique 'appId' for your app, usually something like '_io.myCompany.myApp_'. This value must be plugged in various places in the instructions below. Once your app has been deployed this appId cannot be changed.

## Register Your Android App

To develop an Android app you must have a valid Google login. 

Before you can publish an app you must register it in the Google Play Store. Begin by going [here](https://play.google.com/apps/publish) and logging in.

On the "All Applications" page you will see a list of all the applications owned by your account; this list will be empty if you have not created an app before. To create a new app you must click the "Create Application" button. You will be asked to fill in a series of dialogs with a lot of information, most of which is used to create your listing page in the app store. This will include the app icon in a set of various sizes and some sample screenshots. You don't have to fill out all of this at once; you will be able to come back to it and edit in the missing pieces when you are ready to supply them.

When you are finished with this process you will have registered your app; now you need to build the app itself based on the Vantiq code in the "_android_" GitHub repository. 

## Create the Keystore

Before the app can be published it must be digitally signed; this involves creating a private key inside a Java "keystore" file. There are several ways to do this -

Here is a description of the process using Android Studio (or IntelliJ): [https://developer.android.com/studio/publish/app-signing](https://developer.android.com/studio/publish/app-signing) 

You can also do this using the "keytool" command from the command line: [http://blog.rabidgremlin.com/2015/11/06/how-to-create-a-private-key-for-signing-android-apps](http://blog.rabidgremlin.com/2015/11/06/how-to-create-a-private-key-for-signing-android-apps)


Both of these techniques will ask you to choose an "alias" and two passwords which you will need later; don't lose them!

You should call your keystore file "android.jks". When done this file should be copied into the "app" directory:

```
app/android.jks
```

## Create the 'keys.gradle' file

Next you must create a file called "keys.gradle" in the "app" directory. This contains information that points to the keystore file and the keys need to access it. The file must look like this:

```js
android {
    signingConfigs {
        config {
            keyAlias 'MyAlias'
            keyPassword 'MyKeyPassword'
            storeFile file('android.jks')
            storePassword 'MyStorePassword'
        }
    }
}
```

'MyAlias', 'MyKeyPassword' and 'MyStorePassword' must be replaced with the values you entered when creating the android.jks keystore file above.


## Customize the 'flavors.gradle' file

Next you will customize the "flavors.gradle" file which is also found in the "app" directory:

```js
android {
    productFlavors {

        //
        //  This is a special branding flavor for your custom app; you must replace "io.mypackage.app" with
        //  your chosen appId.
        //
        custom {
            dimension "brand"
            applicationId "io.mypackage.app"
        }
    }
}
```

The only thing you should change is to replace "io.mypackage.app" with the appId you chose above.

## Customize the FileProvider

Edit the file called app/src/custom/AndroidManifest.xml so it includes your appId in "authorities". Initially it looks like this:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
          package="io.vantiq.rcs">
    
    <application
            android:name=".VantiqApplication"
            android:allowBackup="true"
            android:icon="@drawable/appicon"
            android:label="@string/app_name"
            android:supportsRtl="true"
            android:theme="@style/AppTheme">

        <!-- The "authorities" attribute must contain the appid with '.fileprovider' appended -->
        <provider 
                android:name="android.support.v4.content.FileProvider"
                android:authorities="io.mypackage.app.fileprovider"    
                android:exported="false"
                android:grantUriPermissions="true">
            <meta-data
                    android:name="android.support.FILE_PROVIDER_PATHS"
                    android:resource="@xml/file_paths"/>
        </provider>
        
    </application>

</manifest>
```

Here you must edit "android:authorities="io.mypackage.app.fileprovider" by replacing "io.mypackage.app" with your appId.

## Setup Firebase and connect it to your app

The app uses Firebase as a mechanism to receive "push notifications" from the Vantiq server. In order to register your app to talk to Firebase you must follow the directions found [here](https://firebase.google.com/docs/android/setup) using "Option 1". The end result of this process will include a file called "google-services.json"; this file must copied here (overwriting the sample copy you find there):

```
app/src/global/custom/google-services.json
```

## Brand the app

Now you can begin the actual "branding" portion of this process by modifying various Vantiq-specific default settings. For example, you can override the  appicon (which represents the app on your phone's "home screen") and the icon shown in the "splash screen" when the app starts up. These should be changed by modifying the icons you find in the app/src/custom/res directories. There should be one variant of the icons for each screen resolution.

You can also customize the app message file (found in app/src/custom/res/values/strings.xml). You might want to do this if you need to replace any references to "Vantiq" with your own company name.

Various default colors can be adjusted by editing the file found here:

```
app/src/main/res/values/colors.xml
```

This file contains comments describing how the different color values are applied.

## Build the signed version of the app

When you are ready to build the APK for the app (so you can submit it to the Google Play Store) you can do that using Android Studio or from the command line using

```
gradle assembleGlobalCustomRelease

```

The resulting signed APK will be found here:

```
app/build/outputs/apk/globalCustom/release/app-global-custom-release.apk
```

This can be uploaded to the Play Store using the "Release management" / "App releases" page on the Google Play Console.


## Consumer Mode
Consumer Mode is a special type of branding that bypasses the normal Vantiq authentication views by specifying a dedicated Vantiq server URL, namespace and [Public Client](cbuser.md#public-clients) name. This allows the branded app to display a Public Client which implements self-registration. Once the Public Client has run and the user has authenticated, Consumer Mode also specifies a single dedicated, private Client to be run. No other functionality found in the existing Vantiq mobile app is available.

There is a source file which is used to control Consumer Mode:

    app/src/main/java/io/vantiq/rcs/misc/Configuration.java

This file allows you to set several different constant values which are used to modify the behavior of the Android app. 

To enable Consumer mode there is a boolean value called "isConsumer" which must be set to "true". If Consumer mode is "true" then you **must** also set these values as well:


* debugConsumerModeServer
* releaseConsumerModeServer

* debugConsumerModeNamespace
* releaseConsumerModeNamespace

* debugPublicClientName
* releasePublicClientName

* debugPrivateClientName
* releasePrivateClientName

These are used to set the hardcoded server, namespace, public Client and private Client which are required in Consumer mode. Note that for convenience there is both a "debug" and a "release" flavor of each value. This allows you to use one set of values during development ("debug") and a different set when building the app for deployment in the app store ("release").


There are a few other parameters that affect the operation of "geoFencing" which can be found in Configuration.java; refer to the comments for a description.


