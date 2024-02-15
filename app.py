from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
from datetime import datetime

app = Flask(__name__)

# CSV file setup
CSV_FILE = 'ebay_sales.csv'

def read_csv():
    sales = []
    try:
        with open(CSV_FILE, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                sales.append(row)
    except FileNotFoundError:
        pass
    return sales

def write_csv(data):
    # Add the dollar sign before List Price and Sale Price
    data['List Price'] = "${}".format(data['List Price'])
    data['Sale Price'] = "${}".format(data['Sale Price'])

    with open(CSV_FILE, 'a', newline='') as csvfile:
        fieldnames = ['Sale Date', 'Item Description', 'eBay Number', 'Days on Market', 'List Price', 'Sale Price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)

@app.route('/')
def index():
    sales = read_csv()
    return render_template('index.html', sales=sales)

@app.route('/add_sale', methods=['POST'])
def add_sale():
    sale_date = request.form['sale_date']
    item_description = request.form['item_description']
    ebay_number = request.form['ebay_number']
    days_on_market = request.form['days_on_market']
    list_price = request.form['list_price']
    sale_price = request.form['sale_price']

    data = {
        'Sale Date': sale_date,
        'Item Description': item_description,
        'eBay Number': ebay_number,
        'Days on Market': days_on_market,
        'List Price': list_price,
        'Sale Price': sale_price
    }

    write_csv(data)

    return redirect(url_for('index'))

@app.route('/export_csv')
def export_csv():
    return send_file(CSV_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
