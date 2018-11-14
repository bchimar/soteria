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
# 				   Soteria_libs.py:							#
#	 contiene las funciones de apoyo al módulo principal	#
#############################################################

from markupsafe import Markup, escape	# Funciones para formatear y renderizar HTML.

import re   	# Libreria de funciones para manejo de Expresiones Regulares.
import os		# Libreria de funciones relacionadas con el Sistema Operativo.
import random	# Librería para generación de números aleatorios.
import time		# Funciones de manejo de la fecha y hora del sistema.
from datetime import datetime,date,timedelta	# Funciones para el manejo de fechas.
from math import floor	# Para ajustar los valores por defecto.

import sys								# Se importa y carga la información de sistema para control interno del middleware Flask.
reload(sys)
sys.setdefaultencoding("utf-8")			# Se trabaja por defecto con codificación de caracteres UTF-8.

from smtplib import SMTP				# Librería con las funciones que permiten enviar correo electrónico.
from email.mime.text import MIMEText	# Librería para la generación de los correos a enviar.

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


# Genera el código a insertar en la función javascript init() de la cabecera según el módulo de que se trate (index, manage_incident o new_incident):
def get_init_content(mod,csirt,status):

	js_code_init = ''

	if mod == 'manage_incident':
		if csirt == 'S':
			js_code_init += 'document.getElementById("severity").disabled=true;\n\n\t\t\t\t'
		if status == 'C':
			js_code_init += 'document.getElementById("lift_it_up").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("accountable").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("severity").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("Conf").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("Inte").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("Avai").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("Auth").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("Trac").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("status").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("false_p").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("false_n").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("table_pm").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("details").disabled=true;' +\
			'\n\t\t\t\tdocument.getElementById("reports").disabled=true;'
	elif mod == 'new_incident':
		js_code_init = 'document.getElementById("id_csirt").disabled=true;\n' +\
		'\t\t\t\tdocument.getElementById("id_csirt").value="";'
	
	return Markup(js_code_init)


# Devuelve el interfaz maquetado HTML para la búsqueda de incidencias:
def get_search_incidents():

	max_id = str(int(time.strftime("%Y")))+'9999'
	max_id_csirt = str(int(time.strftime("%Y")))+'99'

	search_incidents_content = '<form method="post" action="">' +\
		'<fieldset style="width: 60%; height: 80%; background: #FFFFFF; font-size: 16px; margin-top: 10px; margin-left: 10%; text-align: left;">' +\
			'<legend style="font-size: 20px; font-weight: bold;">Seleccione los criterios de consulta</legend>' +\
			'<p>ID:<input type="number" name="id_incid" value="" min="20150001" max="'+max_id+'" size="6" maxlength="8" style="margin-left: 7px;"></p>' +\
			'<p>Detección:&emsp;Fecha de inicio:<input type="date" name="start_date" value="" style="margin-left: 7px;">&emsp;&emsp;Fecha de fin:<input type="date" name="stop_date" value="" style="margin-left: 7px;"></p>' +\
			'<p>Estado:<select name="status" style="margin-left: 7px;">' +\
					'<option name="status" value=""></option>' +\
					'<option name="status" value="A">Abierta</option>' +\
					'<option name="status" value="U">Cuarentena</option>' +\
					'<option name="status" value="C">Cerrada</option>' +\
				'</select></p>' +\
			'<p>Severidad:<select name="severity" style="margin-left: 7px;">' +\
			'<option name="severity" value=""></option>' +\
					'<option name="severity" value="B">Baja</option>' +\
					'<option name="severity" value="M">Media</option>' +\
					'<option name="severity" value="A">Alta</option>' +\
					'<option name="severity" value="C">Crítica</option>' +\
				'</select></p>' +\
			'<p>Dimensiones de seguridad afectadas:&emsp;' +\
				'<input type="checkbox" class="case" name="Conf" value=""> C&emsp;' +\
				'<input type="checkbox" class="case" name="Inte" value=""> I&emsp;' +\
				'<input type="checkbox" class="case" name="Avai" value=""> D&emsp;' +\
				'<input type="checkbox" class="case" name="Auth" value=""> A&emsp;' +\
				'<input type="checkbox" class="case" name="Trac" value=""> T&emsp;&emsp;' +\
				'<select name="operator" style="margin-left: 3px;">' +\
					'<option name="operator" value="and">AND</option>' +\
					'<option name="operator" value="or">OR</option>' +\
				'</select>' +\
			'</p>' +\
			'<p>Originador (ID de usuario):<input type="text" size="7" maxlength="9" name="originator" value="" style="margin-left: 7px;"></p>' +\
			'<p>Responsable (ID de usuario):<input type="text" size="7" maxlength="9" name="accountable" value="" style="margin-left: 7px;"></p>' +\
			'<p>Tipo de incidencia (código ENS):<input type="number" size="1" maxlength="3" name="type" value="" min="511" max="584" style="margin-left: 7px;"></p>' +\
			'<p>Área afectada:<select name="area" style="margin-left: 7px;">' +\
					'<option name="area" value=""></option>' +\
					'<option name="area" value="Jefatura">Jefatura</option>' +\
					'<option name="area" value="Secretaría">Secretaría</option>' +\
					'<option name="area" value="Apoyo al Personal">Apoyo al Personal</option>' +\
					'<option name="area" value="Escuadrón #1">Escuadrón #1</option>' +\
					'<option name="area" value="Escuadrón #2">Escuadrón #2</option>' +\
					'<option name="area" value="Escuadrón #3">Escuadrón #3</option>' +\
					'<option name="area" value="Abastecimiento">Abastecimiento</option>' +\
					'<option name="area" value="Automóviles">Automóviles</option>' +\
					'<option name="area" value="Global">Global</option>' +\
				'</select></p>' +\
			'<p>CSIRT:<select name="csirt" style="margin-left: 7px;">' +\
					'<option name="csirt" value=""></option>' +\
					'<option name="csirt" value="S">Sí</option>' +\
					'<option name="csirt" value="N">No</option>' +\
				'</select>&emsp;&emsp;CSIRT_ID: <input type="number" name="id_csirt" value="" size="4" maxlength="6" min="201501" max="'+max_id_csirt+'" style="margin-left: 7px;"></p>' +\
			'<p><input type="radio" name="falses" value="false_p">  Falso positivo<input type="radio" name="falses" value="false_n">  Falso negativo</p>' +\
			'<input type="image" src="img/database-search.ico" name="query" value="query" style="margin-left: 45%;">' +\
		'</fieldset>' +\
	'<p id="new_incident"><input type="image" src="img/new_incident.png" name="new_incident" value="new_incident" style="width:30%; height:3%;"><br/>Alta de Incidencia</a></p>'+\
	'<input type="hidden" name="form_id" value="launch_query">' +\
	'</form>'
	
	return Markup(search_incidents_content)		# Se devuelve formateado para la correcta visualización a través del interfaz Web.


def get_new_incident_content(id_incid,id_csirt):

	new_incident_content = '<form method="post" action="">'+\
		'<fieldset style="width: 60%; height: 80%; background: #FFFFFF; font-size: 16px; margin-top: 10px; margin-left: 17%; text-align: left;">'+\
			'<legend style="font-size: 20px; font-weight: bold;">Inserte los datos de la nueva incidencia</legend>'+\
			'<p>ID:<input readonly type="text" name="id_incid" value="' + str(id_incid) +'" size="6" maxlength="8" style="margin-left: 7px; height: 14px; width: 70px;"></p>'+\
			'<p>Estado*:<select name="status" style="margin-left: 7px;">'+\
					'<option name="status" value=""></option>'+\
					'<option name="status" value="A">Abierta</option>'+\
					'<option name="status" value="U">Cuarentena</option>'+\
					'<option name="status" value="C">Cerrada</option>'+\
				'</select></p>'+\
			'<p>Severidad*:<select name="severity" id="severity" style="margin-left: 7px;">'+\
			'<option name="severity" value=""></option>'+\
					'<option name="severity" value="B">Baja</option>'+\
					'<option name="severity" value="M">Media</option>'+\
					'<option name="severity" value="A">Alta</option>'+\
					'<option name="severity" value="C">Crítica</option>'+\
				'</select></p>'+\
			'<p>Dimensiones de seguridad afectadas*:&emsp;&emsp;'+\
				'<input type="checkbox" class="case" name="Conf" value=""> C&emsp;&emsp;'+\
				'<input type="checkbox" class="case" name="Inte" value=""> I&emsp;&emsp;'+\
				'<input type="checkbox" class="case" name="Avai" value=""> D&emsp;&emsp;'+\
				'<input type="checkbox" class="case" name="Auth" value=""> A&emsp;&emsp;'+\
				'<input type="checkbox" class="case" name="Trac" value=""> T'+\
			'</p>'+\
			'<p>Responsable (ID de usuario)*:<input type="text" id="accountable" size="7" maxlength="9" name="accountable" value="" style="margin-left: 7px;"></p>'+\
			'<p>Tipo de incidencia (código ENS)*:<input type="number" size="1" maxlength="3" name="type" value="" min="511" max="584" style="margin-left: 7px;"></p>'+\
			'<p>Área afectada*:<select name="area" style="margin-left: 7px;">'+\
					'<option name="area" value=""></option>'+\
					'<option name="area" value="Jefatura">Jefatura</option>'+\
					'<option name="area" value="Secretaría">Secretaría</option>'+\
					'<option name="area" value="Apoyo al Personal">Apoyo al Personal</option>'+\
					'<option name="area" value="Escuadrón #1">Escuadrón #1</option>'+\
					'<option name="area" value="Escuadrón #2">Escuadrón #2</option>'+\
					'<option name="area" value="Escuadrón #3">Escuadrón #3</option>'+\
					'<option name="area" value="Abastecimiento">Abastecimiento</option>'+\
					'<option name="area" value="Automóviles">Automóviles</option>'+\
					'<option name="area" value="Global">Global</option>'+\
				'</select></p>'+\
			'<p>CSIRT:<select name="csirt" id="csirt" style="margin-left: 7px;">'+\
					'<option value="S">Sí</option>'+\
					'<option value="N" selected>No</option>'+\
				'</select>&emsp;&emsp;'+\
				'CSIRT_ID: <input readonly type="text" name="id_csirt" id="id_csirt" size="4" maxlength="6" value="' + str(id_csirt) + '" style="margin-left: 7px; width: 60px;"></p>'+\
			'<input type="image" src="img/upload.png" name="new_incident" value="new_incident" style="width: 8%; margin-left: 45%; margin-top: 5%;">'+\
			'<input readonly value=" *Campos obligatorios" style="width: 22%; margin-left: 76%; float: left; margin-top: 0%; font-weight: bold; border-left: 6px solid red; border-right: 6px solid red; border-bottom: none; border-top: none;">'+\
			'<input type="hidden" name="form_id" value="set_new_incident">'+\
		'</fieldset>'+\
	'</form>'

	return Markup(new_incident_content)
	

