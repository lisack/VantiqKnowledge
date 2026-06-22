# Open Inference Protocol Tutorial

## Purpose

This tutorial demonstrates how to use a Remote source to connect to an AI model hosted on an inference server that supports the [Open Inference Protocol](https://github.com/kserve/open-inference-protocol) (OIP).

## Objectives

By the end of this tutorial, a Vantiq developer will be able to:

* Define a Remote source that connects to an OIP-compatible inference server
* Specify input and output tensors for interacting with AI models
* Configure requests and responses to use the OIP binary extension for efficient tensor transmission
* Build model pipelines that include pre-processing and post-processing steps

## Tutorial Overview

This tutorial provides a practical guide to using the Open Inference Protocol (OIP) with Vantiq’s Remote source [OIP capabilities](../openinference.md).
OIP is a standardized protocol for interacting with AI models hosted on inference servers, enabling efficient data exchange and model invocation.

In this tutorial, you will learn how to:

* Deploy a Triton Inference Server with Python backend models
* Create a Remote source in Vantiq to connect to the Triton server
* Define a Vantiq Service to invoke models using OIP
* Handle input and output tensors, including binary data formats
* Build an image classification pipeline with pre- and post-processing components

>Note: This tutorial assumes you are familiar with core Vantiq concepts such as Services, Procedures, and Remote Sources.
If you are new to Vantiq, we recommend starting with the [Introductory Tutorial](tutorial.md) and completing the [Vantiq Applications Developer Foundations](https://community.vantiq.com/courses/applications-developer-level-1/) course.
Also, this tutorial is not a comprehensive guide to the Open Inference Protocol (OIP), but rather a hands-on example of how to use it within the Vantiq platform.

### Prerequisites

To follow this tutorial, you will need:

* A running Triton Inference Server instance, either local or remote (see below for setup instructions using Docker)
* Python 3.8 or later installed (required in Part 4 to download and install a classification model)

## Tutorial Directory

In this tutorial, the term *tutorial directory* refers to the root directory from which all example commands and paths are referenced.
More precisely, it is the directory that contains the Triton `model_repository`, where models are stored.
The location of `model_repository` is specified in the Triton Inference Server configuration.

- If you already have a running Triton server, the *tutorial directory* is the parent of the configured `model_repository` directory.
- If you install Triton using this tutorial’s instructions, the *tutorial directory* is simply the directory where you run the Triton setup script.

Unless otherwise noted, all file paths in this tutorial are relative to the *tutorial directory*.

## 1: Inference Server

This tutorial uses the [Triton Inference Server](https://github.com/triton-inference-server/server) as the inference backend.
Triton natively supports the Open Inference Protocol (OIP), making it particularly well-suited for demonstrating Remote source 
integration with OIP-compatible inference servers.

If you do not already have access to a Triton Inference Server, you can deploy one using Docker. For simplicity, this tutorial 
assumes that the Triton Inference Server is running in a Docker container on the same machine as the Vantiq server, 
and is accessible at `http://<host_IP>:18000`.  

A typical setup might involve running a [Vantiq Edge Server](../vantiqedge.md#docker-deployment) alongside the Triton server on the same host. 
Be aware that in this configuration, the two containers run in separate Docker network namespaces, so the Vantiq container 
cannot directly connect to the Triton container. You should therefore use the host machine’s local IP address - not `localhost` - as `<host_IP>` 
in the URI. This allows traffic from the Vantiq container to be routed through the host network to the Triton container’s exposed port.
 
Alternatively, Triton can be deployed on any machine that is reachable from the Vantiq server — for example, on a cloud 
instance such as AWS EC2. In that case, you can configure the Remote source to connect to Triton using the public IP or DNS of that instance.

> Note: This tutorial assumes a local Triton instance. If you're using a remote setup, update the inference server URI accordingly.


### Triton Inference Server

The Triton Inference Server can be installed via Docker using the following script:

```bash
#! /bin/bash
docker run --rm -p18000:8000 \
  -v ./model_repository:/models \
  -v ./requirements.txt:/tmp/requirements.txt \
  nvcr.io/nvidia/tritonserver:24.12-py3 \
  bash -c "pip install -r /tmp/requirements.txt && tritonserver --model-repository=/models --model-control-mode=poll --repository-poll-secs=5"
```

This script sets the `model-control-mode` option to `poll` and `repository-poll-secs` to `5`.
These settings enable the server to automatically detect new models and make them available for inference requests.
In addition, any changes made to an existing model will be picked up automatically within 5 seconds.

Before running the script, choose a *tutorial directory* where you will:

- create the requirements.txt file,
- create the model_repository directory,
- run the installation script.

> Note: All scripts provided in this tutorial assume a Unix-like environment with bash and a POSIX-style directory structure.


1 - Create a `requirements.txt` file with the following content:

```
Pillow
numpy
```

2 - Create a `model_repository` directory. You can leave it empty for now.

The `model_repository` directory will contain the model files, including the model configuration and the Python backend implementation.

Its structure will follow this pattern:

```
model_repository
├── <model_name>
│   ├── 1
│   │   └── model.py
│   └── config.pbtxt
└── <another_model_name>
    ├── 1
    │   └── model.py
    └── config.pbtxt
```

You will add models to the `model_repository` as you progress through this tutorial. If you want to start with a fully populated
version containing all model files and configurations, download [`model_repository.zip`](https://github.com/Vantiq/Tutorials/blob/master/Open%20Inference/documents/model_repository.zip)
from the completed _Open Inference_ tutorial and extract it into your *tutorial directory*.
Alternatively, you can import the _Open Inference_ tutorial in a different namespace via `Project > Import > Tutorials`, then
from `Menu > Show > Documents`, download `model_repository.zip`.


3 - Once the `model_repository` directory and the `requirements.txt` file have been created, you can run the installation 
script to start the Triton Inference Server.

If port `18000` is already in use on your host machine, map Triton’s internal port `8000` to an alternative host port 
by modifying the docker run command. For example:

```bash
docker run --rm -p28280:8000 \
  -v ./model_repository:/models \
  -v ./requirements.txt:/tmp/requirements.txt \
  nvcr.io/nvidia/tritonserver:24.12-py3 \
  bash -c "pip install -r /tmp/requirements.txt && tritonserver --model-repository=/models --model-control-mode=poll --repository-poll-secs=5"

```

If you change the port, make sure to update the Remote source URI accordingly throughout this tutorial.


##  2: Vector multiplication model

In this section, we will create and deploy the first model - a simple implementation that performs vector multiplication. 
We will then define a Vantiq Service to invoke the model and retrieve the result. We will also examine how the `openInference` 
and `openInferenceReshape` properties affect the shape of the output tensor.


### Create the model files

Inside the `model_repository` directory, create a new directory named `dot_product`. Within this directory, create a subdirectory named `1`.

Next, in the `dot_product` directory, create a file named `config.pbtxt` with the following content:


```
name: "dot_product"
backend: "python"
max_batch_size: 0 

input [
  {
    name: "first_input"
    data_type: TYPE_FP64
    dims: [ 3, 1 ]
  },
  {
    name: "second_input"
    data_type: TYPE_FP64
    dims: [ 1, 3 ]
  }
]

output [
  {
    name: "result"
    data_type: TYPE_FP64
    dims: [ 3, 3 ]
  }
]
```

This file describes the model's inputs and outputs. Both `first_input` and `second_input` are float tensors and will
map to the `FP64` data type in OIP. The output is also a two-dimensional tensor representing the result of the vector multiplication.

In the `dot_product/1` directory, create a file named `model.py` with the following content:

```python
import numpy as np
import triton_python_backend_utils as pb_utils

class TritonPythonModel:
    """
    A Triton Python backend model that calculates the dot product
    of a [3,1] tensor and a [1,3] tensor.
    """

    def execute(self, requests):
        responses = []

        for request in requests:
            in_0 = pb_utils.get_input_tensor_by_name(request, "first_input").as_numpy()
            in_1 = pb_utils.get_input_tensor_by_name(request, "second_input").as_numpy()

            dot_product_result = np.dot(in_0, in_1)

            out_tensor = pb_utils.Tensor(
                "result",
                dot_product_result.astype(np.float64)
            )

            inference_response = pb_utils.InferenceResponse(
                output_tensors=[out_tensor]
            )
            responses.append(inference_response)

        return responses
```

The `model_repository` directory structure should now look like this:

```
model_repository
└── dot_product
    ├── 1
    │   └── model.py
    └── config.pbtxt
```

At this point, the model is deployed and should be available for inference requests. 

Restart the Triton server to see the model in the server’s startup logs, confirming that it has been loaded successfully:

```text
+---------------+---------+--------+
| Model         | Version | Status |
+---------------+---------+--------+
| dot_product   | 1       | READY  |
+---------------+---------+--------+
```


### Create the Remote source

Create or select a Vantiq namespace where you will define the resources for this tutorial.

Within the selected namespace, create a new source:

- Source Name: `TritonServer`
- Package: `example.oip`
- Source Type: `REMOTE`

In the `Properties` tab, specify the URI of the Triton Inference Server:

- Server URI: `http://<host_IP>:18000` (or `http://<host_IP>:28280` if you changed the port in the Docker command)

> Note: Replace `<host_IP>` with the IP address of the machine running the Triton Inference Server Docker container.
If you imported the completed tutorial, the URI is preconfigured as `http://host_IP:18000` and must be updated 
with the correct host IP address.

Next, click on `Edit Config as JSON` and add the `openInference` property inside the `requestDefaults` object, as shown below:

```json
{
    "uri": "http://<host_IP>:18000",
    "requestDefaults": {
        "openInference": true
    }
}
```

Save the source configuration. The Remote source is now defined and ready to be used for invoking the model.

### Create a Service

Create a new Service named `InferService` with the Package name `example.oip`. This service will hold the procedures 
you will define as you progress through the tutorial. To begin, you will define two procedures: one to check whether the Triton Inference Server 
is ready, and another to invoke the model for a dot product computation.

Start by creating a public procedure named `isServerReady`:

```text
package example.oip

stateless PROCEDURE InferService.isServerReady()

var status = select one FROM source TritonServer with path = "/v2/health/ready", method = "GET", asFullResponse = true

return (status && status.status == 200)
```

Save and run the procedure. It should return `true` if the Triton Inference Server is running and ready to accept requests.

Next, create a second public procedure, `dotProduct`, which will send an inference request to the deployed model:

```text
package example.oip

stateless PROCEDURE InferService.dotProduct()

var payload = {
	inputs: [
		{
		  name: "first_input",
		  shape: [3, 1],             
		  datatype: "FP64",
		  data: [ [1.5], [0.2], [3.0] ]
		},
		{
		  name: "second_input",
		  shape: [1, 3],             
		  datatype: "FP64",
		  data: [ [4.0, 2.5, 5.0] ]
		}
    ]
}

var response = select one FROM source TritonServer with path = "/v2/models/dot_product/infer", 
                                                        method = "POST", body = payload
return response
```

The two input values are tensors that match the input definitions specified in the model configuration.
The `first_input` tensor has shape 3×1, and the `second_input` tensor has shape 1×3. The `data` field in each tensor 
contains the actual tensor values used in the computation.

Save the procedure and execute `dotProduct`. The response should be equivalent to the following, though its formatting may differ:

```json
{
   "model_name": "dot_product",
   "model_version": "1",
   "outputs": [
      {
         "name": "result",
         "datatype": "FP64",
         "shape": [ 3, 3 ],
         "data": [
            [ 6,   3.75, 7.5 ],
            [ 0.8, 0.5,  1 ],
            [ 12,  7.5, 15 ]
         ]
      }
   ]
}
```

Next, we will modify the `openInference` and `openInferenceReshape` properties to observe how they affect the output tensor.

Change the Remote source invocation to disable the `openInference` property by setting it to `false`.

```text
var response = select one FROM source TritonServer with path = "/v2/models/dot_product/infer", 
												   method = "POST", body = payload,
												   openInference = false
return response
```

Save the procedure changes and execute the `dotProduct` procedure again. With `openInference` set to false, 
the exchange with the server uses the default JSON format instead of the OIP binary format.
Although this does not affect the model behavior or the computation result, disabling the `openInference` property 
prevents the result tensor from being automatically reshaped.

The response tensor will now look like this:

```json
{
   "model_name": "dot_product",
   "model_version": "1",
   "outputs": [
      {
         "name": "result",
         "datatype": "FP64",
         "shape": [3, 3],
         "data": [ 6, 3.75, 7.5, 0.8, 0.5, 1, 12, 7.5, 15 ]
      }
   ]
}
```

To demonstrate how the built-in `io.vantiq.ai.OpenInference` service can be used, modify the code to explicitly reshape the output tensor:

```text
var response = select one FROM source TritonServer with path = "/v2/models/dot_product/infer", 
												   method = "POST", body = payload,
												   openInference = false
var output = response.outputs[0]
response = io.vantiq.ai.OpenInference.reshape(output.data, output.shape)
return response
```

Save the procedure changes and execute the `dotProduct` procedure again. The response will now look like the following:

```text
[
   [ 6, 3.75, 7.5 ],
   [ 0.8, 0.5, 1 ],
   [ 12, 7.5, 15 ]
]
```

Now, modify the procedure to use the `openInferenceReshape` property instead, as shown below:

```text
var response = select one FROM source TritonServer with path = "/v2/models/dot_product/infer", 
												   method = "POST", body = payload,
												   openInferenceReshape = false
return response
```

With this change, the Remote source remains configured with the `openInference` property set to `true`,
but this specific request overrides the default reshaping behavior by setting `openInferenceReshape` to false.
As a result, executing the procedure again will produce the same response as when `openInference` was disabled — returning a flat tensor:

```json
{
   "model_name": "dot_product",
   "model_version": "1",
   "outputs": [
      {
         "name": "result",
         "datatype": "FP64",
         "shape": [3, 3],
         "data": [ 6, 3.75, 7.5, 0.8, 0.5, 1, 12, 7.5, 15 ]
      }
   ]
}
```

The previous examples illustrate how the `openInferenceReshape` and `openInference` properties can be specified in the `WITH` 
clause of a Remote source invocation. In most cases, it is recommended to set the `openInference` property in the 
Remote source configuration and rely on its default behavior to automatically reshape output tensors.


##  3: Image reversal model

In this section, we will create another model that reverses both an image and a string, and then define a procedure 
to invoke it. This example uses tensors with the `BYTES` data type, which is commonly used to represent binary 
content such as images or strings. We will also use the `vantiq_binary_data` and `binary_data` configuration parameters 
to enable fine-grained control over how tensors are serialized and deserialized - either as JSON or binary data.

> Important: to run this example, you _must_ have the `documentExpansion` [quota](../workloadmanagement.md#quota-interactions) defined in your Vantiq organization. 
Without it, receiving the image will fail due to a memory safeguard that limits how much data can be processed in a single request. 
By default, this limit is set to 0, which effectively disables handling of large objects such as images.

As a prerequisite, this example requires uploading an image to the `system.documents` collection in your Vantiq namespace. 
You may use the image of your choice, or the image [provided here](../assets/img/openinferancetutorial/cat.jpg).

To upload the image, navigate to `Menu > Show > Documents`, click on the `Upload` button, select the image file from your local machine,
and provide a name for the document, such as `cat.jpg`. This will create a new document in the `system.documents` collection with the specified name.

### Create the model files

Inside the `model_repository` directory, create a new directory named `reverse_image`. Within this directory, create a subdirectory named `1`.

Then, in the `reverse_image` directory, create a file named `config.pbtxt` with the following content:

```
name: "reverse_image"
backend: "python"
max_batch_size: 0

# Input tensors
input [
  {
    name: "image"
    data_type: TYPE_STRING
    dims: [ 1 ]
  }
]
input [
  {
    name: "title"
    data_type: TYPE_STRING
    dims: [ 1 ]
  }
]

# Output tensors
output [
  {
    name: "output_image"
    data_type: TYPE_STRING
    dims: [ 1 ]
  }
]
output [
  {
    name: "output_title"
    data_type: TYPE_STRING
    dims: [ 1 ]
  }
]
```

This file defines the model's inputs and outputs. Both `image` and `title` inputs are `TYPE_STRING` tensors, which
map to the `BYTES` data type in OIP. The outputs are also `TYPE_STRING` tensors, as they return the reversed forms of the input values.

The tensor dimensions are set to `[1]`, indicating that the model expects single-element tensor for both input and output.


In the `reverse_image/1` directory, create a file named `model.py` with the following content:

```python
import numpy as np
import io
import triton_python_backend_utils as pb_utils
from PIL import Image

class TritonPythonModel:
    
    def initialize(self, args):
        self.logger = pb_utils.Logger
    
    def execute(self, requests):
        responses = []
        
        for request in requests:
            # --- Get Input Tensors ---
            self.logger.log_info("Executing reverse request.")
            in_image = pb_utils.get_input_tensor_by_name(request, "image")
            in_title = pb_utils.get_input_tensor_by_name(request, "title")
            
            image_bytes = in_image.as_numpy()[0]
            title_bytes = in_title.as_numpy()[0]
            title_string = title_bytes.decode('utf-8')
            self.logger.log_info(f"Received title: '{title_string}'")
            self.logger.log_info(f"Received image data of size: {len(image_bytes)} bytes")
            
            # --- Reverse the title string ---
            reversed_title_string = title_string[::-1]
            reversed_title_bytes = reversed_title_string.encode('utf-8')
            
            # --- Image Manipulation using Pillow ---
            img = Image.open(io.BytesIO(image_bytes))
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            output_buffer = io.BytesIO()
            img_format = img.format if img.format else 'PNG'
            img.save(output_buffer, format=img_format)
            processed_image_bytes = output_buffer.getvalue()
            
            # --- Create Output Tensors ---
            out_image = pb_utils.Tensor(
                "output_image",
                np.array([processed_image_bytes], dtype=np.object_)
            )
            
            out_title = pb_utils.Tensor(
                "output_title",
                np.array([reversed_title_bytes], dtype=np.object_)
            )
            
            # --- Construct and Send Response ---
            inference_response = pb_utils.InferenceResponse(
                output_tensors=[out_image, out_title]
            )
            responses.append(inference_response)
            self.logger.log_info("Successfully processed request.")
        
        return responses
```

This Python backend serves as the model implementation. It reverses the input `title` string and flips the input image 
both vertically and horizontally, returning both in the response.

Since the Triton server is running with the `model-control-mode` option set to `poll`, it should automatically detect 
the new model and make it available for inference requests.

The `model_repository` directory structure should now look like this:

```
model_repository
├── dot_product
│   ├── 1
│   │   └── model.py
│   └── config.pbtxt
└── reverse_image
    ├── 1
    │   └── model.py
    └── config.pbtxt
```

Restart the Triton server to see the model in the server’s startup logs, confirming that it has been loaded successfully:

```text
+---------------+---------+--------+
| Model         | Version | Status |
+---------------+---------+--------+
| dot_product   | 1       | READY  |
| reverse_image | 1       | READY  |
+---------------+---------+--------+
```

### Add an inference procedure

Within the `InferService` Service, create a new public procedure named `reverseImage`:

```
package example.oip

stateless PROCEDURE InferService.reverseImage(imageName String)

var content = Utils.packageReference("documents/" + imageName)

var payload = {
	inputs: [
		{
		  name: "image",
		  shape: [1],             
		  datatype: "BYTES",
		  data: [ content ]
		},
		{
		  name: "title",
		  shape: [1],             
		  datatype: "BYTES",
		  data: [ imageName ],
		  parameters : { vantiq_binary_data : false }
		}
    ],
	outputs: [
		{
          name: "output_image",
  	      parameters : { binary_data: true }
		},
		{
          name: "output_title",
  	      parameters : { binary_data: false }
		}
	]
}

// Invoke the inference endpoint
var result = select one FROM source TritonServer with path = "/v2/models/reverse_image/infer", 
												   method = "POST", body = payload

// A reference to the reversed image, as a TempBlob resource
var outImage = result.outputs[0].data[0]
// The reversed title string
var revImageName = result.outputs[1].data[0]

// Save the received reversed image from the model, using the reversed name
upsert system.documents(name: revImageName, fromTemp: outImage.contentRef, fileType: "image/jpg")

return result
```

This procedure takes a document name as input, retrieves the corresponding image from the `system.documents` collection, 
and sends it to the Triton Inference Server for processing. When executing the procedure, specify
the name of the image you uploaded earlier - for example, `cat.jpg`.

The `binary_data` configuration property is used to control how each output tensor is returned:

- `output_title` is set to `false` to return it as a string.
- `output_image` is set to `true` to return it as binary data.

If the `output_title` tensor were transmitted as binary data, it would materialize as a [Temp Blob](../resourceguide.md#tempblobs).
While returning a Temp Blob is appropriate for large binary content such as images, it is unnecessary for the title string,
which we want to receive as plain text.

Note that when output tensors are explicitly listed in the `outputs` section of the request payload, only those tensors are included in the response.
For this reason, both `output_image` and `output_title` are explicitly listed in the `outputs` array.

If you want all output tensors to be returned as binary data, you could omit the `outputs` section entirely and use 
the [`binary_data_output`](../openinference.md#output-binary-tensors) parameter instead.

Save the procedure and execute `reverseImage`.

The reversed image is saved as a new document in the `system.documents` collection, using the reversed name as its name. 
This view the reversed image, navigate to `Menu > Show > Documents`, selecting the context menu on the saved document row, 
and choosing *`View the Image`*.

The procedure returns the full response from the Triton Inference Server, allowing you to examine the output structure.

For example, after invoking the `reverseImage` procedure with an image named `cat.jpg`:

```
{
   "model_name": "reverse_image",
   "model_version": "1",
   "outputs": [
      {
         "name": "output_image",
         "datatype": "BYTES",
         "shape": [ 1 ],
         "parameters": { "binary_data_size": 348906 },
         "data": [
            {
               "fileType": "application/octet-stream",
               "contentSize": 348902,
               "contentRef": "/system.tempblobs/c0e863a0-5d44-11f0-ac5c-f6f99b5a98de__93ac1ce8-aadb-430c-8b9a-29492066e06b"
            }
         ]
      },
      {
         "name": "output_title",
         "datatype": "BYTES",
         "shape": [ 1 ],
         "data": [ "gpj.tac" ]
      }
   ]
}
```

## 4: Image classification model

The `dot_product` and `reverse_image` models demonstrate how to use the Open Inference Protocol (OIP) with Vantiq’s 
Remote source capabilities. These simple examples illustrate how to send and receive tensors, and how to configure 
options that control data formats and tensor handling.

We now move beyond these basic examples and construct a more realistic image classification pipeline.

This example uses the `google/vit-base-patch16-224` model from the Hugging Face Model Hub - a Vision Transformer (ViT) pre-trained on the ImageNet dataset.

To support this, we will build a model pipeline — also known as an ensemble in Triton — composed of three components:

- A Python backend for pre-processing
- The ONNX version of the ViT model as the core classifier
- A Python backend for post-processing

The pre-processing step transforms the input tensor from the application into the format expected by the model.
The post-processing step converts the raw model output into a more usable result tailored to the application.
This structure promotes modularity, allowing each stage of the pipeline to handle a specific part of the inference flow.

> Note: If you downloaded the `model_repository.zip` file from the completed _Open Inference_ tutorial, you still need
to download the model as instructed below, as the ONNX model is not included in the zip file.

### Download the model

To use the `google/vit-base-patch16-224` model, we must first download it from the Hugging Face Model Hub and convert it to ONNX format.
This requires Python version 3.8 or higher to be installed.

Within the _tutorial_ directory, create a python virtual environment and install the Hugging Face optimum CLI, which 
will be used to download and convert the model:

```bash
python -m venv venv
source venv/bin/activate
pip install "optimum[exporters]"
```

Next, download the model using the following command:

```bash
optimum-cli export onnx --model google/vit-base-patch16-224 vit-onnx/
```

The model is downloaded and converted to ONNX format, with the resulting files saved in the `vit-onnx` directory.

### Create the model files

In the `model_repository` directory, create four subdirectories to define the components of the image classification pipeline: `vit_preprocess`, `vit_classifier`, `vit_postprocess`, and `vit_pipeline`.

- `vit_preprocess`: a Python backend that transforms the input image into the format expected by the classifier
- `vit_classifier`: the ONNX model based on `google/vit-base-patch16-224`, which performs image classification
- `vit_postprocess`: a Python backend that extracts the top predictions from the classifier output
- `vit_pipeline`: a Triton ensemble that chains the three components together into a single, callable model

```bash
mkdir model_repository/vit_preprocess 
mkdir model_repository/vit_classifier 
mkdir model_repository/vit_postprocess 
mkdir model_repository/vit_pipeline
```

#### vit_classifier model

Inside the `vit_classifier` directory, create a subdirectory named `1`. Within this directory, copy the ONNX model file from the `vit-onnx` directory:

```bash
mkdir model_repository/vit_classifier/1
cp vit-onnx/model.onnx model_repository/vit_classifier/1
```

Within the `vit_classifier` directory, create a file named `config.pbtxt` with the following content:

```text
name: "vit_classifier"
platform: "onnxruntime_onnx"
max_batch_size: 8

input [
  {
    name: "pixel_values"
    data_type: TYPE_FP32
    dims: [ 3, 224, 224 ]
  }
]

output [
  {
    name: "logits"
    data_type: TYPE_FP32
    dims: [ 1000 ]
  }
]
```

This file defines the model's inputs and outputs. The `pixel_values` input is a 3-dimensional tensor representing the image,
and the `logits` output is a 1-dimensional tensor containing the classification scores for each of the 1,000 ImageNet classes.
The input and output tensor names, `pixel_values` and `logits`, are defined by the model itself.

#### vit_preprocess model

The pre-processing step converts the input image provided by the application into the format expected by the ViT model.

Within the `vit_preprocess` directory, create a file named `config.pbtxt` with the following content:

```text
name: "vit_preprocess"
backend: "python"
max_batch_size: 0 # Simplifies handling of single image bytes

input [
  {
    name: "RAW_IMAGE"
    data_type: TYPE_STRING
    dims: [ 1 ]
  }
]

output [
  {
    name: "pixel_values"
    data_type: TYPE_FP32
    dims: [ 3, 224, 224 ]
  }
]
```

Inside the `vit_preprocess` directory, create a subdirectory named `1`. Within this directory, create a file named `model.py` with the following content:

```python
import io
import numpy as np
from PIL import Image
import triton_python_backend_utils as pb_utils

class TritonPythonModel:
    """
    Performs manual preprocessing for a ViT model.
    """

    def initialize(self, args):
        # Define model-specific parameters manually
        self.image_size = (224, 224)
        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    def execute(self, requests):
        responses = []
        for request in requests:
            # Get raw image bytes
            raw_image_bytes = pb_utils.get_input_tensor_by_name(
                request, "RAW_IMAGE"
            ).as_numpy()[0]

            # Preprocess raw image bytes into a normalized, model-ready tensor.
            image = Image.open(io.BytesIO(raw_image_bytes)).convert("RGB")
            image = image.resize(self.image_size)
            image_np = np.array(image, dtype=np.float32) / 255.0
            normalized_np = (image_np - self.mean) / self.std
            transposed_np = normalized_np.transpose((2, 0, 1))
            output_tensor = pb_utils.Tensor("pixel_values", transposed_np)

            inference_response = pb_utils.InferenceResponse(
                output_tensors=[output_tensor]
            )
            responses.append(inference_response)

        return responses
```

> Note: for the purpose of this tutorial, the image preprocessing steps are simplified and written manually using Pillow and NumPy.
In a production setting, however, it is recommended to use the official ViTImageProcessor from Hugging Face to guarantee 
that the preprocessing perfectly matches the model's training conditions.

#### vit_postprocess model

The post-processing step converts the model's output logits into a human-readable format, such as class labels and probabilities.

Within the `vit_postprocess` directory, create a file named `config.pbtxt` with the following content:

```text
name: "vit_postprocess"
backend: "python"
max_batch_size: 8

# Input tensor for the raw logits from the main model
input [
  {
    name: "logits"
    data_type: TYPE_FP32
    dims: [ 1000 ]
  }
]

# Output tensor containing the JSON string of top 3 predictions
output [
  {
    name: "top_3_predictions"
    data_type: TYPE_STRING
    dims: [ 1 ]
  }
]
```

Within the `vit_postprocess` directory, create a subdirectory named `1`. Within this directory, create a file named `model.py` with the following content:

```python
import json
import numpy as np
import triton_python_backend_utils as pb_utils
import os

class TritonPythonModel:
    """
    This model takes raw logits, applies softmax, and returns a JSON string
    containing the top 3 class labels and their probabilities.
    """

    def initialize(self, args):
        # Load config.json and extract the label dictionary
        labels_path = os.path.join(args['model_repository'], args['model_version'], 'config.json')

        try:
            with open(labels_path, "r") as f:
                config_data = json.load(f)
                self.labels = config_data.get("id2label")
            if not self.labels:
                raise pb_utils.TritonModelException("Could not find 'id2label' key in the JSON file.")
        except Exception as e:
            raise pb_utils.TritonModelException(f"Failed to load or parse config file '{labels_path}'. Reason: {e}")

    def execute(self, requests):
        # Converts input logits to a JSON string with the top 3 labeled predictions.
        responses = []

        for request in requests:
            # Get the input tensor 'logits'
            logits_tensor = pb_utils.get_input_tensor_by_name(request, "logits")
            logits = logits_tensor.as_numpy().flatten()

            # Apply softmax to convert logits to probabilities, then get the top 3 predictions
            exp_logits = np.exp(logits - np.max(logits))
            probabilities = exp_logits / np.sum(exp_logits)

            top_3_indices = np.argsort(probabilities)[-3:][::-1]
            predictions = []
            for idx in top_3_indices:
                i = int(idx)  # Convert to Python int
                label = self.labels.get(str(i), f"class_{i}")
                prob = float(probabilities[i])

                predictions.append({
                    "label": label,
                    "probability": prob
                })

            output_string = json.dumps({"predictions": predictions})
            out_tensor = pb_utils.Tensor(
                "top_3_predictions",
                np.array([output_string], dtype=np.object_)
            )
            inference_response = pb_utils.InferenceResponse(output_tensors=[out_tensor])
            responses.append(inference_response)

        return responses
```

Then, copy the configuration JSON file from the `vit-onnx` directory, which is a subdirectory of the *tutorial directory*.
This file contains the classification labels used to map model outputs to human-readable label names:

```bash
# File containing the classification labels
cp vit-onnx/config.json model_repository/vit_postprocess/1
```

### Create the pipeline model

In this section, we create a Triton ensemble model that combines pre-processing, classification, and post-processing 
into a single pipeline for end-to-end inference.

Within the `vit_pipeline` directory, create a file named `config.pbtxt` with the following content:

```text
name: "vit_pipeline"
platform: "ensemble"
max_batch_size: 0   # must match vit_preprocess

input [
  {
    name: "RAW_IMAGE"
    data_type: TYPE_STRING
    dims: [1]        # string of raw image bytes
  }
]

output [
  {
    name: "top_3_predictions"
    data_type: TYPE_STRING
    dims: [1]        # JSON string (or plain text) with top-3 labels
  }
]

ensemble_scheduling {
  step [
    {
      model_name: "vit_preprocess"
      model_version: -1            # use latest
      input_map {
        key: "RAW_IMAGE"           value: "RAW_IMAGE"
      }
      output_map {
        key: "pixel_values"        value: "pixel_values"
      }
    },
    {
      model_name: "vit_classifier"
      model_version: -1
      input_map {
        key: "pixel_values"        value: "pixel_values"
      }
      output_map {
        key: "logits"              value: "logits"
      }
    },
    {
      model_name: "vit_postprocess"
      model_version: -1
      input_map {
        key: "logits"              value: "logits"
      }
      output_map {
        key: "top_3_predictions"   value: "top_3_predictions"
      }
    }
  ]
}
```

Within the `vit_pipeline` directory, create a subdirectory named `1`, and leave it empty. The pipeline model is defined 
entirely in the `config.pbtxt` file and does not require any additional files in the versioned subdirectory.

This completes the definition and deployment of the classification model. You should now have the following directory structure:

```text
model_repository/
├── vit_classifier/
│   ├── config.pbtxt
│   └── 1/
│       └── model.onnx
├── vit_pipeline/
│   ├── config.pbtxt
│   └── 1/
├── vit_postprocess/
│   ├── config.pbtxt
│   └── 1/
│       ├── config.json
│       └── model.py
└── vit_preprocess/
    ├── config.pbtxt
    └── 1/
        └── model.py
```

> Note: This structure shows only the components of the image classification pipeline. The earlier models
> (dot_product and reverse_image) are not listed here, although they remain present in the model_repository directory.
> Python cache directories (__pycache__) created by the Triton server are also omitted.

Restart the Triton server to see the models in the server’s startup logs, confirming that they have been loaded successfully:

```text
+-----------------+---------+--------+
| Model           | Version | Status |
+-----------------+---------+--------+
| vit_classifier  | 1       | READY  |
| vit_pipeline    | 1       | READY  |
| vit_postprocess | 1       | READY  |
| vit_preprocess  | 1       | READY  |
+-----------------+---------+--------+
```

### Add an inference procedure

Within the Vantiq IDE, add a new public procedure named `classifyImage` to the `InferService` Service:

```text
package example.oip

stateless PROCEDURE InferService.classifyImage(imageName String)

var content = Utils.packageReference("documents/" + imageName)

var payload = {
	inputs: [
    {
	  "name": "RAW_IMAGE",
      "shape": [1],             
      "datatype": "BYTES",
      "data": [ content ]
    }
  ]
}

var result = select one FROM source TritonServer with path = "/v2/models/vit_pipeline/infer", 
												   method = "POST", body = payload

var classifyOutput = result.outputs[0].data[0]
return parse(classifyOutput)
```

Since the TritonServer source is configured with the `openInference` property set to `true`, the image is sent as a binary payload.
The model receives the raw image bytes in the `RAW_IMAGE` input tensor. The request payload does not include
an `outputs` section, so all output tensors are returned by default - in this case the `top_3_predictions` tensor. 

Because no `binary_data` parameters are specified, the output tensor is returned in JSON format as a string, which is the desired format.
The `parse` function is then used to convert this JSON string into a Vantiq object that the procedure returns.

Note that the model name specified in the request is `vit_pipeline`, which refers to the ensemble model defined earlier.
The inference request is routed through the ensemble: it begins with the pre-processing step, followed by the core 
classification model, and ends with post-processing, which returns the top 3 predictions.

Make sure to save the procedure, then execute it by passing the name of the image you uploaded earlier - for example `cat.jpg`.

You should receive a response similar to the following:

```json
{
   "predictions": [
      {
         "label": "tiger cat",
         "probability": 0.4318448603153229
      },
      {
         "label": "tabby, tabby cat",
         "probability": 0.2525225579738617
      },
      {
         "label": "Egyptian cat",
         "probability": 0.24466434121131897
      }
   ]
}
```

This response contains the top three predicted labels along with their associated probabilities, indicating the model’s 
confidence in each classification.

### Video Source

This tutorial used an image stored in the `system.documents` collection as input to the classification model, in order 
to focus on the use of the Open Inference Protocol. The tutorial would remain the same if a VIDEO source were used; 
only the image acquisition step would differ.

For example, you could modify the `classifyImage` procedure to retrieve the latest frame from a video source and use
it as input to the classification model:

```text
package example.oip

stateless PROCEDURE InferService.classifyImage(videoSource String)

var image = SELECT ONE FROM SOURCE @videoSource WITH 
			    resize = { maxHeight: 224, maxWidth: 224 }

var content = Utils.packageReference(image.contentRef)

var payload = {
	inputs: [
    {
	  "name": "RAW_IMAGE",
      "shape": [1],             
      "datatype": "BYTES",
      "data": [ content ]
    }
  ]
}

var result = select one FROM source TritonServer with path = "/v2/models/vit_pipeline/infer", 
												   method = "POST", body = payload

var classifyOutput = result.outputs[0].data[0]
return parse(classifyOutput)
```

## Conclusion

This tutorial demonstrated how to use the Open Inference Protocol (OIP) with Vantiq’s Remote source capabilities 
to perform AI model inference through the Triton Inference Server.

We began with simple examples to introduce the core concepts: a vector multiplication model to show basic tensor exchange, 
and an image reversal model to illustrate binary data handling and fine-grained control over tensor serialization.
We then progressed to a more advanced use case: an image classification pipeline built using a Triton ensemble composed 
of pre-processing, a ViT-based ONNX classifier, and post-processing stages.

Along the way, you learned how to:

- Deploy models to Triton and organize them in a `model_repository`
- Configure a Remote source in Vantiq to communicate with an OIP-compatible inference server
- Send and receive tensors in both JSON and binary formats using `openInference`, `openInferenceReshape`, and `binary_data` settings
- Use Vantiq Services to construct procedures that invoke models and handle the results programmatically

These examples provide a practical foundation for integrating AI models into Vantiq applications using the Open Inference 
Protocol, with Triton as an example implementation.
