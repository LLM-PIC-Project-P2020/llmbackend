#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='wcr12345%',
                     database='sql_user')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 创建用户数据表
def create1_users():
    create1 = """CREATE table `users`(
            `user_id` int primary key,
            `user_name` varchar(20) not null,
            `password` varchar(20) not null,
            `user_state` int ,
            `user_email` varchar(20)
        );"""
    return create1

def create2_users_logins():
    create2 = """CREATE table `logins`(
        `user_id` int primary key,
        `login_time` varchar(20) not null,
        `token` varchar(20) not null
    );"""
    return create2




def create_user(user_id, username, email, password, status):

    try:
        # 创建游标对象
        cursor = db.cursor()

        # 插入用户数据的SQL语句
        sql_query = """
        INSERT INTO users (user_id, user_name, email, password, state)
        VALUES (%s, %s, %s, %s, %s)
        """
        user_data = (user_id, username, email, password, status)

        # 执行SQL语句
        cursor.execute(sql_query, user_data)

        # 提交事务
        db.commit()

        # 返回成功信息
        return True, "用户注册成功！"

    except pymysql.Error as e:
        # 回滚事务
        db.rollback()
        # 返回失败信息
        return False, f"用户注册失败: {e}"

    finally:
        # 关闭游标
        cursor.close()



"""
查询用户是否存在，返回布尔值
"""

def search(username, password):

    try:
        # 创建游标对象
        cursor = db.cursor()

        # 查询用户数据的SQL语句
        sql_query = """
        SELECT * FROM users WHERE user_name = %s AND password = %s
        """
        user_data = (username, password)

        # 执行SQL查询
        cursor.execute(sql_query, user_data)

        # 获取查询结果
        result = cursor.fetchone()

        # 如果查询到结果，返回 True；否则返回 False
        return result is not None

    except pymysql.Error as e:
        print(f"查询失败: {e}")
        return False

    finally:
        # 关闭游标
        cursor.close()



"""
添加logins数据库数据，返回是否成功
"""

from datetime import datetime

def user_login(user_id, token):

    try:
        # 获取当前时间
        login_time = datetime.now()

        # 创建游标对象
        cursor = db.cursor()

        # 插入登录信息的SQL语句
        sql_query = """
        INSERT INTO logins (user_id, login_time, token)
        VALUES (%s, %s, %s)
        """
        login_data = (user_id, login_time, token)

        # 执行SQL语句
        cursor.execute(sql_query, login_data)

        # 提交事务
        db.commit()

        # 返回成功
        return True

    except pymysql.Error as e:
        # 回滚事务
        db.rollback()
        print(f"登录信息插入失败: {e}")
        return False

    finally:
        # 关闭游标
        cursor.close()


"""
删除logins数据库数据，返回是否成功
"""

def user_logout(db, token):

    try:
        # 创建游标对象
        cursor = db.cursor()

        # 删除登录信息的SQL语句
        sql_query = """
        DELETE FROM logins
        WHERE token = %s
        """
        logout_data = (token,)

        # 执行SQL语句
        cursor.execute(sql_query, logout_data)

        # 提交事务
        db.commit()

        # 检查是否成功删除
        if cursor.rowcount > 0:
            return True  # 删除成功
        else:
            return False  # 没有匹配的记录

    except pymysql.Error as e:
        # 回滚事务
        db.rollback()
        print(f"登出信息删除失败: {e}")
        return False

    finally:
        # 关闭游标
        cursor.close()

def token_check(token):
    cursor = db.cursor() 
    sql_query = """
    SELECT * FROM logins WHERE token = %s
    """
    token_data = (token,)
    cursor.execute(sql_query, token_data)
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False

#cursor.execute(create)
#db.commit()



# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()


# 关闭数据库连接
db.close()
if __name__ == '__main__':
    create1_users()
    create2_users_logins()