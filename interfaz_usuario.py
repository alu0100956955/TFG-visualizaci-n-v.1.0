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

        #opcionesPack = False # Esta variable es para controlar si ya esta dentro el optionMenu, debido a que puede cambiar seguna la grafica y tengo que redeclararla para evitar que se añada multiples veces a la ventana

        # --------------------------Funciones para las distintas opciones ---------------------------------------
        def showGrafica(grafica, seleccionados, urlDatos):
            mediador.show2(grafica, seleccionados, urlDatos)

        def getBotonShow(): # La funcion que Añade el boton para hacer la grafica | esta separado porque se puede pedir dentro de seleccionados o si es un mapa se pide solo
            # En la funcion recibe la opcion de grafica (int), el array con los elementos elegidos para mostrar (array), y la url de la fuente de datos para obtener el dataset (string)
            botonGrafica.pack(pady=20)

        # Metodo para añadir a la ventana el dropdownList para quel usuario escoja los elementos que quiere seleccionar
        def getSeleccionados():
            dataS = Mediador.getParse(fuenteDatos.get()).getDataset()
            #label4.pack()
            label3.pack(pady=10)
            opciones = dataS.getOpciones()
            seleccionado.set(opciones[0])   # le asigno el primero como default
            dropDownSeleccion = OptionMenu(ventana, seleccionado, *opciones, command=addSeleccion)
            if (dropDownSeleccion.winfo_ismapped() == False):
                dropDownSeleccion.pack()
                #opcionesPack = True;


            getBotonShow()  # para que se añada el boton de


        # Añade a la ventana los radiobutton para escoger el tipo de grafica
        def graficas():
            label2.pack(pady=10)
            linea_mat.pack()
            linea_pygal.pack()
            linea_plotly.pack()
            barras_plotly.pack()
            mapa_pygal.pack()
            scatter_plotly.pack()

        def addSeleccion(seleccion):

            elegidos.append(seleccion)
            lContSeleccionados.config(text=len(elegidos))
            lSeleccionados.pack()
            lContSeleccionados.pack()

        #--------------------- Declaracion de los elementos para la ventana ---------------------------
        urlConfirmados = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        ventana = tk.Tk()
        ventana.geometry('400x550')
        grafica = IntVar() # Variabla para controlar la opcion seleccionada por el usuario
        fuenteDatos = StringVar()
        dataS = Dataset('default')


        # Los radiobutton para el tipo de fuente
        rbCasosConfirmados = Radiobutton(ventana, text="Casos confirmados", variable=fuenteDatos,value='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv', command=graficas)
        rbSegunda = Radiobutton(ventana, text="Accidentes trafico", variable=fuenteDatos,value='data/muertos_en_accidentes_de_trafico.csv', command=graficas)


        # Elementos de getGrafica
        # Declaro los radiobutton para el tipo de grafica y la etiqueta
        linea_mat = Radiobutton(ventana, text="Linea_mat", variable=grafica,value=1, command=getSeleccionados)
        linea_pygal = Radiobutton(ventana, text="Linea_pygal", variable=grafica,value=2, command=getSeleccionados)
        linea_plotly = Radiobutton(ventana, text="Linea_plotly", variable=grafica,value=3, command=getSeleccionados)
        barras_plotly = Radiobutton(ventana, text="Linea_mat", variable=grafica,value=4, command=getSeleccionados)
        mapa_pygal = Radiobutton(ventana, text="Linea_pygal", variable=grafica,value=5, command=getBotonShow) # Como no hay que seleccionar pais le pongo el boton de representar directamente
        scatter_plotly = Radiobutton(ventana, text="Linea_plotly", variable=grafica,value=6, command=getSeleccionados)
        label2 = tk.Label(ventana, text="Seleccione el tipo de gráfica")

        # Elementos de getSeleccionados
        opciones = [''] # La dejo vacia al princio para que no salte error al declarar el OptionMenu
        seleccionado = StringVar(ventana)   # la variable encargado despues de almacenar lo que seleccione el usuario
        label3 = tk.Label(ventana, text="Selecciona los elementos a representar" )
        dropDownSeleccion = OptionMenu(ventana, seleccionado, *opciones, command=addSeleccion)

        label1 = tk.Label(ventana, text="MARQUE la fuente de datos")
        #cajaTexto = tk.Entry(ventana)

        # Elementos de getBotonShow
        botonGrafica = Button(ventana, text ="Hacer grafica" , pady= 5, command = lambda: Mediador.show( grafica.get(),elegidos,fuenteDatos.get()))

        # ---------------------- Añadimos los elementos a la ventana -----------------------------
        label1.pack()
        rbCasosConfirmados.pack()
        rbSegunda.pack()

        # Por ahora lo dejo cableado pero esto dependera de lo que escoga el usuario
        #elegidos = ['Spain','Italy','China','Portugal']
        elegidos = [] # se añadira un elemento por cada vez que el usuario lo indique ( habra que controlar los duplicados)

        # El dropdownList para elegir que seleccionar
        #dropDownSeleccion = OptionMenu(ventana, seleccionado, *opciones)
        lSeleccionados = tk.Label(ventana, text="Cantidad de seleccionados")
        lContSeleccionados = tk.Label(ventana)
        label4 = tk.Label(ventana, text="funciona la funcion")

        rbCasosConfirmados.deselect()
        rbSegunda.deselect()

        ventana.mainloop()

#adsfgasf
