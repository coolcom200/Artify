from ariadne import QueryType
from ariadne import convert_kwargs_to_snake_case
from flask import g

from api.resolvers import login_required

query = QueryType()


@query.field("search")
@convert_kwargs_to_snake_case
def resolve_search(_, info, search_query=None, min_price=None, max_price=None):
    database = info.context["database"]
    result = database.get_products(search_query, min_price, max_price)
    return result


@query.field("me")
@login_required
def resolve_me(_, info):
    if "user" not in g or g.user is None:
        return None
    else:
        return g.user
