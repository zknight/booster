from booster import app, db
from booster.models import Product, Picture
from flask import render_template, url_for, redirect, session, flash
from booster.stuff import protected
from flask.ext.wtf import Form
from wtforms.fields import *
from wtforms.validators import *

@app.route("/store")
def store_index():
    products = Product.query.filter(Product.instock == True).all()
    return render_template("store.html", products = products)

#############
# admin views
#############
@app.route("/store/admin")
@protected("/store")
def store_admin():
    products = Product.query.all()
    return render_template("admin/store.html", products = products)

@app.route("/store/admin/product/add", methods=['GET', 'POST'])
@protected("/store")
def add_product():
    product_form = ProductForm()

    if product_form.validate_on_submit():
        new_product = Product(
                name=product_form.name.data,
                description=product_form.description.data,
                instock=product_form.instock.data,
                dollars=product_form.dollars.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product {0} added. Now attach pictures.".format(new_product.name))
        return redirect(url_for('store_admin'))
    
    return render_template("admin/product_form.html",
            product_form = product_form,
            action = url_for('add_product'))

@app.route("/store/admin/product/edit/<pid>", methods=['GET', 'POST'])
@protected("/store")
def edit_product(pid):
    p = Product.query.filter(Product.id==pid).first()
    if not p:
        return redirect(url_for('store_admin'))
    product_form = ProductForm(obj=p)
    if product_form.validate_on_submit():
        p.name = product_form.name.data
        p.description = product_form.description.data
        p.instock = product_form.instock.data
        p.dollars = product_form.dollars.data

        db.session.commit()
        return redirect(url_for('store_admin'))

    return render_template("admin/product_form.html",
            product_form = product_form,
            action = url_for('edit_product', pid = p.id))

@app.route("/store/admin/product/delete/<pid>")
@protected("/store")
def delete_product(pid):
    p = Product.query.filter(Product.id==pid).first()
    if not p:
        flash("No valid product with that id.")
    else:
        db.session.delete(p)
        db.session.commit()
        flash("Event deleted.")
    return redirect(url_for('store_admin'))

@app.route("/store/admin/product/togglestock/<pid>")
@protected("/store")
def toggle_stock(pid):
    p = Product.query.filter(Product.id==pid).first()
    if not p:
        flash("No valid product with that id.")
    else:
        p.instock = not p.instock
        db.session.commit()
    return redirect(url_for('store_admin'))

@app.route("/store/admin/product/<pid>/addpic")
@protected("/store")
def add_picture(pid):
    p = Product.query.filter(Product.id==pid).first()
    if not p:
        flash("No valid product with that id.")
    else:
        pass
#TODO add form for adding picture
    return redirect(url_for('store_admin'))

##############
# Product Form
##############
class ProductForm(Form):
    name = TextField("Product Name", validators=[
        Length(min=3, max=128,
            message="Name must have at least 3 characters but no more " 
            "than 128"),
        Regexp(("[0-9a-zA-Z_-]"), 
            message="Name can't contain non-alphanumeric characters")
        ])

    description = TextAreaField("Product Description", validators=[
        InputRequired(message="Text Input Required")
        ])

    instock = BooleanField("In Stock?", default=True)

    dollars = DecimalField("Price $", validators=[
        InputRequired(message="Please enter a price")
        ])

