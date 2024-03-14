import winreg
import datetime
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

# 根据输入检测系统是否处于深色模式
def GetTheme(text):
    if text == "Auto":
        # 检查系统是否启用了黑暗主题
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            if value:
                return "Day"
            return "Night"  # 如果为 0 则表示启用了深色主题
        except FileNotFoundError:
            return "Night"  # 注册表项不存在，可能意味着系统不是 Windows 10 或者深色模式未启用
    return text

# 将当前的时间转为字符并输出
def GetTime():
    y = datetime.datetime.now().year
    m = datetime.datetime.now().month
    d = datetime.datetime.now().day
    return "%d-%.2d-%.2d" % (y, m, d)

# 将当前的时间转为字符并输出
def GetAllTime():
    y = datetime.datetime.now().year
    m = datetime.datetime.now().month
    d = datetime.datetime.now().day
    h = datetime.datetime.now().hour
    m_ = datetime.datetime.now().minute
    s = datetime.datetime.now().second
    return "%d-%.2d-%.2d-%.2d-%.2d-%.2d" % (y, m, d, h, m_, s)

# 检测一个图片是否存在
def IsGoodImg(path):
    try:
        with Image.open(path) as img:
            return True
    except:
        return False

# 清空一个布局的所有内容
def RemoveLayoutItem(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
        else:
            layout.removeItem(item)

# 把一个长方形图片变成一个正方形图片(居中)
def RectangularToSquare(img):
    # 先把图片弄小一点
    # w_max = int(AllQss.img_max_w)
    # size = img.shape
    # w, h = size[0], size[1]
    # img = cv2.resize(img, (int(h / w * w_max), w_max))

    size = img.size
    w, h = size[0], size[1]
    w2 = min(w, h)
    x1, x2 = (w - w2) // 2, (w - w2) // 2 + w2
    y1, y2 = (h - w2) // 2, (h - w2) // 2 + w2
    # return img[x1:x2:1, y1:y2:1]
    return img.crop((x1, y1, x2, y2))

# 得到正方形且格式正确的图片
def GetImg(path, Square=True):
    # img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
    # img = RectangularToSquare(img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # height, width, channel = img.shape
    # bytesPerLine = 3 * width
    # qImg = QImage(img[:], width, height, bytesPerLine, QImage.Format_RGB888)
    # return QPixmap.fromImage(qImg)
    with Image.open(path) as img:
        if Square:
            img = RectangularToSquare(img)
        img = img.convert('RGB')
        width, height = img.size
        bytesPerLine = 3 * width
        img_data = img.tobytes()
        qImg = QImage(img_data, width, height, bytesPerLine, QImage.Format_RGB888)
        return QPixmap.fromImage(qImg)


# 把一个文字约束到几个字以内
def LimitStrLen(s, l):
    if len(s) <= l:
        return s
    return s[:l-1] + "..."

# 返回两个信息不同的地方，文字格式
def ShowDifferent(name, text1, text2):
    ans = [""]
    for a, b, c in zip(name, text1, text2):
        if b != c:
            ans.append("%s: %s -> %s\n" % (a, b, c))
    return ''.join(ans)

# 返回更改的主题的详细信息
def GetDetailedInformation(table_data_old, table_name_old, table_data_new, table_name_new, rename_name):

    # 表单数据改变
    data_change = ShowDifferent(["主题", "创建时间", "备注", "主题类型", "密码", "加载方式"], table_data_old, table_data_new)

    # 获取被删除掉的列
    new_name = set(table_name_new) | set(a for a, b in rename_name)
    del_text = []
    for name in table_name_old:
        if name not in new_name:
            del_text.append(name)
    del_text = ", ".join(del_text)

    # 获取被删除掉的列
    add_text = []
    new_name = set(table_name_old) | set(b for a, b in rename_name)
    for name in table_name_new:
        if name not in new_name:
            add_text.append(name)
    add_text = ", ".join(add_text)

    rename_text = ''.join("%s -> %s\n" % (old, new) for old, new in rename_name)

    ans = []
    if data_change:
        ans.append("<主题格式改变>\n" + data_change)
    if del_text:
        ans.append("\n<这些标签被删除>\n" + del_text)
    if add_text:
        ans.append("\n<新添加了这些标签>\n" + add_text)
    if rename_text:
        ans.append("\n<这些标签被改名>\n" + rename_text)
    print(ans)
    return "\n".join(ans)


if __name__ == "__main__":
    table_data_old = []
    table_name_old = ["1", "2", "3", "4"]
    table_data_new = []
    table_name_new = ["1", "4", "7", "8"]
    rename_name = [["2", "8"]]
    GetDetailedInformation(table_data_old, table_name_old, table_data_new, table_name_new, rename_name)