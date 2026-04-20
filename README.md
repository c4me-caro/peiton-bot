
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