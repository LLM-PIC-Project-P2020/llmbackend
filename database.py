#!/usr/bin/python3

import pymysql


# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='12345678',
                     database='sql_user')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")

# 创建用户数据表

create1 = """CREATE table `users`(
            `user_id` int primary key,
            `user_name` varchar(20) not null,
            `password` varchar(20) not null,
            `user_state` int ,
            `user_email` varchar(20)
        );"""


create2 = """CREATE table `logins`(
        `user_id` int primary key,
        `login_time` varchar(20) not null,
        `token` varchar(20) not null
    );"""


create3 = """CREATE table `classes`(
            `class_id` int primary key,
            `class_name` varchar(20) not null,
            `chapter_name` varchar(20) not null,
            `chapter_id` int not null,
            `class_content` varchar(100) not null
    );"""

create4 = """CREATE table `history`(
            `user_id` int primary key,
            `user_name` varchar(20) not null,
            `learned_class` varchar(50) not null,
            `learn_time` varchar(20) not null,
            `code_time` varchar(20) not null
    );"""

create5 = """CREATE table `course`(
            `chapter_id` int primary key,
            `chapter_name` varchar(20) not null
    );"""

def create_tables(db,excute):
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='12345678',
                     database='sql_user')
    cursor = db.cursor()
    try:
        cursor.execute(excute)
        db.commit()
        print("Table 'user' created successfully!")
    except pymysql.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()


"""
表users函数
向用户信息数据库添加数据
"""
def create_user(db, user_id, username, email, password, status):

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
表users函数
查询用户是否存在，返回布尔值
"""

def search(db, username, password):

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
表logins函数
添加logins数据库数据，返回是否成功
"""

from datetime import datetime

def user_login(db, user_id, token):

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
表logins函数
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


"""
表classes函数
获取某一特定章节的所有课程信息
"""

def get_all_classes(db, chapter_id):

    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 查询特定章节的课程
        sql = """
        SELECT class_id as id, class_name as name 
        FROM classes 
        WHERE chapter_id = %s
        ORDER BY class_id
        """
        cursor.execute(sql, (chapter_id,))

        classes = cursor.fetchall()

        if not classes:
            return True, []  # 章节存在但无课程时返回空列表

        return True, classes

    except pymysql.Error as e:
        return False, f"数据库查询错误: {e}"
    finally:
        cursor.close()

"""
表classes函数
输入章节ID和课程ID，获取课程内容
"""

def get_class_description(db, chapter_id, class_id):

    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 查询特定课程的内容
        sql = """
        SELECT class_content 
        FROM classes 
        WHERE chapter_id = %s AND class_id = %s
        """
        cursor.execute(sql, (chapter_id, class_id))

        result = cursor.fetchone()

        if not result:
            return False, "未找到指定课程"

        return True, result['content']

    except pymysql.Error as e:
        return False, f"数据库查询错误: {e}"
    finally:
        cursor.close()

"""
表history函数
增加课程学习时间
"""

def add_class_time(db, user_name, time_to_add):

    try:
        # 验证输入时间是否为有效数字
        if not isinstance(time_to_add, (int, float)) or time_to_add <= 0:
            return False, "时间参数必须是正数"
        cursor = db.cursor()

        # 检查用户是否存在
        check_sql = "SELECT user_id FROM history WHERE user_name = %s"
        cursor.execute(check_sql, (user_name,))
        if not cursor.fetchone():
            return False, "用户不存在"

        # 更新学习时间
        update_sql = """
        UPDATE history 
        SET learn_time = learn_time + %s 
        WHERE user_name = %s
        """
        cursor.execute(update_sql, (time_to_add, user_name))

        # 检查是否更新成功
        if cursor.rowcount == 0:
            return False, "更新学习时间失败"

        db.commit()
        return True, "学习时间已成功更新"

    except pymysql.Error as e:
        db.rollback()
        return False, f"数据库错误: {e}"
    except ValueError:
        return False, "时间参数必须是数字"
    finally:
        cursor.close()

"""
表history函数
增加编程时间
"""

