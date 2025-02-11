from flask import Blueprint, request, render_template
from ..services.car_service import calculate_market_price
import psycopg2

main = Blueprint('main', __name__)

def get_db_connection():
    conn = psycopg2.connect("dbname=autos_db user=admin host=localhost password=yourpassword")
    return conn

@main.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        year = request.form['year']
        make = request.form['make']
        model = request.form['model']
        mileage = request.form.get('mileage', None)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Consulta para obtener el precio de mercado estimado
        query = """
        SELECT AVG(listing_price) FROM cars
        WHERE year = %s AND make = %s AND model = %s
        """
        cur.execute(query, (year, make, model))
        market_price = cur.fetchone()[0]
        
        # Consulta para obtener las muestras de listados
        query = """
        SELECT make, model, listing_price, listing_mileage, dealer_city, dealer_state
        FROM cars
        WHERE year = %s AND make = %s AND model = %s
        LIMIT 100
        """
        cur.execute(query, (year, make, model))
        listings = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return render_template('results.html', market_price=market_price, listings=listings)
    
    return render_template('search.html')

@main.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        # Aquí iría la lógica para mostrar los resultados basados en la búsqueda
        return render_template('results.html')
    else:
        # Si se accede con GET, simplemente muestra la página de resultados vacía o un mensaje
        return render_template('results.html', market_price=None, listings=[]) 