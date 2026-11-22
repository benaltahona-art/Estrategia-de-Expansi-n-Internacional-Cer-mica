# ¿A qué mercado debería exportar Corona baldosas cerámicas para piso?

Proyecto final de Data Mining and Business Intelligence. Compara cinco mercados de Centroamérica y el Caribe (Costa Rica, República Dominicana, Guatemala, Honduras y Panamá) para la subpartida HS 690722, años 2022 a 2024, y recomienda un mercado prioritario y dos alternativas.

**Dashboard publicado:** https://estrategia-de-expansi-n-internacional-cer-mica-gsmqlsplwmgmm45.streamlit.app/

## Qué contiene este repositorio

| Archivo | Para qué sirve |
|---|---|
| `app.py` | Código fuente del dashboard (Streamlit) |
| `requirements.txt` | Librerías necesarias |
| `analisis_mercados.ipynb` | Cuaderno de análisis: limpia datos, calcula indicadores, ranking y escenarios, y (sección 7) las cifras de precio por kg y flete de la presentación |
| `base_procesada_indicadores_corregida.csv` | Base procesada: cinco indicadores por país |
| `ranking_final_mercados_corregido.csv` | Ranking y puntajes por escenario de pesos |
| `base_anual_paises.csv` | Importaciones, participación de Colombia y HHI por país y año |
| `importaciones_por_proveedor.csv` | Importaciones por país, año y proveedor |
| `exportaciones_colombia_dane.csv` | Exportaciones totales de Colombia por año (millones de USD) |
| `UNComtrade-trade-statistics-official-CAHS-20261121-1517.xlsx` | Datos originales de UN Comtrade |
| `anex-EXPORTACIONES-SerieDestino-sep2026.xlsx` | Datos originales del DANE |

## Cómo reproducir los resultados

**Opción 1: ver el dashboard.** Abre el enlace de arriba. No necesitas instalar nada.

**Opción 2: repetir el análisis.**
1. Abre `analisis_mercados.ipynb` en Google Colab (colab.research.google.com).
2. Sube a Colab los dos archivos Excel originales.
3. Ejecuta todas las celdas en orden (Entorno de ejecución > Ejecutar todo).
4. Al final se generan los cinco CSV que usa el dashboard y la sección 7 imprime las cifras de la diapositiva de riesgos.

Si lo ejecutas fuera de Colab, instala antes `pip install pandas numpy openpyxl jupyter` (openpyxl es necesario para leer los Excel).

**Opción 3: correr el dashboard en tu computador.**
1. Instala Python 3.10 o superior.
2. En la carpeta del proyecto ejecuta `pip install -r requirements.txt`.
3. Ejecuta `streamlit run app.py`.

## Fuentes y unidades

- UN Comtrade: importaciones reportadas por cada país, subpartida 690722, USD corrientes y peso en kg.
- DANE: exportaciones totales de Colombia, millones de USD.

## Limitaciones

- La subpartida 690722 agrupa baldosas de muchos tipos y marcas, no solo el piso de Corona.
- República Dominicana no reporta peso en kg en ningún año, y Guatemala no lo reporta en 2024.
- Los datos no incluyen aranceles ni costos de flete; el precio se aproxima con el valor unitario de importación (USD/kg).
- Con solo cinco países, la normalización de 0 a 100 exagera diferencias pequeñas.
