import pandas


def get_client(conn):
 return pandas.read_sql(f'''
 select * from client
 ''', conn)

def get_manager(conn):
 return pandas.read_sql(f'''
 select * from manager
 ''', conn)

def get_works(conn):
 return pandas.read_sql(f'''
  select manager_id, contract_id from work_with_client
  ''', conn)


def create_client(conn, name, series, nubmer):
 cursor = conn.cursor()
 cursor.execute('''
 Insert into 
 client
 (name, passport_series, passport_number)
 Values
 (:p_name, :p_series, :p_number)
 ''', {"p_name": name, "p_series": series, "p_number": nubmer})
 conn.commit()
 cursor.execute('''
 SELECT last_insert_rowid()
 ''')
 return cursor.fetchall()[0][0];

def create_work(conn, product, manager, client):
 cursor = conn.cursor()
 cursor.execute('''
 Insert into 
 work_with_client
 (product_id, manager_id, client_id)
 Values
 (:p_prod, :p_manager, :p_client)
 ''', {"p_prod": product, "p_client": client, "p_manager": manager})
 cursor.execute('''
 SELECT last_insert_rowid()
 ''')
 work_id = cursor.fetchall()[0][0];
 cursor.execute('''
 Insert into
 pass_stage
 (work_id, stage_id)
 select work_id, stage_id from work_with_client join stage where
 work_id = :p_work
 ''', {"p_work": work_id})
 conn.commit()


def get_product(conn, product_id):
  return pandas.read_sql(f'''
  select mark_name, model, color, body_type_name, engine_type_name, engine_capacity, cost from product 
  inner join mark on mark.mark_id = product.product_id,
  engine_type on engine_type.engine_type_id = product.engine_type_id,
  body_type on body_type.body_type_id = product.body_type_id
  where product_id = {product_id}
  ''', conn)