# Devuelve la tabla HTML maquetada con el listado de incidencias que encajan con la búsqueda:
def get_table_incidents(result):

	table = '<h2>Resultado de la consulta:</h2>' +\
			'<form method="post" action="">' +\
			'<p>'

	table += u'<table style="margin-left: 1%; border: none;"><tr><th>ID</th><th>Originador</th><th>Clasificación ENS</th><th>Descripción</th><th>Área</th><th>Responsable</th><th>CSIRT</th><th>ID_CSIRT</th><th>Detección</th><th>Notificación</th><th>Severidad</th><th>Dimensiones</th><th>Estado</th><th>Informes</th><th>Detalles</th><th>Info MP</th><th>Falso Positivo</th><th>Falso Negativo</th><th>Cierre</th></tr>'

	field = ''
	
	odd = 's'	# Controla si se encuentra en fila par o impar (para aplicación de CSS).
	
	for row in range(len(result)):	# Cada entrada de result recoge los datos de un registro.
	
		row_data = ''
		
		entry = str(result[row]).decode('unicode_escape')	# Recoge los resultados. Cada entrada en result simboliza un registro que encaja con la consulta.
				
		first_field = 's'			# Permitirá controlar que se añada el botón de acceso a la consulta detallada de cada incidencia.
		
		# Se alterna en el sombreado de cada fila de la tabla:
		if odd == 's':
			row_data_init = '<tr id="odd_row">'
			odd = 'n'
		else:
			row_data_init = '<tr id="even_row">'
			odd = 's'
		
		j = 0				# Se empleará para el control de visualización de la fecha de detección.
		
		row_data_head = ''	# Para control del primer campo (selección de incidente).
		
		for i in range(1,len(entry)):

			if entry[i] != ',' or (entry[i-1].isdigit() and entry[i+2].isdigit()) or (entry[i-1].isdigit() and entry[i+2] != 'u') or (entry[i-1] != "'" and entry[i+2] != 'u'):
					field = field + entry[i]
			else:
				field = field.replace("u'","")
				field = field.replace("'","")
				if len(field) > 20:
					field = field[0:17] + '...'		# En este apartado sólo se lista de manera rápida los datos de los incidentes consultados.
				if first_field == 's':				# Se inserta el botón de selección de la incidencia por si se necesita para la consulta detallada.
					if row == 0:
						row_data_head = '<input type="submit" name="id_incid" id="id_incid" value="' + field + '"></td>'
					else:
						row_data_head = '<input type="submit" name="id_incid" id="id_incid" value="' + field[len(field)-8:len(field)] + '"></td>'
						
					first_field = 'n'						
				else:
					if j == 8:		# Si se trata del campo detect_date, hay que decodificarlo para mostrarlo de manera legible:
						row_data += '<td>' + field[7:9] + '/' + field[5:7] + '/' + field[1:5] + ' ' + field[9:11] + ':' + field[11:13] + '</td>'
					elif j == 10:	# Severity => se inserta el icono correspondiente:
						if field.find('B') > -1:
							img = '<td><img src="img/Incidentes_04_Baja_01.ico" width="10%" style="margin-left: 3px; margin-right: 1px;">'
						elif field.find('M') > -1:
							img = '<td><img src="img/Incidentes_03_Media_01.png" width="12%" style="margin-right: 1px;">'
						elif field.find('A') > -1:
							img = '<td><img src="img/Incidentes_02_Alta_01.ico" width="10%" style="margin-left: 3px; margin-right: 1px;">'
						else:
							img = '<td><img src="img/Incidentes_01_Critica_01.ico" width="12%" style="margin-right: 2px;">'
						
						row_data = row_data_init + img + row_data_head + row_data + '<td>' + field + '</td>'
					elif j == 3:
						row_data += '<td style="width: 6%;">' + field + '</td>'
					else:
						row_data += '<td>' + field + '</td>'
						
				field = ''
				j += 1

		# Se añade el último campo (fecha de cierre):
		field = field.replace("u'","")
		field = field.replace("'","")
		field = field.replace(" ","")
		field = field.replace(")","")
		if field != '0':		# Se formatea la fecha para mostrarla correctamente.
			closing_date = field[6:8] + '/' + field[4:6] + '/' + field[0:4]
		else:
			closing_date = ''
			
		row_data += '<td style="width: 3%;">' + closing_date + '</td>'		
						
		table += row_data + '</tr>'	# Se cierra cada entrada en la tabla (registro).
		
	table += '</table>'				# Por último, se cierra la tabla.
	
	table += '<input type="hidden" name="form_id" value="manage_incident">'		# Se añade el control para el procesado.
	
	table += '</p></form>'			# Se cierra la maquetación HTML.
		
	table_incidents = Markup(table)	# Se formatea para la correcta visualización a través del interfaz Web.
		
	return table_incidents			# Se devuelve la tabla maquetada para su visualización HTML.

	
# Devuelve la tabla HTML maquetada con el contenido de la tabla STAFF de la BBDD Soteria:
def get_staff(cursor):
	cursor.execute("SELECT surname,name,user,email,status FROM STAFF order by status,surname")	# Se realiza la consulta de la cadena formateada. OK.
	result = cursor.fetchall()
	
	table = u'<table style="width: 770px; margin-left: 1%; margin-top: 2%; border: none;"><tr><th style="width: 25%;">Apellidos</th><th style="width: 20%;">Nombre</th><th style="width: 12%;">Usuario</th><th style="width: 23%;">Correo</th><th style="width: 20%;">Situación</th></tr>'	

	field = ''
	
	odd = 's'												# Controla si se encuentra en fila par o impar (para aplicación de CSS).
	
	for row in range(len(result)):							# Cada entrada de result recoge los datos de un registro.
		
		entry = str(result[row]).decode('unicode_escape')	# Recoge los resultados. Cada entrada en result simboliza un registro que encaja con la consulta.
		
		# Se alterna en el sombreado de cada fila de la tabla:
		if odd == 's':
			table = table + '<tr id="odd_row">'
			odd = 'n'
		else:
			table = table + '<tr id="even_row">'
			odd = 's'
		
		column = 0
		
		for i in range(1,len(entry)):

			if entry[i] != ',' or (entry[i-1].isdigit() and entry[i+2].isdigit()) or (entry[i-1].isdigit() and entry[i+2] != 'u') or (entry[i-1] != "'" and entry[i+2] != 'u'):
					field = field + entry[i]
			else:
				field = field.replace("u'","")
				field = field.replace("'","")
				field = field.replace(")","")	# Se depura la cadena.
				
				if column == 2:					# Se guarda el nombre de usuario en caso de que se edite su situación.
					username = field
					username = username.replace(" ","")
				
				if column < 4:
					if column == 0 and row != 0:
						table += '<td>' + field[2:len(field)] + '</td>'
					else:
						table += '<td>' + field + '</td>'
					
				field = ''
				column +=1

		# Se añade el último campo:
		field = field.replace("u'","")
		field = field.replace("'","")
		# Al tratarse del campo status, hay que decodificarlo para mostrarlo de manera legible:

		if field.find('A') > -1:
			table += '<td><form method="post" action=""><select name="new_status_staff" style="margin-left: 12px;">' +\
						'<option name="new_status_staff" value="A" selected="selected">Activo</option>' +\
						'<option name="new_status_staff" value="B">Baja temporal</option>' +\
						'<option name="new_status_staff" value="D">Baja definitiva</option>' +\
						'<option name="new_status_staff" value="V">Vacaciones</option>'
		elif field.find('B') > -1:
			table += '<td><form method="post" action=""><select name="new_status_staff" style="margin-left: 12px;">' +\
						'<option name="new_status_staff" value="A">Activo</option>' +\
						'<option name="new_status_staff" value="B" selected="selected">Baja temporal</option>' +\
						'<option name="new_status_staff" value="D">Baja definitiva</option>' +\
						'<option name="new_status_staff" value="V">Vacaciones</option>'
		elif field.find('D') > -1:
			table += '<td><form method="post" action=""><select name="new_status_staff" disabled="true" style="margin-left: 12px;">' +\
						'<option name="new_status_staff" value="A">Activo</option>' +\
						'<option name="new_status_staff" value="B">Baja temporal</option>' +\
						'<option name="new_status_staff" value="D" selected="selected">Baja definitiva</option>' +\
						'<option name="new_status_staff" value="V">Vacaciones</option>'
		else:
			table += '<td><form method="post" action=""><select name="new_status_staff" style="margin-left: 12px;">' +\
						'<option name="new_status_staff" value="A">Activo</option>' +\
						'<option name="new_status_staff" value="B">Baja temporal</option>' +\
						'<option name="new_status_staff" value="D">Baja definitiva</option>' +\
						'<option name="new_status_staff" value="V" selected="selected">Vacaciones</option>'
			
		table += '<input type="hidden" name="user_n" value="' + username + '"><input type="hidden" name="form_id" value="update_staff_status">'
		table += '<input type="image" src="img/save.png" name="" value="" style="width: 12%;"></form></td>'
						
		table += '</tr>'		# Se cierra cada entrada en la tabla (registro).
		
	table += '</table>'			# Por último, se cierra la tabla.
	
	table_staff = Markup(table)	# Se formatea para la correcta visualización a través del interfaz Web.
	
	return table_staff			# Se devuelve la tabla maquetada HTML.

	
