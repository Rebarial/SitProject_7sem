from app import app
from flask import render_template, request, redirect
# import sqlite3
from utils import get_db_connection
from models.index_model import get_client_working, get_marks, get_contract_id, del_work, get_stages, get_stage

@app.route('/', methods=['get'])
def index():

    conn = get_db_connection()

    if (request.values.get('delete')):
        req = request.values.get('delete')
        del_work(conn, req)

    df_work = get_client_working(conn)

    df_pass_stage = get_stages(conn)

    df_stage = get_stage(conn)



    if (request.values.get('client_name') and request.values.get('client_name') != '' and not request.values.get('action') == 'Очистить'):
        client_name = request.values.get('client_name')
        df_work = df_work[df_work['client_name'].str.contains(client_name)]
    else:
        client_name = ''
    if (request.values.get('manager_name') and request.values.get('manager_name') != '' and not request.values.get('action') == 'Очистить'):
        manager_name = request.values.get('manager_name')
        df_work = df_work[df_work['manager_name'].str.contains(manager_name)]
    else:
        manager_name = ''
    if (request.values.get('model_name') and request.values.get('model_name') != '' and not request.values.get('action') == 'Очистить'):
        model_name = request.values.get('model_name')
        df_work = df_work[df_work['model_name'].str.contains(model_name)]
    else:
        model_name = ''
    if (request.values.get('contract_begin') and not request.values.get('action') == 'Очистить'):
        contract_begin = request.values.get('contract_begin')
        df_work = df_work[df_work['contract'] >= contract_begin]
    else:
        contract_begin = ''
    if (request.values.get('contract_end') and not request.values.get('action') == 'Очистить'):
        contract_end = request.values.get('contract_end')
        df_work = df_work[df_work['contract'] <= contract_end]
    else:
        contract_end = ''

    df_marks = get_marks(conn)

    if (request.values.getlist('stage[]') and not request.values.get('clear') == 'Очистить'):
        stage_select = request.values.getlist('stage[]')
    else:
        stage_select = df_stage['stage_name'].to_list()
        stage_select.append('None')

    #df_work = df_work.groupby(df_work['manager_id']).size().reset_index().rename(columns={0: 'count'})
    df_pass_stage = df_pass_stage[df_pass_stage['date'].notna()]
    df_pass_stage = df_pass_stage.groupby('work_id')['stage_name'].apply(lambda x: ", " .join(x)).reset_index()
    df_work = df_work.merge(df_pass_stage[['work_id', 'stage_name']], on='work_id', how='left').fillna('None')
    if (not('None' in stage_select)):
        df_work = df_work[df_work['stage_name'].str.contains('None') == False]
    if (not('Тест-драйв' in stage_select)):
        df_work = df_work[df_work['stage_name'].str.contains('Тест-драйв') == False]
    if (not('Технический осмотр' in stage_select)):
        df_work = df_work[df_work['stage_name'].str.contains('Технический осмотр') == False]

    action_i = ''
    work_id = ''
    if (request.values.getlist('contract')):
        contract_id = get_contract_id(conn, request.values.getlist('work_id')[0])['contract_id'].to_list()[0]
        if (contract_id == None):
            action_i = 'contract'
            work_id = request.values.getlist('work_id')[0]
        else:
            return redirect(f"/contract?work_id={request.values.getlist('work_id')[0]}", code=302)

    cnt_contracts = 0
    sum_contracts = 0
    cnt_no_contracts = 0
    if (request.values.get('action')):
        action = request.values.get('action')
        if (action == 'Отчет'):
            action_i = 'Отчет'
            cnt_contracts = len(df_work[df_work['contract'].str.contains('None') == False])
            sum_contracts = df_work[df_work['contract'].str.contains('None') == False]['cost'].sum()
            cnt_no_contracts = len(df_work[df_work['contract'].str.contains('None') == True])


    df_work['product_name'] = df_work['mark_name'] + ' ' + df_work['model_name']
    # выводим форму
    html = render_template(
        'index.html',
        cnt_contracts = cnt_contracts,
        sum_contracts = sum_contracts,
        cnt_no_contracts = cnt_no_contracts,
        action_i = action_i,
        contract_begin = contract_begin,
        contract_end = contract_end,
        work_id = work_id,
        marks = df_marks['mark_name'].to_list(),
        client_name = client_name,
        manager_name = manager_name,
        model_name = model_name,
        stage_select = stage_select,
        stage = df_stage,
        #pass_stage = df_pass_stage[df_pass_stage['date'].notna()],
        work = df_work[['work_id', 'client_name', 'manager_name', 'product_name', 'contract', 'stage_name']].reset_index(drop=True),
        len=len
    )
    return html


