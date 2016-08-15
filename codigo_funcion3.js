function funcion3 (var_logica, var_entera1, var_entera2){
	var a = false;
	var b = true;
	var fin = false;
	do{
		if (a || b ) var_logica = b;
		var_entera2 +=  var_entera1 + 2 ;
		var_entera1 = var_entera1 + 1;
		var_no_declarada1 = var_entera1 + var_entera2;
		prompt(fin);
		prompt(var_no_declarada2);
	 }while(fin)
	document.write("El valor de la variable lógica es: ",var_logica,"El resultado de la función es ", var_entera2);
	document.write(var_no_declarada3);
	return var_entera2;
}

