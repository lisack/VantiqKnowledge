# Client Styling User's Guide

## Introduction
"Clients" are a component of Vantiq's application development system. They are the piece that embodies an interaction with the end user by displaying and collecting information. The Vantiq [Client Builder](cbuser.md) allows the developer to build complex, multi-page Clients that run on both desktop browsers and the Vantiq mobile apps. The Client Builder has several ways to customize the look of the Client as a whole and individual widgets within the Client. This guide provides examples of how Clients and Client widgets may be styled to suit the needs of the Client user.

It is recommended that before reading this User's Guide that the developer completes the lessons in the [Client Builder Tutorial](tutorials/client.md). The examples in this guide use the Vantiq project created in the Client Builder Tutorial

## Client Themes
The easiest way to color and background style Clients is using the Client Builder's Theming feature. From the Client Builder pane:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![RunClient](assets/img/client/TutRunClient.png "Run Client")

use the **Properties** button to display the Client Properties dialog then click the _Theme_ tab:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![ThemeTab](assets/img/client/ThemeTab.png "Theme Tab")

There are seven built-in themes available in the **Theme** menu. The built-in themes affect only colors in the _General Colors_ and _Card Colors_ sections. The Client developer may change any of the colors in the _General Colors_ and _Card Colors_ as well as providing a background image in the _Background_ section. Once any of the theming properties have been changed, the **Theme** menu value changes to _Custom_ to indicate the Client theme is developer-defined and the **Save Theme** button appears in the lower-left of the Client Properties dialog. Click the **Save Theme** button to display the _Save Theme_ dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![SaveThem](assets/img/client/SaveTheme.png "Save Theme")

Name the theme and click the **Upload** button to upload the theme to the Vantiq documents store. The theme is saved to the _vantiq/themes/_ directory of the documents store, is available for any other Client in the Vantiq namespace, and can be downloaded and used in other Vantiq namespaces using the upload action from the Documents pane. The name of the theme also appears in the **Theme** menu whenever the Client Properties Theme tab is open.

The _Preview_ section on the right side of the Theme tab shows how a representative Client appears given the theme properties.

Be sure to use the **Save Changes** icon button (down arrow at the top, right of the Client pane) to save any Client Theme changes.

## Widget Styling
Each Client widget also has one or more style properties which are used to affect the look of the widget when the Client is running. To view and edit widget styling properties, click inside the widget when the Client is not running, then click the _Style_ category on the left side of the property sheet. For example, here are the Style properties available for the Data Table widget:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![WidgetProperties](assets/img/client/WidgetProperties.png "Widget Properties")

Every widget has a _CSS Class_ property. The next section, [Widget CSS Styling](#widget-css-styling), describes the use of this property.

All other Style properties are specific to the widget. Some widgets, such as the Data Table widget, have many such properties while other widgets, such as the Chat widget, have only two Style properties.

Changing Style properties on any particular widget applies those properties on only that instance of the widget. Those properties do not apply to other widgets of the same type. Changing any property value will usually be reflected visually immediately in the appearance of the widget so the developer can preview the effect of the change. However, some properties will only affect the widget appearance when the Client is running.

Be sure to use the **Save Changes** icon button (down arrow at the top, right of the Client pane) to save any widget style changes.

## Widget CSS Styling
While the per-widget Style properties are usually sufficient to change the appearance of widgets, sometimes the developer or user of the widget wants to make unusual styling property changes. As described in the previous [Widget Styling](#widget-styling) section, each widget has a _CSS Class_ property. [CSS (Cascading Style Sheets)](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) is a language standard for describing how HTML content appears. Client widgets use CSS to affect the appearance of the widget when running.

If the developer needs to apply custom CSS to widget(s), use the following steps:

* Upload a file containing CSS to the Vantiq document store. Use the IDE **Show** button to select **Advanced>Documents** to display the documents uploaded to the namespace:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Documents](assets/img/client/Documents.png "Documents")

* Either use the **New** button to create a new document with content type 'text/css' or use the **Upload** button to upload an existing CSS document.
 
* Add the uploaded CSS document to the Client. Use the **Properties** button of the Client to display the Client Properties dialog then click the _Basic_ tab:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![BasicTab](assets/img/client/BasicTab.png "Basic Tab")

* Use the _Custom Assets_ property to display the _Edit CSS and JavaScript Assets_ dialog:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![CustomAssets](assets/img/client/CustomAssets.png "Custom Assets")

* Use the **Add** ('+') button in the _CSS Assets_ section to create a new table entry, then use the **Select or Upload Document** (up arrow to cloud) to select the CSS document you uploaded in the first step.

When the Client is run, the CSS document is read and widgets that refer to its class definition are styled using the class properties. For example, if the developer wants all Button widgets to have a green background and their titles to be rendered in Times font, the CSS looks like the following:

```js
.vantiqButton {
	background-color: #00ff00 !important;
    font-family: Times;
}
```

since the default _CSS Class_ property for all Button widgets is _vantiqButton_. The first property, _background-color_, sets the button color to _#00ff00_ which specifies pure green and also contains _!important_ to make sure that all Client theming and widget styling is overridden. The second property, _font-family_, sets the font to _Times_ but doesn't need the _!important_ property since _font-family_ is not a property that's part of either Client theming or the Button widget's Style properties.

Be sure to use the **Save Changes** icon button (down arrow at the top, right of the Client pane) to save any custom assets changes.

Once one or more CSS documents have been referenced by a Client, the **CSS** button at the upper-right of the Client Builder pane becomes important:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;![Documents](assets/img/client/CSSButton.png "CSS Button")

To enable the **CSS** button, check the **Apply Custom CSS Assets** checkbox in the Client Properties>Advanced tab. Clicking the **CSS** button displays a menu of all CSS files added to the Client's _Custom Assets_ list. Clicking the edit icon next to the CSS file name allows the user to directly edit the CSS file. Once the user clicks the editor's OK button, the changes to the CSS are applied immediately to the Client. This editing feature makes styling Client widgets simple and quick by providing immediate feedback in how the Client looks.


## Client Navigation Bar Styling
The Client Launcher is a web app that allows the user to launch Clients outside the Client Builder environment. When a Client is run using the Client Launcher, it displays a navigation bar at the top of the browser window that uses the standard Vantiq styling. This navigation bar has extensive styling capabilities which are described in the [Customizing the Client Launcher](cbuser.md#launching-clients-from-a-browser) of the [Client Builder User's Guide](cbuser.md).