# Genera el interfaz HTML maquetado para la edición de una nueva entrada en la tabla STAFF de la BBDD Soteria:
def get_edit_staff():

	edit_staff = u'<fieldset style="width: 16%; height: 30%; background: #FFFFFF; font-size: 16px; position: absolute; top: 28%; left: 76%; text-align: left;">' +\
							'<legend style="font-size: 20px; font-weight: bold;">Alta de nuevo usuario</legend>' +\
							'<form method="post" action="">' +\
								'<p>Apellidos:<input type="text" size="16" maxlength="36" name="surname" value="" style="margin-left: 8px;"></p>' +\
								'<p>Nombre:<input type="text" size="12" maxlength="20" name="name" value="" style="margin-left: 18px;"></p>' +\
								'<p>Situación:<select name="status_staff" style="margin-left: 12px;">' +\
										'<option name="status_staff" value="A">Activo</option>' +\
										'<option name="status_staff" value="B">Baja temporal</option>' +\
										'<option name="status_staff" value="D">Baja definitiva</option>' +\
										'<option name="status_staff" value="V">Vacaciones</option>' +\
								'<p><input type="image" src="img/new_staff.png" name="" value="" style="width: 25%; margin-left: 40%; margin-top: 10%;"></p>' +\
								'<input type="hidden" name="form_id" value="new_staff">' +\
							'</form>' +\
						'</fieldset>'
	
	return Markup(edit_staff)

	
# Devuelve la tabla HTML maquetada con el contenido de la tabla CSIRT de la BBDD Soteria:
def get_csirt_and_edit(cursor):

	cursor.execute("SELECT surname,name FROM STAFF where status='A' order by surname")
	user_names = cursor.fetchall()	# En primer lugar se extrae el listado de personal. Servirá a la hora de editar los equipos.
	user_list = []
	i = 0
	for row in user_names:
		user_list.append(str(user_names[i][0]) + ', ' + str(user_names[i][1]))
		i += 1

	cursor.execute("SELECT status FROM INCIDENTS where id IN (SELECT id_incid FROM CSIRT)")
	incidents_status_t = cursor.fetchall()
	incidents_status_list = []
	for row in incidents_status_t:
		if row[0] == 'C':
			incidents_status_list.append('No')
		else:
			incidents_status_list.append('Si')
		
	cursor.execute("SELECT id,id_incid,team,team_date FROM CSIRT order by id")	# Se realiza la consulta de la cadena formateada.
	result = cursor.fetchall()
	
	table = u'<table style="width: 620px; margin-left: 3%; margin-top: 2%;"><tr><th style="width: 10%;">ID</th><th style="width: 18%;">INCIDENCIA</th><th style="width: 44%;">Equipo de Respuesta</th><th style="width: 22%;">Conformación</th><th style="width: 6%;">Activo</th></tr>'	

	field = ''
	
	odd = 's'				# Controla si se encuentra en fila par o impar (para aplicación de CSS).

	team_list_names = {}	# Recoge el listado de nombres de los equipos activos y su ID asociado.
	team_list = []			# Recogerá los índices de los Equipos de Respuesta activos y de sus 3 componentes.
	j = 0					# Permitirá controlar la confección del listado de Equipos de Respuesta y su ID asociado.
	jj = 0					# Control de índice solamente para los equipos activos.
	
	index_user_1 = index_user_2 = index_user_3 = 0
	
	for row in range(len(result)):	# Cada entrada de result recoge los datos de un registro.
		
		entry = str(result[row]).decode('unicode_escape')	# Recoge los resultados. Cada entrada en result simboliza un registro que encaja con la consulta.
		
		# Se alterna en el sombreado de cada fila de la tabla:
		if odd == 's':
			table = table + '<tr id="odd_row">'
			odd = 'n'
		else:
			table = table + '<tr id="even_row">'
			odd = 's'
		
		column = 0	# Permitirá controlar en qué columna se encuentra el procesado para operar el contenido de dicha columna convenientemente.
		
		for i in range(1,len(entry)):

			if entry[i] != ',':
					field = field + entry[i]
			else:
				# Se depura la cadena:
				field = field.replace("u'","")
				field = field.replace("'","")
				field = field.replace("(","")
				field = field.replace(")","")					
				field = field.replace("[","")
				field = field.replace("]","")
				
				if column == 2:		# Se expanden los nombres completos del personal de seguridad.
				
					table += '<td>'
				
					cursor.execute("SELECT surname,name FROM STAFF where user=%s", (field[1:10],))	# Se realiza la consulta de la cadena formateada.
					user_name = cursor.fetchall()
					user_name_t1 = user_name[0][0] + ', ' + user_name[0][1]
					table += user_name_t1 + '<br/>'
					cursor.execute("SELECT surname,name FROM STAFF where user=%s", (field[10:19],))	# Se realiza la consulta de la cadena formateada.
					user_name = cursor.fetchall()
					user_name_t2 = user_name[0][0] + ', ' + user_name[0][1]
					table += user_name_t2 + '<br/>'
					cursor.execute("SELECT surname,name FROM STAFF where user=%s", (field[19:28],))	# Se realiza la consulta de la cadena formateada.
					user_name = cursor.fetchall()
					user_name_t3 = user_name[0][0] + ', ' + user_name[0][1]
					table += user_name_t3 + '</td>'
					
					if incidents_status_list[j] == 'Si':	# Equipo de Respuesta actualmente activo.
					
						k = 0
						for row in user_list:
							if user_name_t1 == row:
								index_user_1 = k
							elif user_name_t2 == row:
								index_user_2 = k
							elif user_name_t3 == row:
								index_user_3 = k							
							k += 1
								
						team_list.append([jj,index_user_1,index_user_2,index_user_3])
						team_list_names[jj,1] = user_name_t1
						team_list_names[jj,2] = user_name_t2
						team_list_names[jj,3] = user_name_t3
						
						jj += 1
						
				else:
					if column == 0:
						table += '<td>' + field[len(field)-6:len(field)] + '</td>'
						if incidents_status_list[j] == 'Si':	# Equipo de Respuesta actualmente activo.
							team_list_names[jj,0] = field[len(field)-6:len(field)]
					else:
						table += '<td>' + field + '</td>'
					
				field = ''
				column +=1

		# Se añade el último campo:
		field = field.replace("u'","")
		field = field.replace("'","")
		field = field.replace(")","")
		table += '<td>' + field + '</td>'
		
		# Se añade la columna que informa si el CSIRT se encuentra activo o no:
		table += '<td>' + incidents_status_list[j] + '</td>'
						
		table += '</tr>'		# Se cierra cada entrada en la tabla (registro).
		
		j += 1
	
	table += '</table><br/>'	# Por último, se cierra la tabla.
	
	num_teams = jj				# Se guarda el número de Equipos de Respuesta registrados hasta el momento.
	
	# Generación del interfaz de edición de los Equipos de Respuesta:
						
	edit_csirt = u'<fieldset style="width: 18%; height: 40%; background: #FFFFFF; font-size: 16px; position: absolute; top: 27%; left: 68%; text-align: left;">\n' +\
	'<legend style="font-size: 20px; font-weight: bold;">Edición de Equipos</legend>\n' +\
	'<form method="post" action="">\n' +\
	'<p>CSIRT:<select name="csirt_id" id="csirt_id" style="margin-left: 12px;">\n'
		
	for i in range(jj):
		edit_csirt += '<option name="csirt_id" id="csirt_id" value=' + str(i) + '>' + str(team_list_names[i,0]) + '</option>\n'

	jj = 0	# Se establece por defecto para la primera entrada. El resto debe controlarse según selección del usuario en el interfaz web mediante JavaScript.
		
	edit_csirt += '</select></p><p>Componente 1 (Responsable):<select name="staff_1" id="staff_1" style="margin-left: 12px;">\n'
	i = 0
	for row in user_names:
		if str(user_names[i][0]) + ', ' + str(user_names[i][1]) == team_list_names[jj,1]:
			edit_csirt += '<option name="staff_1" value=' + str(i) + ' selected="selected">' + team_list_names[jj,1] + '</option>\n'
			team_1 = i
		else:
			edit_csirt += '<option name="staff_1" value=' + str(i) + '>' + str(user_names[i][0]) + ', ' + str(user_names[i][1]) + '</option>\n'
		i += 1
	
	edit_csirt += '</select></p><p>Componente 2:<select name="staff_2" id="staff_2" style="margin-left: 12px;">\n'
	i = 0
	for row in user_names:
		if str(user_names[i][0]) + ', ' + str(user_names[i][1]) == team_list_names[jj,2]:
			edit_csirt += '<option name="staff_2" value=' + str(i) + ' selected="selected">' + team_list_names[jj,2] + '</option>\n'
			team_2 = i
		else:
			edit_csirt += '<option name="staff_2" value=' + str(i) + '>' + str(user_names[i][0]) + ', ' + str(user_names[i][1]) + '</option>\n'
		i += 1

	edit_csirt += '</select></p><p>Componente 3:<select name="staff_3" id="staff_3" style="margin-left: 12px;">\n'
	i = 0
	for row in user_names:
		if str(user_names[i][0]) + ', ' + str(user_names[i][1]) == team_list_names[jj,3]:
			edit_csirt += '<option name="staff_3" value=' + str(i) + ' selected="selected">' + team_list_names[jj,3] + '</option>\n'
			team_3 = i
		else:
			edit_csirt += '<option name="staff_3" value=' + str(i) + '>' + str(user_names[i][0]) + ', ' + str(user_names[i][1]) + '</option>\n'
		i += 1

	edit_csirt += '</select></p><p><input type="image" src="img/team_update.png" name="" value="" style="width: 25%; margin-left: 40%; margin-top: 5%;"></p>\n' +\
		'<input type="hidden" name="form_id" value="edit_csirt">\n' +\
	'</form></fieldset>\n'
	
	team_list_index = team_list		# Lista de índices para control en el interfaz web.
	
	team_list_csirts = []			# Recoge el listado de ID's de Equipos de Respuesta conformados hasta el momento.
	
	for i in range(num_teams):
		team_list_csirts.append(team_list_names[i,0])
	
	return Markup(table+edit_csirt),team_list_index,team_list_csirts,user_list
	# Se devuelven los siguientes datos:
	# La tabla y el interfaz de edición de los Equipos de Respuesta maquetados HTML.
	# El listado de índices para el control de selección desde el interfaz web.
	# El listado de equipos (ID's).
	# El listado de usuarios.


