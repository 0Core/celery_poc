# Flask -> Celery with RabbitMQ and Redis 

***Run docker compose with RabbitMQ,Redis and Flask server with demo application
```
./run-local
```

***Shutdown docker compose

```
./close-local
```

***Use curl or postman

```
#return server status
GET http://localhost:7090

#create celery async task and return task id
POST http://localhost:7090/task  

#use previous task id for polliing
#return json with state and result when ready
GET http://localhost:7090/task/task_id_from_previous_response

```
