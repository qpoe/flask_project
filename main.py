from flask import Flask
from flask import render_template
from flask import redirect
from data import db_session, products_blueprint, profile_blueprint
from forms.register import RegisterForm
import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.login import LoginForm
from data.users import User
from forms.product_form import ProductForm
from data.product import Products
from data.buy import Buy
from data.products_blueprint import product_list
from flask import request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Почта уже зарегистрирована, авторизуйтесь")
        if db_sess.query(User).filter(User.login == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if len(form.password.data) < 8:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароль содержит меньше 8 символов")
        user = User(
            login=form.name.data,
            email=form.email.data,
            is_company=form.company.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
@app.route('/main_page')
def main_page():
    search = request.args.get('search')
    db_sess = db_session.create_session()
    if search:
        products = db_sess.query(Products).filter(Products.title.contains(search) |
                                                  Products.description.contains(search) |
                                                  Products.price.contains(search))
    else:
        products = db_sess.query(Products)
    return render_template('main_page.html', products=products)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/register")


@app.route('/my_products')
@login_required
def my_products():
    db_sess = db_session.create_session()
    products = db_sess.query(Products).filter(Products.company_id == current_user.id)
    if not current_user.is_company:
        return render_template("deny.html")
    return render_template("products_company.html", products=products)


@app.route('/add_products', methods=['GET', 'POST'])
@login_required
def add_products():
    if not current_user.is_company:
        return render_template("deny.html")
    form = ProductForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        products = Products(
            title=form.title.data,
            description=form.description.data,
            city=form.city.data,
            price=form.price.data,
            company_id=current_user.id,
            created_date=str(datetime.datetime.now())
        )
        db_sess.add(products)
        db_sess.commit()
        return redirect('/my_products')
    return render_template('add_products.html', title='Добавление продуктов',
                           form=form)


@app.route('/add_to_basket')
@login_required
def add_to_basket():
    if current_user.is_company:
        return render_template("deny.html")
    db_sess = db_session.create_session()
    buyings = Buy(
        title=product_list[0],
        created_date=product_list[1],
        user_id=current_user.id,
    )
    db_sess.add(buyings)
    db_sess.commit()
    return render_template("success_buy.html")


@app.route('/buyings')
@login_required
def buyings():
    if current_user.is_company:
        return render_template("deny.html")
    db_sess = db_session.create_session()
    buyings = db_sess.query(Buy).filter(Buy.user_id == current_user.id)
    return render_template("buying.html", buyings=buyings)


def main():
    db_session.global_init("db/clients.db")
    app.register_blueprint(products_blueprint.blueprint)
    app.register_blueprint(profile_blueprint.blueprint)
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
