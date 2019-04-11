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
#   MEDIANTE ESTE SCRIPT PYTHON SE GENERA EL CÓDIGO .SQL    # 
#   QUE SE UTILIZARÁ PARA RELLENAR LA BBDD CON DATOS DE     # 
#   PRUEBA INICIALES PARA INSERTAR DE MANERA AUTOMÁTICA.    #
#############################################################

#############################################################
#				MODELO DE DATOS A GENERAR 					#
#############################################################
#    EN PRIMER LUGAR SE GENERAN DATOS PARA LA TABLA ENS     #
#############################################################
# EN SEGUNDO LUGAR SE GENERAN DATOS PARA LA TABLA INCIDENTS #
#############################################################
#############################################################
# 	  POR ÚLTIMO, SE GENERAN DATOS PARA LA TABLA CSIRT 		#
#############################################################


import re		# Librería de funciones para manejo de Expresiones Regulares.
import random	# Librería para generación de números aleatorios.
import time		# Funciones de manejo de la fecha y hora del sistema.


			# GENERACIÓN DE LA TABLA ENS:

# La tabla ENS contiene los siguientes campos (se incluye algunos ejemplos de inserción de datos de prueba):
##INSERT INTO ENS
## (id, pm_list) 
## values
## (453, '4531 Bla bla bla1.4532Bla bla bla2.4533Bla bla bla3.'),
## (431, '4311 Bla bla bla1.4312Bla bla bla2.4313Bla bla bla3.'),
## (552, '5521 Bla bla bla1.5522Bla bla bla2.5523Bla bla bla3.'),
## (326, '3261 Bla bla bla1.3262Bla bla bla2.3263Bla bla bla3.'),
## (448, '4481 Bla bla bla1.4482Bla bla bla2.4483Bla bla bla3.');

# En este caso no se rellenará la tabla con datos de prueba, sino que albergará realmente el contenido de las medidas de protección del ENS,
# recogidas en la guía CCN-STIC 804, de Implantación del ENS, en su versión actual en vigor de junio 2017.

# El formato será el definido en el diseño, a saber:
# “ID+Descripción OBJETIVO 5.X.Y”
# “ID medida de protección XYZ#n. Descripción medida de protección XYZ#n”
# “ID medida de protección XYZ#(n+1). Descripción medida de protección XYZ#(n+1)”
# …

# La codificación, tal como se expone en la memoria de este TFM, incluye la maquetación HTML básica para facilitar su visionado.

# Para facilitar el procesado programático, se incluirá el contenido de cada objetivo en una sola línea de código.


# A continuación, se definen los objetivos de seguridad:

obj_511 = '<h3>5.1.1 [MP.IF.1] ÁREAS SEPARADAS Y CON CONTROL DE ACCESO</h3>328. Se deben delimitar las áreas de trabajo y de equipos, disponiendo de un inventario actualizado que para cada área determine su función y las personas responsables de su seguridad y de autorizar el acceso.<br/>329. Cuando el acceso se controle por medio de llaves o dispositivos equivalentes, se dispondrá de un inventario de llaves junto con un registro de quién las toma, quién las devuelve y en manos de quién hay copias en cada momento. En caso de sustracción o pérdida, se procederá al cambio con diligencia para evitar el riesgo.<br/>330. Se dispondrá de medios que eviten el acceso por puntos diferentes al que dispone del control de acceso. Se evitarán ventanas accesibles y puertas desprotegidas. En particular hay que vigilar puertas de evacuación de emergencia para que no permitan la entrada ni en condiciones normales ni cuando se utilizan como vía de evacuación (por ejemplo, cámaras de vigilancia, cerraduras electrónicas que registran cada acceso, etc.).<br/>331. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.1 - Áreas seguraso</li><li>11.2.1 - Emplazamiento y protección de equipos</li></ul></ul>332. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[PE-18] Location of Information System Components</li><li>[PE-3] Physical Access Control</li><li>[PE-4] Access Control for Transmission Medium</li><li>[PE-5] Access Control for Output Devices</li></ul>'

obj_512 = '<h3>5.1.2 [MP.IF.2] IDENTIFICACIÓN DE LAS PERSONAS</h3>333. Para las áreas de acceso restringido, se debe mantener una relación de personas autorizadas y un sistema de control de acceso que verifique la identidad y la autorización y deje registro de todos los accesos de personas (por ejemplo, persona o identificador corporativo, fecha y hora de cada entrada y salida).<br/><br/>334. Se recomienda que exista segregación de funciones en el proceso de gestión de acceso a los locales con equipamiento (solicitud y autorización). Dichas funciones deben recaer en al menos dos personas.<br/><br/>335. Debe realizarse periódicamente una revisión de las autorizaciones, identificando si continúa existiendo la necesidad de acceso que motivó la autorización.<br/><br/>336. ISO/IEC 27000 <ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>11.1.2 - Controles físicos de entrada</li></ul></ul>337. NIST SP 800-53 rev.4<ul style="list-style-type:square"><li>[PE-2] Physical Access Authorizations</li><li>[PE-6] Monitoring Physical Access</li><li>[PE-8] Visitor Access Records</li></ul>'

obj_513 = '<h3>5.1.3 [MP.IF.3] ACONDICIONAMIENTO DE LOS LOCALES</h3>338. Se debe disponer de unas instalaciones adecuadas para el eficaz desempeño del equipamiento que se instala en ellas.<br/><br/>339. Sin perjuicio de lo dispuesto en otras medidas más específicas, los locales deben:<ul style="list-style-type:square"><li> garantizar que la temperatura se encuentra en el margen especificado por los fabricantes de los equipos</li><li>garantizar que la humedad se encuentra dentro del margen especificado por los fabricantes de los equipos</li><li>se debe proteger el local frente a las amenazas identificadas en el análisis de riesgos, tanto de índole natural, como derivadas del entorno o con origen humano, accidental o deliberado (complementando [mp.if.1], [mp.if4], [mp.if.5], [mp.if.6] y [mp.if.7])</li><li>se debe evitar que el propio local sea una amenaza en sí mismo, o factor determinante de otras amenazas, como la existencia de material innecesario o inflamable en el local (papel, cajas, etc.) o que pueda ser causa de otros incidentes (elementos con agua, etc.)</li><li>el cableado debe estar:</li><ul style="list-style-type:circle"><li>etiquetado: se puede identificar cada cable físico y su correspondencia a los planos de la instalación</li><li>controlado: para identificar el cableado fuera de uso</li><li>protegido frente a accidentes: por ejemplo, para evitar que las personas tropiecen con los cables</li><li>protegido frente a accesos no autorizados: protegiendo armarios de distribución y canaletas</li></ul></ul>340. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.2.2 - Instalaciones de suministro</li><li>11.2.3 - Seguridad del cableado</li></ul></ul>341. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[PE-14] Temperature and Humidity Controls</li></ul>'

obj_514 = '<h3>5.1.4 [MP.IF.4] ENERGÍA ELÉCTRICA</h3>342. Se deben prever medidas para atajar un posible corte de suministro eléctrico y un correcto funcionamiento de las luces de emergencia.<br/><br/>343. Prevención de problemas de origen interno:<ul style="list-style-type:square"><li>dimensionado y protección del cableado de potencia</li><li>dimensionado y protección de los cuadros y armarios de potencia</li></ul>344. Reacción a problemas de origen externo:<ul style="list-style-type:square"><li>suministro alternativo: UPS, generadores, proveedor alternativo</li></ul>345. Se debe disponer de un plan de emergencia, de reacción y de recuperación de desastres.<br/><br/>346. Hay que disponer de una alimentación suficiente para apagar los equipos de forma ordenada. Normalmente, esto supone una alimentación local (SAI, o UPS por sus siglas en inglés) que garantice el suministro eléctrico durante los minutos necesarios para activar y concluir el procedimiento de apagado de emergencia, y grupos electrógenos en caso de ser necesario.<br/><br/>347. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.2.2 - Instalaciones de suministro</li></ul></ul>348. NIST SP 800-53 rev.4<ul style="list-style-type:square"><li>[PE-9] Power Equipment and Cabling</li><li>[PE-10] Emergency Shutoff</li><li>[PE-11] Emergency Power</li><li>[PE-12] Emergency Lighting</li>'

obj_515 = '<h3>5.1.5 [MP.IF.5] PROTECCIÓN FRENTE A INCENDIOS</h3>349. Se debe realizar un estudio del riesgo de incendios, tanto de origen natural como industrial:<ul style="list-style-type:square"><li>entorno natural proclive a incendios</li><li>entorno industrial que pudiera incendiarse</li><li>instalaciones propias con riesgo de incendio</li></ul>350. Si el fuego no se puede evitar, hay que desplegar medidas de prevención, monitorización y limitación del impacto<ul style="list-style-type:square"><li>disponer de carteles para evacuación</li><li>evitar el uso de materiales inflamables</li><li>aislamiento (cortafuegos, puertas ignífugas)</li><li>sistema de detección conectado a central de alarmas 24x7</li><li>medios de reacción: medios de extinción</li><li>plan de emergencia, de reacción y de recuperación de desastres</li></ul>351. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.1.4 - Protección contra las amenazas externas y de origen ambiental</li></ul></ul>352. NIST SP 800-53 rev.4<ul style="list-style-type:square"><li>[PE-13] Fire Protection</li></ul>353. Otras referencias:<ul style="list-style-type:square"><li>Planes de emergencia y evacuación contra incendios de locales y edificios. http://www.mtas.es/insht/FDN/FDN_011.htm</li></ul>'

obj_516 = '<h3>5.1.6 [MP.IF.6] PROTECCIÓN FRENTE A INUNDACIONES</h3>354. Se debe realizar un estudio del riesgo de inundaciones, tanto de origen natural como industrial: <ul style="list-style-type:square"><li>cercanía a ríos o corrientes de agua</li><li>canalizaciones de agua (tuberías) especialmente encima de los equipos</li></ul>355. Si el riesgo no se puede evitar, hay que desplegar medidas de prevención, monitorización y limitación del impacto<ul style="list-style-type:square"><li>aislamiento de humedades</li><li>canalización de desagüe con procedimientos regulares de limpieza</li><li>sistema de detección conectado a central de alarmas 24x7</li><li>plan de reacción y recuperación de desastres; en el caso de canalizaciones industriales, el plan de reacción puede incluir el cierre de llaves o válvulas que atajen el vertido</li></ul>356. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.1.4 - Protección contra las amenazas externas y de origen ambiental</li></ul></ul>357. NIST SP 800-53 rev.4<ul style="list-style-type:square"><li>[PE-15] Water Damage Protection</li></ul>'

obj_517 = '<h3>5.1.7 [MP.IF.7] REGISTRO DE ENTRADA Y SALIDA DE EQUIPAMIENTO</h3>358. Se debe llevar un registro pormenorizado de toda entrada y salida de equipamiento, haciendo constar en el mismo:<ul style="list-style-type:square"><li>fecha y hora</li><li>identificación inequívoca del equipamiento (servidores, portátiles, equipos de comunicaciones, soportes de información, etc.)</li><li>persona que realiza la entrada o salida</li><li>persona que autoriza la entrada o salida</li><li>persona que realiza el registro</li></ul>359. Se recomienda que exista segregación de funciones en el proceso de gestión de entrada y salida de equipamiento en los locales (solicitud y autorización). Dichas funciones deben recaer en al menos dos personas.<br/><br/>360. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>11.2.5 - Retirada de materiales propiedad de la empresa</li><li>11.2.6 - Seguridad de los equipos fuera de las instalaciones</li></ul></ul>361. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[PE-16] Delivery and Removal</li></ul>'

obj_518 = '<h3>5.1.8 [MP.IF.8] INSTALACIONES ALTERNATIVAS</h3>362. Se debe disponer de planes para poder prestar los servicios en un lugar alternativo en caso de indisponibilidad de las instalaciones actuales.<br/><br/>363. Las instalaciones alternativas deben garantizar las mismas medidas de protección que las habituales. En particular, en lo que respecta a control de acceso de personas y entrada y salida de equipos.<br/><br/>364. Las instalaciones alternativas pueden estar dispuestas para entrar en servicio inmediatamente (hot site) o requerir un tiempo de personalización (cold site). En todo caso el tiempo de entrada en servicio debe estar respaldado por un análisis de impacto (ver [op.cont.1]), ser parte del plan de continuidad probado (ver [op.cont.2]) y ser objeto de pruebas regulares para validar la viabilidad del plan (ver [op.cont.3]).<br/><br/>365. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de los medios de procesamiento de información</li></ul></ul>366. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP-2] Contingency Plan</li><li>[CP-6] Alternate Storage Site</li><li>[CP-7] Alternate Processing Site</li><li>[PE-17] Alternate Work Site</li></ul>'

obj_521 = '<h3>5.2.1 [MP.PER.1] CARACTERIZACIÓN DEL PUESTO DE TRABAJO</h3>368. Se deben definir las responsabilidades relacionadas con cada puesto de trabajo en materia de seguridad. La definición debe venir respaldada por el análisis de riesgos en la medida en que afecta a cada puesto de trabajo.<br/><br/>369. Se deben definir los requisitos que deben satisfacer las personas que vayan a ocupar el puesto de trabajo, en particular en términos de confidencialidad.<br/><br/>370. Se deben tener en cuenta dichos requisitos en la selección de la persona que va a ocuparlo, incluyendo la verificación de sus antecedentes laborales, formación y otras referencias: dentro del marco de la ley.<br/><br/>371. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>7.1.1 - Investigación de antecedentes</li></ul></ul>372. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[PS-2] Position Risk Designation</li><li>[PS-3] Personnel Screening</li><li>[SA-21] Developer Screening</li></ul>'

obj_522 = '<h3>5.2.2 [MP.PER.2] DEBERES Y OBLIGACIONES</h3>373. Se debe informar a cada persona relacionada con el sistema de los deberes y responsabilidades de su puesto de trabajo en materia de seguridad, incluyendo las medidas disciplinarias a que haya lugar.<br/><br/>374. Se debe cubrir tanto el periodo durante el cual se desempeña el puesto como las obligaciones en caso de terminación de la asignación, incluyendo el caso de traslado a otro puesto de trabajo.<br/><br/>375. Es de especial relevancia el deber de confidencialidad respecto de los datos a los que tengan acceso, tanto durante el periodo durante el que estén adscritos al puesto de trabajo, como su prolongación posterior a la terminación de la función para la que tuvo acceso a la información confidencial.<br/><br/>376. En el caso de personal contratado a través de una tercera parte:<ul style="list-style-type:square"><li>se deben determinar deberes y obligaciones de la persona</li><li>se deben determinar deberes y obligaciones de la parte contratante</li><li>se debe determinar el procedimiento de resolución de incidentes relacionados con el incumplimiento de las obligaciones, involucrando a la parte contratante</li></ul>377. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>7.1.2 - Términos y condiciones de contratación</li><li>7.2.1 - Responsabilidades de la Dirección</li><li>7.2.3 - Proceso disciplinario</li><li>7.3.1 - Terminación o cambio de responsabilidades laborales</li><li>8.1.4 - Devolución de activos</li><li>13.2.4 - Acuerdos de confidencialidad o no divulgación</li></ul></ul>378. NIST 800-53 rev. 4<ul style="list-style-type:square"><li>[PL-4] Rules of Behavior</li><li>[PS-6] Access Agreements</li><li>[PS-7] Third-Party Personnel Security</li><li>[PS-4] Personnel Termination</li><li>[PS-5] Personnel Transfer</li><li>[PS-8] Personnel Sanctions</li></ul>'

obj_523 = '<h3>5.2.3 [MP.PER.3] CONCIENCIACIÓN</h3>379. Se debe concienciar regularmente al personal acerca de su papel y responsabilidad para que la seguridad del sistema alcance los niveles exigidos.<br/><br/>380. En particular hay que refrescar regularmente:<ul style="list-style-type:square"><li>la normativa de seguridad relativa al buen uso de los sistemas</li><li>la identificación de incidentes, actividades o comportamientos sospechosos que deban ser reportados para su tratamiento por personal especializado</li><li>el procedimiento de reporte de incidentes de seguridad, seas reales o falsas alarmas</li></ul>381. Todo el personal debe recibir inicial y regularmente información acerca de los puntos arriba descritos.<br/><br/>382. ISO/IEC 27000<ul style="list-style-type:square"><li>27001:2013</li><ul style="list-style-type:circle"><li>7.3 - Concienciación</li></ul><li>27002:2013</li><ul style="list-style-type:circle"><li>7.2.2 - Concienciación, formación y capacitación en seguridad de la información</li></ul></ul>383. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AT-2] Security Awareness Training</li><li>[AT-3] Role-Based Security Training</li><li>[CP-3] Contingency Training</li><li>[IR-2] Incident Response Training<li>[PM-13] Information Security Resources</li></ul>384. Otras referencias:<ul style="list-style-type:square"><li>NIST SP 800-50 - Building an Information Technology Security Awareness and Training Program</li></ul>'

