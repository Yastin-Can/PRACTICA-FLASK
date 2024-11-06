from flask import Flask, render_template, session, request, redirect, url_for, flash
from models.user import User
from models.amigos import Amigos
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main'))
    return render_template('dashboard.html')

@app.route('/friends')
def friends():
    if 'user_id' not in session:
        return redirect(url_for('main'))
    
    user_id = session['user_id']
    user_friends = Amigos.get_friends(user_id)  
    other_users = User.get_non_friends(user_id) 
    
    return render_template('friends.html', friends=user_friends, other_users=other_users)


@app.route('/add_friend/<int:friend_id>', methods=['POST'])
def add_friend(friend_id):
    if 'user_id' not in session:
        return redirect(url_for('main'))
    
    user_id = session['user_id']
    Amigos.add_friend(user_id, friend_id)
    flash("Amigo añadido con éxito", "success")
    return redirect(url_for('friends'))

@app.route('/remove_friend/<int:friend_id>', methods=['POST'])
def remove_friend(friend_id):
    if 'user_id' not in session:
        return redirect(url_for('main'))
    
    user_id = session['user_id']
    Amigos.remove_friend(user_id, friend_id)
    flash("Amigo eliminado con éxito", "success")
    return redirect(url_for('friends'))

# INICIAR SESION

@app.route('/')
def main():
    return render_template('index.html', login_errors=[], register_errors=[])

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]
    password2 = request.form["password2"]

    errors = []

    if not first_name or len(first_name) < 3:
        errors.append("Nombre inválido")
    if not last_name or len(last_name) < 3:
        errors.append("Apellido inválido")
    if not email or len(email) < 3:
        errors.append("Email inválido")
    if password != password2:
        errors.append("Las contraseñas no coinciden")
    if len(password) < 4:  
        errors.append("La contraseña debe tener al menos 4 caracteres")

    existing_user = User.get_by_email(email)
    if existing_user:
        errors.append("El usuario ya está registrado")

    if errors:
        return render_template("index.html", register_errors=errors, login_errors=[])

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User.insert_one(first_name, last_name, email, password_hash)
    
    session['user_id'] = user.id
    session['first_name'] = user.first_name

    return redirect(url_for('friends'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.get_by_email(email)

    if not user or not bcrypt.check_password_hash(user.password, password):
        return render_template("index.html", login_errors=["Email o contraseña incorrectos"], register_errors=[])

    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name

    return redirect(url_for('friends'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('main'))

#ver perfil del usuario

@app.route('/verPerfil/<int:user_id>', methods=['GET', 'POST'])
def ver_perfil(user_id):
    if 'user_id' not in session:
        return redirect(url_for('main'))
    
    user = User.get_by_id(user_id)
    if not user:
        flash("Usuario no encontrado", "danger")
        return redirect(url_for('friends'))

    is_friend = Amigos.are_friends(session['user_id'], user_id)
    
    return render_template('verPerfil.html', user=user, is_friend=is_friend)


if __name__ == '__main__':
    app.run(debug=True)
