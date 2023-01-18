from app import app
from flask import render_template, request, redirect, session
# import sqlite3
from utils import get_db_connection
from models.stage_model import get_work_stage, set_date, set_null_date, get_client_working

@app.route('/stage', methods=['get'])
def stage():

    conn = get_db_connection()
    if (request.values.get('action')):
        action = request.values.get('action')
        if (action == 'date'):
            set_date(conn, request.values.get('work_id'), request.values.get('stage_id'))
        if (action == 'delete'):
            set_null_date(conn, request.values.get('work_id'), request.values.get('stage_id'))
    if (request.values.get('work_id')):
        work_id = request.values.get('work_id')
        session['work_id_stage'] = work_id
    else:
        session['work_id_stage'] = 1;
    df_work_stage = get_work_stage(conn, session['work_id_stage'])
    df_work = get_client_working(conn, work_id)

    html = render_template(
        'stage.html',
        stage = df_work_stage,
        work = df_work,
        work_id = work_id,
        len=len
    )
    return html