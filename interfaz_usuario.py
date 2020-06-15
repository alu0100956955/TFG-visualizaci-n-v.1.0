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


        # --------------------------Funciones para las distintas opciones ---------------------------------------
        def show(grafica, elegidos, ejeX, ejeY, dataS):
            dataS.setSeleccionados(elegidos)
            dataS.setSeleccionEjeX(ejeX)
            dataS.setSeleccionEjeY(ejeY)
            Mediador.show(grafica, dataS)

        def getBotonShow(): # La funcion que Añade el boton para hacer la grafica | esta separado porque se puede pedir dentro de seleccionados o si es un mapa se pide solo
            # En la funcion recibe la opcion de grafica (int), el array con los elementos elegidos para mostrar (array), y la url de la fuente de datos para obtener el dataset (string)
            #botonGrafica.pack(pady=20)
            #seleccionEjeX.append("vacio")   # Esto lo hago por los mapas ya que se muestra directamente el boton y si no añado (appned) un elemento peta 
            #seleccionEjeY.append("vacio")
            botonGrafica.grid(column = 2, row = 24)

        # Metodo para añadir a la ventana el dropdownList para quel usuario escoja los elementos que quiere seleccionar
        def getSeleccionados(event):
            #opcionesPack = dropDownSeleccion.winfo_ismapped() # Asi pregunto si ya esta metido dentro de la ventana antes de volver a declararlo
            #dataS = Mediador.getParse(fuenteDatos.get()).getDataset()
            nonlocal dataS
            #label4.pack()
            #label3.pack(pady=10)
            label3.grid(column = 2, row = 18)
            #opciones = dataS.getOpciones()
            #ejes = dataS.getOpcionesEje()
            opciones_ = dataS.getOpciones()
            # AQUI HAY QUE CONTROLAR QUE EJES SE REPRESENTARAN, de forma que si es una de tipo distibucion hay que ocultar el ejeX y cambiarlo por la opcionesde distribucion
            # En las opciones de distribucion ocurre como seleccionado que seran varios

            seleccionado.set(opciones[0])   # le asigno el primero como default
            
            nonlocal dropDownSeleccion
            dropDownSeleccion["values"] = [*opciones_];
            dropDownSeleccion.bind("<<ComboboxSelected>>", addSeleccion)
            
            #opcionesEjes.bind("<<comboboxselected>>", elegirEje)

            labelEspacio.grid(column = 2, row = 13 )
            labelEjeX.grid(column = 2, row = 14)
            labelEjeY.grid(column = 2, row = 16)
            #if (dropDownSeleccion.winfo_ismapped() == False): #Esto no funciona ya que declaro arriba el dropdown asique cuenta como nuevo
            #if ( dropDownSeleccion.winfo_ismapped() == False):
                #dropDownSeleccion.pack()
            dropDownSeleccion.grid(column = 2, row = 19 )
            opcionesEjesX.grid(column = 2, row = 15)
            opcionesEjesY.grid(column = 2, row = 17) # esto es para elegir que representara el eje
                #opcionesPack = True;
            # Si ha seleccionado la grafica tipo box quito el eje X y añado otras opciones de representacion
            if(opcionesEjesX.winfo_ismapped() & (eleccionDropdown(tipoGrafica.get()) == 7)):
                opcionesEjesX.grid_remove()
                labelEjeX.grid_remove()


        # Metodo para añadir el poder escoger los elementos para las distribuciones
        def distribuciones():
            print("Sin terminar")
            labelOpcionesDistribuciones.grid(column = 2, row = 14)
            if(opcionesDistribucion.winfo_ismapped() == False):# Para no añadir duplicados en la interfaz
                opcionesDistribucion.grid(column = 2, row = 15) # sustituira la posición de elección del eje X


        # Metodo para añadir un elemento para representar 
        def addDistribucion():
            print("Sin terminar | sera como el addSeleccion")


        def graficasNuevo(event):
            nonlocal dataS
            parse = Mediador.getParse(eleccionDropdown(dropdownFuenteDatos.get()))    # le pasamos la eleccion del usuario sobre la fuente de datos
            dataS = parse().getDataset()
            tipoGrafica.grid(column = 2, row = 3 )
            tipos = ["1:  Linea Terminal", "2: Linea html", "3: Linea navegador", "4: Barras navegador", "5: mapa navegador", "6: dispersion navegador", "7: box html"]
            tipoGrafica["values"] = [*tipos]
            # Para actualizar o implementar valores a las opciones de los ejes
            ejes = dataS.getOpcionesEje()
            opcionesEjesY["values"] = [*ejes]
            opcionesEjesX["values"] = [*ejes]
            limpiarSeleccionado()

        #Para saber de las elecciones de los dropdown list cual es la que escogio el usuario
        def eleccionDropdown(eleccion):
            return int(eleccion[0])

        # Metodo para añadir el elemento seleccionado por el usuario
        def addSeleccion(event):
            elegidos.append(dropDownSeleccion.get())
            elementosSeleccionados.configure(state="normal")    # Lo habilito de nuevo para edicion por que sino no me deja añadir el texto
            elementosSeleccionados.insert(tk.INSERT, dropDownSeleccion.get())
            elementosSeleccionados.insert(tk.INSERT, '\n')
            lContSeleccionados.config(text=len(elegidos))
            lSeleccionados.grid(column = 2, row = 20 )
            lContSeleccionados.grid(column = 3, row = 20 )
            elementosSeleccionados.grid(column = 2, row = 22)
            botonQuitarSeleccionado.grid(column = 3, row = 22)

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

        # Metodo para limpiar los seleccionados por si se cambia de fuente de datos
        def limpiarSeleccionado():
            while (len(elegidos) > 0 ):
                elegidos.pop()
            elementosSeleccionados.configure(state="normal")    # Lo habilito de nuevo para edicion por que sino no me deja añadir el texto
            elementosSeleccionados.delete('1.0', END)
            elementosSeleccionados.configure(state="disabled")

        #Para poder escoger las opciones del eje Y
        def elegirEjeY(event):
            #eleccionEje = opcionesEjes.get()
            #if (len(seleccionEjeY) > 0):    # Si ya tiene un eje guardado lo saco para poder guardar la nueva eleccion
            #    while( len(seleccionEjeY) > 0):
            #        seleccionEjeY.pop() 
            #seleccionEjeY.append(opcionesEjesY.get())
            #opcionesEjesY = ttk.Combobox(state = "disabled")    # Al seleccionar hay que desactivar el dropbox
            #seleccionEjeX[0] = opcionesEjesX.get()
            #print("Se escogio = " + opcionesEjes.get())
            nonlocal seleccionEjeY
            seleccionEjeY = opcionesEjesY.get()

        #Para poder escoger las opciones del eje X
        def elegirEjeX(event):
           #if (len(seleccionEjeX) > 0):
            #    while( len(seleccionEjeY) > 0):
            #        seleccionEjeX.pop()
            #seleccionEjeX.append(opcionesEjesX.get())
            nonlocal seleccionEjeX
            seleccionEjeX = opcionesEjesX.get()


        #--------------------- Declaracion de los elementos para la ventana ---------------------------
        urlConfirmados = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
        ventana = tk.Tk()
        ventana.geometry('430x600') # Cambiar las dimensiones cuando se mejore los elementos
        grafica = IntVar() # Variabla para controlar la opcion seleccionada por el usuario
        fuenteDatos = StringVar()
        dataS = Dataset('default')
        #dataS = [] # Lo hago list por que sino no me guarda el dataset dentro de la funcion

        labelEspacio = tk.Label(ventana, text = "        ")

        # Los radiobutton para el tipo de fuente
        rbCasosConfirmados = Radiobutton(ventana, text="Casos confirmados", variable=fuenteDatos,value= 1, command=graficasNuevo)
        rbSegunda = Radiobutton(ventana, text="Accidentes trafico", variable=fuenteDatos,value=2, command=graficasNuevo)
        rbParo= Radiobutton(ventana, text="Paro España", variable=fuenteDatos,value=3, command=graficasNuevo)
        #rbSegunda.configure(state="disabled")   #Lo desactivo mientras mejoro el sistema, despues me pongo arreglar el parse

        dropdownFuenteDatos= ttk.Combobox(state = "readonly")
        dropdownFuenteDatos.bind("<<ComboboxSelected>>",graficasNuevo)


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
        labelEjeX = tk.Label(ventana, text = "Escoge el eje X" )
        opcionesEjesX= ttk.Combobox(state = "readonly")
        opcionesEjesX.bind("<<ComboboxSelected>>", elegirEjeX)

        labelEjeY = tk.Label(ventana, text = "Escoge el eje Y" )
        opcionesEjesY= ttk.Combobox(state = "readonly")
        opcionesEjesY.bind("<<ComboboxSelected>>", elegirEjeY)

        #Para lo que seleccione el usuario de los ejes
        seleccionEjeY = ""
        seleccionEjeX = ""


        # ------------ Elementos de getGrafica --------------
        
        label2 = tk.Label(ventana, text="Seleccione el tipo de gráfica")
        tipoGrafica= ttk.Combobox(state = "readonly")
        #tipoGrafica.bind("<<ComboboxSelected>>",lambda event: getSeleccionados(dropDownSeleccion.winfo_ismapped(), dataS ))
        tipoGrafica.bind("<<ComboboxSelected>>",getSeleccionados)


        # Elementos de getBotonShow
        botonGrafica = Button(ventana, text ="Hacer grafica" , pady= 5, command = lambda: show( eleccionDropdown(tipoGrafica.get()),elegidos,seleccionEjeX,seleccionEjeY,dataS)) # El boton de graficas

        #/////////////////////////////////////////////////   ELEMENTOS INICIALES DE LA VENTANA   //////////////////////////////////////////////////

        label1.grid(column = 2, row = 0)
        # Los radio buttons
        #rbCasosConfirmados.grid(column = 3, row = 1)
        #rbSegunda.grid(column = 3, row = 2)
        #rbParo.grid(column = 4, row = 1)
        tipos = ["1:  Casos de covid confirmados", "2: Accidentes de trafico", "3: Paro en españa"]
        dropdownFuenteDatos["values"] = [*tipos]
        dropdownFuenteDatos.grid(column = 2, row = 1)
        labelEspacio.grid(column = 2, row = 2 )

        elegidos = [] # se añadira un elemento por cada vez que el usuario lo indique ( habra que controlar los duplicados)

        # El dropdownList para elegir que seleccionar
        lSeleccionados = tk.Label(ventana, text="Cantidad de seleccionados")
        lContSeleccionados = tk.Label(ventana)
        label4 = tk.Label(ventana, text="funciona la funcion")

        rbCasosConfirmados.deselect()
        rbSegunda.deselect()

        ventana.mainloop()

#adsfgasf
