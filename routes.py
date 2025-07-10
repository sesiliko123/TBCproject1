import os
from flask import render_template, redirect, flash, abort, request, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from ext import app, db
from forms import RegisterForm, LoginForm, ProductForm, ProfileImageForm, CategoryForm
from models import CartItem, Order
from models import User, Product
from forms import ReviewForm
from models import Review


@app.route('/')
def home():
    categories = [
        {"name": "მობილური", "emoji": "📱"},
        {"name": "ლეპტოპი", "emoji": "💻"},
        {"name": "ტაბი", "emoji": "📲"},
        {"name": "ტელევიზორი", "emoji": "📺"},
        {"name": "მონიტორი", "emoji": "🖥️"},
        {"name": "კონსოლი", "emoji": "🎮"},
        {"name": "ყურსასმენი", "emoji": "🎧"},
        {"name": "სმარტ საათი", "emoji": "⌚"},
    ]
    selected_category = request.args.get("category")
    produktebi = Product.query.all()
    return render_template("index.html", produktebi=produktebi, selected_category=selected_category, categories=categories)

@app.route('/category/<category_name>')
def products_by_category(category_name):
    produktebi = Product.query.filter_by(category=category_name).all()

    category_emojis = {
        "მობილური": "📱",
        "ტაბი": "📲",
        "ლეპტოპი": "💻",
        "ტელევიზორი": "📺",
        "მონიტორი": "🖥️",
        "კონსოლი": "🎮",
        "ყურსასმენი": "🎧",
        "სმარტ საათი": "⌚"
    }

    emoji = category_emojis.get(category_name, "📦")

    return render_template(
        'index.html',
        produktebi=produktebi,
        selected_category=category_name,
        selected_emoji=emoji
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('მომხმარებელი ამ სახელით უკვე არსებობს, სცადეთ სხვა.', 'danger')
            return render_template('register.html', form=form)

        user = User(
            username=form.username.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data
        )
        db.session.add(user)
        db.session.commit()
        flash('რეგისტრაცია წარმატებით დასრულდა. ახლა შედით სისტემაში.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("წარმატებით გამოხვედით სისტემიდან", "info")
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("სისტემაში შესვლა წარმატებით შესრულდა", "success")
            return redirect(url_for('profile'))
        else:
            flash("მომხმარებელი ან პაროლი არასწორია", "danger")

    return render_template('login.html', form=form)

@app.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    if 'selected_category' not in session:
        return redirect(url_for('choose_category'))

    selected_category = session['selected_category']
    form = ProductForm()

    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image = form.image.data
            filename = secure_filename(image.filename)
            image_path = os.path.join('static/images', filename)
            image.save(image_path)
            image_file = filename

        product = Product(
            category=selected_category,
            name=form.name.data,
            price=form.price.data,
            image=image_file,
            storage=form.storage.data,
            ram=form.ram.data,
            screen_size=form.screen_size.data,
            resolution=form.resolution.data,
            refresh_rate=form.refresh_rate.data,
            screen_type=form.screen_type.data,
            bluetooth=form.bluetooth.data,
            battery=form.battery.data,
            noise_cancellation=form.noise_cancellation.data,
            charging_time=form.charging_time.data,
            type_c=form.type_c.data,
            processor=form.processor.data,
            cores=form.cores.data,
            frequency=form.frequency.data,
            viewing_angle=form.viewing_angle.data,
            work_time=form.work_time.data,
            user_id=current_user.id
        )

        db.session.add(product)
        db.session.commit()

        flash("✅ პროდუქტი წარმატებით დაემატა!", "success")
        session.pop('selected_category', None)
        return redirect(url_for('home'))

    return render_template('create_product.html', form=form, selected_category=selected_category)
@app.route('/choose_category', methods=['GET', 'POST'])
@login_required
def choose_category():
    form = CategoryForm()
    if form.validate_on_submit():
        session['selected_category'] = form.category.data
        return redirect(url_for('create_product'))
    return render_template('choose_category.html', form=form)
@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if current_user.role != "Admin":
        abort(403)

    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    selected_category = product.category

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data
        product.storage = form.storage.data
        product.ram = form.ram.data
        product.screen_size = form.screen_size.data
        product.resolution = form.resolution.data
        product.refresh_rate = form.refresh_rate.data
        product.screen_type = form.screen_type.data
        product.bluetooth = form.bluetooth.data
        product.battery = form.battery.data
        product.noise_cancellation = form.noise_cancellation.data
        product.charging_time = form.charging_time.data
        product.type_c = form.type_c.data
        product.processor = form.processor.data
        product.cores = form.cores.data
        product.frequency = form.frequency.data
        product.viewing_angle = form.viewing_angle.data
        product.work_time = form.work_time.data

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join('static/images', filename)
            form.image.data.save(image_path)
            product.image = filename

        db.session.commit()
        flash("✔️ პროდუქტი წარმატებით განახლდა", "success")
        return redirect(url_for("product_detail", product_id=product.id))

    return render_template("edit_product.html", form=form, product=product, selected_category=selected_category)

@app.route("/delete_product/<int:product_id>", methods=["POST"])  # მხოლოდ POST!
@login_required
def delete_product(product_id):
    if current_user.role != "Admin":
        abort(403)

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("🗑️ პროდუქტი წაიშალა", "success")
    return redirect("/")

@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        new_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=1)
        db.session.add(new_item)

    db.session.commit()
    flash("🛒 პროდუქტი დაემატა კალათაში", "success")
    return redirect(url_for('home'))

@app.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in items)
    return render_template('cart.html', cart_items=items, total=total)

