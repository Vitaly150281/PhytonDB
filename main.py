import psycopg2

def structure_db(conn):
    cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id      SERIAL      PRIMARY KEY,
                name    VARCHAR(10) NOT NULL,
                surname VARCHAR(10) NOT NULL,
                email   VARCHAR(50) NOT NULL
            );
    """)
    cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
                id        SERIAL      PRIMARY KEY,
                phone     VARCHAR(12) NOT NULL,
                client_id INTEGER     NOT NULL REFERENCES clients(id)
            );
    """)
    conn.commit()

def add_client(conn, first_name, last_name, email, new_phone=None):
    cur.execute("""
            INSERT INTO clients(name, surname, email) 
            VALUES (%s, %s, %s) RETURNING id;
    """, (first_name, last_name, email))
    new_client = cur.fetchone()
    if new_phone is not None:
        cur.execute("""
                INSERT INTO phones(phone, client_id) 
                VALUES (%s, %s);
        """, (new_phone, new_client[0]))
    conn.commit()

def add_phone(conn, new_phone, id_client):
    cur.execute("""
            SELECT phone 
              FROM phones 
             WHERE phone=%s 
               AND client_id=%s;
    """, (new_phone, id_client))
    found_phone = cur.fetchone()

    if found_phone is None:
        cur.execute("""
                INSERT INTO phones(phone, client_id) 
                VALUES (%s, %s);
        """, (new_phone, id_client))
    conn.commit()

def change_client(conn, id_client, first_name=None, last_name=None, email=None, new_phone=None):
    if first_name is not None:
        cur.execute("""
                UPDATE clients 
                   SET name=%s 
                 WHERE id=%s;
        """, (first_name, id_client))

    if last_name is not None:
        cur.execute("""
                UPDATE clients 
                   SET surname=%s 
                 WHERE id=%s;
        """, (last_name, id_client))

    if email is not None:
        cur.execute("""
                UPDATE clients 
                   SET email=%s 
                 WHERE id=%s;
        """, (email, id_client))

    if new_phone is not None:
        cur.execute("""
                SELECT client_id, COUNT(phone)
                  FROM phones
                 GROUP BY client_id
                HAVING client_id=%s;
        """, (id_client, ))
        if cur.fetchone()[1] > 1:
            change_phone = input("У клиента больше 1го номера, выберите номер: ")
            cur.execute("""
                    UPDATE phones
                       SET phone=%s
                     WHERE phone=%s
                       AND client_id=%s;
            """, (new_phone, change_phone, id_client))
        else:
            cur.execute("""
                  UPDATE phones
                     SET phone=%s
                   WHERE client_id=%s;
            """, (new_phone, id_client))
    conn.commit()

def del_phone(conn, id_client, new_phone):
    cur.execute("""
            DELETE FROM phones
             WHERE phone=%s
               AND client_id=%s;
    """, (new_phone, id_client))
    conn.commit()

def del_client(conn, id_client):
    cur.execute("""
            DELETE FROM phones 
             WHERE client_id=%s;
    """, (id_client,))
    cur.execute("""
            DELETE FROM clients 
             WHERE id=%s;
    """, (id_client,))
    conn.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if phone is not None:
        cur.execute("""
                SELECT c.id 
                  FROM clients c
                       JOIN phones p 
                       ON p.client_id = c.id
                 WHERE p.phone=%s;  
        """, (phone,))
    else:
        cur.execute("""
                SELECT id FROM clients 
                 WHERE name=%s 
                    OR surname=%s 
                    OR email=%s;
        """, (first_name, last_name, email))
    print(cur.fetchone())

if __name__ == '__main__':
    conn = psycopg2.connect(database="netology_db", user="postgres", password="Spartak")
    with conn.cursor() as cur:
        # structure_db(conn)
        # add_client(conn, 'Владимир', 'Путин', 'putin@mail.ru', '+79139184242')
        # add_client(conn, 'Петр', 'Петров', 'petrov@gmail.com')
        # add_phone(conn, '+79137891521', 5)
        # change_client(conn, 4, 'Ivan')
        # change_client(conn, 4, None, 'Ivanov')
        # change_client(conn, 5, None, None, None, '777')
        # del_phone(conn, 5, '777')
        # del_client(conn, 5)
        # add_client(conn, 'Владимир', 'Путин', 'putin@mail.ru', '+79139184242')
        # add_client(conn, 'Петр', 'Первый', 'petr@mail.ru', '+79258962145')
        # find_client(conn, None, None, None, '+79139184242')
        # add_phone(conn, '888888', 8)
        # change_client(conn, 8, None, None, None, '777')
        # change_client(conn, 7, None, None, None, '22222')
    conn.close()
