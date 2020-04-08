import plotly.graph_objects as go
from leerDatos import ParseCasosConfirmados
import numpy as np
from clases_base import Grafica

# El resultado de plotly es un html

class Barras_plotly(Grafica):

    def show(data, seleccionados):
        #paises = ['Spain','Italy','China','Portugal']
        fig = go.Figure()
        for selec in seleccionados:
            fig.add_trace(go.Bar(y = data.getEjeY(selec)))
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

    def show(data, seleccionados):
        #paises = ['Spain','Italy','China','Portugal']
        fig = go.Figure()
        for selec in seleccionados:
            fig.add_trace(go.Scatter(y = data.getEjeY(selec)))
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

#asdfasdfasd
