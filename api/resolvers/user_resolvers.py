from ariadne import ObjectType

user = ObjectType("User")


@user.field("products")
def resolve_products(obj, info):
    return obj.products
