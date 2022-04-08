import flask
import datetime
from data import db_session
from data.product import Products
from data.users import User
from flask import jsonify, render_template

blueprint = flask.Blueprint(
    'products_api',
    __name__,
    template_folder='templates'
)
product_list = []


@blueprint.route('/products/<int:id>')
def open_product(id):
    global product_list
    product_list.clear()
    db_sess = db_session.create_session()
    products = db_sess.query(Products).get(id)
    users = db_sess.query(User).get(products.company_id)
    product_list.append(products.title)
    product_list.append(str(datetime.datetime.now())[0:10])

    if not products:
        return jsonify({'error': 'Not found'})
    return render_template('one_product.html', products=products, users=users)