# Función para generar el interfaz de la pestaña Conocimiento:
def get_knowledge(cursor,option):
	
	knowledge = ''
	
	cursor.execute("select id,description from ENS")
	result_type = cursor.fetchall()
	cursor.execute("select id from NOTIFIED")
	result_notified = cursor.fetchall()
	
	if option == 0:
		knowledge = '<fieldset style="width: 38%; height: 50%; background: #FFFFFF; font-size: 16px; font-weight: bold; '+\
			'margin-left: 240px; margin-top: 40px; text-align: left;">' +\
			'<legend style="font-size: 20px;">Seleccione el histórico que desee consultar</legend>' +\
			'<form method="post" action="">' +\
			'<p>Incidencias por categoría: <select name="type" id="type">'
		for row in result_type:
			knowledge += '<option name="type" value="' + str(row[0]) + '">' + str(row[1]) + '</option>' 
		knowledge += '</select></p>' +\
			'<input type="image" src="img/light.png" style="width: 10%; margin-left: 45%;"><br/><br/>' +\
			'<input type="hidden" name="form_id" value="knowledge_type">' +\
			'</form>' +\
			'<form method="post" action="">' +\
			'<p>Incidencias notificadas: <select name="id_incid" id="id_incid">'
		for row in result_notified:
			knowledge += '<option name="id_incid" value="' + str(row[0]) + '">' + str(row[0]) + '</option>'	
		knowledge += '</select><input type="image" src="img/notified.png" style="width: 10%; margin-left: 53%; margin-top: -9%;"></p>' +\
			'<input type="hidden" name="form_id" value="knowledge_notified">' +\
			'</fieldset>'+\
			'</form>'
			
			
			
	
	# 2º Interfaz, una vez seleccionado el tipo de incidencia:
	# cursor.execute("SELECT id,id_csirt, from INCIDENTS where type=%s and status=C", (type,))
	
	return Markup(knowledge)

	
# Devuelve la tabla maquetada HTML para la visualización detallada por tipo de incidencia:
def get_knowledge_type(cursor,type):

	cursor.execute("select description from ENS where id=%s", (type,))
	result = cursor.fetchall()
	description = result[0][0]
	
	table_type = '<h1>' + str(description) + '</h1>'

	cursor.execute("select pm_info,details,reports from INCIDENTS where type=%s and status='C'", (type,))
	result = cursor.fetchall()
	
	table_type += '<table style="width: 98%; background=#FFFFFF; border: 1px solid #ddd;"><tr style="color: DarkBlue;"><th>MEDIDAS DE PROTECCIÓN</th><th></th><th>DETALLES</th><th></th><th>INFORMES</th></tr>'
	table_type += '<tr style="height: 10px;"> </tr>'
	
	for row in result:
		reports = extract_reports (str(row[2]))
		pm_extended = compound_pm_extended(str(row[0]))
		table_type += '<tr><td style="width: 40%; border-bottom: 1px solid #6666AA;">' + pm_extended + '</td><td style="width: 1%;"></td>' + '<td style="width: 30%; vertical-align: top; border-bottom: 1px solid #6666AA;">' + str(row[1]) + '</td><td style="width: 1%;"></td>' + '<td style="width: 30%; vertical-align: top; border-bottom: 1px solid #6666AA;">' + reports + '</td></tr>'
		table_type += '<tr style="height: 10px;"> </tr>'
		
	table_type += '</table>'

	return Markup(table_type)


# Función para generar el interfaz de la pestaña Análisis:
def get_stats_option():
	
	options = [u'Número de Incidencias', u'Intervalo Detección <-> Notificación', u'Intervalo Detección <-> Cierre', 'Falsos Positivos', 'Falsos Negativos',\
	'Distribución por Severidad', u'Distribución por Categorías de Incidencias (tipo)', 'Equipos de Respuesta', 'Escalado de Incidencias', u'Distribución de Altas Manuales y Automáticas']
	
	i = 0
	
	stats = '<fieldset style="width: 38%; height: 44%; background: #FFFFFF; font-size: 16px; font-weight: bold; '+\
			'margin-left: 240px; margin-top: 40px; text-align: left;">' +\
			'<legend style="font-size: 20px;">Seleccione el tipo de información y el periodo</legend>' +\
			'<form method="post" action="">' +\
			'<p>Datos relativos a: <select name="option" id="option">'
	for entry in options:
		stats += '<option name="option" value="' + str(i) + '">' + str(entry) + '</option>'
		i += 1
	stats += '</select></p><p><input type="radio" name="lapse" id="yearly" value="yearly" checked="checked">  Anual<input type="radio" name="lapse" ' +\
	'id="monthly" value="monthly">  Mensual <select name="year" id="year">'
	current_year = 2015
	while current_year <= int(time.strftime("%Y")):
		stats += '<option name="year" value="' + str(current_year) + '">' + str(current_year) + '</option>'
		current_year += 1
	stats += '<input type="radio" name="lapse" id="custom" value="custom">  Intervalo:<br/><br/>&emsp;Inicio:<input type="date" name="start_date" id="start_date" ' +\
	'value="" style="margin-left: 10px;">&emsp;Fin:<input type="date" name="stop_date" id="stop_date" value="" style="margin-left: 5px;"><br/><br/>' + \
	'Tipo de Gráfica: <select name="graph_type" id="graph_type"><option name="graph_type" value="0">Barras verticales</option><option name="graph_type" value="1">' +\
	'Barras horizontales</option><option name="graph_type" value="2">Línea</option>' +\
	'</p><br/><input type="image" src="img/stats.png" style="width: 10%; margin-left: 45%; margin-top: 12px;"><input type="hidden" name="form_id" value="stats">' +\
	'</form></fieldset>'

	return Markup(stats)


