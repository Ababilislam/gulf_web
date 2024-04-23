#Name of functions

import urllib.parse
from gluon.tools import fetch


def index(): 
    # response.title="GULF-OIL-BANGLADESH"
    session.clear()
    return dict()

# def webUserCheck():
#     session.flash = 'Unauthorized User Please Reset Your Password'
#     redirect(URL('index'))

def check_user():
    # response.title="GULF-OIL-BANGLADESH"
    cid = str(request.vars.cid).strip().upper()
    # return cid
    uid = str(request.vars.uid).strip().upper()
    password = str(request.vars.password).strip()

    # if cid,userid,pass blank
    if (cid == '' or uid == '' or password == ''):
        session.flash = 'User ID and Password required !'
        redirect(URL('index'))

        # =================== user
    userRows = db((db.sm_user.cid == cid) & (db.sm_user.user_id == uid) & (db.sm_user.password == password) & (db.sm_user.status == 'ACTIVE')).select(db.sm_user.ALL, limitby=(0, 1))
    # return db._lastsql
    if not userRows:
        session.flash = 'Unauthorized User'
        redirect(URL('index'))
    else:
        cid = cid
        user_id = uid
        user_type = userRows[0].user_type
        user_name = userRows[0].user_name
        user_role = userRows[0].user_role
        status = userRows[0].status

        sysItemPerPageRows = db(db.sm_settings.cid == cid).select(db.sm_settings.s_key,db.sm_settings.s_value)

        for records in sysItemPerPageRows:
            s_key = records.s_key
            value = records.s_value
            if (s_key == 'ITEM_PER_PAGE'):
                itemPerPage = int(value)
                session.items_per_page = itemPerPage
                break
        if (session.items_per_page == None):
            session.flash = 'Need settings data for item per page!'
            redirect(URL('index'))

        else:
            roleRows = db((db.sm_roletask.cid == cid) & (db.sm_roletask.roleid == user_role)).select(db.sm_roletask.taskid)

            my_task = ''
            if not roleRows:
                session.flash = 'Required login permission !'
                redirect(URL('index'))
            else:
                for roleRow in roleRows:
                    taskid = str(roleRow.taskid).strip()
                    if my_task == '':
                        my_task = taskid
                    else:
                        my_task = my_task + ',' + taskid

                session.cid = cid
                session.user_id = user_id
                session.user_type = user_type
                session.user_role = user_role
                session.user_name = user_name
                session.task_listStr = my_task


                # tbl_insert_log = db.waid_userlog.insert(cid=session.cid, userid=session.user_id,lastlogintime=datetime_fixed)

                redirect(URL('home'))
    return dict()




def home():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title="GULF-OIL-BANGLADESH"
    # if (session.user_id=='' or session.user_id==None):
    #     redirect(URL('index'))
    syncCode = 0
    syncCodeCheck = db(db.sm_user.user_id == session.user_id).select(db.sm_user.sync_code, limitby=(0, 1))
    if syncCodeCheck:
        syncCode = syncCodeCheck[0][db.sm_user.sync_code]

    # if (session.sync_codeCheck != syncCode):
    #     session.flash = 'Unauthorized User Please Reset Your Password'
    #     redirect(URL('default', 'index'))

    

    return dict()

def logout():
    session.clear()
    return redirect (URL('default','index'))


