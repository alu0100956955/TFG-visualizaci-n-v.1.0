#!/usr/bin/env python
# -*- coding: utf-8 -*-
from leerDatos import ParseCasosConfirmados
#from grafica_mat import Linea_mat
#from grafica_pygal import Linea_pygal, Box_pygal
#from interfaz_usuario import Usuario
from factory import Selector
from estrategia import ContextoGrafica

# La clase mediador debe de tener todas las clases ya que sera la que medie entre ellas

class Intermedio:

    # Metodo nuevo
    def show(grafica, Datos):
        contextoG = ContextoGrafica() 
        Selector.grafica(grafica,contextoG)
        contextoG.show(Datos)

    def getParse(eleccion):  # le indicamos a la clase se seleccion que ha seleccionado el usuario y nos devuelve el parse correspondiente
        #return Selector.getParse(url)
        return Selector.getParse(eleccion)
    def getParseSpark(eleccion):
        return Selector.getParseSpark(eleccion)

    # Metodo antiguo
    # Llamo a la interfaz de usuario, esta me devuelve los valores del usuario, se los paso al parse, que me devulve las clases que necesito y ejecuto los metodos principales
    # TO DO: parametrizar la ruta de los datos
    def show2():
        aux = 20
        Usuario.ventanaUsuario()#pasarle un mediador
        contextoG = ContextoGrafica()
        ruta = 'data/casos_2019.csv'  #Datos en el pc
        ruta2 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv' # Datos gitHub
        paises = ['Spain','Italy','China','Portugal'] # No puede estar cableado
        #while int(aux) != 0:
        if(False):
            contextoG.setSeleccionados(paises)  # le pasamos al contexto los paises que se van a representar, es decir los elementos seleccionados de entre todos
            aux = Usuario.pedirGrafica() # Pedimos al usuario el tipo de grafica que quiere
            if (int(aux) != 0):
                Selector.grafica(aux,contextoG)  # Le pasamos el contexto para que le indique que tipo de grafica usara
                parse = Selector.parse(ruta2) # la ruta la pongo a mano por ahora ya vere como parametrizarla | hay que habilitar el contexto para los parse
                contextoG.show(parse)
# fsadgfsgfdg