# Función para generar las estadísticas y datos asociados para el apartado de Análisis:
def get_stats(option,cursor,lapse,year,start_date,stop_date):

	graph = ''
	data = []
	num_elements = 0
	stats = []
	label = ''
	labels = []
	ave = 0
	min = 0
	max = 0
	date_min = ''
	date_max = ''
	
	graph = 'incid_stats'	# Por ahora, se trabajará con una misma estructura de gráficos.
	
	if option == '0':		# Número de Incidencias.
	
		#graph = 'incid_stats'	# En caso de que sea necesario personalizar los gráficos según los datos...
		
		if lapse == 'yearly':

			cursor.execute("select count(id) from INCIDENTS where id like '2015%'")
			result = cursor.fetchall()
			data.append(int(result[0][0]))		

			cursor.execute("select count(id) from INCIDENTS where id like '2016%'")
			result = cursor.fetchall()
			data.append(int(result[0][0]))

			cursor.execute("select count(id) from INCIDENTS where id like '2017%'")
			result = cursor.fetchall()
			data.append(int(result[0][0]))

			cursor.execute("select count(id) from INCIDENTS where id like '2018%'")
			result = cursor.fetchall()
			data.append(int(result[0][0]))
			
			labels = ['2015', '2016', '2017', '2018']
			
			min = 200	# Se puede indicar el máximo estimado superior que se desee. Los datasets estaban generados para un máximo de 150 por año.
			max = 0
			
			year_min = 0
			year_max = 0
			
			global_t = 0
			
			num_elements = len(data)
			
			for i in range(num_elements):
				global_t += data[i]
				if data[i] < min:
					min = data[i]
					year_min = i
				if data[i] > max:
					max = data[i]
					year_max = i

			ave = global_t / (i+1)
			
			year_min += 2015
			year_max += 2015
			
			date_min = ' (año: ' + str(year_min) + ')'
			date_max = ' (año: ' + str(year_max) + ')'
			
			stats = [global_t, ave, min, date_min, max, date_max]
			
			label = u'Número de Incidencias anuales'
			
		elif lapse == 'monthly':
		
			detect_date_init = year+'01000000'
			detect_date_end = year+'02000000'
			
			for i in range(1,13):
							
				cursor.execute("select count(id) from INCIDENTS where detect_date>%s and detect_date<%s", (detect_date_init,detect_date_end))
				result = cursor.fetchall()
				data.append(int(result[0][0]))
				
				if i < 8:
					detect_date_init = year+'0'+str(i+1)+'000000'
					detect_date_end = year+'0'+str(i+2)+'000000'
				elif i == 8:
					detect_date_init = year+'09000000'
					detect_date_end = year+'10000000'
				elif i == 9:
					detect_date_init = year+'10000000'
					detect_date_end = year+'11000000'
				else:
					detect_date_init = year+'1'+str(i+1-10)+'000000'
					detect_date_end = year+'1'+str(i+2-10)+'000000'
					
			labels = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
			
			min = 17	# 200/12 ~ 17 -> máximo número estimado de incidencias por mes. Se puede ajustar al valor más alto que se desee.
			max = 0
			
			month_min = 0
			month_max = 0
			
			global_t = 0
			
			num_elements = len(data)
			
			for i in range(0,num_elements):
				global_t += data[i]
				if data[i] < min:
					min = data[i]
					month_min = i
				elif data[i] > max:
					max = data[i]
					month_max = i

			ave = global_t / i -1
			
			month_min = labels[month_min]
			month_max = labels[month_max]
			
			date_min = ' (mes: ' + str(month_min) + ')'
			date_max = ' (mes: ' + str(month_max) + ')'
			
			stats = [global_t, ave, min, date_min, max, date_max]
			
			label = u'Número de Incidencias según mes para el año ' + year
		
		else:	# Por intervalo de tiempo (custom):
		
			# En este caso el recuento se hace de manera diaria:
			
			# Se ajusta al formato conveniente para poder comparar fechas: AAAA-MM-DD => AAAAMMDD, e ir haciendo el incremento en días!
			start_date_view = start_date[8:10] + '/' + start_date[5:7] + '/' + start_date[0:4]
			stop_date_view = stop_date[8:10] + '/' + stop_date[5:7] + '/' + stop_date[0:4]
			start_date = start_date.replace("-","")
			stop_date = stop_date.replace("-","")
			stop_date = int(stop_date)

			current_day = datetime
			current_day = date(int(start_date[0:4]), int(start_date[4:6]), int(start_date[6:8]))
			current_day_t = str(current_day).replace("-","")
			current_day_int = int(current_day_t)
			day = timedelta(days=1)
			
			min = 6		# Se indica un número de incidencias diario suficiente elevado que sea poco probable se superar.
			max = 0		# En el caso del máximo se inicializa con el mínimo.
			
			while current_day_int <= stop_date:
			
				current_day_t = str(current_day).replace("-","")
				query_text = "select count(id) from INCIDENTS WHERE detect_date LIKE '%%%s%%'" % (current_day_t)
				cursor.execute(query_text)
				result = cursor.fetchall()
				data.append(int(result[0][0]))
				if int(result[0][0]) < min:
					min = int(result[0][0])
					date_min = str(current_day.strftime("%d/%m/%Y"))
				if int(result[0][0]) > max:
					max = int(result[0][0])
					date_max = str(current_day.strftime("%d/%m/%Y"))
				labels.append(str(current_day.strftime("%d/%m/%Y")))
				current_day += day
				current_day_t = str(current_day).replace("-","")
				current_day_int = int(current_day_t)

			num_elements = len(data)
			
			global_t = sum(data)
			
			ave = float((global_t+0.0)/(num_elements+0.0))
			ave = round(ave,2)
			
			stats = [global_t, ave, min, date_min, max, date_max]
				
			label = u'Incidencias por día durante el periodo ' + start_date_view + ' a ' + stop_date_view
		
	elif option == '1':		# Intervalo Detección <-> Notificación:
	
		#graph = 'lapse_detect_notify'	# En caso de que sea necesario personalizar los gráficos según los datos...
	
		# Serán de interés aquellas aquellas incidencias notificadas, es decir, de severidad Crítica o Alta:
		cursor.execute("SELECT detect_date,notify_date,id FROM INCIDENTS WHERE severity='C' or severity='A'")
		result = cursor.fetchall()
		
		min = 15	# Se inicializa a un valor elevado.
		max = 0		# Se inicializa al mínimo posible.
		
		# Se recorre la lista doble calculando la diferencia entre ambas fechas.
		# Como la diferencia es muy baja, del orden de muy pocos minutos (en la realidad, incluso menos), se trabaja solo con las horas y minutos:
		for entry in result:
			# entry[0] alberga la fecha de detección con formato: AAAAMMDDHHmm, mientras que entry[1] alberga la fecha de notificación con formato DD/MM/AAAA HH:mm.
			# Hay que establecer por tanto un formato común para comparar, que será HHmm. Se extraerá y trabajará las HH y los mm por separado:
			hh_detect = entry[0][8:10]
			mm_detect = entry[0][10:12]
			hh_notify = entry[1][11:13]
			mm_notify = entry[1][14:16]
		
			diff = 0
			
		# El resultado se trabajará en minutos:
			if hh_notify == hh_detect:
				diff = int(mm_notify) - int(mm_detect)
			else:
				diff = int(mm_notify) + 60 - int(mm_detect)
				
			data.append(diff)
			
			if diff < min:
				min = diff
				incid_min = '(incidencia ' + str(entry[2]) + ')'
			if diff > max:
				max = diff
				incid_max = '(incidencia ' + str(entry[2]) + ')'
				
			labels.append(entry[2])

		num_elements = len(data)
				
		global_t = sum(data)

		ave = (global_t+0.0)/(num_elements+0.0)
		ave = round(ave,2)
		
		stats = [0, ave, min, incid_min, max, incid_max]	# En este caso, la suma global de los tiempos no es un dato relevante.
			
		label = u'Intervalo entre la Detección y la Notificación de la Incidencia'

	elif option == '2':		# Intervalo Detección <-> Cierre:
	
		#graph = 'lapse_detect_closing'	# En caso de que sea necesario personalizar los gráficos según los datos...
	
		# Serán de interés aquellas incidencias que se encuentren cerradas:
		cursor.execute("SELECT detect_date,closing_date,id FROM INCIDENTS WHERE status='C'")
		result = cursor.fetchall()
		
		min = 2*354	# Se inicializa a un valor elevado, en este caso, 2 años. Se considerará que, por política de seguridad, se mantengan abiertas un máximo de 2 años.
		max = 0		# Se inicializa al mínimo posible.
		
		# Se recorre la lista doble calculando la diferencia entre ambas fechas.
		# Como la diferencia es muy baja, del orden de muy pocos minutos (en la realidad, incluso menos), se trabaja solo con las horas y minutos:
		for entry in result:
			# entry[0] alberga la fecha de detección con formato: AAAAMMDDHHmm, mientras que entry[1] alberga la fecha de notificación con el mismo formato.
			# Por tanto, se puede comparar directamente. Como el tiempo transcurrido  entre la detección y la solución(cierre) de una incidencia suele ser
			# medio o largo plazo, se trabajará con una resolución de hasta días => AAAAMMDD, y el resultado se expresará en días.
			aaaa_detect = entry[0][0:4]
			aaaa_closing = entry[1][0:4]
			mm_detect = entry[0][4:6]
			mm_closing = entry[1][4:6]
			dd_detect = entry[0][6:8]
			dd_closing = entry[1][6:8]
			
			detect_date = date(int(aaaa_detect),int(mm_detect),int(dd_detect))
			closing_date = date(int(aaaa_closing),int(mm_closing),int(dd_closing))
		
			diff = abs(closing_date - detect_date).days
				
			data.append(diff)
			
			if diff < min:
				min = diff
				incid_min = '(incidencia ' + str(entry[2]) + ')'
			if diff > max:
				max = diff
				incid_max = '(incidencia ' + str(entry[2]) + ')'
				
			labels.append(entry[2])

		num_elements = len(data)
				
		global_t = sum(data)

		ave = global_t / num_elements
		
		stats = [0, ave, min, incid_min, max, incid_max]	# En este caso, la suma global de los tiempos no es un dato relevante.
			
		label = u'Intervalo entre la Detección y el Cierre de la Incidencia'
		
	if option == '3' or option == '4':		# Falsos Positivos.
	
		# En este caso, los datos de interés son: recuento total, relación entre número de FP's y número de incidencias e intervalo medio entre FP's.
		# Al igual que ocurre con los intervalos Detección<->Notificación y Detección<->Cierre, para que los datos estadísticos sean relevantes hay que
		# aplicarlo sobre un periodo suficientemente largo, por lo que el cálculo del intervalo medio se aplicará para todo el periodo de observación:
		# 3 años + 11 meses:
		
		cursor.execute("select count(id) from INCIDENTS")							# Total de incidencias.	
		result = cursor.fetchall()
		global_t = result[0][0]
		
		if option == '3':
			cursor.execute("select count(id) from INCIDENTS where false_p='S'")		# Total de FP's.
		else:
			cursor.execute("select count(id) from INCIDENTS where false_n='S'")		# Total de FN's.
		result = cursor.fetchall()
		num_falses = result[0][0]
		
		falses_incids_relation = round((int(num_falses)+0.0)/(int(global_t)+0.0)*100,2)	# Relación FP's/total incidencias == proporción de FP's.
			
		lapse = (3*365 + 11*30) / num_falses											# Periodo medio, en dias, entre dos FP's.
		
		stats = [num_falses, falses_incids_relation, lapse, '', '', '']					# Se generan los datos estadísticos a devolver.
		
		# Por otro lado, de cara a la representación gráfica, se genera el vector: valor 1 para los días con FP, y 0 para los días sin FP:
		if option == '3':
			cursor.execute("select id,false_p from INCIDENTS")
		else:
			cursor.execute("select id,false_n from INCIDENTS")
		result = cursor.fetchall()
		
		for entry in result:
			if entry[1] == 'S':
				labels.append('')
				data.append(1)
			else:
				labels.append('')
				data.append(0)
		
		num_elements = len(data)
		
		if option == '3':
			label = 'Informe sobre Falsos Positivos'
		else:
			label = 'Informe sobre Falsos Negativos'
			
	elif option == '6':		# Distribución por categorías de incidencias.
	
		cursor.execute("select id from ENS")	# Se extrae el conjunto de categorías de incidencias de la tabla ENS.
		result = cursor.fetchall()
		
		min = 1000	# Se inicializa a un valor elevado.
		max = 0		# Se inicializa al mínimo posible.
		
		for entry in result:
			cursor.execute("select count(id) from INCIDENTS where type=%s", (entry[0],))
			result_inner = cursor.fetchall()
			data.append(int(result_inner[0][0]))
			labels.append(str(entry[0]))
			if int(result_inner[0][0]) < min:
				min = int(result_inner[0][0])
				type_min = '(' + str(entry[0]) + ')'
			if int(result_inner[0][0]) > max:
				max = int(result_inner[0][0])
				type_max = '(' + str(entry[0]) + ')'

		num_elements = len(data)
		global_t = sum(data)
		ave = round((global_t+0.0)/(num_elements+0.0),2)
		
		stats = [global_t, ave, min, type_min, max, type_max]
		
		label = u'Distribución por Categorías de Incidencias (tipo)'

	elif option == '7':		# Equipos de Respuesta.
	
		cursor.execute("select count(id) from INCIDENTS")	# Se extrae el recuento total de incidencias de cara a las estadísticas.
		result = cursor.fetchall()
		num_incids = int(result[0][0])
	
		cursor.execute("select id_csirt,detect_date from INCIDENTS where csirt='S'")
		result = cursor.fetchall()
		
		for entry in result:
			data.append(1)
			labels.append(str(entry[0])+' '+str(entry[1])[6:8]+'/'+str(entry[1])[4:6]+'/'+str(entry[1])[0:4])
			
		num_elements = len(data)
		global_t = sum(data)
		relation = round((global_t+0.0)/(num_incids+0.0)*100,2)
		
		stats = [global_t, num_incids, relation, '', 0, '']
		
		label = 'Equipos de Respuesta'
	
	elif option == '8':		# Escalado de incidencias.

		cursor.execute("select count(id) from INCIDENTS")	# Se extrae el recuento total de incidencias de cara a las estadísticas.
		result = cursor.fetchall()
		num_incids = int(result[0][0])
	
		cursor.execute("select id,detect_date from INCIDENTS where details LIKE '%se escala la incidencia%'")
		result = cursor.fetchall()
		
		for entry in result:
			data.append(1)
			labels.append(str(entry[0])+' '+str(entry[1])[6:8]+'/'+str(entry[1])[4:6]+'/'+str(entry[1])[0:4])
			
		num_elements = len(data)
		global_t = sum(data)
		relation = round((global_t+0.0)/(num_incids+0.0)*100,2)
		
		stats = [global_t, num_incids, relation, '', 0, '']
		
		label = 'Incidencias Escaladas'
		
	return graph, data, num_elements, stats, Markup(label), Markup(labels)
	

