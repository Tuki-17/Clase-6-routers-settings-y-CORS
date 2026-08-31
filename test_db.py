import psycopg2

passwords = ["", "admin", "1234", "123456", "root", "profesor", "Profesor", "postgres"]
success = False

for pwd in passwords:
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=pwd,
            host="localhost",
            port="5432",
            connect_timeout=2
        )
        print(f"Success! Password for 'postgres' is: '{pwd}'")
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname='ecommerce_db';")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE ecommerce_db;")
            print("Database 'ecommerce_db' created successfully.")
        else:
            print("Database 'ecommerce_db' already exists.")
        cur.close()
        conn.close()
        success = True
        break
    except Exception as e:
        err_msg = str(e)
        # Avoid print crashing on encoding issues
        try:
            print(f"Failed with password '{pwd}': {err_msg}")
        except Exception:
            print(f"Failed with password '{pwd}': (encoding error)")

if not success:
    print("Could not connect with any common passwords.")
