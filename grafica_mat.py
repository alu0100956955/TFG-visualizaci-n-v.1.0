import matplotlib.pyplot as plt
from leerDatos import ParseCasosConfirmados
import numpy as np
from clases_base import Grafica

#l = Lector('data/casos_2019.csv')

class Linea_mat(Grafica):


#funcion encargada de hacer que no aparezcan todos los valores ya que eso hara la vision mas jodida
    def ticks(self,array):
        i = 0
        for x in array:
            if(i%2==0):
                add(i)
                i +=1

# TO DO:
# El metodo para poder rotar entre los distintso tipos de lineas ( mirar hojas)
# probar mas tipos de graficas
# Permitir distintos tipos de graficas o tener distintos metodos para hacere las graficas
    def show(data):
        #paises = ['Spain','Italy','China','Portugal']
        seleccionados = data.getSeleccionados()
        for i in range(len(seleccionados)):
             # TO DO ver como alterar el tipo de grafica y sus opciones en cada iteracion
            plt.plot(data.getEjeX(),data.getEjeY(seleccionados[i]), marker = Linea_mat.marker(i), linestyle = Linea_mat.line(i), markeredgecolor = Linea_mat.color(i))
            plt.text(data.getEjeX().size,data.getEjeY(seleccionados[i])[-1],s = seleccionados[i]) # Para que aparezcan los nombres de los elementos al final de la linea
        #plt.xticks(ticks=Linea_mat.rango(data),labels=data.getEjeX(),rotation=70)
        plt.xticks(ticks=Linea_mat.rango(data.getEjeX()),labels=data.getEjeX(),rotation=70)
        plt.title(data.getTitle())
        plt.legend()
        plt.grid()
        plt.show()

    # metodo encargado de genrar un array para el eje x que sea mucho mas visible, para ello combertira algunos valores en string vacios
    # array: sera el array del ejeX que contendra los elementos string de las fechas
    def rango(array):
        #return np.arange(0,dataset.getEjeX().size,3).tolist()
        #rango = []
        for i in range(array.size):
            if(i%3 != 0):
                array[i] = ""
        return array

# To do : controlar cuando se sale de rango, si se pasa restarle la cantidad del array o hacer % o una division...
# Controlar cuando se salga del limite
    # Metodo que devuelve el tipo de marca
    def marker(indice):
        markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_' ]
        return markers[indice]

    # Metodo que devuelve el tipo de linea
    def line(indice):
        line = ['-', '--', '-.', ':' ]
        return line[indice]

    # Metodo que devuelve el color de la linea
    def color(indice):
        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w' ]
        return colors[indice]

    def prueba():
        a = l.ejeX(4)
        print(a)
        a = l.ejeX(12)
        print(a)

#adfasfd
