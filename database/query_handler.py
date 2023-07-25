def generate_format_string(fields):
    result = ''
    for i in fields:
        result += f'%({i})s, '
    return result


def generate_columns(fields):
    columns = fields.copy()
    columns.append('created_at')
    return str(tuple(columns)).replace("'", '')


def generate_update_query(data) -> str:
    result = ''
    for column, value in data.items():
        result += f'"{column}" = {value}, '
    return result[:-2]