obj_524 = '<h3>5.2.4 [MP.PER.4] FORMACIÓN</h3>385. Se debe formar regularmente a las personas en aquellas técnicas que requieran para el desempeño de sus funciones.<br/><br/>386. Es de destacar, sin perjuicio de otros aspectos:<ul style="list-style-type:square"><li>configuración de sistemas</li><li>gestión de incidentes (detección y reacción)</li><li>procedimientos relativos a sus funciones sobre la gestión de la información (almacenamiento, transferencia, copias, distribución y destrucción)</li></ul>387. La formación debe actualizarse cada vez que cambian los componentes del sistema de información, introduciéndose nuevos equipos, nuevo software, nuevas instalaciones, etc.<br/><br/>388. ISO/IEC 27000<ul style="list-style-type:square"><li>27001:2013</li><ul style="list-style-type:circle"><li>7.2 - Competencias</li></ul><li>27002:2013</li><ul style="list-style-type:circle"><li>7.2.2 - Concienciación, formación y capacitación en seguridad de la información</li></ul></ul>389. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AT-2] Security Awareness Training</li><li>[AT-3] Role-Based Security Training</li><li>[AT-4] Security Training Records</li><li>[CP-3] Contingency Training</li><li>[IR-2] Incident Response Training</li><li>[PM-13] Information Security Resources</li></ul>390. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.17 - Security Skills Assessment and Appropriate Training to Fill Gaps</li></ul><li>NIST SP 800-16 - Information Technology Security Training Requirements: A Role- and Performance-Based Model</li><li>NIST SP 800-50 - Building an Information Technology Security Awareness and Training Program</li></ul>'

obj_525 = '<h3>5.2.5 [MP.PER.5] PERSONAL ALTERNATIVO</h3>391. Se debe prever la existencia de otras personas que se puedan hacer cargo de las funciones en caso de indisponibilidad del personal habitual. El personal alternativo deberá ofrecer las mismas garantías de seguridad que el personal habitual.<br/><br/>392. Este personal alternativo puede ser, por ejemplo:<ul style="list-style-type:square"><li>Personal del mismo equipo sobredimensionado con capacidad de asumir el trabajo</li><li>Personal de otros turnos 24x7 que puedan cubrir bajas eventuales</li><li>Personal de otros departamentos con los conocimientos necesarios (respetando la segregación)</li><li>Personal de un tercero contratado previsto en el Plan de Continuidad</li></ul>393. El plan de utilización de personal alternativo se vertebra dentro del plan de continuidad de la organización, incluyéndose en las pruebas periódicas.<br/><br/>394. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de los recursos de tratamiento de la información</li></ul></ul>395. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP-2] Contingency Plan</li><li>[CP-6] Alternate Storage Site</li><li>[CP-7] Alternate Processing Site</li></ul>'

obj_531 = '<h3>5.3.1 [MP.EQ.1] PUESTO DE TRABAJO DESPEJADO</h3>396. Se debe exigir que los puestos de trabajo permanezcan despejados, sin más material encima de la mesa que el requerido para la actividad que se está realizando en cada momento. Según se termine una tarea, el material se retirará a otra zona: cajones, estanterías personales o comunes, cuarto de almacenamiento, etc.<br/><br/>397. El material de trabajo se guardará en lugar cerrado. Pueden ser cajones o armarios con llave, o un cuarto separado cerrado con llave al menos fuera del horario de trabajo.<br/><br/>398. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>11.2.9 - Política de puesto de trabajo despejado y pantalla limpia</li></ul></ul>399. NIST SP 800-53 rev. 4'

obj_532 = '<h3>5.3.2 [MP.EQ.2] BLOQUEO DE PUESTO DE TRABAJO</h3>400. Se debe bloquear automáticamente el puesto de trabajo desde el que se accede a servicios o datos de nivel medio o superior al cabo de un tiempo de inactividad, que se marcará por parte de la entidad o compañía.<br/><br/>401. Se debe requerir al usuario autenticarse de nuevo para reanudar la actividad en curso.<br/><br/>402. El tiempo mencionado será parte de la configuración del equipo y no podrá ser alterado por el usuario.<br/><br/>403. Se cancelarán las sesiones abiertas tanto desde dicho puesto de trabajo como las remotas al cabo de un tiempo de inactividad (superior al bloqueo del puesto de trabajo).<br/><br/>404. El tiempo mencionado será parte de la configuración del equipo y no podrá ser alterado por el usuario.<br/><br/>405. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>11.2.8 - Equipo de usuario desatendido</li></ul></ul>406. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AC-11] Session Lock</li><li>[AC-12] Session Termination</li></ul>'

obj_533 = '<h3>5.3.3 [MP.EQ.3] PROTECCIÓN DE EQUIPOS PORTÁTILES</h3>407. Debe existir un inventario de los equipos portátiles, que identifique el equipo portátil junto a la persona responsable del mismo. Se debe verificar regularmente en el inventario que el equipo permanece bajo control del usuario al que está asignado.<br/><br/>408. Se recomienda que los equipos portátiles tengan instalado y activado un sistema de protección perimetral (cortafuegos personal) configurado para bloquear accesos salvo los autorizados. Los accesos autorizados seguirán los procedimientos de autorización del organismo (ver [org.4]).<br/><br/>409. Los accesos realizados remotamente deberán ser distinguidos por el servidor para que pueda limitar y autorizar la información y los servicios accesibles cuando se conecten remotamente a través de redes que no pueda controlar la organización.<br/><br/>410. El mecanismo de control del equipo formará parte de la configuración del equipo y no podrá ser modificado por el usuario.<br/><br/>411. Los usuarios recibirán instrucciones sobre el uso admisible del equipo, sobre los aspectos que debe contemplar en su manejo diario y del canal de comunicación para informar al servicio de gestión de incidentes en caso de avería, pérdida, robo o terminación.<br/><br/>412. Se deberá comunicar al personal que los equipos portátiles no deben contener claves de acceso remoto a la organización y se identificará y aprobará formalmente aquellos casos en los que no puede aplicarse.<br/><br/>413. Los equipos portátiles deberán disponer de detectores de violación que permitan saber si el equipo ha sido manipulado y, en caso afirmativo, activar los procedimientos de gestión del incidente. Los detectores de violación podrán ser:<ul style="list-style-type:square"><li>Físicos: por ejemplo, pegatinas que se alteran al manipularlas, bridas de protección, etc.</li><li>Lógicos: por ejemplo, herramientas automatizadas que detecten si algún componente del portátil ha sido extraído o sustituido</li></ul>414. Se recomienda proteger el acceso a la información que contienen los equipos portátiles que sean susceptibles de salir de las instalaciones de la organización (por ejemplo, con candados, discos duros cifrados, etc.).<br/><br/>415. Se debe proteger la información contenida de nivel alto por medios criptográficos: [mp.si.2].<br/><br/>416. Las claves criptográficas deben protegerse según [op.exp.11].<br/><br/>417. Cuando el equipo es desmantelado, se debe aplicar lo previsto en [mp.si.5].<br/><br/>418. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-827 - Gestión y uso de dispositivos móviles</li></ul>419. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>6.2.1 - Política de dispositivos móviles</li><li>11.2.6 - Seguridad de los equipos fuera de las instalaciones</li></ul></ul>420. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[AC-19] Access Control for Mobile Devices</li></ul>'

obj_534 = '<h3>5.3.4 [MP.EQ.4] MEDIOS ALTERNATIVOS</h3>421. Se debe prever medios alternativos de tratamiento de la información para el caso de que fallen los equipos de personal habituales. Estos medios alternativos estarán sujetos a las mismas garantías de protección.<br/><br/>422. Se debe establecer un tiempo máximo para que los equipos alternativos entren en funcionamiento.<br/><br/>423. Los equipos alternativos pueden estar dispuestos para entrar en servicio inmediatamente (es decir, configurados) o requerir un tiempo de personalización (se puede disponer de ellos en el tiempo prestablecido; pero hay que configurarlos y cargar los datos). En todo caso el tiempo de entrada en servicio debe estar respaldado por un análisis de impacto (ver [op.cont.1]).<br/><br/>424. ISP/IEC 27000<ul style="list-style-type:square"><li>27002:2013</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de instalaciones de tratamiento de la información</li></ul></ul>425. NIST SP 800-53 rev. 4'

obj_541 = '<h3>5.4.1 [MP.COM.1] PERÍMETRO SEGURO</h3>426. Se debe delimitar el perímetro lógico del sistema; es decir, los puntos de interconexión con el exterior. Este perímetro deberá estar reflejado en la documentación de la arquitectura del sistema (por ejemplo, el esquema de red).<br/><br/>427. Se debe disponer de cortafuegos que separen la red interna del exterior. Todo el tráfico deberá atravesar dichos cortafuegos que sólo dejaran transitar los flujos previamente autorizados.<br/><br/>428. Cuando se requiera niveles de seguridad ALTA, el sistema de cortafuegos constará de dos o más equipos de diferente fabricante dispuestos en cascada. Estos cortafuegos podrán ser equipos físicos o instalaciones o aplicaciones cortafuegos virtuales.<br/><br/>429. Cuando la disponibilidad de las transmisiones a través del cortafuegos sea de nivel ALTO, se dispondrán sistemas redundantes.<br/><br/>430. Los ataques de denegación de servicio pueden ser afrontados en el perímetro, aunque pueden requerir la intervención de otros elementos. En el perímetro se pueden detectar patrones sospechosos de comportamiento: avalanchas de peticiones, peticiones trucadas y, en general, un uso malicioso de los protocolos de comunicaciones. Algunas de estas peticiones pueden ser denegadas directamente por el equipo perimetral, en otras ocasiones hay que levantar una alarma para actuar en donde corresponda (servidores web, servidores de bases de datos... o contactando con los centros de respuesta a incidentes).<br/><br/>431. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-408 - Seguridad Perimetral - Cortafuegos</li><li>Guía CCN-STIC-419 - Configuración segura con IPtables</li><li>Serie CCN-STIC-500 - Guías para Entornos Windows</li><li>Serie CCN-STIC-600 - Guías para otros Entornos</li><li>Guía CCN-STIC-811 - Interconexión</li></ul>432. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>13.1.2 - Seguridad de los servicios de red</li></ul></ul>433. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AC-4] Information Flow Enforcement</li><li>[CA-3] System Interconnections</li><li>[SC-7] Boundary Protection</li></ul>434. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.8 - Malware Defenses</li><li>CSC.9 – Limitation and Control of Network Ports</li><li>CSC.11 – Secure Configurations for Network Devices</li><li>CSC.12 – Boundary Defense</li><li>CSC.13 – Data Protection</li><li>CSC.15 - Wireless Access Control</li></ul><br/><li>NIST SP 800-41 - Guidelines on Firewalls and Firewall Policy</li></ul>'

obj_542 = '<h3>5.4.2 [MP.COM.2] PROTECCIÓN DE LA CONFIDENCIALIDAD</h3>435. Es frecuente que autenticidad, integridad y confidencialidad se traten de forma conjunta negociando los protocolos, los parámetros y las claves en la fase de establecimiento. Es por ello que esta medida suele implementarse a la par que [mp.com.3].<br/><br/>436. Se deben emplear algoritmos acreditados por el Centro Criptológico Nacional que garanticen el secreto de los datos transmitidos.<br/><br/>437. En conexiones establecidas fuera del dominio de seguridad de la organización, se recurrirá a redes privadas virtuales que, con métodos criptográficos y tras una autenticación fiable (ver [mp.com.3]), establecen una clave de cifrado para la sesión.<br/><br/>438. El cifrado de las comunicaciones es especialmente adecuado en redes inalámbricas (WiFi)20. Los equipos inalámbricos llevan incorporados mecanismos de cifrado de las comunicaciones, que deberán ser configurados de forma segura (ver [op.exp.2] y [op.exp.3]) empleando mecanismos actualizados.<br/><br/>439. Hay que atender al secreto de las claves de cifrado según lo indicado en [op.exp.11]. En el caso de redes privadas virtuales, el secreto debe ser impredecible, mantenerse bajo custodia mientras dure la sesión, y ser destruido al terminar. En el caso de otros procedimientos de cifrado, hay que cuidar de las claves de cifrado durante su ciclo de vida: generación, distribución, empleo, retirada del servicio y retención si la hubiera.<br/><br/>440. Hay que seleccionar algoritmos evaluados o acreditados. A menudo basta con seleccionar los algoritmos y los parámetros adecuados dentro de las opciones posibles.<br/><br/>441. Hay que procurar que las tareas de cifrado en los extremos se realicen en equipos hardware especializados y certificados, conforme a [op.pl.5], evitando el cifrado por software.<br/><br/>442. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-807 Criptografía de empleo en el ENS</li><li>Guía CCN-STIC-827 - Gestión y uso de dispositivos móviles</li><li>Guía CCN-STIC-406 - Seguridad en Redes Inalámbricas</li><li>Guía CCN-STIC-416 - Seguridad en redes privadas virtuales</li></ul>443. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>10.1.1 - Política de uso de los controles criptográficos</li><li>13.1.1 - Controles de red</li><li>13.1.2 - Seguridad de los servicios de red</li><li>14.1.2 - Asegurar los servicios de aplicaciones en redes públicas</li><li>18.1.5 - Regulación de los controles criptográficos</li></ul></ul>444. NIST 800-53 rev. 4<ul style="list-style-type:square"><li>[AC-4] Information Flow Enforcement</li><li>[AC-18] Wireless Access</li><li>[SC-8] Transmission Confidentiality and Integrity</li><li>[SC-12] Cryptographic Key Establishment and Management</li><li>[SC-13] Cryptographic Protection</li><li>[SC-40] Wireless Link Protection</li></ul>445. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.15 - Wireless Access Control</li></ul></ul><ul style="list-style-type:square"><li>NIST SP 800-48 - Wireless Network Security for IEEE 802.11a/b/g and Bluetooth</li><li>NIST SP 800-52 - Guidelines for the Selection and Use of Transport Layer Security (TLS) Implementations</li><li>NIST SP 800-77 - Guide to IPsec VPNs</li><li>NIST SP 800-113 - Guide to SSL VPNs</li><li>NIST SP 800-121 - Guide to Bluetooth Security</li><li>NIST SP 800-127 - Guide to Securing WiMAX Wireless Communications</li><li>NIST SP 800-153 - Guidelines for Securing Wireless Local Area Networks (WLANs)</li><li>SSL – Secure Sockets Layer</li><ul style="list-style-type:circle"><li>[RFC 6101] The Secure Sockets Layer (SSL) Protocol Version 3.0</li><li>Guía CCN-STIC-826 Configuración de SSL/TLS</li></ul><li>TLS – Transport Layer Security</li><ul style="list-style-type:circle"><li>[RFC 5246] The Transport Layer Security (TLS) Protocol – Version 1.2</li><li>[RFC 6176] Prohibiting Secure Sockets Layer (SSL) Version 2.0</li><li>Guía CCN-STIC-826 Configuración de SSL/TLS</li></ul><li>SSH – Secure Shell</li><li>SCP – Secure copy</li><li>SFTP – SSH File Transfer Protocol</li></ul>'

obj_543 = '<h3>5.4.3 [MP.COM.3] PROTECCIÓN DE LA AUTENTICIDAD Y DE LA INTEGRIDAD</h3>446. Es frecuente que autenticidad, integridad y confidencialidad se traten de forma conjunta negociando los protocolos, los parámetros y las claves en la fase de establecimiento. Es por ello que esta medida suele implementarse a la par que [mp.com.2].<br/><br/>447. Se debe establecer de forma fehaciente la autenticidad del otro extremo de un canal de comunicación antes de intercambiar información alguna.<br/><br/>448. Se debe evitar la utilización de mecanismos de autenticación y protocolos no contemplados en la normativa de la organización.<br/><br/>449. Se deben usar protocolos que garanticen o al menos comprueben y detecten violaciones en la integridad de los datos intercambiados y en la secuencia de los paquetes.<br/><br/>450. La forma más habitual de establecer esta medida es establecer una red privada virtual que:<ul style="list-style-type:square"><li>garantice la autenticación de las partes al inicio de sesión, cuando la red se establece</li><li>controle que la sesión no puede ser secuestrada por una tercera parte</li><li>que no permita realizar ataques activos (alteración de la información en tránsito o inyección de información espuria) sin que sea, al menos, detectada</li></ul>451. Hay que seleccionar algoritmos evaluados o acreditados por el Centro Criptológico Nacional que garanticen el secreto de los datos transmitidos. A menudo basta con seleccionar los algoritmos y los parámetros adecuados dentro de las opciones posibles.<br/><br/>452. Se debe evitar la utilización de mecanismos de autenticación y protocolos no contemplados en la normativa de aplicación. Además, en caso de utilizar claves concertadas, deberán utilizarse con cautela aplicando exigencias medias de calidad.<br/><br/>453. En conexiones establecidas fuera del dominio de seguridad de la organización, se puede recurrir a redes privadas virtuales que, con métodos criptográficos y tras una autenticación fiable, establecen una clave de cifrado para la sesión.<br/><br/>454. El cifrado de las comunicaciones es especialmente adecuado en redes inalámbricas (WiFi). Los equipos inalámbricos llevan incorporados mecanismos de cifrado de las comunicaciones, que deberán ser configurados de forma segura (ver [op.exp.2] y [op.exp.3]) empleando mecanismos actualizados.<br/><br/>455. Hay que atender al secreto de las claves de cifrado según lo indicado en [op.exp.11]. En el caso de redes privadas virtuales, el secreto debe ser impredecible, mantenerse bajo custodia mientras dure la sesión, y ser destruido al terminar. En el caso de otros procedimientos de cifrado, hay que cuidar de las claves de cifrado durante su ciclo de vida: generación, distribución, empleo, retirada del servicio y retención si la hubiera.<br/><br/>456. Hay que procurar que las tareas de cifrado en los extremos se realicen en equipos hardware especializados y certificados, conforme a [op.pl.5], evitando el cifrado por software.<br/><br/>457. Se debe evitar la utilización de mecanismos de autenticación y protocolos no contemplados en la normativa de aplicación. Además, en caso de utilizar claves concertadas, deberán utilizarse con cautela aplicando exigencias altas de calidad.<br/><br/>458. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-416 - Seguridad en redes privadas virtuales</li><li>Guía CCN-STIC-807 – Criptografía de empleo en el ENS</li></ul>459. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>10.1.1 - Política de uso de los controles criptográficos</li><li>13.1.1 - Controles de red</li><li>13.1.2 - Seguridad de los servicios de red</li><li>14.1.2 - Asegurar los servicios de aplicaciones en redes públicas</li></ul></ul>460. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AC-18] Wireless Access</li><li>[SC-8] Transmission Confidentiality and Integrity</li><li>[SC-13] Cryptographic Protection</li><li>[SC-23] Session Authenticity</li><li> [SC-40] Wireless Link Protection</li></ul>461. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.15 - Wireless Access Control</li></ul></ul>'

