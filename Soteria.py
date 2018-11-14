# -*- coding: cp1252 -*-
# Permite que el archivo .py contenga caracteres especiales: tildes, �, etc.

#############################################################
#                     CUD - MAR�N                           # 
#                       MGSTICS                             # 
#                      2017/2018                            # 
#               TRABAJO DE FIN DE M�STER                    # 
#   DISE�O E IMPLEMENTACI�N DE UNA PLATAFORMA WEB PARA      # 
#  LA GESTI�N DE INCIDENTES DE SEGURIDAD DE LA INFORMACI�N  # 
#                ALUMNO: BLAS CHICA MARTOS.                 # 
#############################################################


#############################################################
# 					  	Soteria.py:							#
# m�dulo principal de la programaci�n activa del servidor	#
#############################################################


#---------#
# IMPORTS #
#---------#
# Selecci�n de los recursos de Flask, librer�as de python y funciones propias utilizados:

from Soteria_libs import *				# Librer�a de funciones de desarrollo propio para operaciones de apoyo.
from data_valid import *				# Librer�a de funciones de desarrollo propio para validaci�n de la entrada de datos desde el interfaz web.

import mysql.connector as mariadb		# Conector de acceso a la BBDD de MariaDB.

from markupsafe import Markup, escape	# Funciones para formatear y renderizar HTML.

from subprocess import call, Popen, check_call	# Funciones de sistema.

import re   							# Libreria de funciones para manejo de Expresiones Regulares.
import time								# Funciones de manejo de la fecha y hora del sistema.

# Funciones relacionadas con el middleware Flask:
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash
from flask_script import Manager
from flask_login import LoginManager, UserMixin, login_user, logout_user, \
    current_user

import random								# Para generaci�n de n�meros aleatorios.

from datetime import datetime, timedelta	# Funciones de fecha y hora.									

import os									# Funciones de SO.

import commands								# Funciones de sistema.

import sys									# Se importa y carga la informaci�n de sistema para control interno del middleware Flask.
reload(sys)
sys.setdefaultencoding("utf-8")				# Se trabaja por defecto con codificaci�n de caracteres UTF-8.


#---------------------------------------#
# CONFIGURACION DE LA APLICACION Flask: #
#---------------------------------------#
app = Flask(__name__)
app.config['SECRET_KEY'] = '>aJkFe340cFbApItW592.3fjGlDeY<'
app.config['SESSION_COOKIE_SECURE'] = True	# Configura el SECURE FLAG => se asegura que solo se env�an cookies mediante HTTPS!
app.config.from_object('config')

manager = Manager(app)
lm = LoginManager(app)
lm.login_view = '/'

#---------------------------------------------------------------#
# CONFIGURACION DE LA RUTA POR DEFECTO PARA LAS PLANTILLAS WEB:	#
#---------------------------------------------------------------#
from werkzeug import SharedDataMiddleware
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'templates',
        app.config['DEFAULT_TPL'])
})


#--------------------#
# VARIABLES GLOBALES #
#--------------------#

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))		# Necesario para poder localizar los archivos de datos.

# Inicializaci�n del acceso a la BBDD:
mariadb_connection = mariadb.connect(user='root', password='Junio333', database='soteria', use_unicode=True, charset='utf8')
cursor = mariadb_connection.cursor()
mariadb_connection.autocommit = True	# Permite que se refresquen los datos en cada consulta y evitar los problemas de la memoria cach�.

query_text = ''		# Recoger� la cadena compuesta con la consulta de b�squeda, seg�n los criterios seleccionados por el usuario.
result = ''			# Recoger� el resultado de la consulta a la BBDD.

