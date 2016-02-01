# -*- coding: utf-8 -*-

from gluon.custom_import import track_changes; track_changes(True)
from primos_circulares import PrimosCirculares
import time

def index():
    response.flash = STRONG('Bienvenido  ',I(_class='glyphicon glyphicon-thumbs-up'))
    pcList = []
    msg = ''
    form = SQLFORM.factory(
            Field('hasta','integer' ,requires=[IS_NOT_EMPTY(),IS_INT_IN_RANGE(1, 1000001)],default=1000000),
            _class='form-inline'
            )

    if form.process().accepted:
        numero_max = form.vars.hasta
        pc = PrimosCirculares()
        startTime = time.time()
        pcList = pc.buscar(int(numero_max))
        endTime = time.time()
        response.flash = ''
        if pc:
            msg = '%s números encontrados en %s segundos.' %(len(pcList), endTime - startTime)
        else:
            response.flash = 'Ocurrió un problema'

    elif form.errors:
        response.flash = 'Formulario erroneo'

    return dict(form = form,pc = pcList,msg= msg)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


