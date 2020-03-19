from leerDatos import Lector
from grafica_mat import Grafica_mat
from grafica_bokeh import Grafica_bokeh
from grafica_pygal import Grafica_pygal


# main simple inicial para probar las graficas
# to do : la labor de hablar con la clase Lector y Grafica deberia ser un mediador, por tanto implementar una clase mediador

l = Lector('data/casos_2019.csv')
#grafica = Grafica_mat
#grafica = Grafica_bokeh
grafica = Grafica_pygal
grafica.show(l)








# adfgasdg
