# -*- coding: utf8 -*-
# Permite que el archivo .py contenga caracteres especiales: tildes, ñ, etc.

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
# 				  		 siem.py:							#
#	 			simulación del sistema SIEM					#
#															#
# Simula la generación automática de incidencias que podría #
# desarrollar un sistema SIEM durante su funcionamiento.	#
#############################################################


import sys								# Se importa y carga la información de sistema para control interno del middleware Flask.
reload(sys)
sys.setdefaultencoding("utf-8")			# Se trabaja por defecto con codificación de caracteres UTF-8.


import mysql.connector as mariadb				# Conector de acceso a la BBDD de MariaDB.
from subprocess import call, Popen, check_call	# Funciones de sistema.

import re   	# Libreria de funciones para manejo de Expresiones Regulares.
import os		# Libreria de funciones relacionadas con el Sistema Operativo.
import random	# Librería para generación de números aleatorios.
import time		# Funciones de manejo de la fecha y hora del sistema.
from datetime import datetime,date,timedelta	# Funciones para el manejo de fechas.
from markupsafe import Markup, escape			# Funciones para formatear y renderizar HTML.


# Inicialización del acceso a la BBDD:
mariadb_connection = mariadb.connect(user='root', password='Junio333', database='soteria', use_unicode=True, charset='utf8')
cursor = mariadb_connection.cursor()
mariadb_connection.autocommit = True	# Permite que se refresquen los datos en cada consulta y evitar los problemas de la memoria caché.

# Los datos mínimos de partida que se precisan generar son:
# id, originator(SIEM), type, description, area, accountable, csirt, id_csirt, detect_date(fecha actual), notify_date(según severidad), severity,
# dimensions, status(U), reports, details, pm_info, false_p(N), false_n(N), closing_date(0)

# Se comienza por los campos cuyo valor se conoce de antemano y serán, por tanto, de valor fijo en el momento de la creación de la incidencia:

originator = 'SIEM'
detect_date = str(time.strftime("%Y%m%d%H%M"))
status = 'U'	# Por defecto, se crea la incidencia en estado de Cuarentena.
false_p = 'N'
false_n = 'N'
closing_date = 0

# A continuación, los datos que hay que generar mediante procesado:
# id:
cursor.execute("select max(id) from INCIDENTS")
result = cursor.fetchall()
id = int(result[0][0])+1
# type y description:
ens_id_obj = ['511', '512', '513', '514', '515', '516', '517', '518', '521', '522', '523', '524', '525', '531', '532', '533', '534', '541',\
'542', '543', '544', '545', '551', '552', '553', '554', '555', '561', '562', '571', '572', '573', '574', '575', '576', '577', '581', '582',\
'583', '584']
i = random.randrange(len(ens_id_obj))
type = int(ens_id_obj[i])

ens_descrip = ['5.1.1 [MP.IF.1] ÁREAS SEPARADAS Y CON CONTROL DE ACCESO', '5.1.2 [MP.IF.2] IDENTIFICACIÓN DE LAS PERSONAS', '5.1.3 [MP.IF.3] ACONDICIONAMIENTO DE LOS LOCALES',\
'5.1.4 [MP.IF.4] ENERGÍA ELÉCTRICA', '5.1.5 [MP.IF.5] PROTECCIÓN FRENTE A INCENDIOS', '5.1.6 [MP.IF.6] PROTECCIÓN FRENTE A INUNDACIONES', '5.1.7 [MP.IF.7] REGISTRO DE ENTRADA Y SALIDA DE EQUIPAMIENTO',\
'5.1.8 [MP.IF.8] INSTALACIONES ALTERNATIVAS', '5.2.1 [MP.PER.1] CARACTERIZACIÓN DEL PUESTO DE TRABAJO', '5.2.2 [MP.PER.2] DEBERES Y OBLIGACIONES', '5.2.3 [MP.PER.3] CONCIENCIACIÓN',\
'5.2.4 [MP.PER.4] FORMACIÓN', '5.2.5 [MP.PER.5] PERSONAL ALTERNATIVO', '5.3.1 [MP.EQ.1] PUESTO DE TRABAJO DESPEJADO', '5.3.2 [MP.EQ.2] BLOQUEO DE PUESTO DE TRABAJO', '5.3.3 [MP.EQ.3] PROTECCIÓN DE EQUIPOS PORTÁTILES',\
'5.3.4 [MP.EQ.4] MEDIOS ALTERNATIVOS', '5.4.1 [MP.COM.1] PERÍMETRO SEGURO', '5.4.2 [MP.COM.2] PROTECCIÓN DE LA CONFIDENCIALIDAD', '5.4.3 [MP.COM.3] PROTECCIÓN DE LA AUTENTICIDAD Y DE LA INTEGRIDAD',\
'5.4.4 [MP.COM.4] SEGREGACIÓN DE REDES', '5.4.5 [MP.COM.5] MEDIOS ALTERNATIVOS', '5.5.1 [MP.SI.1] ETIQUETADO', '5.5.2 [MP.SI.2] CRIPTOGRAFÍA', '5.5.3 [MP.SI.3] CUSTODIA',\
'5.5.4 [MP.SI.4] TRANSPORTE', '5.5.5 [MP.SI.5] BORRADO Y DESTRUCCIÓN', '5.6.1 [MP.SW.1] DESARROLLO', '5.6.2 [MP.SW.2] ACEPTACIÓN Y PUESTA EN SERVICIO: Categoría ALTA',\
'5.7.1 [MP.INFO.1] DATOS DE CARÁCTER PERSONAL', '5.7.2 [MP.INFO.2] CALIFICACIÓN DE LA INFORMACIÓN', '5.7.3 [MP.INFO.3] CIFRADO', '5.7.4 [MP.INFO.4] FIRMA ELECTRÓNICA',\
'5.7.5 [MP.INFO.5] SELLOS DE TIEMPO', '5.7.6 [MP.INFO.6] LIMPIEZA DE DOCUMENTOS', '5.7.7 [MP.INFO.7] COPIAS DE SEGURIDAD (BACKUP)', '5.8.1 [MP.S.1] PROTECCIÓN DEL CORREO ELECTRÓNICO (E-MAIL)',\
'5.8.2 [MP.S.2] PROTECCIÓN DE SERVICIOS Y APLICACIONES WEB', '5.8.3 [MP.S.3] PROTECCIÓN FRENTE A LA DENEGACIÓN DE SERVICIO', '5.8.4 [MP.S.4] MEDIOS ALTERNATIVOS']
description = ens_descrip[i]

