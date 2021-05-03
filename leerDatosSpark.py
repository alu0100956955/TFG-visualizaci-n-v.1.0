#!/usr/bin/env python
# -*- coding: utf-8 -*-
import findspark
import pyspark
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import VectorIndexer, StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import SparkSession
import pandas as pd
import numpy as np
from clases_base import Parse
from dataset import Dataset
import datetime
from datetime import datetime



class ParsePokemonSpark:

    # Primera parte para foramr el dataframe
    def __init__(self):# inicializo la sesión para poder ejecutar comandos de spark como si estubiese en la terminal
        #findspark.init("C:\Spark\spark-3.0.0-preview2-bin-hadoop2.7")# La ruta correcta
        #spark = SparkSession.builder \
        #   .master("local") \
        #   .appName("saprk") \
        #   .config("spark.executor.memory", "2gb") \
        #   .getOrCreate()
        spark= SparkSession.builder.appName('abc').getOrCreate()  # Lo hago más simple para ver si no salta el error

        self.df = spark.read.option("header","true").csv("data/pokemon.csv")
        self.df = df.withColumn("HP",self.df.HP.astype("Int"))
        self.df = self.df.withColumn("Attack",self.df.Attack.astype("Int"))
        self.df = self.df.withColumn("Defense",self.df.Defense.astype("Int"))
        self.df = self.df.withColumn("SP_Atk",self.df.Sp_Atk.astype("Int"))
        self.df = self.df.withColumn("Sp_Def",self.df.Sp_Def.astype("Int"))
        self.df = self.df.withColumn("Speed",self.df.Speed.astype("Int"))

        labelIndexer = StringIndexer(inputCol="Type1", outputCol="label")
        self.df = labelIndexer.fit(self.df).transform(self.df)

    def getDataset(self):
        return self.df



# Fin