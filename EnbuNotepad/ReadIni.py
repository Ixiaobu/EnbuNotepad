from configparser import ConfigParser
import chardet

# 可以把字典键值对转换为一个类
class Config():
    def __init__(self, **input):
        self.__dict__.update(input)

# 按照对应格式读取配置文件
def read_config_file(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']
    with open(file_path, 'r', encoding=encoding) as f:
        conf = ConfigParser()
        conf.read_file(f)
    return conf


conf = read_config_file('data/config.ini')
AllQss   = Config(**conf["AllQss"])
AllQss.font_size = int(AllQss.font_size)
AllQss.img_max_w = int(AllQss.img_max_w)

DayQss   = Config(**conf["DayQss"])
NightQss = Config(**conf["NightQss"])
AllText  = Config(**conf["AllText"])