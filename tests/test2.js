let number x;  /* global*/
x = 3;
function number factorial(boolean y)
/* se define la función recursiva con un parámetro, 
   que oculta a la variable global de igual nombre */
{
    if (x == 1) x++;
    x = x++;


}	/* la función devuelve un entero*/
function boolean Suma(boolean aux, number fin)
/* se define la función Suma que recibe 
   dos enteros por valor */
/* usa la variable global x */
{
    pax = factorial(aux && aux);

    return pax != 10000;
}	/* la función devuelve un lógico*/
function Imprime(number a) {
    alert(a);
    return;	/* esta instrucción se podría omitir*/
}	/* la función no devuelve nada*/

do {
    x++;
    alert(x);

} while (x != 5);
Imprime(factorial(Suma(1, false)));	/* se llama a las tres funciones*/
