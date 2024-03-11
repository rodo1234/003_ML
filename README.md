# 003_ML
## Proyecto 3 de Micro 

En este proyecto nos enfocamos en la implementación de tres potentes modelos de clasificación: Regresión Logística, Support Vector Classification (SVC) y XGBoost. Nuestra meta es trascender la mera predicción de precios de acciones, centrándonos en la clasificación de señales de compra y venta sobre de información sobre diferentes intervalos de tiempo. Este enfoque nos capacita para anticipar con precisión si el precio de una acción estará dentro de un rango específico, brindando así una herramienta estratégica para maximizar la ganancia esperada.

## Descripción de Modelos
1. Regresión Logística: Es un algoritmo de clasificación que se utiliza para predecir la probabilidad de una variable dependiente categórica. En la regresión logística, la variable dependiente es una variable binaria que contiene datos codificados como 1 (sí, éxito, etc.) o 0 (no, fracaso, etc.). En otras palabras, el modelo de regresión logística predice P(Y=1) en función de X.

2. Support Vector Classification (SVC): Es un algoritmo de aprendizaje automático que se utiliza en problemas de clasificación y regresión. SVCs son más comúnmente utilizados en problemas de clasificación. Este algoritmo crea un hiperplano o líneas de decisión que separan las clases lo más posible. Los puntos de datos que están más cerca del hiperplano se llaman vectores de soporte.

3. XGBoost: Es una implementación de los árboles de decisión de gradiente potenciado diseñados para la velocidad y el rendimiento. XGBoost es una abreviatura de eXtreme Gradient Boosting. El "Gradient Boosting" se refiere al hecho de que el algoritmo utiliza la técnica de descenso de gradiente para minimizar el error al añadir nuevos modelos.

## Datos de entrada y salida

1. Para nuestras X o datos de salida usamos el precio Close, x_t-n en este caso hasta -3 y el RSI con ventana de 28.
2. Para la Y o datos de salida usamos una condicion para ver si el precio xt era menor para determinar la compra y menor la venta dependiendo del quinto precio en los datos (P_t+5)

### Parámetros por operación

1. Stop Loss Long: Este parámetro establece el nivel de precio al cual se activará una orden de venta para cerrar una posición larga y limitar las pérdidas. (0.01, 0.95)
2.	Take Profit Long: Especifica el nivel de precio al cual se activará una orden de venta para cerrar una posición larga y asegurar las ganancias. (0.01, 0.95)
3.	Stop Loss Short: Determina el nivel de precio al cual se activará una orden de compra para cerrar una posición corta y limitar las pérdidas. (0.01, 0.95)
4.	Take Profit Short: Indica el nivel de precio al cual se activará una orden de compra para cerrar una posición corta y asegurar las ganancias. (0.01, 0.95)
5.	Número de Acciones (n_shares): Este parámetro define la cantidad de acciones a comprar o vender en cada operación. (10, 100)

### Parámetros por función:

#### 1.	Regresión Lineal:
-	Penalty: Tipo de regularización aplicada al modelo para prevenir el sobreajuste y mejorar su generalización. ("elasticnet")
-	C: Representa el inverso de la fuerza de la regularización. (.001, 10)
-	Fit_intercept: Determina si se añade un término de intercepción al modelo, permitiendo que la regresión se ajuste mejor a los datos.  (True, False)
-	Random_state: Se utiliza para controlar la semilla de aleatoriedad en procesos o métodos que involucran operaciones estocásticas, asegurando resultados reproducibles. (42)
-	Solver: Especifica el algoritmo utilizado para encontrar los parámetros del modelo que minimizan la función de costo, influyendo en la eficiencia y precisión de la solución. (“saga”)
-	Max_Iter: Número máximo de iteraciones del algoritmo de optimización para encontrar los parámetros del modelo. (10,000)

#### 2.	SVM:
-	C: Controla la compensación entre un margen de decisión suave y la clasificación correcta de los puntos de entrenamiento. (.001, 10)
-	Gamma: Determina la influencia de un solo punto de entrenamiento. (Scale, Auto)
-	Random_state: Asegura resultados reproducibles al iniciar las semillas de aleatoriedad en procesos estocásticos. (42)
#### 3.	XgBoost:
-	Gamma: Especifica la reducción mínima de pérdida requerida para realizar una partición adicional en un nodo del árbol. (.01, 50)
-	Max_depth: Determina la profundidad máxima de los árboles. (3, 10)
-	Lamda: Es el término de regularización L2 en los pesos. (.01, 10)
-	Alpha: Es el término de regularización L1 en los pesos. (.01, 10)
