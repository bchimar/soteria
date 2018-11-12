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
# 					  	Soteria.wsgi:						#
#		módulo de configuración de la aplicación Flask		#
#		en el caso de utilizar un servidor web externo		#
#############################################################


#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Soteria/src")

activate_this = '/var/www/Soteria/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from Soteria import app as application
application.secret_key = '>aJkFe340cFbApItW592.3fjGlDeY<'


#################
# FIN config.py #
#################
