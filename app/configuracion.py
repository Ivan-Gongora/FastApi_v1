# app/configuracion.py

import os

class ConfiguracionSimulacion:
    # Configuración de la base de datos MySQL (XAMPP)
    db_host: str = "localhost" #si su xampp esta en windows y su entorno virtual en ubuntu , poner su ip de computadora
                                  # y modificar el usuario root de phpmyadmin quitarle el "localhost y ponerle el " %" "
                                  #si todo esta en windows, solo cambien esto por localhost
    db_port: int = 3306
    db_user: str = "root" # Usuario por defecto de XAMPP MySQL
    db_password: str = "" # Contraseña por defecto de XAMPP MySQL (vacía por defecto en XAMPP)
    db_name: str = "sistema_iot" # El nombre de tu base de datos

    # Mapeo de nombres de CSV a IDs de campo en la DB.
    # Estos IDs corresponden a los campos 'Temperatura' y 'Humedad'
    # de tus sensores 'STM-01' y 'SHM-01' respectivamente.
    # ¡Estos IDs SÍ DEBES OBTENERLOS y ponerlos aquí!
    campo_temperatura_id: int = 2 # Ejemplo: 1
    campo_humedad_id: int = 3 # Ejemplo: 4


# Instancia de configuración
configuracion = ConfiguracionSimulacion()