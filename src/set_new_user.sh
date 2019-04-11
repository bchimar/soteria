#!/bin/bash

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
# 				set_new_user.sh: 							#
# Shell Script para gestionar el alta de nuevos usuarios.	#
#############################################################

clear
server="127.0.0.1"

cp /home/common-password_hardening /etc/pam.d/common-password	# Se asegura que se establece una contraseña de suficiente robustez.

echo 'Introduzca el nombre de usuario a dar de alta:'
read new_user		# Lectura desde la consola.
adduser $new_user	# Creación del nuevo usuario

mkdir /home/users/$new_user		# Se crea la carpeta que albergará las credenciales del usuario para Google Authenticator.

echo -en '\n'
echo 'A continuación se generarán la clave secreta y el código QR para Google Authenticator.'
echo 'El nuevo usuario debe capturar el código QR, añadiéndolo a la aplicación cliente:'
sudo -u $new_user -H sh -c "cd /home/$new_user; google-authenticator"	# Se cambia a la cuenta del nuevo usuario.
# Se ejecuta la herramienta para generar la nueva clave/código QR para autenticación mediante PIN.

# Antes de nada, se realiza una copia de seguridad del archivo de configuración de Google Authenticator del usuario:
cp /home/$new_user/.google_authenticator /home/users/$new_user
# Ello permitirá restituir el permiso de acceso en caso necesario.

# En este punto también se recomienda, por parte del personal de seguridad, capturar la pantalla que contiene el código QR:
echo -en '\n'
echo 'Personal de gestión de cuentas: por favor, capture el código QR y regístrelo en la carpeta /home/users/'$new_user
echo 'Pulse una tecla para continuar...'
read -n 1 -s

echo -en '\n'
echo 'Inserte la clave secreta (aparece justo debajo del código QR):'
read token

echo -en '\n'
echo 'Se añaden las credenciales a los archivos de Google Authenticator:'
htdigest /home/osboxes/apache_2fa/apache_credentials $server $new_user

echo -en '\n'
echo 'Por último, se añade el nuevo usuario al fichero de tokens 2FA de Google Authenticator (tokens.json).'
sed 's@\"$@\",\n  \"'"$new_user"'\": \"'"$token"\"'@g' /home/osboxes/apache_2fa/tokens_backup.json > /home/osboxes/apache_2fa/tokens.json

echo -en '\n'
echo 'Alta de nuevo usuario completada!'
echo -en '\n'
