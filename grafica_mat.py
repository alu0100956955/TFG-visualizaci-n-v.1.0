
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
        for i in range(len(seleccionados)): # Lo hago con el rango para los metodos complementarios
            #TO DO: pasar de forma parametrizada el eje que se quiere representar
            plt.plot(data.getEje(data.getSeleccionEjeX(),0),data.getEje(data.getSeleccionEjeY(),seleccionados[i]), marker = Linea_mat.marker(i), linestyle = Linea_mat.line(i), markeredgecolor = Linea_mat.color(i) , label = seleccionados[i])
            # TO DO falta quitar lo de ejeY y poner solo getEje
            #plt.text(len(data.getEje("Dias",0)),data.getEjeY(seleccionados[i])[-1],s = seleccionados[i]) # Para que aparezcan los nombres de los elementos al final de la linea
        #plt.xticks(ticks=Linea_mat.rango(data),labels=data.getEjeX(),rotation=70)
        plt.xticks(ticks=Grafica.espaciar(data.getEje("Dias",0)),labels=data.getEjeX(),rotation=1)  # ARREGLAR
        plt.title(data.getTitle())
        plt.legend()
        plt.grid()
        plt.show()

# To do : controlar cuando se sale de rango, si se pasa restarle la cantidad del array o hacer % o una division...
# Controlar cuando se salga del limite
    # Metodo que devuelve el tipo de marca
    def marker(indice):
        if (indice > 21):
            return marker(indice -21)
        else:
            markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '|', '_' ]
        return markers[indice]

    # Metodo que devuelve el tipo de linea
    def line(indice):
        if ( indice > 3):   # Si el indice es mayor que la cuarta posicion le restamos 4 y empleamos la recursividad
            return line(indice-4)
        else:
            line = ['-', '--', '-.', ':' ]
        return line[indice]

    # Metodo que devuelve el color de la linea
    def color(indice):
        if( indice > 7):
            return color(indice - 7)
        else:
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w' ]
        return colors[indice]

    def prueba():
        a = l.ejeX(4)
        print(a)
        a = l.ejeX(12)
        print(a)

#adfasfd
