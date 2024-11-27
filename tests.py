list = [1,2,3,4,'apple']


def push_new_value(list, value):
    list.append(value)
    print(f'This is the list values: {list}')

def search_value(value):
    ans = list.index(value)

    print(f"here is the value you looked for: {ans}")


push_new_value(list, 6)
search_value(6)