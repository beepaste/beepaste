from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='about', renderer='templates/about.jinja2')
def aboutus(request):
    title = 'about us' + " - " + request.registry.settings['beepaste.siteName']
    return {'title': title}
