from flask import Blueprint, render_template
from models.product import Product

bp = Blueprint('static_product', __name__)

@bp.route('/product/<int:product_id>')
def static_product_page(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('static_product.html', product=product)