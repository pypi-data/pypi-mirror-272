import jinja2
from faker import Faker

faker = Faker()
faker_zh = Faker(locale='zh_CN')


def is_key(key, value_map={}):
    """精确匹配是否存在key

    Args:
        key (str): 字符串key
        value_map (dict, optional): 是否存在该key的字典. Defaults to {}.

    Returns:
        _type_: 最终的key，如果不存在则为None
    """
    newkey = key.lower()
    if newkey in value_map:
        return newkey
    return None


def is_fuzzy_key(key, value_map={}):
    """
    检查key或者key的复数形式在map中，并返回最终map中的key
    """
    newkey = key.lower()
    if newkey in value_map:
        return newkey
    if newkey.endswith('s'):
        newkey = newkey[:-1]
    else:
        newkey = newkey + 's'
    if newkey in value_map:
        return newkey
    return None


def parse_url_params(url_query):
    params = url_query.lstrip('?')  # 移除开头的问号
    pairs = params.split(',')  # 将参数对分割
    result = {}

    for pair in pairs:
        key, value = pair.split('=')  # 分割键和值
        result[key] = value  # 添加到结果字典
    return result


def template_render(template, **kwargs):
    temp = jinja2.Template(template)
    temp.globals.update({"faker": faker, "faker_zh": faker_zh})
    faker.phone_number()
    return temp.render(**kwargs)
