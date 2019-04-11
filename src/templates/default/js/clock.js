
/*
#############################################################
#                     CUD - MARÍN                           # 
#                       MGSTICS                             # 
#                      2017/2018                            # 
#               TRABAJO DE FIN DE MÁSTER                    # 
#   DISEÑO E IMPLEMENTACIÓN DE UNA PLATAFORMA WEB PARA      # 
#  LA GESTIÓN DE INCIDENTES DE SEGURIDAD DE LA INFORMACIÓN  # 
#                ALUMNO: BLAS CHICA MARTOS.                 # 
#############################################################

#############################################################
# PERMITE MOSTRAR UN RELOJ DIGITAL HH:MM DD/MM/AAAA EN EL   #
#					  INTERFAZ WEB 							#
#############################################################

############################################################################################
# BASADO EN LA VERSIÓN: https://www.w3schools.com/js/tryit.asp?filename=tryjs_timing_clock #
############################################################################################

*/

function startTime()
{
	// Declaración de variables y asignación de valor:
	var now=new Date();
	var h=now.getHours();
	var m=now.getMinutes();
	var d=now.getDate();
	var mo=now.getMonth()+1;	// Ojo! el mes se devuelve con valor en el rango [0<->11] !!
	var y=now.getFullYear();
	// Se evita trabajar con segundos para evitar la sensación estresante de la actualización continua del segundero.

	// Normalización:
	h=checkTime(h);	
	m=checkTime(m);
	d=checkTime(d);
	mo=checkTime(mo);
	
	// Se genera la cadena de texto a mostrar:
	document.getElementById('clock').innerHTML=h+":"+m+"<br/>"+d+"/"+mo+"/"+y;
	
	// Por último, se establece un temporizador para actualizar los datos periódicamente, en este caso, cada segundo:
	t=setTimeout('startTime()',1000);	
}

// Se normaliza el formato: cifras < 10 se normalizan a 2 dígitos, insertando un 0 delante si fuera preciso:
function checkTime(i)
{
	if (i<10)
	{
		i="0" + i;
	}
	return i;
}
