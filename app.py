from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__)

# Function to fetch products from the database based on search term
def get_products(search_term):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_term + '%',))
    products = cursor.fetchall()
    conn.close()
    return products

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['searchInput']
    products = get_products(search_term)
    return render_template('search_res.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image_url = request.form['image_url']
        categories= request.form['categories']
        
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, price, image_url, categories) VALUES (?, ?, ?, ?)", (name, price, image_url, categories))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(debug=True)
