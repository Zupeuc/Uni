# README T04 Daniel Zupeuc

La simulación se demora un tiempo en correr, pero despues de unos minutos debería terminar. Al final salen las estadísticas printeadas si corres el módulo simulación. Se pueden quitar los prints y dejarla que retorne los puros parametros de las estadisticas en un diccionario si en el input despues de los diccionarios de las personas se le pone un False:
Ejemplo:
m = Semestre(vendedores, alumnos, funcionarios, False)
m.run()
Si ahí se pone un True, printea los sucesos diarios en la simulación hasta que termina.

# Simulación :

 - La simulación se encuentra dividida en dos clases. La clase Simulacion se dedica a simular el paso de un día en la universidad y la clase semestre de simular el semestre academico completo.
 - Como se me pide simular un semestre academico completo. Asumí que el semestre iba a tener 4 meses y cada mes 22 días hábiles. Para simplificar las cosas no se toman en cuenta los otros días. Para efectos de concha acustica, que se hace solo los viernes, se asume que el viernes es cada 5 día hábil para simplificar las cosas.

# Alcances:

# 1 Entidades:

 - Fueron creadas todas las entidades con sus determinadas características. Este item está casi completo. 
 - Alumnos: Completo
 - Vendedores: Completo a excepción de que no bajan su precio (solo lo suben) y tampoco se van del mercado despues de 20 días sin vender.
 - Funcionarios: Completo
 - Carabineros: Creados con todas sus caracterísiticas y atributos. LLegan cuando son llamados pero se me bugeaba cuando confizcaban a un vendedor. Hay una función creada en Simulación que se llama fiscaliza_paco a cargo de hacer todo este proceso. No alcance a debugearla por lo que solo la dejé expresada y no la implementé finalmente. La función revisa un vendedor al azar en el tiempo determinado, le pide permiso y le da oportunidad de engañarlo. Sin embargo no se implementa lo de revisar los productos.
 - QuickDevil creado según se pide.
 - Productos creados según se pide.

# 2 Eventos programados:

-Todos estos eventos fueron programados en la simulación en la clase "simulacion". Fue completamente logrado.

# 3 Eventos NO programados:

Estos se encuentran en el run() de la clase Semestre en el módulo simulación. Todos fueron implementados y logrados. Para como distribuían traté de apegarme a lo que decía el enunciado pero cambie un poco las distribuciones para que sea mas realista para las temperaturas extremas y las lluvias de hamburguesas, ya que no entendí muy bien ciertos aspectos de como distribuían en el enunciado.

# 4 Estadísticas:

-Implementados los output que fueron posibles calcular durante la simulación, ya que no pude implementar las confiscaciones de los carabineros debido a un bug que se presentó al final de mi proceso programando :(. Espero esto no sea muy terrible ya que necesito nota :/.

-Al correr la simulación se puede ver que tira muchos prints, por lo que a la clase semestre si se le pone un False en el input, este no tira los prints y simplemente retorna las estadísticas!

# 5 Escenarios:

-Intenté implementar esta funcionalidad en mi simulación, pero me tope con el problema de que ya había hecho todas las variables del módulo variables en la simulación y no se me ocurrió como implementar una forma para que en lugar de leer_parametros() que retorna un diccionario de los parametros_iniciales, retornara un diccionario con los parametros del escenario a elegir. No supe bien como hacer la interacción entre módulos para hacer un cambio en las variables. Quizas debería haber hecho un módulo nuevo de variables para cada escenario (?) 

-Dejé eso sí las ideas expresadas para que se entendiera que si se me ocurría como implementar los escenarios.
____________________________________________

Muchas gracias por tu paciencia :)
