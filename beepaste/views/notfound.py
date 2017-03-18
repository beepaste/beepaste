from pyramid.view import notfound_view_config


@notfound_view_config(renderer='templates/404.jinja2')
def notfound_view(request):
    request.response.status = 404
    title = '404: page not found' + " - " + request.registry.settings['beepaste.siteName']
    return {'title': title, 'description': '404: Page Not Found, please try again!'}
