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

## Actualizaciones recientes

- Se agregó soporte para cifrado híbrido utilizando BB84, Diffie-Hellman y AES-GCM.
- Mejoras en la validación de claves para algoritmos de cifrado.
- Se corrigieron errores en el cifrado y descifrado de mensajes con RSA.
- Se implementaron pruebas unitarias adicionales para garantizar la calidad del cifrado y descifrado.

## Ejecución de pruebas

puedes crear tus propias pruebas unitarias para verificar la funcionalidad de los algoritmos de cifrado y descifrado. A continuación, se describe un paso a paso para hacerlo:

1. **Crea un archivo de pruebas**:

   - En el directorio `crypto_app/src`, crea un archivo llamado `test_algorithms.py`.

2. **Escribe las pruebas**:

   - Utiliza el módulo `unittest` o `pytest` para escribir tus pruebas. Por ejemplo:

     ```python
     import unittest
     from crypto_app.src.algorithms.aes import encrypt, decrypt

     class TestAES(unittest.TestCase):
         def test_encrypt_decrypt(self):
             message = "Hola, mundo!"
             key = "clave_secreta"
             encrypted = encrypt(message, key)
             decrypted = decrypt(encrypted, key)
             self.assertEqual(message, decrypted)

     if __name__ == "__main__":
         unittest.main()
     ```

3. **Ejecuta las pruebas**:

   - Abre una terminal en el directorio raíz del proyecto y ejecuta:

     ```bash
     python -m unittest discover -s crypto_app/src -p "test_*.py"
     ```

   - Si prefieres usar `pytest`, instala la librería si no está disponible:

     ```bash
     pip install pytest
     ```

     Luego, ejecuta:

     ```bash
     pytest crypto_app/src
     ```

4. **Revisa los resultados**:
   - Los resultados de las pruebas se mostrarán en la terminal, indicando si todas las pruebas pasaron o si hubo fallos.

## Despliegue

Para desplegar en Heroku u otra plataforma compatible con Procfile:

```bash
heroku create
git push heroku main
```

## Contribuciones

¡Las contribuciones son bienvenidas! Abre un issue o envía un pull request.
