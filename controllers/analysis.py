def analysis():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    task_id='analysisM'
    access_permission=check_role(task_id)
    if (access_permission==False ):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
    
    response.title='Analysis'

    reqPage = len(request.args)

    # --------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)

    #-----
    db.sm_search_date.from_dt.requires=IS_DATE(format=T('%d-%m-%Y'))
    db.sm_search_date.to_dt.requires=IS_DATE(format=T('%d-%m-%Y'))
    search_form =SQLFORM(db.sm_search_date)

    #--------------------------------------patient
    btn_agency_report=request.vars.btn_agency_report
    posmCode = request.vars.posmCode
    cm_compliance = request.vars.cm_compliance
    exe_discrepancy = request.vars.exe_discrepancy
    exe_discrepancy_download = request.vars.exe_discrepancy_download

    townCode = request.vars.townCode

    posmCodeAgency = request.vars.posmCodeAgency
    agencyCode = request.vars.agencyCode
    territory_Name = request.vars.territory_Name
    townCode_Name = request.vars.townCode_Name
    # return townCode_Name
    # return agencyCode
    userCheck = db(db.sm_user.user_id==session.user_id).select(db.sm_user.user_role,db.sm_user.agency_code,db.sm_user.agency_name)
    # if userCheck:
    #     user_role = str(userCheck[0].user_role)
    if (btn_agency_report):

        fromDt = request.vars.from_dt
        toDt = request.vars.to_dt

        dateFlag = True
        try:
            from_dt = str(datetime.datetime.strptime(str(fromDt), '%Y-%m-%d'))[0:10]
            to_dt = str(datetime.datetime.strptime(str(toDt), '%Y-%m-%d'))[0:10]
        except:
            dateFlag = False

        if dateFlag == False or agencyCode =="" or agencyCode ==None  or posmCodeAgency=="" or posmCodeAgency ==None or territory_Name=="" or territory_Name==None:
            response.flash = "Required POSM Code Agency Territory and Date rage"
        elif dateFlag == False:
            response.flash = "Invalid Date"
        else:
            redirect (URL('analysis','agency_report',vars=dict(townCode_Name=townCode_Name,fromDate=from_dt,toDate=to_dt,posmCodeAgency=posmCodeAgency,agencyCode=agencyCode,territoryName=territory_Name)))

    if cm_compliance:
        fromDt = request.vars.from_dt
        toDt = request.vars.to_dt

        if posmCode == None or posmCode=='':
            response.flash = "Required POSM Code"
        else:
            redirect (URL('reports','cmComplianceReport',vars=dict(posmCode=posmCode,fromDate=fromDt,toDate=toDt)))

    if exe_discrepancy:
        if posmCode == None or posmCode == '':
            response.flash = "Required POSM Code"
        else:
            redirect(URL('execution_discrepancy', 'execution_discrepancy_rec', vars=dict(posmCode=posmCode)))
    if exe_discrepancy_download:
        if posmCode == None or posmCode == '':
            response.flash = "Required POSM Code"
        else:
            redirect(URL('execution_discrepancy', 'execution_discrepancy_rec_Download', vars=dict(posmCode=posmCode)))

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    qset = db()
    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code == session.town_code)

    qset = qset(db.alc.id == db.alc_detail.alc_id)
    qset = qset(db.alc.due_date < current_date)
    qset = qset(db.alc_detail.r_qty == 0)
    qset = qset(db.alc_detail.penalty_flag == 0)
    record2 = qset.select(db.alc_detail.town_code.count(), db.alc_detail.town_code, db.alc_detail.town_name, db.alc.ALL,groupby=db.alc_detail.posm_code, orderby=~db.alc.due_date)
    # recCM = db((db.sm_rep.rep_type=='CM')&(db.sm_rep.status=='ACTIVE')).select(db.sm_rep.rep_id,db.sm_rep.rep_name, groupby=db.sm_rep.rep_id)
    # return recCM
    # recRegion = db(db.sm_town.region != 'ZREGION').select(db.sm_town.region, groupby=db.sm_town.region,orderby=db.sm_town.region)
    # return record2


    # cmComRecords = "SELECT cm_id,town_code,posm_code,posm_type,brand,sum(target_qty) as target_qty,sum(a_qty) as a_qty from ((SELECT cm_id as cm_id,town_code,posm_code,posm_type,brand,target_qty,0 as a_qty FROM cm_target WHERE cm_id!='') union (SELECT rep_id as cm_id,town_code,posm_code,posm_type,brand,0 as target_qty,a_qty FROM usages)) p group by cm_id,town_code,posm_code,posm_type,brand"
    recordList ='' #db.executesql(cmComRecords, as_dict=True)

    return dict(userCheck=userCheck,search_form=search_form, record2=record2,page=page)

