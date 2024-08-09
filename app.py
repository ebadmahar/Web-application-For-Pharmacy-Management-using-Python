from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import subprocess

app = Flask(__name__, static_folder='static', template_folder='templates')

app.secret_key = '48cd369636bff56ccdcaa972f3119032'

medicines = []

users = {
    "admin": "12345678",
    "operator": "12345678"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' in session and session['username'] == 'admin':
        if request.method == 'POST':
            if 'delete' in request.form:
                name_to_delete = request.form.get('delete')
                global medicines
                medicines = [med for med in medicines if med['name'] != name_to_delete]
            else:
                name = request.form.get('name')
                quantity = request.form.get('quantity')
                price = request.form.get('price')
                expiry_date = request.form.get('expiry_date')
                medicines.append({
                    'name': name,
                    'quantity': quantity,
                    'price': price,
                    'expiry_date': expiry_date
                })
            return redirect(url_for('admin'))
        
        search_query = request.args.get('search', '')
        filtered_medicines = [med for med in medicines if search_query.lower() in med['name'].lower()]
        return render_template('admin.html', medicines=filtered_medicines)
    else:
        return redirect(url_for('login'))

@app.route('/operator', methods=['GET', 'POST'])
def operator():
    if 'username' in session and session['username'] == 'operator':
        if request.method == 'POST':
            name = request.form.get('name')
            new_quantity = request.form.get('quantity')
            for med in medicines:
                if med['name'] == name:
                    med['quantity'] = new_quantity
                    break
            return redirect(url_for('operator'))
        
        search_query = request.args.get('search', '')
        filtered_medicines = [med for med in medicines if search_query.lower() in med['name'].lower()]
        return render_template('operator.html', medicines=filtered_medicines)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if users.get(username) == password:
            session['username'] = username
            if username == 'admin':
                return redirect(url_for('admin'))
            elif username == 'operator':
                return redirect(url_for('operator'))
        else:
            return render_template('login.html', error=True)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
