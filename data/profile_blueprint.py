import flask

from data import db_session
from data.users import User
from flask import jsonify, render_template
from flask_login import login_required
blueprint = flask.Blueprint(
    'profile_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/profile/<int:id>')
@login_required
def profile(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(id)
    return render_template('profile.html', users=users)