# EventHub - Entorno inicial de pruebas

Este proyecto contiene las tres funciones de lógica de negocio en Python y la estructura para comenzar a diseñar las pruebas desde cero.

## Contenido

- `business_logic.py`: código original de las tres funciones.
- `simular.py`: menú interactivo para ingresar datos y ejecutar cada función por separado.
- `tests/`: archivos separados para diseñar las pruebas de cada función. Están vacíos intencionalmente.
- `requirements.txt`: dependencias para pruebas y cobertura.
- `pytest.ini`: configuración para descubrir las pruebas.
- `.coveragerc`: configuración de cobertura de sentencias y ramas.

## 1. Abrir el proyecto

Descomprime el archivo y abre la carpeta `EventHub_Pruebas_Inicial` en Visual Studio Code.

Abre una terminal integrada desde el menú **Terminal > New Terminal**.

## 2. Crear y activar un entorno virtual manualmente

Ejecuta estos comandos, uno por uno, desde la carpeta del proyecto:

```bash
python -m venv .venv
```

Activa el entorno virtual según tu sistema:

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
.venv\\Scripts\\Activate.ps1
```

Si PowerShell bloquea la activación, puedes continuar usando el intérprete de `.venv` directamente o ajustar la política de ejecución según las reglas de tu equipo. No es necesario usar scripts `.bat`.

## 3. Instalar las dependencias manualmente

Con el entorno virtual activado, ejecuta:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Simular las funciones ingresando datos

Ejecuta:

```bash
python simular.py
```

El menú permite ejecutar por separado:

1. `calculateTicketPrice`
2. `validateBookingEligibility`
3. `evaluateEventAlerts`

El simulador solicita los datos por teclado y muestra el resultado que devuelve cada función.

## 5. Ejecutar las pruebas

Cuando se hayan diseñado y escrito los casos en los archivos de `tests/`, ejecuta:

```bash
python -m pytest -v
```

**Importante:** los archivos de pruebas están vacíos. Si ejecutas pytest antes de escribir pruebas, indicará que no encontró pruebas. Esto es intencional: no se incluyeron casos de prueba.

## 6. Medir cobertura de sentencias y ramas

Después de escribir las pruebas, ejecuta manualmente:

```bash
python -m coverage erase
python -m coverage run --branch -m pytest
python -m coverage report -m
```

Para generar el informe HTML:

```bash
python -m coverage html
```

Abre `htmlcov/index.html` en el navegador.

- La cobertura de sentencias indica qué líneas se ejecutaron.
- La opción `--branch` registra también la cobertura de ramas o decisiones.
- La cobertura de ramas no demuestra por sí sola cobertura de condiciones individuales ni cobertura completa de caminos. Esos análisis deberán diseñarse y justificarse por separado.

## 7. Orden de trabajo recomendado

1. Revisar las entradas y salidas de cada función.
2. Diseñar particiones de equivalencia.
3. Diseñar valores límite.
4. Diseñar pruebas de caja blanca para sentencias, decisiones y condiciones.
5. Construir el grafo de flujo y seleccionar caminos independientes.
6. Ejecutar las pruebas y registrar resultados.
7. Generar y analizar los informes de cobertura.

## Requisito

Se recomienda Python 3.10 o superior.
