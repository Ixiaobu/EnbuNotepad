from AlertWindow import AlertWindow
import SQLopt
from ReadIni import AllQss

# 检查用户新建表单时的输入
def CheckCreateTable(dad, cur, table_info, name_list):
    name = table_info[0]
    remark = table_info[2]
    password = table_info[4]
    if name in [AllQss.text1, ""] + SQLopt.GetAllTableName(cur):
        AlertWindow(dad, "😧", "<%s> 已存在, 换一个名字吧~" % name).show()
        return False
    if not remark:
        AlertWindow(dad, "😧", "这个主题还没有描述呢，写一点吧").show()
        return False
    if "" in name_list:
        AlertWindow(dad, "😧", "检测到有未命名的标签，请删除不必要的空白项").show()
        return False
    if len(set(name_list)) != len(name_list):
        AlertWindow(dad, "😧", "这里的标签不能重复哦，换个其他名字吧").show()
        return False
    if not password:
        AlertWindow(dad, "😘", "您没有设置密码，如需设置右键主题名称即可设置").show()
        return True

    return True

def CheckEditTable(dad, cur, table_name_old, table_info, name_list):
    name = table_info[0]
    remark = table_info[2]
    password = table_info[4]
    if name in [AllQss.text1, ""] + SQLopt.GetAllTableName(cur) and table_name_old != name:
        AlertWindow(dad, "😧", "<%s> 已存在, 换一个名字吧~" % name).show()
        return False
    if not remark:
        AlertWindow(dad, "😧", "这个主题还没有描述呢，写一点吧").show()
        return False
    if "" in name_list:
        AlertWindow(dad, "😧", "检测到有未命名的标签，请删除不必要的空白项").show()
        return False
    if len(set(name_list)) != len(name_list):
        AlertWindow(dad, "😧", "这里的标签不能重复哦，换个其他名字吧").show()
        return False
    return True

# 检查用户天机数据时是否合格
def CheckAddInfo(dad, data):
    if not data[0]:
        AlertWindow(dad, "🤭", "信息的标题不可以是空白哦").show()
        return False
    return True