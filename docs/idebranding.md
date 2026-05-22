#White-Labeling Vantiq

This article describes how to use the "white labeling" features of Vantiq to customize various "branding" aspects of the UI when deploying a "private cloud" server. The intent is to let a customer override references to the name "Vantiq" and its related branding and replace them with their own company's specific preferences. 

These customizations are in two basic categories:

First is the ability to replace company-specific strings like the name "Vantiq" and the link to the company website with values specific to your company. This involves customizing a set of string values in a server configuration file.

Second is the ability to modify the appearance of the "navbar" at the top of the Modelo. This includes things like changing the icon, colors and fonts that appear there.

These customizations are accomplished by configuring a "server configuration" file called `webUIConfig.json`. The location of this file is determined using the server's "configDir" startup parameter. After making changes to this file (or any file it refers to) you need to restart the server for the values to take effect.

> For installations deployed via Kubernetes see the branding example in the [Configuration Overrides](https://github.com/Vantiq/k8sdeploy_tools#configuration-overrides) section of the  documentation for details on how to manage these configuration files. (Note this is a link to the Vantiq "k8sdeploy_tools" GitHub repository and is only accessible to the Vantiq Professional Services group.)

Below is an example of a fully configured `webUIConfig.json`. Of course you only need to supply those values you wish to override:

```
{
  "loadGoogleComponents": true,

  "brandedProperties": "override.properties",
 
  "navbarDefaults": {
      "backgroundColor": "#1e6cb6",
      "titleColor": "#ffffff",
      "titleFontWeight": "400",
      "titleFontFamily": "'Source Sans Pro', Helvetica, Arial, sans-serif",
      "titleFontStyle": "normal",
      "titleFontSize": 20,
      "appicon": "myAppIcon.png",
      "icon": "myNavbarIcon.png",
      "iconHeight": 26,
      "iconWidth": 98,
      "height": 50,
      "titleTopPadding": 0,
      "iconTopPadding": 12
  }
}
```

### loadGoogleComponents

"loadGoogleComponents" is a boolean value which controls whether or not Google "map" libraries are included in Modelo and its Clients at runtime. You should set this to false if your private server does not have access to the internet.

### brandedProperties

"brandedProperties" points to a file in the  "Java properties" format that contains the values that you wish to override. These are a set of terms that contain Vantiq-specific values which you may wish to change.

Here is an unmodified version of the "override.properties file" that allows you to override the strings that contain various company-specific values. The meanings should mostly be obvious, but it is important to make clear the difference between "core.company.name" and "core.product.name"; the first refers to the name of the company itself and the second refers to the name of the product; for Vantiq these terms are the same but they are kept separate in case they differ in your case. 

```
core.company.name = Vantiq
core.product.name = Vantiq
core.privacy.policy = https://vantiq.com/wp-content/uploads/VANTIQ-Privacy-Policy.pdf
core.terms.and.conditions = http://vantiq.com/vantiq-terms-services
core.modelo.title = Vantiq - Modelo
core.pronto.title = Vantiq - Pronto
core.rtc.title = Vantiq Client Launcher
core.mpi.title = Vantiq Launcher
core.drp.title = Vantiq Request Processor
core.orgWebsite = http://www.vantiq.com
core.supportUrl = support@vantiq.com
core.forumUrl = http://stackoverflow.com/questions/tagged/vantiq
core.modelo.name = Modelo
core.modelo.full.name = Modelo Full
core.modelo.light.name = Modelo Light
core.pronto.name = Pronto
core.platform.name = Platform
core.configProntoMod = Configure Pronto and Modelo
```

### navbarDefaults

"navbarDefaults" is a configuration object containing values that tell the UI how to modify the default "navbar" styling. Some of these values correspond to properties on the runtime "Client" object.

<table style="width:auto;border-color:grey;border-width:2px;border-style:solid;font-size:12px;">
    <thead>
        <tr>
            <th>navbarDefaults</th>
            <th>‘Client’ properties</th>
            <th>Default</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>backgroundColor</td>
            <td>navBarBackgroundColor</td>
            <td>#1e6cb6</td>
            <td>The navbar background color</td>
        </tr>
        <tr>
            <td>titleColor</td>
            <td>navBarForegroundColor</td>
            <td>#ffffff</td>
            <td>The navbar title color</td>
        </tr>
        <tr>
            <td>titleFontWeight</td>
            <td>navBarTitleFontWeight</td>
            <td>400</td>
            <td>The navbar title font “weight” (‘bold’, ‘normal’, etc.)</td>
        </tr>
        <tr>
            <td>titleFontFamily</td>
            <td>navBarTitleFontFamily</td>
            <td>‘Source Sans Pro’, Helvetica, Arial, sans-serif</td>
            <td>The navbar title font family</td>
        </tr>
        <tr>
            <td>titleFontStyle</td>
            <td>navBarTitleFontStyle</td>
            <td>normal</td>
            <td>The navbar title font “style” (‘italic’, ‘normal’, etc.)</td>
        </tr>
        <tr>
            <td>titleFontSize</td>
            <td>navBarTitleFontSize</td>
            <td>20</td>
            <td>The navbar title font size in points</td>
        </tr>
        <tr>
            <td>appicon</td>
            <td>n/a</td>
            <td>webroot/cmn/assets/branding/appicon.png</td>
            <td>The browser ‘appicon’; must be 32x32</td>
        </tr>
        <tr>
            <td>icon</td>
            <td>navBarIcon</td>
            <td>webroot/cmn/assets/branding/navbarIcon.png</td>
            <td>The navbar icon</td>
        </tr>
        <tr>
            <td>iconHeight</td>
            <td>navBarIconHeight</td>
            <td>26</td>
            <td>The height of the navbar icon in pixels</td>
        </tr>
        <tr>
            <td>iconWidth</td>
            <td>navBarIconWidth</td>
            <td>98</td>
            <td>The width of the navbar icon in pixels</td>
        </tr>
        <tr>
            <td>height</td>
            <td>n/a</td>
            <td>50</td>
            <td>The height of the navbar in pixels</td>
        </tr>
        <tr>
            <td>titleTopPadding</td>
            <td>n/a</td>
            <td>0</td>
            <td>Extra top padding on the title</td>
        </tr>
        <tr>
            <td>iconTopPadding</td>
            <td>n/a</td>
            <td>12</td>
            <td>Extra top padding on the icon</td>
        </tr>
    </tbody>
</table>

