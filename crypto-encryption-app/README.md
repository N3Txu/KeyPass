# Aplicación de Criptografía

## Descripción general

La Aplicación de Criptografía es una aplicación en Python diseñada para cifrar y descifrar mensajes usando distintos algoritmos criptográficos. Cuenta con una interfaz de usuario que permite ingresar mensajes, seleccionar métodos de cifrado y visualizar los resultados.

## Características

- Selección dinámica de algoritmos de cifrado.
- Gestión de claves por parte del usuario con validación.
- Descifrado preciso para recuperar el texto original.
- Eliminada la función de hashing.

## Estructura del proyecto

```
crypto-encryption-app
├── src
│   ├── main.py               # Punto de entrada de la aplicación
│   ├── encryption.py         # Funciones de cifrado de mensajes
│   ├── decryption.py         # Funciones de descifrado de mensajes
│   ├── algorithms            # Directorio con implementaciones de algoritmos
│   │   ├── caesar.py         # Implementación del cifrado César
│   │   ├── aes.py            # Implementación AES
│   │   ├── rsa.py            # Implementación RSA
│   │   └── hybrid.py         # Implementación híbrida
│   └── ui.py                 # Gestión de la interfaz de usuario
├── tests                     # Pruebas unitarias
│   └── test_encryption.py    # Pruebas para funciones de cifrado y descifrado
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
   cd crypto-encryption-app
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta la aplicación con:

```bash
python src/main.py
```

Sigue las indicaciones:

1. Cifrar un mensaje
2. Descifrar un mensaje
3. Salir

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

## Contribuciones

¡Las contribuciones son bienvenidas! Abre un issue o envía un pull request.
