# Push Notification Source Integration

A PUSH\_NOTIF (Push Notification) source represents a mechanism for sending Apple Push Notification (for Apple iOS) and Android Push Notification (for Android) messages to mobile apps. Apple push notifications use [Apple Push Notification Services](https://developer.apple.com/notifications/) (APNS) whereas Android push notifications use Google's [Firebase](https://firebase.google.com/).

## Define a PUSH\_NOTIF Source
A PUSH\_NOTIF source is created in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**. Use the **New Source** button to create a new source:

![Create MySource](../assets/img/mobile/mySource.png "Create MySource")

A PUSH\_NOTIF source contains the following properties:

* **Source Name**: the name of the source
* **Source Type**: select PUSH\_NOTIF from the pull-down menu
* **Target Vantiq Mobile App**: enable this checkbox to send specifically-formatted notification messages to the Vantiq iOS app (available from the Apple App Store) and the Vantiq Android app (available from the Google Play Store). Disable this checkbox to send notification messages to a custom iOS or Android app. By disabling this checkbox, some or all of the following properties must be configured.
* **Android App ID**: the app package name configured in the Android development environment. (Android-specific)
* **Firebase Server Key**: the server key obtained by registering your Android project on the Google [Firebase](https://firebase.google.com/) site. (Android-specific)
* **iOS App ID**: the app Bundle Identifier configured in your Xcode iOS project. (iOS-specific)
* **Send To APNS Development (Sandbox) Server**: enable this checkbox when your app is in development stages. Disable this checkbox when your app has been submitted and approved by the Apple App Store. (iOS-specific)
* **APNS PKCS12 File Password**: the password associated with the APNS-required PKCS12 certificate. That certificate is generated using the Keychain Access application on OS X.
* **PKCS12 File Contents**: Once the PKCS12 certificate has been generated (in .p12 format), use the following command to generate a Base64 encoded version which is then pasted into this property:

```sh
% openssl base64 -in cert.p12 -out outfile
```

## Sending Push Notifications
Once a PUSH\_NOTIF source is running, use the Vantiq built-in Notification.sendPayload procedure to send push notification messages. Please see the [Vantiq Client Builder User's Guide](../cbuser.md) for more details about how notifications are sent and interpreted by the Vantiq mobile apps.