# Recoge el contenido de la Gu�a CCN-STIC 804 de Implantaci�n del ENS, en su apartado 5: Medidas de protecci�n:
ens = u'<h1>CONSULTA GU�A CCN-STIC 804: IMPLANTACI�N DEL ENS. APARTADO 5: MEDIDAS DE PROTECCI�N</h1><h2>Versi�n Junio 2017</h2>	<h3>5.1.1 [MP.IF.1] �REAS SEPARADAS Y CON CONTROL DE ACCESO</h3>328. Se deben delimitar las �reas de trabajo y de equipos, disponiendo de un inventario actualizado que para cada �rea determine su funci�n y las personas responsables de su seguridad y de autorizar el acceso.<br/><br/>329. Cuando el acceso se controle por medio de llaves o dispositivos equivalentes, se dispondr� de un inventario de llaves junto con un registro de qui�n las toma, qui�n las devuelve y en manos de qui�n hay copias en cada momento. En caso de sustracci�n o p�rdida, se proceder� al cambio con diligencia para evitar el riesgo.<br/><br/>330. Se dispondr� de medios que eviten el acceso por puntos diferentes al que dispone del control de acceso. Se evitar�n ventanas accesibles y puertas desprotegidas. En particular hay que vigilar puertas de evacuaci�n de emergencia para que no permitan la entrada ni en condiciones normales ni cuando se utilizan como v�a de evacuaci�n (por ejemplo, c�maras de vigilancia, cerraduras electr�nicas que registran cada acceso, etc.).<br/><br/>331. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.1 - �reas seguras</li><li>11.2.1 - Emplazamiento y protecci�n de equipos</li></ul></ul>332. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[PE-18] Location of Information System Components</li><li>[PE-3] Physical Access Control</li><li>[PE-4] Access Control for Transmission Medium</li><li>[PE-5] Access Control for Output Devices</li></ul><h3>5.1.2 [MP.IF.2] IDENTIFICACI�N DE LAS PERSONAS</h3>333. Para las �reas de acceso restringido, se debe mantener una relaci�n de personas autorizadas y un sistema de control de acceso que verifique la identidad y la autorizaci�n y deje registro de todos los accesos de personas (por ejemplo, persona o identificador corporativo, fecha y hora de cada entrada y salida).<br/><br/>334. Se recomienda que exista segregaci�n de funciones en el proceso de gesti�n de acceso a los locales con equipamiento (solicitud y autorizaci�n). Dichas funciones deben recaer en al menos dos personas.<br/><br/>335. Debe realizarse peri�dicamente una revisi�n de las autorizaciones, identificando si contin�a existiendo la necesidad de acceso que motiv� la autorizaci�n.<br/><br/>336. ISO/IEC 27000 <ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>11.1.2 - Controles f�sicos de entrada</li></ul></ul>337. NIST SP 800-53 rev.4<ul style="list-style-type:square"><li>[PE-2] Physical Access Authorizations</li><li>[PE-6] Monitoring Physical Access</li><li>[PE-8] Visitor Access Records</li></ul><h3>5.1.3 [MP.IF.3] ACONDICIONAMIENTO DE LOS LOCALES</h3>338. Se debe disponer de unas instalaciones adecuadas para el eficaz desempe�o del equipamiento que se instala en ellas.<br/><br/>339. Sin perjuicio de lo dispuesto en otras medidas m�s espec�ficas, los locales deben:<ul style="list-style-type:square"><li> garantizar que la temperatura se encuentra en el margen especificado por los fabricantes de los equipos</li><li>garantizar que la humedad se encuentra dentro del margen especificado por los fabricantes de los equipos</li><li>se debe proteger el local frente a las amenazas identificadas en el an�lisis de riesgos, tanto de �ndole natural, como derivadas del entorno o con origen humano, accidental o deliberado (complementando [mp.if.1], [mp.if4], [mp.if.5], [mp.if.6] y [mp.if.7])</li><li>se debe evitar que el propio local sea una amenaza en s� mismo, o factor determinante de otras amenazas, como la existencia de material innecesario o inflamable en el local (papel, cajas, etc.) o que pueda ser causa de otros incidentes (elementos con agua, etc.)</li><li>el cableado debe estar:</li><ul style="list-style-type:circle"><li>etiquetado: se puede identificar cada cable f�sico y su correspondencia a los planos de la instalaci�n</li><li>controlado: para identificar el cableado fuera de uso</li><li>protegido frente a accidentes: por ejemplo, para evitar que las personas tropiecen con los cables</li><li>protegido frente a accesos no autorizados: protegiendo armarios de distribuci�n y canaletas</li></ul></ul>340. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.2.2 - Instalaciones de suministro</li><li>11.2.3 - Seguridad del cableado</li></ul></ul>341. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[PE-14] Temperature and Humidity Controls</li></ul><h3>5.1.4 [MP.IF.4] ENERG�A EL�CTRICA</h3>342. Se deben prever medidas para atajar un posible corte de suministro el�ctrico y un correcto funcionamiento de las luces de emergencia.<br/><br/>343. Prevenci�n de problemas de origen interno:<ul style="list-style-type:square"><li>dimensionado y protecci�n del cableado de potencia</li><li>dimensionado y protecci�n de los cuadros y armarios de potencia</li></ul>344. Reacci�n a problemas de origen externo:<ul style="list-style-type:square"><li>suministro alternativo: UPS, generadores, proveedor alternativo</li></ul>345. Se debe disponer de un plan de emergencia, de reacci�n y de recuperaci�n de desastres.<br/><br/>346. Hay que disponer de una alimentaci�n suficiente para apagar los equipos de forma ordenada. Normalmente, esto supone una alimentaci�n local (SAI, o UPS por sus siglas en ingl�s) que garantice el suministro el�ctrico durante los minutos necesarios para activar y concluir el procedimiento de apagado de emergencia, y grupos electr�genos en caso de ser necesario.<br/><br/>347. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.2.2 - Instalaciones de suministro</li></ul></ul>348. NIST SP 800-53 rev.4<ul style="list-style-type:square"><li>[PE-9] Power Equipment and Cabling</li><li>[PE-10] Emergency Shutoff</li><li>[PE-11] Emergency Power</li><li>[PE-12] Emergency Lighting</li></ul><h3>5.1.5 [MP.IF.5] PROTECCI�N FRENTE A INCENDIOS</h3>349. Se debe realizar un estudio del riesgo de incendios, tanto de origen natural como industrial:<ul style="list-style-type:square"><li>entorno natural proclive a incendios</li><li>entorno industrial que pudiera incendiarse</li><li>instalaciones propias con riesgo de incendio</li></ul>350. Si el fuego no se puede evitar, hay que desplegar medidas de prevenci�n, monitorizaci�n y limitaci�n del impacto<ul style="list-style-type:square"><li>disponer de carteles para evacuaci�n</li><li>evitar el uso de materiales inflamables</li><li>aislamiento (cortafuegos, puertas ign�fugas)</li><li>sistema de detecci�n conectado a central de alarmas 24x7</li><li>medios de reacci�n: medios de extinci�n</li><li>plan de emergencia, de reacci�n y de recuperaci�n de desastres</li></ul>351. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.1.4 - Protecci�n contra las amenazas externas y de origen ambiental</li></ul></ul>352. NIST SP 800-53 rev.4<ul style="list-style-type:square"><li>[PE-13] Fire Protection</li></ul>353. Otras referencias:<ul style="list-style-type:square"><li>Planes de emergencia y evacuaci�n contra incendios de locales y edificios. http://www.mtas.es/insht/FDN/FDN_011.htm</li></ul><h3>5.1.6 [MP.IF.6] PROTECCI�N FRENTE A INUNDACIONES</h3>354. Se debe realizar un estudio del riesgo de inundaciones, tanto de origen natural como industrial: <ul style="list-style-type:square"><li>cercan�a a r�os o corrientes de agua</li><li>canalizaciones de agua (tuber�as) especialmente encima de los equipos</li></ul>355. Si el riesgo no se puede evitar, hay que desplegar medidas de prevenci�n, monitorizaci�n y limitaci�n del impacto<ul style="list-style-type:square"><li>aislamiento de humedades</li><li>canalizaci�n de desag�e con procedimientos regulares de limpieza</li><li>sistema de detecci�n conectado a central de alarmas 24x7</li><li>plan de reacci�n y recuperaci�n de desastres; en el caso de canalizaciones industriales, el plan de reacci�n puede incluir el cierre de llaves o v�lvulas que atajen el vertido</li></ul>356. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.1.4 - Protecci�n contra las amenazas externas y de origen ambiental</li></ul></ul>357. NIST SP 800-53 rev.4<ul style="list-style-type:square"><li>[PE-15] Water Damage Protection</li></ul><h3>5.1.7 [MP.IF.7] REGISTRO DE ENTRADA Y SALIDA DE EQUIPAMIENTO</h3>358. Se debe llevar un registro pormenorizado de toda entrada y salida de equipamiento, haciendo constar en el mismo:<ul style="list-style-type:square"><li>fecha y hora</li><li>identificaci�n inequ�voca del equipamiento (servidores, port�tiles, equipos de comunicaciones, soportes de informaci�n, etc.)</li><li>persona que realiza la entrada o salida</li><li>persona que autoriza la entrada o salida</li><li>persona que realiza el registro</li></ul>359. Se recomienda que exista segregaci�n de funciones en el proceso de gesti�n de entrada y salida de equipamiento en los locales (solicitud y autorizaci�n). Dichas funciones deben recaer en al menos dos personas.<br/><br/>360. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.2.5 - Retirada de materiales propiedad de la empresa</li><li>11.2.6 - Seguridad de los equipos fuera de las instalaciones</li></ul></ul>361. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[PE-16] Delivery and Removal</li></ul><h3>5.1.8 [MP.IF.8] INSTALACIONES ALTERNATIVAS</h3>362. Se debe disponer de planes para poder prestar los servicios en un lugar alternativo en caso de indisponibilidad de las instalaciones actuales.<br/><br/>363. Las instalaciones alternativas deben garantizar las mismas medidas de protecci�n que las habituales. En particular, en lo que respecta a control de acceso de personas y entrada y salida de equipos.<br/><br/>364. Las instalaciones alternativas pueden estar dispuestas para entrar en servicio inmediatamente (hot site) o requerir un tiempo de personalizaci�n (cold site). En todo caso el tiempo de entrada en servicio debe estar respaldado por un an�lisis de impacto (ver [op.cont.1]), ser parte del plan de continuidad probado (ver [op.cont.2]) y ser objeto de pruebas regulares para validar la viabilidad del plan (ver [op.cont.3]).<br/><br/>365. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de los medios de procesamiento de informaci�n</li></ul></ul>366. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP-2] Contingency Plan</li><li>[CP-6] Alternate Storage Site</li><li>[CP-7] Alternate Processing Site</li><li>[PE-17] Alternate Work Site</li></ul><h3>5.2.1 [MP.PER.1] CARACTERIZACI�N DEL PUESTO DE TRABAJO</h3>368. Se deben definir las responsabilidades relacionadas con cada puesto de trabajo en materia de seguridad. La definici�n debe venir respaldada por el an�lisis de riesgos en la medida en que afecta a cada puesto de trabajo.<br/><br/>369. Se deben definir los requisitos que deben satisfacer las personas que vayan a ocupar el puesto de trabajo, en particular en t�rminos de confidencialidad.<br/><br/>370. Se deben tener en cuenta dichos requisitos en la selecci�n de la persona que va a ocuparlo, incluyendo la verificaci�n de sus antecedentes laborales, formaci�n y otras referencias: dentro del marco de la ley.<br/><br/>371. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>7.1.1 - Investigaci�n de antecedentes</li></ul></ul>372. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[PS-2] Position Risk Designation</li><li>[PS-3] Personnel Screening</li><li>[SA-21] Developer Screening</li></ul><h3>5.2.2 [MP.PER.2] DEBERES Y OBLIGACIONES</h3>373. Se debe informar a cada persona relacionada con el sistema de los deberes y responsabilidades de su puesto de trabajo en materia de seguridad, incluyendo las medidas disciplinarias a que haya lugar.<br/><br/>374. Se debe cubrir tanto el periodo durante el cual se desempe�a el puesto como las obligaciones en caso de terminaci�n de la asignaci�n, incluyendo el caso de traslado a otro puesto de trabajo.<br/><br/>375. Es de especial relevancia el deber de confidencialidad respecto de los datos a los que tengan acceso, tanto durante el periodo durante el que est�n adscritos al puesto de trabajo, como su prolongaci�n posterior a la terminaci�n de la funci�n para la que tuvo acceso a la informaci�n confidencial.<br/><br/>376. En el caso de personal contratado a trav�s de una tercera parte:<ul style="list-style-type:square"><li>se deben determinar deberes y obligaciones de la persona</li><li>se deben determinar deberes y obligaciones de la parte contratante</li><li>se debe determinar el procedimiento de resoluci�n de incidentes relacionados con el incumplimiento de las obligaciones, involucrando a la parte contratante</li></ul>377. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>7.1.2 - T�rminos y condiciones de contrataci�n</li><li>7.2.1 - Responsabilidades de la Direcci�n</li><li>7.2.3 - Proceso disciplinario</li><li>7.3.1 - Terminaci�n o cambio de responsabilidades laborales</li><li>8.1.4 - Devoluci�n de activos</li><li>13.2.4 - Acuerdos de confidencialidad o no divulgaci�n</li></ul></ul>378. NIST 800-53 rev. 4<ul style="list-style-type:square"><li>[PL-4] Rules of Behavior</li><li>[PS-6] Access Agreements</li><li>[PS-7] Third-Party Personnel Security</li><li>[PS-4] Personnel Termination</li><li>[PS-5] Personnel Transfer</li><li>[PS-8] Personnel Sanctions</li></ul><h3>5.2.3 [MP.PER.3] CONCIENCIACI�N</h3>379. Se debe concienciar regularmente al personal acerca de su papel y responsabilidad para que la seguridad del sistema alcance los niveles exigidos.<br/><br/>380. En particular hay que refrescar regularmente:<ul style="list-style-type:square"><li>la normativa de seguridad relativa al buen uso de los sistemas</li><li>la identificaci�n de incidentes, actividades o comportamientos sospechosos que deban ser reportados para su tratamiento por personal especializado</li><li>el procedimiento de reporte de incidentes de seguridad, seas reales o falsas alarmas</li></ul>381. Todo el personal debe recibir inicial y regularmente informaci�n acerca de los puntos arriba descritos.<br/><br/>382. ISO/IEC 27000<ul style="list-style-type:square"><li>27001:2013</li><ul style="list-style-type:circle"><li>7.3 - Concienciaci�n</li></ul><li>27002:2013</li><ul style="list-style-type:circle"><li>7.2.2 - Concienciaci�n, formaci�n y capacitaci�n en seguridad de la informaci�n</li></ul></ul>383. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AT-2] Security Awareness Training</li><li>[AT-3] Role-Based Security Training</li><li>[CP-3] Contingency Training</li><li>[IR-2] Incident Response Training<li>[PM-13] Information Security Resources</li></ul>384. Otras referencias:<ul style="list-style-type:square"><li>NIST SP 800-50 - Building an Information Technology Security Awareness and Training Program</li></ul><h3>5.2.4 [MP.PER.4] FORMACI�N</h3>385. Se debe formar regularmente a las personas en aquellas t�cnicas que requieran para el desempe�o de sus funciones.<br/><br/>386. Es de destacar, sin perjuicio de otros aspectos:<ul style="list-style-type:square"><li>configuraci�n de sistemas</li><li>gesti�n de incidentes (detecci�n y reacci�n)</li><li>procedimientos relativos a sus funciones sobre la gesti�n de la informaci�n (almacenamiento, transferencia, copias, distribuci�n y destrucci�n)</li></ul>387. La formaci�n debe actualizarse cada vez que cambian los componentes del sistema de informaci�n, introduci�ndose nuevos equipos, nuevo software, nuevas instalaciones, etc.<br/><br/>388. ISO/IEC 27000<ul style="list-style-type:square"><li>27001:2013</li><ul style="list-style-type:circle"><li>7.2 - Competencias</li></ul><li>27002:2013</li><ul style="list-style-type:circle"><li>7.2.2 - Concienciaci�n, formaci�n y capacitaci�n en seguridad de la informaci�n</li></ul></ul>389. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AT-2] Security Awareness Training</li><li>[AT-3] Role-Based Security Training</li><li>[AT-4] Security Training Records</li><li>[CP-3] Contingency Training</li><li>[IR-2] Incident Response Training</li><li>[PM-13] Information Security Resources</li></ul>390. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.17 - Security Skills Assessment and Appropriate Training to Fill Gaps</li></ul><li>NIST SP 800-16 - Information Technology Security Training Requirements: A Role- and Performance-Based Model</li><li>NIST SP 800-50 - Building an Information Technology Security Awareness and Training Program</li></ul><h3>5.2.5 [MP.PER.5] PERSONAL ALTERNATIVO</h3>391. Se debe prever la existencia de otras personas que se puedan hacer cargo de las funciones en caso de indisponibilidad del personal habitual. El personal alternativo deber� ofrecer las mismas garant�as de seguridad que el personal habitual.<br/><br/>392. Este personal alternativo puede ser, por ejemplo:<ul style="list-style-type:square"><li>Personal del mismo equipo sobredimensionado con capacidad de asumir el trabajo</li><li>Personal de otros turnos 24x7 que puedan cubrir bajas eventuales</li><li>Personal de otros departamentos con los conocimientos necesarios (respetando la segregaci�n)</li><li>Personal de un tercero contratado previsto en el Plan de Continuidad</li></ul>393. El plan de utilizaci�n de personal alternativo se vertebra dentro del plan de continuidad de la organizaci�n, incluy�ndose en las pruebas peri�dicas.<br/><br/>394. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de los recursos de tratamiento de la informaci�n</li></ul></ul>395. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP-2] Contingency Plan</li><li>[CP-6] Alternate Storage Site</li><li>[CP-7] Alternate Processing Site</li></ul><h3>5.3.1 [MP.EQ.1] PUESTO DE TRABAJO DESPEJADO</h3>396. Se debe exigir que los puestos de trabajo permanezcan despejados, sin m�s material encima de la mesa que el requerido para la actividad que se est� realizando en cada momento. Seg�n se termine una tarea, el material se retirar� a otra zona: cajones, estanter�as personales o comunes, cuarto de almacenamiento, etc.<br/><br/>397. El material de trabajo se guardar� en lugar cerrado. Pueden ser cajones o armarios con llave, o un cuarto separado cerrado con llave al menos fuera del horario de trabajo.<br/><br/>398. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>11.2.9 - Pol�tica de puesto de trabajo despejado y pantalla limpia</li></ul></ul>399. NIST SP 800-53 rev. 4<h3>5.3.2 [MP.EQ.2] BLOQUEO DE PUESTO DE TRABAJO</h3>400. Se debe bloquear autom�ticamente el puesto de trabajo desde el que se accede a servicios o datos de nivel medio o superior al cabo de un tiempo de inactividad, que se marcar� por parte de la entidad o compa��a.<br/><br/>401. Se debe requerir al usuario autenticarse de nuevo para reanudar la actividad en curso.<br/><br/>402. El tiempo mencionado ser� parte de la configuraci�n del equipo y no podr� ser alterado por el usuario.<br/><br/>403. Se cancelar�n las sesiones abiertas tanto desde dicho puesto de trabajo como las remotas al cabo de un tiempo de inactividad (superior al bloqueo del puesto de trabajo).<br/><br/>404. El tiempo mencionado ser� parte de la configuraci�n del equipo y no podr� ser alterado por el usuario.<br/><br/>405. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>11.2.8 - Equipo de usuario desatendido</li></ul></ul>406. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AC-11] Session Lock</li><li>[AC-12] Session Termination</li></ul><h3>5.3.3 [MP.EQ.3] PROTECCI�N DE EQUIPOS PORT�TILES</h3>407. Debe existir un inventario de los equipos port�tiles, que identifique el equipo port�til junto a la persona responsable del mismo. Se debe verificar regularmente en el inventario que el equipo permanece bajo control del usuario al que est� asignado.<br/><br/>408. Se recomienda que los equipos port�tiles tengan instalado y activado un sistema de protecci�n perimetral (cortafuegos personal) configurado para bloquear accesos salvo los autorizados. Los accesos autorizados seguir�n los procedimientos de autorizaci�n del organismo (ver [org.4]).<br/><br/>409. Los accesos realizados remotamente deber�n ser distinguidos por el servidor para que pueda limitar y autorizar la informaci�n y los servicios accesibles cuando se conecten remotamente a trav�s de redes que no pueda controlar la organizaci�n.<br/><br/>410. El mecanismo de control del equipo formar� parte de la configuraci�n del equipo y no podr� ser modificado por el usuario.<br/><br/>411. Los usuarios recibir�n instrucciones sobre el uso admisible del equipo, sobre los aspectos que debe contemplar en su manejo diario y del canal de comunicaci�n para informar al servicio de gesti�n de incidentes en caso de aver�a, p�rdida, robo o terminaci�n.<br/><br/>412. Se deber� comunicar al personal que los equipos port�tiles no deben contener claves de acceso remoto a la organizaci�n y se identificar� y aprobar� formalmente aquellos casos en los que no puede aplicarse.<br/><br/>413. Los equipos port�tiles deber�n disponer de detectores de violaci�n que permitan saber si el equipo ha sido manipulado y, en caso afirmativo, activar los procedimientos de gesti�n del incidente. Los detectores de violaci�n podr�n ser:<ul style="list-style-type:square"><li>F�sicos: por ejemplo, pegatinas que se alteran al manipularlas, bridas de protecci�n, etc.</li><li>L�gicos: por ejemplo, herramientas automatizadas que detecten si alg�n componente del port�til ha sido extra�do o sustituido</li></ul>414. Se recomienda proteger el acceso a la informaci�n que contienen los equipos port�tiles que sean susceptibles de salir de las instalaciones de la organizaci�n (por ejemplo, con candados, discos duros cifrados, etc.).<br/><br/>415. Se debe proteger la informaci�n contenida de nivel alto por medios criptogr�ficos: [mp.si.2].<br/><br/>416. Las claves criptogr�ficas deben protegerse seg�n [op.exp.11].<br/><br/>417. Cuando el equipo es desmantelado, se debe aplicar lo previsto en [mp.si.5].<br/><br/>418. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-827 - Gesti�n y uso de dispositivos m�viles</li></ul>419. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>6.2.1 - Pol�tica de dispositivos m�viles</li><li>11.2.6 - Seguridad de los equipos fuera de las instalaciones</li></ul></ul>420. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[AC-19] Access Control for Mobile Devices</li></ul><h3>5.3.4 [MP.EQ.4] MEDIOS ALTERNATIVOS</h3>421. Se debe prever medios alternativos de tratamiento de la informaci�n para el caso de que fallen los equipos de personal habituales. Estos medios alternativos estar�n sujetos a las mismas garant�as de protecci�n.<br/><br/>422. Se debe establecer un tiempo m�ximo para que los equipos alternativos entren en funcionamiento.<br/><br/>423. Los equipos alternativos pueden estar dispuestos para entrar en servicio inmediatamente (es decir, configurados) o requerir un tiempo de personalizaci�n (se puede disponer de ellos en el tiempo prestablecido; pero hay que configurarlos y cargar los datos). En todo caso el tiempo de entrada en servicio debe estar respaldado por un an�lisis de impacto (ver [op.cont.1]).<br/><br/>424. ISP/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de instalaciones de tratamiento de la informaci�n</li></ul></ul>425. NIST SP 800-53 rev. 4<h3>5.4.1 [MP.COM.1] PER�METRO SEGURO</h3>426. Se debe delimitar el per�metro l�gico del sistema; es decir, los puntos de interconexi�n con el exterior. Este per�metro deber� estar reflejado en la documentaci�n de la arquitectura del sistema (por ejemplo, el esquema de red).<br/><br/>427. Se debe disponer de cortafuegos que separen la red interna del exterior. Todo el tr�fico deber� atravesar dichos cortafuegos que s�lo dejaran transitar los flujos previamente autorizados.<br/><br/>428. Cuando se requiera niveles de seguridad ALTA, el sistema de cortafuegos constar� de dos o m�s equipos de diferente fabricante dispuestos en cascada. Estos cortafuegos podr�n ser equipos f�sicos o instalaciones o aplicaciones cortafuegos virtuales.<br/><br/>429. Cuando la disponibilidad de las transmisiones a trav�s del cortafuegos sea de nivel ALTO, se dispondr�n sistemas redundantes.<br/><br/>430. Los ataques de denegaci�n de servicio pueden ser afrontados en el per�metro, aunque pueden requerir la intervenci�n de otros elementos. En el per�metro se pueden detectar patrones sospechosos de comportamiento: avalanchas de peticiones, peticiones trucadas y, en general, un uso malicioso de los protocolos de comunicaciones. Algunas de estas peticiones pueden ser denegadas directamente por el equipo perimetral, en otras ocasiones hay que levantar una alarma para actuar en donde corresponda (servidores web, servidores de bases de datos... o contactando con los centros de respuesta a incidentes).<br/><br/>431. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-408 - Seguridad Perimetral - Cortafuegos</li><li>Gu�a CCN-STIC-419 - Configuraci�n segura con IPtables</li><li>Serie CCN-STIC-500 - Gu�as para Entornos Windows</li><li>Serie CCN-STIC-600 - Gu�as para otros Entornos</li><li>Gu�a CCN-STIC-811 - Interconexi�n</li></ul>432. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>13.1.2 - Seguridad de los servicios de red</li></ul></ul>433. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AC-4] Information Flow Enforcement</li><li>[CA-3] System Interconnections</li><li>[SC-7] Boundary Protection</li></ul>434. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.8 - Malware Defenses</li><li>CSC.9 � Limitation and Control of Network Ports</li><li>CSC.11 � Secure Configurations for Network Devices</li><li>CSC.12 � Boundary Defense</li><li>CSC.13 � Data Protection</li><li>CSC.15 - Wireless Access Control</li></ul><br/><li>NIST SP 800-41 - Guidelines on Firewalls and Firewall Policy</li></ul><h3>5.4.2 [MP.COM.2] PROTECCI�N DE LA CONFIDENCIALIDAD</h3>435. Es frecuente que autenticidad, integridad y confidencialidad se traten de forma conjunta negociando los protocolos, los par�metros y las claves en la fase de establecimiento. Es por ello que esta medida suele implementarse a la par que [mp.com.3].<br/><br/>436. Se deben emplear algoritmos acreditados por el Centro Criptol�gico Nacional que garanticen el secreto de los datos transmitidos.<br/><br/>437. En conexiones establecidas fuera del dominio de seguridad de la organizaci�n, se recurrir� a redes privadas virtuales que, con m�todos criptogr�ficos y tras una autenticaci�n fiable (ver [mp.com.3]), establecen una clave de cifrado para la sesi�n.<br/><br/>438. El cifrado de las comunicaciones es especialmente adecuado en redes inal�mbricas (WiFi)20. Los equipos inal�mbricos llevan incorporados mecanismos de cifrado de las comunicaciones, que deber�n ser configurados de forma segura (ver [op.exp.2] y [op.exp.3]) empleando mecanismos actualizados.<br/><br/>439. Hay que atender al secreto de las claves de cifrado seg�n lo indicado en [op.exp.11]. En el caso de redes privadas virtuales, el secreto debe ser impredecible, mantenerse bajo custodia mientras dure la sesi�n, y ser destruido al terminar. En el caso de otros procedimientos de cifrado, hay que cuidar de las claves de cifrado durante su ciclo de vida: generaci�n, distribuci�n, empleo, retirada del servicio y retenci�n si la hubiera.<br/><br/>440. Hay que seleccionar algoritmos evaluados o acreditados. A menudo basta con seleccionar los algoritmos y los par�metros adecuados dentro de las opciones posibles.<br/><br/>441. Hay que procurar que las tareas de cifrado en los extremos se realicen en equipos hardware especializados y certificados, conforme a [op.pl.5], evitando el cifrado por software.<br/><br/>442. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-807 Criptograf�a de empleo en el ENS</li><li>Gu�a CCN-STIC-827 - Gesti�n y uso de dispositivos m�viles</li><li>Gu�a CCN-STIC-406 - Seguridad en Redes Inal�mbricas</li><li>Gu�a CCN-STIC-416 - Seguridad en redes privadas virtuales</li></ul>443. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>10.1.1 - Pol�tica de uso de los controles criptogr�ficos</li><li>13.1.1 - Controles de red</li><li>13.1.2 - Seguridad de los servicios de red</li><li>14.1.2 - Asegurar los servicios de aplicaciones en redes p�blicas</li><li>18.1.5 - Regulaci�n de los controles criptogr�ficos</li></ul></ul>444. NIST 800-53 rev. 4<ul style="list-style-type:square"><li>[AC-4] Information Flow Enforcement</li><li>[AC-18] Wireless Access</li><li>[SC-8] Transmission Confidentiality and Integrity</li><li>[SC-12] Cryptographic Key Establishment and Management</li><li>[SC-13] Cryptographic Protection</li><li>[SC-40] Wireless Link Protection</li></ul>445. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.15 - Wireless Access Control</li></ul></ul><ul style="list-style-type:square"><li>NIST SP 800-48 - Wireless Network Security for IEEE 802.11a/b/g and Bluetooth</li><li>NIST SP 800-52 - Guidelines for the Selection and Use of Transport Layer Security (TLS) Implementations</li><li>NIST SP 800-77 - Guide to IPsec VPNs</li><li>NIST SP 800-113 - Guide to SSL VPNs</li><li>NIST SP 800-121 - Guide to Bluetooth Security</li><li>NIST SP 800-127 - Guide to Securing WiMAX Wireless Communications</li><li>NIST SP 800-153 - Guidelines for Securing Wireless Local Area Networks (WLANs)</li><li>SSL � Secure Sockets Layer</li><ul style="list-style-type:circle"><li>[RFC 6101] The Secure Sockets Layer (SSL) Protocol Version 3.0</li><li>Gu�a CCN-STIC-826 Configuraci�n de SSL/TLS</li></ul><li>TLS � Transport Layer Security</li><ul style="list-style-type:circle"><li>[RFC 5246] The Transport Layer Security (TLS) Protocol � Version 1.2</li><li>[RFC 6176] Prohibiting Secure Sockets Layer (SSL) Version 2.0</li><li>Gu�a CCN-STIC-826 Configuraci�n de SSL/TLS</li></ul><li>SSH � Secure Shell</li><li>SCP � Secure copy</li><li>SFTP � SSH File Transfer Protocol</li></ul><h3>5.4.3 [MP.COM.3] PROTECCI�N DE LA AUTENTICIDAD Y DE LA INTEGRIDAD</h3>446. Es frecuente que autenticidad, integridad y confidencialidad se traten de forma conjunta negociando los protocolos, los par�metros y las claves en la fase de establecimiento. Es por ello que esta medida suele implementarse a la par que [mp.com.2].<br/><br/>447. Se debe establecer de forma fehaciente la autenticidad del otro extremo de un canal de comunicaci�n antes de intercambiar informaci�n alguna.<br/><br/>448. Se debe evitar la utilizaci�n de mecanismos de autenticaci�n y protocolos no contemplados en la normativa de la organizaci�n.<br/><br/>449. Se deben usar protocolos que garanticen o al menos comprueben y detecten violaciones en la integridad de los datos intercambiados y en la secuencia de los paquetes.<br/><br/>450. La forma m�s habitual de establecer esta medida es establecer una red privada virtual que:<ul style="list-style-type:square"><li>garantice la autenticaci�n de las partes al inicio de sesi�n, cuando la red se establece</li><li>controle que la sesi�n no puede ser secuestrada por una tercera parte</li><li>que no permita realizar ataques activos (alteraci�n de la informaci�n en tr�nsito o inyecci�n de informaci�n espuria) sin que sea, al menos, detectada</li></ul>451. Hay que seleccionar algoritmos evaluados o acreditados por el Centro Criptol�gico Nacional que garanticen el secreto de los datos transmitidos. A menudo basta con seleccionar los algoritmos y los par�metros adecuados dentro de las opciones posibles.<br/><br/>452. Se debe evitar la utilizaci�n de mecanismos de autenticaci�n y protocolos no contemplados en la normativa de aplicaci�n. Adem�s, en caso de utilizar claves concertadas, deber�n utilizarse con cautela aplicando exigencias medias de calidad.<br/><br/>453. En conexiones establecidas fuera del dominio de seguridad de la organizaci�n, se puede recurrir a redes privadas virtuales que, con m�todos criptogr�ficos y tras una autenticaci�n fiable, establecen una clave de cifrado para la sesi�n.<br/><br/>454. El cifrado de las comunicaciones es especialmente adecuado en redes inal�mbricas (WiFi). Los equipos inal�mbricos llevan incorporados mecanismos de cifrado de las comunicaciones, que deber�n ser configurados de forma segura (ver [op.exp.2] y [op.exp.3]) empleando mecanismos actualizados.<br/><br/>455. Hay que atender al secreto de las claves de cifrado seg�n lo indicado en [op.exp.11]. En el caso de redes privadas virtuales, el secreto debe ser impredecible, mantenerse bajo custodia mientras dure la sesi�n, y ser destruido al terminar. En el caso de otros procedimientos de cifrado, hay que cuidar de las claves de cifrado durante su ciclo de vida: generaci�n, distribuci�n, empleo, retirada del servicio y retenci�n si la hubiera.<br/><br/>456. Hay que procurar que las tareas de cifrado en los extremos se realicen en equipos hardware especializados y certificados, conforme a [op.pl.5], evitando el cifrado por software.<br/><br/>457. Se debe evitar la utilizaci�n de mecanismos de autenticaci�n y protocolos no contemplados en la normativa de aplicaci�n. Adem�s, en caso de utilizar claves concertadas, deber�n utilizarse con cautela aplicando exigencias altas de calidad.<br/><br/>458. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-416 - Seguridad en redes privadas virtuales</li><li>Gu�a CCN-STIC-807 � Criptograf�a de empleo en el ENS</li></ul>459. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>10.1.1 - Pol�tica de uso de los controles criptogr�ficos</li><li>13.1.1 - Controles de red</li><li>13.1.2 - Seguridad de los servicios de red</li><li>14.1.2 - Asegurar los servicios de aplicaciones en redes p�blicas</li></ul></ul>460. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AC-18] Wireless Access</li><li>[SC-8] Transmission Confidentiality and Integrity</li><li>[SC-13] Cryptographic Protection</li><li>[SC-23] Session Authenticity</li><li> [SC-40] Wireless Link Protection</li></ul>461. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.15 - Wireless Access Control</li></ul></ul><h3>5.4.4 [MP.COM.4] SEGREGACI�N DE REDES</h3>462. La segregaci�n de redes acota el acceso a la informaci�n y acota la propagaci�n de los incidentes de seguridad que quedan restringidos al entorno donde ocurren. Esta deber� quedar reflejada en documentaci�n de la arquitectura del sistema (por ejemplo, el esquema de red) [op.pl.2].<br/><br/>463. Se debe segmentar la red de forma que haya:<ul style="list-style-type:square"><li>control (de entrada) de los usuarios que pueden trabajar en cada segmento, en particular si el acceso se realiza desde el exterior del segmento, tanto si es desde otro segmento de la red corporativa como si el acceso procede del exterior de la red, extremando las precauciones en este �ltimo escenario</li><li>control (de salida) de la informaci�n disponible en cada segmento</li><li>control (de entrada) de las aplicaciones utilizables en cada segmento</li></ul>464. El punto de interconexi�n debe estar particularmente asegurado, mantenido y monitorizado (ver [mp.com.1]). Estos puntos de interconexi�n interna son una defensa cr�tica frente a intrusos que han logrado superar las barreas exteriores y se alojan en el interior. N�tese que a menudo el objetivo de estas intrusiones es extraer informaci�n y enviarla al exterior, lo que se traduce en que hay que vigilar los protocolos de comunicaciones que se establecen y los datos que se transmiten.<br/><br/>465. No deber�a permitirse ning�n protocolo directo entre los segmentos internos y el exterior, intermediando todos los intercambios de informaci�n.<br/><br/>466. Las redes se pueden segmentar por dispositivos f�sicos o l�gicos.<br/><br/>467. Esta medida puede establecerse din�micamente como reacci�n frente a intrusiones (supuestas o detectadas) y que van a requerir un cierto periodo de tiempo (d�as) en poder ser erradicadas. Los primeros servicios a aislar ser�an los servidores de datos y los servidores de autenticaci�n para monitorizar y controlar su uso. Otros candidatos a ser aislados son los servicios de administraci�n del propio sistema para evitar que se capturen credenciales con privilegios de administraci�n o se pueda suplantar la identidad de los administradores.<br/><br/>468. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-408 - Seguridad perimetral (cortafuegos)</li><li>Gu�a CCN-STIC-419 - Configuraci�n segura con IPtables</li><li>Serie CCN-STIC-600 Gu�as para otros Entornos</li><li>Gu�a CCN-STIC-641 - Seguridad en routers Cisco</li></ul>469. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>13.1.3 - Segregaci�n en redes</li></ul></ul>470. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[SC-32] Information System Partitioning</li></ul>	<h3>5.4.5 [MP.COM.5] MEDIOS ALTERNATIVOS</h3>471. Se debe prever medios alternativos de comunicaci�n para el caso de que fallen los medios habituales. Estos medios alternativos deben proporcionar las mismas garant�as de seguridad que los medios habituales y deber� establecerse un tiempo m�ximo de entrada en funcionamiento que est� aprobado por su responsable.<br/><br/>472. En todo caso, el tiempo de entrada en servicio debe estar respaldado por un an�lisis de impacto (ver [op.cont.1]), ser parte del plan de continuidad probado (ver [op.cont.2]) y ser objeto de pruebas regulares para validar la viabilidad del plan (ver [op.cont.3]).<br/><br/>473. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de los recursos de tratamiento de la informaci�n</li></ul></ul>474. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP-8] Telecommunications Services</li><li>[CP-11] Alternate Communications Protocol</li></ul><h3>5.5.1 [MP.SI.1] ETIQUETADO</h3>477. Se debe etiquetar de forma que, sin revelar su contenido, se indique el nivel de calificaci�n m�s alto de la informaci�n contenida.<br/><br/>478. Una opci�n es que el propio soporte, en su exterior, lleve escrito el nivel de informaci�n que contiene o puede contener.<br/><br/>479. Una alternativa es que el soporte sea identificable por medio de alg�n c�digo o referencia y que el usuario pueda acceder a un repositorio de informaci�n donde se indica el nivel de informaci�n que el soporte contiene o puede contener.<br/><br/>480. La etiqueta del soporte determina las normativas y los procedimientos que deben aplicarse al mismo, concretamente en lo referente a:<ul style="list-style-type:square"><li>control de acceso</li><li>cifrado del contenido</li><li>entrada y salida de las instalaciones</li><li>medios de transporte</li></ul>481. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>8.2.2 - Etiquetado de la informaci�n</li><li>8.3.1 - Gesti�n de soportes extra�bles</li></ul></ul>482. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[MP-3] Media Marking</li></ul><h3>5.5.2 [MP.SI.2] CRIPTOGRAF�A</h3>483. Este requisito se aplica, en particular, a todos los dispositivos removibles (como CD, DVD, discos USB, etc.).<br/><br/>484. En lo referente a claves criptogr�ficas, se debe aplicar [op.exp.11].<br/><br/>485. Una opci�n es asegurarse que los datos se protegen antes de copiarse al soporte; es decir, se cifran o se firman exteriormente.<br/><br/>486. Otra opci�n es proteger todo el soporte instalando en el mismo un disco virtual que se encarga de acoger todo lo que se copie en el mismo, as� como controlar el acceso al mismo.<br/><br/>487. Otra opci�n es emplear soportes con cifrado incorporado por hardware que se encarga de acoger todo lo que se copie en el soporte, as� como controlar el acceso al mismo.<br/><br/>488. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-807 - Criptograf�a</li><li>Gu�a CCN-STIC-437 - Herramientas de Cifrado Software</li><li>Gu�a CCN-STIC-955 - Recomendaciones empleo GnuPG</li></ul>489. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>8.3.1 - Gesti�n de soportes extra�bles</li><li>10.1.1 - Pol�tica de uso de los controles criptogr�ficos</li></ul></ul>490. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[SC-28] Protection of Information at Rest</li></ul>491. Otras referencias:<ul style="list-style-type:square"><li>NIST SP 800-111 - Guide to Storage Encryption Technologies for End User Devices</li></ul>492. Productos. Hay muchos donde elegir; s�lo se citan algunos de uso frecuente:<ul style="list-style-type:square"><li>BitLocker � Microsoft</li><li>Crypt2000 � Secuware</li><li>GPG � http://www.gnupg.org/</li><li>PGP � Symantec</li><li>Veracrypt</li></ul><h3>5.5.3 [MP.SI.3] CUSTODIA</h3>493. Se debe aplicar la debida diligencia y control a los soportes de informaci�n (tanto en soporte electr�nico como no electr�nico) que permanecen bajo la responsabilidad de la organizaci�n:<ul style="list-style-type:square"><li>garantizando el control de acceso con medidas f�sicas ([mp.if.1] y [mp.if.7) o l�gicas ([mp.si.2]) o ambas</li><li>garantizando que se respetan las exigencias de mantenimiento del fabricante, en especial en lo referente a temperatura, humedad y otros agresores medioambientales</li></ul>494. Se recomienda conservar la historia de cada dispositivo, desde su primer uso hasta la terminaci�n de su vida �til y verificar regularmente que los soportes cumplen las reglas acordes a su etiquetado.<br/><br/>495. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>8.3.1 - Gesti�n de soportes extra�bles</li></ul></ul>496. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[MP-4] Media Storage</li></ul>497. Otras referencias:<ul style="list-style-type:square"><li>NIST SP 800-111 � Guide to Storage Encryption Technologies for End User Devices</li></ul><h3>5.5.4 [MP.SI.4] TRANSPORTE</h3>498. Se debe garantizar que los dispositivos permanecen bajo control y se satisfacen sus requisitos de seguridad mientras est�n siendo desplazados de un lugar a otro.<br/><br/>499. Se debe:<ul style="list-style-type:square"><li>disponer de un registro de salida que identifica al menos la etiqueta y al transportista que recibe el soporte para su traslado (tanto electr�nico como no electr�nico)</li><li>disponer de un registro de entrada que identifica al menos la etiqueta y al transportista que lo entrega</li><li>disponer de un procedimiento rutinario que coteja las salidas con las llegadas y levanta las alarmas pertinentes cuando se detecta alg�n incidente</li><li>utilizar los medios de protecci�n criptogr�fica ([mp.si.2]) correspondientes al nivel de clasificaci�n de la informaci�n contenida de mayor nivel</li><li>gestionar las claves seg�n [op.exp.11]</li></ul>500. Se recomienda disponer de un procedimiento al respecto y se verifica regularmente que los procedimientos establecidos se siguen, aplicando medidas correctivas en su defecto.<br/><br/>501. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-typecircle"><li>8.3.3 - Soportes f�sicos en tr�nsito</li><li>11.2.5 - Retirada de materiales propiedad de la empresa</li></ul></ul>502. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[MP-5] Media Transport</li></ul><h3>5.5.5 [MP.SI.5] BORRADO Y DESTRUCCI�N</h3>503. Se debe aplicar un mecanismo de borrado seguro a los soportes extra�bles (electr�nicos y no electr�nicos) que vayan a ser reutilizados para otra informaci�n o liberados a otra organizaci�n. El mecanismo de borrado ser� proporcionado a la clasificaci�n de la informaci�n que ha estado presente en el soporte.<br/><br/>504. Se deben destruir los soportes, de forma segura:<ul style="list-style-type:square"><li>cuando la naturaleza del soporte no permita un borrado seguro</li><li>cuando el procedimiento asociado al nivel de clasificaci�n de la informaci�n contenida as� lo requiera</li></ul>505. El mecanismo de destrucci�n ser� proporcionado a la clasificaci�n de la informaci�n contenida.<br/><br/>506. Los mecanismos de borrado y destrucci�n deben tener en la normativa de protecci�n medioambiental y los certificados de calidad medioambiental de la organizaci�n.<br/><br/>507. Se deben elegir productos certificados conforme a lo establecido en [op.pl.5]<br/><br/>508. Recomendaciones (tomadas de NIST SP 800-88):<br/><br/><table style="width:100%" border="1"><tr><th>Medio</th><th>Procedimiento</th><th>Acciones</th></tr><tr><td>papel<br/>microfilm</td><td>destruir</td>    <td><ul><li>trituradora en tiras o cuadraditos: 2mm</li></ul></td></tr><tr><td>m�viles<br/>PDAs</td><td>borrar manualmente</td><td><ul><li>agenda</li><li>mensajes</li><li>llamadas</li><li>resetear a la configuraci�n de f�brica</li></ul></td></tr><tr><td>routers</td><td>borrar manualmente</td><td><ul><li>tablas de encaminamiento</li><li>registros de actividad</li><li>cuentas de administraci�n</li><li>resetear a la configuraci�n de f�brica</li></ul></td></tr><tr><td>impresoras<br/>fax</td><td>borrar manualmente</td><td><ul><li>resetear a la configuraci�n de f�brica</li></ul></td></tr><tr><td>discos reescribibles</td><td>reescribir</td><td><ul><li>reescribir 3 veces: con ceros, con unos, con datos aleatorios</li></ul></td></tr><tr><td>discos de solo lectura</td><td>destruir</td><td><ul><li>trituradora: 5mm</li></ul></td></tr><tr><td>discos virtuales cifrados</td><td>adem�s de lo anterior</td><td><ul><li>destruir las claves</li></ul></td></tr></table>Tabla 4: Recomendaciones NIST SP 800-88 para borrado y destrucci�n<br/><br/>509. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-305 � Destrucci�n y sanitizaci�n de soportes inform�ticos (uso oficial)</li><li>Gu�a CCN-STIC-400 - Manual de seguridad de las TIC</li><li>Gu�a CCN-STIC-403 - Herramientas de seguridad</li><li>Gu�a CCN-STIC-404 - Control de soportes inform�ticos</li><li>Gu�a CCN-STIC-818 - Herramientas de seguridad</li></ul>510. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>8.3.2 - Eliminaci�n de soportes</li><li>11.2.7 - Reutilizaci�n o eliminaci�n segura de equipos</li></ul></ul>511. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[MP-6] Media Sanitization</li><li>[MP-8] Media Downgrading</li></ul>512. Otras referencias:<ul style="list-style-type:square"><li>NIST SP 800-88 - Guidelines for Media Sanitization</li><li>DoD 5220 Block Erase</li></ul><h3>5.6.1 [MP.SW.1] DESARROLLO</h3>513. El desarrollo de aplicaciones se realizar� sobre un sistema diferente y separado del de producci�n, no debiendo existir herramientas o datos de desarrollo en el entorno de producci�n. Ver [op.acc.3] sobre segregaci�n de funciones. Para que la segregaci�n sea cre�ble, se deben separar los entornos y controlar los mecanismos de identificaci�n, autenticaci�n y control de acceso de los usuarios diferenciando rigurosamente los privilegios de cada uno.<br/><br/>514. La metodolog�a de desarrollo conviene que sea un est�ndar reconocido que incluya la seguridad como parte integral del desarrollo (por ejemplo, METRICA, Security Development Lifecycle, Correctness by Construction, Building Security In Maturity Model, OWASP, etc.). Es decir, desde la concepci�n arquitect�nica hay que plantear los requisitos de seguridad del sistema final e ir optando por soluciones que introduzcan los controles necesarios en el software desarrollado.<br/><br/>515. Hay que evitar que se desarrolle pensando �nicamente en la funcionalidad y que los requisitos de seguridad se a�adan posteriormente parcheando.<br/><br/>516. Desarrollo integral significa que las funciones de seguridad son parte de la interfaz de usuario, que los registros de actividad e incidencias son parte de la arquitectura de registro y que existen mecanismos de validaci�n, protecci�n de la informaci�n y verificaci�n de que se respeta la pol�tica de seguridad deseada.<br/><br/>517. Durante las pruebas de desarrollo y de aceptaci�n no se usar�n datos de prueba reales, sino datos espec�ficos para pruebas. Cuando los datos de prueba procedan de datos reales, se manipular�n para que no se puedan reconocer datos reales en las pruebas. En �ltimo caso, si fuera inevitable usar datos reales, se proteger�n como si estuvieran en producci�n. Por �ltimo, los datos de prueba deben retirarse cuando el sistema pasa a producci�n.<br/><br/>518. La inspecci�n del c�digo fuente debe ser posible tanto durante el desarrollo como durante la vida �til del software. Inspeccionar todo el c�digo es costoso y probablemente injustificado en los sistemas de soporte al ENS; pero es necesario acceder al c�digo fuente para analizar incidentes y para planificar pruebas de penetraci�n. Por ello debe estar disponible con las debidas garant�as de control de acceso.<br/><br/>519. En todo caso hay que revisar fallos t�picos de programaci�n que puedan derivar en problemas de seguridad:<ul style="list-style-type:square"><li>desbordamiento de buffers,</li><li>informaci�n residual en almacenamiento temporal (RAM, ficheros en disco, datos en la red, datos en la nube, �),</li><li>almacenamiento de claves y material criptogr�fico,</li><li>validaci�n de los datos de entrada, de usuarios y entre procesos,</li><li>validaci�n de la configuraci�n,</li><li>posibilidades de inyecci�n de c�digo,</li><li>posibles race conditions (carreras de concurrencia),</li><li> escalado de privilegios,</li><li>comunicaciones sin autenticar y/o sin cifrar,</li><li>etc.</li></ul>520. Se incluyen normas de programaci�n segura. Se recomienda adoptar soluciones automatizadas de an�lisis de c�digo est�tico que permitan verificar ante cada nueva versi�n que no es publicada con errores de programaci�n conocidos.<br/><br/>521. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-205 - Actividades Seguridad Ciclo Vida CIS</li></ul>522. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>9.4.5 - Control de acceso al c�digo fuente de los programas</li><li>12.1.4 - Separaci�n de los recursos de desarrollo, prueba y operaci�n</li><li>14.2.1 - Pol�tica de desarrollo seguro</li><li>14.2.5 - Principios de ingenier�a de sistemas seguros</li><li>14.2.6 - Entorno de desarrollo seguro</li><li>14.2.7 - Externalizaci�n del desarrollo de software</li><li>14.3.1 - Protecci�n de los datos de prueba</li></ul></ul>523. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CM-4] (1) Security Impact Analysis - Separate Test Environments</li><li>[SA-3] System Development Life Cycle</li><li>[SA-4] Acquisition Process</li><li>[SA-8] Security Engineering Principles</li><li>[SA-10] Developer Configuration Management</li><li>[SA-11] Developer Security Testing and Evaluation</li><li>[SA-12] Supply Chain Protections</li><li>[SA-15] Development Process, Standards, and Tools</li><li>[SA-17] Developer Security Architecture and Design</li></ul>524. Otras referencias:<ul style="list-style-type:square"><li>SANS</li>http://www.sans.org/curricula/secure-software-development<li>M�trica v3 - Metodolog�a de Planificaci�n, Desarrollo y Mantenimiento de sistemas de informaci�n, Ministerio de Administraciones P�blicas, Consejo Superior de Administraci�n Electr�nica</li><li>NIST SP 800-64 - Security Considerations in the System Development Life Cycle</li></ul><h3>5.6.2 [MP.SW.2] ACEPTACI�N Y PUESTA EN SERVICIO: Categor�a ALTA</h3>530. El an�lisis de coherencia se hace a nivel de procesos, concretamente de los que componen el proceso administrativo que le compete a la organizaci�n. Para cada proceso propio, hay que ejecutar pruebas comprobando que los datos de entrada producen los datos de salida correctos, y que datos incorrectos de entrada son detectados y atajados antes de destruir la integridad del sistema.<br/><br/>531. Para categor�a ALTA, el ENS pide que se considere una auditor�a de c�digo fuente. Se refiere a la expresi�n inglesa "source code review" y no puede ser obligatorio para todos los sistemas ya que es un proceso desproporcionadamente lento y costoso. Adem�s, es un proceso cuya profundidad es muy modulable.<br/><br/>532. La revisi�n de c�digo fuente va m�s all� del empleo de herramientas automatizadas para buscar librer�as, funciones o patrones de vulnerablidades, aspectos que ya se contemplan en categor�a MEDIA. La revisi�n de c�digo fuente es una actividad que requiere inteligencia humana para revisar sistem�ticamente que el c�digo se ejecutar� de forma segura sin dejarle oportunidades a incidentes accidentales o deliberados, que no quedan puertas abiertas y que los controles de seguridad est�n implantados de forma efectiva. Por una parte, se busca que no haya vulnerabilidades y por otra que la aplicaci�n sea capaz de defenderse a s� misma (self-defending) en el contexto en el que va a operar.<br/><br/>533. Esta actividad de expertos suele apoyarse en herramientas de auditor�a y ataques controlados de penetraci�n; pero va un paso m�s all� a analizar la integraci�n de piezas de c�digo o componentes. Las herramientas son ideales para tratar sistem�ticamente grandes vol�menes de c�digo y para validar que las vulnerabilidades son efectivamente explotables. Las personas son necesarias para comprender el contexto.<br/><br/>534. Por ejemplo, se buscan carreras (race conditions) en ejecuci�n concurrente, oportunidades de escalar privilegios, fallos de limpieza de informaci�n sensible, acceso seguro a otros servicios, existencia de credenciales empotrados en el c�digo, etc.<br/><br/>535. A efectos de cumplir con lo prescrito en el ENS, se valorar� la oportunidad de proceder a la inspecci�n del c�digo fuente; pero en la pr�ctica solo se justifica en sistemas cr�ticos como pueden ser elementos de frontera con una red p�blica y solamente si el software no est� acreditado en el sentido de [op.pl.5].<br/><br/>536. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>12.1.4 - Separaci�n de los recursos de desarrollo, prueba y operaci�n</li><li>12.5.1 - Instalaci�n del software en explotaci�n</li><li>14.2.8 - Pruebas funcionales de seguridad de sistemas</li><li>14.2.9 - Pruebas de aceptaci�n de sistemas</li><li>14.2.7 - Externalizaci�n del desarrollo de software</li><li>14.3.1 - Protecci�n de los datos de prueba</li></ul></ul>537. NIST SP 800-53 rev. 4<br/><br/>538. Otras referencias:<ul style="list-style-type:square"><li>M�trica v3 - Metodolog�a de Planificaci�n, Desarrollo y Mantenimiento de sistemas de informaci�n, Ministerio de Administraciones P�blicas, Consejo Superior de Administraci�n Electr�nica</li></ul><h3>5.7.1 [MP.INFO.1] DATOS DE CAR�CTER PERSONAL</h3>539. Es obligatorio el cumplimiento de la regulaci�n de protecci�n de informaci�n personal que est� vigente, ya sean las medidas de protecci�n determinadas para cada nivel en el Real Decreto 1720/2007 o las especificaciones del Reglamento General de Protecci�n de Datos.<br/><br/>540. Referencias<ul style="list-style-type:square"><li>Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016, relativo a la protecci�n de las personas f�sicas en lo que respecta al tratamiento de datos personales y a la libre circulaci�n de estos datos</li><li>Ley Org�nica 15/1999, de 13 de diciembre, de Protecci�n de Datos de Car�cter Personal (B.O.E. N� 298, de 14 de diciembre de 1999)</li><li>Real Decreto 1720/2007 de 21 de diciembre, por el que se aprueba el Reglamento de desarrollo de la Ley Org�nica 15/1999, de 13 de diciembre, de protecci�n de datos de car�cter personal</li><li>Real Decreto 3/2010, de 8 de enero, del Esquema Nacional de Seguridad</li><li>Real Decreto 951/2015, de 23 de octubre, de modificaci�n del Real Decreto 3/2010, de 8 de enero, por el que se regula el Esquema Nacional de Seguridad en el �mbito de la Administraci�n Electr�nica</li></ul><h3>5.7.2 [MP.INFO.2] CALIFICACI�N DE LA INFORMACI�N</h3>541. Se debe establecer un esquema para asignar un nivel de calificaci�n a la informaci�n, en funci�n de sus necesidades de confidencialidad.<br/><br/>542. El sistema de calificaci�n:<ul style="list-style-type:square"><li>debe ser acorde con otros sistemas de calificaci�n propios del entorno en el que desarrolla su actividad la organizaci�n</li><li>debe ser acorde con lo indicado en el Anexo I del ENS sobre calificaci�n de la informaci�n y categorizaci�n de los sistemas de informaci�n</li><li>debe establecer las responsabilidades para adscribir inicialmente una cierta informaci�n a una cierta calificaci�n y para posibles re-calificaciones posteriores (niveles de seguridad) y determinar el responsable de la documentaci�n y aprobaci�n formal</li></ul>543. Se deben desarrollar procedimientos de uso de la informaci�n para cada nivel (etiquetado y tratamiento), cubriendo al menos los siguientes aspectos:<ul style="list-style-type:square"><li>c�mo se controla el acceso, es decir, normativa, y procedimientos de autorizaci�n y mecanismos de control [op.acc]</li><li>c�mo se realiza el almacenamiento (local, en la nube, cifrado, etc.) [mp.si.2] y [mp.si.3]</li><li>normativa relativa a la realizaci�n de copias en diferentes medios: proceso de autorizaci�n y mecanismos de control [mp.info.9]</li><li>c�mo se marcan los documentos (etiquetado de soportes) [mp.si.1]</li><li>condiciones de adquisici�n, inventario, marcado, uso, borrado y destrucci�n de los soportes de informaci�n</li><li>c�mo se gestiona el papel impreso y qui�n y d�nde puede imprimir</li><li>transporte f�sico: condiciones sobre el medio de transporte, del mensajero, autorizaciones de salida y controles de recepci�n</li><li>condiciones de seguridad sobre el canal de comunicaciones (especialmente, autenticaci�n y cifrado) y autorizaciones necesarias para poder trasmitir por redes de comunicaciones [mp.com]</li></ul>544. Cabe esperar que los organismos organicen la informaci�n en tres niveles: BAJO, MEDIO y ALTO, alineados a los niveles del Anexo I. Siguiendo este esquema, se pueden desarrollar tablas como la siguiente:<br/><br/><table style="width:100%" border="1"><tr><th>Elemento de ejemplo</th><th>Bajo</th><th>Medio</th><th>Alto</th></tr><tr><td>autorizador de acceso [org.4]</td><td><ul><li>accesible a todo el personal propio</li></ul></td><td><ul><li>accesible a los que lo necesitan conocer por sus funciones</li></ul></td><td><ul><li>autorizaci�n del organismo a la persona</li></ul></td></tr><tr><td>copias impresas [mp.si]</td><td><ul><li>marcadas</li><li>cada persona se encarga de su destrucci�n cuando ya no hace falta</li></ul></td><td><ul><li>marcadas</li><li>destrucci�n usando destructora</li></ul></td><td><ul><li>marcadas</li><li>se lleva un inventario de las copias realizadas</li><li>destrucci�n procedimentada con actualizaci�n del inventario</li></ul></td></tr><tr><td>soportes electr�nicos de informaci�n [mp.si]</td><td><ul><li>etiquetados</li><li>se borra el contenido o se inhabilita</li></ul></td><td><ul><li>etiquetados</li><li>se cifra el contenido</li><li>se usa software de borrado seguro o se destruye</li></ul></td><td><ul><li>etiquetados</li><li>se cifra el contenido</li><li>se usa software de borrado seguro o se destruye en trituradora homologada</li></ul></td></tr><tr><td>uso en equipos port�tiles y PDAs [mp.info.3] [mp.eq.3]</td><td><ul><li>con control de acceso</li></ul></td><td><ul><li>con control de acceso</li></ul></td><td><ul><li>debe estar cifrada en reposo</li></ul></td></tr><tr><td>transmisi�n telem�tica [mp.com.2] [mp.com.3]</td><td><ul><li>canales autenticados</li></ul></td><td><ul><li>canales autenticados y cifrados</li></ul></td><td><ul><li>canales autenticados y cifrados</li></ul></td></tr></table>Tabla 5: Ejemplo de criterios de uso de acuerdo con la calificaci�n de la informaci�n seg�n categor�a del sistema<br/><br/>545. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-001 - Seguridad de las TIC que manejan informaci�n nacional clasificada en la Administraci�n</li></ul>546. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>8.1.2 - Propiedad de los activos</li><li>8.2.1 - Clasificaci�n de la informaci�n</li></ul></ul>547. NIST SP 800-53 rev.<h3>5.7.3 [MP.INFO.3] CIFRADO</h3>548. Se debe cifrar la informaci�n de nivel alto, tanto durante su almacenamiento (mp.si.2) como durante su transmisi�n (mp.com.2). S�lo estar� en claro mientras se est� haciendo uso de ella. Esto incluye:<ul style="list-style-type:square"><li>cifrado de ficheros</li><li>cifrado de directorios</li><li>discos virtuales cifrados</li><li>cifrado de datos en bases de datos</li></ul>549. Se debe cifrar la informaci�n en funci�n de su calificaci�n y el medio en el que se almacena.<br/><br/>550. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-807 � Criptograf�a de empleo en el ENS</li><li>Gu�a CCN-STIC-955 - Recomendaciones empleo GnuPG v 1.4.7</li><li>Gu�a CCN-STIC-955 B - Recomendaciones empleo GPG</li></ul>551. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>10.1.1 - Pol�tica de uso de los controles criptogr�ficos</li><li>14.1.3 - Protecci�n de las transacciones de servicios de aplicaciones</li><li>18.1.5 - Regulaci�n de los controles criptogr�ficos</li></ul></ul>552. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[SC-13] Cryptographic Protection</li><li>[SC-28] Protection of Information at Rest</li></ul>553. Otras referencias:<ul style="list-style-type:square"><li>GNUPG � The GNU Privacy Guard</li><li>PGP � Pretty Good Privacy</li><li>Veracrypt</li></ul><h3>5.7.4 [MP.INFO.4] FIRMA ELECTR�NICA</h3>554. Todas las actividades relacionadas con la firma electr�nica y el sellado de tiempo deben regirse por un marco t�cnico y procedimental aprobado formalmente. Se suele denominar Pol�tica de Firma.<br/><br/>555. En el caso de que se utilicen otros mecanismos de firma electr�nica sujetos a derecho, el sistema debe incorporar medidas compensatorias suficientes que ofrezcan garant�as equivalentes o superiores en lo relativo a prevenci�n del repudio.<br/><br/><b>Pol�tica de firma electr�nica</b><br/><br/>556. Pol�tica de firma electr�nica. En el caso de la Administraci�n General del Estado, debe cumplir los requisitos establecidos en el art�culo 24 del Real Decreto 1671/2009.<br/><br/>557. En todos los casos debe cubrir los siguientes puntos t�cnicos y procedimentales:<ul style="list-style-type:square"><li>delimitaci�n del �mbito de aplicaci�n; es decir, qu� informaci�n ir� firmada y en qu� procesos o procedimientos se firmar� y se verificar� cada firma</li><li>los roles y funciones del personal involucrado en la generaci�n y verificaci�n de firmas</li><li>los roles y funciones del personal involucrado en la administraci�n de los medios de firma</li><li>los roles y funciones del personal involucrado en la generaci�n, custodia y distribuci�n de claves y certificados</li><li>directrices y normas t�cnicas aplicables a la utilizaci�n de certificados y firmas electr�nicas</li><li>los requisitos exigibles a las firmas electr�nicas presentadas</li><li>los medios de validaci�n y verificaci�n de firmas: protocolos y prestadores del servicio</li></ul>558. En la Administraci�n General del Estado se dispone de un marco de referencia.<br/>Ver http://administracionelectronica.gob.es/es/ctt/politicafirma<br/><br/>559. La pol�tica de firma debe cumplir los requisitos del Esquema Nacional de Interoperabilidad.<br/><br/>560. En cualquier escenario se debe buscar una interoperabilidad de las firmas electr�nicas por lo que se recomienda fuertemente que los organismos referencien la pol�tica de firma de electr�nica de un �rgano superior y s�lo en muy contadas ocasiones se establezca una pol�tica independiente.<br/><br/><b>Uso de claves concertadas para firmar</b><br/><br/>561. La firma con un secreto compartido requiere algunas cautelas.<br/><br/>562. Lo m�s que podemos hacer es:<ul style="list-style-type:square"><li>presentarle la informaci�n al ciudadano en una p�gina web</li><li>pedirle que introduzca la clave de firma (sin memoria: hay que introducirla expresamente)</li><li>conservar como evidencia el HMAC23 (documento + clave_concertada)</li></ul>563. Este mecanismo garantiza la integridad del documento e identifica al ciudadano; pero no garantiza el no-repudio ya que cualquiera que puede verificar la firma, puede tambi�n generarla. Es decir, no cumple los requisitos de una firma electr�nica avanzada, que requiere que �haya sido creada por medios que el firmante puede mantener bajo su exclusivo control� (Ley 59/2003).<br/><br/>564. Se considerar� firma electr�nica, sin m�s.<br/><br/><b>C�digo seguro de verificaci�n</b><br/><br/>565. Se trata de una forma alternativa de asegurar la autenticidad e integridad de la informaci�n proporcionada por la Administraci�n.<br/><br/>566. En lugar de proteger la informaci�n por medio de una firma inviolable, lo que se proporciona es una forma c�moda de verificar que la informaci�n es aut�ntica y no se ha modificado (es �ntegra).<br/><br/>567. El sistema de c�digo seguro de verificaci�n (CSV) deber� garantizar, en todo caso:<ul style="list-style-type:square"><li>El car�cter �nico del c�digo generado para cada documento.</li><li>Su vinculaci�n con el documento generado y con el firmante.</li><li>Asimismo, se debe garantizar la posibilidad de verificar el documento por el tiempo que se establezca en la resoluci�n que autorice la aplicaci�n de este procedimiento.</li></ul>568. La Administraci�n queda obligada a:<ul style="list-style-type:square"><li>garantizar la disponibilidad del mecanismo de verificaci�n</li><li>garantizar la integridad del documento referenciado</li><li>garantizar la confidencialidad del documento correspondiente; por ejemplo, controlando el acceso para que s�lo accedan las personas autorizadas</li></ul>569. Una forma f�cil de proporcionar CSVs es usar un n�mero consecutivo en un archivo documental identificado (lo que ser�a una clave primaria en una base de datos documental). Al ciudadano hay que proporcionarle la identificaci�n del archivo y el n�mero de expediente.<br/><br/>570. Una forma f�cil de cumplir los requisitos de autenticidad e integridad es que el documento referenciado por medio del CSV, sea en s� mismo un documento firmado electr�nicamente. De esta forma, el ciudadano (o cualquier tercera parte autorizada) puede en cualquier momento recabar el documento y conservarlo en su poder.<br/><br/><b>Integridad o autenticidad: nivel ALTO</b><br/><br/>577. Se usa una firma electr�nica cualificada, que incorpora certificados cualificados y dispositivos cualificados de creaci�n de firma.<br/><br/>578. Se emplean productos certificados, conforme a lo establecido en [op.pl.5].<br/><br/>579. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-807 � Criptograf�a de empleo en el ENS</li><li>Gu�a CCN-STIC-405 - Algoritmos y Par�metros de Firma Electr�nica</li></ul>580. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>10.1.1 - Pol�tica de uso de los controles criptogr�ficos</li><li>14.1.3 - Protecci�n de las transacciones de servicios de aplicaciones</li><li>18.1.5 - Regulaci�n de los controles criptogr�ficos</li></ul></ul>581. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[SC-13] Cryptographic Protection</li><li>[SC-28] Protection of Information at Rest</li></ul>582. Otras referencias:<ul style="list-style-type:square"><li>Reglamento (UE) 910/2014, del Parlamento Europeo y el Consejo, de 23 de julio de 2014, relativo a la identificaci�n electr�nica (eID) y los servicios de confianza para transacciones electr�nicas en el mercado interior y por la que se deroga la Directiva 1999/93/CE</li><li>Real Decreto 1671 de 2009</li><li>IST SP 800-89 - Recommendation for Obtaining Assurances for Digital Signature Applications</li><li>Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Com�n de las Administraciones P�blicas.</li><li>Ley 40/2015, de 1 de octubre, de R�gimen Jur�dico del Sector P�blico.</li><li>Real Decreto 1065/2007, de 27 de julio, por el que se aprueba el Reglamento General de las actuaciones y los procedimientos de gesti�n e inspecci�n tributaria y de desarrollo de las normas comunes de los procedimientos de aplicaci�n de los tributos.</li></ul><h3>5.7.5 [MP.INFO.5] SELLOS DE TIEMPO</h3>583. Los sellos de tiempo previenen la posibilidad de un repudio posterior de la informaci�n que sea susceptible de ser utilizada como evidencia en el futuro, o que requiera capacidad probatoria seg�n la ley de procedimiento administrativo. Por ello, todas las actividades relacionadas con la firma electr�nica y el sellado de tiempo deben regirse por un marco t�cnico y procedimental aprobado formalmente. Se suele denominar Pol�tica de Firma.<br/><br/>584. Debe identificarse y establecerse el tiempo de retenci�n de la informaci�n.<br/><br/>585. Se fechan electr�nicamente los documentos cuya fecha y hora de entrada debe acreditarse fehacientemente.<br/><br/>586. Se fechan electr�nicamente los documentos cuya fecha y hora de salida debe acreditarse fehacientemente.<br/><br/>587. Se fechan electr�nicamente las firmas cuya validez deba extenderse por largos periodos o as� lo exija la normativa aplicable, hasta que la informaci�n protegida ya no sea requerida por el proceso administrativo al que da soporte; alternativamente se pueden utilizar formatos de firma avanzada que incluyan fechado.<br/><br/>588. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-807 Criptograf�a de empleo en el ENS</li></ul>589. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>14.1.3 - Protecci�n de las transacciones de servicios de aplicaciones</li></ul></ul>590. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AU-10] Non-repudiation</li><br/><li>ISO/IEC 18014-1:2008<br/>Information technology � Security techniques � Time-stamping services �<br/>Part 1: Framework</li><br/><li>ISO/IEC 18014-2:2009<br/>Information technology � Security techniques � Time-stamping services �<br/>Part 2: Mechanisms producing independent tokens</li><br/><li>ISO/IEC 18014-3:2009<br/>Information technology � Security techniques � Time-stamping services �<br/>Part 3: Mechanisms producing linked tokens</li><br/><li>ISO/IEC TR 29149:2012<br/>Information technology � Security techniques �<br/>Best practices for the provision and use of time-stamping services</li><br/><li>RFC 3161 Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP)</li><br/><li>Ley 39/2015, de 1 de octubre, de Procedimiento Administrativo Com�n de las Administraciones P�blicas.</li><br/><li>Ley 40/2015, de 1 de octubre, de R�gimen Jur�dico del Sector P�blico.</li></ul><h3>5.7.6 [MP.INFO.6] LIMPIEZA DE DOCUMENTOS</h3>591. Se debe retirar de los documentos que van a ser trasferido a un �mbito fuera del dominio de seguridad toda la informaci�n adicional contenida en campos ocultos, meta-datos, comentarios, revisiones anteriores, etc. salvo cuando dicha informaci�n sea pertinente para el receptor del documento.<br/><br/>592. Esta medida es especialmente relevante cuando el documento se difunde ampliamente, como ocurre cuando se ofrece al p�blico en un servidor web u otro tipo de repositorios de informaci�n.<br/><br/>593. El incumplimiento de esta medida puede perjudicar:<ul style="list-style-type:square"><li>al mantenimiento de la confidencialidad de informaci�n que no deber�a haberse revelado al receptor del documento</li><li>al mantenimiento de la confidencialidad de las fuentes u or�genes de la informaci�n, que no debe conocer el receptor del documento</li><li>a la buena imagen de la organizaci�n que difunde el documento por cuanto demuestra un descuido en su buen hacer</li></ul>594. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-835 Borrado de metadatos en el marco del ENS</li></ul>595. NIST SP 800-53 rev. 4<h3>5.7.7 [MP.INFO.7] COPIAS DE SEGURIDAD (BACKUP)</h3>596. Se deben realizar copias de respaldo que permitan recuperar datos perdidos accidental o intencionadamente con una antig�edad a determinar por la organizaci�n.<br/><br/>597. Las copias de respaldo poseer�n el mismo nivel de seguridad que los datos originales en lo que se refiere a integridad, confidencialidad, autenticidad y trazabilidad. En particular, debe considerarse la conveniencia o necesidad de que las copias de seguridad est�n cifradas para garantizar la confidencialidad (en cuyo caso se estar� a lo dispuesto en [op.exp.11]).<br/><br/>598. Se recomienda establecer un proceso de autorizaci�n para la recuperaci�n de informaci�n de las copias de respaldo.<br/><br/>599. Se recomienda conservar las copias de respaldo en lugar(es) suficientemente independiente(s) de la ubicaci�n normal de la informaci�n en explotaci�n como para que los incidentes previstos en el an�lisis de riesgos no se den simult�neamente en ambos lugares, por ejemplo, si se conservan en la misma sala utilizar un armario ign�fugo.<br/><br/>600. El transporte de copias de respaldo desde el lugar donde se producen hasta su lugar de almacenamiento garantiza las mismas seguridades que los controles de acceso a la informaci�n original.<br/><br/>601. Las copias de respaldo deben abarcar:<ul style="list-style-type:square"><li>informaci�n de trabajo de la organizaci�n</li><li>aplicaciones en explotaci�n, incluyendo los sistemas operativos</li><li>datos de configuraci�n, servicios, aplicaciones, equipos, etc.</li><li>claves utilizadas para preservar la confidencialidad de la informaci�n</li></ul>602. Para los puntos anteriores ver [op.exp] y [mp.info.3].<br/><br/>603. El responsable de la informaci�n debe determinar la frecuencia con la que deben realizarse las copias y el periodo de retenci�n durante el que mantenerlas.<br/><br/>604. En caso de disponer de un Plan de Continuidad, las copias de seguridad deber�n realizarse con una frecuencia que permita cumplir con el RPO y con un objetivo de tiempo de restauraci�n que permita cumplir el RTO.<br/><br/>605. Se recomienda realizar peri�dicamente pruebas de restauraci�n de copias de seguridad.<br/><br/>606. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>12.3.1 - Copias de seguridad de la informaci�n</li></ul></ul>607. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[CP-6] Alternate Storage Site</li><li>[CP-9] Information System Backup</li><li>[CP-10] Information System Recovery and Reconstitution</li></ul>608. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.10 - Data Recovery Capability</li></ul></ul><h3>5.8.1 [MP.S.1] PROTECCI�N DEL CORREO ELECTR�NICO (E-MAIL)</h3>609. Cuando se ofrezca correo electr�nico como parte del sistema, deber� protegerse frente a las amenazas que le son propias mediante:<ul style="list-style-type:square"><li>Protecci�n del cuerpo de los mensajes y documentos adjuntos que pueda contener el correo electr�nico</li><li>Protecci�n del encaminamiento de mensajes (por ejemplo, protegiendo el servidor DNS y su configuraci�n) y del establecimiento de las conexiones (impidiendo que el usuario final pueda conectarse a un servidor de correo que no sea el corporativo)</li><li>Protecci�n de la organizaci�n frente a correos no solicitados (spam), virus, gusanos, troyanos, programas esp�as (spyware) y c�digo m�vil tipo applet (por ejemplo, con la instalaci�n de un antivirus, ya sea en el servidor de correo o en el puesto de usuario)</li><li>Limitaci�n del uso del correo electr�nico al estrictamente profesional y concienciaci�n y formaci�n relativas al uso adecuado del mismo</li></ul>610. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-681 � Configuraci�n segura de servidores de correo Postfix</li><li>Gu�a CCN-STIC-682 � Configuraci�n segura de Sendmail</li><li>Gu�a CCN-STIC-814 � Seguridad en Correo electr�nico</li></ul>611. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>13.2.3 - Mensajer�a electr�nica</li></ul></ul>612. NIST 800-53 rev. 4<ul style="list-style-type:square"><li>[SI-8] Spam Protection</li></ul>613. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.7 - Email and Web Browser Protections</li></ul><li>NIST SP 800-45 � Guidelines on Electronic Mail Security</li></ul><h3>5.8.2 [MP.S.2] PROTECCI�N DE SERVICIOS Y APLICACIONES WEB</h3>614. Se debe proteger a los subsistemas dedicados a la publicaci�n de informaci�n frente a los ataques o amenazas que les son propias.<br/><br/>615. Una serie de medidas son preventivas, poniendo el �nfasis en los procesos de<ul style="list-style-type:square"><li>desarrollo de aplicaciones y servicios (mp.sw),</li><li>configuraci�n de seguridad (op.exp.2 y op.exp.3),</li><li>en los controles de mantenimiento (op.exp.4) y</li><li>en las protecciones de separaci�n de tareas (op.acc.3).</li></ul>616. Las tareas preventivas no excusan de un sistema de monitorizaci�n y reacci�n frente a ataques exitosos.<br/><br/>617. Pueden presentarse ataques a nivel de red, a nivel del sistema operativo del servidor y a nivel de la aplicaci�n que atiende a peticiones web. De los dos primeros modos de ataque nos defenderemos protegiendo el equipo de frontera.<br/><br/>618. B�sicamente hay 2 formas de proteger el servidor frontal: protegiendo el equipo y el software que proporciona la interfaz para acceso al servicio web, o disponiendo una protecci�n previa en forma de cortafuegos de aplicaci�n (appliance) entre el servidor y los usuarios.<br/><br/>619. Los ataques a nivel de aplicaci�n pueden detectarse en el servidor frontal o en alg�n servidor de soporte en la retaguardia; es decir, puede haber ataques que aparecen como correctos (sint�cticamente correctos) pero que causan problemas por el tipo de petici�n o por la secuencia de peticiones (sem�ntica incorrecta). Para los ataques que entran en el nivel interno ser� necesario desarrollar reglas espec�ficas para detectar y reaccionar. Reglas de tipo:<ul style="list-style-type:square"><li>l�mite en el n�mero de sesiones, total o por usuario an�nimo o identificado</li><li>cierre de sesiones al cabo de un tiempo</li><li>l�mite en el volumen de datos (individual y agregado)</li></ul>620. Para verificar que en el proceso de desarrollo de la aplicaci�n se han establecido los controles frente a ataques potenciales se deben identificar posibles vulnerabilidades a corregir. Para ello se pueden realizar auditor�as de seguridad peri�dicas o pruebas de penetraci�n (hacking �tico) de los servicios y aplicaciones web para posteriormente modificar el aplicativo o establecer elementos que lo protejan al menos frente a:<ul style="list-style-type:square"><li>Ataques que eviten el control de acceso obviando la autenticaci�n, si la hubiera, mediante accesos por v�as alternativas al protocolo predefinido (por ejemplo, HTTP y HTTPS, manipulaciones de URL o cookies o ataques de inyecci�n de c�digo (como introducir caracteres no autorizados por la aplicaci�n).</li><li>Ataques de escalado de privilegios (como ejecutar acciones haci�ndose pasar por otro usuario).</li><li>Ataques de Cross Site Scripting (XSS) que permiten robar informaci�n delicada, secuestrar sesiones de usuario o comprometer la integridad del sistema (introduciendo informaci�n en la p�gina web que se muestre as� posteriormente al usuario, por ejemplo).</li><li>Ataques de manipulaci�n de proxies y cach�s, en caso de utilizar estas tecnolog�as.</li></ul>621. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Serie CCN-STIC-500 - Gu�as para Entornos Windows</li><li>Serie CCN-STIC-600 - Gu�as para otros Entornos</li><li>Gu�a CCN-STIC-812 - Seguridad en entornos y aplicaciones Web</li></ul>622. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>14.1.2 - Asegurar los servicios de aplicaciones en redes p�blicas</li></ul></ul>623. NIST SP 800-53 rev. 4<br/><br/>624. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.7 - Email and Web Browser Protections</li></ul><li>NIST SP 800-44 - Guidelines on Securing Public Web Servers</li><li>PCI-DSS v3.0</li><ul style="list-style-type:circle"><li>Requisito 6: Desarrolle y mantenga sistemas y aplicaciones seguras</li></ul></ul><h3>5.8.3 [MP.S.3] PROTECCI�N FRENTE A LA DENEGACI�N DE SERVICIO</h3>625. Se deben establecer medidas preventivas y reactivas frente a ataques de denegaci�n de servicio (DoS).<br/><br/>626. Los ataques de denegaci�n de servicio pueden prevenirse dimensionando con holgura los elementos susceptibles de ser atacados desde el exterior, aunque poco se puede hacer frente a un ataque con suficientes recursos por parte del atacante.<br/><br/>627. M�ltiples ataques de denegaci�n de servicio son facilitados por un software deficiente por parte del servidor, bien porque no se han actualizado las versiones, bien porque la configuraci�n no es id�nea. Ambos aspectos deber�n ser analizados y reparados (ver medidas de protecci�n [mp.exp] en lo relativo a configuraci�n, mantenimiento y cambios), de modo que se actualicen y bastionen las tecnolog�as utilizadas de cara a prevenir ataques conocidos.<br/><br/>628. Aun estando preparados, podemos ser v�ctimas de un nuevo tipo de ataque imprevisto, en cuyo caso hay que detectarlo r�pidamente y gestionar la incidencia.<br/><br/>629. Los ataques de denegaci�n de servicio pueden ser detectados y afrontados en el per�metro ([mp.com.1]), aunque pueden requerir la intervenci�n de otros elementos. En el per�metro se pueden detectar patrones sospechosos de comportamiento: avalanchas de peticiones, peticiones trucadas y, en general, un uso malicioso de los protocolos de comunicaciones. Algunas de estas peticiones pueden ser denegadas directamente por el equipo perimetral, en otras ocasiones hay que reaccionar ante ellos y levantar una alarma para actuar en donde corresponda (servidores web, servidores de bases de datos�, y contactando con el proveedor de comunicaciones o los centros de respuesta a incidentes, CERT). Por tanto, es importante disponer de un procedimiento documentado que indique el procedimiento de reacci�n ante los ataques.<br/><br/>630. Es responsabilidad del organismo detectar y bloquear el uso deliberado o accidental del propio sistema de informaci�n para atacar a terceros desde las propias instalaciones. N�tese que el organismo puede ser simplemente v�ctima de una infecci�n da�ina de elementos agresivos que son lanzados contra otros o de un ataque deliberado por parte de un empleado interno y al proveedor de comunicaciones o al centro de respuesta de emergencia (CERT) para coordinar la respuesta.<br/><br/>631. Como posibles tecnolog�as a utilizar para prevenir ataques se encuentran los sistemas de detecci�n de intrusos (IDS), monitores con alarmas al alcanzar un consumo determinado de ancho de banda o de solicitud de peticiones, mecanismos para bloquear un n�mero elevado de conexiones internas concurrentes o para bloquear el env�o de grandes cantidades de informaci�n, etc.<br/><br/>632. Gu�as CCN-STIC:<ul style="list-style-type:square"><li>Gu�a CCN-STIC-820 � Gu�a de protecci�n contra Denegaci�n de Servicio</li></ul>633. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>12.1.3 - Gesti�n de capacidades</li></ul></ul>634. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP-2] (2) Contingency Plan - Capacity Planning</li><li>[SC-5] (2) Denial of Service Protection - Excess Capacity / Bandwidth / Redundancy</li></ul><h3>5.8.4 [MP.S.4] MEDIOS ALTERNATIVOS</h3>635. Se debe prever medios alternativos para ofrecer los servicios en el caso de que fallen los medios habituales, mientras se recupera la disponibilidad de �stos (como por ejemplo una instancia alternativa a un portal). Estos medios alternativos estar�n sujetos a las mismas garant�as de protecci�n.<br/><br/>636. Se debe establecer un tiempo m�ximo para que los servicios alternativos entren en funcionamiento.<br/><br/>637. Los servicios alternativos pueden estar dispuestos para entrar en servicio inmediatamente o requerir un tiempo de personalizaci�n. En todo caso, el tiempo de entrada en servicio debe estar respaldado por un an�lisis de impacto (ver [op.cont.1]).<br/><br/>638. El plan de utilizaci�n de servicios alternativos se vertebrar� dentro del plan de continuidad aprobado (ver [op.cont.2]) y ser objeto de pruebas regulares para validar la viabilidad del plan (ver [op.cont.3]).<br/><br/>639. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de los recursos de tratamiento de la informaci�n</li></ul></ul>640. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP] Contingency Planning</li></ul>'
ens_unescape = Markup(ens)		# Se formatea para la correcta maquetaci�n HTML.
table_STAFF = get_staff(cursor)	# Se obtiene el contenido de la tabla STAFF maquetado para HTML.
edit_STAFF = get_edit_staff()	# Se obtiene la cadena con la maquetaci�n HTML para la inserci�n de nuevo personal.
[table_and_edit_CSIRT,team_list_index,team_list_csirts,user_list] = get_csirt_and_edit(cursor)	# Se obtienen los datos para la gesti�n de la tabla CSIRT.
stats_option = get_stats_option()		# Recoge el interfaz de selecci�n para la generaci�n de estad�sticas y gr�ficas.
knowledge = get_knowledge(cursor,0)		# Recoge el interfaz maquetado HTML para el apartado de Conocimiento.
info = get_info()				# Recoge el interfaz maquetado HTML de la pesta�a Informaci�n. En este caso ser� una constante, no tendr� modificaci�n.

