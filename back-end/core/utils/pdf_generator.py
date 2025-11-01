import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from django.conf import settings
import os

def generar_pdf_anamnesis(anamnesis):
    """
    Genera un PDF con los datos actualizados de la anamnesis.
    Guarda el archivo en /media/anamnesis_pdfs/
    """
    # Ruta donde se guardará el PDF
    folder_path = os.path.join(settings.MEDIA_ROOT, "anamnesis_pdfs")
    os.makedirs(folder_path, exist_ok=True)
    filename = f"anamnesis_{anamnesis.id}.pdf"
    file_path = os.path.join(folder_path, filename)

    # Crear PDF en memoria
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Encabezado
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, height - 60, "Informe de Anamnesis")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, height - 100, f"Estudiante: {anamnesis.evaluacion_integral.estudiante.nombres_apellidos}")
    pdf.drawString(100, height - 120, f"Fecha: {anamnesis.fecha or 'No registrada'}")
    pdf.drawString(100, height - 140, f"Definición del problema:")
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(120, height - 160, (anamnesis.definicion_problema or "No registrada")[:100])

    pdf.setFont("Helvetica", 11)
    pdf.drawString(100, height - 200, "Observaciones generales:")
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(120, height - 220, (anamnesis.observaciones_generales or "No registradas")[:100])

    pdf.showPage()
    pdf.save()

    # Guardar PDF
    with open(file_path, "wb") as f:
        f.write(buffer.getvalue())

    buffer.close()

    # Retornar ruta relativa (para usar en front)
    relative_path = os.path.join("anamnesis_pdfs", filename)
    return relative_path
