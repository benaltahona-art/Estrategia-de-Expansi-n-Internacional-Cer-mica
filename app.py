import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración general de la página
st.set_page_config(
    page_title="Decisión de Exportación - Corona Cerámica",
    page_icon="🏺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores sutiles y elegantes (Beige cálido y Azules apagados/serenos)
COLOR_BG = "#F8F5F0"
COLOR_SIDEBAR = "#EFEAE1"
COLOR_PRIMARY = "#2B4C6F"
COLOR_SECONDARY = "#4A7C9B"
COLOR_MUTED_BLUE = "#7B9EA8"
COLOR_LIGHT_BLUE = "#BDD2DE"
COLOR_BEIGE_CARD = "#F2ECE3"
COLOR_BORDER = "#D6CABA"
COLOR_TERRACOTTA = "#C77D58"
COLOR_TEXT_MAIN = "#24323E"
COLOR_TEXT_MUTED = "#5A6E7F"

def estilo_figura(fig, height=390):
    fig.update_layout(
        font=dict(family="sans-serif", color=COLOR_TEXT_MAIN, size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(240, 234, 225, 0.45)",
        height=height,
        margin=dict(l=20, r=20, t=35, b=20),
        xaxis=dict(
            gridcolor="rgba(123, 158, 168, 0.18)",
            linecolor="rgba(123, 158, 168, 0.3)",
            tickfont=dict(color=COLOR_TEXT_MUTED)
        ),
        yaxis=dict(
            gridcolor="rgba(123, 158, 168, 0.18)",
            linecolor="rgba(123, 158, 168, 0.3)",
            tickfont=dict(color=COLOR_TEXT_MUTED)
        ),
        legend=dict(
            bgcolor="rgba(248, 245, 240, 0.85)",
            bordercolor="rgba(214, 202, 186, 0.6)",
            borderwidth=1,
            font=dict(color=COLOR_TEXT_MAIN, size=11)
        )
    )
    return fig

# Estilos CSS personalizados
st.markdown(f"""
<style>
    /* Fondo principal y contenedor general */
    .stApp {{
        background-color: {COLOR_BG} !important;
        color: {COLOR_TEXT_MAIN} !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {COLOR_SIDEBAR} !important;
        border-right: 1px solid {COLOR_BORDER} !important;
    }}
    
    /* Encabezados con mayor jerarquía, presencia y centrados */
    .header-container {{
        text-align: center !important;
        margin-top: 0.2rem !important;
        margin-bottom: 2rem !important;
        padding: 0 1rem !important;
    }}
    .main-title {{
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: {COLOR_PRIMARY} !important;
        letter-spacing: -1px !important;
        line-height: 1.15 !important;
        margin-bottom: 0.5rem !important;
        text-align: center !important;
    }}
    .sub-title {{
        font-size: 1.25rem !important;
        color: {COLOR_TEXT_MUTED} !important;
        font-weight: 450 !important;
        line-height: 1.45 !important;
        max-width: 900px !important;
        margin: 0 auto !important;
        text-align: center !important;
    }}
    
    /* Tarjeta Recomendación Principal */
    .rec-card-main {{
        background: linear-gradient(145deg, #2D4E72 0%, #3D678F 100%);
        color: #FAF8F5;
        padding: 1.35rem 1.4rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(45, 78, 114, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }}
    
    /* Tarjetas de Alternativas */
    .rec-card-alt {{
        background-color: {COLOR_BEIGE_CARD};
        border-left: 4px solid {COLOR_SECONDARY};
        border-top: 1px solid {COLOR_BORDER};
        border-right: 1px solid {COLOR_BORDER};
        border-bottom: 1px solid {COLOR_BORDER};
        padding: 1.15rem 1.25rem;
        border-radius: 10px;
        color: {COLOR_TEXT_MAIN};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }}
    
    /* Etiquetas de fuente y datos */
    .source-tag {{
        font-size: 0.82rem;
        color: {COLOR_TEXT_MUTED};
        font-style: italic;
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
    }}
    
    /* Caja de limitaciones metodológicas */
    .limitations-box {{
        background-color: #F3ECE1;
        border-left: 4px solid #C4986C;
        border: 1px solid #E5DCCE;
        border-left-width: 4px;
        padding: 0.85rem 1.1rem;
        border-radius: 8px;
        font-size: 0.88rem;
        color: #5C4A3A;
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
    }}
    
    /* DISEÑO MEJORADO DE LAS PESTAÑAS (TABS):
       Contorno suave, cuadrado con esquinas redondeadas, mucho más visibles y grandes */
    div[data-testid="stTabs"] div[role="tablist"],
    div.stTabs div[role="tablist"],
    .stTabs [data-baseweb="tab-list"] {{
        gap: 16px !important;
        background-color: #E8E0D1 !important;
        padding: 12px 14px !important;
        border-radius: 14px !important;
        border: 1.5px solid {COLOR_BORDER} !important;
        margin-top: 1rem !important;
        margin-bottom: 2rem !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05) !important;
        display: flex !important;
        flex-wrap: wrap !important;
    }}
    
    div[data-testid="stTabs"] button[role="tab"],
    div.stTabs button[role="tab"],
    .stTabs [data-baseweb="tab"],
    .stTabs button {{
        background-color: #FAF6EE !important;
        border: 1.5px solid #D6CABA !important;
        border-radius: 10px !important;
        color: {COLOR_TEXT_MAIN} !important;
        padding: 14px 28px !important;
        height: auto !important;
        min-height: 52px !important;
        font-weight: 700 !important;
        font-size: 1.18rem !important;
        letter-spacing: -0.2px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    
    div[data-testid="stTabs"] button[role="tab"] p,
    div.stTabs button[role="tab"] p,
    .stTabs [data-baseweb="tab"] p {{
        font-size: 1.18rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    div[data-testid="stTabs"] button[role="tab"]:hover,
    div.stTabs button[role="tab"]:hover,
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: #FFFFFF !important;
        border-color: {COLOR_SECONDARY} !important;
        color: {COLOR_PRIMARY} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 12px rgba(0, 0, 0, 0.08) !important;
    }}
    
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
    div.stTabs button[role="tab"][aria-selected="true"],
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #234161 0%, #355C82 100%) !important;
        color: #FFFFFF !important;
        border: 1.5px solid #1B334D !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        box-shadow: 0 6px 16px rgba(35, 65, 97, 0.32) !important;
        transform: scale(1.02) !important;
    }}
    
    div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p,
    div.stTabs button[role="tab"][aria-selected="true"] p,
    .stTabs [aria-selected="true"] p {{
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }}
    
    /* Eliminar la línea roja/roja-rosada inferior por defecto de Streamlit */
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
        background-color: transparent !important;
    }}
    
    /* Estilo de los botones tipo píldora/filtro en la barra lateral */
    div[data-testid="stSidebar"] div.stButton > button {{
        width: 100%;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 0.88rem;
        font-weight: 500;
        border: 1px solid {COLOR_BORDER};
        background-color: #FAF8F5;
        color: {COLOR_TEXT_MAIN};
        transition: all 0.15s ease;
    }}
    
    div[data-testid="stSidebar"] div.stButton > button:hover {{
        border-color: {COLOR_SECONDARY};
        background-color: #F2ECE3;
        color: {COLOR_PRIMARY};
    }}
    
    /* Botón activo seleccionado */
    .btn-filter-active {{
        background: {COLOR_PRIMARY} !important;
        color: #FFFFFF !important;
        border: 1px solid #1E354D !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 5px rgba(43, 76, 111, 0.25) !important;
    }}
    
    /* Métricas nativas de Streamlit */
    [data-testid="stMetric"] {{
        background-color: {COLOR_BEIGE_CARD};
        border: 1px solid {COLOR_BORDER};
        border-radius: 10px;
        padding: 12px 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }}
</style>
""", unsafe_allow_html=True)

# Carga de datos con fallback entre 'data/' y './'
@st.cache_data
def load_data():
    def get_path(filename):
        if os.path.exists(os.path.join("data", filename)):
            return os.path.join("data", filename)
        elif os.path.exists(filename):
            return filename
        else:
            raise FileNotFoundError(f"No se encontró el archivo: {filename}")

    df_ranking = pd.read_csv(get_path("ranking_final_mercados_corregido.csv"))
    df_base = pd.read_csv(get_path("base_anual_paises.csv"))
    df_prov = pd.read_csv(get_path("importaciones_por_proveedor.csv"))
    df_dane = pd.read_csv(get_path("exportaciones_colombia_dane.csv"))

    # Asegurar tipos numéricos para años
    df_base["anio"] = df_base["anio"].astype(int)
    df_prov["anio"] = df_prov["anio"].astype(int)
    df_dane["anio"] = df_dane["anio"].astype(int)

    return df_ranking, df_base, df_prov, df_dane

df_ranking, df_base, df_prov, df_dane = load_data()

# ----------------- GESTIÓN DE ESTADO DE FILTROS EN SESSION_STATE -----------------
paises_disponibles = sorted(df_base["pais"].unique().tolist())
anios_disponibles = sorted(df_base["anio"].unique().tolist())

# "Todos" representa el estado general (sin filtro individual)
if "filtro_pais" not in st.session_state:
    st.session_state["filtro_pais"] = "Todos"

if "filtro_anio" not in st.session_state:
    st.session_state["filtro_anio"] = "Todos"

# Callbacks para actualizar estado de botones
def set_pais(pais):
    st.session_state["filtro_pais"] = pais

def set_anio(anio):
    st.session_state["filtro_anio"] = anio

# ----------------- BARRA LATERAL (FILTROS CON BOTONES) -----------------
st.sidebar.markdown(f"""
<div style="padding: 0.6rem 0.2rem 1rem 0.2rem; border-bottom: 1px solid {COLOR_BORDER}; margin-bottom: 1.2rem;">
    <span style="font-size: 1.3rem; font-weight: 700; color: {COLOR_PRIMARY};">Panel de Control</span><br>
    <span style="font-size: 0.85rem; color: {COLOR_TEXT_MUTED};">Filtros Interactivos por Botón</span>
</div>
""", unsafe_allow_html=True)

# Sección Filtro Países
st.sidebar.markdown(f"**Mercado / País Destino:**")
cols_p_gen = st.sidebar.columns(1)
with cols_p_gen[0]:
    es_todos_pais = (st.session_state["filtro_pais"] == "Todos")
    btn_label_pais_gen = "🔘 Ver Todos (General)" if es_todos_pais else "⚪ Ver Todos (General)"
    if st.button(btn_label_pais_gen, key="btn_pais_todos", use_container_width=True, type="primary" if es_todos_pais else "secondary"):
        set_pais("Todos")
        st.rerun()

# Botones individuales por país (en 2 columnas para limpieza visual)
for i in range(0, len(paises_disponibles), 2):
    col_a, col_b = st.sidebar.columns(2)
    p1 = paises_disponibles[i]
    with col_a:
        is_sel = (st.session_state["filtro_pais"] == p1)
        lbl = f"📍 {p1}" if is_sel else p1
        if st.button(lbl, key=f"btn_p_{p1}", use_container_width=True, type="primary" if is_sel else "secondary"):
            set_pais(p1)
            st.rerun()
    if i + 1 < len(paises_disponibles):
        p2 = paises_disponibles[i + 1]
        with col_b:
            is_sel = (st.session_state["filtro_pais"] == p2)
            lbl = f"📍 {p2}" if is_sel else p2
            if st.button(lbl, key=f"btn_p_{p2}", use_container_width=True, type="primary" if is_sel else "secondary"):
                set_pais(p2)
                st.rerun()

st.sidebar.markdown("---")

# Sección Filtro Años
st.sidebar.markdown(f"**Año de Análisis:**")
col_a_gen = st.sidebar.columns(1)
with col_a_gen[0]:
    es_todos_anio = (st.session_state["filtro_anio"] == "Todos")
    btn_label_anio_gen = "🔘 Ver Todos los Años" if es_todos_anio else "⚪ Ver Todos los Años"
    if st.button(btn_label_anio_gen, key="btn_anio_todos", use_container_width=True, type="primary" if es_todos_anio else "secondary"):
        set_anio("Todos")
        st.rerun()

# Botones individuales por año
cols_anios = st.sidebar.columns(len(anios_disponibles))
for idx, a in enumerate(anios_disponibles):
    with cols_anios[idx]:
        is_sel_a = (st.session_state["filtro_anio"] == a)
        lbl_a = f"📅 {a}" if is_sel_a else str(a)
        if st.button(lbl_a, key=f"btn_a_{a}", use_container_width=True, type="primary" if is_sel_a else "secondary"):
            set_anio(a)
            st.rerun()

st.sidebar.markdown("---")

# Botón para restablecer todos los filtros
if st.sidebar.button("🔄 Borrar Filtros (Restablecer General)", use_container_width=True):
    set_pais("Todos")
    set_anio("Todos")
    st.rerun()

# Tarjeta resumen de estado activo
st.sidebar.markdown(f"""
<div style="background-color: #F4EFE6; border-radius: 8px; padding: 12px; border: 1px solid {COLOR_BORDER}; font-size: 0.85rem; color: {COLOR_TEXT_MAIN}; line-height: 1.45; margin-top: 10px;">
    <strong>Estado Actual de Visualización:</strong><br>
    • <strong>País:</strong> <span style="color: {COLOR_PRIMARY}; font-weight: 600;">{st.session_state["filtro_pais"]}</span><br>
    • <strong>Año:</strong> <span style="color: {COLOR_PRIMARY}; font-weight: 600;">{st.session_state["filtro_anio"]}</span><br><br>
    <span style="color: {COLOR_TEXT_MUTED}; font-size: 0.78rem;">
        {
            "Mostrando datos individuales detallados." if (st.session_state["filtro_pais"] != "Todos" or st.session_state["filtro_anio"] != "Todos")
            else "Mostrando el consolidado general / total de todos los mercados y años."
        }
    </span>
</div>
""", unsafe_allow_html=True)

# Determinar listas activas para filtrar
if st.session_state["filtro_pais"] == "Todos":
    active_paises = paises_disponibles
else:
    active_paises = [st.session_state["filtro_pais"]]

if st.session_state["filtro_anio"] == "Todos":
    active_anios = anios_disponibles
else:
    active_anios = [int(st.session_state["filtro_anio"])]

# Filtrar dataframes según selección activa
df_base_filtered = df_base[(df_base["pais"].isin(active_paises)) & (df_base["anio"].isin(active_anios))].copy()
df_prov_filtered = df_prov[(df_prov["pais"].isin(active_paises)) & (df_prov["anio"].isin(active_anios))].copy()
df_dane_filtered = df_dane[df_dane["anio"].isin(active_anios)].copy()
df_ranking_filtered = df_ranking[df_ranking["Pais_Importador"].isin(active_paises)].copy()

# ----------------- ENCABEZADO Y RECOMENDACIÓN ESTRATÉGICA -----------------
st.markdown('''
<div class="header-container">
    <div class="main-title">Estrategia de Expansión Internacional: Cerámica Corona</div>
    <div class="sub-title">Evaluación multicriterio para la exportación de baldosas cerámicas (HS 690722) hacia Centroamérica y el Caribe</div>
</div>
''', unsafe_allow_html=True)

# Cálculo dinámico de mercados recomendados (desde CSV original)
ranking_sorted_base = df_ranking.sort_values(by="Puntaje_Base", ascending=False).reset_index(drop=True)
top1_pais = ranking_sorted_base.iloc[0]["Pais_Importador"]
top1_score = ranking_sorted_base.iloc[0]["Puntaje_Base"]
top2_pais = ranking_sorted_base.iloc[1]["Pais_Importador"]
top2_score = ranking_sorted_base.iloc[1]["Puntaje_Base"]
top3_pais = ranking_sorted_base.iloc[2]["Pais_Importador"]
top3_score = ranking_sorted_base.iloc[2]["Puntaje_Base"]

col_rec1, col_rec2, col_rec3 = st.columns([1.3, 1, 1])

with col_rec1:
    st.markdown(f"""
    <div class="rec-card-main">
        <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85;">🎯 Mercado Prioritario Recomendado</div>
        <div style="font-size: 1.85rem; font-weight: 700; margin-top: 0.2rem; color: #FFFFFF;">{top1_pais}</div>
        <div style="font-size: 1.12rem; font-weight: 600; margin-top: 0.25rem; color: #D5E4EF;">Puntaje Base: {top1_score:,.2f} / 100</div>
        <div style="font-size: 0.84rem; margin-top: 0.55rem; opacity: 0.92; line-height: 1.35; color: #E8F0F6;">
            Líder en estabilidad de demanda, menor concentración de competidores y mayor cuota histórica consolidada de Colombia (9.1 %).
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_rec2:
    st.markdown(f"""
    <div class="rec-card-alt">
        <div style="font-size: 0.82rem; font-weight: 700; color: {COLOR_SECONDARY}; text-transform: uppercase; letter-spacing: 0.5px;">Alternativa 1 (Expansión)</div>
        <div style="font-size: 1.45rem; font-weight: 700; color: {COLOR_PRIMARY}; margin-top: 0.2rem;">{top2_pais}</div>
        <div style="font-size: 1.05rem; font-weight: 600; color: {COLOR_MUTED_BLUE}; margin-top: 0.2rem;">Puntaje Base: {top2_score:,.2f} / 100</div>
        <div style="font-size: 0.82rem; color: {COLOR_TEXT_MUTED}; margin-top: 0.4rem; line-height: 1.3;">
            Gran dinamismo y crecimiento de importaciones. Presencia colombiana en ascenso del 3.3 % al 8.9 %.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_rec3:
    st.markdown(f"""
    <div class="rec-card-alt">
        <div style="font-size: 0.82rem; font-weight: 700; color: {COLOR_SECONDARY}; text-transform: uppercase; letter-spacing: 0.5px;">Alternativa 2 (Hub Logístico)</div>
        <div style="font-size: 1.45rem; font-weight: 700; color: {COLOR_PRIMARY}; margin-top: 0.2rem;">{top3_pais}</div>
        <div style="font-size: 1.05rem; font-weight: 600; color: {COLOR_MUTED_BLUE}; margin-top: 0.2rem;">Puntaje Base: {top3_score:,.2f} / 100</div>
        <div style="font-size: 0.82rem; color: {COLOR_TEXT_MUTED}; margin-top: 0.4rem; line-height: 1.3;">
            Mercado vecino de alta cercanía logística y participación colombiana moderada (~4.8 %).
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="limitations-box">
    <strong>📌 Nota Metodológica y Limitaciones del Análisis:</strong>
    La subpartida arancelaria <strong>HS 690722</strong> comprende <em>baldosas y losas de cerámica para pavimentación o revestimiento con un coeficiente de absorción de agua superior a 0,5 % y hasta 10 % en peso</em>. Esta subpartida agrupa múltiples tipologías, formatos, acabados y marcas comerciales a nivel mundial, y no corresponde exclusivamente a la línea de baldosas de piso de Corona.
</div>
""", unsafe_allow_html=True)

# ----------------- TABS PRINCIPALES (SECCIONES ESTILIZADAS) -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Comparación de Mercados",
    "🏆 Ranking e Indicadores",
    "🎛️ Sensibilidad",
    "🚢 Proveedores",
    "🇨🇴 Contexto Colombia"
])

# ==============================================================================
# PESTAÑA 1: COMPARACIÓN DE MERCADOS
# ==============================================================================
with tab1:
    st.subheader("Dinámica y Comparativa del Mercado Importador")
    
    # Mensaje contextual si hay filtro individual activo
    if st.session_state["filtro_pais"] != "Todos" or st.session_state["filtro_anio"] != "Todos":
        st.info(f"🔎 Vista Individual Filtrada: País **{st.session_state['filtro_pais']}** | Año **{st.session_state['filtro_anio']}**.")
    else:
        st.markdown("Consolidado general de importaciones totales y la posición relativa de Colombia en todos los mercados evaluados.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Importaciones Totales por País y Año")
        fig_bar_imp = px.bar(
            df_base_filtered,
            x="pais",
            y="importaciones_usd",
            color="anio",
            barmode="group",
            text_auto=".2s",
            labels={
                "pais": "País Importador",
                "importaciones_usd": "Importaciones Totales (USD)",
                "anio": "Año"
            },
            color_discrete_sequence=["#7B9EA8", "#4A7C9B", "#2B4C6F"]
        )
        fig_bar_imp.update_layout(
            xaxis_title="País",
            yaxis_title="USD Corrientes",
            yaxis=dict(tickformat="$,.0f"),
            legend_title="Año"
        )
        estilo_figura(fig_bar_imp)
        st.plotly_chart(fig_bar_imp, use_container_width=True)
        st.markdown('<div class="source-tag">Fuente: UN Comtrade, importaciones reportadas por cada país, USD corrientes.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("#### Tendencia Temporal de Importaciones")
        df_base_filtered_sorted = df_base_filtered.sort_values(by=["pais", "anio"])
        fig_line_imp = px.line(
            df_base_filtered_sorted,
            x="anio",
            y="importaciones_usd",
            color="pais",
            markers=True,
            labels={
                "anio": "Año",
                "importaciones_usd": "Importaciones Totales (USD)",
                "pais": "País"
            },
            color_discrete_sequence=["#2B4C6F", "#4A7C9B", "#7B9EA8", "#C77D58", "#93A891"]
        )
        fig_line_imp.update_layout(
            xaxis=dict(tickmode="linear", dtick=1),
            yaxis_title="USD Corrientes",
            yaxis=dict(tickformat="$,.0f")
        )
        estilo_figura(fig_line_imp)
        st.plotly_chart(fig_line_imp, use_container_width=True)
        st.markdown('<div class="source-tag">Fuente: UN Comtrade, importaciones reportadas por cada país, USD corrientes.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Participación de Mercado de Colombia (%)")
    
    # Crear columna con porcentaje formateado para visualización
    df_base_filtered_plot = df_base_filtered.copy()
    df_base_filtered_plot["participacion_colombia_pct"] = df_base_filtered_plot["participacion_colombia"] * 100

    fig_share_col = px.bar(
        df_base_filtered_plot,
        x="pais",
        y="participacion_colombia_pct",
        color="anio",
        barmode="group",
        text=df_base_filtered_plot["participacion_colombia_pct"].apply(lambda x: f"{x:.2f}%"),
        labels={
            "pais": "País Importador",
            "participacion_colombia_pct": "Participación de Colombia (%)",
            "anio": "Año"
        },
        color_discrete_sequence=["#9EBECB", "#5C89A6", "#32577D"]
    )
    fig_share_col.update_layout(
        xaxis_title="País Importador",
        yaxis_title="Participación de Colombia (%)",
        yaxis=dict(ticksuffix="%"),
        legend_title="Año"
    )
    estilo_figura(fig_share_col)
    st.plotly_chart(fig_share_col, use_container_width=True)
    st.markdown('<div class="source-tag">Fuente: Cálculos propios con base en UN Comtrade, porcentaje sobre el valor importado total (USD corrientes).</div>', unsafe_allow_html=True)

    # Tabla resumen de datos de mercado
    st.markdown("##### Resumen de Indicadores por País y Año")
    df_table_mercado = df_base_filtered.copy()
    df_table_mercado = df_table_mercado.rename(columns={
        "pais": "País",
        "anio": "Año",
        "importaciones_usd": "Importaciones Totales (USD)",
        "peso_kg": "Volumen (kg)",
        "valor_colombia_usd": "Exportado por Colombia (USD)",
        "participacion_colombia": "Participación Colombia",
        "hhi": "HHI Concentración",
        "n_proveedores": "N° Proveedores"
    })
    
    st.dataframe(
        df_table_mercado.style.format({
            "Importaciones Totales (USD)": "${:,.2f}",
            "Volumen (kg)": lambda v: f"{v:,.0f} kg" if pd.notnull(v) else "N/D",
            "Exportado por Colombia (USD)": "${:,.2f}",
            "Participación Colombia": "{:.2%}",
            "HHI Concentración": "{:,.1f}",
            "N° Proveedores": "{:.0f}"
        }),
        use_container_width=True
    )
    st.markdown('<div class="source-tag">Fuente: UN Comtrade, datos anuales reportados por cada mercado para la subpartida HS 690722.</div>', unsafe_allow_html=True)


# ==============================================================================
# PESTAÑA 2: RANKING E INDICADORES
# ==============================================================================
with tab2:
    st.subheader("Evaluación Multicriterio y Descomposición del Ranking")
    st.markdown("Puntaje ponderado obtenido a partir de los 5 pilares estratégicos de evaluación (ponderación base: Tamaño 25 %, Crecimiento 25 %, Estabilidad 15 %, Concentración 15 %, Presencia Colombia 20 %).")

    # Tabla de ranking e indicadores
    st.markdown("#### Tabla de Desempeño por País")
    df_ranking_display = df_ranking_filtered[[
        "Pais_Importador", "Tamaño_Promedio_USD", "Crecimiento_CAGR", "Estabilidad_CV", 
        "Concentracion_HHI_2024", "Participacion_Colombia_Prom", "Puntaje_Base"
    ]].sort_values(by="Puntaje_Base", ascending=False).reset_index(drop=True)

    df_ranking_display.columns = [
        "País", "Tamaño Prom. (USD)", "Crecimiento (CAGR)", "Estabilidad (CV)", 
        "HHI (2024)", "Part. Colombia Prom.", "Puntaje Base"
    ]

    st.dataframe(
        df_ranking_display.style.format({
            "Tamaño Prom. (USD)": "${:,.2f}",
            "Crecimiento (CAGR)": "{:.2%}",
            "Estabilidad (CV)": "{:.3f}",
            "HHI (2024)": "{:,.1f}",
            "Part. Colombia Prom.": "{:.2%}",
            "Puntaje Base": "{:,.2f} pts"
        }),
        use_container_width=True
    )
    st.markdown('<div class="source-tag">Fuente: Elaboración propia a partir de UN Comtrade (período 2022-2024). Puntajes normalizados de 0 a 100.</div>', unsafe_allow_html=True)

    # Gráfico de barras apiladas: cuánto aporta cada indicador al puntaje
    st.markdown("#### Contribución de Cada Indicador al Puntaje Base")
    
    # Pesos escenario base
    w_tam, w_crec, w_estab, w_conc, w_part = 0.25, 0.25, 0.15, 0.15, 0.20

    df_contrib = df_ranking_filtered.copy()
    df_contrib["Aporte_Tamaño"] = df_contrib["Tamaño"] * w_tam
    df_contrib["Aporte_Crecimiento"] = df_contrib["Crecimiento"] * w_crec
    df_contrib["Aporte_Estabilidad"] = df_contrib["Estabilidad"] * w_estab
    df_contrib["Aporte_Concentracion"] = df_contrib["Concentracion"] * w_conc
    df_contrib["Aporte_Participacion_Col"] = df_contrib["Participacion_Col"] * w_part

    df_contrib = df_contrib.sort_values(by="Puntaje_Base", ascending=True)

    fig_stack = go.Figure()
    fig_stack.add_trace(go.Bar(
        y=df_contrib["Pais_Importador"],
        x=df_contrib["Aporte_Tamaño"],
        name="Tamaño de Mercado (25 %)",
        orientation="h",
        marker=dict(color="#4A7C9B")
    ))
    fig_stack.add_trace(go.Bar(
        y=df_contrib["Pais_Importador"],
        x=df_contrib["Aporte_Crecimiento"],
        name="Crecimiento / CAGR (25 %)",
        orientation="h",
        marker=dict(color="#7B9EA8")
    ))
    fig_stack.add_trace(go.Bar(
        y=df_contrib["Pais_Importador"],
        x=df_contrib["Aporte_Estabilidad"],
        name="Estabilidad / Menor CV (15 %)",
        orientation="h",
        marker=dict(color="#D4A373")
    ))
    fig_stack.add_trace(go.Bar(
        y=df_contrib["Pais_Importador"],
        x=df_contrib["Aporte_Concentracion"],
        name="Apertura / Menor HHI (15 %)",
        orientation="h",
        marker=dict(color="#93A891")
    ))
    fig_stack.add_trace(go.Bar(
        y=df_contrib["Pais_Importador"],
        x=df_contrib["Aporte_Participacion_Col"],
        name="Participación Colombia (20 %)",
        orientation="h",
        marker=dict(color="#C77D58")
    ))

    fig_stack.update_layout(
        barmode="stack",
        xaxis_title="Puntaje Ponderado (Total sobre 100 puntos)",
        yaxis_title="Mercado",
        legend_title="Pilar Evaluado (Ponderación)"
    )
    estilo_figura(fig_stack)
    st.plotly_chart(fig_stack, use_container_width=True)
    st.markdown('<div class="source-tag">Fuente: Modelo multicriterio de evaluación. Aporte = Indicador normalizado (0-100) × Peso del pilar.</div>', unsafe_allow_html=True)

    # Explicación de los indicadores y su dirección de optimización
    st.markdown("---")
    st.markdown("#### Guía Metodológica de Indicadores")

    col_ind1, col_ind2 = st.columns(2)
    with col_ind1:
        st.markdown(f"""
        <div style="background-color: #F3ECE1; padding: 14px; border-radius: 8px; border: 1px solid {COLOR_BORDER}; line-height: 1.45;">
            <strong>1. Tamaño de Mercado (USD)</strong>: Promedio de importaciones anuales 2022-2024.<br>
            • <em>Criterio:</em> <strong>Más es mejor (↑)</strong>. Mercados de mayor volumen absorben mayor escala de despacho.<br><br>
            <strong>2. Crecimiento (CAGR)</strong>: Tasa de crecimiento anual compuesta de importaciones entre 2022 y 2024.<br>
            • <em>Criterio:</em> <strong>Más es mejor (↑)</strong>. Prioriza destinos en fase expansiva o con menor contracción sectorial.<br><br>
            <strong>3. Estabilidad (Coeficiente de Variación - CV)</strong>: Desviación estándar dividida entre la media.<br>
            • <em>Criterio:</em> <strong>Menor es mejor (↓)</strong> <em>(menor CV recibe 100 pts)</em>. Garantiza previsibilidad y menor volatilidad comercial.
        </div>
        """, unsafe_allow_html=True)
    with col_ind2:
        st.markdown(f"""
        <div style="background-color: #F3ECE1; padding: 14px; border-radius: 8px; border: 1px solid {COLOR_BORDER}; line-height: 1.45;">
            <strong>4. Concentración (Índice HHI 2024)</strong>: Herfindahl-Hirschman Index de los proveedores en 2024.<br>
            • <em>Criterio:</em> <strong>Menor es mejor (↓)</strong> <em>(menor HHI recibe 100 pts)</em>. Un HHI bajo refleja un mercado abierto con competencia atomizada y menores barreras oligopólicas.<br><br>
            <strong>5. Participación de Colombia (%)</strong>: Cuota promedio de las compras que provienen de Colombia.<br>
            • <em>Criterio:</em> <strong>Más es mejor (↑)</strong>. Refleja reconocimiento de marca, aceptación del estándar técnico y canales de distribución activos para Corona.
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# PESTAÑA 3: SENSIBILIDAD
# ==============================================================================
with tab3:
    st.subheader("Análisis de Sensibilidad y Simulación en Vivo")
    st.markdown("Ajuste los pesos de cada pilar estratégico mediante los controles deslizantes para recalcular el ranking en tiempo real.")

    # Controles deslizantes interactivos
    st.markdown("##### Calibración de Pesos Estratégicos")
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)

    with col_s1:
        peso_tam = st.slider("Tamaño (%)", min_value=0, max_value=100, value=25, step=5)
    with col_s2:
        peso_crec = st.slider("Crecimiento (%)", min_value=0, max_value=100, value=25, step=5)
    with col_s3:
        peso_estab = st.slider("Estabilidad (%)", min_value=0, max_value=100, value=15, step=5)
    with col_s4:
        peso_conc = st.slider("Apertura/Conc. (%)", min_value=0, max_value=100, value=15, step=5)
    with col_s5:
        peso_col = st.slider("Part. Colombia (%)", min_value=0, max_value=100, value=20, step=5)

    suma_pesos = peso_tam + peso_crec + peso_estab + peso_conc + peso_col

    if suma_pesos == 100:
        st.markdown(f'<div style="color: #2F6F4E; font-size: 0.9rem; margin-bottom: 12px;">✅ Suma de ponderaciones balanceada al <strong>{suma_pesos} %</strong>.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color: #9E5A2A; font-size: 0.9rem; margin-bottom: 12px;">⚠️ La suma de las ponderaciones es <strong>{suma_pesos} %</strong> (debe sumar 100 %). El ranking normaliza proporcionalmente los pesos.</div>', unsafe_allow_html=True)

    # Factor de normalización de pesos
    norm_factor = (suma_pesos / 100.0) if suma_pesos > 0 else 1.0
    w_tam_live = (peso_tam / 100.0) / norm_factor if suma_pesos > 0 else 0.2
    w_crec_live = (peso_crec / 100.0) / norm_factor if suma_pesos > 0 else 0.2
    w_estab_live = (peso_estab / 100.0) / norm_factor if suma_pesos > 0 else 0.2
    w_conc_live = (peso_conc / 100.0) / norm_factor if suma_pesos > 0 else 0.2
    w_col_live = (peso_col / 100.0) / norm_factor if suma_pesos > 0 else 0.2

    # Recalcular puntaje dinámico en vivo
    df_sens = df_ranking_filtered.copy()
    df_sens["Puntaje_Simulado"] = (
        df_sens["Tamaño"] * w_tam_live +
        df_sens["Crecimiento"] * w_crec_live +
        df_sens["Estabilidad"] * w_estab_live +
        df_sens["Concentracion"] * w_conc_live +
        df_sens["Participacion_Col"] * w_col_live
    )
    df_sens = df_sens.sort_values(by="Puntaje_Simulado", ascending=False).reset_index(drop=True)

    # Ranking en vivo
    col_live1, col_live2 = st.columns([1.2, 1])

    with col_live1:
        st.markdown("#### Ranking Recalculado en Vivo")
        fig_live = px.bar(
            df_sens,
            x="Pais_Importador",
            y="Puntaje_Simulado",
            text=df_sens["Puntaje_Simulado"].apply(lambda x: f"{x:.2f} pts"),
            color="Puntaje_Simulado",
            color_continuous_scale=[[0, "#BDD2DE"], [0.5, "#7B9EA8"], [1, "#2B4C6F"]],
            labels={"Pais_Importador": "País", "Puntaje_Simulado": "Puntaje Simulado"}
        )
        fig_live.update_layout(
            yaxis=dict(range=[0, 100])
        )
        estilo_figura(fig_live)
        st.plotly_chart(fig_live, use_container_width=True)

    with col_live2:
        st.markdown("#### Tabla de Posiciones Simuladas")
        st.dataframe(
            df_sens[["Pais_Importador", "Puntaje_Simulado", "Puntaje_Base"]].rename(columns={
                "Pais_Importador": "País",
                "Puntaje_Simulado": "Puntaje Simulado",
                "Puntaje_Base": "Puntaje Base Original"
            }).style.format({
                "Puntaje Simulado": "{:,.2f} pts",
                "Puntaje Base Original": "{:,.2f} pts"
            }),
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("#### Escenarios Estratégicos Predefinidos en el Estudio")
    st.markdown("Comparativa fija de los países líderes en cada escenario modelado en el dataset de decisión:")

    escenarios_info = [
        {"Escenario": "Escenario Base", "Ponderación Clave": "Equilibrio (25 % Tamaño, 25 % Crecimiento, 15 % Estabilidad, 15 % Concentración, 20 % Colombia)", "Columna": "Puntaje_Base"},
        {"Escenario": "Escenario Prudente", "Ponderación Clave": "Mitigación de riesgo (35 % Estabilidad, 25 % Concentración baja, 20 % Tamaño, 10 % Crecimiento, 10 % Colombia)", "Columna": "Puntaje_Prudente"},
        {"Escenario": "Escenario Agresivo", "Ponderación Clave": "Crecimiento rápido (45 % Crecimiento, 25 % Tamaño, 20 % Colombia, 5 % Estabilidad, 5 % Concentración)", "Columna": "Puntaje_Agresivo"},
        {"Escenario": "Escenario Foco Colombia", "Ponderación Clave": "Apalancamiento de canal (50 % Presencia Colombia, 15 % Tamaño, 15 % Crecimiento, 10 % Estabilidad, 10 % Concentración)", "Columna": "Puntaje_Foco Colombia"}
    ]

    tabla_escenarios = []
    for esc in escenarios_info:
        top_row = df_ranking.sort_values(by=esc["Columna"], ascending=False).iloc[0]
        tabla_escenarios.append({
            "Escenario Estratégico": esc["Escenario"],
            "Criterio de Ponderación": esc["Ponderación Clave"],
            "País Primer Lugar (Líder)": top_row["Pais_Importador"],
            "Puntaje Ganador": f"{top_row[esc['Columna']]:,.2f} pts"
        })

    df_escenarios_fija = pd.DataFrame(tabla_escenarios)
    st.dataframe(df_escenarios_fija, use_container_width=True, hide_index=True)
    st.markdown('<div class="source-tag">Fuente: ranking_final_mercados_corregido.csv, cálculo fijo de líderes por escenario multicriterio.</div>', unsafe_allow_html=True)


# ==============================================================================
# PESTAÑA 4: PROVEEDORES
# ==============================================================================
with tab4:
    st.subheader("Análisis de Competencia y Estructura de Proveedores")
    st.markdown("Identificación de los principales competidores internacionales y nivel de concentración de mercado (HHI).")

    # Si hay un país o año individual seleccionado en la barra lateral, se toma como predeterminado
    default_p_idx = active_paises.index(st.session_state["filtro_pais"]) if (st.session_state["filtro_pais"] in active_paises) else 0
    default_a_idx = active_anios.index(int(st.session_state["filtro_anio"])) if (st.session_state["filtro_anio"] != "Todos" and int(st.session_state["filtro_anio"]) in active_anios) else (len(active_anios) - 1)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        pais_prov_sel = st.selectbox(
            "Seleccione el País de Destino a Consultar:",
            options=active_paises,
            index=default_p_idx
        )
    with col_p2:
        anio_prov_sel = st.selectbox(
            "Seleccione el Año a Consultar:",
            options=active_anios,
            index=default_a_idx
        )

    # Filtrar datos de proveedores para el país y año
    df_prov_slice = df_prov[(df_prov["pais"] == pais_prov_sel) & (df_prov["anio"] == anio_prov_sel)].copy()

    # Obtener HHI reportado para ese mercado y año
    hhi_row = df_base[(df_base["pais"] == pais_prov_sel) & (df_base["anio"] == anio_prov_sel)]
    hhi_val = hhi_row["hhi"].values[0] if len(hhi_row) > 0 else None
    n_prov_val = hhi_row["n_proveedores"].values[0] if len(hhi_row) > 0 else len(df_prov_slice)

    # Métricas clave en tarjetas
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        tot_importado = df_prov_slice["valor_usd"].sum() if len(df_prov_slice) > 0 else 0
        st.metric(
            label=f"Total Importado por {pais_prov_sel} ({anio_prov_sel})",
            value=f"${tot_importado:,.0f} USD"
        )
    with col_m2:
        if hhi_val is not None:
            clasif_hhi = "Moderado (1500-2500)" if 1500 <= hhi_val <= 2500 else ("Altamente Concentrado (>2500)" if hhi_val > 2500 else "Baja Concentración (<1500)")
            st.metric(
                label=f"Índice HHI ({anio_prov_sel})",
                value=f"{hhi_val:,.1f}",
                delta=clasif_hhi,
                delta_color="off"
            )
        else:
            st.metric(label="Índice HHI", value="N/D")
    with col_m3:
        st.metric(
            label="Número de Países Proveedores",
            value=f"{int(n_prov_val) if pd.notnull(n_prov_val) else len(df_prov_slice)}"
        )

    if len(df_prov_slice) == 0:
        st.warning(f"No hay registros de proveedores para {pais_prov_sel} en el año {anio_prov_sel}.")
    else:
        # Calcular participación porcentual
        df_prov_slice["participacion"] = (df_prov_slice["valor_usd"] / tot_importado) * 100
        df_top10 = df_prov_slice.sort_values(by="valor_usd", ascending=False).head(10).copy()

        # Resaltar Colombia con terracota suave sofisticado
        df_top10["Es_Colombia"] = df_top10["socio"].apply(lambda s: "Colombia (Corona)" if s == "Colombia" else "Otros Proveedores")

        fig_prov = px.bar(
            df_top10,
            x="participacion",
            y="socio",
            orientation="h",
            text=df_top10["participacion"].apply(lambda p: f"{p:.2f}%"),
            color="Es_Colombia",
            color_discrete_map={"Colombia (Corona)": "#C77D58", "Otros Proveedores": "#4A7C9B"},
            labels={
                "participacion": "Participación de Mercado (%)",
                "socio": "País Proveedor (Socio)",
                "Es_Colombia": "Origen"
            }
        )
        fig_prov.update_layout(
            yaxis=dict(autorange="reversed"),
            xaxis_title="Participación sobre el Total Importado (%)",
            xaxis=dict(ticksuffix="%")
        )
        estilo_figura(fig_prov, height=410)
        st.plotly_chart(fig_prov, use_container_width=True)
        st.markdown(f'<div class="source-tag">Fuente: UN Comtrade, importaciones reportadas por {pais_prov_sel} desglosadas por socio comercial en {anio_prov_sel}, USD corrientes.</div>', unsafe_allow_html=True)

        st.markdown(f"##### Detalle de los 10 Principales Proveedores en {pais_prov_sel} ({anio_prov_sel})")
        st.dataframe(
            df_top10[["socio", "valor_usd", "peso_kg", "participacion"]].rename(columns={
                "socio": "País Proveedor",
                "valor_usd": "Valor Importado (USD)",
                "peso_kg": "Peso Neto (kg)",
                "participacion": "Participación (%)"
            }).style.format({
                "Valor Importado (USD)": "${:,.2f}",
                "Peso Neto (kg)": lambda k: f"{k:,.0f} kg" if pd.notnull(k) else "N/D",
                "Participación (%)": "{:.2f}%"
            }),
            use_container_width=True
        )


# ==============================================================================
# PESTAÑA 5: CONTEXTO COLOMBIA
# ==============================================================================
with tab5:
    st.subheader("Contexto Macroeconómico de Colombia")
    st.markdown("Evolución de las exportaciones totales de bienes de Colombia registradas oficialmente por el DANE.")

    col_d1, col_d2 = st.columns([1.3, 1])

    with col_d1:
        st.markdown("#### Exportaciones Totales de Colombia (Millones de USD)")
        fig_dane = px.bar(
            df_dane_filtered,
            x="anio",
            y="exp_colombia_musd",
            text=df_dane_filtered["exp_colombia_musd"].apply(lambda v: f"${v:,.1f} M"),
            labels={
                "anio": "Año",
                "exp_colombia_musd": "Exportaciones Totales (Millones USD FOB)"
            },
            color_discrete_sequence=["#4A7C9B"]
        )
        fig_dane.update_layout(
            xaxis=dict(tickmode="linear", dtick=1),
            yaxis_title="Millones de USD FOB",
            yaxis=dict(tickformat="$,.0f")
        )
        estilo_figura(fig_dane)
        st.plotly_chart(fig_dane, use_container_width=True)
        st.markdown('<div class="source-tag">Fuente: DANE-DIAN, millones de USD FOB corrientes.</div>', unsafe_allow_html=True)

    with col_d2:
        st.markdown("#### Registro Histórico DANE")
        st.dataframe(
            df_dane_filtered.rename(columns={
                "anio": "Año",
                "exp_colombia_musd": "Exportaciones Colombia (MUSD FOB)"
            }).style.format({
                "Año": "{:.0f}",
                "Exportaciones Colombia (MUSD FOB)": "${:,.2f} MUSD"
            }),
            use_container_width=True,
            hide_index=True
        )
        st.markdown('<div class="source-tag">Fuente: DANE-DIAN, cifras agregadas de comercio exterior.</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background-color: #F1ECE3; border-radius: 8px; padding: 14px; border: 1px solid {COLOR_BORDER}; font-size: 0.88rem; color: {COLOR_TEXT_MAIN}; line-height: 1.45; margin-top: 10px;">
            💡 <strong>Contexto del sector manufacturero y exportador:</strong><br>
            El comportamiento general de las exportaciones de Colombia muestra la normalización posterior al pico de comercio exterior de 2022. 
            En este entorno, la diversificación hacia mercados centroamericanos con tratados comerciales vigentes y alta receptividad de producto colombiano (como Costa Rica y Guatemala) ofrece estabilidad al flujo de divisas de Corona.
        </div>
        """, unsafe_allow_html=True)

# Pie de página ejecutivo
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: {COLOR_TEXT_MUTED}; font-size: 0.82rem; padding: 1rem 0;">
    <strong>Corona Cerámica S.A.S. — Sistema de Apoyo a la Decisión de Internacionalización</strong><br>
    Subpartida Arancelaria HS 690722 | Mercados: Costa Rica, República Dominicana, Guatemala, Honduras, Panamá.<br>
    Fuentes oficiales: UN Comtrade & DANE-DIAN (2022-2024).
</div>
""", unsafe_allow_html=True)
