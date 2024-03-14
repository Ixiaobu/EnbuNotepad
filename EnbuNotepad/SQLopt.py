import os
from collections import deque
from shutil import copyfile
import sqlite3
import xlsxwriter

from ReadIni import AllQss
from ToolFun import GetAllTime


# 打印方法 ========================================
# 返回一个数据库的所有表名

def GetAllTableName(cur):
    cur.execute("select name from sqlite_master where type='table' order by name;")
    return [t[0] for t in  cur.fetchall()]

# 获取一个表单的所有表头
def GetTableName(cur, table_name):
    cur.execute("PRAGMA table_info(%s)" % table_name)  # 获取表头
    return [name[1] for name in cur.fetchall()]

# 返回一个表的所有内容
def GetTableInfo(cur, table_name):
    cur.execute("PRAGMA table_info(%s)" % table_name)  # 获取表头
    table = [name[1] for name in cur.fetchall()]

    ans = [table]
    cur.execute("SELECT * FROM %s" % table_name)  # 执行查询
    for row in cur.fetchall():
        temp = list(row)
        ans.append(temp)
    return ans

# 打印一个表单
def SqlToStr(cur, table_name):
    ans = []
    cur.execute("PRAGMA table_info(%s)" % table_name)  # 获取表头
    ans.append("\t\t".join(map(str, (f[1] for f in cur.fetchall()))))  # 获取每一行的内容
    cur.execute("SELECT * FROM %s" % table_name)  # 执行查询
    for row in cur.fetchall():
        ans.append("\t\t".join(map(str, row)))
    return "\n".join(ans)
# ========================================

# 新建方法==================================
# 创建一个新的表单

def SqlInit():
    s = "CREATE TABLE %s" % "根目录"
    s = s + "(" + " TEXT,".join(["主题名称", "创建时间", "主题备注", "主题类型", "主题密码", "加载方式"]) + " TEXT);"
    cur.execute(s)  # 创建新的表
    conn.commit()  # 提交

# 创建一个表
def CreateTable(conn, cur, table_info, name_list):
    try:
        s = "CREATE TABLE %s" % (table_info[0])
        s = s + "(" + " TEXT,".join(name_list) + " TEXT);"
        cur.execute(s)  # 创建新的表
        InsertSql(conn, cur, "根目录", table_info)  # 将新的表加入根目录
        conn.commit()  # 提交
        return True
    except:
        return False

# 向一个数据库写入内容
def InsertSql(conn, cur, table_name, values):
    text = "INSERT INTO %s VALUES(%s)" % (table_name, "'" + "', '".join(map(str, values)) + "'")
    cur.execute(text)
    conn.commit()  # 提交
# ========================================

# 删除方法==================================
# 删除某一行
def DelereRow(conn, cur, table_name, name, val):
    s = '''DELETE FROM %s WHERE''' % table_name
    s += " AND ".join(''' %s = "%s" ''' % (t_n, v) for t_n, v in zip(name, val))
    cur.execute(s)
    conn.commit()  # 提交

# 替换某一行
def ReplaceRow(conn, cur, table_name, name, old_data, new_data):
    s = "UPDATE %s SET " % table_name
    s += ", ".join(''' %s = "%s" ''' % (t_n, v) for t_n, v in zip(name, new_data))
    s += " WHERE "
    s += " AND ".join(''' %s = "%s" ''' % (t_n, v) for t_n, v in zip(name, old_data))
    s += ";"
    cur.execute(s)
    conn.commit()  # 提交

# 清空某个表
def DeleteTable(conn, cur, table_name):
    # 执行删除表中所有数据的操作
    cur.execute("DROP TABLE %s" % table_name)
    DelereRow(conn, cur, "根目录", ["主题名称"], [table_name])
    conn.commit()  # 提交

# 删除整个数据库
def DeleteSql(conn, cur):
    for name in GetAllTableName(cur):
        cur.execute("DROP TABLE %s" % name)
    SqlInit()  # 初始化
    conn.commit()  # 提交

# ========================================


# 查询方法===================================
# 按项目名称查询
def FindName(cur, table_name, column_name, input):
    try:
        s = "SELECT * FROM " + table_name +" WHERE " + column_name + " LIKE ?"
        cur.execute(s, ('%' + input + '%',))
        ans = []
        for row in cur.fetchall():
            temp = list(row)
            ans.append(temp)
        return ans
    except:
        return []

def SelectSql(cur, table_name, input):
    if input[:4] == "SQL:":
        try:
            s = "SELECT * FROM " + table_name +  input[4:]
            cur.execute(s)
            ans = []
            for row in cur.fetchall():
                temp = list(row)
                ans.append(temp)
            return ans
        except:
            return []
    else:
        return FindName(cur, table_name, "标题", input)
# ========================================

# 其他方法

# 改名方法
def RenameTableName(conn, cur, table_name, names):
    # 防止用户的输入出现环
    names = deque(names)

    while len(names) > 0:
        old, new = names.popleft()
        try:
            s = "ALTER TABLE %s RENAME COLUMN %s TO %s" % (table_name, old, new)
            cur.execute(s)
        except:
            names.append([old, new])
    conn.commit()  # 提交