obj_544 = '<h3>5.4.4 [MP.COM.4] SEGREGACIÓN DE REDES</h3>462. La segregación de redes acota el acceso a la información y acota la propagación de los incidentes de seguridad que quedan restringidos al entorno donde ocurren. Esta deberá quedar reflejada en documentación de la arquitectura del sistema (por ejemplo, el esquema de red) [op.pl.2].<br/><br/>463. Se debe segmentar la red de forma que haya:<ul style="list-style-type:square"><li>control (de entrada) de los usuarios que pueden trabajar en cada segmento, en particular si el acceso se realiza desde el exterior del segmento, tanto si es desde otro segmento de la red corporativa como si el acceso procede del exterior de la red, extremando las precauciones en este último escenario</li><li>control (de salida) de la información disponible en cada segmento</li><li>control (de entrada) de las aplicaciones utilizables en cada segmento</li></ul>464. El punto de interconexión debe estar particularmente asegurado, mantenido y monitorizado (ver [mp.com.1]). Estos puntos de interconexión interna son una defensa crítica frente a intrusos que han logrado superar las barreas exteriores y se alojan en el interior. Nótese que a menudo el objetivo de estas intrusiones es extraer información y enviarla al exterior, lo que se traduce en que hay que vigilar los protocolos de comunicaciones que se establecen y los datos que se transmiten.<br/><br/>465. No debería permitirse ningún protocolo directo entre los segmentos internos y el exterior, intermediando todos los intercambios de información.<br/><br/>466. Las redes se pueden segmentar por dispositivos físicos o lógicos.<br/><br/>467. Esta medida puede establecerse dinámicamente como reacción frente a intrusiones (supuestas o detectadas) y que van a requerir un cierto periodo de tiempo (días) en poder ser erradicadas. Los primeros servicios a aislar serían los servidores de datos y los servidores de autenticación para monitorizar y controlar su uso. Otros candidatos a ser aislados son los servicios de administración del propio sistema para evitar que se capturen credenciales con privilegios de administración o se pueda suplantar la identidad de los administradores.<br/><br/>468. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-408 - Seguridad perimetral (cortafuegos)</li><li>Guía CCN-STIC-419 - Configuración segura con IPtables</li><li>Serie CCN-STIC-600 Guías para otros Entornos</li><li>Guía CCN-STIC-641 - Seguridad en routers Cisco</li></ul>469. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>13.1.3 - Segregación en redes</li></ul></ul>470. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[SC-32] Information System Partitioning</li></ul>'

obj_545 = '<h3>5.4.5 [MP.COM.5] MEDIOS ALTERNATIVOS</h3>471. Se debe prever medios alternativos de comunicación para el caso de que fallen los medios habituales. Estos medios alternativos deben proporcionar las mismas garantías de seguridad que los medios habituales y deberá establecerse un tiempo máximo de entrada en funcionamiento que esté aprobado por su responsable.<br/><br/>472. En todo caso, el tiempo de entrada en servicio debe estar respaldado por un análisis de impacto (ver [op.cont.1]), ser parte del plan de continuidad probado (ver [op.cont.2]) y ser objeto de pruebas regulares para validar la viabilidad del plan (ver [op.cont.3]).<br/><br/>473. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de los recursos de tratamiento de la información</li></ul></ul>474. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP-8] Telecommunications Services</li><li>[CP-11] Alternate Communications Protocol</li></ul>'

obj_551 = '<h3>5.5.1 [MP.SI.1] ETIQUETADO</h3>477. Se debe etiquetar de forma que, sin revelar su contenido, se indique el nivel de calificación más alto de la información contenida.<br/><br/>478. Una opción es que el propio soporte, en su exterior, lleve escrito el nivel de información que contiene o puede contener.<br/><br/>479. Una alternativa es que el soporte sea identificable por medio de algún código o referencia y que el usuario pueda acceder a un repositorio de información donde se indica el nivel de información que el soporte contiene o puede contener.<br/><br/>480. La etiqueta del soporte determina las normativas y los procedimientos que deben aplicarse al mismo, concretamente en lo referente a:<ul style="list-style-type:square"><li>control de acceso</li><li>cifrado del contenido</li><li>entrada y salida de las instalaciones</li><li>medios de transporte</li></ul>481. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>8.2.2 - Etiquetado de la información</li><li>8.3.1 - Gestión de soportes extraíbles</li></ul></ul>482. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[MP-3] Media Marking</li></ul>'

obj_552 = '<h3>5.5.2 [MP.SI.2] CRIPTOGRAFÍA</h3>483. Este requisito se aplica, en particular, a todos los dispositivos removibles (como CD, DVD, discos USB, etc.).<br/><br/>484. En lo referente a claves criptográficas, se debe aplicar [op.exp.11].<br/><br/>485. Una opción es asegurarse que los datos se protegen antes de copiarse al soporte; es decir, se cifran o se firman exteriormente.<br/><br/>486. Otra opción es proteger todo el soporte instalando en el mismo un disco virtual que se encarga de acoger todo lo que se copie en el mismo, así como controlar el acceso al mismo.<br/><br/>487. Otra opción es emplear soportes con cifrado incorporado por hardware que se encarga de acoger todo lo que se copie en el soporte, así como controlar el acceso al mismo.<br/><br/>488. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-807 - Criptografía</li><li>Guía CCN-STIC-437 - Herramientas de Cifrado Software</li><li>Guía CCN-STIC-955 - Recomendaciones empleo GnuPG</li></ul>489. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>8.3.1 - Gestión de soportes extraíbles</li><li>10.1.1 - Política de uso de los controles criptográficos</li></ul></ul>490. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[SC-28] Protection of Information at Rest</li></ul>491. Otras referencias:<ul style="list-style-type:square"><li>NIST SP 800-111 - Guide to Storage Encryption Technologies for End User Devices</li></ul>492. Productos. Hay muchos donde elegir; sólo se citan algunos de uso frecuente:<ul style="list-style-type:square"><li>BitLocker – Microsoft</li><li>Crypt2000 – Secuware</li><li>GPG – http://www.gnupg.org/</li><li>PGP – Symantec</li><li>Veracrypt</li></ul>'

obj_553 = '<h3>5.5.3 [MP.SI.3] CUSTODIA</h3>493. Se debe aplicar la debida diligencia y control a los soportes de información (tanto en soporte electrónico como no electrónico) que permanecen bajo la responsabilidad de la organización:<ul style="list-style-type:square"><li>garantizando el control de acceso con medidas físicas ([mp.if.1] y [mp.if.7) o lógicas ([mp.si.2]) o ambas</li><li>garantizando que se respetan las exigencias de mantenimiento del fabricante, en especial en lo referente a temperatura, humedad y otros agresores medioambientales</li></ul>494. Se recomienda conservar la historia de cada dispositivo, desde su primer uso hasta la terminación de su vida útil y verificar regularmente que los soportes cumplen las reglas acordes a su etiquetado.<br/><br/>495. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>8.3.1 - Gestión de soportes extraíbles</li></ul></ul>496. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[MP-4] Media Storage</li></ul>497. Otras referencias:<ul style="list-style-type:square"><li>NIST SP 800-111 – Guide to Storage Encryption Technologies for End User Devices</li></ul>'

obj_554 = '<h3>5.5.4 [MP.SI.4] TRANSPORTE</h3>498. Se debe garantizar que los dispositivos permanecen bajo control y se satisfacen sus requisitos de seguridad mientras están siendo desplazados de un lugar a otro.<br/><br/>499. Se debe:<ul style="list-style-type:square"><li>disponer de un registro de salida que identifica al menos la etiqueta y al transportista que recibe el soporte para su traslado (tanto electrónico como no electrónico)</li><li>disponer de un registro de entrada que identifica al menos la etiqueta y al transportista que lo entrega</li><li>disponer de un procedimiento rutinario que coteja las salidas con las llegadas y levanta las alarmas pertinentes cuando se detecta algún incidente</li><li>utilizar los medios de protección criptográfica ([mp.si.2]) correspondientes al nivel de clasificación de la información contenida de mayor nivel</li><li>gestionar las claves según [op.exp.11]</li></ul>500. Se recomienda disponer de un procedimiento al respecto y se verifica regularmente que los procedimientos establecidos se siguen, aplicando medidas correctivas en su defecto.<br/><br/>501. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-typecircle"><li>8.3.3 - Soportes físicos en tránsito</li><li>11.2.5 - Retirada de materiales propiedad de la empresa</li></ul></ul>502. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[MP-5] Media Transport</li></ul>'

obj_555 = '<h3>5.5.5 [MP.SI.5] BORRADO Y DESTRUCCIÓN</h3>503. Se debe aplicar un mecanismo de borrado seguro a los soportes extraíbles (electrónicos y no electrónicos) que vayan a ser reutilizados para otra información o liberados a otra organización. El mecanismo de borrado será proporcionado a la clasificación de la información que ha estado presente en el soporte.<br/><br/>504. Se deben destruir los soportes, de forma segura:<ul style="list-style-type:square"><li>cuando la naturaleza del soporte no permita un borrado seguro</li><li>cuando el procedimiento asociado al nivel de clasificación de la información contenida así lo requiera</li></ul>505. El mecanismo de destrucción será proporcionado a la clasificación de la información contenida.<br/><br/>506. Los mecanismos de borrado y destrucción deben tener en la normativa de protección medioambiental y los certificados de calidad medioambiental de la organización.<br/><br/>507. Se deben elegir productos certificados conforme a lo establecido en [op.pl.5]<br/><br/>508. Recomendaciones (tomadas de NIST SP 800-88):<br/><br/><table style="width:100%" border="1"><tr><th>Medio</th><th>Procedimiento</th><th>Acciones</th></tr><tr><td>papel<br/>microfilm</td><td>destruir</td>    <td><ul><li>trituradora en tiras o cuadraditos: 2mm</li></ul></td></tr><tr><td>móviles<br/>PDAs</td><td>borrar manualmente</td><td><ul><li>agenda</li><li>mensajes</li><li>llamadas</li><li>resetear a la configuración de fábrica</li></ul></td></tr><tr><td>routers</td><td>borrar manualmente</td><td><ul><li>tablas de encaminamiento</li><li>registros de actividad</li><li>cuentas de administración</li><li>resetear a la configuración de fábrica</li></ul></td></tr><tr><td>impresoras<br/>fax</td><td>borrar manualmente</td><td><ul><li>resetear a la configuración de fábrica</li></ul></td></tr><tr><td>discos reescribibles</td><td>reescribir</td><td><ul><li>reescribir 3 veces: con ceros, con unos, con datos aleatorios</li></ul></td></tr><tr><td>discos de solo lectura</td><td>destruir</td><td><ul><li>trituradora: 5mm</li></ul></td></tr><tr><td>discos virtuales cifrados</td><td>además de lo anterior</td><td><ul><li>destruir las claves</li></ul></td></tr></table>Tabla 4: Recomendaciones NIST SP 800-88 para borrado y destrucción<br/><br/>509. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-305 – Destrucción y sanitización de soportes informáticos (uso oficial)</li><li>Guía CCN-STIC-400 - Manual de seguridad de las TIC</li><li>Guía CCN-STIC-403 - Herramientas de seguridad</li><li>Guía CCN-STIC-404 - Control de soportes informáticos</li><li>Guía CCN-STIC-818 - Herramientas de seguridad</li></ul>510. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>8.3.2 - Eliminación de soportes</li><li>11.2.7 - Reutilización o eliminación segura de equipos</li></ul></ul>511. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[MP-6] Media Sanitization</li><li>[MP-8] Media Downgrading</li></ul>512. Otras referencias:<ul style="list-style-type:square"><li>NIST SP 800-88 - Guidelines for Media Sanitization</li><li>DoD 5220 Block Erase</li></ul>'

obj_561 = '<h3>5.6.1 [MP.SW.1] DESARROLLO</h3>513. El desarrollo de aplicaciones se realizará sobre un sistema diferente y separado del de producción, no debiendo existir herramientas o datos de desarrollo en el entorno de producción. Ver [op.acc.3] sobre segregación de funciones. Para que la segregación sea creíble, se deben separar los entornos y controlar los mecanismos de identificación, autenticación y control de acceso de los usuarios diferenciando rigurosamente los privilegios de cada uno.<br/><br/>514. La metodología de desarrollo conviene que sea un estándar reconocido que incluya la seguridad como parte integral del desarrollo (por ejemplo, METRICA, Security Development Lifecycle, Correctness by Construction, Building Security In Maturity Model, OWASP, etc.). Es decir, desde la concepción arquitectónica hay que plantear los requisitos de seguridad del sistema final e ir optando por soluciones que introduzcan los controles necesarios en el software desarrollado.<br/><br/>515. Hay que evitar que se desarrolle pensando únicamente en la funcionalidad y que los requisitos de seguridad se añadan posteriormente parcheando.<br/><br/>516. Desarrollo integral significa que las funciones de seguridad son parte de la interfaz de usuario, que los registros de actividad e incidencias son parte de la arquitectura de registro y que existen mecanismos de validación, protección de la información y verificación de que se respeta la política de seguridad deseada.<br/><br/>517. Durante las pruebas de desarrollo y de aceptación no se usarán datos de prueba reales, sino datos específicos para pruebas. Cuando los datos de prueba procedan de datos reales, se manipularán para que no se puedan reconocer datos reales en las pruebas. En último caso, si fuera inevitable usar datos reales, se protegerán como si estuvieran en producción. Por último, los datos de prueba deben retirarse cuando el sistema pasa a producción.<br/><br/>518. La inspección del código fuente debe ser posible tanto durante el desarrollo como durante la vida útil del software. Inspeccionar todo el código es costoso y probablemente injustificado en los sistemas de soporte al ENS; pero es necesario acceder al código fuente para analizar incidentes y para planificar pruebas de penetración. Por ello debe estar disponible con las debidas garantías de control de acceso.<br/><br/>519. En todo caso hay que revisar fallos típicos de programación que puedan derivar en problemas de seguridad:<ul style="list-style-type:square"><li>desbordamiento de buffers,</li><li>información residual en almacenamiento temporal (RAM, ficheros en disco, datos en la red, datos en la nube, …),</li><li>almacenamiento de claves y material criptográfico,</li><li>validación de los datos de entrada, de usuarios y entre procesos,</li><li>validación de la configuración,</li><li>posibilidades de inyección de código,</li><li>posibles race conditions (carreras de concurrencia),</li><li> escalado de privilegios,</li><li>comunicaciones sin autenticar y/o sin cifrar,</li><li>etc.</li></ul>520. Se incluyen normas de programación segura. Se recomienda adoptar soluciones automatizadas de análisis de código estático que permitan verificar ante cada nueva versión que no es publicada con errores de programación conocidos.<br/><br/>521. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-205 - Actividades Seguridad Ciclo Vida CIS</li></ul>522. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>9.4.5 - Control de acceso al código fuente de los programas</li><li>12.1.4 - Separación de los recursos de desarrollo, prueba y operación</li><li>14.2.1 - Política de desarrollo seguro</li><li>14.2.5 - Principios de ingeniería de sistemas seguros</li><li>14.2.6 - Entorno de desarrollo seguro</li><li>14.2.7 - Externalización del desarrollo de software</li><li>14.3.1 - Protección de los datos de prueba</li></ul></ul>523. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CM-4] (1) Security Impact Analysis - Separate Test Environments</li><li>[SA-3] System Development Life Cycle</li><li>[SA-4] Acquisition Process</li><li>[SA-8] Security Engineering Principles</li><li>[SA-10] Developer Configuration Management</li><li>[SA-11] Developer Security Testing and Evaluation</li><li>[SA-12] Supply Chain Protections</li><li>[SA-15] Development Process, Standards, and Tools</li><li>[SA-17] Developer Security Architecture and Design</li></ul>524. Otras referencias:<ul style="list-style-type:square"><li>SANS</li>http://www.sans.org/curricula/secure-software-development<li>Métrica v3 - Metodología de Planificación, Desarrollo y Mantenimiento de sistemas de información, Ministerio de Administraciones Públicas, Consejo Superior de Administración Electrónica</li><li>NIST SP 800-64 - Security Considerations in the System Development Life Cycle</li></ul>'

