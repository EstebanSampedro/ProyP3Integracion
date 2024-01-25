from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def menu_principal():
    return render_template('menu_principal.html')

@main.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    # Aquí incluirás la lógica para crear un usuario
    return render_template('crear_usuario.html')

@main.route('/eliminar_usuario', methods=['GET', 'POST'])
def eliminar_usuario():
    # Aquí incluirás la lógica para eliminar un usuario
    return render_template('eliminar_usuario.html')