# Generación de los datos de las gráficas y estadísticas para el estudio de la severidad:
def get_stats_severity(cursor):

	graph = 'incid_stats'
	#graph = 'severity'		# En caso de que sea necesario personalizar los gráficos según los datos...
	
	data_set1 = []
	data_set2 = []
	data_set3 = []
	data_set4 = []
	labels = []
	label = []

	# En este caso, se realiza contabilizan el número de incidencias según severidad y se muestra según el intervalo seleccionado.
	# Se parte del caso más directo, el estudio por años:
	year_init = 201500000000
	year_end = 201513000000
	year_stop = (int(time.strftime("%Y"))+1) * 100000000
	
	while year_end < year_stop:
		cursor.execute("select count(id) from INCIDENTS where detect_date>%s and detect_date<%s and severity='C'", (str(year_init),str(year_end)))
		result = cursor.fetchall()
		data_set1.append(result[0][0])
		cursor.execute("select count(id) from INCIDENTS where detect_date>%s and detect_date<%s and severity='A'", (str(year_init),str(year_end)))
		result = cursor.fetchall()
		data_set2.append(result[0][0])
		cursor.execute("select count(id) from INCIDENTS where detect_date>%s and detect_date<%s and severity='M'", (str(year_init),str(year_end)))
		result = cursor.fetchall()
		data_set3.append(result[0][0])
		cursor.execute("select count(id) from INCIDENTS where detect_date>%s and detect_date<%s and severity='B'", (str(year_init),str(year_end)))
		result = cursor.fetchall()
		data_set4.append(result[0][0])
		
		labels.append(str(year_init)[0:4])
		
		year_init += 100000000
		year_end += 100000000

	total_c = sum(data_set1)
	total_a = sum(data_set2)
	total_m = sum(data_set3)
	total_b = sum(data_set4)
	total = total_c + total_a + total_m + total_b
	stake_c = round((total_c+0.0)/(total+0.0)*100,2)
	stake_a = round((total_a+0.0)/(total+0.0)*100,2)
	stake_m = round((total_m+0.0)/(total+0.0)*100,2)
	stake_b = round((total_b+0.0)/(total+0.0)*100,2)
	
	stats = [total,total_c,total_a,total_m,total_b,stake_c,stake_a,stake_m,stake_b]
		
	label = ['Severidad Critica', 'Severidad Alta', 'Severidad Media', 'Severidad Baja']
		
	return graph, data_set1, data_set2, data_set3, data_set4, stats, label, Markup(labels)
	

# Generación de los datos de las gráficas y estadísticas para el estudio del origen (alta manual por personal de seguridad, o automática por el SIEM):
def get_stats_originator(cursor):

	graph = 'incid_stats'
	#graph = 'originator'		# En caso de que sea necesario personalizar los gráficos según los datos...
	
	data_set1 = []
	data_set2 = []
	labels = []
	label = []

	# En este caso, se realiza contabilizan el número de incidencias según severidad y se muestra según el intervalo seleccionado.
	# Se parte del caso más directo, el estudio por años:
	year_init = 201500000000
	year_end = 201513000000
	year_stop = (int(time.strftime("%Y"))+1) * 100000000
	
	while year_end < year_stop:
		cursor.execute("select count(id) from INCIDENTS where detect_date>%s and detect_date<%s and originator='SIEM'", (str(year_init),str(year_end)))
		result = cursor.fetchall()
		data_set1.append(result[0][0])
		cursor.execute("select count(id) from INCIDENTS where detect_date>%s and detect_date<%s and originator<>'SIEM'", (str(year_init),str(year_end)))
		result = cursor.fetchall()
		data_set2.append(result[0][0])
		
		labels.append(str(year_init)[0:4])
		
		year_init += 100000000
		year_end += 100000000

	total_siem = sum(data_set1)
	total_personal = sum(data_set2)
	total = total_siem + total_personal
	stake_siem = round((total_siem+0.0)/(total+0.0)*100,2)
	stake_personal = round((total_personal+0.0)/(total+0.0)*100,2)
	
	stats = [total,total_siem,total_personal,stake_siem,stake_personal]
		
	label = ['Originador: sistema SIEM', 'Originador: Personal de Seguridad de la Información']
		
	return graph, data_set1, data_set2, stats, label, Markup(labels)
	
	
