from flask import Blueprint, render_template, redirect, url_for, flash
from dotenv import load_dotenv
import os
from .forms import AddUserForm, DeleteUserForm
from .odoo_service import OdooService  # Asegúrate de que este import esté correcto

# Carga las variables de entorno
load_dotenv()

# Accede a las variables de entorno para configurar las credenciales de Odoo
endpoint = os.getenv('ODOO_URL')
database = os.getenv('ODOO_DB')
user_email = os.getenv('ODOO_EMAIL')
user_password = os.getenv('ODOO_PASSWORD')

odoo = OdooService(endpoint=endpoint, database=database, user_email=user_email, user_password=user_password)

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
        country = form.country.data  # Asegúrate de manejar correctamente el ID del país
        # Crea el empleado en Odoo usando el método correcto
        new_employee_id = odoo.register_employee(name, job_title, work_email, country)
        if new_employee_id:
            flash('Empleado agregado exitosamente con ID: {}'.format(new_employee_id))
        else:
            flash('Hubo un error al agregar el empleado.')
        return redirect(url_for('main.menu_principal'))
    return render_template('crear_usuario.html', form=form)


@main.route('/eliminar_usuario', methods=['GET', 'POST'])
def eliminar_usuario():
    form = DeleteUserForm()
    if form.validate_on_submit():
        work_email = form.work_email.data
        # Elimina el empleado en Odoo
        result = odoo.delete_employee(work_email)
        if result:
            flash('Empleado eliminado exitosamente')
        else:
            flash('Hubo un error al eliminar el empleado.')
        return redirect(url_for('main.menu_principal'))
    return render_template('eliminar_usuario.html', form=form)
