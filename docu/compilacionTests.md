Has terminado la actividad:

Dada la siguiente gramática, ¿cuál de las siguientes afirmaciones relativas al Autómata Reconocedor de Prefijos Viables (método de Análisis Sintáctico Ascendente LR(1)) es correcta?
S → A B | B C
A → 1 A | 2 A | λ
B → 3 C 4 | λ
C → 3 | 2 B
Respuesta:

Desde el estado inicial, hay una transición etiquetada con el símbolo “B” a un estado donde se encuentra el ítem S→A•B

Esta respuesta es incorrecta.

Explicación:

El ítem S→•BC está presente en el estado inicial y eso produce una transición con “B” correspondiente al Goto (I0,B), pero ahí no está el ítem S→A•B

La respuesta correcta era:

Respuesta:

Desde el estado inicial, hay una transición etiquetada con el símbolo “3” a un estado donde se encuentra el ítem C→•3

Explicación:

El ítem B→•3C4 está presente en el estado inicial y eso produce una transición con “3” correspondiente al Goto (I0,3), y ahí estará el ítem C→•3 obtenido al calcular el cierre({B→3•C4})

Para un lenguaje de programación sin declaración previa de variables, se ha creado el siguiente conjunto de atributos de la Tabla de Símbolos. ¿Es correcto (aunque no sea completo)?: Lexema, Tipo, Desplazamiento (o Dirección)
Respuesta:

Falso

Esta respuesta es incorrecta.

Explicación:

Los tres campos indicados son válidos y necesarios para este lenguaje: el lexema, para guardar el nombre del identificador; el tipo, para conocer qué tipo de datos representa el identificador; la dirección, para que durante la ejecución del programa objeto, éste sepa exactamente dónde está el valor de cada variable

goto
Has terminado la actividad:

Para la siguiente gramática, indica cuáles de los siguientes cálculos de los conjuntos cierre o goto son correctos, cuando se quiere construir un Analizador LR:
S → A B
A → B C | k C
B → C D | λ
C → + A
D → k B
Respuestas Seleccionadas:

