import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Love Algorithm v3.0",
    layout="wide",
    page_icon="❤️"
)

TITLE = "LOVE ALGORITHM v3.0"

st.markdown("""
<style>
 .stMetric {
  background-color: #1E1E1E;
  padding: 15px;
  border-radius: 8px;
  border-left: 5px solid #FF4B4B;
 }
 h1, h2, h3 {
  font-family: Helvetica Neue, sans-serif;
 }
</style>
""", unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1
if "data" not in st.session_state:
    st.session_state.data = {"user": {}, "candidate": {}, "missions": {}}

def calculate_deep_metrics(data):
    u = data["user"]
    c = data["candidate"]
    m = data["missions"]
    
    base_score = 50
    log = []
    
    evo_score = 0
    if u.get("goal") == "Familia e Hijos":
        if 20 <= c.get("age", 0) <= 32:
            evo_score = 20
            log.append("✅ Ventana Fértil Óptima: La edad 20-32 maximiza probabilidad de embarazo saludable.")
        elif 33 <= c.get("age", 0) <= 37:
            evo_score = 10
            log.append("⚠️ Ventana Fértil Media: Edad 32 implica urgencia biológica moderada.")
        else:
            evo_score = -10
            log.append("❌ Riesgo Obstétrico: Edad fuera de rango óptimo para familia numerosa.")
    
    gottman_score = 0
    if m.get("testno") == "Aceptacin tranquila":
        gottman_score = 25
        log.append("✅ Bajo Conflicto: Aceptar un No indica seguridad emocional y ausencia de rasgos controladores.")
    elif m.get("testno") == "Molestia visible":
        gottman_score = -15
        log.append("⚠️ Alerta de Neuroticismo: La molestia ante límites sugiere baja tolerancia a la frustración.")
    else:
        gottman_score = -40
        log.append("❌ RED FLAG Narcisismo: La manipulación/venganza ante un límite es predictor #1 de abuso emocional.")
    
    cog_score = 0
    if m.get("testmono") == "Pregunt con inters":
        cog_score = 25
        log.append("✅ Compatibilidad Intelectual: Interés activo (Active Constructive Responding) predice longevidad.")
    elif m.get("testmono") == "Escuch pasivamente":
        cog_score = 5
        log.append("⚠️ Riesgo de Aburrimiento: Escucha pasiva es aceptable, pero tú necesitas estimulación intelectual.")
    else:
        cog_score = -30
        log.append("❌ Desprecio Intelectual: Ignorar tu pasión es un Jinete del Apocalipsis (Gottman).")
    
    mat_score = 0
    if len(m.get("testex", "")) >= 10 and ("culpa" not in m.get("testex", "").lower() or "mi error" in m.get("testex", "").lower()):
        mat_score = 15
        log.append("✅ Locus de Control Interno: Asumir errores propios indica madurez psicológica para resolver conflictos.")
    else:
        mat_score = -20
        log.append("❌ Victimización: No articular autocrítica sugiere inmadurez emocional.")
    
    final_score = base_score + evo_score + gottman_score + cog_score + mat_score
    final_score = max(0, min(100, final_score))
    
    return {
        "total": final_score,
        "breakdown": {
            "Biología/Evolutiva": evo_score,
            "Dinámica de Conflicto (Gottman)": gottman_score,
            "Intelecto/Openness": cog_score,
            "Madurez Emocional": mat_score,
        },
        "reasons": log
    }

def render_dashboard(results):
    st.divider()
    st.markdown("## Dashboard Analítico de Viabilidad Relacional")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("### Índice de Éxito (5 Años)")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=results["total"],
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "white"},
                "steps": [
                    {"range": [0, 40], "color": "#FF4B4B"},
                    {"range": [40, 70], "color": "#FFA500"},
                    {"range": [70, 100], "color": "#00CC96"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 4},
                    "thickness": 0.75,
                    "value": 70
                }
            }
        ))
        fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.markdown("### Desglose de Impacto por Dimensión")
        df_breakdown = pd.DataFrame(list(results["breakdown"].items()), columns=["Dimensión", "Puntos"])
        fig_bar = px.bar(df_breakdown, x="Puntos", y="Dimensión", orientation="h", 
                         color="Puntos", color_continuous_scale="RdYlGn", text="Puntos")
        fig_bar.update_layout(height=300)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col3:
        st.markdown("### Datos del Sujeto")
        st.metric("Índice Final", f"{results['total']:.1f}/100")
        st.metric("Probabilidad de Éxito", f"{(results['total']/100)*100:.1f}%")
        odds = (results['total']/100) / (1 - results['total']/100) if results['total'] not in (0, 100) else None
        if odds:
            st.metric("Odds (éxito:fracaso)", f"{odds:.2f}:1")
    
    st.subheader("✅ Interpretación Detallada de Factores")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Fortalezas Detectadas**")
        strengths = [r for r in results["reasons"] if "✅" in r]
        if strengths:
            for reason in strengths:
                st.info(reason)
        else:
            st.info("No se detectaron fortalezas significativas.")
    with c2:
        st.markdown("**Riesgos y Amenazas**")
        risks = [r for r in results["reasons"] if "❌" in r or "⚠️" in r]
        if risks:
            for reason in risks:
                st.error(reason)
        else:
            st.success("No se detectaron riesgos críticos.")