# 把一列copy到另一个表上
def CopyAtoB(conn, cur, table_name_A, column_name_A, table_name_B, column_name_B):
    # 选择要复制的列
    cur.execute("SELECT %s FROM %s" % (column_name_A, table_name_A, ))
    source_column = cur.fetchall()
    # 将选定的列插入到目标表中：
    # 插入到目标表
    for row in source_column:
        cur.execute("INSERT INTO %s (%s) VALUES (?)" % (table_name_B, column_name_B), row)
    conn.commit()  # 提交

# 更改一个主题的信息
def UpDataTable(conn, cur, table_data_old, table_name_old, table_data_new, table_name_new):

    # 检查是否存在同名的临时表，存在则删除
    cur.execute('DROP TABLE IF EXISTS temp_table')
    # 重命名原表
    cur.execute("ALTER TABLE %s RENAME TO temp_table" % table_data_old[0])

    # 往旧表里面添加数据列
    old_rename_name = set(GetTableName(cur, "temp_table"))
    s = []
    for colmn_name in table_name_new:
        if colmn_name not in old_rename_name:
            cur.execute("ALTER TABLE temp_table ADD COLUMN %s TEXT" % (colmn_name))

    # 从旧表构建新表
    new_rename_name_s = ", ".join(table_name_new)
    s = '''CREATE TABLE %s AS 
                 SELECT %s
                 FROM %s''' % (table_data_new[0], new_rename_name_s, "temp_table")
    cur.execute(s)

    # 删除临时表
    cur.execute('DROP TABLE temp_table')

    # 替换根目录中的信息
    ReplaceRow(conn, cur, "根目录",
               ["主题名称", "创建时间", "主题备注", "主题类型", "主题密码", "加载方式"],
               table_data_old,
               table_data_new)
    conn.commit()  # 提交

# 交换两行信息
def ExchangeTwoRow(conn, cur, table_name, row1, row2):
    name = GetTableName(cur, table_name)
    temp_row = ["周恩布是世界上最帅的男人" for _ in range(len(row1))]
    ReplaceRow(conn, cur, table_name, name, row1, temp_row)
    ReplaceRow(conn, cur, table_name, name, row2, row1)
    ReplaceRow(conn, cur, table_name, name, temp_row, row2)
    conn.commit()  # 提交

# 抱一个表单保存为excel
def SaveSqlAsExcel(cur, table_name):
    try:
        data = GetTableInfo(cur, table_name)

        # 判断文件夹是否存在，如果不存在则创建一个
        folder_name = "SavedFile"
        if not os.path.exists(folder_name):
            # 如果文件夹不存在，创建文件夹
            os.makedirs(folder_name)

        # 创建一个Excel文件
        workbook = xlsxwriter.Workbook(folder_name + r"/%s.xlsx" % table_name)
        worksheet = workbook.add_worksheet()

        # 从list中写入数据
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                worksheet.write(row_num, col_num, col_data)

        workbook.close()
        return 1

    except:
        return 0

# 复制数据库到新的数据库
def CopySql():
    try:
        # 判断文件夹是否存在，如果不存在则创建一个
        folder_path = AllQss.save_folder_path
        if not os.path.exists(folder_path):
            # 如果文件夹不存在，创建文件夹
            os.makedirs(folder_path)

        # 计算文件夹下有几个文件
        file_count = len([name for name in os.listdir(folder_path)])
        # 如果超过最大个数，就删掉一个
        if file_count >= int(AllQss.maximum_number_saves):
            # 列出文件夹中所有的.db文件
            db_files = [f for f in os.listdir(folder_path) if f.endswith('.db')]
            # 找到最早创建的文件
            oldest_file = min(db_files, key=lambda f: os.path.getctime(os.path.join(folder_path, f)))
            # 删除最早创建的文件
            os.remove(os.path.join(folder_path, oldest_file))

        source_file = 'data/test.db'  # 源db文件路径
        destination_file = "HistoricalData/historicalData_%s.db" % (GetAllTime())  # 目标db文件路径

        copyfile(source_file, destination_file)
        return 1
    except:
        return 0



if __name__ == "__main__":
    # 根目录需要具备的东西
    # 主题：写表名
    # 创建时间：写创建时间
    # 备注：写一些备注

    # 类型：分为文字和图片
    # 密码：直接存放密码（加密）
    # 插入类型：Back/Top
    # s = "CREATE TABLE %s" % ("根目录")
    # s = s + "(" + " TEXT,".join(["表名", "创建时间", "备注", "仓库类型", "密码", "加载方式"]) + " TEXT);"
    # cur.execute(s)
    #
    conn = sqlite3.connect('data/test.db')
    cur = conn.cursor()
    # CreateTable(cur, ["一个表", GetTime(), "备注", "TEXT", "密码", "Back"], ["主题", "图片", "账号名", "使用账号", "密码", "备注", "创建时间"])
    # for _ in range(5):
    #     InsertSql(cur, "一个表", ["我得欸经", "", "小布同学", "1231346", "dcada", "", GetTime()])
    #
    # print(SqlToStr(cur, "根目录"))
    DeleteSql(conn, cur)
    print(GetAllTableName(cur))
    cur.close()    # 关闭
    conn.close()   # 关闭

    print(CopySql())
