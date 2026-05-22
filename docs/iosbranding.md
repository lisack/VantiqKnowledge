# Branding the Vantiq iOS Mobile App

This document provides guidance to a developer interested in customizing or rebranding the Vantiq iOS app. The following sections discuss likely operations necessary to develop a new iOS app based on the Vantiq version with the goal of submitting the new app to the Apple App Store.

Please note: this document assumes the reader is an experienced iOS developer. Additionally, if customizing more than just images, the developer should be comfortable developing in Objective-C.

## Fork the Vantiq iOS App Repository
The Vantiq iOS app GitHub repository may be found [here](https://github.com/Vantiq/iOS). (This is a private repository so you must contact Vantiq in order to obtain access to it.) In order to maintain the ability to track changes in the Vantiq-maintained app version, the developer should fork the repository. There are many sources of information for learning how to keep a forked repository up to date with the original. Here is [one summary](https://stackoverflow.com/a/3903835/6309).

## Open Xcode Workspace
The iOS project makes use of several third-party [CocoaPods](https://cocoapods.org/) pods for some of its functionality. Consequently, the project uses the Xcode [Workspace](https://developer.apple.com/library/archive/featuredarticles/XcodeConcepts/Concept-Workspace.html) _Vantiq-ios.xcworkspace_ rather than the Xcode project _Vantiq-ios.xcodeproj_. The workspace is located in the _Vantiq_ directory of the GitHub repository.

There is an additional workspace, _Vantiq-ios plus Watch.xcworkspace_, that has hooks for a companion Apple Watch app. This is an older version of the Vantiq app and is not currently in use.

## Modify the Project Settings
In order to submit the branded app to the Apple App Store, the developer must modify several settings in the _Vantiq-ios_ target. In the Xcode **Project Navigator**, navigate to the _Vantiq-ios_ target and select the **General** tab. Review and modify all appropriate properties (e.g. Display Name, Signing Team, App Icons, Launch Images, etc.).

## Replace Vantiq Related Images
The Vantiq app contains a Vantiq logo PNG format image with three scaled sizes for branding purposes. These images are used in the app's Launch Screen and in at least two more views (Choose Server and Select Namespace). The base image is 150px x 43px (Vantiq-150x43.png) with a transparent background. There are two additional sizes of this image (@2x, @3x) to support Retina displays. These images are found in the _Vantiq/Vantiq-ios/Images_ directory of the GitHub repository.

The easiest way to provide new brand-specific logos is to simply create similarly sized images using the same names as currently exist (i.e. _Vantiq-150x43.png_, _Vantiq-150x43&#64;2x.png_ and _Vantiq-150x43&#64;3x.png_) and replace the files found in the _Images_ directory.

## Change Fonts and Colors
There are two files related to overall app font and color use.

_Branding.h_, found in the _Vantiq/Vantiq-ios/Utilities_ directory, contains the definitions for the two different app Navigation Bar components (background, text and controls) in addition to the list cell background color. This file also contains the names of the bold and regular size fonts used throughout the app. The Vantiq version uses a font imbedded in the app, Source Sans Pro.

_Branding.m_, found in the same directory as _Branding.h_, uses the constants found in _Branding.h_ but contains some additional programmatic options such as default font sizes.

## Consumer Mode
Consumer Mode is a special type of branding that bypasses the normal Vantiq authentication views by specifying a dedicated Vantiq server URL, namespace and [Public Client](cbuser.md#public-clients) name. This allows the branded app to display a Public Client which implements self-registration. Once the Public Client has run and the user has authenticated, Consumer Mode also specifies a single dedicated, private Client to be run. No other functionality found in the existing Vantiq mobile app is available.

There is one file related to Consumer Mode, _Settings.m_, found in the _Vantiq/Vantiq-ios/Settings_ Xcode folder. To enable Consumer Mode, return **YES** in the _isConsumerMode_ function. To specify the dedicated Vantiq server URL, the namespace that contains the Public and private Client, and the Public and private Client names, alter the return values in the _consumerServer_, _consumerNamespace_, _consumerPublicClientName_ and _consumerPrivateClientName_.