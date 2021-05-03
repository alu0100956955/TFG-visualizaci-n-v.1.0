from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import VectorIndexer, StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.regression import LinearRegression
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import RegressionEvaluator
import findspark
import pyspark
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt


class ClasificacionSpark:

    def show(data):
        print("clasificacion spark")
        seleccionados = data.getSeleccionados()
        ejeX = data.getSeleccionEjeX()
        ejeY = data.getSeleccionEjeY()

        assembler = VectorAssembler( inputCols=[opcion1, opcion2], outputCol="features")
        dt = DecisionTreeClassifier(labelCol="label", featuresCol="features")
        df = assembler.transform(df4) # LE pongo las features
        train2, test2 = df4.randomSplit([0.7,0.3], seed = 7) # Lo parto en dos cachos
        modeloDt = dt.fit(train2)
        dfT = modeloDt.transform(test2)
