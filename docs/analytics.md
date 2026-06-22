# Analytics Tutorial
Sentiment Analysis Using Microsoft Azure Machine Learning Studio

## Introduction
The Microsoft Azure Machine Learning Studio (MLStudio) is a workspace for crafting machine learning "experiments". Experiments can be transformed in the MLStudio into Web Services, which allows them to be queried through a RESTful interface to get predications and classifications on demand.

To get started with MLStudio, visit [https://studio.azureml.net/](https://studio.azureml.net/) and sign up for an account if you do not have one already. Microsoft currently allows users to deploy a limited number of experiments for free and provides 10gb of free hosting for your training data. If you aren't familiar with MLStudio already, we recommend watching the tutorials and starting with some of the sample experiments or ones in the experiment gallery. Throughout this tutorial, we'll use a Predictive Experiment for Twitter sentiment analysis found here: [https://gallery.cortanaintelligence.com/Experiment/Predictive-Experiment-for-Twitter-sentiment-analysis-3](https://gallery.cortanaintelligence.com/Experiment/Predictive-Experiment-for-Twitter-sentiment-analysis-3). By the end of this tutorial, you will be able to query this experiment through a Vantiq Analytics Source to get the sentiment of any tweet.

## Setting Up an MLStudio Experiment
After creating a MLStudio account and logging into the workspace, navigate to [https://gallery.cortanaintelligence.com/Experiment/Predictive-Experiment-for-Twitter-sentiment-analysis-3](https://gallery.cortanaintelligence.com/Experiment/Predictive-Experiment-for-Twitter-sentiment-analysis-3) and click the "Open in Studio" link and click the checkmark on the "Copy experiment to gallery" pop-up. Open the experiment up from the list of experiments in your workspace, click "OK" on the bottom menu bar that indicates the experiment is being upgraded, then click run from the bottom menu. Once the run completes (can take around 10 minutes to train the model), select "Deploy Web Service" from the bottom menu and choose the recommended option. 

Once you've deployed the web service, you should be taken to a page that specifies an API key and there should be a table below with rows for the Request/Response API and the Batch API. Select the blue "TEST" button from the Request/Response row and try it out, the response will show up at the bottom of the page. To see what API calls are actually being made here, click on Request/Response in the left hand column. These docs, along with the API key from the previous page are all you need to request Sentiment Analysis from VAIL.

## Configuring the Vantiq Analytics Source
In order to make requests to MLStudio for predictions using the predictive experiment, create a new Analytics Source in your Vantiq namespace with the name "Sentiment". The Analytics Type is "Microsoft MLStudio" and the Request URI is the POST url specified in the Request/Response docs for your experiment. Specify the API key in the Access Token field then save the Analytics Source.

## Using the Analytics Source in VAIL
Now that the Analytics Source has been configured, we can try it out in VAIL. Here's an example procedure that takes a single parameter, a message to classify, and returns the response from running the predictive experiment:

```
PROCEDURE testSentimentOfStatement(msg)

// Construct the request body
// see the Request/Response docs for more details on how this is formulated
var payload = {"Inputs": { "input1": { "ColumnNames": ["tweet_text"], "Values": [[msg]]}}, "GlobalParameters": {}}

// Request the prediction from the source
var prediction = SELECT FROM SOURCE Sentiment WITH body = payload

log.info("Prediction result: {}", [prediction])

// Grab the result field
var result = prediction[0].Results

// Get the values from output1 (the name of the final activity in the experiment)
var output = result["output1"]
var values = output.value.Values
// values is actually an array, so get the first index
values = values[0]

// values is an array of length 2
// first value is the direction (positive, neutral, or negative)
// second value is the score
var polarity = values[0]
var score = values[1]

return {polarity: polarity, score: score}
```

