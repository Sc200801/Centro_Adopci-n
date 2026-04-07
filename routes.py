from flask import Flask, render_template, request, redirect, url_for
import database
import models

app = Flask(__name__)

@app.route('/')
def index():
    # Recuperamos los perros del catálogo real
    dogs_data = database.get_available_dogs()
    # Podemos convertir los datos a objetos 'Dog' si quisiéramos usar métodos de la clase
    available_dogs = [models.Dog(row[0], row[1], row[2], row[3]) for row in dogs_data]
    
    return render_template('catalogo.html', dogs=available_dogs)

@app.route('/adoptar/<int:dog_id>')
def form_adopcion(dog_id):
    dog = database.get_dog_by_id(dog_id)
    if not dog:
        return "Perrito no encontrado", 404
    dog_obj = models.Dog(dog[0], dog[1], dog[2], dog[3])
    return render_template('confirmacion.html', dog=dog_obj)

@app.route('/historial')
def historial():
    adopciones = database.get_adoption_history()
    return render_template('historial.html', adopciones=adopciones)


@app.route('/confirmar_adopcion', methods=['POST'])
def procesar_adopcion():
    # Recibimos datos del formulario de la web
    dog_id = request.form['dog_id']
    name = request.form['name']
    lastname = request.form['lastname']
    address = request.form['address']
    id_card = request.form['id_card']
    
    # Ejecutamos la lógica de negocio modular
    success = database.register_adoption_transactional(dog_id, name, lastname, address, id_card)
    
    if success:
        dog = database.get_dog_by_id(dog_id)
        return render_template('exito.html', dog_name=dog[1])
    else:
        # --- REUTILIZACIÓN DE PLANTILLA PARA ERROR ---
        # Volvemos a obtener los datos del perro para que la página de confirmación no falle
        dog = database.get_dog_by_id(dog_id)
        dog_obj = models.Dog(dog[0], dog[1], dog[2], dog[3])
        
        # Renderizamos la misma plantilla pero enviando la variable 'error'
        return render_template('confirmacion.html', 
                               dog=dog_obj, 
                               error="Error al procesar la adopción. Por favor, inténtalo de nuevo.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)