from app import app
from flask import render_template, request, redirect
# import sqlite3
from utils import get_db_connection
from models.product_model import get_products, get_marks, get_body_type, get_engine_type

@app.route('/product', methods=['get'])
def product():

    conn = get_db_connection()

    title_list = ['id', 'цвет', 'марка', 'модель', 'год выпуска', 'страна', 'тип кузова', 'тип двигателя', 'количество дверей', 'количество сидений', 'объем двигателя', 'цена', 'действие']

    df_products = get_products(conn)
    df_mark = get_marks(conn)
    df_body = get_body_type(conn)
    df_engine = get_engine_type(conn)

    if (request.values.get('color')):
        req = request.values.get('color')[0]
        if req != '':
            df_products = df_products[df_products['color'].str.contains(req)]

    if (request.values.get('mark')):
        req = request.values.get('mark')[0]
        if req != '':
            df_products = df_products[df_products['mark_name'].str.contains(req)]

    if (request.values.get('model')):
        req = request.values.get('model')[0]
        if req != '':
            df_products = df_products[df_products['model'].str.contains(req)]

    if (request.values.get('year_of_release')):
        req = request.values.get('year_of_release')
        if req != '':
            df_products = df_products[df_products['year_of_release'] == int(req)]

    if (request.values.get('country')):
        req = request.values.get('country')[0]
        if req != '':
            df_products = df_products[df_products['country'].str.contains(req)]

    if (request.values.get('body_type')):
        req = request.values.get('body_type')[0]
        if req != '':
            df_products = df_products[df_products['body_type_name'].str.contains(req)]

    if (request.values.get('engine_type')):
        req = request.values.get('engine_type')[0]
        if req != '':
            df_products = df_products[df_products['engine_type_name'].str.contains(req)]

    if (request.values.get('number_of_doors')):
        req = request.values.get('number_of_doors')
        if req != '':
            print(type(req))
            df_products = df_products[df_products['number_of_doors'] == int(req)]

    if (request.values.get('number_of_seats')):
        req = request.values.get('number_of_seats')
        if req != '':
            df_products = df_products[df_products['number_of_seats'] == int(req)]

    if (request.values.get('engine_capacity')):
        req = request.values.get('engine_capacity')
        if req != '':
            df_products = df_products[df_products['engine_capacity'] == float(req)]

    if (request.values.get('cost')):
        req = request.values.get('cost')
        if req != '':
            print(req)
            print(type(int(req)))
            df_products = df_products[df_products['cost'] == int(req)]

    html = render_template(
        'product.html',
        title_list = title_list,
        products = df_products.reset_index(drop=True),
        mark = df_mark,
        body = df_body,
        engine = df_engine,
        len=len
    )
    return html