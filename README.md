
# Peiton-Bot

Un bot de discord hecho con python para ayudar con las tareas básicas de un servidor como saludar a nuevos miembros o administrar notificaciones
## Ejecutar localmente

Clonar el repositorio

```bash
  git clone https://github.com/c4me-caro/peiton-bot
```

Ir al directorio

```bash
  cd peiton-bot
```

Instalar las dependencias

```bash
  pip install -r requirements.txt
```

Iniciar el servicio

```bash
  python main.py
```


## Deployment

Este proyecto se ejecuta con docker, creando un artefacto con el archivo `dockerfile` o pasando el proyecto a un panel como `Dokploy`.


## Sistema de dialogs

Los dialogs emplean archivos `.json` para separar el texto de la lógica del bot, utilizando llaves `{}` como contenedores de variables dinámicas, permitiendo la personalización de respuesta de los comandos.

Ejemplo

```
{
  "commands": {
    "welcome": "@{} Se ha unido al servidor!",
  }
}
```

Respuesta

```
@usuario1 Se ha unido al servidor!
```
## API Reference

Todas las peticiones a la API deben ser realizadas utilizando en el header Authorization el raw de la `API_KEY` proporcionada al crear el servidor

#### Crear un mensaje de bienvenida

```http
  POST /api/welcomes/create
```

| Parameter     | Type     | Description                       |
| :------------ | :------- | :-------------------------------- |
| `guild_id`    | `int`    | **Required**. Servidor a usar     |
| `description` | `string` | **Required**. Mensaje a emitir    |
| `image_url`   | `string` | Un gif por estetica               |
| `channel`     | `int`    | **Required**. Canal de bienvenida |

#### Crear un nuevo alert en el servidor

```http
  POST /api/alerts/create
```

| Parameter     | Type     | Description                       |
| :------------ | :------- | :-------------------------------- |
| `guild_id`    | `int`    | **Required**. Servidor a usar     |
| `title`       | `string` | **Required**. Mensaje a emitir    |
| `image_url`   | `string` | Un gif por estetica               |
| `channel`     | `int`    | **Required**. Canal de bienvenida |

#### Emitir un alert en el servidor

```http
  GET /api/alerts/generate
```

| Parameter     | Type     | Description                 |
| :------------ | :------- | :-------------------------- |
| `id`          | `string` | **Required**. ID del alert  |
| `message`     | `string` | Mensaje o detalles a emitir |
## Comandos disponibles

### comandos del desarrollador

- sync: actualiza el arbol de comandos
- uptime: tiempo desde que el sistema esta funcionando
- ping: compobar la latencia del bot
- load: cargar una extensión del bot
- reload: recargar una extensión del bot
- unload: eliminar una extensión del bot

### comandos de moderación

- embed: generar un mensaje estilo embed
- limpiar: borrar los mensajes del canal actualiza

### comandos generales

- help: obtener ayuda del bot
- lanzar: lanza una moneda
- avatar: muestra un avatar de un perfil
