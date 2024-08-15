# Librerias instaladas por el usuario
import os
from fpdf import FPDF

# Conexión a la base de datos
DIRECCION = {
    "Agricola Oriental":"Av. Javier Rojo Gómez 176, Agrícola Oriental, Iztacalco, 08500 Ciudad de México, CDMX.", 
    "Nezahualcóyotl":"Flamingos 257, Metropolitana 3ra Secc, 57750 Cdad. Nezahualcóyotl, Méx.", 
    "Zapotitlan":"Av. Tlahuac 5882, Santa Ana Poniente, Tláhuac, 13300 Ciudad de México.", 
    "Oaxtepec":"Municipio de, Emperador 3-LOCAL, Centro, 62728 Oaxtepec, Mor.", 
    "Pantitlan":"Calle Corona del Rosal 33, Venustiano Carranza, 15670 CDMX, CDMX."
    }
IMAGE_PDF = {
    "Agricola Oriental":"./assets/pdf_agricola.png",
    "Nezahualcóyotl":"./assets/pdf_neza.png",
    "Zapotitlan":"./assets/pdf_zapo.png",
    "Oaxtepec":"./assets/pdf_oaxte.png",
    "Pantitlan":"./assets/pdf_panti.png"
}

EMPLEADO_LEVANTA = {
    "Agricola Oriental":"ELVIA CASTILLO ALANIZ",
    "Nezahualcóyotl":"HILDA CABRERA ALBA",
    "Zapotitlan":"ERICKA HUITZIL MENDEZ",
    "Oaxtepec":"THALIA ROMERO",
    "Pantitlan":"DOÑA ELY"
}


def descargar_pdf(NOMBRE_SUCURSAL, clave, fecha_pedido, fecha_entrega, producto_cantidad):

    class PDF(FPDF):
        def header(self):
            # Colocamos el logo:
            self.image(IMAGE_PDF[NOMBRE_SUCURSAL], x=10, y=10, w=40, h=25)
            # Titulo 
            self.set_font("helvetica", "B", 15)
            self.cell(w=50, h=5, text="", border=0, align='C', fill=0)
            self.multi_cell(w=0, h=5, text="PASTELERÍAS NARCISSE", border=0, align='C', fill=0)
            self.ln(0.5)
            # Sucursal
            self.set_font("helvetica", "B", 12)
            self.cell(w=50, h=5, text="", border=0, align='C', fill=0)
            self.multi_cell(w=0, h=5, text="SUCURSAL: " + str(NOMBRE_SUCURSAL).upper(), border=0, align='C', fill=0)
            self.ln(0.5)
            # Dirección
            self.set_font('helvetica', '', 9)
            self.cell(w=50, h=5, text="", border=0, align='C', fill=0)
            self.multi_cell(w=0, h=5, text=DIRECCION[NOMBRE_SUCURSAL], border=0, align='C', fill=0)
            self.ln(0.5)
            # Performing a line break:
            self.ln(10)

        def footer(self):
            # Position cursor at 1.5 cm from bottom:
            self.set_y(-15)
            # Setting font: helvetica italic 8
            self.set_font("helvetica", "I", 8)
            # Printing page number:
            self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", align="C")

    #####################
    # CREAMOS UN LIENZO #
    #####################
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=12)

    ###################
    # DATOS INICIALES #
    ###################
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(w=50, h=6, text=clave, border=0, align='L', fill=0)
    pdf.multi_cell(w=0, h=6, text=fecha_pedido, border=0, align='R', fill=0)
    pdf.ln(5)

    ####################
    # DATOS DEL PEDIDO #
    ####################
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(w=0, h=10, text="DATOS DEL PEDIDO", border='B', align='C', fill=0)
    pdf.ln(15)

    pdf.set_fill_color(217, 217, 217)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(w=80, h=6, text="NOMBRE DE QUIEN REALIZA EL PEDIDO:", border=0, align='L', fill=1)
    pdf.multi_cell(w=0, h=6, text= '   ' + EMPLEADO_LEVANTA[NOMBRE_SUCURSAL], border=0, align='L', fill=0)
    pdf.ln(3)
    pdf.cell(w=40, h=6, text="FECHA DE SOLICITUD:", border=0, align='L', fill=1)
    pdf.cell(w=60, h=6, text='   '+ fecha_pedido, border=0, align='L', fill=0)
    pdf.cell(w=40, h=6, text="FECHA DE ENTREGA:", border=0, align='L', fill=1)
    pdf.multi_cell(w=0, h=6, text='   ' + fecha_entrega, border=0, align='L', fill=0)
    pdf.ln(15)

    ##########
    # PEDIDO #
    ##########
    my_w = 75
    w_space = 10
    w_unidad = 15
    pdf.set_font('helvetica', 'B', 8)
    salto = 0
    for producto, cantidad in producto_cantidad:
        if salto < 1:
            pdf.cell(w=my_w, h=6, text=str(producto).upper() + ":", border=0, align='L', fill=1)
            pdf.cell(w=w_unidad, h=6, text=f'{str(cantidad)} uds.', border='B', align='C', fill=0)
            pdf.cell(w=w_space, h=6, text='', border=0, align='C', fill=0)
            salto += 1
        elif salto == 1:
            pdf.cell(w=my_w, h=6, text=str(producto).upper() + ":", border=0, align='L', fill=1)
            pdf.multi_cell(w=0, h=6, text=f'{str(cantidad)} uds.', border='B', align='C', fill=0)
            pdf.ln(2)
            salto = 0

    #############
    # CREAR PDF #
    #############
    pdf_output = pdf.output(dest='S')
    return bytes(pdf_output)