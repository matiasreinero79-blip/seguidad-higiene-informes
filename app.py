import streamlit as st
from datetime import date
from PIL import Image

st.set_page_config(
    page_title="Generador de Informes",
    layout="wide"
)

st.title("🦺 Generador Profesional de Informes")
st.caption("Sistema para inspecciones de Seguridad e Higiene")

st.divider()

col1, col2 = st.columns(2)

with col1:
    empresa = st.text_input("Empresa / Cliente")
    obra = st.text_input("Obra / Proyecto")
    direccion = st.text_input("Dirección")
    inspector = st.text_input("Inspector")

with col2:
    fecha = st.date_input("Fecha de inspección", value=date.today())
    tipo = st.selectbox(
        "Tipo de inspección",
        ["General", "Obra", "Vereda", "Mantenimiento", "Riesgo eléctrico", "Trabajo en altura", "Otro"]
    )
    riesgo = st.selectbox(
        "Nivel de riesgo",
        ["Bajo", "Medio", "Alto", "Crítico"]
    )

st.subheader("✅ Checklist de control")

checklist = {
    "Uso de EPP": st.checkbox("Uso de EPP"),
    "Señalización adecuada": st.checkbox("Señalización adecuada"),
    "Vallado perimetral": st.checkbox("Vallado perimetral"),
    "Orden y limpieza": st.checkbox("Orden y limpieza"),
    "Circulación peatonal segura": st.checkbox("Circulación peatonal segura"),
    "Riesgo eléctrico controlado": st.checkbox("Riesgo eléctrico controlado"),
    "Materiales correctamente acopiados": st.checkbox("Materiales correctamente acopiados"),
    "Extintores / elementos de emergencia": st.checkbox("Extintores / elementos de emergencia"),
}

observaciones = st.text_area("Observaciones detectadas", height=160)
riesgos = st.text_area("Riesgos detectados", height=140)
recomendaciones = st.text_area("Recomendaciones / acciones correctivas", height=140)

imagenes = st.file_uploader(
    "📸 Subir evidencia fotográfica",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

st.divider()

if st.button("📄 Generar vista previa profesional"):

    st.success("Informe generado correctamente")

    st.header("Vista previa del informe")

    st.markdown(f"""
# INFORME TÉCNICO DE INSPECCIÓN

*Fecha:* {fecha}  
*Empresa / Cliente:* {empresa}  
*Obra / Proyecto:* {obra}  
*Dirección:* {direccion}  
*Inspector:* {inspector}  
*Tipo de inspección:* {tipo}  
*Nivel de riesgo:* {riesgo}  

---

## 1. Introducción

En la fecha indicada se realizó una inspección técnica con el objetivo de relevar las condiciones generales de seguridad, higiene y prevención de riesgos presentes en el lugar inspeccionado.

---

## 2. Observaciones generales

{observaciones if observaciones else "No se registraron observaciones generales."}

---

## 3. Riesgos detectados

{riesgos if riesgos else "No se registraron riesgos específicos."}

---

## 4. Checklist de control
""")

    for item, ok in checklist.items():
        estado = "✅ Cumple" if ok else "⚠️ Requiere revisión"
        st.write(f"*{item}:* {estado}")

    st.markdown(f"""
---

## 5. Recomendaciones técnicas

{recomendaciones if recomendaciones else "Se recomienda continuar con controles periódicos y mantener las condiciones de seguridad e higiene correspondientes."}

---

## 6. Conclusión

De acuerdo con la inspección realizada, se deja constancia de las condiciones observadas y de las acciones correctivas recomendadas. El presente informe podrá ser utilizado como registro técnico y evidencia documental para el seguimiento de la obra o sector inspeccionado.
""")

    if imagenes:
        st.markdown("---")
        st.subheader("7. Evidencia fotográfica")

        cols = st.columns(2)
        for i, img in enumerate(imagenes):
            with cols[i % 2]:
             st.image(img, caption=f"Evidencia {i+1}", use_container_width=True)

         