from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  

@app.before_request
def before_request():
    if 'productos' not in session:
        session['productos'] = []
        session['ultimo_id'] = 0

@app.route('/')
def index():
    
    nombre = session.get('nombre', 'No definido')
    carnet = session.get('carnet', 'No definido')
    return render_template('index.html', productos=session['productos'], nombre=nombre, carnet=carnet)

@app.route('/set_student', methods=['POST'])
def set_student():
    session['nombre'] = request.form['nombre']
    session['carnet'] = request.form['carnet']
    return redirect(url_for('index'))

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        
        session['ultimo_id'] = session.get('ultimo_id', 0) + 1
        
        nuevo_producto = {
            'id': session['ultimo_id'],
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }

        productos = session['productos']
        productos.append(nuevo_producto)
        session['productos'] = productos  
        
        return redirect(url_for('index'))
    
    return render_template('agregar_producto.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session['productos']
    producto = next((p for p in productos if p['id'] == id), None)
    
    if request.method == 'POST':
        # Actualizar producto
        producto.update({
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        })
        session['productos'] = productos  
        return redirect(url_for('index'))
    
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    productos = session['productos']
    session['productos'] = [p for p in productos if p['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
