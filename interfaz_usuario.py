import tkinter as tk
from tkinter import *
from mediador import Mediador

# Clase encargada en la interaccion con el usuario
class Usuario:

    # metodo inicial muy basico
    # TO DO: controlar el rango de valores por si el usuario se equivoca e introduce un valor no registrado
    def pedirGrafica():
        print(" 1.Linea matplotlib, 2.Linea pygal, 3.Linea plotly, 4.Barras plotly, 0.Exit")
        print("Que tipo de grafica desea:")
        return input()
    #, 5.Cajas pygal


    # Le paso el mediador y aqui sera el loop principal, desde el mediador se haran los otros pasos
    def ventanaUsuario():
        #Pedir fuente de Datos
        #Comprobar si es valida
        #Pedir tipo de grafica ( radiobutton), si es mapa se puede mostrar directamente en las otras una funcion que le quite el hidden a los otros elementos que les haga el pack
        #Pedir seleccionados si es necesario
        # Botton (Button) para que muestre la grafica, esta la opcion de que se muestre cada vez que escoga un radiobutton pero esa me parece mas peligrosa porque hay que seleccionar los elementos salvo en mapa

        def showGrafica(grafica, seleccionados, urlDatos):
            mediador.show2(grafica, seleccionados, urlDatos)

        urlDatos = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        ventana = tk.Tk()
        ventana.geometry('300x350')
        var = IntVar() # Variabla para controlar la opcion seleccionada por el usuario
        cajaTexto = tk.Entry(ventana)
        linea_mat = Radiobutton(ventana, text="Linea_mat", variable=var,value=1)
        linea_pygal = Radiobutton(ventana, text="Linea_pygal", variable=var,value=2)
        linea_plotly = Radiobutton(ventana, text="Linea_plotly", variable=var,value=3)

        # Por ahora lo dejo cableado
        opciones = ['Spain','Italy','China','Portugal']
        seleccionado = StringVar(ventana)   # la variable encargado despues de almacenar lo que seleccione el usuario
        seleccionado.set(opciones[0])   # le asigno el primero como default
        dropDownSeleccion = OptionMenu(ventana, seleccionado, *opciones)

        botonGrafica = Button(ventana, text ="Hacer grafica" , pady='10', command = lambda: Mediador.show( var.get(),opciones,urlDatos))

        label1 = tk.Label(ventana, text="Introduzca la fuente de datos")
        label2 = tk.Label(ventana, text="Seleccione el tipo de gráfica")
        label3 = tk.Label(ventana, text="Selecciona los elementos a representar" )

        #Añadir los elementos a la ventana
        label1.pack()
        cajaTexto.pack()
        label2.pack()
        linea_mat.pack()
        linea_pygal.pack()
        linea_plotly.pack()
        label3.pack()
        dropDownSeleccion.pack()
        botonGrafica.pack()



        ventana.mainloop()

#adsfgasf
