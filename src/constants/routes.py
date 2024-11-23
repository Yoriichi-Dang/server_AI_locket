
def get_public_routes():
    PUBLIC_ROUTES=['/login','/register','/']
    return PUBLIC_ROUTES
def get_private_routes():
    PRIVATE_ROUTES = ["/profile", "/profile/settings", "/admin"]
    return PRIVATE_ROUTES