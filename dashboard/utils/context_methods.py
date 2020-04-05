""" Helper methods for setting and modifying context in views """

def context_assign_user(user):
    """ Create dict object assign current user and return """
    context = dict()
    context['current_user'] = user.profile
    return context
