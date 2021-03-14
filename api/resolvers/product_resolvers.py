from ariadne import ObjectType

product = ObjectType("Product")


@product.field("images")
def resolve_files(obj, info):
    return obj.images


@product.field("owner")
def resolve_owner(obj, info):
    return obj.owner
