import sqlite3

con = sqlite3.connect("auto_shop.sqlite")
cursor = con.cursor()
#Создание таблиц
"""
con.executescript('''
Create table if not exists mark(
    mark_id integer primary key autoincrement,
    mark_name varchar(30)
);
Create table if not exists body_type(
    body_type_id integer primary key autoincrement,
    body_type_name varchar(30)
);
Create table if not exists engine_type(
    engine_type_id integer primary key autoincrement,
    engine_type_name varchar(30)
);
Create table if not exists client(
    client_id integer primary key autoincrement,
    name varchar(50),
    passport_series varchar(6),
    passport_number varchar(4)
);
Create table if not exists manager(
    manager_id integer primary key autoincrement,
    name varchar(50),
    date_of_employment date
);
Create table if not exists stage(
    stage_id integer primary key autoincrement,
    stage_name varchar(30)
);
Create table if not exists product(
    product_id integer primary key autoincrement,
    color varchar(30),
    year_of_release integer,
    mark_id integer,
    model varchar(30),
    country varchar(40),
    body_type_id integer,
    engine_type_id integer,
    number_of_doors integer,
    number_of_seats integer,
    engine_capacity float,
    foreign key (mark_id) references mark (mark_id) ON DELETE SET NULL,
    foreign key (body_type_id) references body_type (body_type_id) ON DELETE SET NULL,
    foreign key (engine_type_id) references engine_type (engine_type_id) ON DELETE SET NULL
);
Create table if not exists contract(
    contract_id integer primary key autoincrement,
    place_of_create varchar(50) not null,
    date_of_crate date not null,
    client_id integer not null,
    product_id integer not null,
    payment_type varchar(20) not null,
    cost integer not null,
    foreign key (client_id) references client (client_id) ON DELETE CASCADE,
    foreign key (client_id) references client (client_id) ON DELETE CASCADE
);
Create table if not exists work_with_client(
    work_id integer primary key autoincrement,
    product_id integer,
    manager_id integer,
    client_id integer,
    contract_id integer,
    foreign key (product_id) references product (product_id) ON DELETE CASCADE,
    foreign key (manager_id) references manager (manager_id) ON DELETE SET NULL,
    foreign key (client_id) references client (client_id) ON DELETE CASCADE,
    foreign key (contract_id) references contract_id (contract_id) ON DELETE SET NULL
);
Create table if not exists pass_stage(
    stage_id integer NOT NULL,
    work_id integer NOT NULL,
    date date,
    foreign key (stage_id) references stage (stage_id) ON DELETE CASCADE,
    foreign key (work_id) references work (work_id) ON DELETE CASCADE,
    primary key (stage_id, work_id)
);
''')
con.commit()
con.executescript('''
INSERT INTO mark (mark_name) VALUES 
('BMW'),
('Toyota'),
('Nissan'),
('Kia'),
('Hyundai'),
('Лада'),
('Bentley'),
('Москвич'),
('Mercedes-Benz'),
('Volvo');

INSERT INTO body_type (body_type_name) VALUES 
('Купэ'),
('Универсал'),
('Кабриолет'),
('Седан'),
('Лимузин'),
('Внедорожник'),
('Хетчбэк'),
('Пикап');

INSERT INTO engine_type (engine_type_name) VALUES 
('Бензин'),
('Дизель'),
('Электро'),
('Гибрид'),
('ГБО');

INSERT INTO client (name, passport_series, passport_number) VALUES 
('Кожемятько Абдул Михайлович', '1234', '567892'),
('Имонов Сергей Генадьевич', '1234', '456123'),
('Нимчук Светлана Анатольевна', '4561', '123456'),
('Рябчев Кирилл Александрович', '6112', '654321'),
('Гарьев Святослав Анатольевич', '5561', '908721'),
('Цацель Петр Станиславович', '5678', '345676'),
('Кладьюк Ирина Юрьевна', '2341', '947321'),
('Костин Константин Николаевич', '8878', '878787'),
('Патронов Павел Георгович', '4567', '456789'),
('Рамзин Александр Толикович', '9090', '908990');

INSERT INTO manager (name, date_of_employment) VALUES 
('Бородоченко Ирина Масикова', '2011-04-03'),
('Михавчук Варин Дмитрич', '2013-04-03'),
('Павличенко Константин Георгевич', '2010-04-03'),
('Обрамова Лина Петрова', '2012-04-03'),
('Бородоченко Максим Никитич', '2009-04-03');

INSERT INTO stage (stage_name) VALUES 
('Тест-драйв'),
('Технический осмотр');

INSERT INTO product (color,
    year_of_release,
    mark_id,
    model,
    country,
    body_type_id,
    engine_type_id,
    number_of_doors,
    number_of_seats,
    engine_capacity) VALUES
    ('бежевый', 1996, 2, 'prius', 'Япония', 4, 1, 4, 7, 1.5),
    ('черный', 2008, 1, '1-series', 'Германия', 4, 1, 4, 7, 5.5),
    ('красный', 2010, 6, 'приора', 'Россия', 4, 1, 4, 7, 2.5);
    INSERT INTO work_with_client(
    product_id,
    manager_id,
    client_id)
    VALUES
    (1,1,1),
    (1,1,2),
    (1,1,3),
    (1,2,4);
    INSERT INTO pass_stage(stage_id, work_id, date) VALUES
    (1,1, '2015-04-03'),
    (2,1, '2015-04-10'),
    (1,2, '2018-04-03');
    
''')
con.commit()
"""
#link_table Вывести все товары марки A и отсортировать по убыванию года выпуска
cursor.execute('''
select product_id, year_of_release,  mark_name, model
    from product inner join mark ON mark.mark_id = product.product_id where mark_name = :p_mark Order by year_of_release desc;
''', {"p_mark": "Toyota"})
print(cursor.fetchall())
#link_table Вывести имена всех клиентов с которыми еще не был заключен договор, отсортировать по алфавиту
cursor.execute('''
select name, contract_id
    from client inner join work_with_client as wwc ON wwc.client_id = client.client_id where contract_id is NULL Order by name;
''')
print(cursor.fetchall())
#Добавление работы с клиентом и изменение в той же таблице
"""
con.executescript('''
INSERT INTO work_with_client(
    product_id,
    manager_id,
    client_id)
    VALUES
    (2,1,1),
    (3,1,3),
    (3,2,4);
''')
con.commit()
"""
"""
con.executescript('''
update work_with_client
set product_id = 3
where work_id = 1
''')
con.commit()
"""
con.commit()
#group inv Вывести товар с которым больше всего взаимодействовали клиенты
cursor.execute('''
select product.product_id, mark_name, model, color, year_of_release, cn as count 
    from product inner join (select product_id, count() as cn 
    from work_with_client group by product_id) as cw ON (cw.product_id = product.product_id), mark ON (mark.mark_id = product.mark_id)
    where count = (select max(cn) from (select product_id, count() as cn 
    from work_with_client group by product_id))
''')
print(cursor.fetchall())
#inv Вывести список этапов, которые прошел клиент A вместе с датой
cursor.execute('''
select name, stage_name, date from (select name, stage_id, date
    from client inner join 
    (select stage_id, date from work_with_client 
    inner join pass_stage as ps ON (ps.work_id = work_with_client.work_id)) 
    where client_id = :p_id) as bd inner join stage ON (stage.stage_id = bd.stage_id)
''', {"p_id": 1})
print(cursor.fetchall())
"""
con.executescript('''
INSERT INTO
contract(
    place_of_create,
    date_of_crate,
    client_id,
    product_id,
    payment_type,
    cost)
    Values
    ("Россия, Санктпитербург, Вольная, 10", '2015-04-03', 1, 1, "Наличные", 191000);
    
update
work_with_client
    set
    contract_id = 1
    where
    client_id = 1 and product_id = 1
    
INSERT INTO
work_with_client(
    product_id,
    manager_id,
    client_id,
    contract_id)
    Values
    (1,2,1,1);
    ''')
con.commit()
"""
#вывод клиентов, которые потратили больше всего денег суммарно за все покупки
cursor.execute('''
select name, sm from client inner join
(select client_id, sum(cost) as sm from contract) as cs ON cs.client_id = client.client_id
where sm = (select max(sm) from (select client_id, sum(cost) as sm from contract))
''')
print(cursor.fetchall())
#group Вывести имена менеджеров и количество клиентов с котороыми они работали
cursor.execute('''
select name, count(DISTINCT client_id) from manager inner join work_with_client ON (work_with_client.manager_id = manager.manager_id) group by name;
''')
print(cursor.fetchall())
cursor.execute('''
SELECT `AUTO_INCREMENT`
FROM  INFORMATION_SCHEMA.TABLES TABLE_NAME = "work_with_client"
''')
print(cursor.fetchall())
#
"""
con.executescript('''
Insert into 
work_with_client
(product_id, manager_id, client_id)
Values
(:p_prod, :p_manager, :p_client)
Insert into
pass_stage
(work)
(SELECT max(work_id) from work_with_client, 
''', {"p_prod": 2, "p_manager": 2, "p_client": 3})


"""