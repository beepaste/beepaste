def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
# TODO:
#       add og and twitter card tags to main template
    config.add_route('home', '/') # TODO: add csrf
    config.add_route('about', '/about')

    config.add_route('qrcode', '/qrcode/{uri}')
    config.add_route('view_raw', '/view/raw/{pasteID}')
    config.add_route('view_embed', '/view/embed/{pasteID}')
    config.add_route('view_paste', '/view/{pasteID}')

# TODO: add support for users so they can register and have their pastes saved! /user/list
#           route should be added. also users should be able to remove their pastes within
#           /user/list or the paste view itself!

    config.add_route('register', '/user/register') # register, forgotpassword, signin, signout
    config.add_route('forgot', '/user/forgot') # register, forgotpassword, signin, signout
    config.add_route('signin', '/user/signin') # register, forgotpassword, signin, signout
    config.add_route('signout', '/user/signout') # register, forgotpassword, signin, signout
    config.add_route('reset_password', '/user/reset/{resetToken}')

    config.add_route('schedeuled_remove', '/cron/{cronkey}')

    config.add_route('api_langs', '/api/langs') # returns supported langs in json
    config.add_route('api_intro', '/api/doc') # show how to use api html page
    config.add_route('api_get', '/api/{pasteid}') # api handle get
    config.add_route('api_post', '/api') # api handle post
