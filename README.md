# Aplicación de Criptografía

## Descripción general

La Aplicación de Criptografía es una aplicación en Python diseñada para cifrar y descifrar mensajes usando distintos algoritmos criptográficos. Cuenta con una interfaz de usuario que permite ingresar mensajes, seleccionar métodos de cifrado y visualizar los resultados.

## Características

- Selección dinámica de algoritmos de cifrado.
- Gestión de claves por parte del usuario con validación.
- Descifrado preciso para recuperar el texto original.
- Eliminada la función de hashing.

## Estructura del proyecto

```plaintext
.
├── main.py                  # Punto de entrada para iniciar la API con Uvicorn
├── Procfile                 # Definición de proceso para despliegue (Heroku, etc.)
├── crypto_app               # Código fuente de la aplicación
│   ├── __init__.py
│   ├── src
│   │   ├── API.py            # Endpoints de la API con FastAPI
│   │   ├── encryption.py     # Funciones de cifrado de mensajes
│   │   ├── decryption.py     # Funciones de descifrado de mensajes
│   │   ├── Key.py            # Gestión de claves por defecto
│   │   ├── default_keys.json # Claves por defecto en JSON
│   │   └── algorithms        # Implementaciones de algoritmos
│   │       ├── caesar.py     # Cifrado César
│   │       ├── aes.py        # Cifrado AES
│   │       ├── rsa.py        # Cifrado RSA
│   │       └── hybrid.py     # Cifrado híbrido
│   └── tests                 # Pruebas unitarias
│       └── test_encryption.py # Pruebas para cifrado y descifrado
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación del proyecto
```

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/N3Txu/KeyPass.git
   ```
2. Accede al directorio del proyecto:
   ```bash
   cd KeyPass
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta la aplicación localmente:

```bash
python main.py
```

O usando Uvicorn con recarga en desarrollo:

```bash
uvicorn API:app --reload --host 0.0.0.0 --port 5000
```

La API expone los siguientes endpoints:

- **POST /encrypt**: cifrar un mensaje.
- **POST /decrypt**: descifrar un mensaje.

Sigue las peticiones en JSON según el modelo:

```json
{
  "message": "texto",
  "algorithm": "aes"
}
```

## Algoritmos soportados

- **César**: cifrado por desplazamiento en el alfabeto.
- **AES**: cifrado simétrico estándar.
- **RSA**: cifrado asimétrico con par de claves.
- **Híbrido**: combinación de AES y RSA para seguridad y eficiencia.

## Pruebas

Para ejecutar las pruebas unitarias:

```bash
python -m unittest discover -s tests
```

## Despliegue

Para desplegar en Heroku u otra plataforma compatible con Procfile:

```bash
heroku create
git push heroku main
```

## Contribuciones

¡Las contribuciones son bienvenidas! Abre un issue o envía un pull request.
