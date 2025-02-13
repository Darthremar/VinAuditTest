from flask import Blueprint, request, render_template, jsonify
from ..services.car_service import CarService
from ..repositories.car_repository import CarRepository
from ..database import SessionLocal

main = Blueprint('main', __name__)

def get_car_service():
    db = SessionLocal()
    repository = CarRepository(db)
    return CarService(repository)

@main.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        year = request.form['year']
        make = request.form['make']
        model = request.form['model']
        mileage = request.form.get('mileage', None)
        
        car_service = get_car_service()
        
        # Calculate market price
        market_price = car_service.calculate_market_price(year, make, model)
        
        # Calculate price estimate based on mileage
        price_estimate_based_on_mileage = car_service.calculate_price_based_on_mileage(year, make, model, mileage)
        
        # Format prices for display
        market_price_display = f"${market_price:,.0f}" if market_price else "N/A"
        price_estimate_based_on_mileage_display = f"${price_estimate_based_on_mileage:,.0f}" if price_estimate_based_on_mileage else "N/A"
        
        # Get sample listings
        listings = car_service.get_sample_listings(year, make, model)
        
        return render_template('results.html', 
                             market_price=market_price_display, 
                             price_estimate_based_on_mileage=price_estimate_based_on_mileage_display, 
                             listings=listings)
    
    return render_template('search.html')

@main.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        # logic to show results based on search
        return render_template('results.html')
    else:
        # if accessed with GET, simply shows the empty results page or a message
        return render_template('results.html', market_price=None, listings=[])

@main.route('/query', methods=['GET', 'POST'])
def query_view():
    if request.method == 'GET':
        return render_template('query.html')
    
    try:
        car_service = get_car_service()
        offset = request.args.get('offset', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        
        # Obtener y validar los filtros
        filters = {}
        
        make = request.form.get('make', '').strip()
        if make:
            filters['make'] = make
            
        model = request.form.get('model', '').strip()
        if model:
            filters['model'] = model
            
        year = request.form.get('year')
        if year and year.isdigit():
            filters['year'] = int(year)
        
        # Obtener los resultados
        try:
            cars = car_service.get_cars_with_filters(**filters, offset=offset, limit=limit)
            total_count = car_service.get_total_count(filters)
            
            # Convertir los resultados a diccionario
            cars_list = []
            for car, listing, dealer in cars:  # Ahora recibimos tres elementos por cada fila
                car_dict = {
                    'make': car.make,
                    'model': car.model,
                    'year': car.year,
                    'listing_price': None,
                    'listing_mileage': None,
                    'dealer_city': None,
                    'dealer_state': None
                }
                
                if listing:
                    car_dict.update({
                        'listing_price': float(listing.listing_price) if listing.listing_price else None,
                        'listing_mileage': int(listing.listing_mileage) if listing.listing_mileage else None
                    })
                
                if dealer:
                    car_dict.update({
                        'dealer_city': dealer.dealer_city,
                        'dealer_state': dealer.dealer_state
                    })
                
                cars_list.append(car_dict)

            return jsonify({
                'cars': cars_list,
                'total_count': total_count,
                'has_more': offset + limit < total_count
            })
            
        except Exception as e:
            print(f"Error processing database query: {str(e)}")
            return jsonify({
                'error': f"Database error: {str(e)}",
                'cars': [],
                'total_count': 0,
                'has_more': False
            }), 400
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({
            'error': f"Request error: {str(e)}",
            'cars': [],
            'total_count': 0,
            'has_more': False
        }), 400 