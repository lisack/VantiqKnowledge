# SMS Source Integration

An SMS source provides an interface to a Twilio account with the express goal of sending text messages to phones. An SMS source ONLY supports publishing notifications, not receiving text messages as input. 

In order to create an SMS source you must have an account with Twilio. If you do not already have an account you can go [here](https://www.twilio.com) to create one. 

As part of the Twilio signup process you will be assigned a "Live" Account SID and Auth Token. You will also be assigned a phone number which can be used as the "From" number when sending text. All 3 of these must be provided when creating the SMS Source. 

You do not need to provide Twilio with credit card information initially when just testing, but you will only be able to send SMS messages to phones which have been manually registered with Twilio. In order to send text to any arbitrary phone you will have to configure your Twilio account with a credit card, and you will be billed a small amount for each message sent.

## Define an SMS Source

An SMS source is defined in the [Vantiq IDE](../../../../) by using the **Add** button to select **Source...**. Simply click the "Create Source" button and enter the required information:

* Enter a name for your Source
* Select Source Type "SMS"
* Enter your "Live" Twilio Account SID
* Enter your "Live" Twilio Auth Token
* Enter your Twilio-assigned phone number
* Click "Save"

Once registered the SMS source will immediately be available to publish notifications as a text message.

An SMS source may also be defined using the command-line interface by creating a JSON object of type ArsSource that represents the definition of the remote source and submitting the definition to Vantiq for registration. The relevant ArsSource properties are as follows:

* **name** The name given the SMS source by the user
* **twilioAccountSID** Your Twilio Account SID
* **twilioAuthToken** Your Twilio Auth Token
* **twilioFromPhone** The phone number from which the text should seem to originate. This must be the number your were assigned when creating your Twilio account.

## Create SMS Source

```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "SmsSourceName",
    "type": "SMS",
    "config": {
       "twilioAccountSID": "<your twilio account SID>",
       "twilioAuthToken": "<your twilio auth token>",
       "twilioFromPhone": "555-1212"
    }
}
```
    
Creates a SMS source with the twilio credentials specified.

Alternatively, to use a secret twilioAuthToken named "MySecret", change the twilioAuthToken property to a reference and 
specify 'secret' as the twilioAuthTokenType like this:


```json
POST https://dev.vantiq.com/api/v1/resources/sources
{ 
    "name": "SmsSourceName",
    "type": "SMS",
    "config": {
       "twilioAccountSID": "<your twilio account SID>",
       "twilioAuthToken": "/system.secrets/MySecret",
       "twilioAuthTokenType": "secret",
       "twilioFromPhone": "555-1212"
    }
}
```


## Delete SMS Source

```json
DELETE https://dev.vantiq.com/api/v1/resources/sources/SmsSourceName
```

Deletes the SMS source created in the previous example.

## Publish Notifications via an SMS Service

Notifications are produced by the rules system when **PUBLISH** is called as a rule statement. The **PUBLISH** request for SMS sources takes three parameters: the source to which the publish is sent, the body of the text to be sent, and the publish parameters object. The SMS source will deliver the message to the specified phone number via your Twilio account.

For example, inside your rule you could use a line like this to send an SMS message:

```js
PUBLISH { body: "My Text Message Goes Here" } TO SOURCE MySmsSource 
  USING {   to: "+19255551212" }
```
  



