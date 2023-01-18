from app import app
from flask import render_template, request, redirect
# import sqlite3
from utils import get_db_connection
from models.contract_model import get_contract_id, get_client, get_client_id, get_product_id, get_product, create_contract, get_contract, update_contract, del_contract


@app.route('/contract', methods=['get'])
def contract():
    conn = get_db_connection()


    if (request.values.getlist('work_id')):
        work_id = request.values.getlist('work_id')[0]
        contract_id = get_contract_id(conn, work_id)['contract_id'].to_list()[0]

        if request.values.getlist('action'):
            action = request.values.getlist('action')[0]
            if (action == 'Изменить'):
                payment_type = request.values.getlist('payment_type')[0]
                update_contract(conn, contract_id, payment_type)
            if (action == 'Удалить'):
                del_contract(conn, contract_id, work_id)
                return redirect(f"/", code=302)


        client_id = get_client_id(conn, work_id)['client_id'].to_list()[0]
        product_id = get_product_id(conn, work_id)['product_id'].to_list()[0]
        df_product = get_product(conn, product_id)
        df_client = get_client(conn, client_id)
        print(client_id, ' ', product_id, ' ', work_id)
        if (contract_id == None):
            create_contract(conn, client_id, product_id, work_id)
            contract_id = get_contract_id(conn, work_id)['contract_id'].to_list()[0]
            df_contract = get_contract(conn, contract_id)
        else:
            df_contract = get_contract(conn, contract_id)
    else:
        return redirect("/", code=302)




    html = render_template(
        'contract.html',
        client_name = df_client['name'].to_list()[0],
        work_id = work_id,
        client_series = df_client['passport_series'].to_list()[0],
        client_number = df_client['passport_number'].to_list()[0],
        car_mark_model = df_product['mark_name'].to_list()[0] + ', ' + df_product['model'].to_list()[0],
        car_color = df_product['color'].to_list()[0],
        car_body = df_product['body_type_name'].to_list()[0],
        car_engine = df_product['engine_type_name'].to_list()[0],
        year_of_release = df_product['year_of_release'].to_list()[0],
        car_country = df_product['country'].to_list()[0],
        data_of_create = df_contract['date_of_create'].to_list()[0],
        place = df_contract['place_of_create'].to_list()[0],
        contract_id = contract_id,
        cost = df_product['cost'].to_list()[0],
        payment_type =df_contract['payment_type'].to_list()[0],
        len=len
    )
    return html