def townNameList():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    resStr=''

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    qset = db()

    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.sm_town.town_code.belongs(townList))
            else:
                qset = qset(db.sm_town.town_code == session.town_code)

    recOutlet=db().select(db.sm_town.town_name,db.sm_town.town_code)
    for row in recOutlet:
        town_name = str(row.town_name)
        town_code = str(row.town_code)

        if resStr == '':
            resStr = town_code + '|' + town_name
        else:
            resStr += ',' + town_code + '|' + town_name
    return resStr

def agency_report():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    task_id = 'agency_reportM'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied'
        redirect(URL('default', 'home'))

    response.title = 'Agency Report'

    fromDate = request.vars.fromDate
    toDate = request.vars.toDate
    startDt = datetime.datetime.strptime(str(fromDate), '%Y-%m-%d')
    endDate = datetime.datetime.strptime(str(toDate), '%Y-%m-%d')
    endDt = endDate + datetime.timedelta(days=1)
    if str(startDt) > str(endDate):
        # return 'asd'
        session.flash = 'Invalid Date'
        redirect(URL('analysis', 'analysis'))
    # agencytowncode = request.vars.agencytowncode
    posmCodeAgency = request.vars.posmCodeAgency
    agencyCode = request.vars.agencyCode
    territoryName = request.vars.territoryName
    receivedTownCodeName = request.vars.townCode_Name.upper()

    if receivedTownCodeName == None:
        receivedTownCodeName = ''
    receivedTown = ""
    if (receivedTownCodeName != ''):
        receivedTownList = str(receivedTownCodeName).split('|')

        if len(receivedTownList) > 1:
            receivedTown = receivedTownList[0]
        else:
            receivedTown= receivedTownCodeName


    # if posmCodeAgency =='' or agencyCode =="" or fromDate == '' or toDate == '':
    #     session.flash = 'Required POSM Code Agency Code and Date rage'
    #     redirect(URL('analysis', 'analysis'))

    if fromDate != '' and toDate != '':

        from_dtDate = str(datetime.datetime.strptime(str(fromDate), '%Y-%m-%d'))[0:10]

        to_dtate = datetime.datetime.strptime(str(toDate), '%Y-%m-%d') + datetime.timedelta(days=1)

        DateRange = datetime.datetime.strptime(from_dtDate, '%Y-%m-%d') + datetime.timedelta(days=93)
        # return DateRange
        if to_dtate > DateRange:
            # return 'asd'
            session.flash = 'Date Range Max 3 Months'
            redirect(URL('analysis', 'analysis'))



    if agencyCode != '':
        townlistS = agencyCode
        townlist = agencyCode.split('|')
        if len(townlist) > 1:
            agencyCode = townlist[0]
        else:
            agencyCode = townlistS


    #
    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    qset = db()

    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.agency_usage.town_code.belongs(townList))
            else:
                qset = qset(db.agency_usage.town_code == session.town_code)

    qset = qset((db.agency_usage.agency_date >= startDt) & (db.agency_usage.agency_date < endDt) &(db.agency_usage.agency_code==agencyCode)&(db.agency_usage.posm_code==posmCodeAgency))
    qset = qset((db.agency_usage.town_code==db.sm_town.town_code)&(db.sm_town.territory_name==territoryName))
    if receivedTown !='':
        qset = qset(db.agency_usage.town_code == receivedTown)
    records = qset.select(db.agency_usage.ALL, orderby=~db.agency_usage.id)

    if not records:
        session.flash = 'Record Not Found'
        redirect(URL('analysis', 'analysis'))

    region =""
    territory_name = ""
    town_name = ""
    agency_name= ""
    townRecords = db(db.agency.agency_code==agencyCode).select(db.agency.agency_name)
    for rec in townRecords:
        agency_name = str(rec.agency_name)
    #     territory_name = str(rec.territory_name)
    #     town_name = str(rec.town_name)

    return dict(receivedTownCodeName=receivedTownCodeName,agency_name=agency_name,records=records,fromDate=fromDate,toDate=toDate,posmCode=posmCodeAgency,agencyCode=agencyCode,region=region,territory_name=territory_name,town_name=town_name,territory_Name=territoryName)


