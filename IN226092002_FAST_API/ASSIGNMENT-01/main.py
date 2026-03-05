from fastapi import FastAPI,Query
 
app = FastAPI()
 
# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },
    {'id': 5, 'name': 'Laptop Stand', 'price': 999,'category': 'Electronics', 'in_stock': True },
    {'id':6, 'name': 'Mechanical Keyboard', 'price': 1299, 'category': 'Electronics', 'in_stock': False},
    {'id':7, 'name':'Webcam', 'price': 699, 'category': 'Electronics', 'in_stock': True },
]
 
# ── Endpoint — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

# ── Endpoint — Return the store summary ──────────────────────────
@app.get('/store/summary')
def get_store_summary():
    total_products = len(products)
    in_stock_products = len([p for p in products if p['in_stock']])
    categories=set(p['category'] for p in products if p['category'])
    return {
        'total_products': total_products,
        'in_stock_products': in_stock_products,
        'out_of_stock_products': total_products - in_stock_products,
        'categories': list(categories)
    }

# ── Endpoint — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# ── Endpoint — Return all products which are on deal ──────────────────────────
@app.get('/products/deals')
def get_deals():
    best_deal=min(products, key=lambda p: p['price'])
    premium_pick=max(products, key=lambda p: p['price'])
    return {'best_deal': best_deal, 'premium_pick': premium_pick}

# ── Endpoint — Return all products which are in stock ──────────────────────────
@app.get('/products/in-stock')
def get_in_stock_products():
    in_stock_products = [p for p in products if p['in_stock']]
    return {'in_stock_products': in_stock_products, 'total': len(in_stock_products)}

# ── Endpoint — Return all products which matches the keyword ──────────────────────────
@app.get('/products/search/{keyword}')
def search_products(keyword: str):
    results = [p for p in products if keyword.lower() in p['name'].lower()]
    if len(results) == 0:
        return { "No products match"}
    return {'products': results, 'total': len(results)}

# ── Endpoint — Return all products by category ──────────────────────────
@app.get('/products/{category_name}')
def get_products_by_category(category_name: str):
    prod=[]
    for i in products:
        if i['category']==category_name:
            prod.append(i)
    if len(prod)==0:
        return {"error": "No products found in this category"}
    return {"products": prod, "total": len(prod)}

# ── Endpoint — Return all products after filtering ──────────────────────────
@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only')
):
    result = products          # start with all products
 
    if category:
        result = [p for p in result if p['category'] == category]
 
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
 
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
 
    return {'filtered_products': result, 'count': len(result)}
 
# ── Endpoint — Return one product by its ID ──────────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}