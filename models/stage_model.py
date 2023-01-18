import pandas

def get_client_working(conn, work_id):
 return pandas.read_sql(f'''
 Select work_id, wwc.product_id, model as model_name, mark_name, wwc.manager_id, manager.name as manager_name, wwc.client_id, client.name as client_name, wwc.contract_id, date_of_create as contract, cost
 from work_with_client as wwc
 inner join client on client.client_id = wwc.client_id,
 manager on manager.manager_id = wwc.manager_id,
 (select product_id, mark_name, model, cost 
 from product inner join mark on mark.mark_id = product.product_id) as product
 on product.product_id = wwc.product_id LEFT JOIN contract on contract.contract_id = wwc.contract_id
 where work_id = {work_id}
 ''', conn)

def get_work_stage(conn, work_id):
 return pandas.read_sql(f'''
 select stage_name, date, work_id, pass_stage.stage_id from pass_stage inner join stage on pass_stage.stage_id = stage.stage_id where work_id = {work_id}
 ''', conn)

def set_date(conn, work_id, stage_id):
 cursor = conn.cursor()
 cursor.execute('''
 update pass_stage set date = date('now','localtime') where work_id = :p_work and stage_id = :p_stage
 ''', {"p_work": work_id, "p_stage": stage_id})
 conn.commit()

def set_null_date(conn, work_id, stage_id):
 cursor = conn.cursor()
 cursor.execute('''
 update pass_stage set date = NULL where work_id = :p_work and stage_id = :p_stage
 ''', {"p_work": work_id, "p_stage": stage_id})
 conn.commit()