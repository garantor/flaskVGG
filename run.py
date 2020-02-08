import json
from index import Users


ac = Users.query.all()
print(ac)

for a in ac:
    print(ac)

# import json
# my_list = [ 'a', 'b', 'c]
# my_json_string = json.dumps(my_list)
# print(my_json_string)
# # ad = ac
# print(json.dumps(ad))

# data = {'afolabi': 10000}

# json_str = json.dumps(data, indent=4)
# print(json_str)