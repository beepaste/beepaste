from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


my_session_factory = SignedCookieSessionFactory('itsaseekreet')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('pyramid_mailer')
    config.set_session_factory(my_session_factory)
    config.scan()
    return config.make_wsgi_app()
