from pyshorteners import Shortener
from beepaste.models.pastes import Pastes
import string
from random import *
import datetime
from wtforms import Form, TextField, SelectField, validators, RadioField
from beepaste.selectOptions import languagesList, encryptionMethods, expireTimes
from wtforms.ext.csrf.form import SecureForm


class CSRFException(Exception):
    pass


class BaseForm(SecureForm):
    def __init__(self, formdata=None, obj=None, prefix='', csrf_context=None,
                 **kwargs):
        super(BaseForm, self).__init__(formdata=formdata, obj=obj,
                                          prefix=prefix,
                                          csrf_context=csrf_context, **kwargs)
        self._csrf_context = csrf_context

    def generate_csrf_token(self, csrf_context):
        return csrf_context.session.get_csrf_token()

    def validate_csrf_token(self, field):
        if field.data != field.current_token:
            raise CSRFException('Invalid CSRF token')


class createPasteForm(BaseForm):
    pasteTitle = TextField('Title', [validators.Length(min=0, max=255)])
    pasteAuthor = TextField('Author', [validators.Length(min=0, max=255)])
    pasteLanguage = SelectField('Syntax Highlighting', choices=languagesList, default='text', validators=[validators.Required()])
    pasteExpire = SelectField('Expire On', choices=expireTimes, validators=[validators.Required()])
    pasteRaw = TextField('Raw Text', [validators.Required()])
    pasteEncryption = RadioField('Paste Encryption', choices=encryptionMethods)

def pasteExists(uri, request):
    old_uris_count = request.dbsession.query(Pastes).filter_by(pasteURI=uri).count()
    if old_uris_count > 0:
        return True
    return False

def generateURI(len):
    allchar = string.ascii_letters + string.digits
    uri = "".join(choice(allchar) for x in range(len))
    return uri

def generateShortURL(url, request):
    access_token = request.registry.settings['beepaste.bitlyToken']
    shortener = Shortener('Bitly', bitly_token=access_token)
    return shortener.short(url)

def fetchData(data, key, required=True):
    try:
        ret = data[key]
        return ret
    except:
        if required:
            raise Exception(key + ' not found.')
        else:
            return ""

def verifyExpire(exp):
    try:
        tmp = int(exp)
        datetime.timedelta(seconds=int(form.pasteExpire.data))
    except:
        raise Exception('invalid pasteExpire')

def verifyLanguage(lang):
    try:
        count = len([v for i, v in enumerate(languagesList) if v[0] == lang])
        if count == 0:
            raise Exception('invalid pasteLanguage.')
    except:
        raise Exception('invalid pasteLanguage.')

def verifyEncryption(enc):
    try:
        count = len([v for i, v in enumerate(encryptionMethods) if v[0] == enc])
        if count == 0:
            raise Exception('invalid pasteEncryption.')
    except:
        raise Exception('invalid pasteEncryption.')

def verifyTitleAndAuthor(txt):
    if len(txt) > 255:
        raise Exception('invalid length for pasteTitle or pasteAuthor')

def createPaste(form, request):
    newPaste = Pastes()
    URI = generateURI(6)
    while pasteExists(URI, request):
        URI = generateURI(6)
    newPaste.pasteURI = URI
    if form.pasteTitle.data:
        newPaste.title = form.pasteTitle.data
    if form.pasteAuthor.data:
        newPaste.name = form.pasteAuthor.data
    newPaste.lang = form.pasteLanguage.data
    newPaste.text = form.pasteRaw.data
    if form.pasteExpire.data != "0":
        newPaste.toexpire = True
        newPaste.expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(form.pasteExpire.data))
    newPaste.encryption = form.pasteEncryption.data
    newPaste.shortURL = generateShortURL(request.route_url('view_paste', pasteID=URI), request)
    request.dbsession.add(newPaste)
    return URI

def createPasteFromData(data, request):
    newPaste = Pastes()
    URI = generateURI(6)
    while pasteExists(URI, request):
        URI = generateURI(6)
    newPaste.pasteURI = URI
    if data['pasteTitle']:
        newPaste.title = data['pasteTitle']
    if data['pasteAuthor']:
        newPaste.name = data['pasteAuthor']
    newPaste.lang = data['pasteLanguage']
    newPaste.text = data['pasteRaw']
    if data['pasteExpire'] != "0":
        newPaste.toexpire = True
        newPaste.expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(data['pasteExpire']))
    newPaste.encryption = data['pasteEncryption']
    newPaste.shortURL = generateShortURL(request.route_url('view_paste', pasteID=URI), request)
    request.dbsession.add(newPaste)
    return URI

def getPaste(pasteID, request):
    paste = request.dbsession.query(Pastes).filter_by(pasteURI=pasteID).first()
    return paste
