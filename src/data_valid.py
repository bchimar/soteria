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
# 				   data_valid.py:							#
#	 	funciones de validación de la entrada de datos		#
#############################################################


import re   # Libreria de funciones para manejo de Expresiones Regulares.

import time


# Mediante esta función se valida la entrada de datos relativos a los campos originator y accountable de la tabla INCIDENTS:
def user_valid(data):

	error = 0
	
	if len(data) > 9:
		error = 1
	
	pat = re.compile('\W')	# Caracteres no alfanuméricos.
	findbaddata = pat.findall(data)	
	if len(findbaddata) > 0:
		error = 1
	pat = re.compile('\d')	# Caracteres numéricos.
	findbaddata = pat.findall(data)	
	if len(findbaddata) > 0:
		error = 1
	
	return error


# Mediante esta función se valida la entrada de datos relativa al campo type de la tabla INCIDENTS:
def type_valid(data):

	error = 0
	
	if len(data) > 3:
		error = 1
	
	pat = re.compile('\D')	# Caracteres no numéricos.
	findbaddata = pat.findall(data)	
	if len(findbaddata) > 0:
		error = 1
	
	return error

	
# Mediante esta función se valida la entrada de datos relativa a campos de solo texto alfabético:
def only_alpha(data):

	error = 0
	
	data = str(data)			# Se pasa a cadena de texto, lo que facilita su procesado.
	
	remove = u'áéíóúñÁÉÍÓÚÑ'	# Se sustituyen los caracteres especiales.
	change = "aeiounaeioun"
	for i in range(len(remove)):
		data = data.replace(remove[i],change[i])
	
	data = data.replace(" ","")	# Se eliminan los espacios en blanco.
	
	pat = re.compile('\W')	# Caracteres no alfanuméricos.
	findbaddata = pat.findall(data)	
	if len(findbaddata) > 0:
		error = 1
	pat = re.compile('\d')	# Caracteres numéricos.
	findbaddata = pat.findall(data)	
	if len(findbaddata) > 0:
		error = 1

	return error
	

# Mediante esta función se valida la entrada de datos de números enteros:
def data_int_valid(data):

	error = 0
	
	pat = re.compile('\D')	# Cualquier carácter que no sea un dígito de 0 a 9.
	findbaddata = pat.findall(data)
	# Como se trabaja en modo String, se puede aplicar tanto a un dato aislado como a un vector de datos...
	if findbaddata:
		error = 1

	return error

	
# Mediante esta función se valida la entrada de datos de números enteros negativos:
def data_int_negative_valid(data):

	error = 0
	
	pat = re.compile('\d{1,2}')		# Se obtiene la presencia de número enteros.
	findbaddata = pat.findall(data)
	if len(findbaddata) < 1:		# Si no hay, no tiene sentido el dato introducido...
		error = 1
	else:	
		pat = re.compile('\D')	# Cualquier carácter que no sea un dígito de 0 a 9.
		findbaddata = pat.findall(data)
		# Solo se admite 1, y de obligada presencia, carácter distinto de número (el símbolo negativo '-'):
		if len(findbaddata) > 1 or len(findbaddata) < 1:
			error = 1
		else:	
			if findbaddata[0] != '-':	# Solo se admite el carácter '-' en la indicación de enteros negativos.
				error = 1

	return error
	

# Mediante esta función se valida la entrada de datos en coma flotante:
def data_float_valid(data):

	error = 0
	
	pat = re.compile('\D')	# Cualquier carácter que no sea un dígito de 0 a 9.
	findbaddata = pat.findall(data)
	
	# Solo se admite 1 carácter distinto de número: el punto o la coma decimal:
	if len(findbaddata) > 1:
		error = 1
	else:	
		if findbaddata:
			if findbaddata[0] != '.' and findbaddata[0] != ',':
				error = 1
	
	# Si el usuario ha utilizado la coma como separador decimal, se pasa a punto decimal:
	if error == 0:
		pat = re.compile(',')
		findbaddata = pat.findall(data)
		if findbaddata:
			data = float(re.sub(',','.',data))
		else:
			data = float(data)
		
	return error, data		# Se devuelve el resultado de la búsqueda.

	
