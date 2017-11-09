from .__import import *
from .searching import *

def __columnDesc(description):
    return [(l[0], *__typeStr_and_justify(l[1]), l[3], l[6]) for l in description]

def __typeStr_and_justify(code):
    # integral
    if binarysearch([0, 1, 2, 3, 8, 9, 16], code):
        return ("d", False)
    # floating point
    if code <= 5:
        return ("f", False)
    # NULL
    if code == 6:
        return ("r", False)
    # string
    return ("s", True)


# Connect to the database
def __connectDB(host, user, pw, db, charset="utf8mb4", *argv, **kwargs):
    #debug("*argv: %r, **kwargs: %r" %(argv, kwargs))
    conn = None
    try:
        conn = pymysql.connect(host=host,
                               user=user, 
                               password=pw,
                               db=db,
                               charset=charset,
                               cursorclass=pymysql.cursors.DictCursor)
    except:
        warning("cannot connect DB")
    return conn


def connectDB():
    return __connectDB(host="localhost",
                       user="all_proj",
                       pw="all_proj",
                       db="all_proj")

def query(table, columns="", condition="", join=""):
    con = connectDB()
    if con is None:
        return ([], [], [])
    try:
        with con.cursor() as c:
            sql = "SELECT %s FROM %s" % ("*" if columns == "" else columns, table) \
                    + ("" if condition == "" else (" WHERE " + condition))\
                    + ("" if join == "" else (" INNER JOIN " + join))
            debug(sql)
            c.execute(sql)
            result = c.fetchall()
            cols = [l[0] for l in c.description]
            return (__columnDesc(c.description), cols, [[row[col] for col in cols] for row in result])
    finally:
        con.close()

def insert(table, columns=[], values=[]):
    con = connectDB()
    if con is None:
        return -1

    cols = "" if columns == [] else "(" + ", ".join(columns) + ") "
    debug(cols)
    if values == []:
        error("values == []")

    vals = "VALUES (" + ", ".join(values) + ")"
    debug(vals)

    if len(columns) > 0 and len(columns) != len(values):
        error("len(columns) > 0 BUT len(columns) != len(values)")

    try:
        with con.cursor() as c:
            sql = "INSERT INTO %s %s%s" % (table, cols, vals)
            debug(sql)
            c.execute(sql)
            con.commit()
            ret = c.lastrowid
            debug("c.lastrowid:", ret)
            return ret
    finally:
        con.close()

def update(table, column_and_values=[], condition=""):
    con = connectDB()
    if con is None:
        return -1

    if column_and_values == []:
        error("column_and_values == []")
    debug(column_and_values)
    col_and_val_lst = ["%s = %s" for (col, val) in column_and_values]
    debug(col_and_val_lst)
    col_and_val_SQL = ", ".join(col_and_val_lst)
    debug(col_and_val_SQL)

    try:
        with con.cursor() as c:
            sql = "UPDATE %s SET %s %s" % (table, col_and_val_SQL, "" if condition == "" else "WHERE " + condition)
            debug(sql)
            c.execute(sql)
            con.commit()
            rc = c.rowcount
            debug("row affected: %d" % rc)
            return rc
    finally:
        con.close()

def delete(table, condition=""):
    if condition == "":
        warning("deleting all in %s, condition = \"\"" % table)
    con = connectDB()
    
    if con is None:
        return -1

    try:
        with con.cursor() as c:
            sql = "DELETE FROM %s%s" % (table, "" if condition == "" else "WHERE %s" % condition)
            debug(sql)
            c.execute(sql)
            con.commit()
            rc = c.rowcount
            debug("row affected: %d" % rc)
            return rc
    finally:
        con.close()

