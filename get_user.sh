
# -*- coding: utf8 -*-

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
# 					  	get_user.sh:						#
#	   script para obtener el usuario recién autenticado	#
#############################################################

#!/bin/bash
cd /apache_2fa/state/
user_file=$(ls -rt | tail -n 1)
cat "$user_file" | tail -n 1

# Al autenticarse el usuario se crea un fichero cookie bajo el directorio /apache_2fa/state/
# de Google Authenticator. Los últimos 9 caracteres del fichero contienen el nombre del usuario logueado!

