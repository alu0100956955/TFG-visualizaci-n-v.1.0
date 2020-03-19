import matplotlib.pyplot as plt
from leerDatos import Lector
import numpy as np

#l = Lector('data/casos_2019.csv')

class Grafica_mat:


#funcion encargada de hacer que no aparezcan todos los valores ya que eso hara la vision mas jodida
    def ticks(self,array):
        i = 0
        for x in array:
            if(i%2==0):
                add(i)
                i +=1

# TO DO:
# parametrizar el pais que pueda mostrar
# probar mas tipos de graficas
# Permitir distintos tipos de graficas o tener distintos metodos para hacere las graficas
    def show(l):
        plt.plot(l.ejeX(),l.ejeY(18), 'b--', marker='.', label = 'España')
        plt.plot(l.ejeX(),l.ejeY(16), 'g--', marker='^', label = 'Italia')
        plt.xticks(ticks=l.rango(),labels=l.ejeX(),rotation=70)
        plt.title('Casos confirmados')
        plt.legend()
        plt.grid()
        plt.show()

    def prueba():
        a = l.ejeX(4)
        print(a)
        a = l.ejeX(12)
        print(a)

#adfasfd