obj_562 = '<h3>5.6.2 [MP.SW.2] ACEPTACIÓN Y PUESTA EN SERVICIO: Categoría ALTA</h3>530. El análisis de coherencia se hace a nivel de procesos, concretamente de los que componen el proceso administrativo que le compete a la organización. Para cada proceso propio, hay que ejecutar pruebas comprobando que los datos de entrada producen los datos de salida correctos, y que datos incorrectos de entrada son detectados y atajados antes de destruir la integridad del sistema.<br/><br/>531. Para categoría ALTA, el ENS pide que se considere una auditoría de código fuente. Se refiere a la expresión inglesa "source code review" y no puede ser obligatorio para todos los sistemas ya que es un proceso desproporcionadamente lento y costoso. Además, es un proceso cuya profundidad es muy modulable.<br/><br/>532. La revisión de código fuente va más allá del empleo de herramientas automatizadas para buscar librerías, funciones o patrones de vulnerablidades, aspectos que ya se contemplan en categoría MEDIA. La revisión de código fuente es una actividad que requiere inteligencia humana para revisar sistemáticamente que el código se ejecutará de forma segura sin dejarle oportunidades a incidentes accidentales o deliberados, que no quedan puertas abiertas y que los controles de seguridad están implantados de forma efectiva. Por una parte, se busca que no haya vulnerabilidades y por otra que la aplicación sea capaz de defenderse a sí misma (self-defending) en el contexto en el que va a operar.<br/><br/>533. Esta actividad de expertos suele apoyarse en herramientas de auditoría y ataques controlados de penetración; pero va un paso más allá a analizar la integración de piezas de código o componentes. Las herramientas son ideales para tratar sistemáticamente grandes volúmenes de código y para validar que las vulnerabilidades son efectivamente explotables. Las personas son necesarias para comprender el contexto.<br/><br/>534. Por ejemplo, se buscan carreras (race conditions) en ejecución concurrente, oportunidades de escalar privilegios, fallos de limpieza de información sensible, acceso seguro a otros servicios, existencia de credenciales empotrados en el código, etc.<br/><br/>535. A efectos de cumplir con lo prescrito en el ENS, se valorará la oportunidad de proceder a la inspección del código fuente; pero en la práctica solo se justifica en sistemas críticos como pueden ser elementos de frontera con una red pública y solamente si el software no está acreditado en el sentido de [op.pl.5].<br/><br/>536. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>12.1.4 - Separación de los recursos de desarrollo, prueba y operación</li><li>12.5.1 - Instalación del software en explotación</li><li>14.2.8 - Pruebas funcionales de seguridad de sistemas</li><li>14.2.9 - Pruebas de aceptación de sistemas</li><li>14.2.7 - Externalización del desarrollo de software</li><li>14.3.1 - Protección de los datos de prueba</li></ul></ul>537. NIST SP 800-53 rev. 4<br/><br/>538. Otras referencias:<ul style="list-style-type:square"><li>Métrica v3 - Metodología de Planificación, Desarrollo y Mantenimiento de sistemas de información, Ministerio de Administraciones Públicas, Consejo Superior de Administración Electrónica</li></ul>'

obj_571 = '<h3>5.7.1 [MP.INFO.1] DATOS DE CARÁCTER PERSONAL</h3>539. Es obligatorio el cumplimiento de la regulación de protección de información personal que esté vigente, ya sean las medidas de protección determinadas para cada nivel en el Real Decreto 1720/2007 o las especificaciones del Reglamento General de Protección de Datos.<br/><br/>540. Referencias<ul style="list-style-type:square"><li>Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016, relativo a la protección de las personas físicas en lo que respecta al tratamiento de datos personales y a la libre circulación de estos datos</li><li>Ley Orgánica 15/1999, de 13 de diciembre, de Protección de Datos de Carácter Personal (B.O.E. Nº 298, de 14 de diciembre de 1999)</li><li>Real Decreto 1720/2007 de 21 de diciembre, por el que se aprueba el Reglamento de desarrollo de la Ley Orgánica 15/1999, de 13 de diciembre, de protección de datos de carácter personal</li><li>Real Decreto 3/2010, de 8 de enero, del Esquema Nacional de Seguridad</li><li>Real Decreto 951/2015, de 23 de octubre, de modificación del Real Decreto 3/2010, de 8 de enero, por el que se regula el Esquema Nacional de Seguridad en el ámbito de la Administración Electrónica</li></ul>'

obj_572 = '<h3>5.7.2 [MP.INFO.2] CALIFICACIÓN DE LA INFORMACIÓN</h3>541. Se debe establecer un esquema para asignar un nivel de calificación a la información, en función de sus necesidades de confidencialidad.<br/><br/>542. El sistema de calificación:<ul style="list-style-type:square"><li>debe ser acorde con otros sistemas de calificación propios del entorno en el que desarrolla su actividad la organización</li><li>debe ser acorde con lo indicado en el Anexo I del ENS sobre calificación de la información y categorización de los sistemas de información</li><li>debe establecer las responsabilidades para adscribir inicialmente una cierta información a una cierta calificación y para posibles re-calificaciones posteriores (niveles de seguridad) y determinar el responsable de la documentación y aprobación formal</li></ul>543. Se deben desarrollar procedimientos de uso de la información para cada nivel (etiquetado y tratamiento), cubriendo al menos los siguientes aspectos:<ul style="list-style-type:square"><li>cómo se controla el acceso, es decir, normativa, y procedimientos de autorización y mecanismos de control [op.acc]</li><li>cómo se realiza el almacenamiento (local, en la nube, cifrado, etc.) [mp.si.2] y [mp.si.3]</li><li>normativa relativa a la realización de copias en diferentes medios: proceso de autorización y mecanismos de control [mp.info.9]</li><li>cómo se marcan los documentos (etiquetado de soportes) [mp.si.1]</li><li>condiciones de adquisición, inventario, marcado, uso, borrado y destrucción de los soportes de información</li><li>cómo se gestiona el papel impreso y quién y dónde puede imprimir</li><li>transporte físico: condiciones sobre el medio de transporte, del mensajero, autorizaciones de salida y controles de recepción</li><li>condiciones de seguridad sobre el canal de comunicaciones (especialmente, autenticación y cifrado) y autorizaciones necesarias para poder trasmitir por redes de comunicaciones [mp.com]</li></ul>544. Cabe esperar que los organismos organicen la información en tres niveles: BAJO, MEDIO y ALTO, alineados a los niveles del Anexo I. Siguiendo este esquema, se pueden desarrollar tablas como la siguiente:<br/><br/><table style="width:100%" border="1"><tr><th>Elemento de ejemplo</th><th>Bajo</th><th>Medio</th><th>Alto</th></tr><tr><td>autorizador de acceso [org.4]</td><td><ul><li>accesible a todo el personal propio</li></ul></td><td><ul><li>accesible a los que lo necesitan conocer por sus funciones</li></ul></td><td><ul><li>autorización del organismo a la persona</li></ul></td></tr><tr><td>copias impresas [mp.si]</td><td><ul><li>marcadas</li><li>cada persona se encarga de su destrucción cuando ya no hace falta</li></ul></td><td><ul><li>marcadas</li><li>destrucción usando destructora</li></ul></td><td><ul><li>marcadas</li><li>se lleva un inventario de las copias realizadas</li><li>destrucción procedimentada con actualización del inventario</li></ul></td></tr><tr><td>soportes electrónicos de información [mp.si]</td><td><ul><li>etiquetados</li><li>se borra el contenido o se inhabilita</li></ul></td><td><ul><li>etiquetados</li><li>se cifra el contenido</li><li>se usa software de borrado seguro o se destruye</li></ul></td><td><ul><li>etiquetados</li><li>se cifra el contenido</li><li>se usa software de borrado seguro o se destruye en trituradora homologada</li></ul></td></tr><tr><td>uso en equipos portátiles y PDAs [mp.info.3] [mp.eq.3]</td><td><ul><li>con control de acceso</li></ul></td><td><ul><li>con control de acceso</li></ul></td><td><ul><li>debe estar cifrada en reposo</li></ul></td></tr><tr><td>transmisión telemática [mp.com.2] [mp.com.3]</td><td><ul><li>canales autenticados</li></ul></td><td><ul><li>canales autenticados y cifrados</li></ul></td><td><ul><li>canales autenticados y cifrados</li></ul></td></tr></table>Tabla 5: Ejemplo de criterios de uso de acuerdo con la calificación de la información según categoría del sistema<br/><br/>545. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-001 - Seguridad de las TIC que manejan información nacional clasificada en la Administración</li></ul>546. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>8.1.2 - Propiedad de los activos</li><li>8.2.1 - Clasificación de la información</li></ul></ul>547. NIST SP 800-53 rev.'

obj_573 = '<h3>5.7.3 [MP.INFO.3] CIFRADO</h3>548. Se debe cifrar la información de nivel alto, tanto durante su almacenamiento (mp.si.2) como durante su transmisión (mp.com.2). Sólo estará en claro mientras se está haciendo uso de ella. Esto incluye:<ul style="list-style-type:square"><li>cifrado de ficheros</li><li>cifrado de directorios</li><li>discos virtuales cifrados</li><li>cifrado de datos en bases de datos</li></ul>549. Se debe cifrar la información en función de su calificación y el medio en el que se almacena.<br/><br/>550. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-807 – Criptografía de empleo en el ENS</li><li>Guía CCN-STIC-955 - Recomendaciones empleo GnuPG v 1.4.7</li><li>Guía CCN-STIC-955 B - Recomendaciones empleo GPG</li></ul>551. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>10.1.1 - Política de uso de los controles criptográficos</li><li>14.1.3 - Protección de las transacciones de servicios de aplicaciones</li><li>18.1.5 - Regulación de los controles criptográficos</li></ul></ul>552. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[SC-13] Cryptographic Protection</li><li>[SC-28] Protection of Information at Rest</li></ul>553. Otras referencias:<ul style="list-style-type:square"><li>GNUPG – The GNU Privacy Guard</li><li>PGP – Pretty Good Privacy</li><li>Veracrypt</li></ul>'

obj_574 = '<h3>5.7.4 [MP.INFO.4] FIRMA ELECTRÓNICA</h3>554. Todas las actividades relacionadas con la firma electrónica y el sellado de tiempo deben regirse por un marco técnico y procedimental aprobado formalmente. Se suele denominar Política de Firma.<br/><br/>555. En el caso de que se utilicen otros mecanismos de firma electrónica sujetos a derecho, el sistema debe incorporar medidas compensatorias suficientes que ofrezcan garantías equivalentes o superiores en lo relativo a prevención del repudio.<br/><br/><b>Política de firma electrónica</b><br/><br/>556. Política de firma electrónica. En el caso de la Administración General del Estado, debe cumplir los requisitos establecidos en el artículo 24 del Real Decreto 1671/2009.<br/><br/>557. En todos los casos debe cubrir los siguientes puntos técnicos y procedimentales:<ul style="list-style-type:square"><li>delimitación del ámbito de aplicación; es decir, qué información irá firmada y en qué procesos o procedimientos se firmará y se verificará cada firma</li><li>los roles y funciones del personal involucrado en la generación y verificación de firmas</li><li>los roles y funciones del personal involucrado en la administración de los medios de firma</li><li>los roles y funciones del personal involucrado en la generación, custodia y distribución de claves y certificados</li><li>directrices y normas técnicas aplicables a la utilización de certificados y firmas electrónicas</li><li>los requisitos exigibles a las firmas electrónicas presentadas</li><li>los medios de validación y verificación de firmas: protocolos y prestadores del servicio</li></ul>558. En la Administración General del Estado se dispone de un marco de referencia.<br/>Ver http://administracionelectronica.gob.es/es/ctt/politicafirma<br/><br/>559. La política de firma debe cumplir los requisitos del Esquema Nacional de Interoperabilidad.<br/><br/>560. En cualquier escenario se debe buscar una interoperabilidad de las firmas electrónicas por lo que se recomienda fuertemente que los organismos referencien la política de firma de electrónica de un órgano superior y sólo en muy contadas ocasiones se establezca una política independiente.<br/><br/><b>Uso de claves concertadas para firmar</b><br/><br/>561. La firma con un secreto compartido requiere algunas cautelas.<br/><br/>562. Lo más que podemos hacer es:<ul style="list-style-type:square"><li>presentarle la información al ciudadano en una página web</li><li>pedirle que introduzca la clave de firma (sin memoria: hay que introducirla expresamente)</li><li>conservar como evidencia el HMAC23 (documento + clave_concertada)</li></ul>563. Este mecanismo garantiza la integridad del documento e identifica al ciudadano; pero no garantiza el no-repudio ya que cualquiera que puede verificar la firma, puede también generarla. Es decir, no cumple los requisitos de una firma electrónica avanzada, que requiere que “haya sido creada por medios que el firmante puede mantener bajo su exclusivo control” (Ley 59/2003).<br/><br/>564. Se considerará firma electrónica, sin más.<br/><br/><b>Código seguro de verificación</b><br/><br/>565. Se trata de una forma alternativa de asegurar la autenticidad e integridad de la información proporcionada por la Administración.<br/><br/>566. En lugar de proteger la información por medio de una firma inviolable, lo que se proporciona es una forma cómoda de verificar que la información es auténtica y no se ha modificado (es íntegra).<br/><br/>567. El sistema de código seguro de verificación (CSV) deberá garantizar, en todo caso:<ul style="list-style-type:square"><li>El carácter único del código generado para cada documento.</li><li>Su vinculación con el documento generado y con el firmante.</li><li>Asimismo, se debe garantizar la posibilidad de verificar el documento por el tiempo que se establezca en la resolución que autorice la aplicación de este procedimiento.</li></ul>568. La Administración queda obligada a:<ul style="list-style-type:square"><li>garantizar la disponibilidad del mecanismo de verificación</li><li>garantizar la integridad del documento referenciado</li><li>garantizar la confidencialidad del documento correspondiente; por ejemplo, controlando el acceso para que sólo accedan las personas autorizadas</li></ul>569. Una forma fácil de proporcionar CSVs es usar un número consecutivo en un archivo documental identificado (lo que sería una clave primaria en una base de datos documental). Al ciudadano hay que proporcionarle la identificación del archivo y el número de expediente.<br/><br/>570. Una forma fácil de cumplir los requisitos de autenticidad e integridad es que el documento referenciado por medio del CSV, sea en sí mismo un documento firmado electrónicamente. De esta forma, el ciudadano (o cualquier tercera parte autorizada) puede en cualquier momento recabar el documento y conservarlo en su poder.<br/><br/><b>Integridad o autenticidad: nivel ALTO</b><br/><br/>577. Se usa una firma electrónica cualificada, que incorpora certificados cualificados y dispositivos cualificados de creación de firma.<br/><br/>578. Se emplean productos certificados, conforme a lo establecido en [op.pl.5].<br/><br/>579. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-807 – Criptografía de empleo en el ENS</li><li>Guía CCN-STIC-405 - Algoritmos y Parámetros de Firma Electrónica</li></ul>580. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>10.1.1 - Política de uso de los controles criptográficos</li><li>14.1.3 - Protección de las transacciones de servicios de aplicaciones</li><li>18.1.5 - Regulación de los controles criptográficos</li></ul></ul>581. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[SC-13] Cryptographic Protection</li><li>[SC-28] Protection of Information at Rest</li></ul>582. Otras referencias:<ul style="list-style-type:square"><li>Reglamento (UE) 910/2014, del Parlamento Europeo y el Consejo, de 23 de julio de 2014, relativo a la identificación electrónica (eID) y los servicios de confianza para transacciones electrónicas en el mercado interior y por la que se deroga la Directiva 1999/93/CE</li><li>Real Decreto 1671 de 2009</li><li>IST SP 800-89 - Recommendation for Obtaining Assurances for Digital Signature Applications</li><li>Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas.</li><li>Ley 40/2015, de 1 de octubre, de Régimen Jurídico del Sector Público.</li><li>Real Decreto 1065/2007, de 27 de julio, por el que se aprueba el Reglamento General de las actuaciones y los procedimientos de gestión e inspección tributaria y de desarrollo de las normas comunes de los procedimientos de aplicación de los tributos.</li></ul>'

