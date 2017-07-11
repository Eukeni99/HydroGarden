from datetime import date, time


def resolve_data(value):
    if isinstance(value, date):
        return '{:%d-%m-%y}'.format(value)
    if isinstance(value, time):
        return value.strftime('%X')
    if isinstance(value, bool) and value == 1:
        return 1
    if isinstance(value, bool) and value == 0:
        return 0
    if value is None:
        return ''
    return value


def search_sensor(field_name, array):
    for item in array:
        if item.sensor_field == field_name:
            return item
    else:
        return None