incident_updated = 0			# Flag para mostrar el aviso de actualizaci�n correcta de la incidencia.

go_tab = 'pestana1'				# Por defecto, el interfaz web se inicia en la primera pesta�a: gesti�n de incidentes.

email_CISO = 'CISO@soteria.es'	# Simula el correo del �rgano superior, en caso de que se necesite escalar el tratamiento de una incidencia.


		#######################################
		# CONTROLADORES DE LA APP WEB Soteria #
		#######################################
		
		
		##########
		# LOGOUT #
		##########
		
# El siguiente controlador permite realizar un logout seguro. El objetivo principal es implementar un sistema
# de logout seguro de la App Web que evite que se comprometa la seguridad del hogar del ciudadano:
@app.route('/logout')
def logout():
	
	# Debido al proceso de acceso, el logout en este caso consistir� en los siguientes pasos:
	
	# a) Borrar cookie de sesi�n de Google Authenticator:
	command_to_run = '/apache_2fa/remove_user.sh ' + session['current_user']	# Se asegura de eliminar s�lo el fichero relativo al usuario.
	return_code = call([ '/bin/bash', '-c', command_to_run ])

	# b) A continuaci�n, se realiza el logout de la App Web y el borrado de la sesi�n:
	logout_user()
	session.clear()
	
	# c) Por �ltimo, se redirecciona a la p�gina de despedida:	
	return render_template(app.config['DEFAULT_TPL']+'/logout.html',
							conf = app.config)
	
	# Llegado a este punto, para acceder requiere autenticarse de nuevo.
	# Si el usuario se deslogue� correctamente y sigui� las recomendaciones de seguridad,
	# tambi�n tendr� que volver a autenticarse mediante usuario y contrase�a + el PIN de Google Authenticator.
	# En caso contrario, tendr� que introducir solamente el PIN.
	# En cualquier caso, se impide el acceso directo a la sesi�n sin autenticarse de nuevo mediante alg�n m�todo.
	

