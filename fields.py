import geok

# x = geok.core.Field(name="foo", alias="foo")
# print(x.__fields__.values())

y = geok.core.UniqueIdField()
print(y.aliased_dict())
print("\n")
print(y.aliased_json())
print("\n")
print(y.aliased_fields())
