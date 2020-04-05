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
            fig.add_trace(go.Bar(y = data.ejeY(selec)))
        #fig.update_layout(title = 'Casos confirmados', xaxis_title="fecha",yaxis_title="Numero de casos")
        fig.update_layout(title = data.getTitle())
        fig.show()


# TO DO: arreglar el ejeX
#  Pillar el titulo del parse
class Lineas_plotly(Grafica):

    def show(data, seleccionados):
        #paises = ['Spain','Italy','China','Portugal']
        fig = go.Figure()
        for selec in seleccionados:
            fig.add_trace(go.Scatter(y = l.ejeY(selec)))
        #fig.update_layout(title = 'Casos confirmados', xaxis_title="fecha",yaxis_title="Numero de casos")
        #fig.update_layout(xaxis_title=l.ejeX())
        #fig.write_html('output/lineas_ploty.html', auto_open=True)   # para guardar la grafica en un html
        fig.update_layout(title = data.getTitle())
        fig.show()

#asdfasdfasd