# Generación del contenido de la pestaña Información, maquetada para la correcta visualización HTML:
def get_info():

	info = '<fieldset style="width: 32%; height: 26%; background: #FFFFFF; font-size: 16px; position: absolute; top: 18%; left: 18%;">' +\
	'<legend style="font-size: 20px; font-weight: bold; color: #000000;">¿Por qué Soteria?</legend>' +\
		'<p style="font-size: 16px; color: #000000; text-align: center; background: #E0FFFF; margin-top: 8px; border-left: 10px solid #00FFFF;">' +\
			'Simboliza el estado deseado por cualquier persona responsable de un sistema de seguridad: "estar a salvo".<br/>' +\
			'Su origen procede de la mitología griega: Soteria era una diosa que personificaba el concepto abstracto de "estar a salvo", salvación, liberación o preservación.<br/>' +\
		'</p>' +\
		'<p style="text-align: center;"><a href="https://es.wikipedia.org/wiki/Soteria_(mitolog%C3%ADa)"><img src="img/Soteria.jpg" width=10%></a></p>' +\
	'</fieldset>' +\
	'<fieldset style="width: 40%; height: 26%; background: #FFFFFF; font-size: 16px; position: absolute; top: 18%; left: 53%;">' +\
	'<legend style="font-size: 20px; font-weight: bold;">Enlaces a normativa de interés</legend>' +\
		'<table style="text-align: center;">' +\
			'<tr><th style="width: 33%;"></th><th style="width: 33%;"></th><th style="width: 33%;"></th></tr>' +\
			'<tr>' +\
				'<td>' +\
					'<a href="https://www.ccn.cni.es/index.php/es/menu-guias-ccn-stic-es"><img src="img/guias_ccn-stic.png" width=75%></a><br/></br>' +\
					'<a href="https://www.ccn-cert.cni.es/series-ccn-stic/800-guia-esquema-nacional-de-seguridad/505-ccn-stic-804-medidas-de-implantancion-del-ens/file.html"><img src="img/ccs-stic_804.png" width=65%></a><br/><br/>' +\
					'<a href="https://www.ccn-cert.cni.es/pdf/guias/series-ccn-stic/800-guia-esquema-nacional-de-seguridad/3067-ccn-stic-819-medidas-compensatorias/file.html"><img src="img/ccs-stic_819.png" width=65%></a>' +\
				'</td>' +\
				'<td>' +\
					'<a href="https://www.boe.es/buscar/act.php?id=BOE-A-2010-1330"><img src="img/ENS.png" width=55%></a><br/>' +\
					'<a href="https://www.ccn-cert.cni.es/ens.html"><img src="img/ens_en_ccn.png" width=40%></a><br/>' +\
					'<a href="http://www.defensa.gob.es/Galerias/portalservicios/seginfoemp/OM_76_06_Politica_Seguridad_Informacion_MINISDEF.pdf"><img src="img/MINISDEF.png" width=65%></a><br/>' +\
				'</td>' +\
				'<td>' +\
					'<a href="https://www.boe.es/doue/2016/119/L00001-00088.pdf"><img src="img/RGPD.png" width=35%></a><br/>' +\
					'<a href="https://www.boe.es/buscar/doc.php?id=BOE-A-2018-10751"><img src="img/RGPD_deroga_LPOD.png" width=55%></a><br/>' +\
					'<a href="https://sedeagpd.gob.es/sede-electronica-web/vistas/formBrechaSeguridad/procedimientoBrechaSeguridad.jsf"><img src="img/AEPD_Notificaciones.png" width=100%></a>' +\
				'</td>' +\
			'</tr>' +\
		'</table>' +\
	'</fieldset>' +\
	'<fieldset style="width: 32%; height: 26%; background: #FFFFFF; font-size: 16px; position: absolute; top: 48%; left: 18%;">' +\
	'<legend style="font-size: 20px; font-weight: bold;">Revistas y Libros del Sector</legend>' +\
		'<table style="font-size: 8px;">' +\
			'<tr><th style="width: 5%;"></th><th style="width: 35%;"></th><th style="width: 5%;"></th><th style="width: 45%;"></th><th style="width: 5%;"></th></tr>' +\
			'<tr>' +\
				'<td></td>' +\
				'<td>' +\
					'<a href="https://revistasic.es/"><img src="img/revistaSIC.jpg" width=80%></a><br/><br/>' +\
					'<a href="http://www.redseguridad.com/"><img src="img/revista_redseguridad.png" width=90%></a><br/><br/>' +\
					'<a href="https://cuadernosdeseguridad.com/cuadernos-de-seguridad/"><img src="img/cuadernos_de_seguridad.png" width=90%></a>' +\
				'</td>' +\
				'<td></td>' +\
				'<td>' +\
					'<table style="text-align: center;">' +\
						'<tr><th style="width: 33%;"></th><th style="width: 33%;"></th><th style="width: 33%;"></th></tr>' +\
						'<tr><a href="http://www.iso27000.es/boletines.html"><img src="img/iso27000es.png" style="width: 70%; margin-left: 30px; margin-top: -20px;"></a><tr>' +\
						'<tr style="height: 10px;"></tr>' +\
						'<tr>' +\
							'<td><a href="https://www.paraninfo.es/catalogo/9788497325028/?gclid=EAIaIQobChMIpLjf9Mam3gIVpp3tCh2XtQ6zEAYYAiABEgLscPD_BwE"><img src="img/Libro1.jpg" width=90%></a></td>' +\
							'<td><a href="https://www.amazon.es/Reflexiones-convencionales-gerencia-seguridad-informaci%C3%B3n/dp/8499641199/ref=sr_1_19?s=books&ie=UTF8&qid=1540640013&sr=1-19&keywords=seguridad+de+la+informacion"><img src="img/Libro2.jpg" width=90%></a></td>' +\
							'<td><a href="https://www.unebook.es/es/libro/ciberseguridad-global_40375"><img src="img/Libro3.jpg" width=82%></a></td>' +\
						'</tr>' +\
					'</table>' +\
				'</td>' +\
				'<td></td>' +\
			'</tr>' +\
		'</table>' +\
	'</fieldset>' +\
	'<fieldset style="width: 40%; height: 26%; background: #FFFFFF; font-size: 16px; position: absolute; top: 48%; left: 53%;">' +\
	'<legend style="font-size: 20px; font-weight: bold;">Servicios de noticias e información de interés</legend>' +\
		'<table>' +\
			'<tr><th style="width: 33%;"></th><th style="width: 33%;"></th><th style="width: 33%;"></th></tr>' +\
			'<tr>' +\
				'<td>' +\
					'<a href="https://securmatica.com/"><img src="img/SECURMATICA.png" width=55%></a><br/><br/>' +\
					'<a href="https://www.elevenpaths.com/"><img src="img/ElevenPaths.png" width=55%></a><br/><br/>' +\
					'<a href="https://www.incibe.es/"><img src="img/incibe.png" width=75%></a>' +\
				'</td>' +\
				'<td>' +\
					'<a href="https://www.ismsforum.es/"><img src="img/isms_forum_spain.png" width=55%></a><br/>' +\
					'<a href="https://www.csirt.es"><img src="img/csirt_es.png" width=65%></a><br/><br/>' +\
					'<a href="https://www.segurinfo.org/"><img src="img/segurinfo.png" width=65%></a><br/><br/>' +\
				'</td>' +\
				'<td>' +\
					'<a href="http://noticiasseguridad.com/"><img src="img/noticiasseguridad.png" width=70%></a><br/><br/>' +\
					'<a href="https://www.muyseguridad.net/"><img src="img/muyseguridad.png" width=85%></a><br/><br/>' +\
					'<a href="https://www.revistabyte.es/seguridad-informatica/"><img src="img/byte_ti.png" width=75%></a>' +\
				'</td>' +\
			'</tr>' +\
		'</table>' +\
	'</fieldset>'

	return Markup(info)
	

# Devuelve la cadena libre de caracteres especiales: sólo admite [a-z]. Además, la ñ se convierte a n:
def clean_username(name,surnames):

	new_user = str(name[0:3] + surnames[0][0:3] + surnames[1][0:3]).lower()	# Se convierte a mínusculas en primer lugar.

	remove = u'áéíóúñÁÉÍÓÚÑ'	# Se sustituyen los caracteres especiales.
	change = "aeiounaeioun"
	for i in range(len(remove)):
		new_user = new_user.replace(remove[i],change[i])
		
	return new_user		# Devuelve el nombre de usuario del nuevo personal de seguridad filtrado.

# Misma utilidad que la función anterior, pero se aplica cuando se tiene el nombre como una cadena completa:
def clean_username_joined(name):

	name = name.lower()			# Se convierte a mínusculas en primer lugar.

	remove = u'áéíóúñÁÉÍÓÚÑ'	# Se sustituyen los caracteres especiales.
	change = "aeiounaeioun"
	for i in range(len(remove)):
		name = name.replace(remove[i],change[i])
		
	return name		# Devuelve el nombre de usuario filtrado.


# Formatea los informes para la visualización legible HTML:
def extract_reports (reports):

	if reports.find('==') > -1:		# En el caso de que haya informes, se procesan para la visualización:
	
		# Formateo para la ventana de Informes (solo para visualización!):
		matches = re.split(r'==',str(reports[0:len(reports)-2]))
		
		reports_view = reports_t = ''
		
		for item in matches:
			report_name = ''
			# En primer lugar, se extrae el nombre del informe:
			i = len(item)-1
			while item[i] != '/' and i > -1:
				i -= 1
				
			if i > 0:
				report_name = item[i+1:len(item)]
			
			reports_t += str(report_name) + ':<br/>' + str(item) + '<br/><br/>'
		
		reports_t = reports_t.replace(" ","")	# Se eliminan los espacios en blanco.
		
		reports_view = Markup(reports_t)		# Se formatea la cadena para visualización en el interfaz web.
		
		return reports_t
	else:
		return ''

		
# Compone el campo pm_info maquetado para la visualización legible HTML:
def compound_pm_extended(pm_info):

	# Formateo para la ventana de Medidas de Protección:
	# Hay que extraer las medidas aplicables, si se han aplicado o no, y las observaciones para cada una de ellas:		
	matches = re.split(r'==',str(pm_info[0:len(pm_info)-2]))
	
	pm = ''
	set = ''
	notes = ''
	
	i = 0
	
	pm_extended = u'<table name="table_pm" id="table_pm" style="width: 100%;"><tr><th>Código</th><th>Aplicado</th><th>Observaciones</th></tr>'
	
	# Para cada entrada, se extrae el código de la medida de protección, el flag de aplicada o no, y las observaciones:
	for item in matches:
		
		# Se extrae el código de 3 dígitos:
		pattern = re.compile('\d{3}\$\$')
		temp = str(pattern.findall(item))
		remove = "[]$"
		for c in remove:
			temp = temp.replace(c,"")
		pm = temp

		# Se extrae el flag de aplicado/no aplicado:
		pattern = re.compile('\$\$[SN]')
		temp = str(pattern.findall(item))
		remove = "$[]"
		for c in remove:
			temp = temp.replace(c,"")
		if str(temp).find('S') > -1:
			set = 'S'
		else:
			set = 'N'
			
		notes = item[6:len(item)]
		
		if set == 'S':
			select_set = u'<select name="set[]" disabled><option name="set[]" value="Si" selected="selected">Sí</option><option name="set[]" value="No">No</option></select>'
		else:		
			select_set = u'<select name="set[]" disabled><option name="set[]" value="Si">Sí</option><option name="set[]" value="No" selected="selected">No</option></select>'
		
		pm_extended += '<tr style="border-bottom: 2px solid grey;"><td style="width: 9%;"><textarea readonly style="border: none; resize:none; width: 99%; font-size: 16px; margin-top: 20px;">' + pm.replace("'","") + '</textarea></td><td style="width: 11%;">' + select_set + '</td><td style="width: 80%;">' + '<textarea style="width: 99%; height: 80%; resize: none;" disabled>' + notes + '</textarea></td></tr>'
	
	pm_extended += '</table>'
	
	return pm_extended

	