# Mediante esta función se valida la entrada de datos de tipo horario en formato hh:mm:
def data_time_valid(data):

	error = 0
	
	pat = re.compile('\D')	# Cualquier carácter que no sea un dígito de 0 a 9.
	findbaddata = pat.findall(data)
	
	# Solo se admite 1, y de obligada presencia, carácter distinto de número (el separador ':'):
	if len(findbaddata) > 1 or len(findbaddata) < 1:
		error = 1
	else:	
		if findbaddata:
			if findbaddata[0] != ':':	# Solo se admite el carácter ':' en la indicación horaria.
				error = 1
			else:
				# Se comprueba que se escribe correctamente el formato horario: horas de 00 a 23 y minutos de 00 a 59:
				pat = re.compile('\d{1,2}:')
				findbaddata = pat.findall(data)
				if not findbaddata:	# No se ha escrito correctamente la parte relativa a la hora.
					error = 1
				else:
					findbaddata = re.sub(':','',findbaddata[0])	# Se elimina el carácter ':' para obtener el dato numérico entero.
					if int(findbaddata) > 23:
						error = 1
					else:
						pat = re.compile(':\d{1,2}')
						findbaddata = pat.findall(data)
						if not findbaddata:	# No se ha escrito correctamente la parte relativa a los minutos.
							error = 1
						else:
							findbaddata = re.sub(':','',findbaddata[0])	# Se elimina el carácter ':' para obtener el dato numérico entero.
							if int(findbaddata) > 59:
								error = 1
	
	return error
	

# Mediante esta función se extrae y devuelve las horas y minutos por separado de indicaciones horarias en formato hh:mm:
# (también válido para extraer los minutos y segundos en formato mm:ss)
def extract_time(data):

	# Se extrae la parte relativa a la hora:
	pat = re.compile('\d{1,2}:')
	findbaddata = pat.findall(data)
	findbaddata = re.sub(':','',findbaddata[0])	# Se elimina el carácter ':' para obtener el dato numérico entero.	
	hour = int(findbaddata)

	# Se extrae la parte relativa a los minutos:
	pat = re.compile(':\d{1,2}')
	findbaddata = pat.findall(data)
	findbaddata = re.sub(':','',findbaddata[0])	# Se elimina el carácter ':' para obtener el dato numérico entero.
	min = int(findbaddata)

	return hour, min
	
	
# Mediante esta función se valida la entrada de fechas que representen un periodo (desde A hasta B).
def dates_valid(day_A,mon_A,year_A,day_B,mon_B,year_B):

	error = 0
	BB_invalid = 100	# El valor #100 identifica fecha de caducidad no válida.

	# Se comprueba que solo contienen dígitos de 0 a 9:
	pat = re.compile('\D')
	findbaddate = pat.findall(day_A)
	if findbaddate:
		error = 1
	findbaddate = pat.findall(mon_A)
	if findbaddate:
		error = 1
	findbaddate = pat.findall(year_A)
	if findbaddate:
		error = 1
	findbaddate = pat.findall(day_B)
	if findbaddate:
		error = 1
	findbaddate = pat.findall(mon_B)
	if findbaddate:
		error = 1
	findbaddate = pat.findall(year_B)
	if findbaddate:
		error = 1
	# Esta parte anterior se implementar tal como se ha realizado, o bien utilizando la función data_int_valid().
	# En caso de utilizar dicha función, hay que declarar distintas variables de error para no sobrescribir el valor de "error",
	# y hacer la suma final: error = error_A + error_B + ...
		
	if error == 0:
	
		day_A = int(day_A)
		day_B = int(day_B)
		mon_A = int(mon_A)
		mon_B = int(mon_B)
		year_A = int(year_A)
		year_B = int(year_B)
		
		# Se comprueban posibles casos de error a la hora de indicar las fechas el usuario:
		if day_A < 1 or day_A > 31 or day_B < 1 or day_B > 31:
			error = 1
		elif mon_A < 1 or mon_A > 12 or mon_B < 1 or mon_B > 12:
			error = 1
		elif year_A < 2014 or year_B < 2014 or year_A > year_B:
			error = 1
			if year_A > year_B:
				error = BB_invalid		
		elif year_A == year_B:
			if mon_A > mon_B:
				error = BB_invalid
			if mon_A == mon_B:
				if day_A > day_B:
					error = BB_invalid

	return error


