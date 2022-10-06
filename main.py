import psycopg2

def drop_db(conn):
    with conn.cursor() as cur: 
        cur.execute("""
            DROP TABLE clients;
            DROP TABLE phones;
            """)

def create_db(conn): # создать таблицы 
    with conn.cursor() as cur:       
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(40) NOT NULL,
                email VARCHAR(40) NOT NULL);
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES clients(id),
                number VARCHAR(20) UNIQUE);
            """)             
    conn.commit()

def add_client(conn, first_name, last_name, email, phones=None): # добавить нового клиента
    with conn.cursor() as cur: 
        cur.execute("""
                INSERT INTO clients (first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;
            """, (first_name, last_name, email))
        client_id = cur.fetchone()[0]        
    conn.commit()
    if phones == None:
        print('Phone is none, not update')
    else:
        add_phone(conn, client_id, phones)

def add_phone(conn, client_id, phones): # добавить телефон для существующего клиента
    with conn.cursor() as cur: 
        cur.execute("""
            INSERT INTO phones (number, client_id) VALUES( %s, %s);
            """, (phones, client_id))

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None): # изменить данные о клиенте
    cur = conn.cursor()
    if first_name == None:
        print('first_name is none, not update')
    else:
        sql_string = """
        UPDATE clients SET first_name = %s where id = %s;
        """
        cur.execute(sql_string, (first_name, client_id))
        conn.commit()
    if last_name == None:
        print('last_name is none, not update')
    else:
        sql_string = """
        UPDATE clients SET last_name = %s where id = %s;
        """
        cur.execute(sql_string, (last_name, client_id))
        conn.commit()

    if email == None:
        print('last_name is none, not update')
    else:
        sql_string = """
        UPDATE clients SET email = %s where id = %s;
        """
        cur.execute(sql_string, (email, client_id))
        conn.commit()

    if phones == None:
        print('phones is none, not update')
    else:
        add_phone(conn, client_id, phones)

def delete_phone(conn, client_id, phone): # удалить телефон для существующего клиента
    with conn.cursor() as cur: 
        cur.execute("""
        DELETE FROM phones WHERE client_id = %s and number = %s ;
           """, (client_id, phone))
    conn.commit()

def delete_client(conn, client_id): # удалить существующего клиента
    with conn.cursor() as cur: 
        cur.execute("""
            DELETE FROM phones WHERE client_id = %s;
            """, (client_id,))
        conn.commit()
    
    with conn.cursor() as cur: 
        cur.execute("""
            DELETE FROM clients WHERE id = %s;
            """, (client_id,)) 
        conn.commit()   

def find_client(conn, first_name=None, last_name=None, email=None, phone=None): # найти клиента по его данным (имени, фамилии, email-у или телефону)
    cur = conn.cursor()

    if first_name == None:
        print('Не найдено')
    else:
        cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, p.number from clients c
        LEFT JOIN phones p ON c.id = p.client_id
        WHERE c.first_name = %s;
                """, (first_name,))
        cursor_string = cur.fetchall()
    
    if last_name == None:
        print('Не найдено')
    else:
        cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, p.number from clients c
        LEFT JOIN phones p ON c.id = p.client_id
        WHERE c.last_name = %s;
                """, (last_name,))
        for fetch_all in cur.fetchall():
            cursor_string.append(fetch_all)
    
    if email == None:
        print('Не найдено')
    else:
        cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, p.number from clients c
        LEFT JOIN phone_number pn ON c.id = pn.client_id
        WHERE c.email = %s;
                """, (email,))
        for fetch_all in cur.fetchall():
            cursor_string.append(fetch_all)


    if phone == None:
        print('Не найдено')
    else:
        cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, p.number from clients c
        LEFT JOIN clients c on pn.client_id = c.id
        WHERE p.number = %s;
                """, (phone,))
        for fetch_all in cur.fetchall():
            cursor_string.append(fetch_all)
        return cursor_string

    conn.commit()   



with psycopg2.connect(database="netology_db", user="postgres", password="password") as conn:
    #create_db(conn)
    #add_client (conn, 'Иван', 'Иванов', 'ivan@mail.ru', '+78888888888')
    #add_client (conn, 'Петр', 'Петров', 'petr@mail.ru')
    #add_phone (conn, 2 , '+77777777777')
    #change_client(conn, 1, 'Вася')
    find_client(conn, first_name='Иван')

conn.close
