## About

A simple http server framework base on Python BaseHTTPServer

#### Features
	Support python2 and python3
	Use threading to process requests (No blocking)
	Support https
	Include simple route
	Dynamic load worker class

#### Support methods
	GET	-
	POST	-
	PUT	-
	DELETE	-

## Quick Start:
#### Start Server
	python server.py
	
#### Test Server
	curl localhost:5000

## Route Settings

### Add New Route

	To set route, just need to modify app/route.py and specify route and worker

### Route Settings

#### Route Parameters
	
Default
	
	'/request/path/{VAR_NAME}'

Filter Number only

	'/request/path/{VAR_NAME|n}'
	
Filter Charactor only

	'/request/path/{VAR_NAME|c}'


#### Worker

The worker definition

	{WORKER_MODULE_PATH}(/{WORKER_CLASS_NAME})

Supply module path and class name (class name is optional)

	'app.api.index/Index'

So, if only module path is supplied like

	'app.api.index'

The loader will automatically load the first worker class under the module
	
	
