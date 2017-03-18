from pyramid.response import Response
from pyramid.view import view_config
from beepaste.models.pastes import Pastes
from beepaste.pasteFunctions import pasteExists
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
import base64

@view_config(route_name='view_raw', renderer='templates/pasteRaw.jinja2')
def viewRaw(request):
    uri = request.matchdict['pasteID']
    if not pasteExists(uri, request):
        raise HTTPNotFound()
    paste = request.dbsession.query(Pastes).filter_by(pasteURI=uri).first()
    raw = base64.b64decode(paste.text.encode('utf-8')).decode('utf-8')
    request.response.content_type = "text/plain; charset=UTF-8"
    return {'raw': raw}

@view_config(route_name='view_embed', renderer='templates/pasteEmbed.jinja2')
def viewEmbed(request):
    uri = request.matchdict['pasteID']
    if not pasteExists(uri, request):
        raise HTTPNotFound()
    paste = request.dbsession.query(Pastes).filter_by(pasteURI=uri).first()
    title = paste.title + " - " + request.registry.settings['beepaste.siteName']
    return {'paste': paste, 'title': title}

@view_config(route_name='view_paste', renderer='templates/pasteView.jinja2')
def viewPaste(request):
    uri = request.matchdict['pasteID']
    if not pasteExists(uri, request):
        raise HTTPNotFound()
    paste = request.dbsession.query(Pastes).filter_by(pasteURI=uri).first()
    embedCode = '<iframe src="' + request.route_url('view_embed', pasteID=paste.pasteURI) +'" style="border:none;width:100%;min-height:300px;"></iframe>'
    title = paste.title + " - " + request.registry.settings['beepaste.siteName']
    description = "Paste by "+ paste.name + ", Created about " + paste.created_in_words() + " ago. View more information in link!"
    return {'paste': paste, 'embedCode': embedCode, 'title': title, 'description': description}
