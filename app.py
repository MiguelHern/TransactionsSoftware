from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from models import db, User, Library  

app = Flask(__name__)
app.config.from_object(Config)

# Inicializa la instancia de SQLAlchemy
db.init_app(app)

# Inicializa Flask-Migrate
migrate = Migrate(app, db)

@app.route('/')
def index():
    libraries = Library.query.all()
    return render_template('base.html', libraries=libraries)


@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        # Para agregar un nuevo usuario
        user_name = request.form['user_name']
        major = request.form['major']
        email = request.form['email']
        phone_number = request.form['phone_number']
        address = request.form['address']

        new_user = User(user_name=user_name, major=major, email=email, phone_number=phone_number, address=address)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!')

        return redirect(url_for('manage_users'))

    # Obtener todos los usuarios
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    
    if request.form['_method'] == 'PUT':
        user = User.query.get(user_id)
        user.user_name = request.form['user_name']
        user.major = request.form['major']
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        user.address = request.form['address']
        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('manage_users'))

    elif request.form['_method'] == 'DELETE':
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!')
        return redirect(url_for('manage_users'))
    

    










if __name__ == '__main__':
    app.run(debug=True)
