def get_item_by_idx(DICT, idx):
    for key, value in DICT.items():
        if value['idx'] == idx:
            return value
    return None