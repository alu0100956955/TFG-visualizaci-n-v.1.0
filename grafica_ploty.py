#!/usr/bin/env python
# -*- coding: utf-8 -*-
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
import pandas as pd
from urllib.request import urlopen
#Mis clases
from leerDatos import ParseCasosConfirmados
from clases_base import Grafica
from datetime import datetime
from sklearn import model_selection, linear_model

# El resultado de plotly es un html

class auxiliar():
    def comprobarDias(data, eleccion):
        if (eleccion == "Dias"):
            diasFormateado = []
            for i in data:
                diasFormateado.append(datetime.strptime(i,'%m/%d/%y'))
            return diasFormateado
        return data #Si no es la elección dias devolvera el conjunto de datos igual

class Barras_plotly(Grafica):

    def show(data):
        #paises = ['Spain','Italy','China','Portugal']
        seleccionados =  data.getSeleccionados()
        fig = go.Figure()
        for selec in seleccionados:
            #ejeX = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeX(),selec), data.getSeleccionEjeX())
            #ejeY = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeY(),selec), data.getSeleccionEjeY())
            ejeX = data.getEje(data.getSeleccionEjeX(),selec)
            ejeY = data.getEje(data.getSeleccionEjeY(),selec)

            fig.add_trace(go.Bar(y = data.getEje(data.getSeleccionEjeY(),selec), name = selec))
        #fig.update_layout(title = 'Casos confirmados', xaxis_title="fecha",yaxis_title="Numero de casos")
        fig.update_layout(title = data.getTitle())
        # range(data.getEjeX().size)
        ticksy = []
        for i in range(len(data.getEje(data.getSeleccionEjeX(),seleccionados[0]))):    # Que hace un 0 ahí??
            ticksy.append(i)
        # Para cambiar el eje X
        fig.update_layout(xaxis = dict(title=data.getSeleccionEjeX(), tickmode = 'array', tickvals =ticksy , 
                                       ticktext = Grafica.espaciar(data.getEje(data.getSeleccionEjeX(),seleccionados[0])) ),
                         yaxis=dict(title=data.getSeleccionEjeY())  )
        fig.show()


# TO DO: arreglar el ejeX
#  Pillar el titulo del parse
class Lineas_plotly(Grafica):

    def show(data):
        #paises = ['Spain','Italy','China','Portugal']
        seleccionados = data.getSeleccionados()
        fig = go.Figure()

        for selec in seleccionados:
            #ejeX = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeX(),selec), data.getSeleccionEjeX())
            #ejeY = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeY(),selec), data.getSeleccionEjeY())
            ejeX = data.getEje(data.getSeleccionEjeX(),selec)
            ejeY = data.getEje(data.getSeleccionEjeY(),selec)
            ejeX,ejeY = Lineas_plotly.sort(ejeX,ejeY)
            fig.add_trace(go.Scatter(x = ejeX, y = ejeY, name = selec))
        #fig.update_layout(title = 'Casos confirmados', xaxis_title="fecha",yaxis_title="Numero de casos")
        #fig.update_layout(xaxis_title=l.ejeX())
        #fig.write_html('output/lineas_ploty.html', auto_open=True)   # para guardar la grafica en un html
        fig.update_layout(title = data.getTitle(),xaxis=dict(title=data.getSeleccionEjeX()),yaxis=dict(title=data.getSeleccionEjeY()))
        #ticksy = []
        #for i in range(data.getEje("Dias",0).size):   # Este es el eje X por eso pongo Dias
        #    ticksy.append(i)
        # Para cambiar los valores del eje X
        #fig.update_layout(xaxis = dict( tickmode = 'array', tickvals =ticksy , ticktext = Grafica.espaciar(data.getEje("Dias",0))))
        fig.show()

    def sort(ejex,ejey): 
        # https://www.programiz.com/python-programming/methods/built-in/sorted
        if(isinstance(ejex[0],int) or isinstance(ejex[0],float)  ):# Si es un int o float hay que ordenar
            ejex, ejey = (list(t) for t in zip(*sorted(zip(ejex, ejey))))

        if( ejex.dtype == 'int64'): # TODO comprar con los otros typos de numeros
            orden = ejex.argsort()   
            ejex = ejex[orden]
            ejey = ejey[orden]
        
        return ejex, ejey

    # Metodo para comprobar si la eleccion del eje es de tipo dia, para arreglar el tipo de dato
    


