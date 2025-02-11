import csv
from psycopg2 import connect

def load_data(file_path):
    conn = connect("dbname=autos_db user=admin host=localhost password=yourpassword")
    cur = conn.cursor()
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # Inserta los datos en la base de datos
            pass
    cur.close()
    conn.close() 