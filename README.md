# Comandos Docker para Correr el Demo de Contenedores

A continuación se presenta una lista de comandos Docker necesarios para ejecutar el proyecto de contenedores:
### 0. **Prerequisitos**
docker
### 1. **Construir las imágenes**
```bash
docker build -t server ./server
docker build -t plotter ./plotter
docker build -t client ./client
```

### 2. **Crear una red para la comunicación entre contenedores**
```bash
docker network create my_network
```

### 3. **Crear un volumen compartido**
```bash
docker volume create shared_volume
```

### 4. **Ejecutar el contenedor del servidor**
```bash
docker run -d --name server --network my_network -v shared_volume:/shared_volume server
```

### 5. **Ejecutar el contenedor del plotter**
```bash
docker run -d --name plotter --network my_network -v shared_volume:/shared_volume plotter
```

### 6. **Ejecutar el contenedor del cliente**
```bash
docker run -it --network my_network --name client client
```

### 7. **Ver los logs de un contenedor**
```bash
docker logs servidor
# o
docker logs plotter
```

### 8. **Detener y eliminar todos los contenedores**
```bash
docker stop servidor plotter
docker rm servidor plotter
```
### 9. **Entrar a la terminal de un contenedor**
```bash
 docker exec -it <nombre_contenedor> /bin/bash
```
---
