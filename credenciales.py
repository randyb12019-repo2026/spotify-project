import mysql.connector
mysql_config = {
    "host": "gateway01.us-west-2.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "TU_USUARIO",
    "password": "TU_CLAVE",
    "database": "proyecto_final",
    "ssl_disabled": False,
    "connect_timeout": 30,
}

conn = mysql.connector.connect(**mysql_config)

print(f"Conectado a {mysql_config['host']}:{mysql_config['port']}")
print(f"Base de datos: {mysql_config['database']}")