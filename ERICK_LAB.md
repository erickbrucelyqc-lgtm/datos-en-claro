# Insight Lab · Erick Quio

**Dashboard interactivo de datos sobre Streamlit.** Este fork conserva el proyecto
[Streamlit](https://github.com/streamlit/streamlit) y su licencia Apache-2.0.
La aportación local es una demo independiente; no es una contribución aceptada por upstream.

## Qué incluye

- Carga de CSV con validación de columnas, fechas e importes finitos.
- Filtros por categoría, tres indicadores, distribución y evolución diaria.
- Descarga de la selección y estados vacíos comprensibles.
- Datos sintéticos reproducibles y pruebas de interacción con AppTest.

## Ejecutar la demo

Desde la raíz del fork, en un entorno Python 3.12 independiente con `uv`:

```bash
uv run --no-project --with-requirements erick_requirements.txt streamlit run erick_dashboard.py
```

Abre la URL local que muestra Streamlit. El archivo de ejemplo tiene diez registros
y un importe total de **USD 11 750**. La categoría Software suma **USD 4 450**.

### Formato del CSV

```csv
date,category,amount
2026-01-01,Software,1200
2026-01-02,Datos,700
```

Los importes se interpretan como USD; el programa no convierte monedas. Se admiten
importes negativos para ajustes. Las filas inválidas se descartan con un aviso.
El CSV se procesa en el servidor local de Streamlit; esta demo no llama APIs externas.

## Verificación

```bash
uv run --no-project --with-requirements erick_requirements.txt python -m pytest test_erick_dashboard.py -q
```

Verificado con Python 3.12, Streamlit 1.66.1 y pandas 3.1.0: carga de muestra,
métricas, filtro por categoría, selección vacía y validación de datos.
Estas pruebas cubren la demo; no constituyen una ejecución de la suite de Streamlit.

## Archivos de esta adaptación

`erick_dashboard.py`, `erick_sample.csv`, `erick_requirements.txt`,
`test_erick_dashboard.py`, `erick_cover.svg` y esta guía.
