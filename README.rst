PVC
===

PVC is a REST API and clients for packages.vectorlinux.com.
The REST API provides access to the Vector Linux repository. A web client will
be developed in parallel, and more clients will follow (many applications have
use cases for the API.)


State
-----

PVC is in very early development.


TODO
----

In no particular order:

* Factor out big fat angular script into services
* Images service (image requests will go through a separated service) 
* Split static site (the web client will not live with the API in the server)
* Python client for the API using python-requests
* Authentication for the API 
* Schema consolidation
* Deployment tools
* Everything