class Scatter_plotly(Grafica):

    #Si el usuario escoge un eje que no es numerico el scatter sera como un histograma, asique tengo que hacer un metodo para que
    # guarde la cantidad de casos distintos y cuantas veces por cada caso
    #https://matplotlib.org/3.2.2/gallery/lines_bars_and_markers/scatter_with_legend.html#sphx-glr-gallery-lines-bars-and-markers-scatter-with-legend-py
    def show(data):
        seleccionados = data.getSeleccionados()
        fig = go.Figure()
        valoresX = [] # contendra todos los valores de todos los elementos seleccionados del eje X
        valoresY = [] # contendra todos los valores de todos los elementos seleccionados del eje Y
        for selec in seleccionados:
            #ejeX = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeX(),selec), data.getSeleccionEjeX())
            #ejeY = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeY(),selec), data.getSeleccionEjeY())
            ejeX = data.getEje(data.getSeleccionEjeX(),selec)
            ejeY = data.getEje(data.getSeleccionEjeY(),selec)
            valoresX.extend(ejeX)
            valoresY.extend(ejeY)

            fig.add_trace(go.Scatter(x = ejeX, y = ejeY, mode='markers', name = selec, marker= dict( size = 16, colorscale = 'Viridis')))
            # Falta añadir la linea de regresion
        regresion_x,regresion_y = Scatter_plotly.regresionPoints(valoresX,valoresY)
        fig.add_trace(go.Scatter(x = regresion_x , y = regresion_y))
        #print(x)
        #print(y)
        fig.update_layout(title = data.getTitle(), xaxis_title= data.getSeleccionEjeX(), yaxis_title= data.getSeleccionEjeY())

        fig.show()

    #https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html
    # a contendra el array de valores de X
    # b  contendra el array de valores de Y
    def regresionPoints(x,y):
        entrenamientoX, validacionX, entrenamientoY, validacionY = model_selection.train_test_split(x, y) #, test_size=0.25, train_size=0.75
        model = linear_model.LinearRegression()
        #entrenamientoY.reshape(-1,1)
        entrenamientoX_np = np.array(entrenamientoX).reshape((-1,1))
        model.fit(entrenamientoX_np,entrenamientoY)    # Entreno el modelo
        validacionX_np = np.array(validacionX).reshape((-1,1))
        prediccion = model.predict(validacionX_np)
        #print(prediccion)
        return validacionX, prediccion