obj_575 = '<h3>5.7.5 [MP.INFO.5] SELLOS DE TIEMPO</h3>583. Los sellos de tiempo previenen la posibilidad de un repudio posterior de la información que sea susceptible de ser utilizada como evidencia en el futuro, o que requiera capacidad probatoria según la ley de procedimiento administrativo. Por ello, todas las actividades relacionadas con la firma electrónica y el sellado de tiempo deben regirse por un marco técnico y procedimental aprobado formalmente. Se suele denominar Política de Firma.<br/><br/>584. Debe identificarse y establecerse el tiempo de retención de la información.<br/><br/>585. Se fechan electrónicamente los documentos cuya fecha y hora de entrada debe acreditarse fehacientemente.<br/><br/>586. Se fechan electrónicamente los documentos cuya fecha y hora de salida debe acreditarse fehacientemente.<br/><br/>587. Se fechan electrónicamente las firmas cuya validez deba extenderse por largos periodos o así lo exija la normativa aplicable, hasta que la información protegida ya no sea requerida por el proceso administrativo al que da soporte; alternativamente se pueden utilizar formatos de firma avanzada que incluyan fechado.<br/><br/>588. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-807 Criptografía de empleo en el ENS</li></ul>589. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>14.1.3 - Protección de las transacciones de servicios de aplicaciones</li></ul></ul>590. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[AU-10] Non-repudiation</li><br/><li>ISO/IEC 18014-1:2008<br/>Information technology – Security techniques – Time-stamping services –<br/>Part 1: Framework</li><br/><li>ISO/IEC 18014-2:2009<br/>Information technology – Security techniques – Time-stamping services –<br/>Part 2: Mechanisms producing independent tokens</li><br/><li>ISO/IEC 18014-3:2009<br/>Information technology – Security techniques – Time-stamping services –<br/>Part 3: Mechanisms producing linked tokens</li><br/><li>ISO/IEC TR 29149:2012<br/>Information technology – Security techniques –<br/>Best practices for the provision and use of time-stamping services</li><br/><li>RFC 3161 Internet X.509 Public Key Infrastructure Time-Stamp Protocol (TSP)</li><br/><li>Ley 39/2015, de 1 de octubre, de Procedimiento Administrativo Común de las Administraciones Públicas.</li><br/><li>Ley 40/2015, de 1 de octubre, de Régimen Jurídico del Sector Público.</li></ul>'

obj_576 = '<h3>5.7.6 [MP.INFO.6] LIMPIEZA DE DOCUMENTOS</h3>591. Se debe retirar de los documentos que van a ser trasferido a un ámbito fuera del dominio de seguridad toda la información adicional contenida en campos ocultos, meta-datos, comentarios, revisiones anteriores, etc. salvo cuando dicha información sea pertinente para el receptor del documento.<br/><br/>592. Esta medida es especialmente relevante cuando el documento se difunde ampliamente, como ocurre cuando se ofrece al público en un servidor web u otro tipo de repositorios de información.<br/><br/>593. El incumplimiento de esta medida puede perjudicar:<ul style="list-style-type:square"><li>al mantenimiento de la confidencialidad de información que no debería haberse revelado al receptor del documento</li><li>al mantenimiento de la confidencialidad de las fuentes u orígenes de la información, que no debe conocer el receptor del documento</li><li>a la buena imagen de la organización que difunde el documento por cuanto demuestra un descuido en su buen hacer</li></ul>594. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-835 Borrado de metadatos en el marco del ENS</li></ul>595. NIST SP 800-53 rev. 4'

obj_577 = '<h3>5.7.7 [MP.INFO.7] COPIAS DE SEGURIDAD (BACKUP)</h3>596. Se deben realizar copias de respaldo que permitan recuperar datos perdidos accidental o intencionadamente con una antigüedad a determinar por la organización.<br/><br/>597. Las copias de respaldo poseerán el mismo nivel de seguridad que los datos originales en lo que se refiere a integridad, confidencialidad, autenticidad y trazabilidad. En particular, debe considerarse la conveniencia o necesidad de que las copias de seguridad estén cifradas para garantizar la confidencialidad (en cuyo caso se estará a lo dispuesto en [op.exp.11]).<br/><br/>598. Se recomienda establecer un proceso de autorización para la recuperación de información de las copias de respaldo.<br/><br/>599. Se recomienda conservar las copias de respaldo en lugar(es) suficientemente independiente(s) de la ubicación normal de la información en explotación como para que los incidentes previstos en el análisis de riesgos no se den simultáneamente en ambos lugares, por ejemplo, si se conservan en la misma sala utilizar un armario ignífugo.<br/><br/>600. El transporte de copias de respaldo desde el lugar donde se producen hasta su lugar de almacenamiento garantiza las mismas seguridades que los controles de acceso a la información original.<br/><br/>601. Las copias de respaldo deben abarcar:<ul style="list-style-type:square"><li>información de trabajo de la organización</li><li>aplicaciones en explotación, incluyendo los sistemas operativos</li><li>datos de configuración, servicios, aplicaciones, equipos, etc.</li><li>claves utilizadas para preservar la confidencialidad de la información</li></ul>602. Para los puntos anteriores ver [op.exp] y [mp.info.3].<br/><br/>603. El responsable de la información debe determinar la frecuencia con la que deben realizarse las copias y el periodo de retención durante el que mantenerlas.<br/><br/>604. En caso de disponer de un Plan de Continuidad, las copias de seguridad deberán realizarse con una frecuencia que permita cumplir con el RPO y con un objetivo de tiempo de restauración que permita cumplir el RTO.<br/><br/>605. Se recomienda realizar periódicamente pruebas de restauración de copias de seguridad.<br/><br/>606. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>12.3.1 - Copias de seguridad de la información</li></ul></ul>607. NIST SP 800-53 rev4:<ul style="list-style-type:square"><li>[CP-6] Alternate Storage Site</li><li>[CP-9] Information System Backup</li><li>[CP-10] Information System Recovery and Reconstitution</li></ul>608. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.10 - Data Recovery Capability</li></ul></ul>'

obj_581 = '<h3>5.8.1 [MP.S.1] PROTECCIÓN DEL CORREO ELECTRÓNICO (E-MAIL)</h3>609. Cuando se ofrezca correo electrónico como parte del sistema, deberá protegerse frente a las amenazas que le son propias mediante:<ul style="list-style-type:square"><li>Protección del cuerpo de los mensajes y documentos adjuntos que pueda contener el correo electrónico</li><li>Protección del encaminamiento de mensajes (por ejemplo, protegiendo el servidor DNS y su configuración) y del establecimiento de las conexiones (impidiendo que el usuario final pueda conectarse a un servidor de correo que no sea el corporativo)</li><li>Protección de la organización frente a correos no solicitados (spam), virus, gusanos, troyanos, programas espías (spyware) y código móvil tipo applet (por ejemplo, con la instalación de un antivirus, ya sea en el servidor de correo o en el puesto de usuario)</li><li>Limitación del uso del correo electrónico al estrictamente profesional y concienciación y formación relativas al uso adecuado del mismo</li></ul>610. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-681 – Configuración segura de servidores de correo Postfix</li><li>Guía CCN-STIC-682 – Configuración segura de Sendmail</li><li>Guía CCN-STIC-814 – Seguridad en Correo electrónico</li></ul>611. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>13.2.3 - Mensajería electrónica</li></ul></ul>612. NIST 800-53 rev. 4<ul style="list-style-type:square"><li>[SI-8] Spam Protection</li></ul>613. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.7 - Email and Web Browser Protections</li></ul><li>NIST SP 800-45 – Guidelines on Electronic Mail Security</li></ul>'

obj_582 = '<h3>5.8.2 [MP.S.2] PROTECCIÓN DE SERVICIOS Y APLICACIONES WEB</h3>614. Se debe proteger a los subsistemas dedicados a la publicación de información frente a los ataques o amenazas que les son propias.<br/><br/>615. Una serie de medidas son preventivas, poniendo el énfasis en los procesos de<ul style="list-style-type:square"><li>desarrollo de aplicaciones y servicios (mp.sw),</li><li>configuración de seguridad (op.exp.2 y op.exp.3),</li><li>en los controles de mantenimiento (op.exp.4) y</li><li>en las protecciones de separación de tareas (op.acc.3).</li></ul>616. Las tareas preventivas no excusan de un sistema de monitorización y reacción frente a ataques exitosos.<br/><br/>617. Pueden presentarse ataques a nivel de red, a nivel del sistema operativo del servidor y a nivel de la aplicación que atiende a peticiones web. De los dos primeros modos de ataque nos defenderemos protegiendo el equipo de frontera.<br/><br/>618. Básicamente hay 2 formas de proteger el servidor frontal: protegiendo el equipo y el software que proporciona la interfaz para acceso al servicio web, o disponiendo una protección previa en forma de cortafuegos de aplicación (appliance) entre el servidor y los usuarios.<br/><br/>619. Los ataques a nivel de aplicación pueden detectarse en el servidor frontal o en algún servidor de soporte en la retaguardia; es decir, puede haber ataques que aparecen como correctos (sintácticamente correctos) pero que causan problemas por el tipo de petición o por la secuencia de peticiones (semántica incorrecta). Para los ataques que entran en el nivel interno será necesario desarrollar reglas específicas para detectar y reaccionar. Reglas de tipo:<ul style="list-style-type:square"><li>límite en el número de sesiones, total o por usuario anónimo o identificado</li><li>cierre de sesiones al cabo de un tiempo</li><li>límite en el volumen de datos (individual y agregado)</li></ul>620. Para verificar que en el proceso de desarrollo de la aplicación se han establecido los controles frente a ataques potenciales se deben identificar posibles vulnerabilidades a corregir. Para ello se pueden realizar auditorías de seguridad periódicas o pruebas de penetración (hacking ético) de los servicios y aplicaciones web para posteriormente modificar el aplicativo o establecer elementos que lo protejan al menos frente a:<ul style="list-style-type:square"><li>Ataques que eviten el control de acceso obviando la autenticación, si la hubiera, mediante accesos por vías alternativas al protocolo predefinido (por ejemplo, HTTP y HTTPS, manipulaciones de URL o cookies o ataques de inyección de código (como introducir caracteres no autorizados por la aplicación).</li><li>Ataques de escalado de privilegios (como ejecutar acciones haciéndose pasar por otro usuario).</li><li>Ataques de Cross Site Scripting (XSS) que permiten robar información delicada, secuestrar sesiones de usuario o comprometer la integridad del sistema (introduciendo información en la página web que se muestre así posteriormente al usuario, por ejemplo).</li><li>Ataques de manipulación de proxies y cachés, en caso de utilizar estas tecnologías.</li></ul>621. Guías CCN-STIC:<ul style="list-style-type:square"><li>Serie CCN-STIC-500 - Guías para Entornos Windows</li><li>Serie CCN-STIC-600 - Guías para otros Entornos</li><li>Guía CCN-STIC-812 - Seguridad en entornos y aplicaciones Web</li></ul>622. ISO/IEC 27000<ul style="list-style-type:square"><li>27002:2013:</li><ul style="list-style-type:circle"><li>14.1.2 - Asegurar los servicios de aplicaciones en redes públicas</li></ul></ul>623. NIST SP 800-53 rev. 4<br/><br/>624. Otras referencias:<ul style="list-style-type:square"><li>SANS - CIS Critical Security Controls - Version 6.1</li><ul style="list-style-type:circle"><li>CSC.7 - Email and Web Browser Protections</li></ul><li>NIST SP 800-44 - Guidelines on Securing Public Web Servers</li><li>PCI-DSS v3.0</li><ul style="list-style-type:circle"><li>Requisito 6: Desarrolle y mantenga sistemas y aplicaciones seguras</li></ul></ul>'

obj_583 = '<h3>5.8.3 [MP.S.3] PROTECCIÓN FRENTE A LA DENEGACIÓN DE SERVICIO</h3>625. Se deben establecer medidas preventivas y reactivas frente a ataques de denegación de servicio (DoS).<br/><br/>626. Los ataques de denegación de servicio pueden prevenirse dimensionando con holgura los elementos susceptibles de ser atacados desde el exterior, aunque poco se puede hacer frente a un ataque con suficientes recursos por parte del atacante.<br/><br/>627. Múltiples ataques de denegación de servicio son facilitados por un software deficiente por parte del servidor, bien porque no se han actualizado las versiones, bien porque la configuración no es idónea. Ambos aspectos deberán ser analizados y reparados (ver medidas de protección [mp.exp] en lo relativo a configuración, mantenimiento y cambios), de modo que se actualicen y bastionen las tecnologías utilizadas de cara a prevenir ataques conocidos.<br/><br/>628. Aun estando preparados, podemos ser víctimas de un nuevo tipo de ataque imprevisto, en cuyo caso hay que detectarlo rápidamente y gestionar la incidencia.<br/><br/>629. Los ataques de denegación de servicio pueden ser detectados y afrontados en el perímetro ([mp.com.1]), aunque pueden requerir la intervención de otros elementos. En el perímetro se pueden detectar patrones sospechosos de comportamiento: avalanchas de peticiones, peticiones trucadas y, en general, un uso malicioso de los protocolos de comunicaciones. Algunas de estas peticiones pueden ser denegadas directamente por el equipo perimetral, en otras ocasiones hay que reaccionar ante ellos y levantar una alarma para actuar en donde corresponda (servidores web, servidores de bases de datos…, y contactando con el proveedor de comunicaciones o los centros de respuesta a incidentes, CERT). Por tanto, es importante disponer de un procedimiento documentado que indique el procedimiento de reacción ante los ataques.<br/><br/>630. Es responsabilidad del organismo detectar y bloquear el uso deliberado o accidental del propio sistema de información para atacar a terceros desde las propias instalaciones. Nótese que el organismo puede ser simplemente víctima de una infección dañina de elementos agresivos que son lanzados contra otros o de un ataque deliberado por parte de un empleado interno y al proveedor de comunicaciones o al centro de respuesta de emergencia (CERT) para coordinar la respuesta.<br/><br/>631. Como posibles tecnologías a utilizar para prevenir ataques se encuentran los sistemas de detección de intrusos (IDS), monitores con alarmas al alcanzar un consumo determinado de ancho de banda o de solicitud de peticiones, mecanismos para bloquear un número elevado de conexiones internas concurrentes o para bloquear el envío de grandes cantidades de información, etc.<br/><br/>632. Guías CCN-STIC:<ul style="list-style-type:square"><li>Guía CCN-STIC-820 – Guía de protección contra Denegación de Servicio</li></ul>633. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>12.1.3 - Gestión de capacidades</li></ul></ul>634. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP-2] (2) Contingency Plan - Capacity Planning</li><li>[SC-5] (2) Denial of Service Protection - Excess Capacity / Bandwidth / Redundancy</li></ul>'

obj_584 = '<h3>5.8.4 [MP.S.4] MEDIOS ALTERNATIVOS</h3>635. Se debe prever medios alternativos para ofrecer los servicios en el caso de que fallen los medios habituales, mientras se recupera la disponibilidad de éstos (como por ejemplo una instancia alternativa a un portal). Estos medios alternativos estarán sujetos a las mismas garantías de protección.<br/><br/>636. Se debe establecer un tiempo máximo para que los servicios alternativos entren en funcionamiento.<br/><br/>637. Los servicios alternativos pueden estar dispuestos para entrar en servicio inmediatamente o requerir un tiempo de personalización. En todo caso, el tiempo de entrada en servicio debe estar respaldado por un análisis de impacto (ver [op.cont.1]).<br/><br/>638. El plan de utilización de servicios alternativos se vertebrará dentro del plan de continuidad aprobado (ver [op.cont.2]) y ser objeto de pruebas regulares para validar la viabilidad del plan (ver [op.cont.3]).<br/><br/>639. ISO/IEC 27000<ul style="list-style-type:square"><li>ISO/IEC 27002:2013:</li><ul style="list-style-type:circle"><li>17.2.1 - Disponibilidad de los recursos de tratamiento de la información</li></ul></ul>640. NIST SP 800-53 rev. 4<ul style="list-style-type:square"><li>[CP] Contingency Planning</li></ul>'

