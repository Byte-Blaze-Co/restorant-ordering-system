from flask import Blueprint, render_template, flash, redirect, request, jsonify
from .models import Product, Cart, Order, Customer
from flask_login import login_required, current_user
from . import db
from intasend import APIService



views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'YOUR_PUBLISHABLE_KEY'

API_TOKEN = 'YOUR_API_TOKEN'


@views.route('/')
def home():

    items = Product.query.filter_by(flash_sale=True)

    return render_template('home.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])


@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exists = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exists:
        try:
            item_exists.quantity = item_exists.quantity + 1
            db.session.commit()
            flash(f'{ item_exists.product.product_name } Ürününün Adisyonu Güncellendi 😄')
            return redirect(request.referrer)
        except Exception as e:
            print('Adisyon Güncellenemedi', e)
            flash(f'{ item_exists.product.product_name } Ürününün Adisyonu Güncellenemedi 😥')
            return redirect(request.referrer)

    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.product_name} Sepete Eklendi 🥳')
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.product.product_name} Sepete Eklenirken bir sorun oluştu 😥')

    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.product.current_price * item.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount + 15)


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity + 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount + 15
        }

        return jsonify(data)


@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        if cart_item.quantity >=2:
                cart_item.quantity = cart_item.quantity - 1
                db.session.commit()

                cart = Cart.query.filter_by(customer_link=current_user.id).all()

                amount = 0

                for item in cart:
                   amount += item.product.current_price * item.quantity

                   data = {
                       'quantity': cart_item.quantity,
                       'amount': amount,
                       'total': amount + 15
                          }
                   
                return jsonify(data)
        else:
            flash('daha fazla eksiltemezsiniz 🫤')
            return jsonify(data)


@views.route('/payment')
@login_required
def paymentrequest():
    degisiklik_sayisi=0
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    
        
    for order in orders:
        print('a')
        order_id = order.id  
        # ID numarası 1 olan satırı sorgulama
        order_stat = Order.query.get(order_id)
        print(order_id)
        print(order_stat.Payment)          
        
        if order_stat.Payment != 'Ödeme Yapıldı' and order_stat.Payment != 'Ödeme İsteği Alındı':

            order = order
            order.Payment = 'Ödeme İsteği Alındı'
            db.session.commit()
            degisiklik_sayisi=degisiklik_sayisi+1
    if degisiklik_sayisi >=1:

        from plyer import notification
        bildirim_numarası=current_user.id
        print(bildirim_numarası)
        bildirim_numarası=bildirim_numarası-6
        print(bildirim_numarası)
        bildirim_numarası=str(bildirim_numarası)
        notification.notify(
                        title='Yeni Ödeme İsteği',
                        message='Masa '+bildirim_numarası+' ödeme isteği gönderdi',
                        app_name='Restorant Yönetimi',
                        timeout=10  # Bildirimin ekranda ne kadar süre kalacağını belirler
                        )
        flash('Ödeme isteğiniz gönderildi/güncellendi garson birazdan yanınızda olacak 😁')
        return redirect('/')
    else:
        flash("zaten ödeme isteği yapmışsınız ve değişiklik yok")
        return redirect('/')
    
@views.route('removecart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()

        amount = 0

        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity': cart_item.quantity,
            'amount': amount,
            'total': amount
        }

        return [jsonify(data)]


@views.route('/place-order')
@login_required
def place_order():
    from win10toast import ToastNotifier
    customer_cart = Cart.query.filter_by(customer_link=current_user.id)
    if customer_cart:
        
            total = 0
            for item in customer_cart:
                total += item.product.current_price * item.quantity
                


            for item in customer_cart:
                new_order = Order()
                new_order.quantity = item.quantity
                new_order.price = item.product.current_price
                new_order.status = 'Beklemede'
                new_order.Payment = 'Ödeme Yapılmadı'

                new_order.product_link = item.product_link
                new_order.customer_link = item.customer_link

                db.session.add(new_order)
                
                product = Product.query.get(item.product_link)

                product.in_stock -= item.quantity

                db.session.delete(item)
                bildirim_numarası=current_user.id
                print(bildirim_numarası)
                bildirim_numarası=bildirim_numarası-6
                print(bildirim_numarası)
                bildirim_numarası=str(bildirim_numarası)
                db.session.commit()
            from plyer import notification
            notification.notify(
                            title='Yeni Sipariş Var',
                            message='Masa '+bildirim_numarası+' sipariş verdi',
                            app_name='Restorant Yönetim',
                            timeout=5  # Bildirimin ekranda ne kadar süre kalacağını belirler
                            )

            try:

                flash('Sipariş Başarıyla Oluşturuldu 🎉')
                return redirect('/orders')
            except:
                print("hata kodu :orderERR101")
                flash('Sipariş Oluşturulurken Bir Hata Meydana Geldi 😥')
                return redirect('/')
    else:
        flash('Sepetiniz Boş 😑')
        return redirect('/')


@views.route('/orders', methods=['GET', 'POST'])
@login_required
def order():
    orders = Order.query.filter_by(customer_link=current_user.id).all()
    return render_template('orders.html', orders=orders)


@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
        return render_template('search.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

    return render_template('search.html')
@views.route('/deserts')
def deserts():
    items = Product.query.filter_by(desert=True)
    return render_template('deserts.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

@views.route("/mainmenu")
def mainmenu():
    items = Product.query.filter_by(main=True)
    return render_template('mainmenu.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

@views.route("/sneaks")
def sneaks():
    items = Product.query.filter_by(sneak=True)
    print(items)
    return render_template('sneaks.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

@views.route("/hotdrinks")
def hotdrinks():
    items = Product.query.filter_by(hotdrink=True)
    return render_template('hotdrinks.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

@views.route("/colddrinks")
def colddrinks():
    items = Product.query.filter_by(colddrink=True)
    return render_template('colddrinks.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

@views.route("/salads")
def salads():
    items = Product.query.filter_by(salad=True)
    return render_template('salads.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])














