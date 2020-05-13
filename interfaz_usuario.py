#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext as st
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
        def show(grafica, elegidos, eje, dataS):
            dataS.setSeleccionados(elegidos)
            dataS.setSeleccionEje(eje)
            Mediador.show(grafica, dataS)

        def getBotonShow(): # La funcion que Añade el boton para hacer la grafica | esta separado porque se puede pedir dentro de seleccionados o si es un mapa se pide solo
            # En la funcion recibe la opcion de grafica (int), el array con los elementos elegidos para mostrar (array), y la url de la fuente de datos para obtener el dataset (string)
            #botonGrafica.pack(pady=20)
            botonGrafica.grid(column = 2, row = 22)

        # Metodo para añadir a la ventana el dropdownList para quel usuario escoja los elementos que quiere seleccionar
        def getSeleccionados(opcionesPack):
            #opcionesPack = dropDownSeleccion.winfo_ismapped() # Asi pregunto si ya esta metido dentro de la ventana antes de volver a declararlo
            #dataS = Mediador.getParse(fuenteDatos.get()).getDataset()
            parse = Mediador.getParse(fuenteDatos.get())    # le pasamos la eleccion del usuario sobre la fuente de datos
            #dataS = parse().getDataset()    # Le pido el dataset al parse
            dataS.append(parse().getDataset())
            #label4.pack()
            #label3.pack(pady=10)
            label3.grid(column = 2, row = 16)
            opciones = dataS[0].getOpciones()
            ejes = dataS[0].getOpcionesEje()
            seleccionado.set(opciones[0])   # le asigno el primero como default
            #dropDownSeleccion = OptionMenu(ventana, seleccionado, *opciones, command=addSeleccion)
            #dropDownSeleccion = ttk.Combobox( opciones.all())
            dropDownSeleccion["values"] = [*opciones];
            dropDownSeleccion.bind("<<ComboboxSelected>>", addSeleccion)
            opcionesEjes["values"] = [*ejes]
            #opcionesEjes.bind("<<comboboxselected>>", elegirEje)

            labelEspacio.grid(column = 2, row = 13 )
            labelEje.grid(column = 2, row = 14)
            #if (dropDownSeleccion.winfo_ismapped() == False): #Esto no funciona ya que declaro arriba el dropdown asique cuenta como nuevo
            if ( opcionesPack == False):
                #dropDownSeleccion.pack()
                dropDownSeleccion.grid(column = 2, row = 17 )
                opcionesEjes.grid(column = 2, row = 15) # esto es para elegir que representara el eje
                #opcionesPack = True;

            #Para mostrar los seleccionados
            #lSeleccionados.pack(side=tk.LEFT)
            #lContSeleccionados.pack(side=tk.RIGHT)


        # Añade a la ventana los radiobutton para escoger el tipo de grafica
        def graficas():
            labelEspacio.grid(column = 2, row = 3 )
            label2.grid(column = 2, row = 4)
            linea_mat.grid(column = 2, row = 6)
            linea_pygal.grid(column = 2, row = 7)
            linea_plotly.grid(column = 2, row = 8)
            barras_plotly.grid(column = 2, row = 9)
            mapa_plotly.grid(column = 2, row = 10)
            scatter_plotly.grid(column = 2, row = 11)
            box_pygal.grid(column = 2, row = 12)

        # Metodo para añadir el elemento seleccionado por el usuario
        def addSeleccion(event):
            #print(event)
            #seleccion = event
            elegidos.append(dropDownSeleccion.get())
            elementosSeleccionados.configure(state="normal")    # Lo habilito de nuevo para edicion por que sino no me deja añadir el texto
            elementosSeleccionados.insert(tk.INSERT, dropDownSeleccion.get())
            elementosSeleccionados.insert(tk.INSERT, '\n')
            lContSeleccionados.config(text=len(elegidos))
            lSeleccionados.grid(column = 2, row = 18 )
            lContSeleccionados.grid(column = 3, row = 18 )
            elementosSeleccionados.grid(column = 2, row = 20)
            botonQuitarSeleccionado.grid(column = 3, row = 20)

            elementosSeleccionados.configure(state="disabled")  # no quiero que el usuario escriba es para mostrar los elementos que han sido seleccionados
            getBotonShow()  # para que se añada el boton de

        # Para quitar uno de los elementos seleccionados
        def quitarSeleccionado():
            if (len(elegidos) > 0 ):    # Si no hay elementos no se puede hacer pop
                elegidos.pop()  # Le quito el ultimo elemento
                lContSeleccionados.config(text=len(elegidos))   # Actualizo el conteo de elementos seleccionados
                elementosSeleccionados.configure(state="normal")    # Lo habilito de nuevo para edicion por que sino no me deja añadir el texto
                elementosSeleccionados.delete('1.0', END)
                for i in elegidos:# Como me lo elimina todo lo reescribo
                    elementosSeleccionados.insert(tk.INSERT, i)
                    elementosSeleccionados.insert(tk.INSERT, '\n')
                elementosSeleccionados.configure(state="disabled")

        #Para poder escoger las opciones de cada eje
        def elegirEje(event):
            #eleccionEje = opcionesEjes.get()
            seleccionEje.append(opcionesEjes.get())
             #seleccionEjeX[0] = opcionesEjesX.get()
             #print("Se escogio = " + opcionesEjes.get())

        def elegirEjeY(event):
            seleccionEjeY[1] = opcionesEjesY.get()


        #--------------------- Declaracion de los elementos para la ventana ---------------------------
        urlConfirmados = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        ventana = tk.Tk()
        ventana.geometry('380x550') # Cambiar las dimensiones cuando se mejore los elementos
        grafica = IntVar() # Variabla para controlar la opcion seleccionada por el usuario
        fuenteDatos = StringVar()
        #dataS = Dataset('default')
        dataS = []  # Lo hago list por que sino no me guarda el dataset dentro de la funcion

        labelEspacio = tk.Label(ventana, text="        ")

        # Los radiobutton para el tipo de fuente
        rbCasosConfirmados = Radiobutton(ventana, text="Casos confirmados", variable=fuenteDatos,value= 1, command=graficas)
        rbSegunda = Radiobutton(ventana, text="Accidentes trafico", variable=fuenteDatos,value=2, command=graficas)
        rbSegunda.configure(state="disabled")   #Lo desactivo mientras mejoro el sistema, despues me pongo arreglar el parse


        # --------------- Elementos de getSeleccionados ---------------
        opciones = [''] # La dejo vacia al princio para que no salte error al declarar el OptionMenu
        seleccionado = StringVar(ventana)   # la variable encargado despues de almacenar lo que seleccione el usuario
        label3 = tk.Label(ventana, text="Selecciona los elementos a representar" )
        #dropDownSeleccion = OptionMenu(ventana, seleccionado, *opciones, command=addSeleccion)
        dropDownSeleccion = ttk.Combobox(state = "readonly")
        dropDownSeleccion.bind("<<ComboboxSelected>>", addSeleccion)
        opcionesPack = False # Esta variable es para controlar si ya esta dentro el optionMenu, debido a que puede cambiar seguna la grafica y tengo que redeclararla para evitar que se añada multiples veces a la ventana
        label1 = tk.Label(ventana, text="MARQUE la fuente de datos")
        elementosSeleccionados = st.ScrolledText(ventana, height=5, width=20)

        botonQuitarSeleccionado = Button(ventana, text ="Quitar ultimo seleccionado" , pady= 5, command = quitarSeleccionado)

        #Esto tendria que estar en un metodo aparte pero por ahora lo mando junto con la seleccionde elementos
        labelEje = tk.Label(ventana, text = "Escoge el eje Y" )
        opcionesEjes= ttk.Combobox(state = "readonly")
        opcionesEjes.bind("<<ComboboxSelected>>", elegirEje)
        seleccionEje = []



        # ------------ Elementos de getGrafica --------------
        # Declaro los radiobutton para el tipo de grafica y la etiqueta
        linea_mat = Radiobutton(ventana, text="Linea_mat", variable=grafica,value=1, command = lambda: getSeleccionados(dropDownSeleccion.winfo_ismapped()))
        linea_pygal = Radiobutton(ventana, text="Linea_pygal", variable=grafica,value=2, command = lambda: getSeleccionados(dropDownSeleccion.winfo_ismapped()))
        linea_plotly = Radiobutton(ventana, text="Linea_plotly", variable=grafica,value=3, command = lambda: getSeleccionados(dropDownSeleccion.winfo_ismapped()))
        barras_plotly = Radiobutton(ventana, text="Barras_plotly", variable=grafica,value=4, command = lambda: getSeleccionados(dropDownSeleccion.winfo_ismapped()))
        mapa_plotly = Radiobutton(ventana, text="Mapa_plotly", variable=grafica,value=5, command = getBotonShow) # Como no hay que seleccionar pais ni el eje le pongo el boton de representar directamente
        scatter_plotly = Radiobutton(ventana, text="Scatter_plotly", variable=grafica,value=6, command = lambda: getSeleccionados(dropDownSeleccion.winfo_ismapped()))
        box_pygal = Radiobutton(ventana, text="Box_pygal", variable=grafica,value=7, command = lambda: getSeleccionados(dropDownSeleccion.winfo_ismapped()))
        label2 = tk.Label(ventana, text="Seleccione el tipo de gráfica")

        #print("------------------------------------------------------------------")

        # Elementos de getBotonShow
        botonGrafica = Button(ventana, text ="Hacer grafica" , pady= 5, command = lambda: show( grafica.get(),elegidos,seleccionEje[0],dataS[0])) # El boton de graficas

        # ---------------------- Añadimos los elementos principales a la ventana -----------------------------
        #label1.pack()
        #rbCasosConfirmados.pack()
        #rbSegunda.pack()

        label1.grid(column = 2, row = 0)
        rbCasosConfirmados.grid(column = 2, row = 1)
        rbSegunda.grid(column = 2, row = 2)

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
