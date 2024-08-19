import sqlite3

conn = sqlite3.connect('emaildb.sqlite')  # Conecta (o crea) una base de datos SQLite llamada 'emaildb.sqlite'.
cur = conn.cursor()  # Crea un cursor que se utiliza para ejecutar comandos SQL.

cur.execute('DROP TABLE IF EXISTS Counts')  # Elimina la tabla 'Counts' si ya existe, para comenzar con una tabla limpia.

cur.execute('''CREATE TABLE Counts (email TEXT, count INTEGER)''')  # Crea una nueva tabla 'Counts' con dos columnas: 'email' (texto) y 'count' (entero).

fname = input('Enter file name: ')  # Solicita al usuario que ingrese el nombre de un archivo.
if (len(fname) < 1): fname = 'mbox-short.txt'  # Si el usuario no ingresa un nombre de archivo, se usa 'mbox-short.txt' por defecto.
fh = open(fname)  # Abre el archivo para lectura.
for line in fh:  # Itera sobre cada línea del archivo.
    if not line.startswith('From: '): continue  # Si la línea no comienza con 'From: ', se omite.
    pieces = line.split()  # Divide la línea en palabras.
    email = pieces[1]  # Obtiene la dirección de correo electrónico (segundo elemento en la línea).
    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email,))  # Busca si ya existe un registro para esa dirección de correo en la base de datos.
    row = cur.fetchone()  # Obtiene el resultado de la consulta.
    if row is None:  # Si no hay ningún registro para ese correo...
        cur.execute('''INSERT INTO Counts (email, count)
                VALUES (?, 1)''', (email,))  # ...inserta una nueva entrada con el conteo inicial de 1.
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?',
                    (email,))  # Si ya existe, incrementa el conteo en 1.
        conn.commit()  # Guarda (commitea) los cambios en la base de datos.

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'  # Prepara una consulta SQL para seleccionar los 10 correos con más apariciones.

for row in cur.execute(sqlstr):  # Ejecuta la consulta SQL y recorre los resultados.
    print(str(row[0]), row[1])  # Imprime el correo y su conteo.

cur.close()  # Cierra el cursor para liberar recursos.
