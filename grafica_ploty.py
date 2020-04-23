import plotly.graph_objects as go
import plotly.express as px
import numpy as np
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
        fig.update_layout(xaxis = dict( tickmode = 'array', tickvals =ticksy , ticktext = data.getEjeX()))
        fig.show()


# TO DO: arreglar el ejeX
#  Pillar el titulo del parse
class Lineas_plotly(Grafica):

    def show(data):
        #paises = ['Spain','Italy','China','Portugal']
        seleccionados = data.getSeleccionados()
        fig = go.Figure()
        for selec in seleccionados:
            fig.add_trace(go.Scatter(y = data.getEjeY(selec), name = selec))
        #fig.update_layout(title = 'Casos confirmados', xaxis_title="fecha",yaxis_title="Numero de casos")
        #fig.update_layout(xaxis_title=l.ejeX())
        #fig.write_html('output/lineas_ploty.html', auto_open=True)   # para guardar la grafica en un html
        fig.update_layout(title = data.getTitle())
        ticksy = []
        for i in range(data.getEjeX().size):
            ticksy.append(i)
        # Para cambiar los valores del eje X
        fig.update_layout(xaxis = dict( tickmode = 'array', tickvals =ticksy , ticktext = data.getEjeX()))
        fig.show()


class Scatter_plotly(Grafica):

    def show(data):
        seleccionados = data.getSeleccionados()
        fig = go.Figure()
        for elemento in data.getOpciones():
            fig.add_trace(go.Scatter(y = data.getEjeY(elemento), mode='markers', name = elemento))
        fig.update_layout(title = data.getTitle())

        fig.show()



class Mapa_plotly(Grafica):
    
    def show(data):
        fig = go.Figure(go.Scattergeo())
        fig.update_geos(
            projection_type="natural earth",
            showcountries=True, countrycolor="Purple",
            showland=True, landcolor="LightGreen",
            showocean=True, oceancolor="LightBlue"
        )
        fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})

        fig.show()




#asdfasdfasd
