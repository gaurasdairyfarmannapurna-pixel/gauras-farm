from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize a lightweight local SQL database
def init_db():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, phone TEXT, address TEXT, 
            breed TEXT, time_pref TEXT, volume TEXT, duration TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route 1: Handle form submissions from order.html
@app.route('/submit-order', methods=['POST'])
def submit_order():
    name = request.form.get('Customer Name')
    phone = request.form.get('Customer Phone')
    address = request.form.get('Delivery Destination')
    breed = request.form.get('Milk Breed Variety')
    time_pref = request.form.get('Delivery Schedule Preference')
    volume = request.form.get('Volume Per Day')
    duration = request.form.get('Subscription Length')

    # Save to our local database
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (name, phone, address, breed, time_pref, volume, duration)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, address, breed, time_pref, volume, duration))
    conn.commit()
    conn.close()

    # Smoothly redirect directly to your billing placeholder page
    return redirect('/billing.html')

# Route 2: Your Live Admin Dashboard Panel
@app.route('/annapurna')
def dashboard():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()

    # A clean, milky-themed admin panel view matching your site
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gauras Hub — Admin Panel</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { background-color: #FDFBF7; color: #1D1D1F; font-family: -apple-system, sans-serif; padding: 20px; }
            .panel { max-width: 800px; margin: 0 auto; background: #FFF; border: 1px solid #F2EFE9; padding: 24px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
            h2 { border-bottom: 2px solid #F2EFE9; padding-bottom: 12px; }
            .order-card { background: #FDFBF7; border: 1px solid #F2EFE9; padding: 16px; border-radius: 12px; margin-bottom: 12px; }
            .meta { color: #6E6E73; font-size: 13px; margin-bottom: 6px; }
            .phone-link { color: #C5A880; font-weight: bold; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="panel">
            <h2>Gauras Dairy Request Hub Dashboard</h2>
            <p style="color: #6E6E73;">Total Logged Allocations: {{ rows|length }}</p>
            {% if not rows %}
                <p style="margin-top:20px; color:#6E6E73;">No requests incoming yet.</p>
            {% endif %}
            {% for row in rows %}
                <div class="order-card">
                    <div class="meta">ID: #{{ row[0] }} | Breed: <strong>{{ row[4] }}</strong> | Preference: <strong>{{ row[5] }}</strong></div>
                    <div style="font-size: 18px; font-weight: bold; margin-bottom: 4px;">{{ row[1] }}</div>
                    <p style="margin: 4px 0;">📍 {{ row[3] }}</p>
                    <p style="margin: 4px 0;">🥛 {{ row[6] }} Ltrs / Day for {{ row[7] }} Days</p>
                    <p style="margin-top: 8px;">📞 Call to Verify: <a class="phone-link" href="tel:{{ row[2] }}">{{ row[2] }}</a></p>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template, rows=rows)

# Static file routers to serve your HTML pages on the same port
@app.route('/')
def home(): return open('index.html').read()
@app.route('/order.html')
def order_page(): return open('order.html').read()
@app.route('/billing.html')
def bill_page(): return open('billing.html').read()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