data = 'INSERT INTO ENS' + '\n' + '(id, pm_list)' + '\n' + 'values' + '\n' + '(511, \'' + obj_511 + '\'),' + '\n' + '(512, \'' + obj_512 + '\'),' + '\n'\
       + '(513, \'' + obj_513 + '\'),' + '\n' + '(514, \'' + obj_514 + '\'),' + '\n' + '(515, \'' + obj_515 + '\'),' + '\n' + '(516, \'' + obj_516 + '\'),' + '\n'\
	   + '(517, \'' + obj_517 + '\'),' + '\n' + '(518, \'' + obj_518 + '\'),' + '\n' + '(521, \'' + obj_521 + '\'),' + '\n' + '(522, \'' + obj_522 + '\'),' + '\n'\
	   + '(523, \'' + obj_523 + '\'),' + '\n' + '(524, \'' + obj_524 + '\'),' + '\n' + '(525, \'' + obj_525 + '\'),' + '\n' + '(531, \'' + obj_531 + '\'),' + '\n'\
	   + '(532, \'' + obj_532 + '\'),' + '\n' + '(533, \'' + obj_533 + '\'),' + '\n' + '(534, \'' + obj_534 + '\'),' + '\n' + '(541, \'' + obj_541 + '\'),' + '\n'\
	   + '(542, \'' + obj_542 + '\'),' + '\n' + '(543, \'' + obj_543 + '\'),' + '\n' + '(544, \'' + obj_544 + '\'),' + '\n' + '(545, \'' + obj_545 + '\'),' + '\n'\
	   + '(551, \'' + obj_551 + '\'),' + '\n' + '(552, \'' + obj_552 + '\'),' + '\n' + '(553, \'' + obj_553 + '\'),' + '\n' + '(554, \'' + obj_554 + '\'),' + '\n'\
	   + '(555, \'' + obj_555 + '\'),' + '\n' + '(561, \'' + obj_561 + '\'),' + '\n' + '(562, \'' + obj_562 + '\'),' + '\n' + '(571, \'' + obj_571 + '\'),' + '\n'\
	   + '(572, \'' + obj_572 + '\'),' + '\n' + '(573, \'' + obj_573 + '\'),' + '\n' + '(574, \'' + obj_574 + '\'),' + '\n' + '(575, \'' + obj_575 + '\'),' + '\n'\
	   + '(576, \'' + obj_576 + '\'),' + '\n' + '(577, \'' + obj_577 + '\'),' + '\n' + '(581, \'' + obj_581 + '\'),' + '\n' + '(582, \'' + obj_582 + '\'),' + '\n'\
	   + '(583, \'' + obj_583 + '\'),' + '\n' + '(584, \'' + obj_584 + '\');' + '\n'
		
#print data


# Una vez se cuenta con el contenido de todos los registros de la tabla ENS, se vuelca en un fichero .sql para su procesado posterior:
ens_table = open ('ens_table.sql','w')	# Se crea el archivo.
ens_table.write(data)					# Se escribe el contenido.
ens_table.close()						# Por último, se cierra, haciendo efectivos los cambios.

# A continuación, se extrae la descripción de los objetivos de seguridad. Se necesitará para generar los datos de la tabla INCIDENTS:

pat = re.compile('<h3>.*</h3>')

objs = pat.findall(data)

for i in range(len(objs)):
        objs[i] = objs[i].replace("<h3>","")
        objs[i] = objs[i].replace("</h3>","")

#print objs	# Se comprueba que se extraen correctamente.

#objs_f = open ('Objetivos.txt','w')	# Se crea el archivo.
#objs_f.write(objs[10])			# Se escribe el contenido.
#objs_f.close()				# Por último, se cierra, haciendo efectivos los cambios.

		
			# GENERACIÓN DE LA TABLA INCIDENTS:
	
# La tabla INCIDENTS contiene los siguientes campos:
## INSERT INTO INCIDENTS
## (id, originator, type, description, area, accountable, csirt, id_csirt, detect_date, notify_date, severity, dimensions, status, reports, details, pm_info, false_p, false_n) 

# Se incluye algunos ejemplos de inserción de datos de prueba:

## INSERT INTO INCIDENTS
## (id, originator, type, description, area, accountable, csirt, id_csirt, detect_date, notify_date, severity, dimensions, status, reports, details, pm_info, false_p, false_n) 
## values
## (20180001, 'SIEM', 552, 'Acceso no autorizado servidor BBDD.', 'Datos centrales.', 'davgonvaz', 'S', 201805, '12/08/2018 18:37', '12/08/2018 18:39', 'C', 'CI', 'U', '', '', '5521 Bla bla bla1.**N//5522Bla bla bla2.**N//5523Bla bla bla3.**N]]', 'N', 'N'),
## (20180002, 'blachimar', 448, 'Acceso no autorizado servidor web.', 'Datos centrales.', 'blachimar', 'S', 201804, '11/08/2018 18:37', '11/08/2018 18:39', 'C', 'CI', 'A', '', '', '4481 Bla bla bla1.**NEn pruebas.//4482Bla bla bla2.**NSe aplicará el 14 de agosto.//4483Bla bla bla3.**SAplicado satisfactoriamente.]]', 'N', 'N'),
## (20180003, 'SIEM', 326, 'Caída servidor web #1.', 'DMZ.', 'artgaldel', 'S', 201802, '10/08/2018 08:19', '10/08/2018 08:20', 'A', 'D', 'A', '', '', '3261 Bla bla bla1.**SAplicada satisfactoriamente.//3262Bla bla bla2.**NPendiente estudio.//3263Bla bla bla3.**NPendiente aplicar 3262.]]', 'N', 'N'),
## (20180004, 'SIEM', 431, 'Ficheros corruptos servidor impresión.', 'Servicios de apoyo.', 'davgonvaz', 'N', 0, '08/08/2018 09:46', '', 'B', 'I', 'A', '', '', '4311 Bla bla bla1.**N//4312Bla bla bla2.**N//4313Bla bla bla3.**N]]', 'S', 'N'),
## (20180005, 'SIEM', 453, 'Caída firewall #3.', 'Servicios de apoyo.', 'SIEM', 'N', 0, '13/08/2018 14:06', '', 'M', 'I', 'U', '', '', '4531 Bla bla bla1.**N//4532Bla bla bla2.**N//4533Bla bla bla3.**N]]', 'N', 'N');

## Antes de pasar a ver el código, conviene revisar los criterios elegidos para generar los datos, de esta manera se entenderá la manera de proceder
## en la implementación.

## id:
## Respecto al año, se generarán incidentes en el periodo 2015<->2018, con una media de 130 incidencias al año => bucle externo de 4 iteraciones, y bucle interno
## de 130 +/- [0<->20]. Se generarán 4 valores aleatorios de media 130 y desviación +/- [0<->20] -> simbolizarán las incidencias a generar para cada uno de los 4 años.
## Se controlará el año actual teniendo en cuenta el tiempo transcurrido y no generar más allá de la fecha actual!

## originator:
## Al disponer de un sistema SIEM, es de suponer que la mayoría de detecciones se darán gracias a él, ya que trabaja de manera automática e ininterrumpidamente.
## Habría que tener en cuenta también los falsos positivos/negativos, pero de cara a la generación de datos de prueba y de prueba de funcionalidad de la BBDD,
## ello no influye. Este detalle sí se tendrá en cuenta de cara a las estadísticas.
## Se establecerá un reparto de un 80/20%.

## type, description:
## Lista MP -> de 5.1.1 a 5.1.8, 5.2.1 a 5.2.5, 5.3.1 a 5.3.4, 5.4.1 a 5.4.5, 5.5.1 a 5.5.5, 5.6.1 a 5.6.2, 5.7.1 a 5.7.7 y 5.8.1 a 5.8.4 => 511 a 584. Distribución aleatoria.
## Generar lista con el valor (sin puntos .): 511, 512, ...
## => Total: 40 objetivos de seguridad => generar número aleatorio [0,39] para elegir MP al azar!
## Generar lista con los 40 objetivos => el valor aleatorio anterior servirá de índice para extraer el texto (4º campo de la tabla).

ens_id_obj = ['511', '512', '513', '514', '515', '516', '517', '518', '521', '522', '523', '524', '525', '531', '532', '533', '534', '541',\
'542', '543', '544', '545', '551', '552', '553', '554', '555', '561', '562', '571', '572', '573', '574', '575', '576', '577', '581', '582',\
'583', '584']

ens_descrip = objs	# Ya se extrajo anteriormente al generar la tabla ENS.

## area:
## Generar algunas areas y seleccionar de manera aleatoria para cada registro. Por ejemplo: 5 areas => número aleatorio [1,5].

## accountable:
## Tal como se refleja en la documentación del trabajo, si el originador ha sido el sistema SIEM, y la nueva incidencia
## aún no ha sido revisada por un analista, en el campo accountable aparecerá el código de usuario de una persona responsable de seguridad
## elegida al azar entre el personal en activo, y la incidencia quedará en estado de cuarentena ('U').
## Por tanto, lo que se hará es asignar un responsable de manera aleatoria, de la siguiente manera:
## a) Si el originador es el sistema SIEM, se seleccionará un responsable de seguridad de manera aleatoria siguiendo el procedimiento aplicado anteriormente.
## b) Si el originador es personal de seguridad (alta manual), por lo general será la misma persona que se haga responsable, pero
## esto no tiene porqué darse en el 100% de los casos. Se supondrá una coincidencia del 80%.
## c) En cualquier caso, en el caso de conformarse un equipo de respuesta, el responsable será la persona que aparezca en primera lugar en el CSIRT.

## severity:
## Se distribuirá de manera aleatoria, teniendo en cuenta que las incidencias más graves es normal que ocurran con menor frecuencia, y las de menor severidad
## se produzcan más habitualmente. El reparto será el siguiente:
## Críticas: 5%.
## Altas: 10%.
## Medias: 30%.
## Bajas: 55%.
## Se utilizará un generador aleatorio en el rango [1,100]: 1<->5, 6<->15, 16<->45 y 46<->100.

## csirt:
## Si la incidencia es detectada por el SIEM y la severidad es Crítica, se conforma un csirt automáticamente.
## Teniendo en cuenta que el SIEM detectará el 80% de las incidencias y que de ellas, el 5% se estiman críticas: 0,8 x 0,05 = 0,04.
## Por otro lado, en el caso del alta manual de incidencias: 20%, de las cuales el 5% se estiman críticas. De ellas, se estima que para el 70%
## se hace necesario asignar un equipo de respuesta: 0,2 x 0,05 x 0,7 = 0,007.
## En total, hay una probabilidad de 0,047 de que se conforme un CSIRT.
## Para facilitar el cálculo y cuándo activar un equipo de respuesta, se analizará de la siguiente manera:
## Del 80% de detecciones procedentes del SIEM, el 5% son críticas, y de ellas, todas generan un CSIRT.
## Del 20% de detecciones manuales, el 70% genera un CSIRT.
## => En total, de las incidencias clasificadas como 'C', generan un CSIRT: 0,8 x 1 + 0,2 x 0,7 = 0,94.

## id_csirt:
## En realidad, primero se conformaría un equipo de respuesta, se registraría en la tabla CSIRT y a continuación se añadiría la ID al campo
## INCIDENTS.id_csirt. Esta sería la manera de funcionar de la plataforma web de gestión de incidencias.
## De cara a la generación de datos de prueba, conforme se vayan generando equipos asociados a las nuevas incidencias que se van registrando,
## se irán insertando los datos respectos tanto en la tabla INCIDENTS como en la tabla CSIRT.

## csirt_team:  (en realidad es un campo de la tabla CSIRT, pero lo generamos ahora para cuando se rellene la tabla CSIRT)
## También se puede conformar un equipo de respuesta de manera manual, siempre y cuando la incidencia tenga una severidad Crítica.
## 		Generación de datos para el campo csirt_team:
## Un equipo de respuesta (CSIRT) se puede conformar de 2 maneras:
## a) de manera manual, por personal responsable de seguridad. En ese caso, a la hora de registrar el alta de la nueva incidencia, se permitirá
## confeccionar un equipo de respuesta. De manera automática, la aplicación web propondrá 3 personas para formar un CSIRT entre el personal
## en activo, y que tenga menos participaciones en equipos de respuesta. El personal responsable de seguridad que esté realizando el alta de
## la incidencia y conformando el CSIRT también tendrá la posibilidad de seleccionar de entre el personal en activo de manera manual.
## b) de manera automática, si es el sistema SIEM el que detecta una incidencia de categoría crítica. En ese caso se seleccionará el personal
## que integra el CSIRT de manera automática entre el personal de seguridad en activo. No obstante, la incidencia quedará en estado de cuarentena
## ('U') hasta la revisión por parte del personal de seguridad. El analista que se encargue de supervisar la incidencia podrá realizar
## modificaciones, si se estima necesario.

## De cara a la generación de datos de prueba, en aquellos casos en que se haya conformado un CSIRT, se escogerán 3 personas de manera aleatoria
## de entre el personal responsable de seguridad en activo.
## Se mantendrá el contador de equipos CSIRT's generados para mantener la secuencia dentro de cada año.

## detect_date, notify_date:
## La fecha de detección se generará de tal manera que se vayan distribuyendo las incidencias generadas a lo largo de cada año.
## Se parte del número de incidencias a generar para cada año. Se divide entre 12. El número resultante ("resultado") indica las incidencias a generar para cada mes: 
## se recorre cada uno de los 12 meses, para cada uno de ellos se generan "resultado" números entre [1,max_dias(mes)]: [1,31] para enero, [1,28] para febrero...
## La fecha de notificación afectará solo a incidencias de severidad Crítica y Alta, ya que sólo en estos casos generarán notificación.
## La notificación se realiza de manera automática por correo electrónico (¿otra vía adicional?) en cuanto se detecta una incidencia. En el caso de dar de alta la
## incidencia de manera manual, se da la potestad al personal de seguridad de ejecutar notificación o no desde el interfaz web.
## En cualquier caso, de realizarse, la notificación es casi inmediata, por lo que se generará la fecha de notificación a partir de la fecha de detección, sin más que
## añadir un pequeño desfase aleatorio de unos 5 minutos random[1<->5], por ejemplo.

## dimensions:
## Las dimensiones de seguridad vendrán determinadas, o bien por el sistema SIEM en función de lo que haya detectado y concluido, o bien indicadas de manera manual
## en el caso del alta por parte del personal de seguridad responsable.
## Recordar que es un campo editable durante el ciclo de vida de la incidencia.
## El determinar de manera correcta las dimensiones de seguridad es un indicativo de la calidad de detección por parte del sistema SIEM, o bien de la
## calidad de gestión por parte del personal de seguridad, por lo que es un factor de calidad importante a tener en cuenta.
## De cara a la generación de datos para las pruebas, se generará de manera aleatoria.

## status:
## Se considerarán [C]erradas el 100% de las incidencias para los años 2015 y 2016, el 90% para 2017 y el 75% para 2018.
## Se considerarán en c[U]arentena 5% de incidencias del año 2017 (ejemplo de lo que podría ser quedar pendiente de resolver por diversos motivos), 12% del año 2018
## debido a que, o bien están recién detectadas pendientes de estudio, o bien pendientes de otros motivos. 0 incidencias en cuarentena para los años anteriores.
## El resto de incidencias permanecerán en estado [A]biertas.

## reports:
## En algunas de las incidencias se añadirá la existencia de informes según el formato establecido por diseño:
## “Enlace a documento #1” // “Enlace a documento #2” // … ]]
## Los informes se debe a situaciones especiales donde se necesita anexar documentación que no se puede recoger en el campo de detalles utilizado durante
## el ciclo de vida de la incidencia, o bien por la especial criticidad de la incidencia, dificultad en la resolución, necesidad de documentación de referencia, etc.
## Se considerá que un 20% de las incidencias cuentan con informes anexos.
## De cara a la generación de datos de prueba, se construirá una lista cerrada de enlaces online a documentos de referencia generales, como documentación del CCN,
## por ejemplo:
reports_list = ['https://www.ccn-cert.cni.es/series-ccn-stic/800-guia-esquema-nacional-de-seguridad/505-ccn-stic-804-medidas-de-implantancion-del-ens',\
'https://www.ccn-cert.cni.es/series-ccn-stic/800-guia-esquema-nacional-de-seguridad/502-ccn-stic-802-auditoria-del-ens',\
'https://www.ccn-cert.cni.es/series-ccn-stic/800-guia-esquema-nacional-de-seguridad/518-ccn-stic-808-verificacion-del-cumplimiento-de-las-medidas-en-el-ens-borrador',\
'https://www.ccn-cert.cni.es/series-ccn-stic/800-guia-esquema-nacional-de-seguridad/2728-ccn-stic-831-registro-de-la-actividad-de-los-usuarios',\
'https://www.ccn-cert.cni.es/series-ccn-stic/800-guia-esquema-nacional-de-seguridad/1279-ccn-stic-809-declaracion-de-conformidad-con-el-ens',\
'https://www.ccn-cert.cni.es/pdf/guias/series-ccn-stic/guias-de-acceso-publico-ccn-stic/2913-ccn-stic-496-sistemas-de-comunicaciones-moviles',\
'https://www.ccn-cert.cni.es/pdf/guias/series-ccn-stic/guias-de-acceso-publico-ccn-stic/2901-ccn-stic-453d-seguridad-de-dispositivos-moviles-android-6-x']

