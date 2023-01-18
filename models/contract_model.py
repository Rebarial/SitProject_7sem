import pandas

def get_contract_id(conn, work_id):
 return pandas.read_sql(f'''
 select contract_id from work_with_client where work_id = {work_id}
 ''', conn)

def get_client_id(conn, work_id):
 return pandas.read_sql(f'''
 select client_id from work_with_client where work_id = {work_id}
 ''', conn)

def get_product_id(conn, work_id):
 return pandas.read_sql(f'''
 select product_id from work_with_client where work_id = {work_id}
 ''', conn)

def get_contract(conn, contract_id):
 return pandas.read_sql(f'''
 Select * from contract where contract_id = {contract_id}
 ''', conn)


def get_product(conn, product_id):
 return pandas.read_sql(f'''
 select color, year_of_release, mark_name, model, country, body_type_name, engine_type_name, cost from product 
 inner join mark on mark.mark_id = product.product_id,
 engine_type on engine_type.engine_type_id = product.engine_type_id,
 body_type on body_type.body_type_id = product.body_type_id
 where product_id = {product_id}
 ''', conn)

def get_client(conn, client_id):
 return pandas.read_sql(f'''
 Select * from client where client_id = {client_id}
 ''', conn)

def get_marks(conn):
 return pandas.read_sql('''
 select * from mark
 ''', conn)

def del_contract(conn, contract_id, work_id):
 cursor = conn.cursor()
 cursor.execute('''
 Delete from contract where contract_id = :p_contract
 ''', {"p_contract": contract_id})
 cursor.execute('''
  Update work_with_client set contract_id = null where work_id = :p_work
  ''', {"p_work": work_id})
 conn.commit()

def update_contract(conn, contract,payment):
 cursor = conn.cursor()
 cursor.execute('''
 Update contract set payment_type = :p_payment where contract_id = :p_contract
 ''', {"p_payment": payment, "p_contract": contract})
 conn.commit()

def create_contract(conn, cli, product, work):
 cursor = conn.cursor()
 cursor.execute('''
Insert into 
contract
(place_of_create, date_of_create, client_id, product_id, payment_type)
Values
("Россия, Санктпитербург, Вольная, 10, Автомагазин «АвтоОпт»", Date('now'), :p_client, :p_prod, "Наличные")
''', {"p_prod": product, "p_client": cli})
 cursor.execute('''
 SELECT last_insert_rowid()
 ''')
 contract_id = cursor.fetchall()[0][0];
 cursor.execute('''
 UPDATE work_with_client SET contract_id = :p_contract WHERE work_id = :p_work;
 ''', {"p_contract": contract_id, "p_work": work})
 conn.commit()

