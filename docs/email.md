# Email Source Integration

An email source represents an SMTP server with the express goal of sending messages to email accounts using an SMTP server. An email source ONLY supports publishing notifications.

## Define an Email Source

An Email source may be created in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**. Simply click the "New Source" button and enter the required information:

* Enter a name for your Source
* Select Source Type "EMAIL"
* Add a "Server" which should contain the endpoint for the SMTP server, e.g. mail.domain.com. The server is accessed in a secure manner using TLS (port 587) or SSL (port 465), depending on the URI port specification.
* Add a Server Port, the port to access to Server. The server is accessed in a secure manner using TLS (port 587) or SSL (port 465), depending on the given port.
* Enter the Username for your email account
* Enter the Password for your email account
* Click "Save"

Once registered the Email source will immediately be available to publish notifications as email messages.

An Email source may also be defined using the command-line interface by creating a JSON object of type ArsSource that represents the definition of the source and submitting the definition to Vantiq for registration. 

The EMAIL source configuration properties are:

* **host** - the host to use when connecting to the SMTP server.  This property is mandatory.
* **port** - the port to use when connecting to the SMTP server.  This property is mandatory.
* **username** - the name of the user used to authenticate with the SMTP server.
* **passwordType** - specifies the "type" of password that will be provided.  If the given value is "secret" then the password is interpreted as a resource reference to a [Vantiq Secret](../resourceguide.md#secrets).  Otherwise the password value is used as is.
* **password** - the password used to authenticate with the SMTP server (may be a resource reference).
* **from** - the default value to use as the "from" field using an email source to publish a [delegated request](../resourceguide.md#delegated-requests).  If not provided then the **username** will be used as the default "from" in this case.  NOTE -- this value is **not** used when using `PUBLISH` to [send email](#send-email-via-email-source).

In addition, it is also possible to specify any property supported by the [Vert.x MailConfig](https://vertx.io/docs/4.5.28/apidocs/io/vertx/ext/mail/MailConfig.html).

## Create EMAIL Source

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "MyEmailServer",
    "type": "EMAIL",
    "config": {
       "host": "mail.domain.com",
       "port": 587,
       "username": "vantiq",
       "password": "vantiq"
    }
}
```

Creates an EMAIL source with the SMTP server at the URI specified.

Alternatively, to use a secret password named "MySecret", change the password property to a reference and specify 'secret' as the passwordType like this:

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "MyEmailServer",
    "type": "EMAIL",
    "config": {
       "host": "mail.domain.com",
       "port": 587,
       "username": "vantiq",
       "password": "/system.secrets/MySecret",
       "passwordType": "secret"
    }
}
```

## Delete EMAIL Source

```json
DELETE https://dev.vantiq.com/api/v1/resources/sources/MyEmailServer
```
      
Deletes the email source created in the previous example.

## Send Email via EMAIL Source

Email is sent via an EMAIL source using the VAIL [`PUBLISH` statement](../rules.md#sending-to-an-external-system).  The *sendRequest* for EMAIL sources has the following properties:

* **from** - the email address of the sender (represented as a `String`).  This property is required.
* **to** - the email address(es) of the recipient(s) of the email.  This value may be either a `String` (for a single recipient) or an `Array` (for one or more recipients).  This property is required.
* **subject** - a `String` that represents the subject of the email message
* **text** - a `String` containing the body of the email message, permitting only text content
* **html** - a `String` containing the body of the email message, permitting HTML content

For example, the following VAIL statement can be used to send an email message:

```
PUBLISH { text: "The body of the message." } TO SOURCE MyEmailSource 
  USING { from: "me@mydomain.com", 
            to: [ "user1@domain.com", "user2@domain.com" ],
       subject: "The subject line" }
```