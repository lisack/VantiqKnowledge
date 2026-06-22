# LLM Reference Guide

## Overview

This guide provides instructions for configuring Large Language Models (LLMs), for example configuring access to LLMs 
hosted in external systems such as AWS Bedrock, or enabling LLMs to use Tools. 


## AWS

Vantiq integrates with AWS SageMaker and Bedrock, allowing access to their hosted models. A list of available
models can be found in the IDE LLM creation pane, in the Model Name drop-down list.

When you choose a SageMaker or Bedrock model from the Model Name list, the user interface automatically 
displays the necessary fields for entering your AWS credentials:

- Region
- Access Key Id
- Secret Access Key
- Role Arn _(optional)_

The AWS credentials that you specify are used to access the model inference endpoint. For example, if you have
enabled access to a Bedrock model hosted in the `us-east-1` region, you must specify the same region in 
the Region field.

Note that all fields, except Region, are treated as confidential. These credentials are managed as
[secret](resourceguide.md#secrets) references and must be defined before you can use them in the LLM configuration. 

### SageMaker

To access a SageMaker model, you need to provide:

* **Model Name** -- either `sagemaker` for a generative model, or `sagemaker-embedding` for an embedding model.
* **AWS Credentials** -- enter these as detailed in the previous section.
* **Endpoint Name** -- the name of the SageMaker inference endpoint.
* **Message Format** -- the message format name or message format configuration defining the message syntax used to 
access the model.

For advanced settings, the Configuration field allows you to input a JSON document with specific parameters.
For example, a `Llama3-Chat` model configuration may look like this:

```
{
   "endpoint_kwargs": {
      "CustomAttributes": "accept_eula=true"
   },
   "model_kwargs": {
      "max_new_tokens": 350,
      "temperature": 0.1,
      "return_full_text": false
   }
}
```

Please refer to the model documentation to understand the available configuration options and proper format.

#### SageMaker Message Format

The Message Format specifies the expected syntax for all messages sent to the inference endpoint. 
This format encompasses two primary aspects:

- _Marshalling_: it sets the rules for converting a request text message (e.g., prompt) into a format that the inference
endpoint can process.
- _Unmarshalling_: it sets the rules for converting the response received from the inference endpoint.

For models available through SageMaker JumpStart, message format documentation can often 
be found in their associated Notebook as python examples. 

Many models, generative or embedding, use the following generic message syntax:

```
   request:    {"<request_key>": <input_value>, "<request_parameters_key>": model_kwargs}
   response:   response_json<response_path>
```

For example,

```
    request:   {"inputs": <input_value>, "parameters": model_kwargs}
    response:  response_json[0]["generated_text"]
```

or,

```
    request:   {"inputs": <input_value>, **model_kwargs}
    response:  response_json["vectors"]
```

You can configure the message format of any model following this generic syntax by specifying the configuration 
property `message_format_config`, and providing values for:

- `request_key`
- `request_nesting_level`
- `request_parameters_key`
- `response_path`

Both `request_nesting_level` and `request_parameters_key` are optional.

`request_nesting_level` is the number of nesting levels for `<input_value>`. 

For example,

```
    # request_nesting_level = 0  (default value)
    request: {"inputs": <input_value>, "parameters": model_kwargs}

    # request_nesting_level = 1
    request: {"inputs": [<input_value>], "parameters": model_kwargs}

    # request_nesting_level = 2
    request: {"inputs": [[<input_value>]], "parameters": model_kwargs}
```

#### Message Format Examples

Below are message format configuration examples from some of the models available through SageMaker JumpStart.

```text
# Falcon
#
# request:  {"inputs": <input_value>, "parameters": model_kwargs}
# response: response_json[0]["generated_text"]

{
    "message_format_config": {
        "request_key": "inputs",
        "request_parameters_key": "parameters",
        "response_path": "0,generated_text"
    }
}
```

```text
# GPTJ
#
# request:  {"text_inputs": <input_value>, **model_kwargs}
# response: response_json[0][0]["generated_text"]

{
    "message_format_config": {
        "request_key": "text_inputs",
        "response_path": "0,0,generated_text"
    }
}
```

```text
# Bloom
#
# request:  {"text_inputs": <input_value>, **model_kwargs}
# response: response_json["generated_texts"][0]

{
    "message_format_config": {
        "request_key": "text_inputs",
        "response_path": "generated_texts,0"
    }
}
```

```text
# Embedding
#
# request:  {"text_inputs": <input_value>, **model_kwargs}
# response: response_json["embedding"]

{
    "message_format_config": {
        "request_key": "text_inputs",
        "response_path": "embedding"
    }
}
```

#### Message Format Names 

To simplify the configuration of common message formats, Vantiq provides the following pre-defined names
that can be specified in the `Message Format Name` field:

- `llama2-chat`
- `llama3-chat`
- `mistral-instruct`
- `llama2`
- `llama3`
- `falcon`
- `mistral-instruct`
- `mistral`
- `bloom`
- `gptj`

All names except `llama2-chat`, `llama3-chat` and `mistral-instruct` are simple built-in aliases to generic syntax message 
format configurations, as described above. `llama2-chat`, `llama3-chat` and `mistral-instruct` require dedicated code specific
to the LLM model, so they do not rely on the generic syntax. 

If you do not find a configuration that matches your model, please contact Vantiq Support.

### Bedrock

To access a Bedrock model, you need to provide:

* **Model Name** -- select a name from the Model Name Bedrock drop-down list. A name corresponds to the Bedrock `modelId` prefixed with `bedrock/`,
  for example, `bedrock/meta.llama3-8b-instruct-v1:0`. If your desired model is not listed, you can manually enter it using the syntax `bedrock/<model-name>`, where `<model-name>` represents the Bedrock `modelId`.
* **AWS Credentials** -- enter these as detailed in the previous [AWS](#aws) section.

For advanced settings, the Configuration field accepts a JSON document containing model-specific parameters.
For example, to configure a variable-dimension embedding model, you might provide the following:

```
{
   "model_kwargs": {
      "dimensions": 256
   }
}
```

Please refer to each model documentation to understand the available configuration options and their proper format.

#### Custom Bedrock Configuration

Alternatively, instead of manually entering the Bedrock model using the syntax `bedrock/<model-name>`, you can specify a custom configuration. 

The custom configuration must be a JSON document with the following properties:

- **class_name** -- `vantiq.llms.ChatAWSBedrockConverse` for a generative model, or `vantiq.embeddings.BedrockEmbeddings` for an embedding model.
- **model_id** -- the Bedrock _modelId_ value, for example `meta.llama3-8b-instruct-v1:0`.
- **aws_region** -- the AWS region where the model is hosted.
- **aws_access_key_id** - the AWS access key id.
- **aws_secret_access_key** - the AWS secret access key.
- **aws_role_arn** - the AWS role arn _(optional)_.
- **model_kwargs** - a JSON document with the model-specific configuration parameters _(optional)_.

For example, 

```
{
   "class_name": "vantiq.llms.ChatAWSBedrockConverse",
   "model_id": "meta.llama3-8b-instruct-v1:0",
   "aws_region": "us-east-1",
   "aws_access_key_id": "@secrets(AWSAccessKeyId)",
   "aws_secret_access_key": "@secrets(AWSSecretAccessKey)",
   "max_tokens": 512,
   "temperature": 0.2
}
```

The UI field _API Key Secret_ should be left empty and the _Model Name_ field should contain your LLM name, for example `MyBedrockLLM`. Make sure to rely on the [secrets](sources/source.md#using-secrets) 
notation to protect the AWS credentials, as shown in the above example.

Note that manually specifying a model name and its configuration does not guarantee functionality. It is likely to work if the
model you are trying to configure is a variant of a supported model family. For example, 
if the Model Name Bedrock drop-down list includes `bedrock/meta.llama3-2-11b-instruct-v1:0` and you manually specify  
`bedrock/meta.llama3-2-90b-instruct-v1:0`, a custom configuration is likely to function correctly.

If the model you are trying to configure is not a variant of a supported model family, please contact Vantiq Support.

#### Embedding Models

If the Bedrock embedding model you want to use does not appear in the Model Name drop-down list, you can manually enter its name using the syntax `bedrock/<model-name>`. You must also specify the `Vector Size` and `Distance Function` properties.

For variable-dimension models, you may need to specify the vector dimension as an additional configuration property. 

For example, to configure an LLM for the variable-dimension embedding model `amazon.titan-embed-text-v2:0`, set the Model Name to `bedrock/amazon.titan-embed-text-v2:0`, set `Vector Size` to your desired dimension (e.g., 512), and include the following configuration:

```text
{
   "model_kwargs": {
      "dimensions": 512
   }
}
```

Refer to the model’s documentation to determine the supported dimensions and the default dimension. If you are using the default dimension, you can omit the additional configuration and only set the `Vector Size`.

![Bedrock Embedding Configuration](assets/img/ai/BedrockEmbedding.png)

## Google

To specify a Google model, prefix the model name with `google-genai/`, for example `google-genai/gemini-2.0-flash`.

### Embedding Models

Some Google embedding models support variable output dimensions, allowing you to select an embedding size that fits your use case. If the variable-dimension model you want to use appears in the Model Name drop-down list, simply specify the desired embedding size using the `Vector Size` property.

For example, assuming that the model `google-genai/models/gemini-embedding-001` is listed in the Model Name drop-down list, the following would produce embeddings of dimension 768. If no vector size was specified, this model would default to 3072.

![Gemini Embedding](assets/img/ai/GeminiEmbedding.png)

If the embedding model you want is not listed, you can manually enter its name using the syntax `google-genai/<model-name>`.

For variable-dimension models entered manually, you must specify the desired dimension in two places: the `Vector Size` property and the `output_dimensionality` configuration property. These values must match.

For instance, if the model from the example above were not listed, you would set `Vector Size` to 768 and also provide the following configuration:

```text
{
  "output_dimensionality": 768
}
```

### Safety Settings

Gemini models have built-in safety filters to prevent generating harmful or unsafe content.

To change the default safety filter settings, specify the property `safety_settings` in the LLM
configuration, providing a JSON document with a set of key-value pairs where the key is the filter category and the
value is the block level value.

For example,

```
{
    "safety_settings": {
      "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_LOW_AND_ABOVE",
      "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE"
   }
}
```

Gemini models support the following categories:

```
    HARM_CATEGORY_HARASSMENT
    HARM_CATEGORY_HATE_SPEECH
    HARM_CATEGORY_SEXUALLY_EXPLICIT
    HARM_CATEGORY_DANGEROUS_CONTENT
```

The block levels available are:

```
    BLOCK_LOW_AND_ABOVE
    BLOCK_MEDIUM_AND_ABOVE
    BLOCK_ONLY_HIGH
    BLOCK_NONE
```

## Azure

Vantiq integrates with Azure OpenAI, allowing access to OpenAI models deployed in Azure OpenAI Studio.

### OpenAI

To define an Azure OpenAI model using the IDE, you need to provide:

* **Model Name** -- `azure-openai` for a generative model, or `azure-openai-embedding` for an embedding model.
* **Azure Resource Name** -- the name of the Azure OpenAI resource.
* **Deployment Name** -- the name of the Azure OpenAI model deployment.
* **API Version** -- the API version of the model. You may refer to the [Azure documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference).
* **Credentials** -- the model access key (e.g., from _Keys and Endpoint_ in the OpenAI Azure resource Portal).

For a JSON definition format, you need to specify the model endpoint name (`azure_endpoint`), which is constructed from the 
Azure resource name: `https://<resource-name>.openai.azure.com/`

For example,

```
{
  "name": "AzureOpenAI",
  "modelName": "azure-openai",
  "type": "generative",
  "config": {
    "azure_deployment": "gpt-4o-dep",
    "openai_api_version": "2024-10-21",
    "azure_endpoint": "https://vq-open-ai.openai.azure.com/",
    "temperature": 0.1,
    "apiKeySecret": "AzureOpenAISecret"
  }
}
```

Where `vq-open-ai` is the Azure resource name, `gpt-4o-dep` is the deployment name, and `2024-10-21` is the API version.
A secret named `AzureOpenAISecret` holds the model access key.

If you are defining a configuration for an embedding model with configurable output dimensions, such as `text-embedding-3-large`, you must also specify the `dimensions` configuration property and ensure that the `Vector Size` property has the same value.

## NVIDIA NIM

Vantiq integrates with NVIDIA NIM, allowing access to models deployed with NVIDIA NIM.

To define an NVIDIA NIM generative or embedding model using the IDE, you need to provide:

* **Model Name** -- `nvidia-nim/<model>` where `<model>` is the name of the model.
* **Credentials** -- the NVIDIA NIM API Key.

For example,

![NVIDIA NIM Configuration](assets/img/ai/NvidiaNimLLM.png)

Where the model name is `mistralai/mixtral-8x7b-instruct-v0.1` and `NvidiaNimAPIKey` is the secret name for the NVIDIA NIM API Key.

The JSON definition for the above example is:

```json
{
  "name": "NvidiaNimLLM",
  "modelName": "nvidia-nim/mistralai/mixtral-8x7b-instruct-v0.1",
  "type": "generative",
  "description": "Mixtral model deployed with NVIDIA NIM",
  "config": {
    "apiKeySecret": "NvidiaNimAPIKey"
  }
}
```

## OpenAI

To specify an OpenAI model, prefix the model name with `openai/`, such as `openai/gpt-4o` or `openai/o3-mini`.

If you want to interface with a model compatible with OpenAI, you can specify the model using the syntax `openai/<model-name>` or create a custom model definition with the property 
`class_name` set to the OpenAI supporting class `vantiq.llms.ChatOpenAI`.

For example, let's assume that we are running a local `llama3` model using [_Ollama_](https://ollama.com/), which is compatible with the
OpenAI Chat Completions API. Based on the _Ollama_ documentation, the custom configuration would look like,

```
{
   "class_name": "vantiq.llms.ChatOpenAI",
   "model_name": "llama3.2:latest",
   "openai_api_base": "http://localhost:11434/v1",
   "openai_api_key": "unused"
}
```

Where `model_name` is the local model to use, `openai_api_base` (or `base_url`) is the _Ollama_ endpoint and the property `openai_api_key` (or `api_key`) is set to 
any value (it is ignored).

Because we create a custom LLM definition, the Model Name specified must be a descriptive name (e.g., llama3-model) 
and not a name from the suggested models list.

For example,
![OpenAI Configuration](assets/img/ai/CustomOpenAICompatible.png)

The above example can also be specified using a model name prefixed with `openai/`. In this case, 
the Model Name value would be `openai/llama3.2:latest` and since the `openai/` prefix is specified,
the custom configuration would omit the `class_name` property.

![OpenAI Configuration_2](assets/img/ai/CustomOpenAICompatible2.png)

The examples above are scoped as _Ollama_ examples. Depending on the use case, any other ChatOpenAI [configuration
property](https://api.python.langchain.com/en/latest/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html) might be used.

### Embedding Models

To use an OpenAI embedding model, select it from the Model Name drop-down list or enter it manually using the syntax `openai/<model-name>`, for example `openai/text-embedding-3-small`. 

Some OpenAI embedding models, such as `text-embedding-3-small` and `text-embedding-3-large`, support variable output dimensions, allowing you to select an embedding size that fits your use case. Specify the desired size using the `Vector Size` property.

If the variable-dimension model appears in the Model Name drop-down list, simply set the `Vector Size` property. The server recognizes the model and automatically adds the required `dimensions` configuration based on the value you provide, so you do not need to specify it yourself. If no vector size is specified, the model's default size is used (1536 for `text-embedding-3-small` and 3072 for `text-embedding-3-large`).

If the variable-dimension model you want is not listed, you can still enter it manually using `openai/<model-name>`. In this case, you must specify the desired dimension in two places: the `Vector Size` property and the `dimensions` configuration property. These values must match.

For instance, to use a non-listed variable-dimension model with an embedding size of 512, set `Vector Size` to 512 and provide the following configuration:

```text
{
  "dimensions": 512
}
```

### Image Generation

To use a GPT Image Generation model, for example gpt-image-1.5, you must define an LLM generative model that uses the OpenAI Responses API and specifies the image model as a built-in `image_generation` tool. The mainline model is defined as a text-capable model, such as gpt-4.1 or gpt-5. The mainline model decides when and how to generate or edit an image based on your prompt, and the tool `action` parameter controls whether that choice is automatic or forced to generation or editing; it defaults to `auto`.

For example, using models from the mini family,

![OpenAI Image Generation Configuration](assets/img/ai/OpenAIGenImage.png)

with Configuration:

```
{
   "use_responses_api": true,
   "output_version": "responses/v1",
   "model_kwargs": {
      "tools": [
         {
            "type": "image_generation",
            "model": "gpt-image-1-mini",
            "size": "1024x1024",
            "quality": "low",
            "output_format": "jpeg"
         }
      ]
   }
}
```

Please refer to the OpenAI documentation for more details on the available image generation models and `image_generation` tool configuration options.

#### Image reference

To specify an image reference in the prompt, you can provide a publicly accessible image URL, a Vantiq [Document](resourceguide.md#documents) or [Temp Blob](resourceguide.md#tempblobs) reference, or an OpenAI file id (a reference to an image file uploaded to OpenAI).  A Document or Temp Blob reference — for example, a frame captured from a [Video Source](sources/video.md) — is materialized and submitted as part of the prompt, subject to the `documentExpansion` quota.

The recommended, vendor-agnostic way to reference an image is the *flat* `image` content type, whose `url` may be a URL or a Document/Temp Blob reference:

```
var msg = io.vantiq.ai.ChatMessage.buildHumanMessage([
    {type: "text", text: "Convert the image to grayscale."},
    {type: "image", url: "system.documents/myImage.png"}
])
```

Provider-specific syntaxes are also accepted.  OpenAI's chat/completions form takes the URL or reference in `image_url.url`:

```
var msg = io.vantiq.ai.ChatMessage.buildHumanMessage([
    {type: "text", text: "Convert the image to grayscale."},
    {type: "image_url", image_url: {url: "https://example.com/image.png"}}
])
```

and its responses-API form accepts either an `image_url` (URL or reference) or a `file_id` for an image uploaded to OpenAI:

```
var msg = io.vantiq.ai.ChatMessage.buildHumanMessage([
    {type: "text", text: "Convert the image to grayscale."},
    {type: "input_image", file_id: fileId}
])
```

To upload an image document to OpenAI and get a fileId value, you can define a REMOTE source and create a procedure that triggers the upload and returns the file id of the uploaded image. 

For example, assuming a package `some.example` with a service named `ImageService` and a REMOTE source named `OpenAI_FileUpload`,

```
package some.example
stateless PROCEDURE ImageService.publishImageAsOpenAIFile(imageName String)

var rRef = "system.documents/" + imageName

var ret = SELECT ONE FROM SOURCE OpenAI_FileUpload WITH 
			method: "POST",
            parts: [ { name: "purpose", content: "vision" },
                     { name: "file", filename: imageName, ref: rRef, 
                       contentType: "image/jpeg" }]

if (ret && ret.id) {
    // Return OpenAI file id
    return ret.id
} else {
    exception("file.upload.error", "Failed uploading file {0) to OpenAI ", [imageName])
}
```

The REMOTE source `OpenAI_FileUpload` is configured to upload files to the OpenAI file endpoint (`/v1/files`). The source credential type must be set to `Access Token` and reference an OpenAI API key, stored as a Vantiq [Secret](resourceguide.md#secrets) (_menu Administer > Advanced > Secrets_).

```
{
    "accessTokenType": "secret",
    "accessToken": "/system.secrets/OpenAIKey",
    "uri": "https://api.openai.com/v1/files"
}
```

#### Multi-turn editing

Some image generation models can refine a previously generated image over multiple turns.  With OpenAI's Responses API this is done by passing the `previous_response_id` of the prior generation back to the model on the next call.

Because `previous_response_id` is provider-specific and is not part of the standard model interface, you declare it in the LLM configuration using `extra_request_params`.  This is a list of parameter names that, when supplied in the GenAI Procedure's `config` argument (the flow's [runtime configuration](genaibuilder.md#runtime-configuration)), are forwarded as-is to the inference endpoint:

```
{
   "use_responses_api": true,
   "output_version": "responses/v1",
   "model_kwargs": {
      "tools": [
         {
            "type": "image_generation",
            "model": "gpt-image-1",
            "size": "1024x1024",
            "quality": "low",
            "output_format": "jpeg"
         }
      ]
   },
   "extra_request_params": ["previous_response_id"]
}
```

To use the model, build a GenAI Flow whose [LLM component](genaibuilder.md#llm) runs this image-generation LLM, and set that component's **output type** to `None` so the flow returns the full [ChatMessage](rules.md#chatmessage).  This preserves the response `id` (needed to continue the exchange) and the generated image, which is returned in the message content as an `image_generation_call` part whose `result` holds the base64-encoded image.  Expose the flow as a [GenAI Procedure](services.md#genai-procedures) — `ImageService.genImageFlow` in the examples below.

The following procedure generates an image, saves it as a [Document](resourceguide.md#documents), and returns the response `id` so the image can be edited in a later turn:

```
package org.test
stateless PROCEDURE ImageService.genImage()

var msg = io.vantiq.ai.ChatMessage.buildHumanMessage([
    {type: "text", text: "Create a picture of a mouse flying over the moon."}
])

var response = ImageService.genImageFlow([msg])
var ret = "no image saved"

for (part in response.content) {
    if (part.type == "image_generation_call") {
        var image_base64 = part.result
        UPSERT system.documents(name: "myTestImage.jpg", content: Decode.base64Raw(image_base64), fileType: "image/jpg")
        ret = "image saved as myTestImage.jpg - response Id: " + response.id + " - imageId: " + part.id
    }
}

return ret
```

To continue editing, call the flow again with that response `id`, which gets passed as `previous_response_id` in the `config` argument:

```
package org.test
stateless PROCEDURE ImageService.editImage_FromResponseId(responseId String required, prompt String)

if (prompt == null) {
    prompt = "Change the image to be black and white"
}

var msg = io.vantiq.ai.ChatMessage.buildHumanMessage([
    {type: "text", text: prompt}
])

var response = ImageService.genImageFlow([msg], {previous_response_id: responseId})
var ret = response

for (part in response.content) {
    if (part.type == "image_generation_call") {
        var image_base64 = part.result
        UPSERT system.documents(name: "myTestImageEdited.jpg", content: Decode.base64Raw(image_base64), fileType: "image/jpg")
        ret = "image saved as myTestImageEdited.jpg"
    }
}

return ret
```

The same `extra_request_params` mechanism can forward any other provider-specific parameter that is not part of the standard model interface.

## Anthropic

Vantiq integrates with Anthropic, allowing access to Claude generative models.

To define an Anthropic model using the IDE, you need to provide:

* **Model Name** -- `anthropic/<model>` where `<model>` is the Anthropic model name, for example `anthropic/claude-sonnet-4-6`.
* **Credentials** -- the Anthropic API Key.

For example, an Anthropic model can be defined as:

```json
{
  "name": "ClaudeLLM",
  "modelName": "anthropic/claude-sonnet-4-6",
  "type": "generative",
  "description": "Claude model from Anthropic",
  "config": {
    "apiKeySecret": "AnthropicAPIKey"
  }
}
```

## HuggingFace

Vantiq integrates with HuggingFace embedding models. Unlike the other providers, a HuggingFace model runs locally on the Vantiq server — the model is downloaded from [huggingface.co](https://huggingface.co) the first time it is used, cached on the server, and run in-process. No API key is required, but the server needs outbound access to `huggingface.co` for the initial download.

To define a HuggingFace model using the IDE, you need to provide:

* **Model Name** -- `huggingface/<model>` for a model from the `sentence-transformers` organization (for example, `huggingface/all-MiniLM-L12-v2`), or `huggingface/<org>/<model>` for a model hosted under any other HuggingFace Hub organization (for example, `huggingface/BAAI/bge-large-en-v1.5`). A bare model name is resolved against the `sentence-transformers` organization, so models from other organizations must use the `<org>/<model>` form.
* **Vector Size** -- the output dimension of the embedding model. For well-known `sentence-transformers` models this is set automatically and may be omitted; for any other model you must set it to match the model's output dimension.

For example, a HuggingFace model can be defined as:

```json
{
  "name": "HuggingFaceEmbedder",
  "modelName": "huggingface/all-MiniLM-L12-v2",
  "type": "embedding"
}
```

For a model that is not one of the well-known `sentence-transformers` models, set the `Vector Size` property to match its output dimension:

```json
{
  "name": "BgeEmbedder",
  "modelName": "huggingface/BAAI/bge-large-en-v1.5",
  "type": "embedding",
  "vectorSize": 1024
}
```

## Usage

### Configuration

LLMs can be customized using configuration parameters such as `temperature`, `top_p`, or `max_tokens`. 
Although these parameters generally have the same function across different LLMs, not all models expose the same 
parameters in the same manner. A parameter might be unavailable or its syntax could differ between models.

While Vantiq tries to normalize the configuration parameter names across the LLMs it supports,  
the LLM documentation should always be consulted as the definitive source for configuration syntax and availability.

For example, OpenAI expects a configuration property `max_tokens` while a specific Bedrock model might expect `model_kwargs.max_tokens`.

Both LLM configuration property and runtimeConfig property (e.g., [submitPrompt](rules.md#llm)) 
expect the same configuration syntax.

For example, let's assume that we have the following LLM configuration:

```
{
    "model_kwargs": {
        "maxTokenCount": 1024
    }
}
```

If we want to override this default LLM configuration with a lower value for the time of a `submitPrompt` call, 
we would provide a `runtimeConfig` value that would have the same syntax:

```
{
    "model_kwargs": {
        "maxTokenCount": 256
    }
}
```

Note that Vantiq tries to normalize the configuration parameter names across the LLMs it supports. For example, if two LLMs
support the same maxToken parameter, both LLMs will expose it as `max_tokens`, allowing a similar configuration between LLMs.

The normalized configuration parameter names are: `temperature`, `max_tokens`, `top_p`,  `top_k`, `stop`, 
`presence_penalty`, `frequency_penalty`. Not all models support all of these parameters. If a normalized parameter is
specified but not supported by an LLM, it gets ignored.

A normalized configuration parameter can be pictured as an alias to the actual parameter name used by the LLM. For example,
`max_tokens` may be an alias for `model_kwargs.maxTokenCount`.

Usage of normalized configuration parameters is optional. As mentioned previously, an LLM documentation 
is the definitive source for configuration syntax and availability.

### Tools

In the context of a Large Language Model, a tool is an external function or system that the model can use to perform tasks beyond its inherent abilities. 
Tool calling, also known as function calling, refers to the LLM's capability to invoke a tool to carry out a specific task. Tool calling is only available on LLM models that support it.

An LLM can be configured with one or more tools by specifying, for each tool, a schema that defines how the tool should be invoked. This schema includes the tool's name, parameters, return type, and description. It's essential for the schema to have clear parameter names and detailed descriptions to help the LLM understand the tool's purpose and usage.
When the LLM decides to use one of the tools it has been configured with, it returns a document matching the provided tool schema. This document, referred to as a _tool call_ document, describes the tool invocation. It includes the selected tool's name, along with the parameter names and their corresponding values needed for invocation. However, the LLM does not invoke the tool itself; invocation is handled by the Vantiq server based on the tool usage configuration.

To configure an LLM with tools, you can use VAIL procedures where each procedure acts as a tool. The Vantiq server automatically generates a schema for each procedure and configures the LLM using the generated schemas. If the LLM chooses to use a tool, it returns a message containing a _tool call_ description that details how to invoke the procedure. The Vantiq server then executes the procedure on behalf of the LLM.

For example, let's use the following `getCurrentTemperature` VAIL procedure as an LLM tool,

```text
// Return the temperature of the specified location in Celsius
package tool.example
procedure ToolService.getCurrentTemperature(location String Required Description "The location to get the temperature for"): Integer
    // VAIL code to get the temperature from the specified location
    var temp = <logic to retrieve the temperature>
    return temp
```

Notice that the procedure `getCurrentTemperature` contains a [description](rules.md#service-procedures) for the tool itself and for the `location` parameter.

With the `submitPrompt` LLM built-in service, tools are provided as the `tools` parameter,

```text
var ref = "/procedures/tool.example.ToolService.getTemperature"
io.vantiq.ai.LLM.submitPrompt(llmName: "ChatLLM", prompt: "What is the temperature in New York?", tools: [ref])
```

If a service contains multiple procedures, and each public procedure is a tool, you can specify a service reference. This will include all public procedures as tools, 

```text
var ref = "/services/tool.example.ToolService"
io.vantiq.ai.LLM.submitPrompt(llmName: "ChatLLM", prompt: "What is the temperature in New York?", tools: [ref])
```

When the LLM is invoked with the provided prompt, it selects the `getCurrentTemperature` tool and returns a response containing a _tool call_ describing how to invoke the tool. The Vantiq server then invokes the procedure `getCurrentTemperature` on behalf of the LLM and adds the returned value to the LLM's prompt context. The LLM is then automatically re-invoked with this enriched context, enabling it to generate a response that includes the temperature. 

If several tools are specified, the LLM prompt context is enriched with the return values from all the tools it decides to use. 

Tool calling is supported by the [`submitPrompt`](rules.md#llm) built-in service, [`SubmitPrompt`](apps.md#submit-prompt) activity pattern and [`Tool`](genaibuilder.md#tool) GenAI component. Each of these supports defining tools with services and procedures and also with user-provided schemas. 

Execution of a Vail procedure tool can be controlled using the options explained in the [Tool Authorizer](#tool-authorizer) section.

#### MCP Tools

The `mcpTools` property of the GenAI Tools component allows you to specify MCP servers, providing access to the MCP tools 
defined in those servers.

The value of the `mcpTools` property is a JSON object in which each key is an MCP server alias, and each corresponding value 
is an MCP server configuration object. Each MCP server configuration must include the `url` and `transport` properties. 
If the server requires headers (e.g., for authentication), they can be provided using the optional `headers` property.

For example, the following configuration specifies two MCP servers, `mcpServer1` and `mcpServer2`, with their respective 
URLs, transports, and authentication headers:

```json
{
  "mcpTools": {
    "mcpServer1": {
      "url": "https://mcp-server1.example.com/mcp",
      "transport": "streamable_http",
      "headers": {
        "Authorization": "Bearer @secrets(MCPKey_Server1)"
      }
    },
    "mcpServer2": {
      "url": "https://mcp-server2.example.com/mcp",
      "transport": "streamable_http",
      "headers": {
        "Authorization": "Bearer @secrets(MCPKey_Server2)"
      }
    }
  }
}
```

> Note: The `transport` property supports the values `streamable_http` and `sse`.

We recommend using the [`@secrets`](./sources/source.md#using-secrets) notation to protect sensitive information such
as API keys or authentication tokens.

Defining MCP servers in the `mcpTools` property makes their tools available to the LLM. If the `tools` property also 
defines tools, the LLM will have access to both sets of tools.

You can use the `toolAuthorizer` property to control the execution of MCP tools, as described in 
the [Tool Authorizer](#tool-authorizer) section below.

#### Tool Custom Schema

Using VAIL procedures is the most convenient way to configure and work with tools. VAIL procedures offer a simple framework for tool execution and a control mechanism with authorizers. However, VAIL procedures are not the only way to define tools; you can also define tools by specifying custom schemas.  

With a tool defined by a custom schema, the LLM returns a _tool call_ description that the Vantiq server does not attempt to invoke. Instead, the Vantiq server returns the LLM message containing the _tool call_ description to your application, giving you full control over how the _tool call_ information is processed. For example, you could implement a custom invocation tailored to a tool, then provide the tool's response back to the LLM.

Another scenario would be to simply leverage a tool's schema mapping capability. Based on an input document (prompt) the LLM can extract and map the necessary information conforming to the tool's schema, creating a document instance of this schema based on the prompt data. 

For example, imagine a music record classifier tool that defines a schema with fields like title, year, artist, etc. The LLM prompt would include data from a music record, and the LLM would return a message with a _tool call_ description containing the music record in the schema format. In this scenario, no tool invocation is necessary, and no further LLM re-invocation is required. We are simply taking advantage of the LLM capability to generate a document that conforms to a schema.    

Let's take a first example with a tool defined using a GenAI component, relying on a Pydantic schema definition. This example shows the schema mapping capability. Another example that illustrate a custom tool invocation is outlined in the [Tool Custom Invocation](#tool-custom-invocation) section below.  

We keep the above `getCurrentTemperature` procedure example, but this time defined as a Pydantic model class definition in the Tool GenAI component,

```
class getTemperature(BaseModel):
  """Return the temperature of the specified location in Celsius"""
  location: str = Field(..., description="The location to get the temperature for")
```

When we invoke the Tool component with the prompt `What is the temperature in Paris?`, the response is an `ai` message containing the following `tool_calls` property,

```json
[
   {
      "name": "getTemperature",
      "args": {
         "location": "Paris"
      },
      "id": "toolu_bdrk_012yxuj8nqjSnT9SEsTL9ios",
      "type": "tool_call"
   }
]
```

This _tool call_ description is a JSON document that conforms to the `getTemperature` schema. From this description, we could decide to invoke an external tool that would provide the temperature, then feed the response back into the LLM (see example in the section below), or the response might be sufficient for our processing logic, without the need to call the LLM again for this prompt.

Note that the `tool_calls` property is a list that may contain multiple tools. Each _tool call_ description in this list includes the necessary invocation information. The `id` property uniquely identifies a _tool call_, and if a tool result message needs to be built, the `id` value must be provided as the `tool_call_id` parameter. See section [Tool Custom Invocation](#tool-custom-invocation) for an example.

#### Tool Custom Invocation

Another use case for defining a tool with a custom schema is to explicitly manage its invocation, providing complete control over the process. Based on the _tool call_ description returned by the LLM, you can access the necessary invocation information, invoke the tool, and then provide the tool's response back to the LLM. This allows the LLM to generate an appropriate response using the context provided by the tool.

To do this, you can use the built-in service procedure [`ChatMessage.buildToolResultMessage`](rules.md#chatmessage-builders). This procedure wraps the tool invocation response as a tool message, which can be added back to the LLM prompt context. Note that when adding a tool result message to the prompt context, you must also add the preceding Tool Call AI message containing the tool call descriptions (for example, the `getTemperature` tool call shown in the previous section). This ensures that the LLM has the necessary context: the initial prompts, that Tool Call AI message, and the corresponding tool result message associated with that tool call.

The following VAIL code illustrates how to define a tool with a custom schema and how to explicitly manage its invocation. We continue using `getCurrentTemperature` as a tool, but now we use the `submitPrompt` built-in service procedure along with a function descriptor schema,

```text
package tool.example

import service io.vantiq.ai.LLM
import service io.vantiq.ai.ChatMessage 

// LLM resource must have tool calling capability, e.g., OpenAI, Gemini
// Prompt should ask for the temperature of a location (e.g., "What is the temperature in Paris?")
PROCEDURE ToolSamples.customInvoke(llmName String, prompt String)

// getCurrentWeather schema (io.vantiq.ai.FunctionDescriptor)
var schema = {
    name: "getCurrentWeather",
    description: "Return the temperature of the specified location in Celsius",
    parameters: {
        type: "object",
        properties: {
            location: { 
                type: "string", 
                description: "The location to get the temperature for" 
            }
        },
        required: ["location"]
    }
}

// initial prompt followed by LLM invocation
var prompts = [ChatMessage.buildHumanMessage(prompt)]

// LLM is configured with the getCurrentWeather tool
var result = LLM.submitPrompt(llmName: llmName, prompt: prompts, tools: [schema])

if (typeOf(result) == "Object") {	
	// add message with tool description to prompt context
    prompts.add(result)

	// tool call describes the tool (name, args) - we assume that it gets invoked here and returns a value
    var toolCall = result.tool_calls[0]
	// var tempFromTool = <tool invocation>
	var tempFromTool = 18   // assume the tool returns 18 as the temperature

	// wrap tool returned value as a tool result message and add to prompt context
    var toolResult = ChatMessage.buildToolResultMessage(toolCall.name, tempFromTool, toolCall.id)
    prompts.add(toolResult)

	// with complete context, invoke LLM again - we should now get the expected response 
	result = LLM.submitPrompt(llmName: llmName, prompt: prompts)
} else {
	exception("org.test.error", "expected a message response with tool_calls", [])
}

// e.g., ret = "The temperature in Paris is 18 degrees Celsius."
return result
```

Once the tool is invoked using the information from the `tool_calls` property description (`<tool invocation>` placeholder above), a tool result message is created and added to the prompt context. The tool response message contains the tool name, tool returned value and the tool `id` value from the _tool call_ description.

This example uses a single tool for simplicity. If multiple schemas are provided and the LLM chooses to use more than one tool (i.e., the _tool call_ description list contains multiple tools), you must handle each tool invocation separately and provide a tool result message for each response. The LLM prompt context should then include the initial LLM result with the _tool call_ descriptions, followed by a tool result message for each invoked tool. 

**Synthetic Tool Call message**

In the previous example, we added the Tool Call AI message returned by the LLM to the prompt context. If you want to create a synthetic Tool Call message instead, you can use the built-in service procedure `ChatMessage.buildToolCallMessage`, providing a list of tool call descriptions. This approach allows you to create a tool call message even when the LLM does not return one, or to modify a tool call description before adding it to the prompt context.

The `ChatMessage.buildToolCallMessage` procedure requires two parameters: a message name and a list of tool call descriptions. The message name can be any value. Each tool call description in the list must include the tool name, arguments, a unique id, and the type "tool_call". The return value is an AI message that can be added to the prompt context, just like a Tool Call AI message returned by the LLM.

This is illustrated in the following code below, which modifies the previous example to create a synthetic tool call message instead of using the one returned by the LLM.

```text
package tool.example

import service io.vantiq.ai.LLM
import service io.vantiq.ai.ChatMessage 

// LLM resource must have tool calling capability, e.g., OpenAI, Gemini
PROCEDURE ToolSamples.customInvoke(llmName String, cityName String)

// initial prompt
var prompt = "What is the temperature in " + cityName + "?"
var prompts = [ChatMessage.buildHumanMessage(prompt)]

// tool call description for the selected tool
var toolCall = {
        name: "getCurrentWeather",
        args: { location: cityName },
        id: uuid(),
        type: "tool_call"
    }
    
// synthetic AI Tool Call message describing the selected tool    
var result = ChatMessage.buildToolCallMessage("someName", [toolCall])    
    
// add message with tool description to prompt context
prompts.add(result)

// where the tool gets invoked and returns a value (placeholder for actual tool invocation logic)
// var tempFromTool = <tool invocation>
var tempFromTool = 18   // assume the tool returns 18 as the temperature

// wrap tool returned value as a tool result message and add to prompt context
var toolResult = ChatMessage.buildToolResultMessage(toolCall.name, tempFromTool, toolCall.id)
prompts.add(toolResult)

// with complete context, invoke LLM - we should get the expected response 
result = LLM.submitPrompt(llmName: llmName, prompt: prompts)

// e.g., ret = "The temperature in Paris is 18 degrees Celsius."
return result
```

As with an LLM-generated tool call, the tool result message must reference the same tool id value so that the LLM can associate the tool response with the corresponding tool call.

#### Tool Parameter Override

When an LLM selects a tool, it returns a _tool call_ document that specifies the tool name and input parameters. The Vantiq server 
uses this information to perform the tool invocation. In some cases, you may want to override certain parameters - for example, 
to provide a value for an optional parameter the LLM did not set, or to replace a value it selected.
To do this, you can use the GenAI Flow [runtime configuration](./genaibuilder.md#runtime-configuration) property `toolParameterOverride`.

Its general syntax is:

```text
{
  "toolParameterOverride": {
    tool: <tool_name>               
    name: <parameter_name>          
    value: <searchable_value>       
    override: <override_value>      
  }
}
```

Properties of the `toolParameterOverride` object are:

* **tool** -- The name of the tool that the parameter belongs to.
* **name** -- The name of the parameter to override.
* **value** -- A substring to match against the parameter value selected by the LLM. If a match is found, the override is applied.
* **override** -- The value to use instead of the value returned by the LLM.

To illustrate how `toolParameterOverride` works, consider the following VAIL procedure `getMedicalRecord`, defined as a tool:

```text
// Get the medical record for the specified patient, providing their name and optionally their social security number
PROCEDURE getMedicalRecord(name String Required Description "Name of the person",
					       ssn  String Description "Person social security number")
```

**_Override parameter by name_** 

Suppose the LLM selects this tool and returns a _tool call_ with the name parameter set to "Alice" and the ssn parameter set to "123-45-6789".
To override the ssn value regardless of what the LLM selected, specify the following `toolParameterOverride` in your runtime configuration:

```text
{
  "toolParameterOverride": {
    "tool": "getMedicalRecord",
    "name": "ssn",
    "override": "987-65-4321"
  }
}
```

In this case, the Vantiq server will invoke the `getMedicalRecord` procedure with the name parameter set to "Alice" and 
ssn set to "987-65-4321", replacing the value selected by the LLM.

> For a Vantiq procedure tool, the `tool` property must specify the fully qualified procedure name.
If the `getMedicalRecord` procedure were part of the `MedicalService` service in the `health.records` package, the tool property value would be
`health.records.MedicalService.getMedicalRecord`.

**_Override parameter by value_**

Now suppose your prompt is: `Get the medical record for Alice. For the SSN value, use the string: SSN_VALUE.`

The LLM returns a tool call with name set to "Alice" and ssn set to "SSN_VALUE". To override this value based on a match, use the following configuration:

```text
{
  "toolParameterOverride": {
    "tool": "getMedicalRecord",
    "value": "SSN_VALUE",
    "override": "987-65-4321"
  }
}
```

The Vantiq server searches all _tool call_ parameters for values containing the substring "SSN_VALUE". For each match, 
the override is applied, and the entire LLM-selected value is replaced with "987-65-4321".

> Note: The match is based on substring search. This means that even if the LLM-selected value was "SSN_VALUE_Alice", 
the override would still apply, replacing "SSN_VALUE_Alice" with "987-65-4321".

**_Override parameter by name and value_**

You must specify at least the name or value property - but you can provide both. If both are set, the override 
applies only when the parameter name matches and the value contains the specified substring.

Using _by name_ makes the override deterministic: it always applies to that parameter, no matter what value the LLM picks.
Using _by value_ is more flexible: it lets you match based on the selected content, which is useful if you do not know the parameter name.

**_Several parameters override_**

If you have several parameters to override, you can specify a list as the value of the `toolParameterOverride` property.

For example,

```
{
  "toolParameterOverride": [
    {
      "tool": "getMedicalRecord",
      "name": "ssn",
      "override": "987-65-4321"
    },
    {
      "tool": "getPersonalInfo",
      "name": "redacted",
      "override": "true"
    }
  ]
}
```

> Note that `toolParameterOverride` is a runtime configuration, so it applies only to the call where it is specified.

Tool parameter overrides can be used with both VAIL procedure and service tools and MCP tools.

### Tool Authorizer

For LLMs capable of tool calling, tools can be specified as VAIL resources (either procedures or services) in the
[`submitPrompt`](rules.md#llm) invocation, [`SubmitPrompt`](apps.md#submit-prompt) activity pattern or [`Tool`](genaibuilder.md#tool) GenAI component.
Tools can also be specified as MCP server resources using the GenAI [`Tool`](genaibuilder.md#tool) component `mcpTools` property.

When the LLM selects one of these specified tools, it can automatically execute the corresponding VAIL procedure or MCP server tool, thus providing the LLM with the additional context it requires.

To control tool execution, you can include a tool authorizer. For example as a parameter to the `submitPrompt` LLM built-in service,
as the `functionAuthorizer` configuration property of the [`SubmitPrompt`](apps.md#submit-prompt) activity pattern or as the `authorizer` configuration property of the [`Tool`](genaibuilder.md#tool) GenAI component.

The authorizer is a VAIL procedure that is evaluated before executing any tool. It must return `true` to authorize the tool's execution or `false` to deny it. 
If denied, tool execution fails. For example, in the case of a `submitPrompt` invocation, it would fail with the error `io.vantiq.llm.function.exec.denied`.

A tool authorizer requires _name_ and _arguments_ parameters. The _name_ parameter specifies the tool to be executed,
and the _arguments_ parameter holds the values of the tool’s parameters.

For example,

```text
procedure confirmExecution(name String, arguments Object): Boolean
```

To control if a tool can be automatically executed or not, you can specify the `aiExecute` property in its procedure definition.
The `aiExecute` property can have the following values:

* **allow** -- invocation is allowed - the procedure is automatically executed, unless an authorizer invocation denies it.
* **authorized** -- invocation must be authorized - the procedure cannot be executed unless an authorizer invocation authorizes it.

For example, the following procedure `submitOrder` can only be executed as an LLM tool if a tool authorizer allows it:

```text
// Submit an order named 'item' for a total price specified by the integer property 'price'
procedure submitOrder(item String Required Description "The name of the item to order",
                      price Integer Required Description "The total price of the order"): String
                      with properties = {aiExecute = authorized}
```

Let's assume that we have an `AIService` with an authorizer as defined above. Let's also assume that we
 have a reference to the `submitOrder` procedure. A call to `submitPrompt` would look like this:

```text
var ref = "/procedures/submitOrder"
var refAuthorizer = "/procedures/org.test.AIService.confirmExecution"
io.vantiq.ai.LLM.submitPrompt(llmName: "OpenAI", prompt: "Order one large pizza for $20.", 
                              functions: [ref], functionAuthorizer: refAuthorizer)
``` 

As the LLM chooses to invoke `submitOrder`, the authorizer `confirmExecution` is invoked with the name parameter set to `submitOrder` 
and the arguments parameter set to `{"item": "large pizza", "price": 20}`. The authorizer decides to either grant execution (return `true`)
or deny it (return `false`).

MCP tools have an implied execution mode of `allow`. Therefore, if the GenAI Tools component’s `mode` property is set 
to `Execute`, the MCP tools are executed automatically unless explicitly denied by an authorizer.

## LLM Playground

The LLM playground offers a tool for verifying LLM connections and experimenting with different large language models and their settings.
It is also a useful tool for creating and refining prompts (a task often referred to as *Prompt Engineering*).

There are two ways to access the LLM playground in the IDE.  Use the _Test - LLM Playground_ menu from the top navigation bar menu.  Or use the "Run Playground" button found in an LLM's detail pane.

The LLM playground has three main UI components: navigation panel, main chatting area and settings panel.

![LLM Playground UI](assets/img/ai/llmplayground.jpg)

### Main Chatting Area
The main chatting area is where you can choose the LLM to work on and type in a prompt to see the response from the selected LLM. 

Once a prompt is submitted, it is added to the end of the current conversation, along with its response.  There is a context menu associated with each user prompt.

![User Prompt Context Menu](assets/img/ai/promptmenu.jpg)

- **_Edit Prompt_** -- Edit the prompt in place. You will have the option to save the modified prompt only or submit the modified prompt. If you choose to submit, the modified prompt will be submitted and the original prompt and everything after it will be deleted. It is a quicker alternative for deleting the prompt first, then submitting a new prompt.
- **_Edit Prompt with Template_** -- Works just like _Edit Prompt_, should only be used if the prompt was created from a template.  See section [Working with Template](#working-with-template) below. 
- **_Delete Prompt_** -- Delete one prompt only.
- **_Delete Prompt and All Following Messages_** -- Delete the prompt and all responses and prompts after that prompt.  Any new prompt submitted will be continuing the conversation from the response before the deleted prompt.
- **_Submit again_** --  Do not change existing conversation, but the same prompt will be submitted again.  The new submission and its response will be appended to the end of the conversation. This is a quick way to test different settings without retyping the same prompt.

#### Working with Template
Using a template is an efficient way to build your prompt. A Template is a Vantiq text document which contains placeholders that are dynamically replaced with actual data when the template is used.

Use the **_Load Template_** button to bring up the template editor with your chosen Document. Then provide values for placeholder variables before submitting the prompt.

![Load Template Dialog](assets/img/ai/loadtemplate.jpg)

You can also edit an existing prompt that was created using template. The same template editor will be shown with the template document and user input values loaded.

The editor has the option to "Update Template Document on Save/Submit" which allows you to build your template without leaving the LLM playground.

### Settings Panel
The settings panel is where you can modify LLM to experiment with and understand the capabilities of the LLM.  Edit the settings via the various sliders, or by clicking the setting's value to open a text field.

Initially, settings are loaded from the saved LLM config. Modified settings will be used on the next prompt submission within the playground. It does not modify the LLM until you click the "**_Update LLM_**" button on top of the settings panel.  You can also create a new LLM with the new settings by clicking the "**_Duplicate LLM_**" button.

The "**_Reset_**" button resets all settings back to the current configuration state of the selected LLM.

Note that each LLM has its own settings, and some settings may not apply to all LLMs. For example, the "Functions" setting is currently only available for GPT and Google Gemini models.

There is another sub-tab titled "System". It lets you specify a "System" prompt which is submitted with each user prompt.
The system prompt is a predefined message or question provided by the system to guide the conversation or elicit a specific type of response from the LLM.
For example, a system prompt of "Always generate response in JSON format" instructs the LLM to respond using JSON instead of plain text.

![System Prompt](assets/img/ai/systemprompt.jpg)

The selected LLM may have already defined a default system prompt in its configuration. In this case, the default system prompt will be loaded automatically and displayed as read-only text.

There is also a collapse icon on the panel to minimize the panel to the left side of the screen. This gives you more space to work on the main chat area.

### Navigation Panel
The navigation panel shows the history of conversations. 

You can use the "**New Conversation**" button to start a new conversation. The conversation does not have a title until you submit the first prompt. The first prompt is also used as the initial name of the conversation. You can use the context menu “**_Rename_**” to rename the conversation.

You can click on a conversation name to jump back to an existing conversation.  The main chatting area will load all previous prompts and responses saved for the selected conversation.

To export a conversation, use “**Export**” from its context menu.  The exported conversation is saved as a JSON file.  You can import the conversation back to the playground using the “**Import Conversation**” button on the navigation panel.

To delete a conversation, use “**Delete**” from its context menu.

![Conversation Menu](assets/img/ai/conversationmenu.jpg)

### Testing Semantic Index
Besides testing an LLM, you can also test a Semantic Index you have created in Vantiq.

At the bottom of the Settings panel, there is a radio button "RAG" (this stands for Retrieval Augmented Generation). Enabling it allows you to choose a Semantic Index to test.

![Enable RAG](assets/img/ai/rag.jpg)

Once you have selected a Semantic Index, any new prompt submitted will have the response generated using the Semantic Index (as part of Vantiq's RAG algorithm) instead of from an LLM directly.

The LLM used to generate the response depends on the "Q&A LLM" setting.  This lets you choose to either use the current LLM settings in the playground or use the default LLM specified in the Semantic Index.  If Semantic Index's default LLM is used, the LLM and settings seen in the playground will not be used.