1: I0=cierre({S'→·S})={S'→·S, A→·BC, A→·kC, B→·CD, B→·, C→·+A}
  Esta respuesta es incorrecta.
Explicación:
El primer estado se calcula con el conjunto cierre y falta el ítem S→·AB

2: I0=cierre({S'→·S})={S'→·S, S→·AB, A→·BC, A→·kC, B→·CD, B→·, C→·+A, D→·kB}
  Esta respuesta es incorrecta.
Explicación:
El primer estado se calcula con el conjunto cierre y sobra el ítem D→·kB

3: I3=goto(I0, B)={A→B·C, C→·+A}
  Esta respuesta es correcta.
Explicación:
El cálculo es correcto

4: I5=goto(I0, C)={A→k·C, C→·+A}
  Esta respuesta es incorrecta.
Explicación:
Ambos ítems están mal y faltan B→C·D, D→·kB

5: I1=goto(I0, S)={S'→S·}
  Esta respuesta es correcta.
Explicación:
El cálculo es correcto

as terminado la actividad:

Indica cuáles de los conjuntos First son correctos para la siguiente Gramática:
S ⟶ e A B g | C B
A ⟶ A a | a
B ⟶ b B | λ
C ⟶ E F D
D ⟶ k D | λ
E ⟶ E g | h | λ
F ⟶ i j F | λ
Respuestas Seleccionadas:

1: FIRST (A) = { a }
  Esta respuesta es correcta.
Explicación:
Por la regla A→a, tiene a. La regla (A→Aa) no aporta nada más

2: FIRST (C) = { h, g, i, k, λ }
  Esta respuesta es correcta.
Explicación:
Como C→EFD, los elementos no nulos de FIRST(E) pertenecen a FIRST(C). Como FIRST(E) contiene el elemento nulo, todos los elementos no nulos de FIRST(F) pertenecen a FIRST(C). Como FIRST(F) contiene el elemento nulo, todos los elementos no nulos de FIRST(D) pertenecen a FIRST(C). Y como todos ellos contienen λ, se añade λ a FIRST(C)

3: FIRST (C) = { h, g, i, k }
  Esta respuesta es incorrecta.
Explicación:
Falta λ. Por la regla C→EFD, como λ pertenece a los tres conjuntos FIRST(E), FIRST(F) y FIRST(D), se añade λ a FIRST(C)

4: FIRST (F) = { i, j, λ }
  Esta respuesta es incorrecta.
Explicación:
No hay ninguna razón para añadir j al conjunto

5: FIRST (D) = { k }
  Esta respuesta es incorrecta.
Explicación:
Falta λ, que está en FIRST(D) por la regla D→λ

6: FIRST (S) = { e, h, g, i, k, b }
  Esta respuesta es incorrecta.
Explicación:
Falta λ que se añade por estar en FIRST(B) habiendo estado también en FIRST(C) (cuando se calcula FIRST(CB))

¿Cuáles de los siguientes conjuntos son correctos, dada la siguiente gramática?
P → D P | S P | λ
D → var T id ; D | λ | F ; D
F → function id T ( id : T L ) begin S end
L → ; id : T L | λ
T → integer | boolean
S → if E do S | return E | id := E ; S
E → id ( K )
K → E R
R → λ | ; K R
Respuestas Seleccionadas:

1: First (K) = {id, λ, ;}
  Esta respuesta es incorrecta.
Explicación:
Sobran dos elementos

2: First (P) = {var, function, if, return, id}
  Esta respuesta es incorrecta.
Explicación:
Falta lambda

3: First (P) = {var, function, λ, if, return, id}
  Esta respuesta es correcta.
Explicación:
P puede ser lambda o empezar por lo mismo que empieza D o S

4: First (:=) = {:=}
  Esta respuesta es correcta.
Explicación:
El First de un terminal es el propio terminal

5: First (S) = {if, return, id}
  Esta respuesta es correcta.
Explicación:
S solo puede empezar por uno de esos tres terminales, tal como indican las reglas de S

6: First (K) = {id, ;}
  Esta respuesta es incorrecta.
Explicación:
Sobra un elemento

7: First (K) = {E}
  Esta respuesta es incorrecta.
Explicación:
En un conjunto First no puede haber símbolos no terminales

8: First (R) = {;, λ}
  Esta respuesta es correcta.
Explicación:
R solo puede ser lambda o empezar por punto y coma

Para un lenguaje de programación sin declaración previa de variables, se ha creado el siguiente conjunto de atributos de la Tabla de Símbolos. ¿Es correcto (aunque no sea completo)?: Lexema, TipoDeclarado, TipoNoDeclarado
Respuesta:

Verdadero

Esta respuesta es incorrecta.

Explicación:

Separar los tipos de las variables declaradas de las que no lo han sido no sirve para nada. Todas las variables tendrán su tipo, hayan sido declaradas o no, en función de las características del lenguaje

La respuesta correcta era:

Respuesta:

Falso

Para un lenguaje de programación sin declaración previa de variables, se ha creado el siguiente conjunto de atributos de la Tabla de Símbolos. ¿Es correcto (aunque no sea completo)?: Nº de variables declaradas, Tipo, Dirección (o Desplazamiento)
Respuesta:

Verdadero

Esta respuesta es incorrecta.

Explicación:

El número de variables declaradas no es una característica de un identificador ni sirve para nada saber cuántas hay. En la Tabla de Símbolos se guarda información sobre cada uno de los identificadores.

La respuesta correcta era:

Respuesta:

Falso

¿Qué atributos necesita una Tabla de Símbolos de un lenguaje de programación habitual (del tipo de los vistos en clase) y qué módulo del Procesador del Lenguaje es el encargado de introducir esta información?
Respuestas Seleccionadas:

1: Atributo número de parámetros de un identificador que es una función, introducido por el analizador sintáctico
  Esta respuesta es incorrecta.
Explicación:
El analizador sintáctico solo reconoce la declaración de la función, pero no analiza su significado por lo que desconocerá cuántos parámetros hay

2: Atributo valor de una variable, introducido por el analizador léxico
  Esta respuesta es incorrecta.
Explicación:
El analizador léxico no puede saber jamás el valor que tomará una variable

3: Atributo posición de memoria (o desplazamiento) de una variable, introducido por el analizador léxico
  Esta respuesta es incorrecta.
Explicación:
El analizador léxico no puede asociar a un identificador a una posición de memoria, pues no tiene toda la información necesaria para hacerlo

4: Se guardan las constantes cadenas de caracteres, introducidas por el analizador léxico
  Esta respuesta es incorrecta.
Explicación:
Las cadenas jamás se guardan en la Tabla de Símbolos

5: Atributo tipo, introducido por analizador semántico cuando el lenguaje es tipado con declaraciones obligatorias
  Esta respuesta es correcta.
Explicación:
Cuando el analizador sintáctico ha reconocido una declaración, el semántico asocia el tipo al identificador y lo introduce en la Tabla de Símbolos

6: Se guardan las constantes cadenas de caracteres, introducidas por el analizador semántico
  Esta respuesta es incorrecta.
Explicación:
Las cadenas jamás se guardan en la Tabla de Símbolos

Para un lenguaje de programación sin declaración previa de variables, se ha creado el siguiente conjunto de atributos de la Tabla de Símbolos. ¿Es correcto (aunque no sea completo)?: Lexema, Tipo, Desplazamiento (o Dirección)
Respuesta:

Falso

Esta respuesta es incorrecta.

Explicación:

Los tres campos indicados son válidos y necesarios para este lenguaje: el lexema, para guardar el nombre del identificador; el tipo, para conocer qué tipo de datos representa el identificador; la dirección, para que durante la ejecución del programa objeto, éste sepa exactamente dónde está el valor de cada variable

La respuesta correcta era:

Respuesta:

Verdadero

Explicación:

Todos estos campos son válidos y necesarios en un Procesador de este tipo

¿Cuáles de las siguientes son operaciones que debe permitir realizar un Tipo Abstracto de Datos que represente una Tabla de Símbolos?
Respuestas Seleccionadas:

1: Destruir una Tabla de Símbolos
  Esta respuesta es correcta.
Explicación:
Una vez que la información de una Tabla de Símbolos ya no es necesaria, se puede eliminar

2: En caso de detectar un error en el programa fuente, debe tener una operación que permita llamar al Gestor de Errores
  Esta respuesta es incorrecta.
Explicación:
La Tabla de Símbolos, por sí misma, no detecta errores en el programa fuente. Serán los módulos de Análisis quier, consultando la Tabla de Símbolos, podrán detectar errores y ser ellos quien se lo notifique al Gestor de Errores

3: Acceder a la información de un atributo de una entrada
  Esta respuesta es correcta.
Explicación:
Durante las distintas fases de compilación es necesario acceder a información de los distintos atributos

4: Crear una Tabla de Símbolos vacía
  Esta respuesta es correcta.
Explicación:
Para poder operar con la Tabla de Símbolos debe poderse crear previamente

5: Calcular el tamaño de la Tabla de Símbolos
  Esta respuesta es incorrecta.
Explicación:
No se necesita para nada saber cuánto ocupa una Tabla de Símbolos

¿Cuáles de los siguientes conjuntos son correctos, dada la siguiente gramática?
P → D P | S P | λ
D → var T id ; D | λ | F ; D
F → function id T ( id : T L ) begin S end
L → ; id : T L | λ
T → integer | boolean
S → if E do S | return E | id := E ; S
E → id ( K )
K → E R
R → λ | ; K R
Respuestas Seleccionadas:

1: Follow (D) = {var, function, $, if, return, id}
  Esta respuesta es correcta.
Explicación:
Detrás de D viene P (que puede ser anulable)

2: Follow (R) = {), ;}
  Esta respuesta es correcta.
Explicación:
Tras R vendrá lo mismo que lo que puede estar tras K

3: Follow (T) = {id, (, ), ;}
  Esta respuesta es correcta.
Explicación:
Después de T solo puede venir L o lo que venga tras L

4: Follow (P) = {$}
  Esta respuesta es correcta.
Explicación:
Por definición, el dólar está después del axioma

5: Follow (F) = {;}
  Esta respuesta es correcta.
Explicación:
Después de F no puede venir nada más

6: Follow (K) = {), ;}
  Esta respuesta es correcta.
Explicación:
Tras K solo puede venir el paréntesis o R

7: Follow (T) = {id, (, ;, λ}
  Esta respuesta es incorrecta.
Explicación:
Lambda nunca está en un conjunto Follow

Para la siguiente gramática, indica cuáles de los siguientes cálculos de los conjuntos cierre o goto son correctos, cuando se quiere construir un Analizador LR:
S → A B
A → B C | k C
B → C D | λ
C → + A
D → k B
Respuestas Seleccionadas:

1: I1=goto(I0, S)={S'→·S}
  Esta respuesta es incorrecta.
Explicación:
El ítem correcto de este conjunto es S'→S·

2: I4=goto(I0, k)={A→k·C, C→·+A}
  Esta respuesta es correcta.
Explicación:
El cálculo es correcto

3: I0=cierre({S'→·S})={S→·AB, A→·BC, A→·kC, B→·CD, B→·, C→·+A}
  Esta respuesta es incorrecta.
Explicación:
El primer estado se calcula con el conjunto cierre y falta el ítem S'→·S

4: I6=goto(I0, +)={A→·BC, A→·kC, B→·CD, B→·, C→·+A}
  Esta respuesta es incorrecta.
Explicación:
Falta el ítem C→+·A

5: I6=goto(I0, +)={S→·AB, A→·BC, A→·kC, B→·CD, B→·, C→·+A}
  Esta respuesta es incorrecta.
Explicación:
Sobra el primer ítem

Dado el siguiente estado perteneciente al Autómata reconocedor de Prefijos Viables de un Analizador Sintáctico LR, In={S→A F •, A→B D •, B→3 • A, B→• 3 A, C→3 • 4, B→5 A •} ¿cuál de las siguientes afirmaciones es correcta?
Respuesta:

Si el Follow(B) contiene el terminal “5”, hay un conflicto de Reducción-Desplazamiento

Esta respuesta es incorrecta.

Explicación:

En este estado, se debería reducir (por B→5 A •), pero no hay desplazamiento posible con "5", por lo que no hay un conflicto

La respuesta correcta era:

Respuesta:

Si el Follow(A) contiene el terminal “3”, hay un conflicto de Reducción-Desplazamiento

Explicación:

En este estado, se debería desplazar con el token “3” (por B→• 3 A), pero también reducir (por A→B D •), por lo que hay un conflicto

¿Cuáles de las siguientes afirmaciones son correctas en relación con la Gramática aumentada?
Respuestas Seleccionadas:

1: La gramática aumentada es necesaria para asegurarse que el axioma nunca aparecerá en el lado derecho de ninguna regla
  Esta respuesta es correcta.
Explicación:
De esta manera, al reducir por la nueva regla del nuevo axioma, se sabrá que se debe aceptar la cadena

2: La nueva regla del axioma introducida en la gramática aumentada dará lugar a un ítem en el estado inicial del autómata de prefijos viables que tendrá el punto inmediatamente después del axioma de la gramática original
  Esta respuesta es incorrecta.
Explicación:
Ése será el ítem del estado de aceptación de la cadena, no el inicial

3: En la gramática aumentada, el nuevo axioma aparecerá en la parte derecha de al menos una regla
  Esta respuesta es incorrecta.
Explicación:
La gramática aumentada se obtiene a partir de la gramática original, añadiendo un nuevo axioma y una nueva regla que deriva el nuevo axioma en el axioma de la gramática original

4: La gramática aumentada es igual a la gramática original pero añadiendo una nueva regla lambda al axioma
  Esta respuesta es incorrecta.
Explicación:
La gramática aumentada se obtiene a partir de la gramática original, añadiendo un nuevo axioma y una nueva regla que deriva el nuevo axioma en el axioma de la gramática original
