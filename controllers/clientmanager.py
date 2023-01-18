from app import app
from flask import render_template, request, redirect, session
# import sqlite3
from utils import get_db_connection
from models.clientmanager_model import get_client, get_manager, create_work, create_client, get_product, get_works

@app.route('/clientmanager', methods=['get'])
def clientmanager():

    conn = get_db_connection()

    df_client = get_client(conn)

    df_manager = get_manager(conn)

    df_work = get_works(conn)
    df_work = df_work[df_work['contract_id'].isna()].reset_index(drop=True)
    print(df_work)
    df_work = df_work.groupby(df_work['manager_id']).size().reset_index().rename(columns={0: 'count'})
    print(df_work)
    df_manager = df_manager.merge(df_work[['manager_id', 'count']], on='manager_id', how='left').fillna(0).astype(
        {"count": "Int64"})

    target_client = 0
    target_manager = 0

    if 'client_name' not in session:
        session['client_name'] = ''
    else:
        session['client_name'] = ''
        if (request.values.get('client_name')):
            req = request.values.get('client_name')
            session['client_name'] = req
            df_client = df_client[df_client['name'].str.contains(session['client_name'])]

    if 'number' not in session:
        session['number'] = ''
    else:
        session['number'] = ''
        if (request.values.get('number')):
            req = request.values.get('number')
            session['number'] = req
            df_client = df_client[df_client['passport_number'] == session['number']]

    if 'series' not in session:
        session['series'] = ''
    else:
        session['series'] = ''
        if (request.values.get('series')):
            req = request.values.get('series')
            session['series'] = req
            df_client = df_client[df_client['passport_series'] == session['series']]

    if (request.values.get('action')):
        req = request.values.get('action')
        if (req == 'Добавить' and session['client_name'] != '' and session['series'] != '' and session['number'] != ''):
            id = create_client(conn, session['client_name'], session['series'], session['number'])
            print(id)
            session['client_id'] = id
            df_client = get_client(conn)
        if (req == 'index'):
            session.clear()
            return redirect(f"/", code=302)

    if 'client_id' not in session:
        session['client_id'] = ''
    else:
        if (request.values.get('client_id')):
            req = request.values.get('client_id')
            session['client_id'] = req
        if (session['client_id'] != ''):
            target_client = df_client.loc[df_client['client_id'] == int(session['client_id'])].reset_index(drop=True)
            df_client = df_client.loc[df_client['client_id'] != int(session['client_id'])].reset_index(drop=True)



    if 'manager_id' not in session:
        session['manager_id'] = ''
    else:
        if (request.values.get('manager_id')):
            req = request.values.get('manager_id')
            session['manager_id'] = req
        if (session['manager_id'] != ''):
            target_manager = df_manager.loc[df_manager['manager_id'] == int(session['manager_id'])].reset_index(drop=True)
            df_manager = df_manager.loc[df_manager['manager_id'] != int(session['manager_id'])].reset_index(drop=True)


    if 'maxcount' not in session:
        session['maxcount'] = ''
    else:
        session['maxcount'] = ''
        if (request.values.get('maxcount')):
            req = request.values.get('maxcount')
            session['maxcount'] = req
            df_manager = df_manager[df_manager['count'] <= int(session['maxcount'])]

    if 'manager_name' not in session:
        session['manager_name'] = ''
    else:
        session['manager_name'] = ''
        if (request.values.get('manager_name')):
            req = request.values.get('manager_name')
            session['manager_name'] = req
            df_manager = df_manager[df_manager['name'].str.contains(session['manager_name'])]


    if (request.values.get('product_id')):
        req = request.values.get('product_id')
        session['product_id'] = req




    product = get_product(conn, session['product_id'])

    if (session['manager_id'] and session['client_id'] and session['product_id']):

        create_work(conn, session['product_id'], session['manager_id'], session['client_id'])
        session.clear()
        return redirect(f"/", code=302)



    html = render_template(
        'clientmanager.html',
        product = product,
        client_name = session['client_name'],
        client_id = session['client_id'],
        manager_id = session['manager_id'],
        target_client = target_client,
        target_manager = target_manager,
        manager_name = session['manager_name'],
        series = session['series'],
        number = session['number'],
        maxcount = session['maxcount'],
        manager = df_manager.reset_index(drop=True),
        client = df_client.reset_index(drop=True),
        len=len
    )
    return html
