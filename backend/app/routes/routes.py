from flask import Blueprint, request, render_template, jsonify
from ..services.car_service import calculate_market_price, get_sample_listings, calculate_price_based_on_mileage, query_cars


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        year = request.form['year']
        make = request.form['make']
        model = request.form['model']
        mileage = request.form.get('mileage', None)
        
        # Calculate market price
        market_price = calculate_market_price(year, make, model)
        
        # Calculate price estimate based on mileage
        price_estimate_based_on_mileage = calculate_price_based_on_mileage(year, make, model, mileage)
        
        # Format prices for display
        market_price_display = f"${market_price:,.0f}" if market_price else "N/A"
        price_estimate_based_on_mileage_display = f"${price_estimate_based_on_mileage:,.0f}" if price_estimate_based_on_mileage else "N/A"
        
        # Get sample listings
        listings = get_sample_listings(year, make, model)
        
        return render_template('results.html', market_price=market_price_display, price_estimate_based_on_mileage=price_estimate_based_on_mileage_display, listings=listings)
    
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
    results = []
    error_message = None
    if request.method == 'POST':
        query_params = request.form.to_dict()
        offset = int(request.args.get('offset', 0))
        try:
            results = query_cars(query_params, offset=offset)
        except ValueError as e:
            error_message = str(e)
    return render_template('query.html', results=results, error_message=error_message) 