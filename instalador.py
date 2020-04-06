#Fichero encargado de comprobar que el usuario tenga todas las librerias necesarias para la ejecución del entorno
import os
import importlib.util

class Instalador:

    def comprobarLibrerias():
        # Aqui escribire todas las librerias que son necesarias para el entorno y es lo único necesario alterar en este metodo
        # Si el nombre del paquete tiene "-" entonces sustituirlos por "."
        librerias = ['pygal','seaborn','matplotlib','numpy','plotly','pandas']
        for i in librerias:
            spec = importlib.util.find_spec(i)
            if spec is None:
                os.system('pip install '+ i)
        

#
