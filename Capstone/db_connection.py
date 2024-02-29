import mysql.connector

def create_connection():
    cnx = mysql.connector.connect(user='sql3687279', password='jY1vpLgRWl',
                              host='sql3.freesqldatabase.com',
                              database='sql3687279')
    return cnx

def close_connection(cnx):
    cnx.close()
    
def execute_query(query, cnx):
    if cnx and cnx.is_connected():
        with cnx.cursor() as cursor:

            result = cursor.execute(query)

            rows = cursor.fetchall()

            for row in rows:
                return str(row[0])

    else:
        return "Could not connect"
    
def get_inventory(item):
    query = "SELECT sum(available_quantity) from item where category like '%{}%'".format(item)
    cnx = create_connection()
    value = execute_query(query,cnx)
    close_connection(cnx)
    return value