## details:
## Se trata de recoger en forma de texto plano detalles que el personal de seguridad responsable va anotando a lo largo de la resolución de la incidencia y, en general,
## a lo largo del todo el ciclo de vida de la misma. Realmente es simplemente un campo de texto estructurado en párrafos.
## Se generarán distintos listados de campos de texto de ejemplo para utilizar. Habrá que generar listados según el estado de cada incidencia:
## a) [C]errada: contendrán notas recogidas a lo largo del ciclo de vida de la incidencia y la anotación final del cierre de la misma.
## b) c[U]arentena: se separará a su vez en 2 listados: las incidencias procedentes del SIEM pendientes de estudiar por un analista; y las que permanecen en cuarentena
## por estar pendientes de la resolución de otras incidencias o bien de otras circunstancias (pendiente de equipamiento, pendiente de desarrollo, etc.).
## Para poder hacer una distintición entre estos dos casos:
## 	b.1) se supone que el 100% de las incidencias que se encuentran en cuarentena del año 2017 es debido a estar pendiente de resolución.
##	b.2) se supone que el 80% de las incidencias que se encuentran en cuarentena del año 2018 es debido a estar pendiente de resolución.
##	b.3) el 20% de las incidencias del 2018 en cuarentena es debido a que están recién detectadas por el sistema SIEM, y pendientes de revisar por un analista.
##		 En este caso el campo details no contiene aún ninguna información.
## c) [A]bierta. Contendrá algunas notas acerca de cómo se está atendiendo cada incidencia.

## HAY QUE REPASAR ESTE CAMPO Y SU CONTENIDO DE PRUEBA GENERADO: ¿HAY QUE INSERTAR MAQUETACIÓN HTML...? -> PROBAR UNA VEZ CONSTRUIDO EL INTERFAZ WEB!!

## El comienzo de resolución de la incidencia (atención) por parte del personal de seguridad podría ser algo del estilo:
'Se inician las acciones para la resolución de la incidencia.'
## Se utilizará este texto en el campo de detalles como señal de que la incidencia comienza a atenderse.

details_list_closed = ['Se inician las acciones para la resolución de la incidencia. Tras aplicar las medidas de protección recomendadas, se observa que la incidencia\
 persiste. Se aplican nuevas medidas de seguridad: bla bla bla. Se comprueba que la incidencia queda resuelta',\
 'Se inician las acciones para la resolución de la incidencia. Se aplican las medidas de protección recomendadas, la incidencia queda resuelta.',\
'Se inician las acciones para la resolución de la incidencia. Aplicando las medidas de protección tal, tal y pascual, se observa que la incidencia queda resuelta.',\
'Se inician las acciones para la resolución de la incidencia. Se aplica la medida de protección tal y se observa el comportamiento del sistema. Verificada su \
estabilidad, se aplica la medida de protección pascual. Se comprueba que la incidencia queda resuelta.',\
'Se inician las acciones para la resolución de la incidencia. La resolución de la incidencia requiere que la incidencia ######## se cierre previamente, por lo que se \
deja en cuarentena. La incidencia ######## se cierra correctamente. Se aplican las medidas de protección recomendadas, quedando solucionada la incidencia.',\
'Se inician las acciones para la resolución de la incidencia. La resolución de la incidencia requiere la actualización del siguiente software: bla bla bla, por lo que \
se deja en cuarentena. Una vez actualizado el software la incidencia queda resuelta.']

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

details_list_open = ['Se inician las acciones para la resolución de la incidencia.',\
'Se inician las acciones para la resolución de la incidencia.',\
'Se inician las acciones para la resolución de la incidencia.',\
'Se inician las acciones para la resolución de la incidencia. Aplicadas las medidas de protección tal y pascual de manera correcta. Se continuará aplicando el resto \
de medidas.',\
'Se inician las acciones para la resolución de la incidencia. Para poder aplicar la medida de protección tal se ha hecho necesario reiniciar el servidor pascual. \
Realizando pruebas de estabilidad.',\
'Se inician las acciones para la resolución de la incidencia. La resolución de la incidencia requiere la actualización del siguiente software: bla bla bla, por lo que \
se deja en cuarentena. Una vez actualizado el software correctamente, se retoma la resolución de la incidencia, aplicando el resto de medidas de protección.']

## Se insertan varias entradas solo con el texto inicial (Se inician las acciones para la resolución de la incidencia), ya que será la situación más habitual de las
## últimas incidencias en generarse. Al insertarse aquí de manera repetida se evita tener que aplicar cálculo probabilístico a la hora de generar cada incidencia.

## pm_info:
## Este campo se genera a partir de ENS.pm_list y su estructura es: “ID Medida#1”$$S/N”Observaciones#1”//“ID Medida#2”$$S/N”Observaciones#2”//…]]
## A la hora de generarlo hay que tener encuenta que el contenido de las medidas de protección vienen definidas en el ENS, para cada tipo de incidencia (campo type).
## Habrá que tener en cuenta también el flag de aplicado (S/N), y añadir observaciones.

observ_list_complete = ['Aplicada correctamente.',\
'Aplicada correctamente.',\
'Aplicada correctamente.',\
'Precisa aplicar antes la medida ###. Se aplica la medida ###. Aplicada correctamente.',\
'Precisa actualización del software: bla bla bla. Aplicada correctamente.',\
'No se puede aplicar la recomendación sobre: bla bla bla. Se admite aplicación parcial. Parcialmente aplicada.',\
'Se puede aplicar en su lugar la siguiente medida sustitutiva: bla bla bla. Medida sustitutiva aplicada. Aplicada correctamente.',]

observ_list_pending = ['', '', '',\
'Precisa aplicar antes la medida ###.',\
'Precisa actualización del software: bla bla bla.',\
'Se puede aplicar en su lugar la siguiente medida sustitutiva: bla bla bla.',\
'Precisa la adquisición y despliegue del siguiente material: bla bla bla.']

## Al igual que en el caso de la generación del campo details, se insertan de manera repetida las situaciones más habituales, con lo que se evita
## tener que aplicar cálculo probabilístico a la hora de seleccionar una entrada de la lista.

## false_p y false_n:
## Este dato será importante de cara a las estadísticas y, en especial, a determinar la calidad de detección del SIEM.
## Los falsos positivos se refiere a detecciones que, en la realidad, no se corresponde con una amenaza real. Según la heurística y la configuración que se haya
## establecido, el sistema SIEM será más o menos propenso a generar falsos positivos.
## Mientras que los falsos negativos se producen cuando el personal de seguridad observa que el sistema SIEM no ha sido capaz de detectar una amenaza que ellos
## sí han conseguido detectar.
## Como es lógico, los falsos negativos pueden ser potencialmente más peligrosos que los falsos positivos.

## Las incidencias marcadas como falsos positivos se encontrarán ya [C]erradas, ya que al detectarse que no se trata de una amenaza real y una vez se esté seguro
## de ello, se marcarán como falso positivo y se cerrarán por el personal de seguridad responsable en el mismo instante de gestión de la incidencia.

## Las incidencias marcadas como falsos negativos pueden encontrarse en cualquier estado: [A]bierta, c[U]arentena o [C]errada. En cualquier caso, que sea un falso
## negativo, es decir, un error de detección por parte del sistema SIEM, es independiente del estado de la incidencia conforme se vaya gestionando a lo largo de su
## ciclo de vida. Por tanto, de cara a la generación de datos de prueba, se distribuirá de manera equiprobable.

## En este trabajo no se considerarán los falsos negativos que pueden achacarse también al personal (detección tardía contando ya con evidencias), ya que resulta
## muy complejo establecer un límite a partir del cual deja de ser sólo un falso negativo del sistema SIEM y constituye también un falso negativo del personal. Es decir,
## cuando el personal de seguridad detecta una amenaza, en ese momento se sabe con seguridad que el sistema SIEM ha fallado, ya que no ha sido éste el que la ha
## descubierto, pero, ¿cómo saber si también el personal de seguridad ha fallado y se podría haber detectado antes...? Se dejará como posible línea futura de trabajo.
## Sin embargo, sí se pueden contemplar estadísticas respecto a los falsos positivos del personal de seguridad, ya que indican que generaron una incidencia para lo que
## resultó no ser una amenaza real. Se realizará de manera anónima.

## Como premisa general, false_p y false_n son mútuamente excluyentes, es decir, si uno se encuentra activo el otro debe obligatoriamente encontrarse inactivo.

## Distribución de probabilidad:
## a) entre las incidencias [C]erradas donde originator='SIEM', se establecerá un nivel de un 6% de falsos positivos.
## b) entre las incidencias [C]erradas donde originator<>'SIEM', se establecerá un nivel de un 3% de falsos positivos.
## c) entre las incidencias donde originator='SIEM', se establecerá un 3% de falsos negativos.
## Todo ello resultará en un determinado X% de fallo del sistema SIEM, o lo que es lo mismo, un 100-X% de tasa de acierto, que marcará la calidad de detección del mismo.
## Se deberá separar las estadísticas de falsos positivos de las de falsos negativos, ya que su causa, naturaleza y consecuencias son muy distintos.
## Por otro lado, la tasa de acierto ante los falsos positivos del personal será un indicador de la calidad técnica del mismo.

## closing_date:
## Por último se incorpora el campo closing_date, el cual recoge la fecha de cierre de la incidencia.
## Este dato es importante en el sentido de que marca la fecha total de atención de la incidencia, desde que es detectada hasta que su cierre.
## Se necesita un amplio espectro de valores temporales posibles, de tal manera que se distribuyan suficientemente los valores.
## Se pondrá un tope de 2 años, valor típico en estos sistemas, cuando se desea hacer limpieza de aquellas incidencias cuya resolución se ha quedado atascada largo
## plazo. Normalmente, si se considera de interés, lo que suele hacerse es reabrirse una nueva incidencia que referencie a la anterior, y a partir de la cual se
## pueda proseguir la gestión.
## El límite inferior, de manera normal, viene determinado por aquellas incidencias de severidad Baja que se solucionan del orden de pocos días. De manera excepcional,
## habrá incidencias que se cierren en el mismo día de su apertura debido a regularizaciones (limpieza), o bien a equívocos del personal a la hora de abrir una 
## incidencia, como puede ser equivocarse en un dato fundamental que no admita modificación.
## Planteados los criterios, la distribución por tramos se establece en la siguiente:
## a) Gestión normal de incidencias: el 80% de los casos. Distribución entre 7 días y 3 meses.
## b) Gestión de incidencias de mayor complejidad: 10% de los casos. Distribución entre 3 meses y 1 día, y 9 meses.
## c) Gestión de incidencias de larga duración: 6%. Distribución entre 9 meses y 1 día, y 2 años (tope).
## d) Regularización y rectificación: 4%. Cierre el mismo día de la apertura.

## Una vez expuestas las premisas para generar los datos, se expone el código que da solución a la implementación propuesta:

# (id, originator, type, description, area, accountable, csirt, id_csirt, detect_date, notify_date, severity, dimensions, status, reports, details, pm_info, false_p, false_n) 

year = 2015;	# Se parte del año 2015.
med = 120;		# Media de incidencias para cada año.

# Para generar los datos de prueba relativos a las incidencias, se hace necesario en primer lugar definir el personal responsable de seguridad
# que puede generarlas y atenderlas. Por tanto, en primer lugar se definirá el STAFF, y el estado de cada personal.
# La tabla STAFF se ha generado de manera manual ya que no requiere generar datos aleatorios complejos y contiene un número de registros muy reducido.
# De cara a la generación de la tabla de incidentes, solo se necesita el código de usuario y el estado de cada trabajador:

staff = ['blachimar', 'silsanmel', 'davgonvaz', 'carsevove', 'artgardel', 'marestrom', 'joscarval', 'lucvelrub', 'abegonher', 'analopgar', 'pedcanmal', 'josgommar', 'angigonel', 'danjimcue', 'juamarmor', 'aderosmon', 'framinest', 'rafnadpar', 'mantencar', 'mikzucsav', 'serverguz', 'leocalsot']
staff_status = ['A', 'A', 'A', 'A', 'A', 'A', 'V', 'A', 'B', 'V', 'A', 'A', 'A', 'A', 'A', 'D', 'A', 'A', 'A', 'A', 'B', 'D']
# Se extrae el personal en activo:
staff_active = []	# Recogerá los códigos de usuario del personal que se encuentra actualmente en activo en la organización.
for i in range(len(staff_status)):
	if staff_status[i] == 'A':
		staff_active.append(staff[i])

# Se define también las áreas o departamentos en que puede estar dividida la Unidad:
areas = ['Jefatura', 'Secretaría', 'Apoyo al Personal', 'Escuadrón #1', 'Escuadrón #2', 'Escuadrón #3', 'Abastecimiento', 'Automóviles', 'Global']
# Global simboliza algún incidente que pueda afectar de manera global a toda la organización, como puede ser la detección de ransomware,
# el cual puede prograrse por toda las máquinas con acceso a redes públicas.

id_csirt = 0	# Recogerá el ID al generar cada CSIRT.

# Una vez establecidas las premisas y datos globales, se pasa a generar los datos relativos a las tablas INCIDENTS y CSIRT.
# En primer lugar se inicia laa cadenas de datos que albergarán las tablas:

data_i = ''
data_c = ''
		
data_i += 'INSERT INTO INCIDENTS' + '\n' + '(id, originator, type, description, area, accountable, csirt, id_csirt, detect_date, notify_date, severity, dimensions, status, \
reports, details, pm_info, false_p, false_n, closing_date)' + '\n' + 'values' + '\n'

data_c += 'INSERT INTO CSIRT' + '\n' + '(id, id_incid, team, team_date)' + '\n' + 'values' + '\n'

