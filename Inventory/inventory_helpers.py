def check_item_name(item_name, lst_item):
    print(lst_item)
    for item in lst_item:
        if item == item_name:
            return False
    return True