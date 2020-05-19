import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
import pandas as pd
from urllib.request import urlopen
#Mis clases
from leerDatos import ParseCasosConfirmados
from clases_base import Grafica

# El resultado de plotly es un html

class Barras_plotly(Grafica):

    def show(data):
        #paises = ['Spain','Italy','China','Portugal']
        seleccionados =  data.getSeleccionados()
        fig = go.Figure()
        for selec in seleccionados:
            fig.add_trace(go.Bar(y = data.getEjeY(selec), name = selec))
        #fig.update_layout(title = 'Casos confirmados', xaxis_title="fecha",yaxis_title="Numero de casos")
        fig.update_layout(title = data.getTitle())
        # range(data.getEjeX().size)
        ticksy = []
        for i in range(data.getEjeX().size):
            ticksy.append(i)
        # Para cambiar el eje X
        fig.update_layout(xaxis = dict( tickmode = 'array', tickvals =ticksy , ticktext = Grafica.espaciar(data.getEjeX()) ) )
        fig.show()


# TO DO: arreglar el ejeX
#  Pillar el titulo del parse
class Lineas_plotly(Grafica):

    def show(data):
        #paises = ['Spain','Italy','China','Portugal']
        seleccionados = data.getSeleccionados()
        fig = go.Figure()
        for selec in seleccionados:
            fig.add_trace(go.Scatter(y = data.getEje(data.getSeleccionEje(),selec), name = selec))
        #fig.update_layout(title = 'Casos confirmados', xaxis_title="fecha",yaxis_title="Numero de casos")
        #fig.update_layout(xaxis_title=l.ejeX())
        #fig.write_html('output/lineas_ploty.html', auto_open=True)   # para guardar la grafica en un html
        fig.update_layout(title = data.getTitle())
        ticksy = []
        for i in range(data.getEje("Dias",0).size):   # Este es el eje X por eso pongo Dias
            ticksy.append(i)
        # Para cambiar los valores del eje X
        fig.update_layout(xaxis = dict( tickmode = 'array', tickvals =ticksy , ticktext = Grafica.espaciar(data.getEje("Dias",0))))
        fig.show()


class Scatter_plotly(Grafica):

    def show(data):
        seleccionados = data.getSeleccionados()
        fig = go.Figure()
        for elemento in data.getOpciones():
            fig.add_trace(go.Scatter(y = data.getEjeY(elemento), mode='markers', name = elemento))
        fig.update_layout(title = data.getTitle())

        fig.show()


# Esta hecho exclusivamente para data que contenga todos los paises si no fallara
class Mapa_plotly(Grafica):

    def show(data):
        # El Json que contiene los paises
        with open('data/countries.json') as file:
            countries = json.load(file)

        id = [] # Los id de cada pais correspondientes a los del json para que se represente correctamente cada dato
        valores = []
        nombrePais = [] # El nombre del pais segun el fichero json ( para ver que nombre le asigna ya que hay paises que no me los encuentra)
        #for pais in data.getOpciones():
        for pais in countries['features']:
            nombre = pais['properties']['SOVEREIGNT'] # Este es el nombre del pais
            nombrePais.append(nombre)
            # Hay que controlar si el nombre es correcto
            x = data.getEje("Cantidad de contagios",nombre)
            id.append(pais['id'])
            valores.append(x[-1]) # EL -1 es para sacar el ultimo elemento de la lista que es el del ultimo dia

        df = pd.DataFrame({"id":id,"Casos Confirmados":valores,"Pais":nombrePais}) # El nombre para cada uno determinara lo que se vera al pasar el raton por cada pais

        #fig = go.Figure(go.Scattergeo())

        fig = px.choropleth(df, geojson=countries, locations='id', color='Casos Confirmados',
                                   color_continuous_scale="Viridis",
                                   range_color=(0, 30),
                                   labels={'Casos':'Casos confirmados covid'}
                                  )

        fig.update_geos(
            projection_type="natural earth",
            showcountries=True, countrycolor="Purple",
            showland=True, landcolor="LightGreen",
            showocean=True, oceancolor="LightBlue"
        )
        fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})

        fig.show()

    #Si el nombre que esta registrado en el json es correcto devuelve el nombre que se le paso, en caso contrario pasara el que corresponda
    def nombreCorrecto(nombre):
        # Por ahora solo hay un nombre que es el de US, para poder admitir multiples nombres meter un dicionario
        if (nombre == ""):
            return "US1"
        return nombre



#asdfasdfasd
