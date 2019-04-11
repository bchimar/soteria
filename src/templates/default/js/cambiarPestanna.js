
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
#	  PERMITE EL MANEJO DE PESTAÑAS EN EL INTERFAZ WEB 		#
#############################################################

##################################################################################################################
# BASADO EN ORIGEN EN LA VERSIÓN: https://programandoointentandolo.com/2012/11/como-crear-pestanas-con-html.html #
##################################################################################################################

*/


// Mediante esta función se mantiene visible la pestaña seleccionada, ocultando las demás:
function cambiarPestanna(pestannas,pestanna) {
    
    // Obtiene los elementos con los identificadores pasados:
    pestanna = document.getElementById(pestanna.id);
    listaPestannas = document.getElementById(pestannas.id);
    
    // Obtiene las divisiones que presenta el contenido de las pestañas:
    cpestanna = document.getElementById('c'+pestanna.id);
    listacPestannas = document.getElementById('contenido'+pestannas.id);
   
    // Recorre la lista ocultando todas las pestañas y restaurando el padding de las mismas:
    i=0;
  while (typeof listacPestannas.getElementsByTagName('div')[i] != 'undefined'){
    $(document).ready(function(){
            $(listacPestannas.getElementsByTagName('div')[i]).css('display','none');
            $(listaPestannas.getElementsByTagName('li')[i]).css('padding-bottom','');
        });
        i += 1;
    }

    $(document).ready(function(){
        // Muestra el contenido de la pestaña pasada como parámetro a la función, cambia el color de dicha pestaña y aumenta el padding
		// con el fin de que tape el borde superior del contenido que se encuentra debajo, ofreciendo la sensación de estar seleccionada:
        $(cpestanna).css('display','');
        $(pestanna).css('padding-bottom','2px'); 
    });

}
