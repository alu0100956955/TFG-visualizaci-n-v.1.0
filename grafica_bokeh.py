from leerDatos import Lector
from bokeh.plotting import figure, output_file, show

#l = Lector('data/casos_2019.csv')
class Grafica_bokeh:

# TO DO 
# Arreglar el ejeX
# Probar mas graficas
    def show(l):
        output_file("html/lineas.html")
        p = figure(title="Casos confirmados en España",x_axis_label='Fechas',y_axis_label='Casos')

        #falta el ejeX pero no lo tira bien asi que tengo que mirar que tipo de dato es el que pide para reestructurarlo
        p.line( l.ejeY(18), legend_label="Temp.", line_width=2)


        show(p)


#asdfasdfadf
