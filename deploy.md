# Guía de Despliegue - Simulador de Cartera Hipotecaria

## Opción 1: Despliegue en Heroku (Recomendado)

### Preparación
1. Crea una cuenta en [Heroku](https://heroku.com)
2. Instala [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Instala [Git](https://git-scm.com/) si no lo tienes

### Pasos para desplegar:

1. **Crear archivo requirements.txt** (crear en la raíz del proyecto):
```
Flask==2.3.3
gunicorn==21.2.0
email-validator==2.0.0
```

2. **Crear archivo Procfile** (crear en la raíz del proyecto):
```
web: gunicorn main:app
```

3. **Subir a GitHub primero**:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/simulador-cartera-hipotecaria.git
git push -u origin main
```

4. **Crear aplicación en Heroku**:
```bash
heroku create nombre-de-tu-app
```

5. **Configurar variables de entorno**:
```bash
heroku config:set SESSION_SECRET="tu-clave-secreta-muy-segura"
heroku config:set WHATSAPP_NUMBER="57300XXXXXXX"
```

6. **Desplegar**:
```bash
git push heroku main
```

## Opción 2: Despliegue en Railway

1. Ve a [Railway](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Configura las variables de entorno:
   - `SESSION_SECRET`
   - `WHATSAPP_NUMBER`
4. Railway detectará automáticamente que es una aplicación Flask

## Opción 3: Despliegue en Render

1. Ve a [Render](https://render.com)
2. Conecta tu repositorio de GitHub
3. Configura el servicio:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
4. Agrega las variables de entorno

## Opción 4: Despliegue en Google Cloud Platform

1. Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com)
2. Habilita App Engine
3. Crea archivo `app.yaml`:
```yaml
runtime: python39

env_variables:
  SESSION_SECRET: "tu-clave-secreta"
  WHATSAPP_NUMBER: "57300XXXXXXX"
```
4. Despliega: `gcloud app deploy`

## Configuración de Variables de Entorno

### SESSION_SECRET
- Genera una clave secreta fuerte
- Ejemplo: `python -c "import secrets; print(secrets.token_hex(32))"`

### WHATSAPP_NUMBER
- Formato: 57300XXXXXXX (código país + número sin espacios)
- Ejemplo: 573001234567

## Archivos Necesarios para el Despliegue

Asegúrate de tener estos archivos en tu repositorio:

1. **requirements.txt** - Dependencias de Python
2. **Procfile** - Comando para iniciar la aplicación
3. **app.py** - Aplicación Flask principal
4. **main.py** - Punto de entrada
5. **templates/** - Carpeta con plantillas HTML
6. **static/** - Carpeta con archivos CSS/JS
7. **README.md** - Documentación del proyecto
8. **.gitignore** - Archivos a ignorar por Git

## Comandos Git para Subir a GitHub

```bash
# Inicializar repositorio
git init

# Agregar archivos
git add .

# Hacer commit
git commit -m "Simulador de compra de cartera hipotecaria"

# Cambiar a rama main
git branch -M main

# Agregar repositorio remoto
git remote add origin https://github.com/tu-usuario/simulador-cartera-hipotecaria.git

# Subir código
git push -u origin main
```

## Verificación del Despliegue

Una vez desplegado, verifica que:
1. La aplicación carga correctamente
2. El formulario funciona
3. Los cálculos se realizan correctamente
4. Los enlaces de WhatsApp funcionan
5. El diseño se ve bien en móvil y desktop

## Mantenimiento

- Revisa los logs regularmente
- Actualiza las tasas de interés según sea necesario
- Mantén las dependencias actualizadas
- Monitorea el rendimiento y uso

## Soporte

Si tienes problemas con el despliegue, revisa:
1. Los logs de la aplicación
2. Las variables de entorno
3. Los archivos de configuración
4. Las dependencias en requirements.txt