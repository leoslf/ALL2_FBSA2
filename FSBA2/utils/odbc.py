import pymysql
from .debug import *
from .db_extra import *

fix_import(__file__)
                               


#connect database
def getConnection():
    # TODO use config_dict('db.ini')
    db = None

    try:
        db = pymysql.connect(host = "localhost",  
                             user = "all_proj", 
                             password = "all_proj", 
                             db = "all_proj2",
                             cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        error("cannot get DB connection")

    return db

#def getDBcursor():
#    db = getConnection()
#    return db.cursor

#display data
def queryData(table, columns="*", condition="", join=""):
    sql = "SELECT "  + columns \
                + " FROM " + table \
                + ("" if join == "" else (" INNER JOIN " + join)) \
                + ("" if condition == "" else (" WHERE " + condition))
    debug(sql)

    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql) 
            rows_dict = cursor.fetchall()
            cols = [col[0] for col in cursor.description]
            debug(rows_dict)
            return (cols, [[row[col] for col in cols] for row in rows_dict])
    except Exception as e:
        error("MYSQLError: errno %r, %r", e.args[0], e)
    finally:
        conn.close()

def insertData(table, columns="", values=""):
    """insert data into database"""
    columns = ("" if columns == "" else(" ( " + columns + ") " ))
    sql = ("INSERT INTO " + table + " " + columns + " VALUE ( " + values + " ) ") 
    debug(sql)
    
    conn = getConnection()
    try:
        
        with conn.cursor() as cursor:
            print(sql)
            cursor.execute(sql) 
            conn.commit()
            return cursor.lastrowid
    
    except Exception as e:
        error("MYSQLError: errno %r, %r", e.args[0], e)
    finally:
        conn.close()   

def updateData(table, column_and_value="", condition=""):
    """update data into database"""
    sql = ("UPDATE " + table + " SET " + column_and_value + ("" if condition == "" else(" WHERE " + condition)))
    debug(sql)

    conn = getConnection()
    try:
    
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        error("MYSQLError: errno %r, %r", e.args[0], e)
    finally:
        conn.close()

def deleteData(table, condition=""):
    """delete data from database"""
    sql = ("DELETE FROM " + table + ("" if condition == "" else(" WHERE " + condition)))
    debug(sql)

    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()
            return cursor.rowcount
    except Exception as e:
        error("MYSQLError: errno %r, %r", e.args[0], e)
    finally:
        conn.close()
    
#close database connection
def close():
    db = getConnection()
    try:
        if(db):
            db.close()
            print("Database closed.")
    except Exception:
        error(sys.exc_info())
