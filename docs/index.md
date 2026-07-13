# Vantiq

**Vantiq** is an __Enterprise HP aPaaS__ – a High Productivity Application platform as a service (__aPaaS__) 
solution for development, deployment and execution of real-time event-driven enterprise applications.  It provides 
“low code” and “no-code” rapid application development (RAD) features to enable high productivity.  Modelo is targeted 
at application developers building real-time event-driven applications – such as with industrial IoT, consumer IoT, AI 
applications involving machine-learning(ML), neural networks, AR/VR etc.

With Vantiq, the real-time platform extends from Cloud-to-Edge, with connectivity to ‘edge/gateway’ devices extending to last-mile micro-edge devices.

#### Vantiq includes the following Editions:
* Cloud Edition: For Vantiq cloud
* Server Edition: For client-hosted on-prem/private cloud
* Edge Edition: For Edge “gateway devices”
* Micro Edition: For “edge of edge” Micro-devices

#### Vantiq has 3 key components

1. Real-time, Event-centric Secure, Elastic, Scalable Application Platform
2. Low-code & No-code Powerful Productivity Tools
3. Optimized Deployment on the Cloud, Edge and on-premise

#### Real-time Event-centric Application Platform built on a “Reactive framework”
Vantiq is implemented on a Reactive framework. Vantiq supports design and run-time for applications serving 
billions of business events.  Its distributed, multi-tenant core is portable across cloud (public and private), data 
center and edge. It is highly available, leveraging Reactive event processing for scalability. It is clusterable and 
replicated for simple scaling and fault tolerance.

#### Low-code & No-code Powerful Productivity Tools
Vantiq tooling supports visual declaration of components to generate applications, plus high level scripting for more 
complex elements of Real-time Business Applications not suited to visual development. It provides all the benefits of an 
event-based architecture and Reactive programming, but only requires understanding of JavaScript and SQL. These low-code 
tools include System Modeler, Client Builder, App Builder, Collaboration Builder, and more.

Integration with external systems is enabled through Vantiq Enterprise Connectors.  
Vantiq IDE supports 2 entry points – one for designing and developing 
applications and the other for deploying/monitoring the application (Development and Operations entry points).  


High Productivity graphical tools include:

* [Vantiq IDE](ide.md)
* [Design Modeler](designmodeler.md)
* [System Modeler](tutorials/systemmod.md)
* [Client Builder](cbuser.md)
* [Service Builder](services.md)
* [Visual Event Handler Builder](apps.md)
* [GenAI Builder](genaibuilder.md)

#### Optimized Deployment on the Cloud, Edge and on-premise
Vantiq allows an arbitrary topology of an unlimited number of nodes across a distributed environment. Nodes can be 
peered horizontally to provide more processing power. When the volume of data collected is too great to upload it for 
centralized processing or when low latency is required, nodes can be arranged in a tree structure to handle the processing 
close to the data at the edge. The ability to cluster nodes horizontally not just for scale but failover ensures mission 
critical availability. Since any artifact in the system can be changed dynamically, available nodes can take over or new 
nodes can be launched in case of a failure.

## Using the Documentation

The documentation provides a number of fully worked examples as well as descriptions of each Vantiq feature and the 
details necessary to use the feature effectively.

We recommend starting with the tutorials that contain fully worked example automation systems:

* [Quickstart](tutorials/quickstart.md)
* [Overview](tutorials/tutorial.md)
* [Sources](tutorials/sourcetutorial.md)
* [Analytics](tutorials/analytics.md)
* [System Modeler](tutorials/systemmod.md)
* [Image Mapping](tutorials/imagemaptutorial.md)
* [Debugging](tutorials/debugtutorial.md)
* [Collaborations](tutorials/introcollaboration.md)
* [Client Builder](tutorials/client.md)
* [User and Namespace Administration](tutorials/admin.md)
* [Deployment](tutorials/deploymenttutorial.md)

The [API Reference Guide](api.md) and the [Resource Reference Guide](resourceguide.md) contain detailed 
information on the available resources and the structure of the REST API for accessing the resources. The 
[Rule and Procedure Reference Guide](rules.md) describes all the features available for creating rules to ingest 
data, identify situations and produce actions and notifications.

The resources can also be accessed from the [Vantiq IDE](https://dev.vantiq.com) and from the Vantiq CLI 
[CLI Reference Guide](cli.md).

The integration of external sources and systems is documented in the [Source Overview](sources/source.md).

