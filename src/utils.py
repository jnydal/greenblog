from models import PageModel

def validateLoginModel(loginDataModel):
    
    if ((loginDataModel.id == "nifrostadmin") & (loginDataModel.password == "builtInPw")):
        return "true"
    else:
        return "false"

def menuLinks():
    
    MenuLink_query = PageModel.all()
    menulinks = MenuLink_query.fetch(10);
    return menulinks

def authenticatedUser(session):
    
    if session.has_key("LOGIN_DATA"):
        user = session['LOGIN_DATA']
        return user
    else:
        return 0