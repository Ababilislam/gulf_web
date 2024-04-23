def area_structure():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    return dict()