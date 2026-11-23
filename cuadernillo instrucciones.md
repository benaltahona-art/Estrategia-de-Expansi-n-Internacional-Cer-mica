m# Dashboard de Decisión de Exportación - Corona (Colombia)
### Producto: HS 690722 (Baldosas cerámicas de absorción > 0,5 % y hasta 10 %)
### Mercados: Costa Rica, Dominican Rep., Guatemala, Honduras y Panamá (2022-2024)

Dashboard interactivo desarrollado en **Python** con **Streamlit** y **Plotly** para evaluar y priorizar mercados objetivo de exportación en Centroamérica y el Caribe para **Corona (Colombia)**, mediante un modelo multicriterio cuantitativo fundamentado en datos oficiales de comercio exterior.

---

## 🎯 Hallazgos y Recomendación Estratégica

A partir de los datos analizados del período 2022-2024:
1. **Mercado Prioritario Recomendado:** **Costa Rica** (Puntaje Base: **70.86 / 100**).
   - Es el mercado con mayor estabilidad de importaciones (CV = 0.149), menor nivel de concentración de competidores (HHI = 2,212) y mayor penetración histórica consolidada de Colombia (9.08 % promedio).
2. **Alternativa 1 (Expansión Dinámica):** **Guatemala** (Puntaje Base: **61.66 / 100**).
   - Segundo mercado más grande, líder en crecimiento relativo y con participación colombiana en ascenso acelerado (del 3.3 % al 8.9 % en 2024).
3. **Alternativa 2 (Hub Logístico):** **Panamá** (Puntaje Base: **40.79 / 100**).
   - Proximidad logística y presencia estable de Colombia (~4.8 %).

---

## 📂 Estructura del Repositorio

```text
├── app.py                                   # Aplicación principal de Streamlit
├── requirements.txt                         # Dependencias del proyecto
├── README.md                                # Documentación e instrucciones
├── data/                                    # Carpeta de datos fuente (CSV)
│   ├── ranking_final_mercados_corregido.csv # Indicadores normalizados y puntajes por escenario
│   ├── base_anual_paises.csv                # Importaciones anuales, peso, cuota Colombia y HHI
│   ├── importaciones_por_proveedor.csv      # Proveedores por país y año
│   └── exportaciones_colombia_dane.csv      # Exportaciones totales de Colombia (DANE)
```

---

## 🚀 Instrucciones para Ejecución Local

### 1. Clonar el repositorio y ubicarse en la carpeta
```bash
git clone <URL_DEL_REPOSITORIO>
cd data_ceramica
```

### 2. Crear y activar un entorno virtual (recomendado)
```bash
# Windows
py -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar la aplicación Streamlit
```bash
streamlit run app.py
```
La aplicación se abrirá automáticamente en su navegador web en `http://localhost:8501`.

---

## ☁️ Instrucciones para Desplegar en Streamlit Community Cloud

1. **Subir el código a GitHub:**
   - Cree un nuevo repositorio público o privado en GitHub.
   - Suba todos los archivos manteniendo `app.py`, `requirements.txt` y la carpeta `data/` en la raíz.
2. **Conectar con Streamlit Community Cloud:**
   - Inicie sesión en [share.streamlit.io](https://share.streamlit.io/) con su cuenta de GitHub.
   - Haga clic en el botón **"New app"**.
3. **Configurar los parámetros del despliegue:**
   - **Repository:** seleccione su repositorio de GitHub.
   - **Branch:** `main` (o `master`).
   - **Main file path:** `app.py`.
4. **Desplegar:**
   - Haga clic en **"Deploy!"**. Streamlit instalará automáticamente las librerías listadas en `requirements.txt` y publicará la aplicación con una URL pública accesible.

---

## 📊 Fuentes de Información y Limitaciones

- **Fuentes:** 
  - *UN Comtrade:* Importaciones reportadas por Costa Rica, Dominican Rep., Guatemala, Honduras y Panamá para la subpartida HS 690722 en USD corrientes.
  - *DANE-DIAN:* Estadísticas oficiales de exportación total de Colombia en millones de USD FOB.
- **Nota de Limitaciones:** La subpartida arancelaria **HS 690722** clasifica baldosas cerámicas con absorción de agua entre 0,5 % y 10 %, abarcando múltiples formatos, acabados y fabricantes internacionales, por lo que no corresponde exclusivamente a la producción de piso de Corona.

