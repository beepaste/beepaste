from pyramid.response import Response
from pyramid.view import view_config
from beepaste.pasteFunctions import *

from pyramid.httpexceptions import (
    HTTPFound
)

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    form = createPasteForm(request.POST, csrf_context=request)
    if request.method == 'POST' and form.validate():
        URI = createPaste(form, request)
        return HTTPFound(location=request.route_url('view_paste', pasteID=URI))
    return {'form': form, 'title': request.registry.settings['beepaste.siteName']}