def render_scientific_tab(results):
    st.title("✨ Análisis Científico de Compatibilidad")
    
    score = results["total"]
    prob = score / 100.0
    odds = prob / (1 - prob) if prob not in (0, 1) else None
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score Total (0-100)", f"{score:.1f}")
    with col2:
        st.metric("Probabilidad de Éxito (5 Años)", f"{prob*100:.1f}%")
    with col3:
        if odds is not None:
            st.metric("Odds (éxito:fracaso)", f"{odds:.2f}:1")
        else:
            st.metric("Odds", "No definidas")
    
    st.markdown("### Desglose Matemático Aproximado")
    df_break = pd.DataFrame([
        {"Dimensión": k,
         "Puntos": v,
         "Peso_relativo_%": (v / score * 100) if score != 0 else 0}
        for k, v in results["breakdown"].items()
    ])
    st.dataframe(df_break, use_container_width=True)
    
    st.markdown("""
    **Interpretación Fría y Científica:**
    - El score total se interpreta como una probabilidad estimada de éxito relacional bajo el modelo actual.
    - Cada dimensión aporta un porcentaje aproximado al resultado final.
    - Las dimensiones con mayor peso son: Dinámica de Conflicto (Gottman) y Fertilidad/Edad.
    - Un score > 70 indica relación con alta probabilidad de estabilidad.
    - Un score entre 40-70 sugiere incompatibilidades manejables pero riesgosas.
    - Un score < 40 indica problemas estructurales serios.
    """)

def render_graphics_tab(results):
    st.title("📈 Laboratorio de Gráficos Interactivos")
    
    st.markdown("Juega con las variables para ver cómo cambia la probabilidad estimada de éxito.")
    
    base_data = st.session_state.data
    
    st.subheader("Efecto de la Edad de la Candidata en el Score")
    
    min_age, max_age = 18, 45
    ages = list(range(min_age, max_age + 1))
    rows = []
    for a in ages:
        tmp = {k: (v.copy() if isinstance(v, dict) else v) for k, v in base_data.items()}
        tmp["candidate"]["age"] = a
        r = calculate_deep_metrics(tmp)
        prob = r["total"] / 100.0
        rows.append({"Edad_candidata": a, "Score": r["total"], "Probabilidad": prob})
    
    df = pd.DataFrame(rows)
    
    tab1, tab2 = st.tabs(["Score por Edad", "Probabilidad por Edad"])
    with tab1:
        fig1 = px.line(df, x="Edad_candidata", y="Score", markers=True,
                       title="Score vs Edad",
                       labels={"Edad_candidata": "Edad", "Score": "Score (0-100)"})
        st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        fig2 = px.line(df, x="Edad_candidata", y="Probabilidad", markers=True,
                       title="Probabilidad vs Edad",
                       labels={"Edad_candidata": "Edad", "Probabilidad": "Probabilidad de Éxito"})
        st.plotly_chart(fig2, use_container_width=True)

def main():
    st.title(TITLE)
    
    st.sidebar.title("📊 Progreso")
    st.sidebar.progress(st.session_state.step / 4)
    
    if st.sidebar.button("🔄 Reiniciar Sistema"):
        st.session_state.step = 1
        st.rerun()
    
    if st.session_state.step == 1:
        st.markdown("## Fase 1: Calibración del Operador")
        with st.form("step1"):
            age = st.number_input("Tu Edad", 20, 60, 30)
            income = st.number_input("Ingreso Mensual (USD)", 0, 10000, 2400)
            goal = st.selectbox("Objetivo", ["Familia e Hijos", "Pareja Estable", "Casual"])
            if st.form_submit_button("➡️ Siguiente"):
                st.session_state.data["user"] = {"age": age, "income": income, "goal": goal}
                st.session_state.step = 2
                st.rerun()
    
    elif st.session_state.step == 2:
        st.markdown("## Fase 2: Datos del Sujeto")
        with st.form("step2"):
            name = st.text_input("Nombre")
            age_c = st.number_input("Edad de ella", 18, 50, 28)
            kids = st.checkbox("¿Tiene hijos?")
            if st.form_submit_button("➡️ Siguiente"):
                st.session_state.data["candidate"] = {"name": name, "age": age_c, "has_kids": kids}
                st.session_state.step = 3
                st.rerun()
    
    elif st.session_state.step == 3:
        st.markdown("## Fase 3: Input de Operaciones de Campo")
        st.info("Introduce los resultados de los experimentos conductuales.")
        with st.form("step3"):
            st.markdown("**1. Reacción al Límite (Test del No)**")
            rno = st.radio("Resultado", ["Aceptacin tranquila", "Molestia visible", "ManipulaciónVenganza"])
            
            st.markdown("**2. Reacción Intelectual**")
            rmono = st.radio("Resultado", ["Pregunt con inters", "Escuch pasivamente", "IgnorCelular"])
            
            st.markdown("**3. Madurez (Pregunta del Ex)**")
            rex = st.text_area("¿Qué dijo sobre su error pasado?", "Admitió que era inmadura...")
            
            if st.form_submit_button("📈 GENERAR DASHBOARD"):
                st.session_state.data["missions"] = {"testno": rno, "testmono": rmono, "testex": rex}
                st.session_state.step = 4
                st.rerun()
    
    elif st.session_state.step == 4:
        results = calculate_deep_metrics(st.session_state.data)
        
        tab1, tab2, tab3 = st.tabs(["💘 Lectura Romántica", "🧠 Análisis Científico", "📈 Gráficos"])
        
        with tab1:
            render_dashboard(results)
        
        with tab2:
            render_scientific_tab(results)
        
        with tab3:
            render_graphics_tab(results)

if __name__ == "__main__":
    main()
