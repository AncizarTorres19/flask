# Blueprint para la funcionalidad de contacto
from flask import Blueprint, render_template

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contacto')
def contacto():
    return render_template('contacto.html')