# area:
areas = ['Jefatura', 'Secretaría', 'Apoyo al Personal', 'Escuadrón #1', 'Escuadrón #2', 'Escuadrón #3', 'Abastecimiento', 'Automóviles', 'Global']
area = areas[random.randrange(len(areas))]

# accountable:
cursor.execute("select user from STAFF where status='A' order by rand() limit 1")	# Se extrae un personal en activo de manera aleatoria.
result = cursor.fetchall()
accountable = str(result[0][0])

# severity, csirt e id_csirt:
prob = random.randrange(100)
# Se recuerda la distribución: Críticas: 5%, Altas: 10%, Medias: 30% y Bajas: 55%.
if prob > 94:
	severity = 'C'
elif prob > 84:
	severity = 'A'
elif prob > 54:
	severity = 'M'
else:
	severity = 'B'
	
# Conformación de CSIRT:
csirt = 'N'		# Por defecto, no se conforma.
id_csirt = 0

if severity == 'C':
	if random.randrange(100) < 94:	# Probabilidad del 94% de conformar un CSIRT para incidencias de severidad Crítica.
		csirt = 'S'
		cursor.execute("select max(id) from CSIRT")
		result = cursor.fetchall()
		id_csirt = int(result[0][0]) + 1
		##### AÑADIR LA CREACIÓN DEL CSIRT!!

# notify_date -> se añadirá automáticamente cuando el proceso notify.py detecte que se trata de una incidencia Crítica o Alta y la añada a la notifique!
notify_date = ''	# Por tanto, lo dejamos en blanco!

# dimensions:
conf = random.randrange(2)
integ = random.randrange(2)
avail = random.randrange(2)
authen = random.randrange(2)
trace = random.randrange(2)
dimensions = ''
if conf:
	dimensions += 'C'
if integ:
	dimensions += 'I'
if avail:
	dimensions += 'D'
if authen:
	dimensions += 'A'
if trace:
	dimensions += 'T'
if dimensions == '':
	dimensions_t = 'CIDAT'
	dimensions = dimensions_t[random.randrange(5)];	# Se le asigna un valor por defecto, este campo no puede estar estar vacío!
	
# reports -> al generarse la incidencia desde el SIEM, aún no cuenta con informes hasta que se empiece a atender...
reports = ''

# details:
details_list_quarantine = ['Se inician las acciones para la resolución de la incidencia. Se inician las acciones para la resolución de la incidencia. La resolución \
de la incidencia requiere que la incidencia ######## se cierre previamente, por lo que se deja en cuarentena.',\
'Se inician las acciones para la resolución de la incidencia. La resolución de la incidencia requiere la actualización del siguiente software: bla bla bla, por lo que \
se deja en cuarentena.',\
'Se inician las acciones para la resolución de la incidencia. La resolución de la incidencia requiere la adquisición y despliegue del siguiente material: bla bla bla, \
por lo que se deja en cuarentena.',\
'Se inician las acciones para la resolución de la incidencia. La resolución de la incidencia requiere el desarrollo del siguiente software: bla bla bla, por lo que \
se deja en cuarentena.',\
'Se inician las acciones para la resolución de la incidencia. Tras aplicar las medidas de protección, se requiere un tiempo de observación de comportamiento del \
sistema no inferior a 4 semanas. Se deja, por tanto, en cuarentena.',\
'Se inician las acciones para la resolución de la incidencia. La resolución de la incidencia requiere la virtualización de los siguientes servicios: bla bla bla, por \
lo que se deja cuarentena.']
details = details_list_quarantine[random.randrange(len(details_list_quarantine))]

# pm_info:
cursor.execute("select pm_list from ENS where id=%s", (type,))
result = cursor.fetchall()
pm_list = str(result[0])
pat = re.compile('\d{3}\. ')
pm_list_id = pat.findall(pm_list)
pm_info = ''
for p in range(len(pm_list_id)):
	pm_info += pm_list_id[p].replace(". ","") + '$$N=='

# Por último, se inserta la nueva incidencia en la tabla INCIDENTS:
query_text = "INSERT INTO INCIDENTS (id, originator, type, description, area, accountable, csirt, id_csirt, detect_date, notify_date, severity, dimensions, status, reports, details, pm_info, false_p, false_n, closing_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
values = (id, originator, type, description, area, accountable, csirt, id_csirt, detect_date, notify_date, severity, dimensions, status, reports, details, pm_info, false_p, false_n, closing_date)
cursor.execute(query_text,values)
mariadb_connection.commit()		# Se hacen efectivos los cambios en la BBDD.
	
	
###############
# FIN siem.py #
###############