# Cartel de presentaci�n de la plataforma Soteria:
@app.route('/', methods=['GET', 'POST'])   # M�todos habilitados: GEST() y POST().
def banner():

	session['tab_1_content'] = get_search_incidents()	# Se inicia en el interfaz por defecto: la b�squeda de incidencias.
	
	knowledge = get_knowledge(cursor,0)					# Recoge el interfaz principal maquetado HTML para el apartado de Conocimiento.

	#---------------------------------------------------------------------#
	# OBTENCI�N DEL USUARIO PARA CONTROL EN EL INTERFAZ Y PARA EL LOGOUT: #
	#---------------------------------------------------------------------#
	if not 'current_user' in session:
		last_user = commands.getoutput('/apache_2fa/get_user.sh')	# Permite extraer el usuario reci�n autenticado a partir de la cookie de Google Authenticator.
		session['current_user'] = last_user[len(last_user)-9:len(last_user)]
		
	return render_template(app.config['DEFAULT_TPL']+'/banner.html',		#########
							current_user = session['current_user'],
							conf = app.config)
						

# �ndice general de acceso a los contenidos:
@app.route('/index', methods=['GET', 'POST'])   # M�todos habilitados: GEST() y POST().
def index():
	
	# Se declaran las variables globales que se utilizar�n en este controlador:
	global go_tab
	global ens_unescape
	global table_STAFF
	global table_and_edit_CSIRT
	global team_list_index
	global team_list_csirts
	global user_list
	global knowledge
	global query_text
	global cursor
	global result
	global incident_updated	
	
	go_tab = 'pestana1'		# Por defecto, se mantiene en la pesta�a de Gesti�n de Incidentes.
	
	form_id = ''			# Recoge el ID del formulario recibido para control del procesado.
	
	message = ''
	
	js_code_init = ''
	new_incident_content = ''
	done = 0
	new_incident_ok = ''
	
	csirt_update_ok = ''
	csirt_updated = 0
	
	staff_update_ok = ''
	staff_updated = 0
	
	new_user_ok = ''
	new_user_added = 0
	
	query_text = ''
	start_date = ''
	stop_date = ''
	status = ''
	severity = ''
	dimensions = ''
	details = ''
	reports = ''
	originator = ''
	accountable = ''
	type = ''
	area = ''
	csirt = ''
	id_csirt = ''
	falses = ''

	error = 0	# Variable para control de validaci�n de la entrada de datos.
	
	show_graph = '0'
	data = []
	data_set1 = ''
	data_set2 = ''
	data_set3 = ''
	data_set4 = ''
	stats = ['0','0','0', '0', '0', '0']
	graph = ''
	graph_type = ''
	label = []
	labels = []
	num_elements = ''
	option = '0'
	huge_data = '0'
	MAX_VIEW = 25						# Servir� para control de visualizaci�n de las gr�ficas.
	
	if not 'id_incid' in session:		# Al insertarlo en el espacio de variables de sesi�n se podr� utilizar en peticiones POST diferentes.
		session['id_incid'] = ''

	if not 'tab_1_content' in session:
		session['tab_1_content'] = get_search_incidents()	# Formulario con los criterios de b�squeda de incidentes.

		
	if request.method == 'POST':		# El usuario ha ejecutado alguna selecci�n.
	
		global ens_unescape
		global query_text
		global cursor
		global result
		global table_and_edit_CSIRT
		global team_list_index
		global team_list_csirts
		global user_list
		
		form_id = request.form.get('form_id')	# Se lee el identificativo del formulario recibido.
		
		if form_id.find('edit_csirt') > -1:		# Se refiere a la modificaci�n de un equipo de respuesta => se procesa convenientemente.
			csirt_id_edit = request.form.get('csirt_id')	# Se obtiene el ID del CSIRT afectado.
			
			# A continuaci�n, se extraen por un lado los nombres originales de los nuevos componentes, y los nombres formateados para componer los c�digos de usuario:
			staff_1_original = user_list[int(request.form.get('staff_1'))]
			staff_1 = clean_username_joined(staff_1_original)
			staff_2_original = user_list[int(request.form.get('staff_2'))]
			staff_2 = clean_username_joined(staff_2_original)
			staff_3_original = user_list[int(request.form.get('staff_3'))]
			staff_3 = clean_username_joined(staff_3_original)
			
			new_team_t = staff_1 + staff_2 + staff_3
			
			if new_team_t.count(staff_1) > 1 or new_team_t.count(staff_2) > 1 or new_team_t.count(staff_3) > 1:
				message = Markup(u'swal("No se puede repetir la misma persona!", "\(Gesti�n de Incidencias\)", "warning", {button: "Aceptar",});')
			else:
			
				# Antes de realizar la sustituci�n, se extrae el equipo actual para poder determinar cu�l ha sido el cambio:
				cursor.execute("select team from CSIRT where id=%s", (team_list_csirts[int(csirt_id_edit)],))
				old_team_t = cursor.fetchall()
				old_team = str(old_team_t[0][0])
					
				extended_name = re.split(' ',staff_1)	# Se separa seg�n los espaciones en blanco. Se recuerda el formato: Apellido1 Apellido2, Nombre.
				new_team = extended_name[2][0:3] + extended_name[0][0:3] + extended_name[1][0:3]
				extended_name = re.split(' ',staff_2)	# Se separa seg�n los espaciones en blanco. Se recuerda el formato: Apellido1 Apellido2, Nombre.
				new_team +=  extended_name[2][0:3] + extended_name[0][0:3] + extended_name[1][0:3]
				extended_name = re.split(' ',staff_3)	# Se separa seg�n los espaciones en blanco. Se recuerda el formato: Apellido1 Apellido2, Nombre.
				new_team += extended_name[2][0:3] + extended_name[0][0:3] + extended_name[1][0:3]
							
				cursor.execute("UPDATE CSIRT SET team=%s WHERE id=%s", (new_team,team_list_csirts[int(csirt_id_edit)]))	# Se actualiza el equipo de respuesta en la BBDD.
				mariadb_connection.commit()																				# Se hacen efectivos los cambios en la BBDD.
					
				pos = 0
					
				# El modificar un Equipo de Respuesta es un evento de importancia, por lo que se precisa dejar reflajado en los detalles (hist�rico) de la incidencia:
				for i in range(27):
					if new_team[i] != old_team[i]:
						pos = i
						break
						
				cursor.execute("select surname,name from STAFF where user=%s", (old_team[pos:pos+9],)) # Se extrae el nombre completo del personal sustituido.
				old_name_t = cursor.fetchall()
				old_member = old_team[pos:(pos+9)]
				old_name = old_name_t[0][1] + ' ' + old_name_t[0][0]
				cursor.execute("select surname,name from STAFF where user=%s", (new_team[pos:pos+9],)) # Se extrae el nombre completo del personal que lo sustituye.
				new_name_t = cursor.fetchall()
				new_name = new_name_t[0][1] + ' ' + new_name_t[0][0]
				current_date = time.strftime("%d/%m/%Y")
				warning = "\n" + current_date + ': se sustituye el miembro del Equipo de Respuesta ' + old_name + ', por ' + new_name + '.'
				cursor.execute("select id,details from INCIDENTS where id_csirt=%s", (team_list_csirts[int(csirt_id_edit)],))
				data_incid = cursor.fetchall()
				id_incid_affected = data_incid[0][0]
				new_details = str(data_incid[0][1]) + warning
				cursor.execute("UPDATE INCIDENTS SET details=%s WHERE id=%s", (new_details,id_incid_affected))
				mariadb_connection.commit()
				
				# Se notifica el cambio a los tres componentes del Equipo:
				subject = 'ATENCION: se ha modificado un Equipo de Respuesta!'
				text = 'Se ha modificado el Equipo de Respuesta con ID: ' + str(team_list_csirts[int(csirt_id_edit)]) + ', en el que participa usted.'
				email_notify(new_team[0:9]+'@soteria.es',subject,text)
				email_notify(new_team[9:18]+'@soteria.es',subject,text)
				email_notify(new_team[18:27]+'@soteria.es',subject,text)
				
				# Al haber aplicado cambios, se hace necesario actualizar los datos:
				[table_and_edit_CSIRT,team_list_index,team_list_csirts,user_list] = get_csirt_and_edit(cursor)
				
				csirt_updated = 1		# Por �ltimo, se informa mediante el flag que el equipo se actualiz� correctamente.
				
			go_tab = 'pestana2'			# Se configura el interfaz web para continuar en la pesta�a de gesti�n de Equipos de Respuesta.
			
		elif form_id.find('new_staff') > -1:	# Se refiere al alta de nuevo personal de seguridad => se procesa convenientemente.
		
			error = 0
			
			surname = request.form.get('surname')
			name = request.form.get('name')
			status_staff = request.form.get('status_staff')
			
			error += only_alpha(surname)
			error += only_alpha(name)
			
			if error != 0:
				message = Markup(u'swal("Datos introducidos no v�lidos!", "\(Gesti�n de Personal\)", "error", {button: "Aceptar",});')
				go_tab = 'pestana4'
			else:
			
				# Se incorpora el nuevo usuario a la BBDD:
				surnames = re.split(' ',surname)
				new_user = clean_username(name,surnames)	# Devuelve el nombre de usuario filtrado: min�sculas y sin caracteres especiales.
				
				email = new_user + '@soteria.es'			# Formato direcci�n de correo electr�nico: "nombre_usuario"@soteria.es.
							
				query_text = "INSERT INTO STAFF (user, name, surname, status, email) VALUES (%s,%s,%s,%s,%s)"
				val = (new_user,name,surname,status_staff,email)
				cursor.execute(query_text,val)
					
				mariadb_connection.commit()		# Se hacen efectivos los cambios en la BBDD.
				
				# Se notifica el alta al personal:
				subject = 'ATENCION: ha sido dado de alta correctamente!'
				text = 'Bienvenido!\n\nHa sido incorporado a la Base de Datos de la plataforma Soteria correctamente.'
				email_notify(email,subject,text)
				
				new_user_added = 1		# Por �ltimo, se informa mediante el flag que el usuario se a�adi� correctamente,
				go_tab = 'pestana4'		# y se configura el interfaz web para continuar en la pesta�a de Gesti�n de Personal.
						
				# Al haber aplicado cambios, se hace necesario actualizar los datos:
				table_STAFF = get_staff(cursor)

		elif form_id.find('update_staff_status') > -1:	# Se refiere a la modificaci�n de la situaci�n de un profesional de seguridad.
			user_name = request.form.get('user_n')
			new_s_staff = request.form.get('new_status_staff')
			
			cursor.execute("UPDATE STAFF SET status=%s WHERE user=%s", (new_s_staff,user_name))	# Se actualiza la situaci�n del personal en la BBDD.
			mariadb_connection.commit()															# Se hacen efectivos los cambios en la BBDD.
			
			# Se comprueba si la baja afecta a alg�n Equipo de Respuesta:
			
			if new_s_staff.find('A') == -1:		# Se desea cambiar a cualquier otro estado diferente a '[A]ctivo'.
			
				# Se buscan los CSIRT's activos actualmente:
				cursor.execute("select team,id from CSIRT where id IN (select id_csirt from INCIDENTS where csirt='S' and (status='A' or status='U'))")
				active_csirts = cursor.fetchall()

				i = 0
				
				if active_csirts:	# Si hay CSIRT's activos:
					for row in active_csirts:
										
						if str(row).find(user_name) > -1:	# Se busca el personal que causa baja en los equipos activos.
							cursor.execute("SELECT user FROM STAFF where status='A' and user<>%s", (user_name,))
							active_users = cursor.fetchall()
							selected_user = active_users[random.randrange(len(active_users))][0]
							while active_csirts[i][0].find(selected_user) > -1:	# Se evitan los duplicados de personal en el mismo Equipo de Respuesta.
								selected_user = active_users[random.randrange(len(active_users))][0]
							new_team = active_csirts[i][0].replace(user_name,selected_user)
							cursor.execute("UPDATE CSIRT SET team=%s where id=%s", (new_team,active_csirts[i][1]))
							mariadb_connection.commit()		# Se hacen efectivos los cambios en la BBDD.
														
							# Se notifica el nombramiento para participar en el equipo al personal seleccionado:
							subject = 'ATENCION: ha sido seleccionado como componente de un Equipo de Respuesta!'
							text = 'Ha sido seleccionado para formar parte del Equipo de Respuesta con ID ' + str(active_csirts[i][1]) + ', por baja de personal.'
							email_notify(selected_user+'@soteria.es',subject,text)
							
							# Se registra en el campo de detalles de la incidencia afectada el cambio de composici�n del Equipo de Respuesta:
							# Primero se extraen los detalles anteriores:
							cursor.execute("SELECT details from INCIDENTS where id_csirt IN (SELECT id from CSIRT where id=%s)", (active_csirts[i][1],))
							details_t = cursor.fetchall()
							# Se preparan los nombres extendidos del personal afectado:
							cursor.execute("select surname,name from STAFF where user=%s", (user_name,)) # Se extrae el nombre completo del personal sustituido.
							old_name_t = cursor.fetchall()
							old_name = old_name_t[0][1] + ' ' + old_name_t[0][0]
							cursor.execute("select surname,name from STAFF where user=%s", (selected_user,)) # Se extrae el nombre completo del personal que lo sustituye.
							new_name_t = cursor.fetchall()
							new_name = new_name_t[0][1] + ' ' + new_name_t[0][0]
							# Se actualiza el campo detalles:
							details = details_t[0][0] + '\n' + time.strftime("%d/%m/%Y") + ': por baja del personal se sustituye el componente del Equipo de Respuesta ' +\
							old_name + ' por ' + new_name + '.'
							cursor.execute("UPDATE INCIDENTS SET details=%s where id_csirt=%s", (details,active_csirts[i][1]))
							mariadb_connection.commit()		# Se hacen efectivos los cambios en la BBDD.
							
							# Se actualizan los datos de la tabla CSIRT:
							[table_and_edit_CSIRT,team_list_index,team_list_csirts,user_list] = get_csirt_and_edit(cursor)
								
						i += 1
				
					
			
			staff_updated = 1		# Por �ltimo, se informa mediante el flag que la situaci�n se actualiz� correctamente,
			go_tab = 'pestana4'		# y se configura el interfaz web para continuar en la pesta�a de Gesti�n de Personal.		
						
			# Al haber aplicado cambios, se hace necesario actualizar los datos:
			table_STAFF = get_staff(cursor)
			[table_and_edit_CSIRT,team_list_index,team_list_csirts,user_list] = get_csirt_and_edit(cursor)	# Se obtienen los datos para la gesti�n de la tabla CSIRT.

		elif form_id.find('stats') > -1:				# Procesado de la selecci�n de estad�siticas y gr�ficas.
		
			num_elements = 0
			
			option = request.form.get('option')			# Se lee la opci�n elegida por el usuario.
			lapse = request.form.get('lapse')			# Selecci�n del intervalo temporal: anual, mensual o por intervalo.
			graph_type = request.form.get('graph_type')	# Selecci�n del tipo de gr�fica.
			
			if graph_type == '0':
				graph_type = 'bar'
			elif graph_type == '1':
				graph_type = 'horizontalBar'
			elif graph_type == '2':
				graph_type = 'line'
				
			if option != '0':
				huge_data = '1'
			
			year = ''
			start_date = ''
			stop_date = ''
			
			if lapse == 'monthly':
				year = request.form.get('year')
			
			if lapse == 'custom':						# Por intervalo => se necesita recoger las fechas de inicio y de fin.
				start_date = request.form.get('start_date')
				stop_date = request.form.get('stop_date')
				huge_data = '1'
			
			if option != '5' and option != '9':
				[graph, data, num_elements, stats, label, labels] = get_stats(option,cursor,lapse,year,start_date,stop_date)
			elif option == '9':
				[graph, data_set1, data_set2, stats, label, labels]= get_stats_originator(cursor)
			else:
				[graph, data_set1, data_set2, data_set3, data_set4, stats, label, labels] = get_stats_severity(cursor)
			
			# Se evitan problema de visualizaci�n en el caso de que haya gran cantidad de datos a mostrar:
			if num_elements > MAX_VIEW and graph_type == 'horizontalBar' and option != '7':
				graph_type	= 'line'	# Permite visualizar gran cantidad de datos sin distorsionar las etiquetas de los ejes.
				
			if option == '7' or option == '8':		# Con esta configuraci�n se visualizan los datos completos.
				graph_type = 'horizontalBar'
			
			show_graph = '1'
			
			go_tab = 'pestana5'		# Se indica que se muestre la pesta�a que contiene el apartado de An�lisis.		
			
		elif form_id.find('knowledge_type') > -1:		# Procesado de la selecci�n por tipo de incidencia.
		
			knowledge = get_knowledge_type(cursor,request.form.get('type'))	# Se obtiene la nueva tabla de Conocimiento maquetada HTML.
			
			go_tab = 'pestana6'							# Se selecciona la pesta�a correspondiente.
			
		# elif form_id.find('knowledge_notified') > -1:	# Procesado de la selecci�n de incidencias notificadas.
		
			# session['id_incid'] = request.form.get('id_incid')		# Se almacena en el espacio de variables de la sesi�n => accesible desde siguientes peticiones POST.
			
			# try:	# Se registra el ID de la incidencia seleccionada por el usuario:
				# file = open (SCRIPT_PATH+'/current_id_incid.dat','w')
			# except IOError:
				# print 'Archivo '+SCRIPT_PATH+'/current_id_incid.dat no iniciado!'
			# else:	
				# file.write(session['id_incid'])
				# file.close()
			
			# return redirect(url_for('manage_incident'))		# Se pasa al interfaz de gesti�n de incidencias.
			
		elif form_id.find('launch_query') > -1:	# Procesado de la consulta compleja de incidencias.
					
			if 'new_incident' in str(request.form):
			
				js_code_init = get_init_content('new_incident','','')
				
				message = ''
				error = 0				# Variable de control para la validaci�n de los datos de entrada a trav�s del interfaz web.

				done = 0				# Flag para determinar si se ha completado con �xito el alta de una nueva incidencia.
				new_incident_ok = ''	# Recoger� el mensaje a mostrar al registrarse el alta de la nueva incidencia de manera correcta.

				cursor.execute("SELECT MAX(INCIDENTS.id),MAX(CSIRT.id) from INCIDENTS,CSIRT")	# Se realiza la consulta de la cadena formateada. OK.
				result_ids = cursor.fetchall()
				
				# Se tiene en cuenta el cambio de a�o:
				current_year = time.strftime("%y")
				
				id_incid = 0
				id_csirt = 0
				if str(current_year) == str(result_ids[0][0])[2:4]:
					id_incid = result_ids[0][0]+1
					id_csirt = result_ids[0][1]+1
				else:
					id_incid = int(str(result_ids[0][0])[0:4])*10000+10001
					id_csirt = int(str(result_ids[0][1])[0:4])*100+101

				new_incident_content = get_new_incident_content(id_incid,id_csirt)
				
				return render_template(app.config['DEFAULT_TPL']+'/new_incident.html',
										current_user = session['current_user'],
										js_code_init = js_code_init,
										new_incident_content = new_incident_content,
										message = message,
										table_and_edit_CSIRT = table_and_edit_CSIRT,
										ens = ens_unescape,
										table_STAFF = table_STAFF,
										edit_STAFF = edit_STAFF,
										stats_option = stats_option,
										knowledge = knowledge,
										info = info,
										id_incid = id_incid,
										id_csirt = id_csirt,
										done = done,
										new_incident_ok = new_incident_ok,
										conf = app.config)	
			
			else:
		
				query_text = ''
				id_incid = ''
				start_date = ''
				stop_date = ''
				status = ''
				severity = ''
				dimensions = ''
				originator = ''
				accountable = ''
				type = ''
				area = ''
				csirt = ''
				falses = ''
				error = 0
			
				# Se prepara la cadena de consulta que lanzar� contra el gestor de la BBDD.
				# Para ello se hace necesario comprobar todos los criterios seleccionados por el usuario:
				
				id_incid = request.form.get('id_incid')
				start_date = request.form.get('start_date')
				stop_date = request.form.get('stop_date')
				status = request.form.get('status')
				severity = request.form.get('severity')
				dimensions = request.form.get('dimensions')
				originator = request.form.get('originator')
				accountable = request.form.get('accountable')
				type = request.form.get('type')
				area = request.form.get('area')
				csirt = request.form.get('csirt')
				id_csirt = request.form.get('id_csirt')
				falses = str(request.form.get('falses'))
				
				# En primer lugar, se validan los datos de entrada:
				if id_incid:
					error = data_int_valid(id_incid)
				if start_date and stop_date:
					error += dates_compact_valid(start_date,stop_date)
					
				if originator:
					error += user_valid(originator)
				if accountable:
					error += user_valid(accountable)
					
				if type:
					error += type_valid(type)
				
				if error != 0:
					message = Markup(u'swal("Datos introducidos no v�lidos!", "\(B�squeda de Incidencias\)", "error", {button: "Aceptar",});')
				else:
					false_p = false_n = 'N'			
					falses = str(request.form.get('falses'))
					if falses.find('false_p') > -1:
						false_p = 'S'
					else:
						false_p = 'N'
					if falses.find('false_n') > -1:
						false_n = 'S'
					else:
						false_n = 'N'

					first_field = 's'	# Permite controlar la generaci�n de la cadena.
						
					if id_incid:
						query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE id=%s" % (id_incid)
						first_field = 'n'

					# La b�squeda por fecha se considerar� respecto a la fecha de detecci�n de las incidencias:
					if start_date and stop_date:
						start_date = start_date.replace("-","") + '0000'
						start_date_int = int(start_date[4:8] + start_date[2:4] + start_date[2:4])	# Se formatea la fecha para poder comparar.
						stop_date = stop_date.replace("-","") + '2359'
						stop_date_int = int(stop_date[4:8] + stop_date[2:4] + stop_date[2:4])		# Se formatea la fecha para poder comparar.

						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE detect_date>%s and detect_date<%s" % (start_date,stop_date)
							first_field = 'n'
						else:
							query_text += " and detect_date>=%s and detect_date<=%s" % (start_date,stop_date)

					if status:
						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE status='%s'" % (status)
							first_field = 'n'
						else:
							query_text += " and status='%s'" % (status)

					if severity:
						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE severity='%s'" % (severity)
							first_field = 'n'
						else:
							query_text += " and severity='%s'" % (severity)

					C = request.form.getlist('Conf')
					I = request.form.getlist('Inte')
					Av = request.form.getlist('Avai')
					Au = request.form.getlist('Auth')
					T = request.form.getlist('Trac')
					dimensions = ''
					if len(C) > 0:
						dimensions += 'C'
					if len(I) > 0:
						dimensions += 'I'
					if len(Av) > 0:
						dimensions += 'D'
					if len(Au) > 0:
						dimensions += 'A'
					if len(T) > 0:
						dimensions += 'T'
						
					if dimensions:
						# Lo primero, es conformar la cadena de la consulta para que se busque cualquier opci�n seleccionada:
						
						operator = request.form.get('operator')
						
						compound = "dimensions LIKE '%%%s%%'" % (dimensions[0])
					
						if len(dimensions) > 1:			
							for i in range(1,len(dimensions)):
										compound += " %s dimensions LIKE '%%%s%%'" % (operator,dimensions[i])
					
						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE %s" % (compound)
							first_field = 'n'
						else:
							query_text += " and %s" % (compound)
							
					if originator:
						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE originator='%s'" % (originator)
							first_field = 'n'
						else:
							query_text += " and originator='%s'" % (originator)

					if accountable:
						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE accountable='%s'" % (accountable)
							first_field = 'n'
						else:
							query_text += " and accountable='%s'" % (accountable)

					if type:
						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE type='%s'" % (type)
							first_field = 'n'
						else:
							query_text += " and type='%s'" % (type)

					if area:
						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE area='%s'" % (area)
							first_field = 'n'
						else:
							query_text += " and area='%s'" % (area)

					if csirt:
						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE csirt='%s'" % (csirt)
							first_field = 'n'
						else:
							query_text += " and csirt='%s'" % (csirt)
							
					if id_csirt:
						if first_field == 's':
							query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE id_csirt=%s" % (id_csirt)
							first_field = 'n'
						else:
							query_text += " and id_csirt=%s" % (id_csirt)

					if falses:		
						if falses.find('false_p') > -1:
							false_p = 'S'
						else:
							false_p = 'N'

						if falses.find('false_n') > -1:
							false_n = 'S'
						else:
							false_n = 'N'

						if first_field == 's':
							if false_p == 'S':
								query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE false_p='S'"
							elif false_n == 'S':
								query_text = "SELECT SQL_NO_CACHE * FROM INCIDENTS WHERE false_n='S'"
							first_field = 'n'
						else:
							if false_p == 'S':
								query_text += " and false_p='S'"
							elif false_n == 'S':
								query_text += " and false_n='S'"
												
					if query_text:	# En el caso de que haya datos seleccionados, se lanza la consulta. En caso contrario, se sigue en el interfaz actual.
					
						cursor.execute(query_text)			# Se realiza la consulta de la cadena formateada.
						result = cursor.fetchall()			# Se extrae el resultado de la consulta.
						
						session['tab_1_content'] = get_table_incidents(result)	# Se genera el interfaz web para la muestra de la tabla con los resultados de la b�squeda.
						# Muestra el resultado de la b�squeda indicada por el usuario en forma de tabla, y espera a que el usuario seleccione una incidencia concreta
						# para mostrar sus datos de manera detallada
						
		elif form_id.find('manage_incident') > -1 or form_id.find('knowledge_notified') > -1:		# Muestra detallada de los datos de la incidencia.
		
			session['id_incid'] = request.form.get('id_incid')		# Se captura la identificaci�n de la incidencia seleccionada.
						
			warning_message = ''	# Para mostrar mensajes de aviso en caso de datos incorrectos.
			closing_date = ''		# Recoger� la fecha de cierre de la incidencia, si est� cerrada.
			
			[originator,type,description,area,accountable,csirt,id_csirt,detect_date,notify_date,severity,dimensions,status,reports,details,pm_info,pm_extended,false_p,false_n] = extract_incident_data(cursor,session['id_incid'])
			
			if status == 'C':
				closing_date = time.strftime("%d/%m/%Y")
			
			if reports.find('==') > -1:		# En el caso de que haya informes, se procesan para la visualizaci�n:
			
				# Formateo para la ventana de Informes (solo para visualizaci�n!):
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
					
					reports_t += str(report_name) + ':\n' + str(item) + '\n\n'
				
				reports_t = reports_t.replace(" ","")	# Se eliminan los espacios en blanco.
				
				reports_view = Markup(reports_t)		# Se formatea la cadena para visualizaci�n en el interfaz web.
				
			else:
				reports_view = ''

			cursor.execute("SELECT name,surname FROM STAFF")		# Se realiza la consulta de la incidencia requerida.
			entry = cursor.fetchall()								# Se extraen los datos del usuario.

			names_list = []
			
			for i in range(len(entry)):
				names_list.append(entry[i][0] + ' ' + entry[i][1])
				
			js_code_init = get_init_content('manage_incident',csirt,status)
				
			return render_template(app.config['DEFAULT_TPL']+'/manage_incident.html',
									current_user = session['current_user'],
									js_code_init = js_code_init,
									ens = ens_unescape,
									table_STAFF = table_STAFF,
									edit_STAFF = edit_STAFF,
									table_and_edit_CSIRT = table_and_edit_CSIRT,
									stats_option = stats_option,
									knowledge = knowledge,
									info = info,
									team_list_index = team_list_index,
									id_incid = session['id_incid'],
									originator = originator,
									type = type,
									description = description,
									area = area,
									accountable = accountable,
									csirt = csirt,
									id_csirt = id_csirt,
									detect_date = detect_date,
									notify_date = notify_date,
									severity = severity,
									dimensions = dimensions,
									status = status,
									reports = reports_view,
									details = details,
									pm_extended = pm_extended,
									false_p = false_p,
									false_n = false_n,
									closing_date = closing_date,
									names_list = names_list,
									len_names_list = len(names_list),
									warning_message = warning_message,
									conf = app.config)						
								
		elif form_id.find('update_incident') > -1:			# Actualizaci�n de los datos de la incidencia modificados por el usuario.
		
			[accountable,status,csirt,severity,dimensions,details,reports,pm_info,false_p,false_n] = extract_incident_partial_data(cursor,session['id_incid'])
			
			if status != 'C':			# Se impide modificar una incidencia ya cerrada!

				changed = 0				# Flag que recoger� si ha habido cambios y debe actualizarse la BBDD, o no.
				incident_updated = 0	# Flag para el aviso de actualizaci�n al usuario.
				
				new_details = request.form.get('details')	# Se leen en primer lugar los detalles en caso de que necesite insertarse alguna nota.
			
				# En primer lugar, se recuperan los datos actualizados indicados por el usuario en el interfaz web:
				new_accountable = request.form.get('accountable')
				if new_accountable != accountable:
					accountable_old = accountable
					new_accountable_t = new_accountable
					new_accountable = clean_username_joined(new_accountable)
					name_surnames = new_accountable.split(' ')
					if len(name_surnames) == 3:
						username = name_surnames[0][0:3] + name_surnames[1][0:3] + name_surnames[2][0:3]	# Nombre simple + 2 apellidos.
					else:
						username = name_surnames[0][0:3] + name_surnames[2][0:3] + name_surnames[3][0:3]	# Nombre compuesto + 2 apellidos.
		
					cursor.execute("UPDATE INCIDENTS SET accountable=%s WHERE id=%s", (username,session['id_incid']))	# Finalmente, se a�ade a la BBDD.
					accountable = username	# Se actualiza la variable que retiene el nombre de usuario del responsable.
					changed += 1					# Se actualiza el flag indicando que ha habido cambios.
					new_details += '\n' + time.strftime("%d/%m/%Y") + ': se cambia el responsable de la incidencia ' + accountable_old + ' por ' + new_accountable_t + '.'
					# Por �ltimo, se notifica al afectado el nuevo nombramiento:
					subject = 'ATENCION: ha sido seleccionado como responsable de una incidencia!'
					text = 'Se ruega atienda la incidencia ' + str(session['id_incid']) + '.\n\nGracias y un cordial saludo.'
					email_notify(email_CISO,subject,text)
				
				new_severity = ''
				if csirt != 'S':
					new_severity = request.form.get('severity')
				else:
					new_severity = 'C'
				
				C = request.form.getlist('Conf')
				I = request.form.getlist('Inte')
				Av = request.form.getlist('Avai')
				Au = request.form.getlist('Auth')
				T = request.form.getlist('Trac')
				new_dimensions = ''
				if len(C) > 0:	# Quiere decir que se ha marcado la opci�n.
					new_dimensions += 'C'
				if len(I) > 0:
					new_dimensions += 'I'
				if len(Av) > 0:
					new_dimensions += 'D'
				if len(Au) > 0:
					new_dimensions += 'A'
				if len(T) > 0:
					new_dimensions += 'T'
		
				if new_dimensions == '':
					warning_message = Markup(u'swal("Debe seleccionar, al menos, una dimensi�n de seguridad!", "\(Gesti�n de Incidencias\)", "warning", {button: "Aceptar",});')
				else:
					new_status = request.form.get('status')
					
					if new_status.find('A') > -1:
						new_status = 'A'
					elif new_status.find('U') > -1:
						new_status = 'U'
					else:
						new_status = 'C'

					new_false_p = new_false_n = 'N'
						
					falses = str(request.form.get('falses'))
					
					if not falses:
						new_false_p = 'N'
						new_false_n = 'N'
					else:
						if falses.find('false_p') > -1:
							new_false_p = 'S'
						else:
							new_false_p = 'N'

						if falses.find('false_n') > -1:
							new_false_n = 'S'
						else:
							new_false_n = 'N'

					pm_codes = {}
					pm_set = {}
					notes = {}
					
					pm_codes = request.form.getlist('pm_codes[]')
					pm_set = request.form.getlist('set[]')
					notes = request.form.getlist('notes[]')
					
					new_pm_info = ''
					
					for i in range(len(pm_set)):
						new_pm_info += pm_codes[i] + "$$" + pm_set[i][0] + notes[i] + "=="
						
					if new_pm_info.decode('unicode_escape') != pm_info[1:len(pm_info)].decode('unicode_escape'):
						cursor.execute("UPDATE INCIDENTS SET pm_info=%s WHERE id=%s", (new_pm_info,session['id_incid']))	# Finalmente, se a�ade a la BBDD.
						pm_info = new_pm_info
						changed += 1
					
					lift_it_up = str(request.form.getlist('lift_it_up'))	# Se comprueba si el usuario ha seleccionado escalar la incidencia.
					
					if lift_it_up.find('lift_it_up') > -1:					# Seleccionado!
					
						# Se notifica el escalado de la incidencia:
						subject = 'ATENCION: se ha escalado una incidencia!'
						text = 'Se ruega atiendan la incidencia ' + str(session['id_incid']) + '.\n\nGracias y un cordial saludo.'
						email_notify(email_CISO,subject,text)
						
						# Y se inserta la situaci�n en el campo de detalles:
						new_details += '\n' + time.strftime("%d/%m/%Y") + ': se escala la incidencia.'
					
					new_doc = request.form.get('new_doc')

					if new_doc.find('/') > -1:				# En el caso de que se haya indicado un nuevo documento, se a�ade a los existentes.
						reports += new_doc + '=='			# Se a�ade la nueva cadena a insertar.
						reports = reports.replace(" ","")	# Se eliminan los espacios en blanco.
						cursor.execute("UPDATE INCIDENTS SET reports=%s WHERE id=%s", (reports,session['id_incid']))	# Finalmente, se a�ade a la BBDD.
						changed += 1
					
					# Se actualizan los campos en la BBDD con los nuevos valores.
					# Hay que tener la precauci�n de solo actualizar los valores que hayan cambiado!:	
					
					# Se recuerda los niveles de severidad: [B]aja, [M]edia, [A]lta y [C]r�tica.
					if csirt != 'S' and new_severity != severity:
						cursor.execute("UPDATE INCIDENTS SET severity=%s WHERE id=%s", (new_severity,session['id_incid']))
						severity = new_severity
						changed += 1
						
					if new_dimensions != dimensions:
						cursor.execute("UPDATE INCIDENTS SET dimensions=%s WHERE id=%s", (new_dimensions,session['id_incid']))
						dimensions = new_dimensions
						changed += 1
						
					if new_status != status:
						cursor.execute("UPDATE INCIDENTS SET status=%s WHERE id=%s", (new_status,session['id_incid']))
						if new_status == 'C':
							new_details += '\nFecha de cierre: ' + time.strftime("%d/%m/%Y") + '.'
							cursor.execute("UPDATE INCIDENTS SET closing_date=%s WHERE id=%s", (time.strftime("%Y%m%d"),session['id_incid']))
						status = new_status
						changed += 1
					
					if new_details != details:
						cursor.execute("UPDATE INCIDENTS SET details=%s WHERE id=%s", (new_details,session['id_incid']))
						details = new_details
						changed += 1
							
					if new_false_p != false_p:
						cursor.execute("UPDATE INCIDENTS SET false_p=%s WHERE id=%s", (new_false_p,session['id_incid']))
						false_p = new_false_p
						changed += 1
						
					if new_false_n != false_n:
						cursor.execute("UPDATE INCIDENTS SET false_n=%s WHERE id=%s", (new_false_n,session['id_incid']))
						false_n = new_false_n
						changed += 1
						
					if changed > 0:							# Si ha habido cambios:
						mariadb_connection.commit()			# Se hacen efectivos los cambios en la BBDD.
						incident_updated = 1				# Se informa al usuario que ha habido cambios y se han registrado correctamente!

		
		elif form_id.find('set_new_incident') > -1:			# Registro del alta de nueva incidencia.

			js_code_init = get_init_content('new_incident','','')
	
			message = ''
			error = 0				# Variable de control para la validaci�n de los datos de entrada a trav�s del interfaz web.

			done = 0				# Flag para determinar si se ha completado con �xito el alta de una nueva incidencia.
			new_incident_ok = ''	# Recoger� el mensaje a mostrar al registrarse el alta de la nueva incidencia de manera correcta.
	
			cursor.execute("SELECT MAX(INCIDENTS.id),MAX(CSIRT.id) from INCIDENTS,CSIRT")	# Se realiza la consulta de la cadena formateada. OK.
			result_ids = cursor.fetchall()
			
			# Se tiene en cuenta el cambio de a�o:
			current_year = time.strftime("%y")
			
			id_incid = 0
			id_csirt = 0
			if str(current_year) == str(result_ids[0][0])[2:4]:
				id_incid = result_ids[0][0]+1
				id_csirt = result_ids[0][1]+1
			else:
				id_incid = int(str(result_ids[0][0])[0:4])*10000+10001
				id_csirt = int(str(result_ids[0][1])[0:4])*100+101
		
			status = request.form.get('status')
			severity = request.form.get('severity')
			originator = current_user
			accountable = request.form.get('accountable')
			type = request.form.get('type')
			area = request.form.get('area')
			csirt = request.form.get('csirt')
			if not csirt:	# Si est� deshabilitado desde el interfaz, no se lee nada!
				csirt = 'N'	

			C = request.form.getlist('Conf')
			I = request.form.getlist('Inte')
			Av = request.form.getlist('Avai')
			Au = request.form.getlist('Auth')
			T = request.form.getlist('Trac')
			dimensions = ''
			if len(C) > 0:
				dimensions += 'C'
			if len(I) > 0:
				dimensions += 'I'
			if len(Av) > 0:
				dimensions += 'D'
			if len(Au) > 0:
				dimensions += 'A'
			if len(T) > 0:
				dimensions += 'T'
				
			if not status or not severity or not dimensions or (not accountable and csirt == 'N') or not type or not area:
				nok = u' Rellene los campos obligatorios, por favor! '
				return render_template(app.config['DEFAULT_TPL']+'/nok.html',
								current_user = session['current_user'],
								ens = ens_unescape,
								table_STAFF = table_STAFF,
								edit_STAFF = edit_STAFF,
								nok = nok,
								conf = app.config)

			if csirt == 'S' and severity != 'C':
				nok = u' No se puede generar un equipo de respuesta para una incidencia de severidad inferior a Cr�tica! '
				return render_template(app.config['DEFAULT_TPL']+'/nok.html',
								current_user = session['current_user'],
								ens = ens_unescape,
								table_STAFF = table_STAFF,
								edit_STAFF = edit_STAFF,
								nok = nok,
								conf = app.config)	
		
			error += user_valid(accountable)
			error += type_valid(type)
			
			if error != 0:
				message = Markup(u'swal("Datos introducidos no v�lidos!", "\(Gesti�n de Incidencias\)", "error", {button: "Aceptar",});')
				
			else:
		
				current_date = time.strftime("%d/%m/%Y %H:%M")
				
				detect_date = time.strftime("%Y%m%d%H%M")

				notify_date = ''	# El valor real se insertar� en el campo notify_date de la incidencia desde notify.py cuando realmente se produzca la notificaci�n.
									
				if csirt == 'S':	# Se crea el nuevo equipo de respuesta:	
					cursor.execute("SELECT user FROM STAFF WHERE status='A'")			# Se consulta el personal en activo.
					active_staff = cursor.fetchall()									# Se extraen los nombres de usuario del personal en activo.
					active_staff_indexes = random.sample(range(0,len(active_staff)),2)	# Se genera una lista aleatoria con 2 nombres de usuario entre el personal en activo.
					team = accountable + str(active_staff[active_staff_indexes[0]]) + str(active_staff[active_staff_indexes[1]])
					# En el caso de conformar un equipo de respuesta, el responsable de la incidencia siempre es el que aparece primero.
					team = team.replace("(u'","")
					team = team.replace("',)","")
					team_date = current_date
					query_text = "INSERT INTO CSIRT (id, id_incid, team, team_date) VALUES (%s,%s,%s,%s)"
					val = (id_csirt,id_incid,team,team_date)
					cursor.execute(query_text,val)		# Se ejecuta la consulta para insertar el nuevo Equipo de Respuesta reci�n conformado.
					mariadb_connection.commit()			# Se hacen efectivos los cambios en la BBDD.
					# Por �ltimo, se notifica a los integrantes del equipo:
					# No se hace necesario ya -> notify.py  lo recoge de manera autom�tica y lo notifica!
				else:
					id_csirt = 0
					
				# Se compone el campo pm_info en el caso de que se haya clasificado la incidencia mediante el campo type:
				pm_info_t = ''
				cursor.execute("SELECT pm_list FROM ENS WHERE id=%s", (type,)) 	# Se consulta la lista de medidas de protecci�n aplicables seg�n el ENS.
				pm_list = cursor.fetchall()										# Se extraen las medidas de protecci�n aplicables.			
				
				# En primer lugar, se extrae y se formatea la descripci�n para mostrarla correctamente en el interfaz web:
				pat = re.compile('<h3>.*</h3>')		
				description = str(pat.findall(str(pm_list))[0])
				description = description.replace("<h3>","")
				description = description.replace("</h3>","")
				description = description.replace("u\"[","")
				description = description.replace("]\"","")
				description = description.decode('unicode_escape')
				
				# A continuaci�n se extraen las numeraciones de las medidas de protecci�n aplicables y se compone el campo pm_info:
				pat = re.compile('\d{3}\. ')

				pm_list_id = pat.findall(str(pm_list))
				
				for p in range(len(pm_list_id)):
					pm_info_t += pm_list_id[p].replace(". ","") + '$$' + 'N' + '=='		# Se a�aden inicialmente el flag de No aplicado, y los separadores correspondientes.
				
				type = int(type)	# Para respetar el formato de los datos de cara a insertarlos en la BBDD.
				
				pm_info = pm_info_t.decode('unicode_escape')	# Se formatea para permitir albergar caracteres especiales como tildes o � de manera legible.
				
				query_text = "INSERT INTO INCIDENTS (id, originator, type, description, area, accountable, csirt, id_csirt, detect_date, notify_date, severity, dimensions, status, reports, details, pm_info, false_p, false_n) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				val = (id_incid,session['current_user'],type,description,area,accountable,csirt,id_csirt,detect_date,notify_date,severity,dimensions,status,"","",pm_info,"N","N")
				cursor.execute(query_text,val)
					
				mariadb_connection.commit()		# Se hacen efectivos los cambios en la BBDD.
				
				if csirt == 'S':	# Se actualizan los datos para la visualizaci�n de los Equipos de Respuesta:
					[table_and_edit_CSIRT,team_list_index,team_list_csirts,user_list] = get_csirt_and_edit(cursor)
					id_csirt += 1
				
				new_incident_ok = Markup(u'swal("Nueva incidencia registrada correctamente!", "\(Gesti�n de Incidencias\)", "success", {button: "Aceptar",});')
				
				done = 1		# Flag indicando que se ha completado el alta de la nueva incidencia de manera correcta.
					
				id_incid += 1	# Se deja preparado en caso de que el gestor desee seguir registrando nuevas incidencias.
				
				new_incident_content = get_new_incident_content(id_incid,id_csirt)	# Se actualiza el interfaz web de alta de incidencias.
			
			return render_template(app.config['DEFAULT_TPL']+'/new_incident.html',
									current_user = session['current_user'],
									js_code_init = js_code_init,
									new_incident_content = new_incident_content,
									message = message,
									table_and_edit_CSIRT = table_and_edit_CSIRT,
									ens = ens_unescape,
									table_STAFF = table_STAFF,
									edit_STAFF = edit_STAFF,
									stats_option = stats_option,
									knowledge = knowledge,
									info = info,
									id_incid = id_incid,
									id_csirt = id_csirt,
									done = done,
									new_incident_ok = new_incident_ok,
									conf = app.config)	
			
	if csirt_updated == 1:
		csirt_update_ok = Markup(u'swal("Equipo actualizado correctamente!", "\(Gesti�n de Equipos de Respuesta\)", "success", {button: "Aceptar",});')
		csirt_updated = 0

	if staff_updated == 1:
		staff_update_ok = Markup(u'swal("Situaci�n actualizada correctamente!", "\(Gesti�n de Personal\)", "success", {button: "Aceptar",});')
		staff_updated = 0

	if new_user_added == 1:
		new_user_ok = Markup(u'swal("Nuevo usuario incorporado correctamente!", "\(Gesti�n de Personal\)", "success", {button: "Aceptar",});')
		new_user_added = 0
		
	if incident_updated == 1:	
		message = Markup(u'swal("Incidencia actualizada correctamente!", "\(Gesti�n de Incidencias\)", "success", {button: "Aceptar",});')
		incident_updated = 0
	
	return render_template(app.config['DEFAULT_TPL']+'/index.html',
							current_user = session['current_user'],
							go_tab = go_tab,
							tab_1_content = session['tab_1_content'],
							js_code_init = js_code_init,
							new_incident_content = new_incident_content,
							id_incid = session['id_incid'],
							id_csirt = id_csirt,
							done = done,
							new_incident_ok = new_incident_ok,
							stats_option = stats_option,
							show_graph = show_graph,
							option = option,
							huge_data = huge_data,
							data = data,
							data_set1 =  data_set1,
							data_set2 =  data_set2,
							data_set3 =  data_set3,
							data_set4 =  data_set4,
							stats = stats,
							graph = graph,
							graph_type = graph_type,
							label = label,
							labels = labels,
							num_elements = num_elements,
							knowledge = knowledge,
							ens = ens_unescape,
							table_STAFF = table_STAFF,
							edit_STAFF = edit_STAFF,
							table_and_edit_CSIRT = table_and_edit_CSIRT,
							info = info,
							team_list_index = team_list_index,
							message = message,
							csirt_update_ok = csirt_update_ok,
							staff_update_ok = staff_update_ok,
							new_user_ok = new_user_ok,
							conf = app.config)


		###########################################
		# FIN CONTROLADORES DE LA APP WEB Soteria #
		###########################################


		################################################
		# MAIN: PUESTA EN MARCHA DE LA APP WEB Soteria #
		################################################
if __name__ == '__main__':
	# Esta configuraci�n solo es relevante en el caso de emplear el servidor http interno de Flask:
	
    # Se inicia la aplicacion en la IP actual que tenga la instancia EC2 de AWS y el puerto HTTP (0.0.0.0 por defecto para admitir cualquier IP):
	app.run(debug=True,host='0.0.0.0',port=80)
	# Finalmente se emplea el Servidor Web Apache2, por lo que no se lanza el servidor interno de Flask!
	# Adem�s, se implementa HTTPS, por lo que el puerto real de acceso finalmente es el 443, pero eso se
	# gestiona desde los ficheros de configuraci�n de Apache: /etc/apache2/sites-available
    

##################
# FIN Soteria.py #
##################
