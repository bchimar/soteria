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
# 					  	config.py:							#
#		módulo de configuración de la aplicación Flask		#
#############################################################

import os
DEBUG = True 

_basedir = os.path.abspath(os.path.dirname(__file__))

DEFAULT_TPL = 'default'

SECRET_KEY = 'secret devel key'

URL = 'http://0.0.0.0:80/'
TITLE = 'Soteria'
AUTOR = 'Blas Chica Martos'
VERSION = '1.0'
LANG = 'es'
LANG_DIRECTION = 'ltr'  # Left To Right
YEAR = 'Noviembre 2018'

del os


#################
# FIN config.py #
#################

