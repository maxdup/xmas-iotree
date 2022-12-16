from flask import Blueprint, render_template

bp_webapp = Blueprint('iot_webapp', __name__)


@bp_webapp.route('/', methods=['GET'])
def home():
    return render_template('/index.html')


@bp_webapp.route('/<path:dummy>')
def fallback(dummy):
    return render_template('/index.html')
