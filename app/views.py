from flask import Blueprint, render_template, redirect, url_for, flash
import os
from dotenv import load_dotenv
from .forms import AddUserForm, DeleteUserForm
from .nextcloud import NextcloudService
from .odoo_service import OdooService

# Carga las variables de entorno
load_dotenv()

# Configuración de las credenciales de Odoo
endpoint = os.getenv('ODOO_URL')
database = os.getenv('ODOO_DB')
user_email = os.getenv('ODOO_EMAIL')
user_password = os.getenv('ODOO_PASSWORD')

# Configuración de las credenciales de Nextcloud
nextcloud_url = os.getenv('NEXTCLOUD_URL')
nextcloud_user = os.getenv('NEXTCLOUD_USERNAME')
nextcloud_password = os.getenv('NEXTCLOUD_PASSWORD')

# Instancia de los servicios de Odoo y Nextcloud
odoo = OdooService(endpoint=endpoint, database=database, user_email=user_email, user_password=user_password)
nextcloud = NextcloudService(url=nextcloud_url, username=nextcloud_user, password=nextcloud_password)

main = Blueprint('main', __name__)

@main.route('/')
def menu_principal():
    return render_template('menu_principal.html')

@main.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    form = AddUserForm()
    if form.validate_on_submit():
        name = form.username.data
        job_title = form.job_title.data
        work_email = form.work_email.data
        password = form.password.data  # Asegúrate de que esta línea esté presente en tu AddUserForm

        # Intentar crear el empleado en Odoo
        odoo_response = odoo.register_employee(name, job_title, work_email, password)  # Asumiendo que esta función retorna un booleano
        if odoo_response:
            print(f'Empleado {name} creado en Odoo con ID: {odoo_response}')
            flash(f'Empleado {name} creado en Odoo con ID: {odoo_response}')
            # Intentar crear el usuario en Nextcloud
            nc_response = nextcloud.create_user(userid=work_email, password=password, email=work_email, displayname=name)
            if nc_response.status_code == 200:
                print(f'Usuario {work_email} creado en Nextcloud.')
                flash('Usuario creado exitosamente en Nextcloud.')
            else:
                print(f'Error al crear usuario en Nextcloud: {nc_response.status_code} {nc_response.text}')
                flash(f'Error al crear usuario en Nextcloud: {nc_response.status_code} {nc_response.text}')
        else:
            print('Error al agregar el empleado en Odoo.')
            flash('Hubo un error al agregar el empleado en Odoo.')

        return redirect(url_for('main.menu_principal'))
    return render_template('crear_usuario.html', form=form)

@main.route('/eliminar_usuario', methods=['GET', 'POST'])
def eliminar_usuario():
    form = DeleteUserForm()
    if form.validate_on_submit():
        work_email = form.work_email.data

        # Intentar eliminar el empleado en Odoo
        odoo_result = odoo.remove_employee(work_email)
        if odoo_result:
            print(f'Empleado con email {work_email} eliminado de Odoo.')
            flash('Empleado eliminado exitosamente de Odoo.')
            
            # Intentar eliminar el usuario en Nextcloud
            nc_response = nextcloud.delete_user(userid=work_email)
            if nc_response.status_code == 200:
                print(f'Usuario {work_email} eliminado de Nextcloud.')
                flash('Usuario eliminado exitosamente de Nextcloud.')
            else:
                print(f'Error al eliminar usuario de Nextcloud: {nc_response.status_code} {nc_response.text}')
                flash(f'Error al eliminar usuario de Nextcloud: {nc_response.status_code} {nc_response.text}')
        else:
            print('Error al eliminar el empleado de Odoo.')
            flash('Hubo un error al eliminar el empleado en Odoo.')

        return redirect(url_for('main.menu_principal'))
    return render_template('eliminar_usuario.html', form=form)