for i in range(4):

	# En primer lugar, se conformarán los datos globales que se utilizarán para cada año:

	incidents_year_count = 0	# Se utilizará para contabilizar el número de incidencias generadas por año, y para extraer los datos de fechas.

	csirt_count = 1		# Permite llevar la cuenta de los equipos de respuesta generados para cada año.

	signo = random.randrange(2)
	desv = random.randrange(30)
	
	if signo > 0:
		num_incidents = med - desv
	else:
		num_incidents = med + desv
	# En este punto se cuenta con el número de incidentes a generar para el año correspondiente a la iteración.
	
	# A continuación, se calcula el promedio de incidentes por mes. Servirá para distribuir la fecha de detección a la largo de todo el año.
	# La variable num_incidents contiene el número de incidentes que se generarán para cada año => se divide por 12 para promediar según mes:
	num_incidents_by_month = num_incidents/12
	
	# Seguidamente, se genera la lista con los datos de fecha y hora de detección, y fecha y hora de notificación (si procede):
	
	# Recordamos que la variable num_incidents contiene el número de incidentes que se generarán para cada año,
	# y que la variable num_incidents_by_month recoge el promedio por mes.
	
	# Ahora toca distribuir los incidentes entre cada mes:
	days_by_month = [31,28,31,30,31,30,31,31,30,31,30,31]	# Se necesita conocer el número de días de cada mes para una generación de fecha correcta.
	
	incident_days = []			# Recogerá los días concretos de detección de cada incidencia.
	detect_date_year = []		# Recogerá la lista anual de fechas de detección de las incidencias.
	notify_date_year = []		# Recogerá la lista anual de fechas de notificación de las incidencias.
	closing_date_year_list = []	# Recogerá la lista anual de fechas de cierre de las incidencias.
	
	for m in range(12):
		incident_days = random.sample(range(1,days_by_month[m]+1),num_incidents_by_month)	# Se genera la lista de días concretos para cada mes.
		# (se debe tener cuidado de generar un día válido entre 1 y el último día de cada mes)
		
		incident_days.sort()	# Se ordena el día de menor a mayor.
		
		for n in range(len(incident_days)):	# Para cada día generado, se compone la fecha y hora concretas de detección, de manera aleatoria.
			# Primero se generará la hora, pues se necesitará de cara a generar la hora de la notificación:
			detect_hour = random.randrange(24)
			detect_min = random.randrange(60)
			# Se genera un valor aleatorio entre 1 y 5 que simboliza la diferencia en minutos entre el instante de detección y el de notificación:
			detect_notify_diff = random.randrange(5) + 1
			# Se genera la hora de la notificación:
			notify_hour = detect_hour
			notify_min = detect_min + detect_notify_diff
			# Ajustamos la hora y minuto según el valor resultante:
			if notify_min > 59:
				notify_hour = notify_hour + 1
				notify_min = notify_min - 60

			detect_date = str(str(year) + str('{0:2d}'.format(m+1)).replace(' ','0') + str('{0:2d}'.format(incident_days[n]))).replace(' ','0') + str('{0:2d}'.format(detect_hour)).replace(' ','0') + str('{0:2d}'.format(detect_min)).replace(' ','0')
			detect_date = detect_date.replace('\s\d\d//','\d\d//')	# Se eliminan los espacios en blanco innecesarios.

			notify_date = str(str('{0:2d}'.format(incident_days[n]))).replace(' ','0') + '/' + str('{0:2d}'.format(m+1)).replace(' ','0') + '/' + str(year) + ' ' + str('{0:2d}'.format(notify_hour)).replace(' ','0') + ':' + str('{0:2d}'.format(notify_min)).replace(' ','0')
			notify_date = notify_date.replace('\s\d\d//','\d\d//')	# Se eliminan los espacios en blanco innecesarios.
						
			detect_date_year.append(detect_date)
			notify_date_year.append(notify_date)
			
			# Se calcula y añade la fecha de cierre en base a las premisas establecidas:
			# a) Gestión normal de incidencias: el 80% de los casos. Distribución entre 7 días y 3 meses.
			# b) Gestión de incidencias de mayor complejidad: 10% de los casos. Distribución entre 3 meses y 1 día, y 9 meses.
			# c) Gestión de incidencias de larga duración: 6%. Distribución entre 9 meses y 1 día, y 2 años (tope).
			# d) Gestión rápida, regularización y rectificación: 4%. Cierre dentro de la misma semana: 0 a 6 días.
			# Los cálculo se realizarán en días:
			prob = random.randrange(100)
			if prob < 4:
				days_offset = random.randrange(7)
			elif prob > 3 and prob < 10:
				days_offset = 30*9 + 1 + random.randrange(365*2-(30*9 + 1))
			elif prob > 9 and prob < 20:
				days_offset = 30*3 + 1 + random.randrange(30*6)
			else:
				days_offset = 7 + random.randrange(30*3-6)
			
			days_offset_years = days_offset / 365
			days_offset = days_offset - 365 * days_offset_years
			days_offset_months = days_offset / 30
			days_offset_days = days_offset - days_offset_months * 30

			closing_date_day = int(detect_date[6:8]) + days_offset_days
			closing_date_month = int(detect_date[4:6]) + days_offset_months
			closing_date_year = int(detect_date[0:4]) + days_offset_years
			if closing_date_day > 30:                               # Para las pruebas, se trabaja con meses de 30 d para simplificar los datasets.
					closing_date_month += 1
					closing_date_day -= 30

			if closing_date_month > 12:
					closing_date_year += 1
					closing_date_month -= 12

			if closing_date_month == 2 and closing_date_day > 28:   # Se tiene en cuenta el mes de febrero.
					closing_date_day = 28

			closing_date = str('{0:4d}'.format(closing_date_year)).replace(' ','0') + str('{0:2d}'.format(closing_date_month)).replace(' ','0') + str('{0:2d}'.format(closing_date_day)).replace(' ','0')

			if int(closing_date) > int(time.strftime("%Y%m%d")):
					closing_date = time.strftime("%Y%m%d")
					
			closing_date_year_list.append(str(closing_date))

			
	#print detect_date_year	###
	#print notify_date_year	###
	
	num_incidents = len(detect_date_year)	# Se ajusta al número de fecha generadas para sincronizar con el número de incidencias a generar en cada año.
	
	#print 'Cantidad de fechas generadas: ' + str(len(detect_date_year))		###
	
	# Ahora comenzamos a generar los incidentes, por lo que empleamos un segundo bucle for:
	for j in range(num_incidents):
		# Comenzando por el ID:
		id = str(year)+str('{0:4d}'.format(j+1))
		id = id.replace(' ','0')
		id = int(id)

		# Ahora se pasa a generar el originador de la incidencia, teniendo en cuenta que en el 80% de los casos será el sistema SIEM:
		prob=random.randrange(100)
		if prob < 80:
			originator = 'SIEM'
		else:
			# En este caso, se selecciona aleatoriamente entre el personal en activo. Una vez esté en funcionamiento la aplicación de gestión,
			# el originador será la persona que registra de manera manual el alta de la nueva incidencia detectada:
			num = random.randrange(len(staff_active))
			originator = staff_active[num]
			
		#print originator
		
		# A continuación, se generan los datos type y description:
		
		t = random.randrange(40)
		type = ens_id_obj[t]			# Se extrae el tipo de incidente de manera aleatoria entre los 40 posibles.
		description = ens_descrip[t]	# Junto con el ID del Objetivo, se extrae también su descripción.
		#print description	###
		
		# Seguidamente se asigna, también de manera aleatoria, el área afectada donde se detectó el incidente:
		area = areas[random.randrange(len(areas))]
		#print area	###
		
		# El siguiente paso es la asignación del responsable en el seguimiento de la incidencia (Accountable).
		# Recordando las premisas:
		# a) Si el originador es el sistema SIEM, se seleccionará un responsable de seguridad de manera aleatoria entre el personal en activo.
		# b) Si el originador es personal de seguridad (alta manual), por lo general será la misma persona que se haga responsable, pero
		# esto no tiene porqué darse en el 100% de los casos. Se supondrá una coincidencia del 80%.
		# c) En cualquier caso, en el caso de conformarse un equipo de respuesta, el responsable será la persona que aparezca en primera lugar en el CSIRT.
		# Esta circunstancia se tendrá en cuenta en el caso de que se conforme un equipo de respuesta.
		
		num = random.randrange(len(staff_active))	# Servirá para seleccionar de manera aleatoria una persona en activo como responsable.
		accountable = staff_active[num]				# Será, además, la asignación por defecto.
		
		if originator != 'SIEM':			
			prob = random.randrange(100)
			if prob < 80:
				accountable = originator
		
		#print 'Originator: ' + originator	###
		#print accountable	###
		
		# Hasta aquí, cada incidencia tiene asignada una persona física responsable del seguimiento de la incidencia. Cuando se genere el
		# estado de la incidencia (status), habrá que generar algunas incidencias en estado de cuarentena ('U') y en las que el originador sea
		# el sistema SIEM. En ese caso, se mantendrá 'SIEM' como accountable, pendiente de asignación una vez se revise por un analista.
		# La única excepción al caso anterior es que la incidencia lleve asociada la generación automática de un CSIRT, en ese caso, obligatoriamente,
		# el responsable será la persona que aparezca en primer lugar en el equipo de respuesta.
		# Este campo es editable de manera manual, no obstante y por si fuera necesario.
		
		# Severidad:
		prob = random.randrange(100)
		# Recordemos: Críticas: 5%, Altas: 10%, Medias: 30% y Bajas: 55%.
		if prob > 94:
			severity = 'C'
		elif prob > 84:
			severity = 'A'
		elif prob > 54:
			severity = 'M'
		else:
			severity = 'B'
		#severity = 'C'  ### Pruebas...
		
		#print severity	###

		# Conformación de CSIRT:
		csirt = 'N'		# Por defecto, no se conforma.
		id_csirt = 0
		
		if severity == 'C':
			#print severity	###
			if random.randrange(100) < 94:	# Probabilidad del 94% de conformar un CSIRT para incidencias de severidad crítica.
				csirt = 'S'
				id_csirt = str(year)+str('{0:2d}'.format(csirt_count))
				id_csirt = id_csirt.replace(' ','0')
				id_csirt = int(id_csirt)
				csirt_count = csirt_count + 1
				#print id_csirt	###
				
		#if csirt == 'S':
			#print csirt	###
		
		# Generación de datos para el campo csirt_team:
		# De cara a la generación de datos de prueba, tal como se ha argumentado anteriormente, en aquellos casos en que se haya conformado un CSIRT,
		# se escogerán 3 personas de manera aleatoria de entre el personal responsable de seguridad en activo.
		if severity == 'C' and csirt == 'S':
			# En primer lugar, se generan 3 valores enteros aleatorios diferentes que representarán el índice en la lista de personal en activo:
			nums = random.sample(range(len(staff_active)), 3)
				
			# Por último, se genera el equipo de respuesta:
			csirt_team = ''
			csirt_team += staff_active[int(nums[0])]
			csirt_team += staff_active[int(nums[1])]
			csirt_team += staff_active[int(nums[2])]
			
			accountable = staff_active[int(nums[0])]	# Recordar que, en cualquier caso, al conformar un CSIRT, el responsable es el primer miembro del equipo.
			# csirt_team = []
			# csirt_team.append(staff_active[int(nums[0])])
			# csirt_team.append(staff_active[int(nums[1])])
			# csirt_team.append(staff_active[int(nums[2])])
			
			# accountable = csirt_team[0]		# Recordar que, en cualquier caso, al conformar un CSIRT, el responsable es el primer miembro del equipo.
			
			# Se añade el nuevo CSIRT generado a la cadena de datos:
			data_c += '('+str(id_csirt)+', '+str(id)+', '+"'"+csirt_team+"'"+', '+"'"+notify_date_year[incidents_year_count]+"'"+'),\n'
			# Se aprovecha el desfase de la fecha de notificación respecto a la de detección para tomarla como fecha de creación del equipo de respuesta.

			#print 'CSIRT: ' + str(csirt_team)	###
			
		#print 'Responsable: ' + accountable	###
		
		#elif severity == 'C':
		#	print 'Incidencia Crítica, pero sin CSIRT conformado.'	###

		# El siguiente paso es generar las dimensiones de seguridad potencialmente afectadas por la incidencia.
		# Como se indicaba en la exposición de premisas, de cara a la generación de los datos de prueba, se realizará de manera aleatoria:
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
					
		#print dimensions	###
		
		# El siguiente paso es indicar el estado de la cada incidencia. A continuación, se recuerdan las premisas:
		# Años 2015 y 2016: 100% [C]erradas.
		# Año 2017: 90% [C]erradas, 5% en c[U]arentena.
		# Año 2018: 70% [C]erradas, 12% en c[U]arentena.
		# Resto, [A]biertas.

		status = 'A'	# Estado inicial.
		
		if year == 2015 or year == 2016:
			status = 'C'
			
		elif year == 2017:
			prob = random.randrange(100)
			if prob < 90:
				status = 'C'
			elif prob < 95:
				status = 'U'
				
		elif year == 2018:
			prob = random.randrange(100)
			if prob < 70:
				status = 'C'
			elif prob < 82:
				status = 'U'
		
		#print status	###
		
		# Seguidamente se generan los enlaces a los informes según la proporción del 20% establecida en las premisas:
		prob = random.randrange(100)

		reports = ''
		#reports = reports_t = ''
		
		if prob < 20:
			# Se seleccionarán entre 1 y 3 documentos de manera aleatoria entre la lista disponible:
			num_reports = random.randrange(3) + 1	
			reports_index = random.sample(range(len(reports_list)),num_reports)
			reports_index.sort()
			for l in range(num_reports):
				reports += reports_list[reports_index[l]] + '=='	# Ojo con el separador que se elige, que no conflicte con el contenido!
				#reports_t += reports_list[reports_index[l]] + '=='	# Ojo con el separador que se elige, que no conflicte con el contenido!
			
			#reports = reports_t
			#reports = reports_t[0:len(reports_t)-2] + ']]'
			
			
			#print 'num_reports: ' + str(num_reports)	###
			#print reports	###
			#print '\n\n'
					
		# A continuación, se generarán los detalles de cada incidencia:
		if status == 'C':
			details = details_list_closed[random.randrange(len(details_list_closed))]
		elif status == 'U':
			details = details_list_quarantine[random.randrange(len(details_list_quarantine))]
		elif status == 'A':
			details = details_list_open[random.randrange(len(details_list_open))]
		
		#print status	###
		#print details + '\n\n'

		# HASTA AQUI OK!!

		# El siguiente paso es generar los datos del campo pm_info, a partir del registro ENS.pm_list y los datos añadidos.
		# Recordar que el formato es el siguiente: 
		# “ID Medida#1”$$’S/N’”Observaciones#1”//“ID Medida#2”$$’S/N’”Observaciones#2”//…]]
		# Para generar este campo, por tanto, se precisa el siguiente procesado:
		# a) en primer lugar, extraer las ID's de las medidas de protección aplicables. Ello se realiza a partir del objetivo de seguridad correspondiente (type).
		# b) seleccionar de manera aleatoria si se ha aplicado una determinada medida o no: se considerará equiprobable.
		# c) generar el campo de observaciones. Se empleará una lista con datos de prueba desde la cual se seleccionará una determinada entrada de manera aleatoria.
		#    En este caso se generan dos listas: una en el caso de que la medida se haya aplicado, y otra lista de observaciones cuando no se haya aplicado.
				
		obj_current = locals()['obj_' + type]
			
		#print type		###
		#print obj_current + '\n\n\n'

		pat = re.compile('\d{3}\. ')

		pm_list_id = pat.findall(obj_current)

		#print pm_list_id	###
				
		pm_info = ''
		
		for p in range(len(pm_list_id)):
		
			if random.randrange(2) == 0:
				pm_info += pm_list_id[p].replace(". ","") + '$$' + 'S' + observ_list_complete[random.randrange(len(observ_list_complete))]

			else:
				pm_info += pm_list_id[p].replace(". ","") + '$$' + 'N' + observ_list_pending[random.randrange(len(observ_list_pending))]

			pm_info += '=='		# Se añade el símbolo separador.
			
		#print pm_info	###		
		#raw_input()	###
		
		# Por último, se rellenan los campos relativos a falsos positivos y falsos negativos. Se recuerda la distribución de probabilidad:
		# a) entre las incidencias [C]erradas donde originator='SIEM', se establecerá un nivel de un 16% de falsos positivos.
		# b) entre las incidencias [C]erradas donde originator<>'SIEM', se establecerá un nivel de un 5% de falsos positivos.
		# c) entre todas las incidencias donde originator='SIEM', se establecerá un 4% de falsos negativos.
		# Recordar también que false_p y false_n son mútuamente excluyentes:
		
		prob = random.randrange(100)	# Para distribución de la probabilidad.
		
		false_p = false_n = 'N'			# Por defecto, inactivos.
		
		if originator == 'SIEM' and prob < 4:
			false_n = 'S'
		
		if status == 'C' and false_n == 'N':
			if originator == 'SIEM':
				if prob < 16:
					false_p = 'S'
			else:
				if prob < 5:
					false_p = 'S'
					
		# print 'Falso positivo: ' + false_p	###
		# print 'Falso negativo: ' + false_n
		# if false_p == 'S':
			# false_p_count += 1
		# elif false_n == 'S':
			# false_n_count += 1

		#print 'Contador de incidencias generadas por año: ' + str(incidents_year_count)	###
		
		if status == 'C':
			closing_date = closing_date_year_list[incidents_year_count]
		else:
			closing_date = '0'
			
		# Una vez se dispone de todos los datos para cada incidencia, se añade a la cadena de datos que se utilizará para generar el archivo .sql:
		if year == 2018 and j == (num_incidents-1):
			data_i += '('+str(id)+', '+"'"+originator+"'"+', '+type+', '+"'"+description+"'"+', '+"'"+area+"'"+', '+"'"+accountable+"'"+', '+"'"+csirt+"'"+', '+\
			str(id_csirt)+', '+"'"+detect_date_year[incidents_year_count]+"'"+', '+"'"+notify_date_year[incidents_year_count]+"'"+', '+"'"+severity+"'"+\
			', '+"'"+str(dimensions)+"'"+', '+"'"+status+"'"+', '+"'"+str(reports)+"'"+', '+"'"+str(details)+"'"+', '+"'"+str(pm_info)+"'"+', '+"'"+false_p+"'"+\
			', '+"'"+false_n+"'"+', '+"'"+closing_date+"'"+');\n'
		else:
			data_i += '('+str(id)+', '+"'"+originator+"'"+', '+type+', '+"'"+description+"'"+', '+"'"+area+"'"+', '+"'"+accountable+"'"+', '+"'"+csirt+"'"+', '+\
			str(id_csirt)+', '+"'"+detect_date_year[incidents_year_count]+"'"+', '+"'"+notify_date_year[incidents_year_count]+"'"+', '+"'"+severity+"'"+\
			', '+"'"+str(dimensions)+"'"+', '+"'"+status+"'"+', '+"'"+str(reports)+"'"+', '+"'"+str(details)+"'"+', '+"'"+str(pm_info)+"'"+', '+"'"+false_p+"'"+\
			', '+"'"+false_n+"'"+', '+"'"+closing_date+"'"+'),\n'
		
		incidents_year_count += 1		# Se incrementa el contador global de incidencias generadas.
		
	year += 1	# Se pasa a la generación de datos de incidencias para el siguiente año.
		
#print '\n\nFalsos Positivos: ' + str(false_p_count) + '  Falsos Negativos: ' + str(false_n_count)

# Se realizan últimos ajustes de formato:
data_i = data_i.replace('[]','')

# Una vez se cuenta con el contenido de todos los registros de la tabla INCIDENTS, se vuelca en un fichero .sql para su procesado posterior:
incidents_table = open ('incidents_table.sql','w')	# Se crea el archivo.
incidents_table.write(data_i)						# Se escribe el contenido.
incidents_table.close()								# Por último, se cierra, haciendo efectivos los cambios.

# Por último, para la tabla CSIRT:
data_c = data_c[0:len(data_c)-2] + ';\n'

# Una vez se cuenta con el contenido de todos los registros de la tabla INCIDENTS, se vuelca en un fichero .sql para su procesado posterior:
csirt_table = open ('csirt_table.sql','w')		# Se crea el archivo.
csirt_table.write(data_c)						# Se escribe el contenido.
csirt_table.close()								# Por último, se cierra, haciendo efectivos los cambios.

raw_input()		### Permite lanzar el script desde un editor externo (notepad++, por ejemplo) y mantener la ventana abierta para ver los resultados.