@app.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('პროდუქტი წაიშალა კალათიდან', 'warning')
    return redirect(url_for('cart'))

@app.route("/search")
def search():
    query = request.args.get("q", "")
    if query:
        results = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    else:
        results = []
    return render_template("search_results.html", query=query, results=results)

@app.route('/increase_quantity/<int:item_id>')
@login_required
def increase_quantity(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    item.quantity += 1
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/decrease_quantity/<int:item_id>')
@login_required
def decrease_quantity(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        abort(403)
    if item.quantity > 1:
        item.quantity -= 1
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('cart'))
@app.route('/checkout')
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not items:
        flash("🛒 კალათა ცარიელია", "info")
        return redirect(url_for('cart'))

    total = sum(item.product.price * item.quantity for item in items)

    for item in items:
        order = Order(
            user_id=current_user.id,
            product_id=item.product.id,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity
        )
        db.session.add(order)
        db.session.delete(item)

    db.session.commit()

    flash(f"✅ გადახდა წარმატებით დასრულდა! ჯამური თანხა: {total} ₾", "success")
    return render_template('checkout.html', total=total)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileImageForm()

    if form.validate_on_submit():
        if form.profile_image.data:
            image_file = form.profile_image.data
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.root_path, 'static/images', filename)
            image_file.save(image_path)

            current_user.profile_image = filename
            db.session.commit()
            flash("პროფილის ფოტო განახლდა", "success")
            return redirect(url_for('profile'))
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date_ordered.desc()).all()
    return render_template('profile.html', user=current_user, form=form, orders=orders)

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')


        flash("შეტყობინება წარმატებით გაიგზავნა! მალე დაგიკავშირდებით.", "success")

        return redirect(url_for('contact'))

    return render_template('contact.html')
@app.route('/filter_by_custom_price')
def filter_by_custom_price():
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Product.query
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    produktebi = query.all()
    return render_template('index.html', produktebi=produktebi)

@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    review_form = ReviewForm()

    # საშუალო შეფასება
    reviews = product.reviews
    avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else 0

    # POST მეთოდის დამუშავება
    if review_form.validate_on_submit():
        if current_user.is_authenticated:
            new_review = Review(
                rating=review_form.rating.data,
                comment=review_form.comment.data,
                product_id=product.id,
                user_id=current_user.id
            )
            db.session.add(new_review)
            db.session.commit()
            flash('კომენტარი წარმატებით დაემატა!', 'success')
            return redirect(url_for('product_detail', product_id=product.id))
        else:
            flash('შესვლა აუცილებელია კომენტარის დასამატებლად.', 'danger')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        flash('ფორმა არ არის ვალიდური. გთხოვ შეავსე ყველა ველი.', 'danger')

    return render_template('product_detail.html', product=product, review_form=review_form, avg_rating=avg_rating)
@app.route("/product_count")
def product_count():
    return f"პროდუქტების რაოდენობაა: {Product.query.count()}"