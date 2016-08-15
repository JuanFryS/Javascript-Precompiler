// Prueba con sentencias
var identi = 1;
var fin = true;
var a = false;
var b = true;
do{
	if (a || b) a = b;
	identi = identi + 2;
	prompt(fin);
 }while(fin)
document.write("El valor de indenti es: ", identi);
