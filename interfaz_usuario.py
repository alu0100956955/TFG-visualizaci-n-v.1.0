#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext as st
from mediador import Mediador
from dataset import Dataset
#from tkinter import ttkwidgets


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
        
        # El orden de como seran llamas estas funciones segun la interacion con el usuario esta indicada en el comentario encima del metodo

        # 1. PRIMERO Metodo para cuando se escoja la fuente de datos
        def graficasNuevo(event):
            nonlocal dataS
            parse = Mediador.getParse(eleccionDropdown(dropdownFuenteDatos.get()))    # le pasamos la eleccion del usuario sobre la fuente de datos
            dataS = parse().getDataset()
            #dataS.setNumeroFuenteDatos()
            label2.grid(column = 2, row = 4)
            tipoGrafica.grid(column = 2, row = 5 )
            tipos = dataS.getTiposGraficas()
            tipoGrafica["values"] = [*tipos]
            # Para actualizar o implementar valores a las opciones de los ejes
            ejes = dataS.getOpcionesEje()
            opcionesEjesY["values"] = [*ejes]
            opcionesEjesX["values"] = [*ejes]
            #opcionesDistribucion["values"] = ["1: Combinado","2: Sumado"]
            limpiarSeleccionado()


        #2. SEGUNDO Metodo para añadir a la ventana el dropdownList para quel usuario escoja los elementos que quiere seleccionar
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
            eleccionUsuario = eleccionDropdown(tipoGrafica.get())
            nonlocal dropDownSeleccion
            dropDownSeleccion["values"] = [*opciones_];
            #dropDownSeleccion.set_completion_list(opciones_)   # intento de dropdown con autocomplete
            dropDownSeleccion.bind("<<ComboboxSelected>>", addSeleccion)
            
            #opcionesEjes.bind("<<comboboxselected>>", elegirEje)

            labelEspacio.grid(column = 2, row = 13 )
            if(eleccionUsuario < 7):
                labelEjeX.grid(column = 2, row = 14)
                opcionesEjesX.grid(column = 2, row = 15)
            
            
            labelEjeY.grid(column = 2, row = 16)
            opcionesEjesY.grid(column = 2, row = 17) # esto es para elegir que representara el eje
            botonTodasOpciones.grid(column = 3, row = 19)
            dropDownSeleccion.grid(column = 2, row = 19 )
                #opcionesPack = True;
            # Si ha seleccionado la grafica tipo box quito el eje X y añado otras opciones de representacion
            # TO DO, mejorar la forma en la que oculto los elementos
            
            if(opcionesEjesX.winfo_ismapped() & ((eleccionUsuario == 7) or (eleccionUsuario == 8) or (eleccionUsuario == 9)) ):
                opcionesEjesX.grid_remove()
                labelEjeX.grid_remove()

        # 4. CUARTO metodo para poner en la ventana el boton para mostrar la grafica
        def getBotonShow(): # La funcion que Añade el boton para hacer la grafica | esta separado porque se puede pedir dentro de seleccionados o si es un mapa se pide solo
            # En la funcion recibe la opcion de grafica (int), el array con los elementos elegidos para mostrar (array), y la url de la fuente de datos para obtener el dataset (string)
            #botonGrafica.pack(pady=20)
            #seleccionEjeX.append("vacio")   # Esto lo hago por los mapas ya que se muestra directamente el boton y si no añado (appned) un elemento peta 
            #seleccionEjeY.append("vacio")
            botonGrafica.grid(column = 2, row = 24)

        # 5. QUINTO Metodo para llamar al metodo show y mostrar la grafica
        def show(grafica, elegidos, ejeX, ejeY, dataS):
            dataS.setSeleccionados(elegidos)
            dataS.setSeleccionEjeX(ejeX)
            dataS.setSeleccionEjeY(ejeY)
            Mediador.show(grafica, dataS)

        # CAmbiar para los histogramas
        # Metodo para añadir el poder escoger los elementos para las distribuciones
        def distribuciones():
            print("Sin terminar")
            #labelOpcionesDistribuciones.grid(column = 2, row = 14)
            #if(opcionesDistribucion.winfo_ismapped() == False):# Para no añadir duplicados en la interfaz
            #    opcionesDistribucion.grid(column = 2, row = 15) # sustituira la posición de elección del eje X


        # Metodo para guardar la eleccion del tipo de histograma 
        def tipoHistograma(event):
            print("Sin terminar | sera como el addSeleccion")
            nonlocal dataS
            #dataS.setOpcionDistribucion(opcionesDistribucion.get())

        

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
            nonlocal opcionesEjesX, opcionesEjesY , tipoGrafica
            while (len(elegidos) > 0 ):
                elegidos.pop()
            elementosSeleccionados.configure(state="normal")    # Lo habilito de nuevo para edicion por que sino no me deja añadir el texto
            elementosSeleccionados.delete('1.0', END)
            elementosSeleccionados.configure(state="disabled")
            opcionesEjesX.set('')
            opcionesEjesY.set('')
            tipoGrafica.set('')

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

        # Metodo para seleccionar todas las opciones
        def todasLasOpciones():
            nonlocal dataS
            opciones = dataS.getOpciones()# Saco todas las opciones del dataset
            lContSeleccionados.config(text=len(opciones))
            elementosSeleccionados.configure(state="normal")
            for i in opciones:  # Añado todas las opciones
                elegidos.append(i)
                elementosSeleccionados.insert(tk.INSERT, i)
                elementosSeleccionados.insert(tk.INSERT, '\n')

            lSeleccionados.grid(column = 2, row = 20 )
            lContSeleccionados.grid(column = 3, row = 20 )
            elementosSeleccionados.grid(column = 2, row = 22)
            botonQuitarSeleccionado.grid(column = 3, row = 22)
            botonQuitarTodos.grid(column = 3, row = 21)
            elementosSeleccionados.configure(state="disabled")  # no quiero que el usuario escriba es para mostrar los elementos que han sido seleccionados
            getBotonShow()


        # Metodo para quitar todos los elementos seleccionados
        def quitarTodasOpciones():
            
            if (len(elegidos) > 0 ):
                print("Metodo para quitar todas las opciones")
                elegidos.clear()    # Para vaciar al completo el array de elegidos
                elementosSeleccionados.configure(state="normal")    # Lo habilito de nuevo para edicion por que sino no me deja añadir el texto
                elementosSeleccionados.delete('1.0', END)   # Como lo limpia todo no hace falta que haga nada más
                elementosSeleccionados.configure(state="disabled")
                lContSeleccionados.config(text=0)

        # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
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

        # --------------- Elementos para los histogramas -----------------
        labelOpcionesDistribuciones = ttk.Label(ventana, text = "Agrupación datos histograma")
        #opcionesDistribucion = ttk.Combobox("<<ComboboxSelected>>", tipoHistograma)

        # --------------- Elementos de getSeleccionados ---------------
        opciones = [''] # La dejo vacia al princio para que no salte error al declarar el OptionMenu
        seleccionado = StringVar(ventana)   # la variable encargado despues de almacenar lo que seleccione el usuario
        label3 = tk.Label(ventana, text="Selecciona los elementos a representar" )
        #dropDownSeleccion = OptionMenu(ventana, seleccionado, *opciones, command=addSeleccion)
        dropDownSeleccion = ttk.Combobox(state = "readonly")    # Drop down list que contendra todas las opciones que puede seleccionar el usuario
        botonTodasOpciones = Button(ventana, text ="Seleccionar todas las opciones" , pady= 5, command = todasLasOpciones)  # Boton para añadir todas las opciones disponibles
        botonQuitarTodos = Button(ventana, text ="Quitar todas las opciones" , pady= 5, command = quitarTodasOpciones)
        #box_value = tk.StringVar() # Caja para el nuevo dropdownlist con busqueda
        #dropDownSeleccion = tkentrycomplete.AutocompleteCombobox(textvariable=box_value)   # intento de combobox con autocomplete
        #dropDownSeleccion = AutocompleteCombobox(ventana)   # segundo intento de combobox con autocomplete
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
        tipos = ["1:  Casos de covid confirmados", "2: Accidentes de trafico", "3: Paro en españa", "4: Covid"]
        dropdownFuenteDatos["values"] = [*tipos]
        dropdownFuenteDatos.grid(column = 2, row = 1)
        labelEspacio.grid(column = 2, row = 2 )

        elegidos = [] # se añadira un elemento por cada vez que el usuario lo indique ( habra que controlar los duplicados)

        # El dropdownList para elegir que seleccionar
        lSeleccionados = tk.Label(ventana, text="Cantidad de seleccionados")
        lContSeleccionados = tk.Label(ventana)
        #label4 = tk.Label(ventana, text="funciona la funcion")

        rbCasosConfirmados.deselect()
        rbSegunda.deselect()

        ventana.mainloop()

#Clase para los comboboz que se autocompletan
class AutocompleteCombobox(ttk.Combobox):

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, Tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,Tkinter.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,Tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(Tkinter.INSERT), Tkinter.END)
                        self.position = self.index(Tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(Tkinter.END): # delete the selection
                                self.delete(self.position, Tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, Tkinter.END)
                if event.keysym == "Right":
                        self.position = self.index(Tkinter.END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()
                # No need for up/down, we'll jump to the popup
                # list at the position of the autocompletion

#adsfgasf
