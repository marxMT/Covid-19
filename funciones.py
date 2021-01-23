# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 19:37:53 2020

@author: marx.e.morales.tello
"""
from bs4 import BeautifulSoup
import PyPDF2
from urllib.request import Request, urlopen
from datetime import datetime, date, timedelta
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn import lmplot
import matplotlib.pylab as pyt



def acceso_html(url):
    """Genera la conexion y acceso a la pagina"""
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web = urlopen(req)
        soup_w = BeautifulSoup(web, features="lxml")
    except:
        print("error en al conexion")
    return soup_w

def extraccion_enlaces(soup):
    """
        Retorna una lista de enlaces, para la descarga del  informe
    """
    
    tags = soup.findAll("a",{"class":"btn-sm"})
    urls = [tag.get('href') for tag in tags]
    if len(urls) > 0:
        urls = urls
    else:
        urls = "No existe elementos "
    return urls

def extracion_ultimo_enlace(soup):
    """
        Retorna el ultimo enlace
    """
    tags = soup.findAll("a",{"class":"btn-sm"})
    return tags[0].get("href")

def descargar_pdf(url):
    """Descarga y almacena el informe en la carpeta local"""
    today = date.today()
    fecha = today.strftime('%d-%m-%Y')
    #name_file = "Argentina_Data_"+ fecha+".pdf"
    name_file = url[49:]
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    informe_pdf = urlopen(req)
    with open(name_file, "wb") as f:
        f.write(informe_pdf.read())
        
def procesar_pdf(file_pdf, lista_provincias):
    """Retorna de las provincias y casos"""
    pdf_file = open(file_pdf,mode="rb")
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    paginas =[read_pdf.getPage(i) for i in range(number_of_pages)]
    page_content = " ".join(paginas)
    lista_contenido = page_content.split('\n')
    pdf_file.close()
    lista_contenido_clear = [elemento for elemento in lista_contenido if elemento not in ['-','_', ' ','\t','.'] ]
    lista_data_provincias = []
    for elemento in lista_provincias:
        for line in lista_contenido_clear:
            if line.startswith(elemento):
                lista_data_provincias.append(line)
    return lista_data_provincias

def generar_data_set(lista_data_provincias):
    df = pd.DataFrame({"Ciudad":lista_data_provincias})
    #generamos las columnas : Provincias | infectados | muertos |fecha | dia | mes
    df['Fecha']=today
    df['Dia'] = today.day
    df['Mes'] = today.month
    df['Provincia'] = df['Ciudad'].str.extract(r'(^[aA-zZ]+[" "aA-zZá,é,í,ó,ú]+)')
    df['Infectados'] = df['Ciudad'].str.extract(r'([0-9]+)')
    df['Muertos'] = df['Ciudad'].str.extract(r'([|][" "0-9]+)')
    df['Muertos'] = df['Muertos'].str.extract(r'([0-9]+)')
    #eliminamos la comlumna Ciuad 
    df= df.drop(['Ciudad'], axis=1)
    df['Infectados']=df['Infectados'].astype(int)
    df['Muertos']= df['Muertos'].astype(int)
    return df



    