def add_code_time(db, user_name, time_to_add):

    try:
        # 验证输入时间是否为有效数字
        if not isinstance(time_to_add, (int, float)) or time_to_add <= 0:
            return False, "时间参数必须是正数"

        cursor = db.cursor()

        # 检查用户是否存在
        check_sql = "SELECT user_id FROM history WHERE user_name = %s"
        cursor.execute(check_sql, (user_name,))
        if not cursor.fetchone():
            return False, f"用户不存在"

        # 更新编程时间（原子操作）
        update_sql = """
        UPDATE history 
        SET code_time = code_time + %s 
        WHERE user_name = %s
        """
        cursor.execute(update_sql, (time_to_add, user_name))

        # 验证是否更新成功
        if cursor.rowcount == 0:
            return False, "更新编程时间失败"

        db.commit()
        return True, f"成功为用户 {user_name} 增加 {time_to_add} 小时编程时间"

    except pymysql.Error as e:
        db.rollback()
        return False, f"数据库错误: {e}"
    except Exception as e:
        return False, f"系统错误: {e}"
    finally:
        cursor.close()

"""
表history函数
更新最近学习课程
"""

def update_recent(db, user_name, class_name):

    try:
        cursor = db.cursor()

        # 检查用户是否存在
        check_user_sql = "SELECT user_id FROM users WHERE user_name = %s"
        cursor.execute(check_user_sql, (user_name,))
        if not cursor.fetchone():
            return False, f"用户 {user_name} 不存在"

        # 检查课程是否存在（可选，根据需求）
        check_class_sql = "SELECT class_id FROM classes WHERE class_name = %s"
        cursor.execute(check_class_sql, (class_name,))
        if not cursor.fetchone():
            return False, f"课程 {class_name} 不存在"

        # 更新最近学习的课程
        update_sql = """
        UPDATE history 
        SET learned_class = %s,
        WHERE user_name = %s
        """
        cursor.execute(update_sql, (class_name, user_name))

        # 4. 检查是否更新成功
        if cursor.rowcount == 0:
            return False, "更新最近学习课程失败"

        db.commit()
        return True, f"用户 {user_name} 的最近学习课程已更新为 {class_name}"

    except pymysql.Error as e:
        db.rollback()
        return False, f"数据库错误: {e}"
    except Exception as e:
        return False, f"系统错误: {e}"
    finally:
        cursor.close()

"""
表history函数
创建默认学习记录
"""

def create_history(db, user_id, user_name):

    try:
        cursor = db.cursor()

        # 检查用户是否已存在历史记录
        check_sql = "SELECT user_id FROM history WHERE user_id = %s"
        cursor.execute(check_sql, (user_id,))
        if cursor.fetchone():
            return False, "该用户已存在历史记录"

        # 创建默认历史记录
        insert_sql = """
        INSERT INTO history (
            user_id, 
            user_name, 
            learned_class, 
            learn_time, 
            code_time
        ) VALUES (
            %s, %s, '无', 0, 0
        )
        """
        cursor.execute(insert_sql, (user_id, user_name))

        # 验证是否创建成功
        if cursor.rowcount == 0:
            return False, "创建历史记录失败"

        db.commit()
        return True, f"用户 {user_name} 的默认历史记录已创建"

    except pymysql.Error as e:
        db.rollback()
        return False, f"数据库错误: {e}"
    except Exception as e:
        return False, f"系统错误: {e}"
    finally:
        cursor.close()

"""
表course函数
获取所有章节信息
"""

def get_all_course(db):

    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 查询所有章节信息
        sql = """
        SELECT chapter_id as id, chapter_name as name 
        FROM course 
        GROUP BY chapter_id, chapter_name
        ORDER BY chapter_id
        """
        cursor.execute(sql)

        chapters = cursor.fetchall()

        return True, chapters if chapters else []

    except pymysql.Error as e:
        return False, f"数据库查询错误: {e}"
    finally:
        cursor.close()

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()


# 关闭数据库连接
db.close()

if __name__ == '__main__':
    create_tables(db,create1)
    create_tables(db,create2)
    create_tables(db,create3)
    create_tables(db,create4)
    create_tables(db,create5)