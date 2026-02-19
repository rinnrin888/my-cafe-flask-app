from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, CafeItem

app = Flask(__name__)

# การตั้งค่า Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'cafe_secret_key_123' # สำหรับใช้กับ flash message

db.init_app(app)

# สร้างตารางใน Database อัตโนมัติ
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def home():
    # หน้าที่ 1: Home - ดึงเมนูแนะนำ 3 อย่างไปโชว์
    featured_items = CafeItem.query.limit(3).all()
    return render_template('index.html', items=featured_items)

@app.route('/menu')
def menu_all():
    # หน้าที่ 2: รวมเมนูทุกประเภท
    items = CafeItem.query.all()
    return render_template('menu.html', items=items, title="All Menu")

@app.route('/menu/beverages')
def menu_beverages():
    # หน้าที่ 2 (ย่อย): กรองเฉพาะเครื่องดื่ม
    items = CafeItem.query.filter(CafeItem.category.in_(['Coffee', 'Tea', 'Non-Coffee'])).all()
    return render_template('menu.html', items=items, title="Beverages")

@app.route('/menu/bakery')
def menu_bakery():
    # หน้าที่ 3: กรองเฉพาะขนม
    items = CafeItem.query.filter_by(category='Bakery').all()
    return render_template('menu.html', items=items, title="Bakery & Snacks")

@app.route('/menu/<int:item_id>')
def item_detail(item_id):
    # หน้าที่ 4: รายละเอียดสินค้า (Dynamic Route)
    item = CafeItem.query.get_or_404(item_id)
    return render_template('detail.html', item=item)

@app.route('/admin/add-item', methods=['GET', 'POST'])
def add_item():
    # หน้าที่ 6: Admin เพิ่มเมนูใหม่
    if request.method == 'POST':
        new_item = CafeItem(
            name=request.form.get('name'),
            category=request.form.get('category'),
            price=request.form.get('price'),
            description=request.form.get('description'),
            image_url=request.form.get('image_url')
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('menu_all'))
    
    return render_template('add_item.html')

@app.route('/contact')
def contact():
    # หน้าที่ 9: ข้อมูลติดต่อ
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)