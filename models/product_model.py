import pandas

def get_products(conn):
 return pandas.read_sql(f'''
 select product_id, color, mark_name, model, year_of_release, country, body_type_name, engine_type_name, number_of_doors, number_of_seats, engine_capacity, cost from product 
 inner join mark on mark.mark_id = product.product_id,
 engine_type on engine_type.engine_type_id = product.engine_type_id,
 body_type on body_type.body_type_id = product.body_type_id
 ''', conn)

def get_marks(conn):
 return pandas.read_sql(f'''
 select * from mark
 ''', conn)

def get_body_type(conn):
 return pandas.read_sql(f'''
 select * from body_type
 ''', conn)

def get_engine_type(conn):
 return pandas.read_sql(f'''
 select * from engine_type
 ''', conn)