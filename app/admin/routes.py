from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.admin.forms import ProductForm, UserForm
from app.decorators import admin_required
from app.models import Product, Order, User, OrderItem, Cart, Address

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/orders')
@login_required
@admin_required
def orders():
    # Query all orders in the system and load relationships for each one individually to avoid issues
    orders = Order.query.order_by(Order.order_date.desc()).all()
    # Ensure relationships are loaded by accessing them
    for order in orders:
        # Force the relationships to be loaded
        items = order.items  # This loads the order items
        for item in items:
            _ = item.product  # This loads the product for each item
        _ = order.shipping_address  # This loads the shipping address
        _ = order.customer  # This loads the customer information
    return render_template('admin/orders.html', orders=orders)

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    # Prevent admin from editing their own role/credentials accidentally
    if user.id == current_user.id:
        flash('You cannot edit your own account from here.', 'error')
        return redirect(url_for('admin.users'))
    
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        if form.password.data:  # Only update password if provided
            user.set_password(form.password.data)
        user.role = form.role.data
        
        db.session.commit()
        flash(f'User {user.username} updated successfully!', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # Prevent admin from deleting their own account
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.users'))
    
    # Also delete related records to maintain referential integrity
    # First delete all orders for this user
    from app.models import Order, Cart, Address
    for order in user.orders:
        for item in order.items:
            db.session.delete(item)
        db.session.delete(order)
    
    # Delete cart items and addresses
    for cart_item in user.cart_items:
        db.session.delete(cart_item)
    for address in user.addresses:
        db.session.delete(address)
    
    # Finally delete the user
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/users/<int:user_id>/orders')
@login_required
@admin_required
def user_orders(user_id):
    user = User.query.get_or_404(user_id)
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.order_date.desc()).all()
    # Ensure relationships are loaded
    for order in orders:
        items = order.items
        for item in items:
            _ = item.product
        _ = order.shipping_address
        _ = order.customer
    return render_template('admin/user_orders.html', orders=orders, user=user)

@bp.route('/orders/<int:order_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def order_details(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    # Ensure all relationships are loaded
    _ = order.items  # This loads the order items
    for item in order.items:
        _ = item.product  # This loads the product for each item
    _ = order.shipping_address  # This loads the shipping address
    _ = order.customer  # This loads the customer information
    
    if request.method == 'POST':
        # Handle status update
        new_status = request.form.get('status')
        if new_status in ['PENDING', 'PAID', 'SHIPPED', 'DELIVERED', 'CANCELLED']:
            order.status = new_status
            db.session.commit()
            flash(f'Order status updated to {new_status}', 'success')
            return redirect(url_for('admin.order_details', order_id=order.id))
        else:
            flash('Invalid status', 'error')
    
    return render_template('admin/order_details.html', order=order)

@bp.route('/products')
@login_required
@admin_required
def products():
    products = Product.query.all()
    return render_template('admin/manage_products.html', products=products)

@bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_url=form.image_url.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/_product_form.html', form=form, title='Add Product')

@bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.image_url = form.image_url.data
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/_product_form.html', form=form, title='Edit Product', product=product)

@bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.products'))