import pandas
def get_reader(conn):
 return pandas.read_sql(
 '''
 SELECT * FROM reader
 ''', conn)

def get_client_working(conn):
 return pandas.read_sql('''
 Select work_id, wwc.product_id, model as model_name, mark_name, wwc.manager_id, manager.name as manager_name, wwc.client_id, client.name as client_name, wwc.contract_id, date_of_create as contract, cost
 from work_with_client as wwc
 inner join client on client.client_id = wwc.client_id,
 manager on manager.manager_id = wwc.manager_id,
 (select product_id, mark_name, model, cost 
 from product inner join mark on mark.mark_id = product.product_id) as product
 on product.product_id = wwc.product_id LEFT JOIN contract on contract.contract_id = wwc.contract_id
 ''', conn)

def get_stages(conn):
 return pandas.read_sql('''
 select stage_name, work_id, date from pass_stage inner join stage on stage.stage_id = pass_stage.stage_id
 ''', conn)


def get_marks(conn):
 return pandas.read_sql('''
 select * from mark
 ''', conn)

def get_contract_id(conn, work_id):
 return pandas.read_sql(f'''
 select contract_id from work_with_client where work_id = {work_id}
 ''', conn)

def del_work(conn, work_id):
 cursor = conn.cursor()
 cursor.execute(f'''
  SELECT contract_id from work_with_client where work_id = {work_id}
  ''')
 contract_id = cursor.fetchall()[0][0];
 cursor.execute('''
 Delete from work_with_client where work_id = :p_work
 ''', {"p_work": work_id})
 cursor.execute('''
  Delete from pass_stage where work_id = :p_work
  ''', {"p_work": work_id})
 if contract_id:
  cursor.execute('''
   Delete from contract where contract_id = :p_contract
   ''', {"p_contract": contract_id})
 conn.commit()

def get_stage(conn):
  return pandas.read_sql(f'''
  select * from stage
  ''', conn)