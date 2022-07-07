# userparameters
Test task web application for managing user parameters in database using Flask web-framework
# Tech
- Flask
- Swagger
- SQLAlchemy
- MySQL DBMS
- Celery task queue
- Redis DBMS
- Docker
# Deploy
Build and docker containers:
```bash
docker-compose up -d --remove-orphans --build
```
Stop and remove docker containers:
```bash
docker-compose down --remove-orphans
```

Check all running containers:
```bash
docker ps -a
```
Check logs of docker-container:
```bash
docker logs --tail {amount of last rows} --follow --timestamps {container_name}
```
# Usage
Go to http://localhost:5000/api/docs/ to test web-application using Swagger UI.
Also, this app available on address http://89.108.77.101:5000/api/docs/
