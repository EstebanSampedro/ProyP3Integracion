from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class AddUserForm(FlaskForm):
    username = StringField('Nombre Completo', validators=[DataRequired(), Length(min=4, max=50)])
    job_title = StringField('Título del Trabajo', validators=[DataRequired(), Length(min=2, max=35)])
    work_email = StringField('Correo Electrónico del Trabajo', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    country = SelectField('País', choices=[('1', 'País 1'), ('2', 'País 2')])  # Los valores aquí deben corresponder a los IDs de los países en Odoo
    password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(),
        Length(min=6, max=35),
        EqualTo('confirm', message='Las contraseñas deben coincidir')
    ])
    confirm = PasswordField('Repetir Contraseña')
    submit = SubmitField('Agregar Empleado')

class DeleteUserForm(FlaskForm):
    work_email = StringField('Correo Electrónico del Trabajo', validators=[DataRequired(), Email(), Length(min=6, max=35)])
    submit = SubmitField('Eliminar Empleado')
