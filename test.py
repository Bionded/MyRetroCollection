from tinydb import TinyDB, Query


db = TinyDB('db.json')
#db.insert({'type': 'apple', 'count': 7})
#db.insert({'type': 'peach', 'count': 3})
#db.insert({'type': 'melon', 'count': 4})
#db.insert({'type': 'Melon', 'count': 5})


def search_test(value, field):
    value = value.lower().replace(' ', '')
    field = field.lower().replace(' ', '')
    return field in value
# Query
Fruit = Query()
test = db.search(Fruit.type.test(search_test, 'pplE'))
print(db.search(Fruit.type == 'melon'))
print(db.search(Fruit.type == 'Melon'))
print(db.search(Fruit.type == 'Melon' or Fruit.type == 'melon'))
print(db.search((Fruit.type == 'Melon') | (Fruit.type == 'melon')))
print(db.search(Fruit.type == 'apple'))