# Esta hecho exclusivamente para data que contenga todos los paises si no fallara
class Mapa_plotly(Grafica):

    # scope (enumerated: "world" | "usa" | "europe" | "asia" | "africa" | "north america" | "south america" ) default: "world"

    def show(data):
        # El Json que contiene los paises
        with open('data/countries.json') as file:
            countries = json.load(file)

        id = [] # Los id de cada pais correspondientes a los del json para que se represente correctamente cada dato
        valores = []
        nombrePais = [] # El nombre del pais segun el fichero json ( para ver que nombre le asigna ya que hay paises que no me los encuentra)
        maximo = 0 #El valor maximo para el rango 
        #for pais in data.getOpciones():
        for pais in countries['features']:
            nombre = pais['properties']['SOVEREIGNT'] # Este es el nombre del pais
            if(data.existeElemento(nombre) == False):
                continue
                
            nombrePais.append(nombre)
            # Hay que controlar si el nombre es correcto
            x = data.getEje("Cantidad de contagios",nombre)
            id.append(pais['id'])
            valores.append(x[-1]) # EL -1 es para sacar el ultimo elemento de la lista que es el del ultimo dia
            if(x[-1] > maximo):
                maximo = x[-1]

        df = pd.DataFrame({"id":id,"Casos Confirmados":valores,"Pais":nombrePais}) # El nombre para cada uno determinara lo que se vera al pasar el raton por cada pais

        #fig = go.Figure(go.Scattergeo())

        fig = px.choropleth(df, geojson=countries, locations='id', color='Casos Confirmados',
                                   color_continuous_scale="Viridis",
                                   range_color=(0, maximo),
                                   labels={'Casos':'Casos confirmados covid'}
                                  )

        fig.update_geos(
            projection_type="natural earth",
            showcountries=True, countrycolor="Purple",
            showland=True, landcolor="LightGreen",
            showocean=True, oceancolor="LightBlue"
        )
        fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})

        fig.show()

    #Si el nombre que esta registrado en el json es correcto devuelve el nombre que se le paso, en caso contrario pasara el que corresponda
    def nombreCorrecto(nombre):
        # Por ahora solo hay un nombre que es el de US, para poder admitir multiples nombres meter un dicionario
        if (nombre == ""):
            return "US1"
        return nombre

    
class Box_plotly(Grafica):

    def show(data):
        seleccionados = data.getSeleccionados()
        #dataframe = pd.DataFrame({})
        dataframe = pd.DataFrame(columns= ['Seleccionados', data.getSeleccionEjeY()])
        ejeY = []
        for selec in seleccionados:
            #ejeY = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeY(),selec), data.getSeleccionEjeY())
            ejeY.append( data.getEje(data.getSeleccionEjeY(),selec).tolist())
            #fig = px.box(data.getEje(data.getSeleccionEjeY(),selec),y=data.getSeleccionEjeY()) 
            #dataframe[selec] = data.getEje(data.getSeleccionEjeY(),selec)
            
            #ejeY = data.getEje(data.getSeleccionEjeY(),selec)
            #for i in range (len(ejeY)):
            #    dataframe.loc[i] = selec, ejeY[i]

        for i in range(len(seleccionados)):

            dataframe.insert(i,seleccionados[i], data.getEje(data.getSeleccionEjeY(),seleccionados[i]),True )

        #dataframe.insert(indiceColumna,nombreColumna,datos,True)  # Para insertar una columna

        #dataframe = pd.DataFrame({ "Seleccionado":seleccionados , data.getSeleccionEjeY():ejeY })
        print(dataframe)
        fig = px.box(dataframe, x=seleccionados, y=data.getSeleccionEjeY())   
        fig.update_layout(title = data.getTitle(),xaxis=dict(title=data.getSeleccionEjeX()),yaxis=dict(title=data.getSeleccionEjeY()))
        fig.show()

# https://www.tutorialspoint.com/plotly/plotly_distplots_density_and_error_bar_plot.htm
# https://plotly.com/python/distplot/
class Histograma_plotly(Grafica):

    def show(data):
        seleccionados = data.getSeleccionados()
        dataframe = pd.DataFrame({})
        ejeY = []
        for selec in seleccionados:
            #ejeY = auxiliar.comprobarDias(data.getEje(data.getSeleccionEjeY(),selec), data.getSeleccionEjeY())
            #ejeY.append( data.getEje(data.getSeleccionEjeY(),selec))
            #fig = px.box(data.getEje(data.getSeleccionEjeY(),selec),y=data.getSeleccionEjeY()) 
            dataframe[selec] = data.getEje(data.getSeleccionEjeY(),selec)

        #dataframe = pd.DataFrame({ "Seleccionado":seleccionados , data.getSeleccionEjeY():ejeY })

        fig = px.histogram(dataframe,x=seleccionados[0])   
        fig.show()

#asdfasdfasd
