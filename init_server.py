#!/usr/bin/python3
import psycopg2
# try:
conn = psycopg2.connect(dbname='local', user='root', password='DQnqGP6y', host='localhost', port='5432')
# except:
#     print("I am unable to connect to the database")

cursor = conn.cursor()
func_insert = """INSERT INTO public.terminal_session (sessionId, terminalId, status, clientId, service, balance) \
                VALUES ('0', 23, 0, 0, 5, 0)"""
#cursor.execute("")

cursor.execute("DELETE FROM public.service_service")
service_insert = """INSERT INTO public.service_service (id, code, name, unit, price) VALUES \
            (1, '0', 'Hiwrt', 'l', 26), \
            (2, '1', 'Lowrt', 'l', 26), \
            (3, '2', 'Foam', 'l', 45), \
            (4, '3', 'WAX', 'l', 45), \
            (5, '4', 'OSMOS', 'l', 26), \
            (6, '5', 'PAUSE', 'l', 0)"""
cursor.execute(service_insert)
conn.commit()
cursor.close()
conn.close()
