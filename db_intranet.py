import mariadb
import sys

try:
    conn = mariadb.connect(
        user="UserIntranet",
        password="631353051DBF13D759F78BBB1320E36A",
        host="10.0.0.6",
        port=3306,
        database="sitio_web"
    )
except mariadb.Error as e:
    print (f"Error connecting MariaDB Platform: {e}")

# Get Cursor
cur = conn.cursor()
cur.execute(
    "SELECT nombre,login FROM INTRANET_EMPLEADOS_USUARIOS WHERE LOGIN = 75099353")

# Print Result-set
for (name, login) in cur:
    print(f"Name: {name}, Login: {login}")