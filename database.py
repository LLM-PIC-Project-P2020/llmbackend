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

def create3_courses():
    create3 = """CREATE table `courses`(
            `course_id` int primary key,
            `course_name` varchar(20) not null,
            `course_type` varchar(20) not null,
            `course_content` varchar(100) not null
    );"""
    return create3

def create4_users_history():
    create4 = """CREATE table `history`(
            `user_id` int primary key,
            `user_name` varchar(20) not null,
            `learned_course` varchar(50) not null,
            `learn_time` varchar(20) not null,
            `code_time` varchar(20) not null
    );"""
    return create4


"""
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
添加courses数据库数据，返回是否成功
"""

def add_course(db, course_id, course_name, course_category, course_content):

    try:
        cursor = db.cursor()

        # 插入课程数据的SQL语句
        sql_query = """
        INSERT INTO courses (course_id, course_name, course_type, course_content)
        VALUES (%s, %s, %s, %s)
        """
        course_data = (course_id, course_name, course_type, course_content)

        # 执行SQL语句
        cursor.execute(sql_query, course_data)

        # 提交事务
        db.commit()

        return True, "课程添加成功"

    except pymysql.Error as e:
        # 回滚事务
        db.rollback()
        return False, f"课程添加失败: {e}"

    finally:
        # 关闭游标
        cursor.close()

"""
删除courses数据库数据，返回是否成功
"""

def delete_course(db, course_name):

    try:
        cursor = db.cursor()

        # 检查课程是否存在
        check_sql = "SELECT course_id FROM courses WHERE course_name = %s"
        cursor.execute(check_sql, (course_name,))
        if not cursor.fetchone():
            return False, "课程不存在"

        # 删除课程的SQL语句
        delete_sql = "DELETE FROM courses WHERE course_name = %s"
        cursor.execute(delete_sql, (course_name,))

        # 检查是否成功删除
        if cursor.rowcount == 0:
            return False, "删除失败，课程可能不存在"

        # 提交事务
        db.commit()
        return True, "课程删除成功"

    except pymysql.Error as e:
        # 回滚事务
        db.rollback()
        return False, f"删除课程时出错: {e}"

    finally:
        # 关闭游标
        cursor.close()

"""
调用课程，返回课程内容
"""

def get_course(db, course_name=None, course_type=None):

    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 基础SQL查询
        sql_query = "SELECT * FROM courses WHERE 1=1"
        params = []

        # 动态添加查询条件
        if course_name:
            sql_query += " AND course_name = %s"
            params.append(course_name)
        if course_category:
            sql_query += " AND category = %s"
            params.append(course_category)

        # 执行查询
        cursor.execute(sql_query, tuple(params))
        results = cursor.fetchall()

        if not results:
            return False, "未找到匹配的课程"

        return True, results

    except pymysql.Error as e:
        return False, f"查询课程时出错: {e}"

    finally:
        cursor.close()

#cursor.execute(create)
#db.commit()

"""
增加课程学习时间
"""

def add_course_time(db, user_name, time_to_add):

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
更新最近学习课程
"""

def update_recent(db, user_name, course_name):

    try:
        cursor = db.cursor()

        # 检查用户是否存在
        check_user_sql = "SELECT user_id FROM users WHERE user_name = %s"
        cursor.execute(check_user_sql, (user_name,))
        if not cursor.fetchone():
            return False, f"用户 {user_name} 不存在"

        # 检查课程是否存在（可选，根据需求）
        check_course_sql = "SELECT course_id FROM courses WHERE course_name = %s"
        cursor.execute(check_course_sql, (course_name,))
        if not cursor.fetchone():
            return False, f"课程 {course_name} 不存在"

        # 更新最近学习的课程
        update_sql = """
        UPDATE history 
        SET learned_course = %s,
        WHERE user_name = %s
        """
        cursor.execute(update_sql, (course_name, user_name))

        # 4. 检查是否更新成功
        if cursor.rowcount == 0:
            return False, "更新最近学习课程失败"

        db.commit()
        return True, f"用户 {user_name} 的最近学习课程已更新为 {course_name}"

    except pymysql.Error as e:
        db.rollback()
        return False, f"数据库错误: {e}"
    except Exception as e:
        return False, f"系统错误: {e}"
    finally:
        cursor.close()

"""
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
            learned_course, 
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

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()


# 关闭数据库连接
db.close()