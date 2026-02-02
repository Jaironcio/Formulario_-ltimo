import MySQLdb

def run(cur, q):
    print("\n#", q)
    try:
        cur.execute(q)
        rows = cur.fetchall()
        for r in rows:
            print(r)
        if not rows:
            print("(no rows)")
    except Exception as e:
        print("ERROR:", repr(e))


def main():
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="cermaq_incidencias", charset="utf8mb4")
    cur = db.cursor()

    run(cur, "SELECT DATABASE()")
    run(cur, "SHOW TABLES LIKE 'django_migrations'")
    run(cur, "SHOW TABLE STATUS LIKE 'django_migrations'")
    run(cur, "SELECT table_name, engine, table_rows FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name IN ('django_migrations','incidencias_incidencia')")
    run(cur, "SHOW TABLES LIKE 'incidencias_incidencia'")
    run(cur, "SHOW TABLE STATUS LIKE 'incidencias_incidencia'")

    cur.close()
    db.close()


if __name__ == '__main__':
    main()
