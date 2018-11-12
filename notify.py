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


#####################################################################
#  			  notify.py: Servicio de Notificaciones					#
#	Comprueba si hay nuevas incidencias que precisen notificación.	#
#####################################################################


import sys								# Se importa y carga la información de sistema para control interno.
reload(sys)
sys.setdefaultencoding("utf-8")			# Se trabaja por defecto con codificación de caracteres UTF-8.

from smtplib import SMTP				# Librería con las funciones que permiten enviar correo electrónico.
from email.mime.text import MIMEText	# Librería para la generación de los correos a enviar.

import time								# Funciones de manejo de la fecha y hora del sistema.

# Inicialización del acceso a la BBDD:
import mysql.connector as mariadb		# Conector de acceso a la BBDD de MariaDB.
mariadb_connection = mariadb.connect(user='root', password='XXXXXXXXXX', database='soteria', use_unicode=True, charset='utf8')
cursor = mariadb_connection.cursor()
mariadb_connection.autocommit = True	# Permite que se refresquen los datos en cada consulta y evitar los problemas de la memoria caché.

# Casos de Notificación:
# a) Alta de incidencia de severidad Alta o Crítica: si se ha conformado un CSIRT, se avisa a los tres componentes.
# b) Alta de incidencia que genera una incidencia Crítica de tipo 571, con posible violación de la seguridad de los datos personales:
#    requiere avisar sobre ello al responsable de la incidencia para la gestión adecuada de la notificación a la AEPD (y a los afectados, si procede).
# La manera de proceder, por tanto, será:
# Si existe CSIRT, se comunica la nueva indencia y la severidad a los 3 componentes. En caso contrario, solo al responsable.
# Si la incidencia es de tipo 571 (DATOS DE CARÁCTER PERSONAL), hay que indicarlo claramente en el mensaje de notificación.

cursor.execute("select id,type,severity,description from INCIDENTS where (severity='C' or severity='A') and (status='A' or status='U')")
result = cursor.fetchall()	# Se buscan los nuevos incidentes de severidad Crítica o Alta.

for row in result:
	
	cursor.execute("select id from NOTIFIED where id=%s", (row[0],))	# Se busca si ya se encuentra la tabla.
	result_inner = cursor.fetchall()
	
	if not result_inner:	# Si no se encuentra, se añade a la tabla RGPD y se notifica por email.
	
		description = str(row[3])
		remove = u'áéíóúñÁÉÍÓÚÑ'	# Se sustituyen los caracteres especiales.
		change = "aeiounAEIOUN"
		for i in range(len(remove)):
			description = description.replace(remove[i],change[i])
				
		if str(row[1]).find('571') > -1:	# Si se trata de un posible caso de violación de la seguridad de los datos personales, hay que explicitarlo en la notificación.
			rgpd = 'S'		# Flag de posible caso de violación de la seguridad de los datos personales.
			message = "Se ha detectado una incidencia de severidad " + str(row[2]) + " en la que participa usted, que puede suponer una violacion de la seguridad de los datos personales. ID: " + str(row[0]) + ". Codigo ENS: 571." + " Descripcion: " + description + "."
			mime_message = MIMEText(message)
			mime_message["Subject"] = 'ATENCION: posible violacion de la seguridad de los datos personales!'
		else:
			rgpd = 'N'
			message = "Se ha detectado una incidencia de severidad " + str(row[2]) + ", en la que participa usted. ID: " + str(row[0]) + ". Codigo ENS: "  + str(row[1]) + ". Descripcion: " + description + "."
			mime_message = MIMEText(message)
			mime_message["Subject"] = 'ATENCION: detectada nueva incidencia!'
			
		# Se añade cada incidencia nueva que genere notificación para la AEPD a la tabla NOTIFIED, con el flag de RGPD, y se notifica al responsable:
		cursor.execute("INSERT INTO NOTIFIED (id,rgpd) VALUES (%s,%s)", (row[0],rgpd))			
		mariadb_connection.commit()		# Se hacen efectivos los cambios en la BBDD.
		
		cursor.execute("select csirt from INCIDENTS where id=%s", (row[0],))		# Se comprueba si tiene CSIRT asociado.
		csirt_check = cursor.fetchall()
		
		if str(csirt_check).find('S') > -1:
			cursor.execute("select team from CSIRT where id_incid=%s", (row[0],))
			csirt_team = cursor.fetchall()
			user_csirt_1_email = str(csirt_team[0][0])[0:9] + '@soteria.es'
			user_csirt_2_email = str(csirt_team[0][0])[9:18] + '@soteria.es'
			user_csirt_3_email = str(csirt_team[0][0])[18:27] + '@soteria.es'
			accountable_email = user_csirt_1_email	# El Responsable es el primero que aparece en el Equipo de Respuesta.
		else:		
			cursor.execute("select accountable from INCIDENTS where id=%s", (row[0],))
			user_name = cursor.fetchall()
			accountable_email = str(user_name[0][0]) + '@soteria.es'	# Se construye la dirección de correo electrónico.
			
		# Se añade la fecha de notificación al campo notify_date de la tabla INCIDENTS de la incidencia correspondiente:
		notify_date = str(time.strftime("%d/%m/%Y %H:%M"))
		cursor.execute("UPDATE INCIDENTS SET notify_date=%s where id=%s", (notify_date,row[0]))
		mariadb_connection.commit()

		# En este punto iría el bloque que aparece más abajo para enviar los correos respectivos de cada nueva incidencia con severidad Alta o Crítica.
	
# El siguiente bloque debería estar dentro del if anterior (if not result_inner:...), pero como solo se va
# a probar a enviar un correo sobre una cuenta real, se ejecuta en el cuerpo principal, evitando el bucle:
accountable_email = "bchimar@outlook.es"	# Se prueba sobre una dirección de correo electrónico real sobre la que se tenga control.
mime_message["From"] = "bchimar@outlook.es"
mime_message["To"] = accountable_email		# Se prueba solo con el responsable. En operación real, si se hubiera conformado un CSIRT, se enviaría a los 3 miembros.
smtp = SMTP()
smtp.connect('smtp-mail.outlook.com',587)	# El servidor de Outlook funciona OK (19/10/2018).
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login("bchimar@outlook.es", "MGSTICS2017TFM")
smtp.sendmail("bchimar@outlook.es", accountable_email, mime_message.as_string())
smtp.close()


#################
# FIN notify.py #
#################