# Mediante esta función se valida la entrada de fechas que representen un periodo (desde A hasta B):
def dates_compact_valid(date_A,date_B):

	error = 0
	
	# El formato esperado es DD/MM/AAAA o D/M/AAAA, pero el objeto <input type="date"> lo devuelve en formato AAAA-MM-DD,
	# por lo que requiere adaptarse:
	date_A = date_A[8:10] + '/' + date_A[5:7] + '/' + date_A[0:4]
	date_B = date_B[8:10] + '/' + date_B[5:7] + '/' + date_B[0:4]
	# date_A = date_A.replace("-","/")	# En caso de que se indique con formato DD-MM-AAAA.
	# date_B = date_B.replace("-","/")
	
	
	pat = re.compile('\d{1,2}/\d{1,2}/\d{4}')
	findbaddata_A = pat.findall(date_A)
	findbaddata_B = pat.findall(date_B)
	
	if not findbaddata_A or not findbaddata_B:
		error = 1
		
	else:
		# Se extraen los campos para date_A:
		pat = re.compile('\d{1,2}/')
		findcamp = pat.findall(date_A)
		
		day_A = str(findcamp[0])
		mon_A = str(findcamp[1])
		day_A = re.sub('/','',day_A)
		mon_A = re.sub('/','',mon_A)

		pat = re.compile('\d{4}')
		findcamp=pat.findall(date_A)
		year_A = str(findcamp[0])
		
		# Se extraen los campos para date_B:
		pat = re.compile('\d{1,2}/')
		findcamp = pat.findall(date_B)
		
		day_B = str(findcamp[0])
		mon_B = str(findcamp[1])
		day_B = re.sub('/','',day_B)
		mon_B = re.sub('/','',mon_B)
		
		pat = re.compile('\d{4}')
		findcamp = pat.findall(date_B)
		year_B = str(findcamp[0])
		
		# Ya se puede emplear la función dates_valid():
		error = dates_valid(day_A,mon_A,year_A,day_B,mon_B,year_B)
		
	return error


# Mediante esta función se comprueba que ninguna fecha es posterior a la actual:
def dates_historic_valid(day_A,mon_A,year_A,day_B,mon_B,year_B):
	
	error = 0
	
	# En primer lugar se emplea la función dates_valid() para comprobar que son fechas válidas:
	error = dates_valid(day_A,mon_A,year_A,day_B,mon_B,year_B)
	
	# A continuación se comprueba que ninguna de las fechas indicadas es posterior a la actual:
	if not error:
		day_present = time.strftime("%d")
		mon_present = time.strftime("%m")
		year_present = time.strftime("%Y")
		
		error += dates_valid(day_A,mon_A,year_A,day_present,mon_present,year_present)
		error += dates_valid(day_B,mon_B,year_B,day_present,mon_present,year_present)
	
	# Por último se comprueba que sea un periodo válido: B posterior a A!
	if not error:
		error += dates_valid(day_A,mon_A,year_A,day_B,mon_B,year_B)
	
	return error
	
	
# Mediante esta función se valida la entrada de fechas en formato DD/MM/AAAA:
# (se admite también D/M/AAAA)
def date_valid(data):

	error = 0
	
	pat = re.compile('\d{1,2}/\d{1,2}/\d{4}')	# DD/MM/AAAA o D/M/AAAA.
	findbaddate = pat.findall(data)
	
	if not findbaddate:
		error = 1
	else:	# Se comprueba que los valores para el día, mes y año son correctos:
		pat = re.compile('\d{1,2}/')
		findbaddate = pat.findall(data)
		
		day = findbaddate[0]
		mon = findbaddate[1]
		day = re.sub('/','',day)
		mon = re.sub('/','',mon)

		pat = re.compile('\d{4}')
		year = pat.findall(data)
		
		day = int(day)
		mon = int(mon)
		year = int(year[0])
		
		if day < 1 or day > 31 or mon < 1 or mon > 12 or year < 2014:
			error = 1
	
	return error


#####################
# FIN data_valid.py #
#####################
