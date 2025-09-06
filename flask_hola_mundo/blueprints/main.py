# Blueprint para las páginas principales (inicio y acerca)
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/acerca')
def acerca():
    return render_template('acerca.html')
