# Open Inference Guide

The [Open Inference Protocol](https://github.com/kserve/open-inference-protocol) (OIP) is a specification that standardizes 
communication between client applications and AI model inference servers.

It defines a consistent HTTP/REST contract, specifying the exact JSON structure for inference requests and responses. 
By abstracting away backend implementation details, OIP enables interoperability, allowing applications to interact 
with any compliant server without the need for custom, server-specific integration logic.

In addition, the protocol includes an optional binary data extension that improves performance by enabling efficient 
transmission and processing of large tensor payloads.

Access to OIP-compliant servers is provided through the Remote source, which supports the protocol out of the box. 
Since OIP is based on standard HTTP/REST communication, the Remote source is the natural integration point for 
connecting to OIP endpoints. It can also be configured to use the binary tensor data extension for more efficient data 
transfer when needed.

## Remote source

To interact with an OIP-compliant server, your first step is to define a Remote source.

For example, assuming a local Triton Inference Server running on `http://localhost:8000`, you can create a Remote 
source named `TritonServer`, simply specifying the server URI.

You can then invoke the server health endpoint,

```
var ret = select one from source TritonServer with path = "/v2/health/live", method = "GET", asFullResponse = true
var live = (ret.status == 200)
```

invoke a model health endpoint,

```
var path = Strings.format("/v2/models/{0}/ready", [modelName])
var ret = select one from source TritonServer with path = path, method = "GET", asFullResponse = true
var ready = (ret.status == 200)
```

request the server metadata,

```
select one from source TritonServer with path = "/v2", method = "GET"
```

or send an inference request,

```
var path = Strings.format("/v2/models/{0}/infer", [modelName])
var response = select one from source TritonServer with path = path, method = "POST", 
                                                        body = payload, openInference = true
```

For details about the `openInference` property, refer to the [Source Configuration section](#source-configuration).

An OIP request payload is typically expressed as a list of one or more input tensors, each with a `name`, `shape`, `datatype`, and `data`.

The `name` is a string that identifies the tensor, `shape` is an array of integers representing the dimensions of the tensor,
`datatype` is a string that specifies the type of data in the tensor (e.g., `FP32`, `INT32`, `BYTES`), and `data` is an array
containing the actual tensor values.

For example,

```
{
  "inputs" : [
    {
      "name" : "values",
      "shape" : [2, 2],
      "datatype" : "FP32",
      "data" : [ [1.0, 2.0], [3.0, 4.0] ]
    },
    {
      "name" : "options",
      "shape" : [2],
      "datatype" : "BOOL",
      "data" : [ true, false ]
    }
  ]
}
```

The `data` payload is always an array (tensor values) and can be a nested array for multidimensional tensors. The values
are VAIL data types, such as `Real`, `Integer`, `Boolean`, or `String`.

Please refer to the Open Inference Protocol documentation for details on the request and response payloads, including the
expected structure for input and output tensors.

> Note: datatype, shape and name are tightly coupled to the model server, so you must refer to the model documentation
to determine the expected values for these fields. 


## Data types

Tensor OIP data types have the following Vantiq mapping:

OIP data type | Vantiq data type                                                         
---------|--------------------------------------------------------------------------
`BOOL`                                                                           | `Boolean` 
`UINT8`, `UINT16`, `UINT32`, `UINT64` <br/> `INT8`, `INT16`, `INT32`, `INT64`    | `Integer` 
`FP32`, `FP64`                                                                   | `Real` 
`FP16`, `BF16` _(limited to binary extension)_                                   | `Real` 
`BYTES`                                                                          | `String` or resource reference (e.g., [Temp Blob](resourceguide.md#tempblobs))

> Note: sending FP16 and BF16 values as numbers within JSON is unreliable due to the lack of a universal standard for
their representation. For this reason, it is recommended to send these data types using the binary tensor extension.

> Note: `UINT64` support is limited to `Integer`, which is a _signed_ 64-bit values.

In the example above, the `values` tensor would be Vantiq `Real` values, while the `options` tensor
would be Vantiq `Boolean` values.

## JSON data payload

By default, a Remote source communicating with an OIP-compatible server exchanges input and output tensor data using JSON.  

For example, the following request payload:

```
{
  inputs : [
    {
      name: "values",
      shape: [2, 2],
      datatype: "FP32",
      data: [ [1.0, 2.0], [3.0, 4.0] ]
    },
    {
      name: "image",
      shape: [1],
      datatype: "BYTES",
      data: [ Utils.packageReference("documents/myImage.jpg") ]
    }
  ]
}
```

would send a tensor of floating-point values and an image to the model server as part of the JSON payload (i.e., `data` property values).
As JSON requires binary data to be encoded in text format, typically using base64, the image - specified above as 
a resource reference - would be transmitted as a base64-encoded string. This means that the model would receive an input tensor with
four floating-point values and an image tensor containing the image data as a base64-encoded string.

Similarly, a response payload containing an image and a tensor of integer values would look like this:

```
{
  "model_name": "mymodel",
  "model_version": "1",
  "outputs" : [
    {
      "name" : "image",
      "shape" : [1],
      "datatype" : "BYTES",
      "data" : [ "<base64-encoded image data>" ]
    },
    {
      "name" : "result",
      "shape" : [2, 3],
      "datatype" : "INT32",
      "data" : [ [1, 5, 19], [4, 34, 2] ]
    }
  ]
}
```

## Binary extension

You can configure a Remote source to use the binary tensor data extension if the inference server supports it (e.g., Triton Inference Server). 
When enabled, the Remote source can send and receive tensor data in a more efficient binary format. This reduces the payload 
size and parsing overhead compared to the default JSON format, a benefit that is especially true for large payloads, such as those 
containing image data.

You can check if the inference server supports the binary tensor data extension by querying the server's metadata endpoint.

```
    // Assuming a Remote source named TritonServer
    select one from source TritonServer with path = "/v2", method = "GET"
    
    // The response will include an `extensions` field indicating the supported extensions
    {
        "name": "triton",
        "version": "2.53.0",
        "extensions": [
            ...,
           "binary_tensor_data",   // Indicates support for the binary tensor extension
           ...
       ]
    }    
```

### Enabling binary extension

To enable the binary tensor data extension, you must set the Remote source configuration property `openInference` to true. 
When `openInference` is set to true, the Remote source sends - by default - all tensors as a binary payload.

#### Source configuration

You can set the `openInference` property to true in the Remote source configuration.

In the Remote source Properties tab, click on `Edit Config as JSON` to display the source JSON configuration. Then, 
add the `openInference` property to `requestDefaults` (also adding `requestDefaults` it if it does not already exist).

For example, assuming a Triton Inference Server running on `http://localhost:8080`, the Remote source configuration would look like this:

```
{
    <omitted properties>,
    "requestDefaults": {          
        "openInference": true
    },                             
    "uri": "http://localhost:8080"
}
```

Save the source configuration to persist the changes. Once saved, you can uncheck the `Edit Config as JSON` checkbox.

#### Source request

You can also set the `openInference` property on source requests using the `with` clause. 

```
    var payload = {
	    inputs: [
            {
              name: "image",
              shape: [1],
              datatype: "BYTES",
              data: [ Utils.packageReference("documents/someImage.jpg") ]
            }
        ]
    }
    var path = Strings.format("/v2/models/{0}/infer", [modelName])
    var response = select one from source TritonServer with path = path, method = "POST", 
                                                            body = payload, openInference = true
```

If you want to enable the binary tensor extension for all requests, you should set the `openInference` property in the source configuration as described above.

### Binary payload tensors

Sending and receiving tensors in binary format is transparent to both the Remote source user and the inference server, 
making the binary-tensor extension a simple yet significant performance optimization. Note that `BYTES` resource 
references are _not_ base64-encoded when transmitted in binary format. This is more efficient and ensures that the inference 
server receives raw binary data rather than a base64-encoded string, as is the case with JSON.

For example,

```
// Assuming that IpCamera is a VIDEO source 
var imageFeed = select one from source IpCamera with resize = { maxHeight: 640, maxWidth: 640 }

var payload = {
  inputs: [
    {
      name: "image",
      shape: [ 1, 1 ],
      datatype: "BYTES",
      data: [ Utils.packageReference(imageFeed.contentRef)]
    }
  ]
}

// Assuming that the TritonServer is configured with openInference = true
var modelResponse = select one from source TritonServer with path = "/v2/models/myYoloModel/infer",
                                        method = "POST", body = payload
```

The image from the Video source is a [Temp Blob](resourceguide.md#tempblobs) resource reference, which is provided as the image tensor value. With
the OIP Remote source configured with `openInference = true`, the image data is sent in binary format,
and the model receives the image raw binary data.

For all other data types (boolean, integers and floats), the model receives the tensor values (e.g., floating-point values) 
regardless of the transfer format (JSON or binary). 


### Output binary tensors

To express that responses must be provided using a binary format, the request payload must include the `binary_data` and/or
`binary_data_output` parameters.  These parameters indicate to the model server that the output tensors must be returned 
in binary format, in accordance with the [Binary Tensor Data Extension](https://kserve.github.io/website/master/modelserving/data_plane/binary_tensor_data_extension/) specification. 
If neither `binary_data` nor `binary_data_output` is set, the server returns the output tensors in JSON format. 

For example, the previous payload defined as,

```
var payload = {
  parameters: {
    binary_data_output: true
  },
  inputs: [
    {
      name: "image",
      shape: [ 1, 1 ],
      datatype: "BYTES",
      data: [ Utils.packageReference(imageFeed.contentRef)]
    }
  ]
}
```

instructs the server to return all output tensors in binary format.

### Input binary tensors

The [Binary Tensor Data Extension](https://kserve.github.io/website/master/modelserving/data_plane/binary_tensor_data_extension/) 
specification defines _how_ input tensors are serialized in binary format, but it does not specify a configuration property 
for indicating when tensors should be sent this way. To address this, the Remote source introduces two configuration parameters: 
`vantiq_binary_data` and `vantiq_binary_data_input`. These parameters are analogous to `binary_data` and `binary_data_output`, 
but apply specifically to input tensors, indicating whether they should be transmitted in binary format. 

For example, the following payload will send the `image` tensor in binary format, while the `values` tensor is sent in JSON format:

```
var payload = {
  inputs: [
    {
      name: "values",
      shape: [ 1, 4 ],
      datatype: "FP32",
      data: [ 1.0, 2.0, 3.0, 4.0 ],
      parameters: {
        vantiq_binary_data: false
      }
    },
    {
      name: "image",
      shape: [ 1, 1 ],
      datatype: "BYTES",
      data: [ Utils.packageReference("documents/myImage.jpg") ],
      parameters: {
        vantiq_binary_data: true
      }
    }
  ]
}
```

> Note: `vantiq_binary_data` and `vantiq_binary_data_input` are ignored if `openInference` is not set or set to `false`. 

As with output tensors, the `vantiq_binary_data` and `vantiq_binary_data_input` parameters can be used to control binary 
serialization of input tensors using either an opt-in or opt-out strategy. For example, you can set `vantiq_binary_data_input` 
to true to enable binary format for all input tensors by default, and then override specific tensors by setting `vantiq_binary_data` 
to false. Conversely, you can set `vantiq_binary_data_input` to false and enable binary format selectively by setting 
`vantiq_binary_data` to true for specific tensors.

When the `openInference` flag is set to true, the Remote source defaults to sending all input tensors in binary format 
unless explicitly configured otherwise. The `vantiq_binary_data` and `vantiq_binary_data_input` parameters offer 
finer-grained control in such cases.

## Quota

Since OIP payloads may include large tensors, the memory usage of OIP requests and responses is controlled
by [organization quotas](./workloadmanagement.md).

If OIP responses are expected to include `BYTES` binary data such as images, stored in the Vantiq server 
as [Temp Blobs](./resourceguide.md#tempblobs), the [`documentExpansion` quota](./workloadmanagement.md#default-quotas) must be set, 
and its value must be large enough to accommodate the expected data sizes. This quota setting also applies to the aggregate size of all tensors sent and received
in an OIP request and response.  If a single request or response exceeds the quota, the request will result in an error.

## Tensors shape

The OIP protocol transmits tensors as flat arrays: the data is flattened prior to transmission, and the original tensor 
shape is included in the request or response payload to enable reconstruction on the receiving end.

The Remote source automatically flattens input tensors before sending them to the inference server and reshapes output tensors 
upon receipt. As a result, when using an OIP-enabled Remote source (i.e., with `openInference` set to true), there is 
no need to manually flatten or reshape tensors — this is handled transparently.

If you prefer the Remote source not to automatically reshape response tensors, set the `openInferenceReshape` 
property to false — either in the Remote source configuration or in the source request using the with clause.

```
// Assuming that the TritonServer is configured with openInference = true
select one from source TritonServer with path = "/v2/models/mymodel/infer",
                                method = "POST", body = inferencePayload, openInferenceReshape = false

// Response tensor is not reshaped
{
  "model_name": "mymodel",
  "model_version": "1",
  "outputs" : [
    {
      "name" : "result",
      "shape" : [ 2, 3 ],
      "datatype" : "INT32",
      "data" : [ 1, 2, 3, 4, 5, 6 ]
    }
  ]
}
```

### Built-in flatten and reshape methods

The [built-in `io.vantiq.ai.OpenInference`](./rules.md#open-inference) service provides two methods that can be used to explicitly flatten and reshape tensors when needed:

- `io.vantiq.ai.OpenInference.reshape(data, shape)`
- `io.vantiq.ai.OpenInference.flatten(data)`

For example,

```text
var reshaped = io.vantiq.ai.OpenInference.reshape( [1, 2, 3, 4, 5, 6], [2, 3] )
// reshaped is now [[1, 2, 3], [4, 5, 6]]

var flattened = io.vantiq.ai.OpenInference.flatten( [[1, 2, 3], [4, 5, 6]] )
// flattened is now [1, 2, 3, 4, 5, 6]
```

## Batch size

The Open Inference Protocol supports request batching, allowing multiple inference inputs to be sent within a single payload. 
This is typically reflected in the `shape` property of each input tensor, where the first dimension often represents the batch size.


For example,

```
  inputs: [
    {
      name: "image",
      shape: [ 1, 1 ],
      datatype: "BYTES",
      data: [ Utils.packageReference(imageFeed.contentRef)]
    }
```

and, 

```
  inputs: [
    {
      name: "image",
      shape: [ 1 ],
      datatype: "BYTES",
      data: [ Utils.packageReference(imageFeed.contentRef)]
    }
```

Both examples send a single image. However, the first uses a shape of `[1, 1]`, where the leading dimension explicitly
denotes a batch size of 1 — indicating that the payload could be extended to include more items for batch processing. 
The second uses a shape of `[1]`, with no explicit batch dimension, implying that only one image is sent and expected.

It is important to note that the presence of multiple dimensions does not necessarily imply batching; whether the first 
dimension is treated as a batch size depends on the model’s input specification. The distinction in these examples is 
deliberate, illustrating how batching can be represented in OIP requests.

