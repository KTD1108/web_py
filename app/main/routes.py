from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.main.forms import AddToCartForm, AddressForm
from app.models import Product, Cart, Address, Order, OrderItem


@bp.route('/')
def home():
    products = Product.query.all()
    return render_template('main/home.html', products=products)


@bp.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    form = AddToCartForm()
    return render_template('main/product_detail.html', product=product, form=form)


@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddToCartForm()
    
    if form.validate_on_submit():
        # Check if item already exists in cart
        cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        
        if cart_item:
            cart_item.quantity += form.quantity.data
        else:
            cart_item = Cart(
                user_id=current_user.id,
                product_id=product_id,
                quantity=form.quantity.data
            )
            db.session.add(cart_item)
        
        db.session.commit()
        flash(f'{product.name} added to cart!', 'success')
    
    return redirect(url_for('main.product_detail', id=product_id))


@bp.route('/cart')
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = 0
    
    for item in cart_items:
        total += item.product.price * item.quantity
    
    return render_template('main/cart.html', cart_items=cart_items, total=total)


@bp.route('/update_cart/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = Cart.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
    else:
        db.session.delete(cart_item)
    
    db.session.commit()
    flash('Cart updated successfully!', 'success')
    return redirect(url_for('main.view_cart'))


@bp.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = Cart.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.', 'info')
    return redirect(url_for('main.view_cart'))


@bp.route('/addresses')
@login_required
def addresses():
    user_addresses = Address.query.filter_by(user_id=current_user.id).all()
    address_form = AddressForm()
    return render_template('main/addresses.html', addresses=user_addresses, form=address_form)


@bp.route('/addresses/add', methods=['POST'])
@login_required
def add_address():
    form = AddressForm()
    
    if form.validate_on_submit():
        # If setting as default, unset other default addresses
        if form.is_default.data:
            Address.query.filter_by(user_id=current_user.id, is_default=True).update(dict(is_default=False))
        
        address = Address(
            user_id=current_user.id,
            full_name=form.full_name.data,
            phone=form.phone.data,
            street=form.street.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            is_default=form.is_default.data
        )
        
        db.session.add(address)
        db.session.commit()
        flash('Address added successfully!', 'success')
    
    return redirect(url_for('main.addresses'))


@bp.route('/addresses/edit/<int:address_id>', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    address = Address.query.filter_by(id=address_id, user_id=current_user.id).first_or_404()
    form = AddressForm(obj=address)
    
    if form.validate_on_submit():
        # If setting as default, unset other default addresses
        if form.is_default.data:
            Address.query.filter_by(user_id=current_user.id, is_default=True).update(dict(is_default=False))
        
        address.full_name = form.full_name.data
        address.phone = form.phone.data
        address.street = form.street.data
        address.city = form.city.data
        address.state = form.state.data
        address.zip_code = form.zip_code.data
        address.is_default = form.is_default.data
        
        db.session.commit()
        flash('Address updated successfully!', 'success')
        return redirect(url_for('main.addresses'))
    
    return render_template('main/edit_address.html', form=form, address=address)


@bp.route('/addresses/delete/<int:address_id>', methods=['POST'])
@login_required
def delete_address(address_id):
    address = Address.query.filter_by(id=address_id, user_id=current_user.id).first_or_404()
    db.session.delete(address)
    db.session.commit()
    flash('Address deleted successfully!', 'success')
    return redirect(url_for('main.addresses'))


@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('main.home'))
    
    # Calculate total amount
    total_amount = 0
    for item in cart_items:
        total_amount += item.product.price * item.quantity
    
    user_addresses = Address.query.filter_by(user_id=current_user.id).all()
    
    if request.method == 'POST':
        shipping_address_id = request.form.get('shipping_address_id')
        
        if not shipping_address_id:
            flash('Please select a shipping address.', 'error')
            return render_template('main/checkout.html', cart_items=cart_items, addresses=user_addresses, total=total_amount)
        
        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            shipping_address_id=shipping_address_id
        )
        
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Create order items
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.delete(item)  # Remove from cart
        
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('main.order_success', order_id=order.id))
    
    return render_template('main/checkout.html', cart_items=cart_items, addresses=user_addresses, total=total_amount)


@bp.route('/order_success/<int:order_id>')
@login_required
def order_success(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    # Force the relationships to be loaded
    items = order.items  # This loads the order items
    for item in items:
        _ = item.product  # This loads the product for each item
    _ = order.shipping_address  # This loads the shipping address
    return render_template('main/order_success.html', order=order)

@bp.route('/order_details/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    # Force the relationships to be loaded
    items = order.items  # This loads the order items
    for item in items:
        _ = item.product  # This loads the product for each item
    _ = order.shipping_address  # This loads the shipping address
    return render_template('main/order_details.html', order=order)


@bp.route('/my_orders')
@login_required
def my_orders():
    # Query orders and load relationships for each one individually to avoid issues
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    # Ensure relationships are loaded by accessing them
    for order in orders:
        # Force the relationships to be loaded
        items = order.items  # This loads the order items
        for item in items:
            _ = item.product  # This loads the product for each item
        _ = order.shipping_address  # This loads the shipping address
    return render_template('main/my_orders.html', orders=orders)