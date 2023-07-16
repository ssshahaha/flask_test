from crud import crud_device


def statistics_data_fill(data):
    data_nos = [_[0] for _ in data]
    for _ in crud_device.get_all_name_no():
        if _[0] not in data_nos:
            _info = (_[0], _[1], 0)
            data.append(_info)
    return data