# Función para extraer y formatear los datos completos de una incidencia:	
def	extract_incident_data(cursor,id_incid):

	cursor.execute("SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE id=%s", (str(id_incid),))		# Se realiza la consulta de la incidencia requerida.
	entry = str(cursor.fetchall()).decode('unicode_escape')										# Se extraen los datos de la incidencia requerida.

	fields = []			# Recogerá la composición de los campos a partir del resultado de la consulta.
	field = ''			# Recogerá temporalmente el contenido de cada campo.
	first_field = 's'	# Para ajustar la extracción correcta de los datos.
	
	# A continuación, se genera el listado con el contenido de los campos del registro seleccionado:
	
	for i in range(1,len(entry)):

		if entry[i] != ',' or (entry[i-1].isdigit() and entry[i+2].isdigit()) or (entry[i-1].isdigit() and entry[i+2] != 'u') or (entry[i-1] != "'" and entry[i+2] != 'u'):
				field = field + entry[i]
		else:
			field = field.replace("u'","")
			field = field.replace("'","")
							
			if first_field == 's':
				fields.append(str(field[1:len(field)]))
				first_field = 'n'
			else:
				fields.append(str(field))
			
			field = ''

	# Se añade el último campo:
	field = field.replace("u'","")
	field = field.replace("'","")
	fields.append(str(field[1:len(field)-2]))
	
	# Seguidamente se preparan algunos datos del registro para una mejor visualización y trabajo a través del interfaz web.

	# Hay que tener en cuenta que fields es una lista temporal en memoria, por lo que puede asignarse cualquier cadena a 
	# cualquiera de sus entradas. Sólo afecta para visualizar datos, no se refleja en la BBDD.
	
	# En primer lugar, se indica el nombre completo del usuario, tanto en el caso de que el originador sea una persona, como del responsable:
	
	if str(fields[1]).find('SIEM') == -1:
		fields[1] = str(re.findall("[a-z]{9}", fields[1]))
		fields[1] = fields[1][1:len(fields[1])-1]
		fields[1] = fields[1].replace("'","")
		
		cursor.execute("SELECT name,surname FROM STAFF WHERE user LIKE %s", (fields[1],))	# Se realiza la consulta.
		entry = str(cursor.fetchall()).decode('unicode_escape')								# Se extraen los datos.
		
		fields[1] = str(entry)
		fields[1] = fields[1].replace("[(u'","")
		fields[1] = fields[1].replace("', u'"," ")
		fields[1] = fields[1].replace("')]","")
		
		originator = fields[1]			
	else:
		originator = 'SIEM'
	
	type = fields[2]
	
	description = fields[3]
	
	area = fields[4]
	
	fields[5] = str(re.findall("[a-z]{9}", fields[5]))
	fields[5] = fields[5][1:len(fields[5])-1]
	fields[5] = fields[5].replace("'","")
	
	cursor.execute("SELECT name,surname FROM STAFF WHERE user LIKE %s", (fields[5],))		# Se realiza la consulta.
	entry = str(cursor.fetchall()).decode('unicode_escape')									# Se extraen los datos.
	# Se limpia la cadena de caracteres innecesarios:
	fields[5] = str(entry)
	fields[5] = fields[5].replace("[(u'","")
	fields[5] = fields[5].replace("', u'"," ")
	fields[5] = fields[5].replace("')]","")
	
	accountable = fields[5]					# Se extrae el responsable.
	
	if str(fields[6]).find('S') == -1:		# Se extrae el flag de CSIRT asignado o no.
		csirt = fields[6] = 'N'
	else:
		csirt = fields[6] = 'S'

	id_csirt = fields[7]
		
	# Se formatea la cadena con la fecha de detección:
	fields[8] = fields[8][7:9] + '/' + fields[8][5:7] + '/' + fields[8][1:5] + ' ' + fields[8][9:11] + ':' + fields[8][11:13]
	detect_date = fields[8]
	notify_date = fields[9]
	
	if str(fields[10]).find('C') > -1:		# Se extrae la severidad.
		severity = 'C'
		
	if str(fields[10]).find('A') > -1:
		severity = 'A'
		
	if str(fields[10]).find('M') > -1:
		severity = 'M'
		
	if str(fields[10]).find('B') > -1:
		severity = 'B'
	
	dimensions = fields[11]						# Se extrae la información relativa a las dimensiones de seguridad afectadas.
	dimensions = dimensions.replace(" ", "")	# Se eliminan los espacios en blanco.
		
	if str(fields[12]).find('A') > -1:			# Se extrae el estado de la incidencia.
		status = 'A'
		
	elif str(fields[12]).find('U') > -1:
		status = 'U'
		
	else:
		status = 'C'
	
	reports = fields[13]						# Se extraen la información relativa a los informes que pudiera contener.
	
	# Formateo para la ventana de Medidas de Protección:
	# Hay que extraer las medidas aplicables, si se han aplicado o no, y las observaciones para cada una de ellas:		
	matches = re.split(r'==',str(fields[15][0:len(fields[15])-2]))
	
	pm = ''
	set = ''
	notes = ''
	
	i = 0
	
	pm_extended = u'<table name="table_pm" id="table_pm" style="width: 100%;"><caption style="font-weight: bold; color: #222277">MEDIDAS DE PROTECCIÓN</caption><tr><th>Código</th><th>Aplicado</th><th>Observaciones</th></tr>'
	
	# Para cada entrada, se extrae el código de la medida de protección, el flag de aplicada o no, y las observaciones:
	for item in matches:
		
		# Se extrae el código de 3 dígitos:
		pattern = re.compile('\d{3}\$\$')
		temp = str(pattern.findall(item))
		remove = "[]$"
		for c in remove:
			temp = temp.replace(c,"")
		pm = temp

		# Se extrae el flag de aplicado/no aplicado:
		pattern = re.compile('\$\$[SN]')
		temp = str(pattern.findall(item))
		remove = "$[]"
		for c in remove:
			temp = temp.replace(c,"")
		if str(temp).find('S') > -1:
			set = 'S'
		else:
			set = 'N'
		
		# Se extraen las observaciones:
		if i == 0:
			notes = item[7:len(item)]
			i = 1
		else:
			notes = item[6:len(item)]
		
		if set == 'S':
			if status == 'C':	# En el caso de que la incidencia se encuentre cerrada, se asegura de dejar deshabilitada cualquier modificación de la información.
				select_set = u'<select name="set[]" disabled><option name="set[]" value="Si" selected="selected">Sí</option><option name="set[]" value="No">No</option></select>'
			else:
				select_set = u'<select name="set[]"><option name="set[]" value="Si" selected="selected">Sí</option><option name="set[]" value="No">No</option></select>'
		else:
			if status == 'C':				
				select_set = u'<select name="set[]" disabled><option name="set[]" value="Si">Sí</option><option name="set[]" value="No" selected="selected">No</option></select>'
			else:	
				select_set = u'<select name="set[]"><option name="set[]" value="Si">Sí</option><option name="set[]" value="No" selected="selected">No</option></select>'
		
		if status == 'C':
			pm_extended += '<tr style="border-bottom: 2px solid grey;"><td style="width: 9%;"><textarea readonly style="border: none; resize:none; width: 99%; font-size: 16px; margin-top: 20px;">' + pm.replace("'","") + '</textarea></td><td style="width: 11%;">' + select_set + '</td><td style="width: 80%;">' + '<textarea style="width: 99%; height: 80%; resize: none;" disabled>' + notes + '</textarea></td></tr>'
		else:
			pm_extended += '<tr style="border-bottom: 2px solid grey;"><td style="width: 9%;"><textarea readonly name="pm_codes[]" style="border: none; resize:none; width: 99%; font-size: 16px; margin-top: 20px;">' + pm.replace("'","") + '</textarea></td><td style="width: 11%;">' + select_set + '</td><td style="width: 80%;">' + '<textarea name="notes[]" style="width: 99%; height: 80%; resize: none;">' + notes + '</textarea></td></tr>'
	
	pm_extended += '</table>'
	
	pm_extended = Markup(pm_extended)	# Se formatea para la maquetación HTML.
			
	fields[14] = fields[14][1:len(fields[14])]
	
	details = fields[14]	# Se extrae el campo de detalles.
	
	pm_info = fields[15]	# Se extrae el campo de información relativo a las medidas de protección.

	# Se extraen los flag's de falso positivo/negativo:
	if fields[16].find('S') > -1:
		false_p = 'S'
	else:
		false_p = 'N'
		
	if fields[17].find('S') > -1:
		false_n = 'S'
	else:
		false_n = 'N'		
			
	return originator,type,description,area,accountable,csirt,id_csirt,detect_date,notify_date,severity,dimensions,status,reports,details,pm_info,pm_extended,false_p,false_n

	
# Función para extraer y formatear parte de los datos de una incidencia:	
def	extract_incident_partial_data(cursor,id_incid):

	cursor.execute("SELECT SQL_NO_CACHE accountable,status,csirt,severity,dimensions,details,reports,pm_info,false_p,false_n FROM INCIDENTS WHERE id=%s", (str(id_incid),))
	data_incid = cursor.fetchall()
	
	extract_data = data_incid[0]
	
	cursor.execute("SELECT name,surname FROM STAFF WHERE user LIKE %s", (extract_data[0],))
	entry = str(cursor.fetchall()).decode('unicode_escape')
	# Se limpia la cadena de caracteres innecesarios:
	entry = entry.replace("[(u'","")
	entry = entry.replace("', u'"," ")
	entry = entry.replace("')]","")	
	accountable = entry		# Se extrae el responsable.
	
	status = extract_data[1]
	csirt = extract_data[2]
	severity = extract_data[3]
	dimensions = extract_data[4]
	details = extract_data[5]
	reports = extract_data[6]
	pm_info = extract_data[7]
	false_p = extract_data[8]
	false_n = extract_data[9]
	
	return accountable,status,csirt,severity,dimensions,details,reports,pm_info,false_p,false_n
	
	
# Función para notificaciones puntuales al personal responsable de seguridad:
def email_notify(email,subject,text):

	# Se notifica el texto 'text' al personal afectado con dirección de correo electrónico 'email':
	accountable_email = "bchimar@outlook.es"	# Se prueba sobre una dirección de correo electrónico real sobre la que se tenga control.
	message = text
	mime_message = MIMEText(message)
	mime_message["Subject"] = subject
	mime_message["From"] = "bchimar@outlook.es"
	mime_message["To"] = accountable_email		# Se prueba solo con el responsable. En operación real, si se hubiera conformado un CSIRT, se enviaría a los 3 miembros.
	smtp = SMTP()
	smtp.connect('smtp-mail.outlook.com',587)	# El servidor de Outlook funciona OK (19/10/2018).
	smtp.ehlo()
	smtp.starttls()
	smtp.ehlo()
	smtp.login("bchimar@outlook.es", "YOUR_PASS")
	smtp.sendmail("bchimar@outlook.es", accountable_email, mime_message.as_string())
	smtp.close()

	return
	
	
#######################
# FIN Soteria_libs.py #
#######################
