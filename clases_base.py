#Aqui estaran las clases base o padre | la herencia no funciona igual de bien en python con respecto a java
import numpy as np

class Grafica:

    def show(data, seleccionados):
        pass

    # Este metodo sirve para hacer que sean los elementos espacios menos 7, que seran los ticks del eje X
    def espaciar(valores):
        tam = len(valores)
        z = tam/7   # Este es para la cantidad de ticks, como quiero que solo salgan 7 etiquetas pos el modulo sera con el numero que salga como resultado
        for i in np.arange(0,tam):
            if(i%int(z) != 0): # Cada 10 valores dejo el original para que no este tan aglomerado
                # añadir espcios
                valores[i] = ""
        # devolver el array con las fechas sobreescritas
        return valores


class Parse:

    def ejeX():
        pass

    def ejeY():
        pass



#asdfasdf
