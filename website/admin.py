from flask import Blueprint, render_template, flash, send_from_directory, redirect
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer
from . import db


admin = Blueprint('admin', __name__)


@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 6:
        form = ShopItemsForm()

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            salad = form.salad.data
            hotdrink = form.hotdrink.data
            colddrink = form.colddrink.data
            main = form.main.data
            desert = form.desert.data
            sneak = form.sneak.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)

            file_path = f'./media/{file_name}'

            file.save(file_path)

            new_shop_item = Product()
            new_shop_item.product_name = product_name
            new_shop_item.current_price = current_price
            new_shop_item.previous_price = previous_price
            new_shop_item.in_stock = in_stock
            new_shop_item.flash_sale = flash_sale
            new_shop_item.salad = salad
            new_shop_item.sneak = sneak
            new_shop_item.colddrink = colddrink
            new_shop_item.hotdrink = hotdrink
            new_shop_item.main = main
            new_shop_item.desert = desert

            new_shop_item.product_picture = file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added Successfully')
                print('Product Added')
                return render_template('add_shop_items.html', form=form)
            except Exception as e:
                print(e)
                flash('Product Not Added!!')

        return render_template('add_shop_items.html', form=form)

    return render_template('404.html')


@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 6:
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)
    return render_template('404.html')


@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 6:
        form = ShopItemsForm()

        item_to_update = Product.query.get(item_id)

        form.product_name.render_kw = {'placeholder': item_to_update.product_name}
        form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
        form.current_price.render_kw = {'placeholder': item_to_update.current_price}
        form.in_stock.render_kw = {'placeholder': item_to_update.in_stock}
        form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}
        form.sneak.render_kw = {'placeholder': item_to_update.sneak}
        form.main.render_kw = {'placeholder': item_to_update.main}
        form.colddrink.render_kw = {'placeholder': item_to_update.colddrink}
        form.hotdrink.render_kw = {'placeholder': item_to_update.hotdrink}
        form.desert.render_kw = {'placeholder': item_to_update.desert}
        form.salad.render_kw = {'placeholder': item_to_update.salad}

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            salad = form.salad.data
            hotdrink = form.hotdrink.data
            colddrink = form.colddrink.data
            main = form.main.data
            desert = form.desert.data
            sneak = form.sneak.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'

            file.save(file_path)

            try:
                Product.query.filter_by(id=item_id).update(dict(product_name=product_name,
                                                                current_price=current_price,
                                                                previous_price=previous_price,
                                                                in_stock=in_stock,
                                                                flash_sale=flash_sale,
                                                                salad=salad,
                                                                sneak=sneak,
                                                                desert=desert,
                                                                main=main,
                                                                colddrink=colddrink,
                                                                hotdrink=hotdrink,
                                                                product_picture=file_path))

                db.session.commit()
                flash(f'{product_name} updated Successfully')
                print('Product Upadted')
                return redirect('/shop-items')
            except Exception as e:
                print('Product not Upated', e)
                flash('Item Not Updated!!!')

        return render_template('update_item.html', form=form)
    return render_template('404.html')


@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 6:
        try:
            item_to_delete = Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('One Item deleted')
            return redirect('/shop-items')
        except Exception as e:
            print('Item not deleted', e)
            flash('Item not deleted!!')
        return redirect('/shop-items')

    return render_template('404.html')


@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.id == 6:
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')



@admin.route('/addnewtable')
@login_required
def addnewtable():
    file = open("tablecount.bin", "rb").read()
    tablecount = int(file)
    print(tablecount)
    new_customer = Customer()
    new_customer.email = 'masa'+str(tablecount)+'@gmail.com'
    new_customer.username = 'Masa '+str(tablecount)
    new_customer.password = 'Masa'+str(tablecount)
    new_customer.MasaNo = tablecount
    import qrcode
    img = qrcode.make('http://192.168.1.108/masa'+str(tablecount))
    type(img)  # qrcode.image.pil.PilImage
    imgname="QR/masa "+str(tablecount)+".png"
    img.save(imgname)
    tablecount= tablecount+1
    print(tablecount)
    tablecount=bytes(str(tablecount), encoding="utf-8")
    with open("tablecount.bin", "wb") as file:
        file.write(tablecount)
        print(tablecount)
    file.close()
    try:
        db.session.add(new_customer)
        db.session.commit()
        flash('Masa Başarıyla Oluşturuldu QR kodu QR Kodlar klasöründe bulabilirsiniz!')
        return redirect('/admin-page')
    except Exception as e:
        print(e)
        flash('Sistemde bir sorun oluştu Üretici ile irtibata geçiniz Hata Kodu: ERR101')


@admin.route('/remove-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def remove_order(order_id):  
    order = Order.query.get(order_id)
    db.session.delete(order)  
    db.session.commit()
    flash('sipariş başarıyla silindi')
    return redirect('/view-orders')

@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id == 6:
        form = OrderForm()

        order = Order.query.get(order_id)

        if form.validate_on_submit():
            status = form.order_status.data
            payment = form.order_Payment.data
            order.Payment = payment
            order.status = status

            try:
                db.session.commit()
                flash(f'{order_id} Numaralı Sipariş Başarıyla Güncellendi')
                return redirect('/view-orders')
            except Exception as e:
                print(e)
                flash(f'{order_id} Numaralı Sipariş Güncellenemedi ')
                return redirect('/view-orders')

        return render_template('order_update.html', form=form)

    return render_template('404.html')


@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id == 6:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')


@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 6:
        return render_template('admin.html')
    return render_template('404.html')









