import streamlit as st
from datetime import date
from PIL import Image
from fpdf import FPDF
import tempfile, os

st.set_page_config(
    page_title="Generador de Informes",
    layout="wide"
)

st.title("Generador Profesional de Informes")
st.caption("Sistema para inspecciones de Seguridad e Higiene")

st.divider()

col1, col2 = st.columns(2)

with col1:
    empresa = st.text_input("Empresa / Cliente")
    obra = st.text_input("Obra / Proyecto")
    direccion = st.text_input("Direccion")
    inspector = st.text_input("Inspector")

with col2:
    fecha = st.date_input("Fecha de inspeccion", value=date.today())
    tipo = st.selectbox(
        "Tipo de inspeccion",
        ["General", "Obra", "Vereda", "Mantenimiento", "Riesgo electrico", "Trabajo en altura", "Otro"]
    )
    riesgo = st.selectbox(
        "Nivel de riesgo",
        ["Bajo", "Medio", "Alto", "Critico"]
    )

st.subheader("Checklist de control")

checklist = {
    "Uso de EPP": st.checkbox("Uso de EPP"),
    "Senalizacion adecuada": st.checkbox("Senalizacion adecuada"),
    "Vallado perimetral": st.checkbox("Vallado perimetral"),
    "Orden y limpieza": st.checkbox("Orden y limpieza"),
    "Circulacion peatonal segura": st.checkbox("Circulacion peatonal segura"),
    "Riesgo electrico controlado": st.checkbox("Riesgo electrico controlado"),
    "Materiales correctamente acopiados": st.checkbox("Materiales correctamente acopiados"),
    "Extintores / elementos de emergencia": st.checkbox("Extintores / elementos de emergencia"),
}

observaciones = st.text_area("Observaciones detectadas", height=160)
riesgos_text = st.text_area("Riesgos detectados", height=140)
recomendaciones = st.text_area("Recomendaciones / acciones correctivas", height=140)

imagenes = st.file_uploader(
    "Subir evidencia fotografica",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

st.divider()

if st.button("Generar vista previa profesional"):

    st.success("Informe generado correctamente")
    st.header("Vista previa del informe")

    st.markdown("# INFORME TECNICO DE INSPECCION")
    st.markdown(f"*Fecha:* {fecha}")
    st.markdown(f"*Empresa / Cliente:* {empresa}")
    st.markdown(f"*Obra / Proyecto:* {obra}")
    st.markdown(f"*Direccion:* {direccion}")
    st.markdown(f"*Inspector:* {inspector}")
    st.markdown(f"*Tipo de inspeccion:* {tipo}")
    st.markdown(f"*Nivel de riesgo:* {riesgo}")

    st.markdown("---")
    st.markdown("## 1. Introduccion")
    st.write("En la fecha indicada se realizo una inspeccion tecnica con el objetivo de relevar las condiciones generales de seguridad, higiene y prevencion de riesgos.")

    st.markdown("---")
    st.markdown("## 2. Observaciones generales")
    st.write(observaciones if observaciones else "No se registraron observaciones generales.")

    st.markdown("---")
    st.markdown("## 3. Riesgos detectados")
    st.write(riesgos_text if riesgos_text else "No se registraron riesgos especificos.")

    st.markdown("---")
    st.markdown("## 4. Checklist de control")
    for item, ok in checklist.items():
        estado = "Cumple" if ok else "Requiere revision"
        st.write(f"*{item}:* {estado}")

    st.markdown("---")
    st.markdown("## 5. Recomendaciones tecnicas")
    st.write(recomendaciones if recomendaciones else "Se recomienda continuar con controles periodicos.")

    st.markdown("---")
    st.markdown("## 6. Conclusion")
    st.write("De acuerdo con la inspeccion realizada, se deja constancia de las condiciones observadas y de las acciones correctivas recomendadas.")

    if imagenes:
        st.markdown("---")
        st.subheader("7. Evidencia fotografica")
        cols = st.columns(2)
        for i, img in enumerate(imagenes):
            with cols[i % 2]:
                st.image(img, caption=f"Evidencia {i+1}", use_container_width=True)

    # --- GENERAR PDF ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "INFORME TECNICO DE INSPECCION", ln=True, align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Fecha: {fecha}", ln=True)
    pdf.cell(0, 8, f"Empresa / Cliente: {empresa}", ln=True)
    pdf.cell(0, 8, f"Obra / Proyecto: {obra}", ln=True)
    pdf.cell(0, 8, f"Direccion: {direccion}", ln=True)
    pdf.cell(0, 8, f"Inspector: {inspector}", ln=True)
    pdf.cell(0, 8, f"Tipo de inspeccion: {tipo}", ln=True)
    pdf.cell(0, 8, f"Nivel de riesgo: {riesgo}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "1. Introduccion", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, "En la fecha indicada se realizo una inspeccion tecnica con el objetivo de relevar las condiciones generales de seguridad, higiene y prevencion de riesgos.")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "2. Observaciones generales", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, observaciones if observaciones else "No se registraron observaciones generales.")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "3. Riesgos detectados", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, riesgos_text if riesgos_text else "No se registraron riesgos especificos.")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "4. Checklist de control", ln=True)
    pdf.set_font("Helvetica", "", 11)
    for item, ok in checklist.items():
        estado = "Cumple" if ok else "Requiere revision"
        pdf.cell(0, 7, f"  {item}: {estado}", ln=True)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "5. Recomendaciones tecnicas", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, recomendaciones if recomendaciones else "Se recomienda continuar con controles periodicos.")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "6. Conclusion", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 7, "De acuerdo con la inspeccion realizada, se deja constancia de las condiciones observadas y de las acciones correctivas recomendadas.")

    if imagenes:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, "7. Evidencia fotografica", ln=True)
        pdf.ln(3)
        for i, img in enumerate(imagenes):
            img.seek(0)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(img.read())
                tmp_path = tmp.name
            pdf.image(tmp_path, w=160)
            pdf.ln(3)
            os.unlink(tmp_path)

    pdf_bytes = bytes(pdf.output())
    st.download_button(
        label="Descargar PDF",
        data=pdf_bytes,
        file_name=f"informe_{empresa}_{fecha}.pdf",
        mime="application/pdf"
    )