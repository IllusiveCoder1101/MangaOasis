from main import tables,cache

@cache.memoize(50)
def get_all_books():
    q=tables.Books.query.filter().all()
    return q

@cache.memoize(50)
def get_all_users():
    q=tables.Users.query.filter().all()
    return q