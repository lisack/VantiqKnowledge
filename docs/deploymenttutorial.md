# Application Deployment Tutorial

## Tutorial Overview

This tutorial guides a Vantiq developer through the steps that let you visualize, configure and deploy a Vantiq application to a multi-node Vantiq environment.

In this tutorial you will set up an environment containing three namespaces, import a project and use the Vantiq deployment tool to deploy the application to the target environment.
Then convert the application into a distributed application and deploy different resources to different nodes in the environment.

To get the most from this tutorial, it is highly recommended to complete the short, no-cost Vantiq [Developer Foundations Course](https://community.vantiq.com/courses/applications-developer-level-1/) first.

## Part 1: Creating Two Additional Namespaces for Your Environment

### Step 1: Creating Namespaces

This tutorial requires three namespaces.  If you have not created new namespaces in Vantiq, you should first familiarize yourself with creating and managing
namespaces in the [User and Namespace Administration Tutorial](./admin.md#task-2-adding-a-new-developer).

The first step in creating a new namespace is to change your Vantiq IDE environment to a namespace in which you have developer or higher privileges. From there, you will create more
namespaces (and nodes connecting to them) to use as a deployment environment.

In the IDE, use the **Administer** button to select **Namespaces** to open the Namespaces pane. Use the **Create New** icon button (small plus sign in a circle at the top, right of the Namespaces pane) to create new namespaces with the following names: _factory_, _store_. You should be the admin of each of 
these namespaces.

![Namespaces](../assets/img/deploymenttutorial/namespaces.png "Namespace List")

Change your Vantiq IDE to the _factory_ namespace. Go to **Administer** > **Advanced** > **Access Tokens**. Click the **Create New** icon ("+" button) in the Access Tokens pane. Create an access token named "factoryToken" with expiration date in one year.
Then save the access token value somewhere so you can reference it in the next step of this tutorial.

Change to namespace _store_, and create an access token the same way. Save the access token for use in the next step.

Change back to your original developer namespace.  This is the namespace where you will create your application, environment and deployment.

### Step 2: Creating Nodes

Make sure you are in your assigned developer namespace, not the _factory_ or _store_ namespace.  Go to **Deploy** > **Nodes** and click the **Create New** icon ("+" button) in the Nodes pane to create a new node named "factoryNode".  The URI of the node should match the URI of your current running IDE (e.g. https://dev.vantiq.com).  Use "Credential Type" of "Access Token" and fill in the factoryToken value you saved from the previous step.  Finally, add a property "type = factory" and save the Node.

![factoryNode](../assets/img/deploymenttutorial/factoryNode.png "Create Factory Node") 

Repeat the above steps to create a "storeNode" using the access token from the _store_ namespace and create a new property "type = store".

![storeNode](../assets/img/deploymenttutorial/storeNode.png "Create Store Node") 

The "type" property is required on both nodes for this tutorial application to work in later steps.  You will use this property to partition resources onto different nodes.

### Step 3: Creating the Environment

The next step is to create the environment that includes the factory node and the store node.
Go to **Deploy** > **Environments** and click the **Create New** icon ("+" button) in the environment list to create a new environment named "tutorialEnv".

![newEnvironment](../assets/img/deploymenttutorial/newEnvironment.png "Create Environment")
 
When you click **OK**, the environment is created and a new IDE pane named "Environment: tutorialEnv" is automatically opened. In this environment detail pane, click the **Add Nodes by Name** button to display the _Add Nodes_ dialog. Select both _factoryNode_ and _storeNode_ to be added to this environment.

![addNodesByName](../assets/img/deploymenttutorial/addNodesByName.png "Add Nodes by Name")

Don't forget to save your environment. Now you should have an environment with two nodes in it.

![environmentWithNodes](../assets/img/deploymenttutorial/environmentWithNodes.png "Environment with 2 nodes")

## Part 2: Deploy a Project

### Step 1: Import the deployment tutorial project

Click **Projects** > **Import...** and select _Tutorials_ for the **Select Import Type** field. When the **Select From Tutorials** field appears, select _Deployment Tutorial_ from the list.
Click the **Import** button and reload your browser.

Once project _Deployment Tutorial_ is loaded, click on type _com.vantiq.ims.Store_ in the Project Contents Tree and then click **Add New Record** to add a new record to type _com.vantiq.ims.Store_. Specify _myStore_ for **storeId** and _100_ for **productCount**.  
Click on **Add New Record** to save the record. 

![AddNewRecord](../assets/img/deploymenttutorial/addNewRecord.png "AddNewRecord")

After that, use **Show All Records** from the _Type:com.vantiq.ims.Store_ pane to verify there is a record for type _com.vantiq.ims.Store_.

![ShowAllRecords](../assets/img/deploymenttutorial/showAllRecords.png "ShowAllRecords")

### Step 2: Test run the application
This sample application simulates inventory checking on a store and asks the factory for more products when inventory is low.  The factory will also notify the store when more products are shipped.
 
On the project contents tree, click _Client: StoreClient_ to open the client. Then run the client.  

![RunClient](../assets/img/deploymenttutorial/runClient.png "RunClient")

Click the **Order 1** and **Order 10** buttons multiple times until the product count drops below 50. Wait for a few seconds, you should see a popup dialog saying "More products have arrived" and the product count reset to 100.
Stop the client by clicking the **Stop Running** button.

### Step 3: Creating the deployment
The application is working fine and now it is time to deploy it to different namespaces.

Go to **Deploy** > **Deployments**, click the **New** button on the Deployments pane to create a new deployment with the following settings:

```
Name: testDeploy1
Project: DeploymentTutorial
Environment: tutorialEnv
```

![newDeployment](../assets/img/deploymenttutorial/newDeployment.png "New Deployment")



Click on the _Environment: tutorialEnv_ subtab to view the environment graph.

![testDeploy2](../assets/img/deploymenttutorial/testDeploy2.png "Deployment Environment view")

_factoryNode_ and _storeNode_ are placed in a partition labeled "default". This means all resources within the project will be deployed to every node in the environment. In this case, there are two nodes: storeNode and factoryNode.


### Step 4: Customize the deployment
In Part 2, step 1, you manually added a new record of type _com.vantiq.ims.Store_ to keep track of products in a store.  You also need a way to do that after the type _com.vantiq.ims.Store_ is deployed to a new node.

Click on the _Settings_ subtab. Click the **New Parameter** "+" button for partition "default". In the popup dialog, choose resource of _type/com.vantiq.ims.Store_ and specify a record to be added to type _com.vantiq.ims.Store_ on the target node by copying and pasting the following JSON:

    [
        {
            "storeId": "newStore",
            "productCount": 101
        }
    ] 


![newParameter](../assets/img/deploymenttutorial/newParameter.png "Settings")

The resulting parameter looks like this:

![testDeploy3](../assets/img/deploymenttutorial/testDeploy3.png "Settings view")

Save the deployment.

### Step 5: Deploy
Click on the _Deploy Results_ subtab - note there is no result showing because you have not deployed anything yet.  Click the **Deploy** button to start the deployment process. The deployment results will be updated.

![testDeploy4](../assets/img/deploymenttutorial/testDeploy4.png "Deployment Results view")

Click on "factoryNode" and "storeNode" in the results tree to view details of the deployment on each node.
Both nodes show exactly the same results because the whole project has been deployed to both of them.

### Step 6: Verify Deployment
Switch to the _factory_ namespace. Use the **Projects** menu button to select _DeploymentTutorial_by_testDeploy1_.
Test run  _Client: StoreClient_ as you have done in step 2.  Verify the deployed application is working in this namespace.

Switch to the _store_ namespace. You should be able to test run _Client: StoreClient_ the same way.

## Part 3: Convert to Distributed Application and Deploy to Multiple Nodes

### Step 1: Clean up target namespaces using Undeploy.
Switch back to DeploymentTutorial namespace and find your testDeploy1 Deployment.
Click the **Undeploy** button to undeploy the application from all nodes.  This will remove all resources from the target namespaces.
You can see what resources have been removed from the target namespace in the results subtab.

![testDeploy_undeploy](../assets/img/deploymenttutorial/testDeploy_undeploy.png "Undeploy Results view")

### Step 2: Make the application distributed
Up to this point, the entire application is running within the same namespace.  You are now going to separate the storefront functionality and factory functionality by using the "PROCESSED BY" phrase in Rules and Procedures.

On the project contents tree, click _Service: com.vantiq.ims.StoreService_ to open the service builder.  In the implementation tab of the service, select inbound event _orderProduct_ to open the event handler.  In the event handler editor, line #16, uncomment the second half of the statement to make it read as follows:

    PUBLISH msg TO SERVICE EVENT "com.vantiq.ims.FactoryService/requestMoreProducts" 
        PROCESSED BY {"ars_properties.type":"factory"}

It will publish to service event *requestMoreProducts* on a node whose *ars_properties.type* is *factory*.

On the project contents tree, click *Service: com.vantiq.ims.FactoryService* to open the service builder.  In the implementation tab of the service, select inbound event _requestMoreProducts_ to open the event handler.  In the event handler editor, line #5, uncomment the second half of the statement to make it read as follows:

     PUBLISH event.value to SERVICE EVENT "com.vantiq.ims.StoreService/shipToStore" 
        PROCESSED BY {"ars_properties.type":"store"}

It will publish to service event *shipToStore* on a node whose _ars_properties.type_ is _store_.

In both cases you use _ars_properties.type_ which you defined in the _factory_ and _store_ nodes earlier.  In your future applications, you are free to use any properties you have defined on your nodes.

Save both the services.  Now this application requires two nodes to run successfully.

### Step 3: Project Partitions
Go to Project > Show Partitions.  

![projectPartitions](../assets/img/deploymenttutorial/testDeploy1.png "Project Partitions")

Since this is the first time viewing the project partitions, Vantiq automatically created two partitions by analyzing the "processed by" phrase used in rules and procedures.

Vantiq automatically places Service _com.vantiq.ims.StoreService_ and its related types and client in a partition with the title of {"ars_properties.type":"store"}.

It also places _Service: com.vantiq.ims.FactoryService and its related type, into another partition titled {"ars_properties.type":"factory"}

In a simple application like this, the auto-partition feature of Vantiq does all the work for you. In a more complicated application, you may need to move or copy resources from partition to partition based on your application logic. Please reference the [Deployment Tool User's Guide](../deploymentuser.md#project-partitions) for more information on how to manage partitions.

Save the project to persist partitions before starting the Deployment steps.

Note: if you have visited the Project Partition pane before you modified _Service: com.vantiq.ims.StoreService_ and _Service: com.vantiq.ims.FactoryService_, then you will need to click the **Update Partitions** toolbar button to pick up changes you made to the project and partition resources correctly.
### Step 4: Add Deploy Parameter to New Partition
Since  Type _com.vantiq.ims.Store_ now belongs to partition {"ars_properties.type":"store"}, you need to add a deploy parameter to the partition to add a new record to type _com.vantiq.ims.Store_ on the target node.
Refer to Part 2, Step 2 for adding a deploy parameter.  The only difference is that you need to select the partition {"ars_properties.type":"store"} instead of "default".

![partitionParameters2](../assets/img/deploymenttutorial/testDeploy_parameter2.png "Parameter on different partition")

### Step 5: Deploy the distributed application
In Deployment _testDeploy1_ pane, click on the _Environment: tutorialEnv_ subtab to view the environment graph again.
You will see factoryNode and storeNode shown in different partitions.  This means the resources in each partition will be deployed to different nodes. 

Because custom partitions are defined, resources in the default partition will not be deployed. Therefore, the default partition is no longer shown here.

![updateEnvironment](../assets/img/deploymenttutorial/testDeploy_updateEnv.png "Updated Environment Graph")


Click the **Deploy** button. Check the results subtab to verify that different resources were deployed to different nodes.

![storeNodeResult](../assets/img/deploymenttutorial/testDeploy_storeResult.png "Store Node Result")

![factoryNodeResult](../assets/img/deploymenttutorial/testDeploy_factoryResult.png "Factory Node Result")

### Step 6: Verify Deployment
Switch to the _factory_ namespace. Use the **Projects** menu button to select _DeploymentTutorial_by_testDeploy1_.  You should see that *Service: com.vantiq.ims.FactoryService* and *Type: com.vantiq.ims.Order* were copied here.  Also, a node named _storeNode_ is copied here.

![factoryNamespace](../assets/img/deploymenttutorial/factoryNamespace.png "Factory namespace resources")

Switch to the _store_ namespace and browse around. You should see a different set of resources and nodes copied here.  View all records of type _com.vantiq.ims.Store_ and you should see a record of _newStore_ with a product count of 101. That matches the deployment parameter you created in a previous step.

![storeNamespace](../assets/img/deploymenttutorial/storeNamespace.png "Store namespace resources")

Run the client _StoreClient_ in this namespace. If you continue ordering products you should see that more products get delivered to this store when _productCount_ is below 50. This shows that the application is now running successfully on two nodes.