import pymysql
from .debug import *

#connect database
def getConnection():
    db = pymysql.connect(host = "localhost",  
                         user = "all_proj", 
                         password = "all_proj", 
                         db = "all_proj",
                         cursorclass=pymysql.cursors.DictCursor)
    return db

def getDBcursor():
    db = getConnection()
    return db.cursor

#display data
def queryData(table, columns="*", condition=""):
    sql = "SELECT "  + columns + " FROM " + table + ("" if condition == "" else(" WHERE " + condition))
    conn = getConnection()
    try:
    #cursor = getDBcursor()
        with conn.cursor() as cursor:
            print(sql)
            cursor.execute(sql) 
            result = cursor.fetchall()
            print(cursor.description)
            cols = [col[0] for col in cursor.description]
            return (cols, [[row[col] for col in cols] for row in result])
    
    finally:
        conn.close()

def insertData(table, columns="", values=""):
    """insert data into database"""
    columns = ("" if columns == "" else(" ( " + columns + ") " ))
    sql = ("INSERT INTO " + table + " " + columns + " VALUE ( " + values + " ) ") 
    
    conn = getConnection()
    try:
        
        with conn.cursor() as cursor:
            print(sql)
            cursor.execute(sql) 
            conn.commit()
            return cursor.lastrowid
    
    finally:
        conn.close()   
def updateData(table, columns="", values="", condition=""):
    """update data into database"""
    sql = ("UPDATE " + table + " SET " + columns + " = " + values + ("" if condition == "" else(" WHERE " + condition)))
    conn = getConnection()
    try:
    
        with conn.cursor() as cursor:
            print(sql)
            cursor.execute(sql)
            conn.commit()
            return cursor.rowcount
    
    finally:
        conn.close()

def deleteData(table, condition=""):
    """delete data from database"""
    sql = ("DELETE FROM " + table + ("" if condition == "" else(" WHERE " + condition)))
    conn = getConnection()
    try:
        with conn.cursor() as cursor:
            print(sql)
            cursor.execute(sql)
            conn.commit()
            return cursor.rowcount
    
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
