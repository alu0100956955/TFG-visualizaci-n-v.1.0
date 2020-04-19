import tkinter as tk
from tkinter import *
from mediador import Mediador
from dataset import Dataset

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

        # --------------------------Funciones para las distintas opciones ---------------------------------------
        def showGrafica(grafica, seleccionados, urlDatos):
            mediador.show2(grafica, seleccionados, urlDatos)

        def getBotonShow(): # La funcion que Añade el boton para hacer la grafica | esta separado porque se puede pedir dentro de seleccionados o si es un mapa se pide solo
            # En la funcion recibe la opcion de grafica (int), el array con los elementos elegidos para mostrar (array), y la url de la fuente de datos para obtener el dataset (string)
            botonGrafica = Button(ventana, text ="Hacer grafica" , pady= 5, command = lambda: Mediador.show( grafica.get(),elegidos,fuenteDatos.get()))
            botonGrafica.pack(pady=20)

        # Metodo para añadir a la ventana el dropdownList para quel usuario escoja los elementos que quiere seleccionar
        def getSeleccionados():

            dataS = Mediador.getParse(fuenteDatos.get()).getDataset()
            #label4.pack()
            label3 = tk.Label(ventana, text="Selecciona los elementos a representar" )
            label3.pack(pady=10)
            seleccionado = StringVar(ventana)   # la variable encargado despues de almacenar lo que seleccione el usuario
            opciones = dataS.getOpciones()
            seleccionado.set(opciones[0])   # le asigno el primero como default
            dropDownSeleccion = OptionMenu(ventana, seleccionado, *opciones, command=addSeleccion)
            dropDownSeleccion.pack()
            getBotonShow()  # para que se añada el boton de


        # Añade a la ventana los radiobutton para escoger el tipo de grafica
        def graficas():

            # Ahora los introduzco en la ventana
            label2.pack(pady=10)
            linea_mat.pack()
            linea_pygal.pack()
            linea_plotly.pack()

        def addSeleccion(seleccion):

            elegidos.append(seleccion)
            lContSeleccionados.config(text=len(elegidos))
            lSeleccionados.pack()
            lContSeleccionados.pack()

        #--------------------- Declaracion de los elementos princiapales ---------------------------
        urlConfirmados = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        ventana = tk.Tk()
        ventana.geometry('400x550')
        grafica = IntVar() # Variabla para controlar la opcion seleccionada por el usuario
        fuenteDatos = StringVar()
        dataS = Dataset('default')


        # Declaro los radiobutton para el tipo de grafica y la etiqueta
        linea_mat = Radiobutton(ventana, text="Linea_mat", variable=grafica,value=1, command=getSeleccionados)
        linea_pygal = Radiobutton(ventana, text="Linea_pygal", variable=grafica,value=2, command=getSeleccionados)
        linea_plotly = Radiobutton(ventana, text="Linea_plotly", variable=grafica,value=3, command=getSeleccionados)
        label2 = tk.Label(ventana, text="Seleccione el tipo de gráfica")



        label1 = tk.Label(ventana, text="MARQUE la fuente de datos")
        #cajaTexto = tk.Entry(ventana)
        # Los radiobutton para el tipo de fuente
        rbCasosConfirmados = Radiobutton(ventana, text="Casos confirmados", variable=fuenteDatos,value='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', command=graficas)
        rbSegunda = Radiobutton(ventana, text="Sin terminar", variable=fuenteDatos,value='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

        #Añadir los elementos a la ventana
        label1.pack()
        #cajaTexto.pack()
        rbCasosConfirmados.pack()
        rbSegunda.pack()

        elegidos = ['Spain','Italy','China','Portugal']# Por ahora lo dejo cableado pero esto dependera de lo que escoga el usuario y se añadira un elemento por cada vez que el usuario lo indique ( habra que controlar los duplicados)

        # El dropdownList para elegir que seleccionar
        #dropDownSeleccion = OptionMenu(ventana, seleccionado, *opciones)
        lSeleccionados = tk.Label(ventana, text="Cantidad de seleccionados")
        lContSeleccionados = tk.Label(ventana)
        label4 = tk.Label(ventana, text="funciona la funcion")

        rbCasosConfirmados.deselect()
        rbSegunda.deselect()

        ventana.mainloop()

#adsfgasf
