from flask import Blueprint, render_template, flash, send_from_directory, redirect
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm, PasswordChangeForm, NewTableForm, DomainChangeForm
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer, Settings
import qrcode
from . import db


admin = Blueprint('admin', __name__)


@admin.route('/media/<path:filename>')
def get_image(filename):
        return send_from_directory('../media', filename)
    #return render_template('404.html')

@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 6:
        form = ShopItemsForm()

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = 9999
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
                flash(f'{product_name} ürünü başarıyla eklendi')
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


@admin.route('/employee-management')
@login_required
def test1():
    settings_list = Settings.query.all()
    for setting in settings_list:
        db.session.delete(setting)
        db.session.commit()
    license = "test_license"
    settings = Settings(Domain="example.com", LocalHost=True,businessname="Restorant İsmi",licenseKey=license,Language=1,FirstBoot=False,AcceptedTerms=True,AutoUpdate=True,Telemetry=True)
    db.session.add(settings)
    db.session.commit()

    flash('maalesef görmek istediğiniz sayfa yapım aşamasında')
    return redirect('/admin-page')
@admin.route("/hello")
@login_required
def Hello():
    return render_template("startup.html")
@admin.route('/dashboard')
@login_required
def test():
    return render_template('dashboard.html')

@admin.route('/settings')
@login_required
def profile():
    if current_user.id == 6:
        customer = Customer.query.get(6)
        settings = Settings.query.all()  
        return render_template('settings.html', customer=customer, settings=settings)
    return render_template('404.html')

@admin.route('/change-domain', methods=['GET', 'POST'])
@login_required
def change_domain():
    if current_user.id == 6:
        form = DomainChangeForm()
        settings = Settings.query.first()
        if form.validate_on_submit():
            new_domain = form.domain.data
            print(new_domain)
            new_localhost = form.Localhost.data
            settings.Domain=new_domain
            settings.LocalHost=new_localhost
            db.session.commit()
            flash('Domain ayarlarınız başarıyla güncellendi')
            return redirect(f'/settings')
        return render_template('domain.html', form=form)
    return render_template('404.html')

@admin.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if current_user.id == 6:
        form = PasswordChangeForm()
        customer = Customer.query.get(6)
        if form.validate_on_submit():
            current_password = form.current_password.data
            new_password = form.new_password.data
            confirm_new_password = form.confirm_new_password.data

            if customer.verify_password(current_password):
                if new_password == confirm_new_password:
                    customer.password = confirm_new_password
                    db.session.commit()
                    flash('Şifreniz Başarıyla Değiştirildi')
                    return redirect(f'/settings')
                else:
                    flash('Yeni Şifreniz Doğrulanamadı')

            else:
                flash('Şuanki şifrenizi yanlış girdiniz')
        return render_template('password.html', form=form)
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
            in_stock = 9999
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
                flash(f'{product_name} Başarıyla Güncellendi')
                print('Ürün Güncellendi')
                return redirect('/shop-items')
            except Exception as e:
                print('Ürün Güncellenemedi Sorun devam ederse destek ile iletişime geçiniz', e)
                flash('Ürün Güncellendi!!!')

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
            flash('Bir öğe silindi')
            return redirect('/shop-items')
        except Exception as e:
            print('öğe silinemedi', e)
            flash('öğe silinemedi muhtemelen ürün birinin sepetinde ekli veya siparişlerde bulunuyor bu siparişleri temizleyip bir daha deneyin')
        return redirect('/shop-items')

    return render_template('404.html')


@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.id == 6:
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')



@admin.route('/addnewtable', methods=['GET', 'POST'])
@login_required
def addnewtable():
    if current_user.id == 6:
        form=NewTableForm()
        if form.validate_on_submit():

            table_name = form.table_name.data
            table_no = form.table_no.data
            existing_customer = Customer.query.filter_by(MasaNo=int(table_no)).first()

            if existing_customer:
                flash('Bu masa numarası zaten kullanılıyor, lütfen başka bir numara deneyin.')
                return redirect('/addnewtable')
            new_customer = Customer()
            new_customer.email = 'masa'+str(table_name)+'@gmail.com'
            new_customer.username = str(table_name)
            new_customer.password = 'Masa'+str(table_no)
            new_customer.MasaNo = int(table_no)
            new_customer.MasaAdi = str(table_name)
            settings = Settings.query.first()

            img = qrcode.make(f'{settings.Domain}/masa'+str(table_no))
            type(img)  # qrcode.image.pil.PilImage
            imgname="QR/masa "+str(table_no)+".png"
            img.save(imgname)
            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Masa Başarıyla Oluşturuldu QR kodu QR Kodlar klasöründe bulabilirsiniz 🫡')
                return redirect('/admin-page')
            except Exception as e:
                print(e)
                flash('Sistemde bir sorun oluştu Üretici ile irtibata geçiniz Hata Kodu: ERR101')
        return render_template('newtable.html', form=form)
    return render_template('404.html')

@admin.route('/finish-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def finish_order(order_id):  
    if current_user.id == 6:
        order = Order.query.get(order_id)
        order.Visibility = Order.query.get('Visibility')
        db.session.delete(order)  
        db.session.commit()
        flash('sipariş başarıyla Tamamlandı ve Tamamlanan kategorisine kaydedildi')
        return redirect('/view-orders')
    return render_template('404.html')

@admin.route('/remove-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def remove_order(order_id):  
    if current_user.id == 6:
        order = Order.query.get(order_id)
        db.session.delete(order)  
        db.session.commit()
        flash('sipariş başarıyla silindi')
        return redirect('/view-orders')
    return render_template('404.html')

@admin.route('/remove-user/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def remove_user(customer_id):  
    if current_user.id == 6:
        id = Customer.query.get(customer_id)
        if customer_id == 6:
            flash("admin hesabını silemezsiniz")
            return redirect('/customers')
        try:
            db.session.delete(id)  
            db.session.commit()
            flash('Kullanıcı Başarıyla Silindi')
            return redirect('/customers')
        except:
            flash('Kullanıcı Silinemedi Lütfen Geçerli Kullanıcının Sepetinin Boş Olduğuna ve Siparişlerinin Temizlendiğine Dikkat Edin.')
            return redirect('/customers')
    return render_template('404.html')

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
                flash(f'{order_id} Numaralı Sipariş Başarıyla Güncellendi 👍')
                return redirect('/view-orders')
            except Exception as e:
                print(e)
                flash(f'{order_id} Numaralı Sipariş Güncellenemedi 😥')
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









