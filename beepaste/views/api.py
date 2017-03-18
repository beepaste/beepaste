from pyramid.response import Response
from pyramid.view import view_config
import beepaste.libs.pasteFunctions as func
from beepaste.libs.selectOptions import languagesList
from beepaste.models.api import API
import base64


def verifyKey(apikey, request):
    api_count = request.dbsession.query(API).filter_by(apikey=apikey).count()
    if api_count == 0:
        return {'error': 'api-key is not valid.'}


@view_config(
                route_name='api_intro',
                request_method='GET',
                renderer='templates/apiView.jinja2'
        )
def apiIntro(request):
    title = 'API' + " - " + request.registry.settings['beepaste.siteName']
    description = '''Here is the rest-ful api! With this api you can create or
                get pastes in beepaste! For more information on how to
                work with API and for samples please visit the link.'''
    return {'title': title, 'description': description}


@view_config(
        route_name='api_get',
        request_method='GET',
        renderer='json',
        )
def get_api(request):
    pasteid = request.matchdict['pasteid']
    paste = func.getPaste(pasteid, request)

    if paste:
        retData = {}
        retData['url'] = request.route_url(
                                            'view_paste',
                                            pasteID=paste.pasteURI)
        retData['pasteTitle'] = paste.title
        retData['pasteAuthor'] = paste.name
        retData['pasteLanguage'] = paste.lang
        retData['pasteRaw'] = base64.b64decode(paste.text).decode('utf-8')
        retData['pasteEncryption'] = paste.encryption
        retData['shortURL'] = paste.shortURL

        resp = Response()
        resp.status_int = 200
        resp.json = retData
        return resp
    else:
        return {'error': 'paste not found.'}


@view_config(
        route_name='api_post',
        request_method='POST',
        renderer='json',
        )
def post_api(request):
    try:
        data = request.json_body
    except:
        return {"error": "invalid request"}

    if data:
        apikey = func.fetchData(data, 'api-key')
        verifyKey(apikey, request)

        pasteRaw = func.fetchData(data, 'pasteRaw')
        data['pasteRaw'] = base64.b64encode(
                pasteRaw.encode('utf-8')).decode('utf-8')

        pasteLanguage = func.fetchData(data, 'pasteLanguage')
        func.verifyLanguage(pasteLanguage)

        pasteTitle = func.fetchData(data, 'pasteTitle', False)
        if pasteTitle:
            func.verifyTitleAndAuthor(pasteTitle)
        else:
            data['pasteTitle'] = pasteTitle

        pasteAuthor = func.fetchData(data, 'pasteAuthor', False)
        if pasteAuthor:
            func.verifyTitleAndAuthor(pasteAuthor)
        else:
            data['pasteAuthor'] = pasteAuthor

        pasteExpire = func.fetchData(data, 'pasteExpire', False)
        if pasteExpire:
            func.verifyExpire(pasteExpire)
        else:
            data['pasteExpire'] = "0"

        pasteEncryption = func.fetchData(data, 'pasteEncryption', False)
        if pasteEncryption:
            func.verifyEncryption(pasteEncryption)
        else:
            data['pasteEncryption'] = pasteEncryption

        newPasteURI = func.createPasteFromData(data, request)

        retData = {}
        retData['url'] = request.route_url('view_paste', pasteID=newPasteURI)

        resp = Response()
        resp.status_int = 201
        resp.json = retData
        return resp


@view_config(route_name='api_langs')
def apiLang(request):
    retData = {}
    retData['pasteLanguages'] = languagesList

    resp = Response()
    resp.status_int = 200
    resp.json = retData

    return resp
