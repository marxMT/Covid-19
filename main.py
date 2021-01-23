# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 21:41:24 2020

@author: marx.e.morales.tello
"""
from funciones import *

lista_provincias = ['Buenos Aires','Ciudad de Buenos Aires','Chaco','Santa Fe',
                    'Córdoba','Tierra del Fuego','San Juan','Corrientes','Jujuy',
                    'La Pampa','Entre Ríos','La Rioja','Mendoza','Misiones','Neuquén',
                    'Río Negro','Salta','San Luis',
                    'Santa Cruz','Santiago','Tucumán','Catamarca','Chubut','Formosa']
url = "https://www.argentina.gob.ar/coronavirus/informe-diario"
soup_w = acceso_html(url)
urls = extraccion_enlaces(soup_w)
for url in urls:
    descargar_pdf(url)

    