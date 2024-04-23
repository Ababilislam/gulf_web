#Name of functions

import urllib.parse
from gluon.tools import fetch


def index(): 
    session.clear()
    return dict()

# def webUserCheck():
#     session.flash = 'Unauthorized User Please Reset Your Password'
#     redirect(URL('index'))

def check_user():
    cid = str(request.vars.cid).strip().upper()
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
    # if (session.user_id=='' or session.user_id==None):
    #     redirect(URL('index'))
    syncCode = 0
    syncCodeCheck = db(db.sm_user.user_id == session.user_id).select(db.sm_user.sync_code, limitby=(0, 1))
    if syncCodeCheck:
        syncCode = syncCodeCheck[0][db.sm_user.sync_code]

    # if (session.sync_codeCheck != syncCode):
    #     session.flash = 'Unauthorized User Please Reset Your Password'
    #     redirect(URL('default', 'index'))

    response.title="LAFARGE- TLP"

    return dict()

def sub_months(sourcedate, months):
    month = sourcedate.month - 2 - months
    year = sourcedate.year + int(month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

def dashboard_new():
    if (session.user_id=='' or session.user_id==None):
        redirect(URL('index'))
    syncCode = 0
    syncCodeCheck = db(db.sm_user.user_id == session.user_id).select(db.sm_user.sync_code, limitby=(0, 1))
    if syncCodeCheck:
        syncCode = syncCodeCheck[0][db.sm_user.sync_code]

    if (session.sync_codeCheck != syncCode):
        session.flash = 'Unauthorized User Please Reset Your Password'
        redirect(URL('default', 'index'))

    response.title="Hawk's Eye"
    curent_month = str(current_date)[:7] + '-' + '01'

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])
    townListRsql=str(townList).replace('[','').replace(']','')

    psDataRec=''
    attList=[]

    qset10 = db()
    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset10 = qset10(db.sm_rep.base_town.belongs(townList))
            else:
                qset10 = qset10(db.sm_rep.base_town == session.town_code)

    totalCMSup = qset10((db.sm_rep.rep_type == 'CM')& (db.sm_rep.status == 'ACTIVE') & ((~db.sm_rep.rep_id.contains('Z99'))&(~db.sm_rep.rep_id.contains('T99')))).count()

    # qset11 = db()
    # if session.town_code != '':
    #     if session.town_code != 'ALL':
    #         if len(town_code) > 1:
    #             qset11 = qset11(db.sm_attendance.base_town.belongs(townList))
    #         else:
    #             qset11 = qset11(db.sm_attendance.base_town == session.town_code)
    #
    # cmAttenData = qset11((db.sm_attendance.rep_type == 'CM')&(db.sm_attendance.day_attendance == current_date)& ((~db.sm_attendance.rep_id.contains('Z99'))&(~db.sm_attendance.rep_id.contains('T99')))).count()
    # # return db._lastsql
    # attPercent=cmAttenData*100/totalCMSup

    dateMOCcom = ''
    lastMocComp = db().select(db.z_result.MOC_ID)
    for rowM in lastMocComp:
        dateMOCcom = rowM.MOC_ID

    lastMOCAuditFromDate = ''
    lastMOCAuditToDate = ''

    mocRows = db(db.sm_settings.s_key == 'MOC').select(db.sm_settings.s_value)
    for mocRow in mocRows:
        mocDate = mocRow.s_value.split(',')
        lastMOCAuditFromDate = mocDate[1]
        lastMOCAuditToDate = mocDate[2]
        # dateMOCcom = mocDate[1].replace('-', '')[0:6] + '01'
        if current_date >= lastMOCAuditFromDate and current_date <= lastMOCAuditToDate:

            recordList=[]
            recordList1 = []
            recordListCmUsages=[]
            recordListAgencyUsages=[]
            recordListCom=[]
            # regRec = db(db.sm_town.region != 'ZREGION').select(db.sm_town.region, groupby=db.sm_town.region)
            # for row in regRec:
            #     region = row.region
            #     # psCount = db((db.outlet.region == region)&(db.outlet.ps_status == 1)).count()
            #
            # townList = []
            # recTown = db(db.sm_town.region == region).select(db.sm_town.town_code)
            # for rowTown in recTown:
            #     townList.append(rowTown.town_code)


            # cmRows =db(((db.sm_rep.rep_type == 'CM') | (db.sm_rep.rep_type == 'SUPERVISOR')) &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code.belongs(townList))).select(db.sm_rep.rep_id)
            # cmCount = len(cmRows)
            #
            # cmList= []
            # for cmRow in cmRows:
            #     cmList.append(cmRow[db.sm_rep.rep_id])
            # return townListRsql
            #====================
            # return len(town_code)
            if session.user_role=='TM':
                if session.town_code!='ALL':
                    if len(town_code)>1:
                        dateRecordsSrSch="select field1 as region,towncode as towncode,town_name as town_name, sum(ecoRate) as ecoRate, sum(strikeRate) as strikeRate from (select field1,towncode,town_name, 0 as ecoRate, sum(s_q)/sum(v_q)*100 as strikeRate from (SELECT field1,towncode,town_name, COUNT(visitsl) as v_q, 0 as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and towncode in ("+str(townListRsql)+") and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' GROUP BY towncode union SELECT field1,towncode,town_name, 0 as v_q, COUNT(visitsl) as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and towncode in ("+str(townListRsql)+") and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' AND visitsl>0 GROUP BY towncode) as z group by towncode union select field1,towncode,town_name, sum(s_q)/sum(v_q)*100 as ecoRate, 0 as strikeRate from (SELECT field1,towncode,town_name, COUNT(DISTINCT(outletcode)) as v_q,0 as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and towncode in ("+str(townListRsql)+") and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' GROUP BY towncode union SELECT field1,towncode,town_name, 0 as v_q,COUNT(DISTINCT(outletcode)) as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and towncode in ("+str(townListRsql)+") and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' AND visitsl>0 GROUP BY towncode) as z GROUP BY towncode) as z group by towncode"
                    else:
                        dateRecordsSrSch="select field1 as region,towncode as towncode,town_name as town_name, sum(ecoRate) as ecoRate, sum(strikeRate) as strikeRate from (select field1,towncode,town_name, 0 as ecoRate, sum(s_q)/sum(v_q)*100 as strikeRate from (SELECT field1,towncode,town_name, COUNT(visitsl) as v_q, 0 as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and towncode = '"+str(session.town_code)+"' and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' GROUP BY towncode union SELECT field1,towncode,town_name, 0 as v_q, COUNT(visitsl) as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and towncode = '"+str(session.town_code)+"' and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' AND visitsl>0 GROUP BY towncode) as z group by towncode union select field1,towncode,town_name, sum(s_q)/sum(v_q)*100 as ecoRate, 0 as strikeRate from (SELECT field1,towncode,town_name, COUNT(DISTINCT(outletcode)) as v_q,0 as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and towncode = '"+str(session.town_code)+"' and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' GROUP BY towncode union SELECT field1,towncode,town_name, 0 as v_q,COUNT(DISTINCT(outletcode)) as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and towncode = '"+str(session.town_code)+"' and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' AND visitsl>0 GROUP BY towncode) as z GROUP BY towncode) as z group by towncode"
                        # return dateRecordsSrSch
            else:
                dateRecordsSrSch="select field1 as region,towncode as towncode,town_name as town_name, sum(ecoRate) as ecoRate, sum(strikeRate) as strikeRate from (select field1,towncode,town_name, 0 as ecoRate, sum(s_q)/sum(v_q)*100 as strikeRate from (SELECT field1,towncode,town_name, COUNT(visitsl) as v_q, 0 as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' GROUP BY field1 union SELECT field1,towncode,town_name, 0 as v_q, COUNT(visitsl) as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' AND visitsl>0 GROUP BY field1) as z group by field1 union select field1,towncode,town_name, sum(s_q)/sum(v_q)*100 as ecoRate, 0 as strikeRate from (SELECT field1,towncode,town_name, COUNT(DISTINCT(outletcode)) as v_q,0 as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' GROUP BY field1 union SELECT field1,towncode,town_name, 0 as v_q,COUNT(DISTINCT(outletcode)) as s_q FROM `z_outlet_schedule` WHERE field1!='ZREGION' and `scheduleDate`>='"+lastMOCAuditFromDate+"' AND `scheduleDate`<='"+lastMOCAuditToDate+"' AND visitsl>0 GROUP BY field1) as z GROUP BY field1) as z group by field1"
            # return dateRecordsSrSch
            srOutletScheduleRec=db.executesql(dateRecordsSrSch,as_dict = True)
            for i in range(len(srOutletScheduleRec)):
                recordListStr=srOutletScheduleRec[i]

                region=recordListStr['region'].upper()
                ecoRate=recordListStr['ecoRate']
                strikeRate=recordListStr['strikeRate']
                towncode = recordListStr['towncode'].upper()+'-'+recordListStr['town_name'].upper()
                if session.user_role == 'TM':
                    dictData1 = {'towncode':str(towncode), 'ECO':int(ecoRate),'SR':int(strikeRate)}
                else:
                    dictData1 = {'Region': str(region), 'ECO': int(ecoRate), 'SR': int(strikeRate)}
                recordList1.append(dictData1)

            if session.user_role=='TM':
                if session.town_code!='ALL':
                    if len(town_code)>1:
                        dateRecordsCompliance="select `REGION`,`TownCode`,`TOWN`, sum(passOutlet) as passOutlet, sum(totalOutlet) as totalOutlet from (SELECT `REGION`, `TownCode`,`TOWN`, count(`OUTLET_CODE`) as passOutlet,0 as totalOutlet  FROM `z_result` where `COMPLIANCE_6P`='Y' and TownCode in ("+str(townListRsql)+") AND MOC_ID='"+str(dateMOCcom)+"' group by `TownCode` union SELECT `REGION`, `TownCode`,`TOWN`, 0 as passOutlet, count(`OUTLET_CODE`) as totalOutlet FROM `z_result` where TownCode in ("+str(townListRsql)+") AND MOC_ID='"+str(dateMOCcom)+"' group by `TownCode`) as z group by TownCode"
                    else:
                        # return 'abcd'
                        dateRecordsCompliance="select `REGION`, `TownCode`, `TOWN`,sum(passOutlet) as passOutlet, sum(totalOutlet) as totalOutlet from (SELECT `REGION`, `TownCode`,`TOWN`, count(`OUTLET_CODE`) as passOutlet,0 as totalOutlet  FROM `z_result` where `COMPLIANCE_6P`='Y' and TownCode = '"+str(session.town_code)+"' AND MOC_ID='"+str(dateMOCcom)+"' group by `TownCode` union SELECT `REGION`, `TownCode`, `TOWN`,0 as passOutlet, count(`OUTLET_CODE`) as totalOutlet FROM `z_result` where TownCode = '"+str(session.town_code)+"' AND MOC_ID='"+str(dateMOCcom)+"' group by `TownCode`) as z group by TownCode"
            else:
                dateRecordsCompliance="select `REGION`,`TownCode`, `TOWN`,sum(passOutlet) as passOutlet, sum(totalOutlet) as totalOutlet from (SELECT `REGION`,`TownCode`, `TOWN`,count(`OUTLET_CODE`) as passOutlet,0 as totalOutlet  FROM `z_result` where `COMPLIANCE_6P`='Y' AND MOC_ID='"+str(dateMOCcom)+"' group by `REGION` union SELECT `REGION`,`TownCode`,`TOWN`, 0 as passOutlet, count(`OUTLET_CODE`) as totalOutlet FROM `z_result` where MOC_ID='"+str(dateMOCcom)+"'  group by `REGION`) as z group by REGION"
            # return dateRecordsCompliance
            complianceRec=db.executesql(dateRecordsCompliance,as_dict = True)

            for i in range(len(complianceRec)):
                recordListStr=complianceRec[i]

                region=recordListStr['REGION'].upper()
                passOutlet=recordListStr['passOutlet']
                totalOutlet=recordListStr['totalOutlet']
                TownCode = recordListStr['TownCode'].upper()+'-'+recordListStr['TOWN'].upper()
                # return TownCode
                outletPass=passOutlet*100/totalOutlet
                outletTotal=100-outletPass
                if session.user_role == 'TM':
                    dictDataCom = {'TownCode':str(TownCode), 'PassOutlet':int(outletPass),'TotalOutlet':int(outletTotal)}
                else:
                    dictDataCom = {'Region': str(region), 'PassOutlet': int(outletPass),'TotalOutlet': int(outletTotal)}

                recordListCom.append(dictDataCom)

            posmAloHList=[]
            posmAloHeadRec=db((db.alc.due_date>=lastMOCAuditFromDate)&(db.alc.due_date<=lastMOCAuditToDate)).select(db.alc.posm_code, orderby=db.alc.posm_code)
            for aloH in posmAloHeadRec:
                posmAloHList.append(aloH.posm_code)

            if session.user_role=='TM':
                if session.town_code!='ALL':
                    if len(town_code)>1:
                        posmAloDetailsRec=db((db.alc_detail.posm_code.belongs(posmAloHList)) & (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.posm_code,db.alc_detail.a_qty.sum(),db.alc_detail.c_qty.sum(), groupby=db.alc_detail.posm_code, orderby=db.alc_detail.posm_code)
                    else:
                        posmAloDetailsRec=db((db.alc_detail.posm_code.belongs(posmAloHList)) & (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.posm_code,db.alc_detail.a_qty.sum(),db.alc_detail.c_qty.sum(), groupby=db.alc_detail.posm_code, orderby=db.alc_detail.posm_code)
            else:
                posmAloDetailsRec=db(db.alc_detail.posm_code.belongs(posmAloHList)).select(db.alc_detail.posm_code,db.alc_detail.a_qty.sum(),db.alc_detail.c_qty.sum(), groupby=db.alc_detail.posm_code, orderby=db.alc_detail.posm_code)
            # return db._lastsql
            for aloD in posmAloDetailsRec:
                posm_code=aloD[db.alc_detail.posm_code]
                a_qty=aloD[db.alc_detail.a_qty.sum()]
                c_qty=aloD[db.alc_detail.c_qty.sum()]

                usages=c_qty*100/a_qty
                alocation=100-usages

                dictPosmAlc = {'POSM':str(posm_code), 'Alocation':int(alocation),'Usages':int(usages)}#'Outlet':int(outSchedule),'Visit':int(outVisit)}
                recordListCmUsages.append(dictPosmAlc)

            if session.user_role=='TM':
                if session.town_code!='ALL':
                    if len(town_code)>1:
                        posmAgencyDetailsRec=db((db.agency_details.posm_code.belongs(posmAloHList))& (db.agency_details.town_code.belongs(townList))).select(db.agency_details.posm_code,db.agency_details.allocation_qty.sum(),db.agency_details.usages_qty.sum(), groupby=db.agency_details.posm_code, orderby=db.agency_details.posm_code)
                    else:
                        posmAgencyDetailsRec=db((db.agency_details.posm_code.belongs(posmAloHList))& (db.agency_details.town_code==session.town_code)).select(db.agency_details.posm_code,db.agency_details.allocation_qty.sum(),db.agency_details.usages_qty.sum(), groupby=db.agency_details.posm_code, orderby=db.agency_details.posm_code)
            else:
                posmAgencyDetailsRec=db(db.agency_details.posm_code.belongs(posmAloHList)).select(db.agency_details.posm_code,db.agency_details.allocation_qty.sum(),db.agency_details.usages_qty.sum(), groupby=db.agency_details.posm_code, orderby=db.agency_details.posm_code)
            # return db._lastsql
            # & ((~db.agency_details.town_code.contains('Z99')) & (~db.agency_details.town_code.contains('T99')))
            for aloAgencyD in posmAgencyDetailsRec:
                posm_code=aloAgencyD[db.agency_details.posm_code]
                allocation_qty=aloAgencyD[db.agency_details.allocation_qty.sum()]
                usages_qty=aloAgencyD[db.agency_details.usages_qty.sum()]

                # uQty=allocation_qty-usages_qty

                usages=usages_qty*100/allocation_qty
                alocation=100-usages

                dictPosmAlcAgency = {'POSM':str(posm_code), 'agencyAlocation':int(alocation),'agencyUsages':int(usages)}#'Outlet':int(outSchedule),'Visit':int(outVisit)}
                recordListAgencyUsages.append(dictPosmAlcAgency)

            if session.user_role=='TM':
                if session.town_code!='ALL':
                    if len(town_code)>1:
                        psCountNorth = db((db.z_pjp.field1=='NORTH REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode.belongs(townList))).count()
                        psCountCentralNorth = db((db.z_pjp.field1=='CENTRAL NORTH REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode.belongs(townList))).count()
                        psCountCentralSouth = db((db.z_pjp.field1=='CENTRAL SOUTH REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode.belongs(townList))).count()
                        psCountSouth = db((db.z_pjp.field1=='SOUTH REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode.belongs(townList))).count()
                        psCountEast = db((db.z_pjp.field1=='EAST REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode.belongs(townList))).count()

                        cmCountNorth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='NORTH REGION')& (db.sm_town.town_code.belongs(townList))).count()
                        cmCountCentralNorth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='CENTRAL NORTH REGION')& (db.sm_town.town_code.belongs(townList))).count()
                        cmCountCentralSouth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='CENTRAL SOUTH REGION')& (db.sm_town.town_code.belongs(townList))).count()
                        cmCountSouth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='SOUTH REGION')& (db.sm_town.town_code.belongs(townList))).count()
                        cmCountEast =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='EAST REGION')& (db.sm_town.town_code.belongs(townList))).count()

                        cCountNorth =db((db.z_result.REGION == 'NORTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode.belongs(townList))& (db.z_result.MOC_ID==dateMOCcom)).count()
                        cCountCentralNorth =db((db.z_result.REGION == 'CENTRAL NORTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode.belongs(townList))& (db.z_result.MOC_ID==dateMOCcom)).count()
                        cCountCentralSouth =db((db.z_result.REGION == 'CENTRAL SOUTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode.belongs(townList))& (db.z_result.MOC_ID==dateMOCcom)).count()
                        cCountSouth =db((db.z_result.REGION == 'SOUTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode.belongs(townList))& (db.z_result.MOC_ID==dateMOCcom)).count()
                        cCountEast =db((db.z_result.REGION == 'EAST REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode.belongs(townList))& (db.z_result.MOC_ID==dateMOCcom)).count()

                        sbCountNorth=0
                        sbCountCentralNorth=0
                        sbCountCentralSouth=0
                        sbCountSouth=0
                        sbCountEast=0
                        sbCountNorthCM=0
                        sbCountNorthRecCM =db((db.alc_detail.region=='NORTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if sbCountNorthRecCM:
                            sbCountNorthCM=sbCountNorthRecCM[0][db.alc_detail.c_qty.sum()]

                        sbCountNorthAgency = 0
                        sbCountNorthRecAgency = db((db.agency_details.town_code.belongs(townList))&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'NORTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountNorthRecAgency:
                            sbCountNorthAgency = sbCountNorthRecAgency[0][db.agency_details.usages_qty.sum()]

                        sbCountNorth = sbCountNorthCM + sbCountNorthAgency
                        sbCountCentralNorthCM = 0
                        sbCountCentralNorthRecCM =db((db.alc_detail.region=='CENTRAL NORTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)

                        if sbCountCentralNorthRecCM:
                            sbCountCentralNorthCM=sbCountCentralNorthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        sbCountCentralNorthAgency = 0
                        sbCountCentralNorthRecAgency = db((db.agency_details.town_code.belongs(townList))&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL NORTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountCentralNorthRecAgency:
                            sbCountCentralNorthAgency = sbCountCentralNorthRecAgency[0][db.agency_details.usages_qty.sum()]
                            # return sbCountCentralNorthAgency
                        sbCountCentralNorth = sbCountCentralNorthAgency + sbCountCentralNorthCM

                        #
                        sbCountCentralSouthCM = 0
                        sbCountCentralSouthRecCM =db((db.alc_detail.region=='CENTRAL SOUTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if sbCountCentralSouthRecCM:
                            sbCountCentralSouthCM=sbCountCentralSouthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        sbCountCentralSouthAgency = 0
                        sbCountCentralSouthRecAgency = db((db.agency_details.town_code.belongs(townList))&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL SOUTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountCentralSouthRecAgency:
                            sbCountCentralSouthAgency = sbCountCentralSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                        sbCountCentralSouth = sbCountCentralSouthCM + sbCountCentralSouthAgency

                        #
                        sbCountSouthCM = 0
                        sbCountSouthRecCM =db((db.alc_detail.region=='SOUTH REGION')&((db.alc_detail.posm_type =='SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if sbCountSouthRecCM:
                            sbCountSouthCM=sbCountSouthRecCM[0][db.alc_detail.c_qty.sum()]
                        #

                        sbCountSouthCMAgency = 0
                        sbCountSouthRecAgency = db((db.agency_details.town_code.belongs(townList))&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'SOUTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountSouthRecAgency:
                            sbCountSouthCMAgency = sbCountSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                        sbCountSouth = sbCountSouthCM + sbCountSouthCMAgency

                        #
                        sbCountEastCM = 0
                        sbCountEastRecCM =db((db.alc_detail.region=='EAST REGION')&((db.alc_detail.posm_type =='SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if sbCountEastRecCM:
                            sbCountEastCM=sbCountEastRecCM[0][db.alc_detail.c_qty.sum()]
                        #

                        sbCountEastAgency = 0
                        sbCountEastRecAgency = db((db.agency_details.town_code.belongs(townList))&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'EAST REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountEastRecAgency:
                            sbCountEastAgency = sbCountEastRecAgency[0][db.agency_details.usages_qty.sum()]
                        sbCountEast = sbCountEastCM + sbCountEastAgency
                        #

                        mCountNorth=0
                        mCountCentralNorth=0
                        mCountCentralSouth=0
                        mCountSouth=0
                        mCountEast=0
                        mCountNorthCM = 0
                        mCountNorthRecCM =db((db.alc_detail.region=='NORTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountNorthRecCM:
                            mCountNorthCM=mCountNorthRecCM[0][db.alc_detail.c_qty.sum()]
                        mCountNorthAgency = 0
                        mCountNorthRecAgency = db((db.agency_details.town_code.belongs(townList)) & (db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'NORTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                        if mCountNorthRecAgency:
                            mCountNorthAgency = mCountNorthRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountNorthCM = mCountNorthCM + mCountNorthAgency

                        mCountCentralNorthCM = 0
                        mCountCentralNorthRecCM =db((db.alc_detail.region=='CENTRAL NORTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountCentralNorthRecCM:
                            mCountCentralNorthCM=mCountCentralNorthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        mCountCentralNorthAgency = 0
                        mCountNorthRecAgency = db((db.agency_details.town_code.belongs(townList)) & (db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL NORTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                        if mCountNorthRecAgency:
                            mCountCentralNorthAgency = mCountNorthRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountCentralNorth = mCountCentralNorthCM + mCountCentralNorthAgency
                        #
                        mCountCentralSouthCM = 0
                        mCountCentralSouthRec =db((db.alc_detail.region=='CENTRAL SOUTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountCentralSouthRec:
                            mCountCentralSouthCM=mCountCentralSouthRec[0][db.alc_detail.c_qty.sum()]

                        #
                        mCountCentralSouthAgecy = 0
                        mCountCentralSouthRecAgency = db((db.agency_details.town_code.belongs(townList)) & (db.agency_details.town_code == db.sm_town.town_code) & ( db.sm_town.region == 'CENTRAL SOUTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                        if mCountCentralSouthRecAgency:
                            mCountCentralSouthAgecy = mCountCentralSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountCentralSouth = mCountCentralSouthCM + mCountCentralSouthAgecy
                        #
                        mCountSouthCM = 0
                        mCountSouthRecCM =db((db.alc_detail.region=='SOUTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountSouthRecCM:
                            mCountSouthCM=mCountSouthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        mCountSouthAgency = 0
                        mCountSouthRecAgency = db((db.agency_details.town_code.belongs(townList)) & (db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'SOUTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                        if mCountSouthRecAgency:
                            mCountSouthAgency = mCountSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountSouth = mCountSouthCM + mCountSouthAgency
                        #
                        mCountEastCM = 0
                        mCountEastRecCM =db((db.alc_detail.region=='EAST REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code.belongs(townList))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountEastRecCM:
                            mCountEastCM=mCountEastRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        mCountEastAgency = 0
                        mCountEastRecAgency = db((db.agency_details.town_code.belongs(townList)) & (db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'EAST REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                        if mCountEastRecAgency:
                            mCountEastAgency = mCountEastRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountEast = mCountEastCM + mCountEastAgency

                        #
                    else:
                        psCountNorth = db((db.z_pjp.field1=='NORTH REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode==session.town_code)).count()
                        psCountCentralNorth = db((db.z_pjp.field1=='CENTRAL NORTH REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode==session.town_code)).count()
                        psCountCentralSouth = db((db.z_pjp.field1=='CENTRAL SOUTH REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode==session.town_code)).count()
                        psCountSouth = db((db.z_pjp.field1=='SOUTH REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode==session.town_code)).count()
                        psCountEast = db((db.z_pjp.field1=='EAST REGION')&(db.z_pjp.field2 ==1)& (db.z_pjp.towncode==session.town_code)).count()

                        cmCountNorth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='NORTH REGION')& (db.sm_town.town_code==session.town_code)).count()
                        cmCountCentralNorth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='CENTRAL NORTH REGION')& (db.sm_town.town_code==session.town_code)).count()
                        cmCountCentralSouth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='CENTRAL SOUTH REGION')& (db.sm_town.town_code==session.town_code)).count()
                        cmCountSouth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='SOUTH REGION')& (db.sm_town.town_code==session.town_code)).count()
                        cmCountEast =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='EAST REGION')& (db.sm_town.town_code==session.town_code)).count()

                        cCountNorth =db((db.z_result.REGION == 'NORTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode==session.town_code)& (db.z_result.MOC_ID==dateMOCcom)).count()
                        cCountCentralNorth =db((db.z_result.REGION == 'CENTRAL NORTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode==session.town_code)& (db.z_result.MOC_ID==dateMOCcom)).count()
                        cCountCentralSouth =db((db.z_result.REGION == 'CENTRAL SOUTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode==session.town_code)& (db.z_result.MOC_ID==dateMOCcom)).count()
                        cCountSouth =db((db.z_result.REGION == 'SOUTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode==session.town_code)& (db.z_result.MOC_ID==dateMOCcom)).count()
                        cCountEast =db((db.z_result.REGION == 'EAST REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.TownCode==session.town_code)& (db.z_result.MOC_ID==dateMOCcom)).count()

                        sbCountNorth=0
                        sbCountCentralNorth=0
                        sbCountCentralSouth=0
                        sbCountSouth=0
                        sbCountEast=0
                        sbCountNorthCM=0
                        sbCountNorthRecCM =db((db.alc_detail.region=='NORTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if sbCountNorthRecCM:
                            sbCountNorthCM=sbCountNorthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        sbCountNorthAgency = 0
                        sbCountNorthRecAgency = db((db.agency_details.town_code== session.town_code)&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'NORTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountNorthRecAgency:
                            sbCountNorthAgency = sbCountNorthRecAgency[0][db.agency_details.usages_qty.sum()]

                        sbCountNorth = sbCountNorthCM + sbCountNorthAgency
                        #
                        sbCountCentralNorthCM=0
                        sbCountCentralNorthRecCM =db((db.alc_detail.region=='CENTRAL NORTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if sbCountCentralNorthRecCM:
                            sbCountCentralNorthCM=sbCountCentralNorthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        sbCountCentralNorthAgency = 0
                        sbCountCentralNorthRecAgency = db((db.agency_details.town_code== session.town_code)&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL NORTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountCentralNorthRecAgency:
                            sbCountCentralNorthAgency = sbCountCentralNorthRecAgency[0][
                                db.agency_details.usages_qty.sum()]
                        sbCountCentralNorth = sbCountCentralNorthAgency + sbCountCentralNorthCM
                        #
                        sbCountCentralSouthCM = 0
                        sbCountCentralSouthRecCM =db((db.alc_detail.region=='CENTRAL SOUTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if sbCountCentralSouthRecCM:
                            sbCountCentralSouthCM=sbCountCentralSouthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        sbCountCentralSouthAgency = 0
                        sbCountCentralSouthRecAgency = db((db.agency_details.town_code== session.town_code)&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL SOUTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountCentralSouthRecAgency:
                            sbCountCentralSouthAgency = sbCountCentralSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                        sbCountCentralSouth = sbCountCentralSouthCM + sbCountCentralSouthAgency

                        #
                        sbCountSouthCM = 0
                        sbCountSouthRecCM =db((db.alc_detail.region=='SOUTH REGION')&((db.alc_detail.posm_type =='SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if sbCountSouthRecCM:
                            sbCountSouthCM=sbCountSouthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        sbCountSouthCMAgency = 0
                        sbCountSouthRecAgency = db((db.agency_details.town_code== session.town_code)&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'SOUTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountSouthRecAgency:
                            sbCountSouthCMAgency = sbCountSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                        sbCountSouth = sbCountSouthCM + sbCountSouthCMAgency

                        #
                        sbCountEastCM = 0
                        sbCountEastRecCM =db((db.alc_detail.region=='EAST REGION')&((db.alc_detail.posm_type =='SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if sbCountEastRecCM:
                            sbCountEastCM=sbCountEastRecCM[0][db.alc_detail.c_qty.sum()]
                        #

                        sbCountEastAgency = 0
                        sbCountEastRecAgency = db((db.agency_details.town_code== session.town_code)&(db.agency_details.town_code==db.sm_town.town_code) & (db.sm_town.region == 'EAST REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)

                        if sbCountEastRecAgency:
                            sbCountEastAgency = sbCountEastRecAgency[0][db.agency_details.usages_qty.sum()]
                        sbCountEast = sbCountEastCM + sbCountEastAgency

                        #

                        mCountNorth=0
                        mCountCentralNorth=0
                        mCountCentralSouth=0
                        mCountSouth=0
                        mCountEast=0
                        mCountNorthCM = 0
                        mCountNorthRecCM =db((db.alc_detail.region=='NORTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountNorthRecCM:
                            mCountNorthCM=mCountNorthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        mCountNorthAgency=0
                        mCountNorthRecAgency = db((db.agency_details.town_code == session.town_code) & (db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'NORTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                        if mCountNorthRecAgency:
                            mCountNorthAgency = mCountNorthRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountNorth = mCountNorthCM + mCountNorthAgency

                        mCountCentralNorthCM = 0
                        mCountCentralNorthRecCM =db((db.alc_detail.region=='CENTRAL NORTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountCentralNorthRecCM:
                            mCountCentralNorthCM=mCountCentralNorthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        mCountCentralNorthAgency = 0
                        mCountCentralNorthRecAgency = db((db.agency_details.town_code == session.town_code) & (db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL NORTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                        if mCountCentralNorthRecAgency:
                            mCountCentralNorthAgency = mCountCentralNorthRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountCentralNorth = mCountCentralNorthCM + mCountCentralNorthAgency

                        #
                        mCountCentralSouthCM = 0
                        mCountCentralSouthRecCM =db((db.alc_detail.region=='CENTRAL SOUTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountCentralSouthRecCM:
                            mCountCentralSouthCM=mCountCentralSouthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        mCountCentralSouthAgency=0
                        mCountCentralSouthRecAgency=db((db.agency_details.town_code==session.town_code)&(db.agency_details.town_code==db.sm_town.town_code)&(db.sm_town.region=='CENTRAL SOUTH REGION')&(db.agency_details.posm_type=='MEGA_HANGER')).select(db.agency_details.usages_qty.sum(),groupby=db.sm_town.region)
                        if mCountCentralSouthRecAgency:
                            mCountCentralSouthAgency=mCountCentralSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountCentralSouth=mCountCentralSouthCM + mCountCentralSouthAgency
                        #
                        mCountSouthCM = 0
                        mCountSouthRecCM =db((db.alc_detail.region=='SOUTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountSouthRecCM:
                            mCountSouthCM=mCountSouthRecCM[0][db.alc_detail.c_qty.sum()]
                        #
                        mCountSouthAgency = 0
                        mCountSouthRecAgency = db((db.agency_details.town_code == session.town_code) & (db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'SOUTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                        if mCountSouthRecAgency:
                            mCountSouthAgency = mCountSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountSouth = mCountSouthCM + mCountSouthAgency
                        #
                        mCountEastCM = 0
                        mCountEastRecCM =db((db.alc_detail.region=='EAST REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')& (db.alc_detail.town_code==session.town_code)).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                        if mCountEastRecCM:
                            mCountEastCM=mCountEastRecCM[0][db.alc_detail.c_qty.sum()]
                        mCountEastAgency = 0
                        mCountEastRecAgency = db((db.agency_details.town_code == session.town_code) & (db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'EAST REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                        if mCountEastRecAgency:
                            mCountEastAgency = mCountEastRecAgency[0][db.agency_details.usages_qty.sum()]
                        mCountEast = mCountEastCM + mCountEastAgency

            else:
                psCountNorth = db((db.z_pjp.field1=='NORTH REGION')&(db.z_pjp.field2 ==1)).count()
                psCountCentralNorth = db((db.z_pjp.field1=='CENTRAL NORTH REGION')&(db.z_pjp.field2 ==1)).count()
                psCountCentralSouth = db((db.z_pjp.field1=='CENTRAL SOUTH REGION')&(db.z_pjp.field2 ==1)).count()
                psCountSouth = db((db.z_pjp.field1=='SOUTH REGION')&(db.z_pjp.field2 ==1)).count()
                psCountEast = db((db.z_pjp.field1=='EAST REGION')&(db.z_pjp.field2 ==1)).count()

                cmCountNorth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='NORTH REGION')).count()
                cmCountCentralNorth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='CENTRAL NORTH REGION')).count()
                cmCountCentralSouth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='CENTRAL SOUTH REGION')).count()
                cmCountSouth =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='SOUTH REGION')).count()
                cmCountEast =db((db.sm_rep.rep_type == 'CM') &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code==db.sm_town.town_code)&(db.sm_town.region=='EAST REGION')).count()

                cCountNorth =db((db.z_result.REGION == 'NORTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.MOC_ID==dateMOCcom)).count()
                cCountCentralNorth =db((db.z_result.REGION == 'CENTRAL NORTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.MOC_ID==dateMOCcom)).count()
                cCountCentralSouth =db((db.z_result.REGION == 'CENTRAL SOUTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.MOC_ID==dateMOCcom)).count()
                cCountSouth =db((db.z_result.REGION == 'SOUTH REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.MOC_ID==dateMOCcom)).count()
                cCountEast =db((db.z_result.REGION == 'EAST REGION') & (db.z_result.COMPLIANCE_6P == 'Y')& (db.z_result.MOC_ID==dateMOCcom)).count()

                sbCountNorthCM=0
                sbCountCentralNorth=0
                sbCountCentralSouth=0
                sbCountSouth=0
                sbCountEast=0
                sbCountNorth=0
                sbCountNorthRec =db((db.alc_detail.region=='NORTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if sbCountNorthRec:
                    sbCountNorthCM=sbCountNorthRec[0][db.alc_detail.c_qty.sum()]

                sbCountNorthAgency = 0
                sbCountNorthRec = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'NORTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(),groupby=db.sm_town.region)

                if sbCountNorthRec:
                    sbCountNorthAgency = sbCountNorthRec[0][db.agency_details.usages_qty.sum()]
                sbCountNorth = sbCountNorthCM + sbCountNorthAgency

                sbCountCentralNorthCM = 0
                sbCountCentralNorthRec =db((db.alc_detail.region=='CENTRAL NORTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if sbCountCentralNorthRec:
                    sbCountCentralNorthCM=sbCountCentralNorthRec[0][db.alc_detail.c_qty.sum()]

                sbCountCentralNorthAgency = 0
                sbCountCentralNorthRecAgency = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL NORTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(),groupby=db.sm_town.region)

                if sbCountCentralNorthRecAgency:
                    sbCountCentralNorthAgency = sbCountCentralNorthRecAgency[0][db.agency_details.usages_qty.sum()]
                sbCountCentralNorth = sbCountCentralNorthAgency + sbCountCentralNorthCM

                sbCountCentralSouthCM=0
                sbCountCentralSouthRecCM =db((db.alc_detail.region=='CENTRAL SOUTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if sbCountCentralSouthRecCM:
                    sbCountCentralSouthCM=sbCountCentralSouthRecCM[0][db.alc_detail.c_qty.sum()]

                sbCountCentralSouthAgency = 0
                sbCountCentralSouthRecAgency = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL SOUTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(),groupby=db.sm_town.region)

                if sbCountCentralSouthRecAgency:
                    sbCountCentralSouthAgency = sbCountCentralSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                sbCountCentralSouth = sbCountCentralSouthCM + sbCountCentralSouthAgency

                sbCountSouthCM=0
                sbCountSouthRec =db((db.alc_detail.region=='SOUTH REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if sbCountSouthRec:
                    sbCountSouthCM=sbCountSouthRec[0][db.alc_detail.c_qty.sum()]

                sbCountSouthCMAgency = 0
                sbCountSouthRecAgency = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'SOUTH REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(),groupby=db.sm_town.region)

                if sbCountSouthRecAgency:
                    sbCountSouthCMAgency = sbCountSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                sbCountSouth = sbCountSouthCM + sbCountSouthCMAgency

                sbCountEastCM=0
                sbCountEastRec =db((db.alc_detail.region=='EAST REGION')&((db.alc_detail.posm_type == 'SHOPBOARD_BACKLIT') | (db.alc_detail.posm_type == 'SHOPBOARD_NONLIT'))).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if sbCountEastRec:
                    sbCountEastCM=sbCountEastRec[0][db.alc_detail.c_qty.sum()]

                sbCountEastAgency = 0
                sbCountEastRecAgency = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'EAST REGION') & ((db.agency_details.posm_type == 'SHOPBOARD_BACKLIT') | (db.agency_details.posm_type == 'SHOPBOARD_NONLIT'))).select(db.agency_details.usages_qty.sum(),groupby=db.sm_town.region)

                if sbCountEastRecAgency:
                    sbCountEastAgency = sbCountEastRecAgency[0][db.agency_details.usages_qty.sum()]
                sbCountEast = sbCountEastCM + sbCountEastAgency


                mCountNorth=0
                mCountCentralNorth=0
                mCountCentralSouth=0
                mCountSouth=0
                mCountEast=0
                mCountNorthCM = 0
                mCountNorthRecCM =db((db.alc_detail.region=='NORTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if mCountNorthRecCM:
                    mCountNorthCM=mCountNorthRecCM[0][db.alc_detail.c_qty.sum()]
                #
                mCountNorthAgency = 0
                mCountNorthRecAgency = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'NORTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(),groupby=db.sm_town.region)
                if mCountNorthRecAgency:
                    mCountNorthAgency = mCountNorthRecAgency[0][db.agency_details.usages_qty.sum()]
                mCountNorth = mCountNorthCM + mCountNorthAgency
                #
                mCountCentralNorthCM = 0
                mCountCentralNorthRecCM =db((db.alc_detail.region=='CENTRAL NORTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if mCountCentralNorthRecCM:
                    mCountCentralNorthCM=mCountCentralNorthRecCM[0][db.alc_detail.c_qty.sum()]
                #
                mCountCentralNorthAgency = 0
                mCountCentralNorthRecAgency = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL NORTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                if mCountCentralNorthRecAgency:
                    mCountCentralNorthAgency = mCountCentralNorthRecAgency[0][db.agency_details.usages_qty.sum()]
                mCountCentralNorth = mCountCentralNorthCM + mCountCentralNorthAgency
                #
                mCountCentralSouthCM = 0
                mCountCentralSouthRecCM =db((db.alc_detail.region=='CENTRAL SOUTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if mCountCentralSouthRecCM:
                    mCountCentralSouthCM=mCountCentralSouthRecCM[0][db.alc_detail.c_qty.sum()]

                #
                mCountCentralSouthAgency = 0
                mCountCentralSouthRecAgency = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'CENTRAL SOUTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                if mCountCentralSouthRecAgency:
                    mCountCentralSouthAgency = mCountCentralSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                mCountCentralSouth = mCountCentralSouthCM + mCountCentralSouthAgency
                #
                mCountSouthCM = 0
                mCountSouthRecCM =db((db.alc_detail.region=='SOUTH REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if mCountSouthRecCM:
                    mCountSouthCM=mCountSouthRecCM[0][db.alc_detail.c_qty.sum()]
                #
                mCountSouthAgency = 0
                mCountSouthRecAgency = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'SOUTH REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                if mCountSouthRecAgency:
                    mCountSouthAgency = mCountSouthRecAgency[0][db.agency_details.usages_qty.sum()]
                mCountSouth = mCountSouthCM + mCountSouthAgency
                #
                mCountEastCM = 0
                mCountEastRecCM =db((db.alc_detail.region=='EAST REGION')&(db.alc_detail.posm_type == 'MEGA_HANGER')).select(db.alc_detail.c_qty.sum(),groupby=db.alc_detail.region)
                if mCountEastRecCM:
                    mCountEastCM=mCountEastRecCM[0][db.alc_detail.c_qty.sum()]
                #
                mCountEastAgency = 0
                mCountEastRecAgency = db((db.agency_details.town_code == db.sm_town.town_code) & (db.sm_town.region == 'EAST REGION') & (db.agency_details.posm_type == 'MEGA_HANGER')).select(db.agency_details.usages_qty.sum(), groupby=db.sm_town.region)
                if mCountEastRecAgency:
                    mCountEastAgency = mCountEastRecAgency[0][db.agency_details.usages_qty.sum()]
                mCountEast = mCountEastCM + mCountEastAgency
                #

    # attList = attPercent,
    
    return dict(lastMOCAuditFromDate=lastMOCAuditFromDate,lastMOCAuditToDate=lastMOCAuditToDate,recordList=recordList,recordList1=recordList1,recordListCmUsages=recordListCmUsages,recordListAgencyUsages=recordListAgencyUsages,recordListCom=recordListCom,psCountNorth=psCountNorth,psCountCentralNorth=psCountCentralNorth,psCountCentralSouth=psCountCentralSouth,psCountSouth=psCountSouth,psCountEast=psCountEast,cmCountNorth=cmCountNorth,cmCountCentralNorth=cmCountCentralNorth,cmCountCentralSouth=cmCountCentralSouth,cmCountSouth=cmCountSouth,cmCountEast=cmCountEast,cCountNorth=cCountNorth,cCountCentralNorth=cCountCentralNorth,cCountCentralSouth=cCountCentralSouth,cCountSouth=cCountSouth,cCountEast=cCountEast,sbCountNorth=sbCountNorth,sbCountCentralNorth=sbCountCentralNorth,sbCountCentralSouth=sbCountCentralSouth,sbCountSouth=sbCountSouth,sbCountEast=sbCountEast,mCountNorth=mCountNorth,mCountCentralNorth=mCountCentralNorth,mCountCentralSouth=mCountCentralSouth,mCountSouth=mCountSouth,mCountEast=mCountEast)
    # return dict(lastMOCAuditFromDate=lastMOCAuditFromDate,lastMOCAuditToDate=lastMOCAuditToDate,recordList=recordList,recordList1=recordList1,attList=attPercent,recordListCmUsages=0,recordListAgencyUsages=0,recordListCom=0,psCountNorth=0,psCountCentralNorth=0,psCountCentralSouth=0,psCountSouth=0,psCountEast=0,cmCountNorth=0,cmCountCentralNorth=0,cmCountCentralSouth=0,cmCountSouth=0,cmCountEast=0,cCountNorth=0,cCountCentralNorth=0,cCountCentralSouth=0,cCountSouth=0,cCountEast=0,sbCountNorth=0,sbCountCentralNorth=0,sbCountCentralSouth=0,sbCountSouth=0,sbCountEast=0,mCountNorth=0,mCountCentralNorth=0,mCountCentralSouth=0,mCountSouth=0,mCountEast=0)


def mapLoad():
    cid=str(request.vars.cid).strip().upper()

    rows=db((db.participant.cid==cid) & (db.participant.district!='')).select(db.participant.district, db.participant.district.count(), groupby = db.participant.district)

    distInfo = ''
    for row in rows:
        districtName = row[db.participant.district]
        districtParticipant = str(row[db.participant.district.count()])

        if distInfo == '':
            distInfo = districtName+'<fd>'+districtParticipant
        else:
            distInfo += '<rd>'+districtName+'<fd>'+districtParticipant



    return distInfo
# def dashboard_new():
#     if (session.user_id=='' or session.user_id==None):
#         redirect(URL('index'))
#
#     response.title="Hawk's Eye"
#     curent_month = str(current_date)[:7] + '-' + '01'
#
#     psDataRec=''
#
#     attList=[['Attendance']]
#
#     totalCMSup = db(((db.sm_rep.rep_type == 'CM') | (db.sm_rep.rep_type == 'SUPERVISOR')) & (db.sm_rep.status == 'ACTIVE')).count()
#
#     cmAttenData = db(db.sm_attendance.day_attendance == current_date).count()
#     # return str(totalCMSup)+'==='+str(cmAttenData)
#     attPercent=cmAttenData*100/totalCMSup
#     dictData2 = [float(attPercent)]
#     attList.append(dictData2)
#
#     lastMOCAuditFromDate = ''
#     lastMOCAuditToDate = ''
#     mocRows = db(db.sm_settings.s_key == 'MOC1').select(db.sm_settings.s_value)
#     for mocRow in mocRows:
#         mocDate = mocRow.s_value.split(',')
#         lastMOCAuditFromDate = mocDate[0]
#         lastMOCAuditToDate = mocDate[1]
#
#     recordList=[]
#     recordList1 = [['Region', 'Schedule Outlet', 'Outlet Visit']]
#     regRec = db(db.sm_town.region != 'ZREGION').select(db.sm_town.region, groupby=db.sm_town.region)
#
#     for row in regRec:
#         region = row.region
#
#         psCount = db((db.outlet.region == region)&(db.outlet.ps_status == 1)).count()
#
#
#         townList = []
#         recTown = db(db.sm_town.region == region).select(db.sm_town.town_code)
#         for rowTown in recTown:
#             townList.append(rowTown.town_code)
#
#
#         cmRows =db(((db.sm_rep.rep_type == 'CM') | (db.sm_rep.rep_type == 'SUPERVISOR')) &(db.sm_rep_town.rep_id == db.sm_rep.rep_id)&(db.sm_rep_town.town_code.belongs(townList))).select(db.sm_rep.rep_id)
#         cmCount = len(cmRows)
#
#         cmList= []
#         for cmRow in cmRows:
#             cmList.append(cmRow[db.sm_rep.rep_id])
#
#         mocVisit = db((db.z_visit.submitDate >= lastMOCAuditFromDate)&(db.z_visit.submitDate < lastMOCAuditToDate) & (db.z_visit.cmcode.belongs(cmList))).count()
#
#         # shopBoard = db((db.usages.usages_date >= lastMOCAuditFromDate) &(db.usages.usages_date < lastMOCAuditToDate) & ((db.usages.posm_type == 'SHOPBOARD_BACKLIT')|(db.usages.posm_type == 'SHOPBOARD_NONLIT')) & (db.usages.town_code.belongs(townList))).count()
#         # # return db._lastsql
#         # megahanger = db((db.usages.usages_date >= lastMOCAuditFromDate) &(db.usages.usages_date < lastMOCAuditToDate) & (db.usages.posm_type == 'MEGA_HANGER')& (db.usages.town_code.belongs(townList))).count()
#
#         condition = ''
#         condition1 = ''
#         # if session.town_code != '':
#         #     if session.town_code != 'ALL':
#         #         if len(town_code) > 1:
#         town = str(townList).replace("[", "").replace("]", "")  # .replace("'","")
#         condition = condition + "AND alc_detail.town_code in (" + str(town) + ")"
#         condition1 = condition1 + "AND agency_details.town_code in (" + str(town) + ")"
#         #         else:
#         # condition = condition + "AND alc_detail.town_code ='" + session.town_code + "'"
#         # condition1 = condition1 + "AND agency_details.town_code ='" + session.town_code + "'"
#
#         dateRecordShop = "select region as region,brand as brand,posm_code as posm_code,posm_type as posm_type,sum(c_qty) as c_qty FROM((select sm_town.region as region,alc_detail.brand as brand,alc_detail.posm_code as posm_code,alc_detail.posm_type as posm_type,sum(alc_detail.c_qty) as c_qty FROM alc_detail,sm_town where alc_detail.town_code=sm_town.town_code and alc_detail.posm_type='SHOPBOARD_BACKLIT' or alc_detail.posm_type='SHOPBOARD_NONLIT'" + condition + " GROUP BY sm_town.region) UNION (select sm_town.region as region,agency_details.brand as brand,agency_details.posm_code as posm_code,agency_details.posm_type as posm_type,sum(agency_details.usages_qty) as c_qty FROM agency_details,sm_town where agency_details.town_code=sm_town.town_code and agency_details.posm_type='SHOPBOARD_BACKLIT' or agency_details.posm_type='SHOPBOARD_NONLIT'" + condition1 + " GROUP BY sm_town.region)) abc GROUP BY region"
#         # return dateRecords
#         recordListShop = db.executesql(dateRecordShop, as_dict=True)
#         for i in range(len(recordListShop)):
#             recordListStr = recordListShop[i]
#
#             c_qty = recordListStr['c_qty']
#         # return c_qty
#
#         dateRecordMEGA = "select region as region,brand as brand,posm_code as posm_code,posm_type as posm_type,sum(c_qty) as cQty FROM((select sm_town.region as region,alc_detail.brand as brand,alc_detail.posm_code as posm_code,alc_detail.posm_type as posm_type,sum(alc_detail.c_qty) as c_qty FROM alc_detail,sm_town where alc_detail.town_code=sm_town.town_code and alc_detail.posm_type='MEGA_HANGER'" + condition + " GROUP BY sm_town.region) UNION (select sm_town.region as region,agency_details.brand as brand,agency_details.posm_code as posm_code,agency_details.posm_type as posm_type,sum(agency_details.usages_qty) as c_qty FROM agency_details,sm_town where agency_details.town_code=sm_town.town_code and agency_details.posm_type='MEGA_HANGER'" + condition1 + " GROUP BY sm_town.region)) abc GROUP BY region"
#         recordListmega = db.executesql(dateRecordMEGA, as_dict=True)
#         for j in range(len(recordListmega)):
#             recordListMegaStr = recordListmega[j]
#
#             c_qtyMega= recordListMegaStr['cQty']
#
#         dictData = {'region':str(region),'psCount':str(psCount),'cmCount':str(cmCount),'mocVisit':str(mocVisit),'recordListShop':str(c_qty),'megahanger':str(c_qtyMega)}
#         recordList.append(dictData)
#
#         schedualOutlet = db((db.z_outlet_schedule.scheduleDate>=lastMOCAuditFromDate)&(db.z_outlet_schedule.scheduleDate<lastMOCAuditToDate)&(db.z_outlet_schedule.towncode.belongs(townList))).count()
#         outletVisit = mocVisit
#         dictData1 = [str(region), int(schedualOutlet), int(outletVisit)]
#         recordList1.append(dictData1)
#
#     return dict(lastMOCAuditFromDate=lastMOCAuditFromDate,lastMOCAuditToDate=lastMOCAuditToDate,recordList=recordList,recordList1=recordList1,attList=attList)

def dashboard():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    response.title = "Hawk's Eye"

    reqPage = len(request.args)

    # --------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # --------end paging

    #----- Brand Show Current Month only
    # curent_month = str(current_date)[:7] + '-' + '01'
    # record = db((db.brand.brand_id == db.alc.brand)&(db.alc.due_date>=curent_month)).select(db.brand.brand_id, db.brand.image,orderby=db.brand.brand_name, groupby=db.brand.brand_id)


    record = db(db.brand.display_dashboard == 'YES').select(db.brand.brand_id, db.brand.image,orderby=db.brand.brand_name)
    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    #recCount=0
    qset=db()
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code==session.town_code)

    qset=qset(db.alc.id == db.alc_detail.alc_id)
    qset=qset(db.alc.due_date < current_date)
    qset=qset(db.alc_detail.r_qty == 0)
    record2 =qset.select(db.alc_detail.town_code.count(), db.alc_detail.town_code, db.alc_detail.town_name, db.alc.ALL,groupby=db.alc_detail.posm_code)

    # currentYear = str(date_fixed)[2:4]
    cMonth = str(date_fixed)[0:7]
    # currentMonth = datetime.datetime.strptime(currentYear + '-' + cMonth + '-' + '01', "%y-%b-%d")
    # currentMonth = str(datetime.datetime.strptime(currentYear + '-' + cMonth + '-' + '01', "%y-%b-%d"))[3:5]
    # return currentMonth

    dateRecords="SELECT due_date  FROM `alc` GROUP BY substr(`due_date`, 3, 5) order by due_date desc"
    recordList = db.executesql(dateRecords, as_dict=True)

    return dict(record=record, page=page, record2=record2,recordList=recordList)


def details_town():
    task_id = 'deadlineMissedPOSMUpdate_Manage'
    access_permission = check_role(task_id)


    # rawId = request.vars.rawId
    brand_id=request.vars.brand_id
    posm_code = request.vars.posm_code
    posm_type = request.vars.posm_type
    town_code = request.vars.town_code
    # return town_code
    # record = db((db.alc.id == db.alc_detail.alc_id) &(db.alc_detail.posm_code == posm_code) &(~db.alc_detail.town_code.belongs(session.recTown))).select(db.alc.posm_type,db.alc_detail.ALL)

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    #recCount=0
    qset=db()
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code==session.town_code)

    qset=qset(db.alc.id == db.alc_detail.alc_id)
    qset=qset(db.alc_detail.posm_code == posm_code)
    qset = qset(db.alc.due_date < current_date)
    qset=qset(db.alc_detail.r_qty==0)
    qset = qset(db.alc_detail.penalty_flag == 0)
    record = qset.select(db.alc.posm_type, db.alc.due_date,db.alc_detail.ALL)

    return dict(record=record, brand_id=brand_id, posm_code=posm_code, posm_type=posm_type, town_code=town_code,access_permission=access_permission)

def deadlineMissedPOSMedit_validation(form):

    note2 = str(request.vars.note)
    note = check_special_char(note2)
    penalty_flag = str(request.vars.penalty_lag)

    if penalty_flag != "YES" or note =="":
        form.errors.note = ''
        response.flash = 'Required Penalty value and Note'

    else:
        penalty_flag = 1
        form.vars.note = note
        form.vars.penalty_flag = penalty_flag

def deadlineMissedPOSMUpdate():


    response.title = 'Deadline Missed POSM - Update'

    rowID = request.args(0)
    brand = request.args(1)
    posm_code = request.args(2)
    posm_type = request.args(3)
    townCode = request.args(4)
    town_name = request.args(5)
    due_date = request.args(6)

    note2 = str(request.vars.note)
    note = check_special_char(note2)
    penalty_flag = str(request.vars.penalty_lag)
    # return note
    if penalty_flag =="YES":
        if note !="" and note!="None":
            update = db(db.alc_detail.id==rowID).update(note=note)

    record = db.alc_detail(rowID) or redirect(URL('details_town'))

    form = SQLFORM(db.alc_detail,
                   record=record,
                   deletable=True,
                   fields=['penalty_flag'],
                   submit_button='Update'
                   )
    if form.accepts(request.vars, session, onvalidation=deadlineMissedPOSMedit_validation):
        session.flash = 'Updated Successfully'
        redirect(URL('details_town',vars=dict(brand_id=brand,posm_code=posm_code,posm_type=posm_type,town_code=townCode)))

    return dict(form=form,brand=brand,posm_code=posm_code,posm_type=posm_type,town_code=townCode,town_name=town_name,due_date=due_date,rowID=rowID)


def dedlineMissTown_details_download():
    record=''

    brand_id = request.vars.brand_id
    posm_code = request.vars.posm_code
    posm_type = request.vars.posm_type
    town_code1 = request.vars.town_code

    # return brand_id
    # record = db((db.alc.id == db.alc_detail.alc_id) &(db.alc_detail.posm_code == posm_code) &(~db.alc_detail.town_code.belongs(session.recTown))).select(db.alc.posm_type,db.alc_detail.ALL)

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    # recCount=0
    qset = db()
    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code == session.town_code)


    qset = qset(db.alc_detail.posm_code == posm_code)
    qset = qset(db.alc_detail.posm_code == db.alc.posm_code)
    qset = qset(db.alc_detail.r_qty == 0)
    qset = qset(db.alc_detail.penalty_flag == 0)
    record = qset.select(db.alc_detail.ALL,db.alc.due_date, orderby=~db.alc.due_date)

    myString='Deadline Missed POSM \n'
    myString += 'Brand,POSM Code,POSM Type,Town Code,Town Name,Deadline Date \n'
    for rec in record:
        brand = rec[db.alc_detail.brand]
        posm_code = rec[db.alc_detail.posm_code]
        posm_type = rec[db.alc_detail.posm_type]
        town_code = rec[db.alc_detail.town_code]
        town_name = rec[db.alc_detail.town_name]
        due_date = rec[db.alc.due_date]


        myString += str(brand)+','+str(posm_code)+','+str(posm_type)+','+str(town_code)+','+str(town_name)+','+str(due_date)+'\n'

    # -----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_Deadline_missed_POSM.csv'
    return str(myString)

    return dict(recordList=recordList)


def all_dedlineMissTown_details_download():
    record=''
    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    # recCount=0
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
    record = qset.select(db.alc_detail.brand,db.alc_detail.posm_code,db.alc_detail.posm_type,db.alc_detail.town_code,db.alc_detail.town_name,db.alc.due_date, orderby=~db.alc.due_date)

    myString='Deadline Missed POSM Details \n'
    myString += 'Brand,POSM Code,POSM Type,Town Code,Town Name,Deadline Date \n'
    for rec in record:
        brand = rec[db.alc_detail.brand]
        posm_code = rec[db.alc_detail.posm_code]
        posm_type = rec[db.alc_detail.posm_type]
        town_code = rec[db.alc_detail.town_code]
        town_name = rec[db.alc_detail.town_name]
        due_date = rec[db.alc.due_date]


        myString += str(brand)+','+str(posm_code)+','+str(posm_type)+','+str(town_code)+','+str(town_name)+','+str(due_date)+'\n'

    # -----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_Deadline_missed_POSM_Details.csv'
    return str(myString)

    return dict(recordList=recordList)


def summary_dedlineMissTown_details_download():
    record=''

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
    record = qset.select(db.alc_detail.town_code.count(), db.alc_detail.town_code, db.alc.due_date,db.alc_detail.posm_code,db.alc_detail.posm_type,db.alc_detail.brand,groupby=db.alc_detail.posm_code, orderby=~db.alc.due_date)

    myString='Deadline Missed POSM Summary \n'
    myString += 'Brand,POSM Code,POSM Type,Town,Deadline Date \n'
    for rec in record:
        brand = rec[db.alc_detail.brand]
        posm_code = rec[db.alc_detail.posm_code]
        posm_type = rec[db.alc_detail.posm_type]
        town_code = rec[db.alc_detail.town_code.count()]
        due_date = rec[db.alc.due_date]


        myString += str(brand)+','+str(posm_code)+','+str(posm_type)+','+str(town_code)+','+str(due_date)+'\n'

    # -----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download__Deadline_missed_POSM(Summary).csv'
    return str(myString)

    return dict(recordList=recordList)

def shopboardLit():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    response.title = 'Shopboard BackLit'

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    condition=''
    condition1=''
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                town=str(townList).replace("[","").replace("]","")#.replace("'","")
                condition = condition+"AND alc_detail.town_code in ("+str(town)+")"
                condition1 = condition1+"AND agency_details.town_code in ("+str(town)+")"
            else:
                condition = condition+"AND alc_detail.town_code ='"+session.town_code+"'"
                condition1 = condition1+"AND agency_details.town_code ='"+session.town_code+"'"

    dateRecords="select region as region,brand as brand,posm_code as posm_code,posm_type as posm_type,sum(c_qty) as c_qty FROM((select sm_town.region as region,alc_detail.brand as brand,alc_detail.posm_code as posm_code,alc_detail.posm_type as posm_type,sum(alc_detail.c_qty) as c_qty FROM alc_detail,sm_town where alc_detail.town_code=sm_town.town_code and alc_detail.posm_type='SHOPBOARD_BACKLIT' "+condition+" GROUP BY sm_town.region,alc_detail.posm_type,alc_detail.brand) UNION (select sm_town.region as region,agency_details.brand as brand,agency_details.posm_code as posm_code,agency_details.posm_type as posm_type,sum(agency_details.usages_qty) as c_qty FROM agency_details,sm_town where agency_details.town_code=sm_town.town_code and agency_details.posm_type='SHOPBOARD_BACKLIT' "+condition1+" GROUP BY sm_town.region,agency_details.posm_type,agency_details.brand)) abc GROUP BY region,posm_type,brand"
    #return dateRecords
    recordList=db.executesql(dateRecords,as_dict = True)



    return dict(recordList=recordList)

def shopboardLit_details_download():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    year = str(request.vars.year)
    if year == '':
        session.flash = 'Please Select Year'
        redirect(URL('default', 'shopboardLit'))

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    condition=''
    condition1=''
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                town=str(townList).replace("[","").replace("]","")#.replace("'","")
                condition = condition+"AND usages.town_code in ("+str(town)+")"
                condition1 = condition1+"AND agency_usage.town_code in ("+str(town)+")"
            else:
                condition = condition+"AND usages.town_code ='"+session.town_code+"'"
                condition1 = condition1+"AND agency_usage.town_code ='"+session.town_code+"'"

    #dateRecords="select region as region,brand as brand,posm_code as posm_code,posm_type as posm_type,sum(c_qty) as c_qty FROM((select sm_town.region as region,alc_detail.brand as brand,alc_detail.posm_code as posm_code,alc_detail.posm_type as posm_type,sum(alc_detail.c_qty) as c_qty FROM alc_detail,sm_town where alc_detail.town_code=sm_town.town_code and alc_detail.posm_type='SHOPBOARD_BACKLIT' "+condition+" GROUP BY sm_town.region,alc_detail.posm_type,alc_detail.brand) UNION (select sm_town.region as region,agency_details.brand as brand,agency_details.posm_code as posm_code,agency_details.posm_type as posm_type,sum(agency_details.usages_qty) as c_qty FROM agency_details,sm_town where agency_details.town_code=sm_town.town_code and agency_details.posm_type='SHOPBOARD_BACKLIT' "+condition1+" GROUP BY sm_town.region,agency_details.posm_type,agency_details.brand)) abc GROUP BY region,posm_type,brand"

    # recordsUsage="select rep_id as rep_id,rep_name as rep_name, mobile as mobile_no, '' as agency_code, '' as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, stock_usage as stock_usage, a_qty as usage_qty, posm_type as posm_type, brand as brand, '' as sft, '' as light, '' as paint, '' as city_cor, usages_date as usages_date FROM usages where posm_type='SHOPBOARD_BACKLIT'"
    #
    # recordAgencyUsage="select agency_code as agency_code, agency_name as agency_name, rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no, outlet_id as outlet_code, outlet_name as outlet_name, route as route_name, town_code as town_code, town_name as town_name, posm_code as posm_code, brand as brand, posm_type as posm_type, allocation as stock_usage, qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, agency_date as usages_date FROM agency_usage where posm_type='SHOPBOARD_BACKLIT'"

    # current_month = str(year)[:4] + '-' + '01'+ '-' + '01'


    dateRecords = "select rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no,agency_code as agency_code, agency_name as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, posm_type as posm_type, brand as brand, stock_usage as stock_usage, usage_qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, usages_date as usages_date FROM((select rep_id as rep_id,rep_name as rep_name, mobile as mobile_no, '' as agency_code, '' as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, posm_type as posm_type, brand as brand, stock_usage as stock_usage, a_qty as usage_qty, '' as sft, '' as light, '' as paint, '' as city_cor, usages_date as usages_date FROM usages where posm_type='SHOPBOARD_BACKLIT' and substr(usages_date,1,4)="+str(year)+" "+condition+")UNION(select rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no,agency_code as agency_code, agency_name as agency_name,town_code as town_code, town_name as town_name, route as route_name, outlet_id as outlet_code, outlet_name as outlet_name,  posm_code as posm_code, posm_type as posm_type, brand as brand,  allocation as stock_usage, qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, agency_date as usages_date FROM agency_usage where posm_type='SHOPBOARD_BACKLIT' and substr(agency_date,1,4)="+str(year)+" "+condition1+"))abc"
    #return dateRecords
    recordList=db.executesql(dateRecords,as_dict = True)

    myString='Backlit Shop Sign\n'
    # myString+='From Date,`'+str(from_dt)+'\n'
    # myString+='To Date,`'+str(to_dt)+'\n'

    myString+='Rep ID,Rep Name,Mobile No,Agency Code,Agency Name,Town Code,Town Name,Route Name,Outlet Code,Outlet Name,POSM Code,POSM Type,Brand,Stock Execution,Execution Qty,SFT,Light,Paint,Tax Area,Execution Date\n'
    for i in range(len(recordList)):
        recordListStr=recordList[i]

        rep_id=recordListStr['rep_id']
        rep_name=recordListStr['rep_name']
        mobile_no=recordListStr['mobile_no']
        agency_code = recordListStr['agency_code']
        agency_name = recordListStr['agency_name']
        town_code = recordListStr['town_code']
        town_name = recordListStr['town_name']
        route_name = recordListStr['route_name']
        outlet_code = recordListStr['outlet_code']
        outlet_name = recordListStr['outlet_name']

        posm_code = recordListStr['posm_code']
        posm_type = recordListStr['posm_type']
        brand = recordListStr['brand']
        stock_usage = recordListStr['stock_usage']
        usage_qty = recordListStr['usage_qty']
        sft = recordListStr['sft']
        light = recordListStr['light']
        paint = recordListStr['paint']
        city_cor = recordListStr['city_cor']
        usages_date = recordListStr['usages_date']

        myString+=str(rep_id)+','+str(rep_name)+','+str(mobile_no)+','+str(agency_code)+','+str(agency_name)+','+str(town_code)+','+str(town_name)+','+str(route_name)+','+str(outlet_code)+','+str(outlet_name)+','+str(posm_code)+','+str(posm_type)+','+str(brand)+','+str(stock_usage)+','+str(usage_qty)+','+str(sft)+','+str(light)+','+str(paint)+','+str(city_cor)+','+str(usages_date)+'\n'

    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_backlit_shop_sign.csv'
    return str(myString)



def shopboardNonLit_details_download():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    year = str(request.vars.year)
    if year == '':
        session.flash = 'Please Select Year'
        redirect(URL('default', 'shopboardNonlit'))


    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    condition=''
    condition1=''
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                town=str(townList).replace("[","").replace("]","")#.replace("'","")
                condition = condition+"AND usages.town_code in ("+str(town)+")"
                condition1 = condition1+"AND agency_usage.town_code in ("+str(town)+")"
            else:
                condition = condition+"AND usages.town_code ='"+session.town_code+"'"
                condition1 = condition1+"AND agency_usage.town_code ='"+session.town_code+"'"

    #dateRecords="select region as region,brand as brand,posm_code as posm_code,posm_type as posm_type,sum(c_qty) as c_qty FROM((select sm_town.region as region,alc_detail.brand as brand,alc_detail.posm_code as posm_code,alc_detail.posm_type as posm_type,sum(alc_detail.c_qty) as c_qty FROM alc_detail,sm_town where alc_detail.town_code=sm_town.town_code and alc_detail.posm_type='SHOPBOARD_BACKLIT' "+condition+" GROUP BY sm_town.region,alc_detail.posm_type,alc_detail.brand) UNION (select sm_town.region as region,agency_details.brand as brand,agency_details.posm_code as posm_code,agency_details.posm_type as posm_type,sum(agency_details.usages_qty) as c_qty FROM agency_details,sm_town where agency_details.town_code=sm_town.town_code and agency_details.posm_type='SHOPBOARD_BACKLIT' "+condition1+" GROUP BY sm_town.region,agency_details.posm_type,agency_details.brand)) abc GROUP BY region,posm_type,brand"

    # recordsUsage="select rep_id as rep_id,rep_name as rep_name, mobile as mobile_no, '' as agency_code, '' as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, stock_usage as stock_usage, a_qty as usage_qty, posm_type as posm_type, brand as brand, '' as sft, '' as light, '' as paint, '' as city_cor, usages_date as usages_date FROM usages where posm_type='SHOPBOARD_BACKLIT'"
    #
    # recordAgencyUsage="select agency_code as agency_code, agency_name as agency_name, rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no, outlet_id as outlet_code, outlet_name as outlet_name, route as route_name, town_code as town_code, town_name as town_name, posm_code as posm_code, brand as brand, posm_type as posm_type, allocation as stock_usage, qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, agency_date as usages_date FROM agency_usage where posm_type='SHOPBOARD_BACKLIT'"

    dateRecords="select rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no,agency_code as agency_code, agency_name as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, posm_type as posm_type, brand as brand, stock_usage as stock_usage, usage_qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, usages_date as usages_date FROM((select rep_id as rep_id,rep_name as rep_name, mobile as mobile_no, '' as agency_code, '' as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, posm_type as posm_type, brand as brand, stock_usage as stock_usage, a_qty as usage_qty, '' as sft, '' as light, '' as paint, '' as city_cor, usages_date as usages_date FROM usages where posm_type='SHOPBOARD_NONLIT' and substr(usages_date,1,4)="+str(year)+" "+condition+")UNION(select rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no,agency_code as agency_code, agency_name as agency_name,town_code as town_code, town_name as town_name, route as route_name, outlet_id as outlet_code, outlet_name as outlet_name,  posm_code as posm_code, posm_type as posm_type, brand as brand,  allocation as stock_usage, qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, agency_date as usages_date FROM agency_usage where posm_type='SHOPBOARD_NONLIT' and substr(agency_date,1,4)="+str(year)+" "+condition1+"))abc"
    #return dateRecords
    recordList=db.executesql(dateRecords,as_dict = True)

    myString='NONLIT Shop Sign\n'
    # myString+='From Date,`'+str(from_dt)+'\n'
    # myString+='To Date,`'+str(to_dt)+'\n'

    myString+='Rep ID,Rep Name,Mobile No,Agency Code,Agency Name,Town Code,Town Name,Route Name,Outlet Code,Outlet Name,POSM Code,POSM Type,Brand,Stock Execution,Execution Qty,SFT,Light,Paint,Tax Area,Execution Date\n'
    for i in range(len(recordList)):
        recordListStr=recordList[i]

        rep_id=recordListStr['rep_id']
        rep_name=recordListStr['rep_name']
        mobile_no=recordListStr['mobile_no']
        agency_code = recordListStr['agency_code']
        agency_name = recordListStr['agency_name']
        town_code = recordListStr['town_code']
        town_name = recordListStr['town_name']
        route_name = recordListStr['route_name']
        outlet_code = recordListStr['outlet_code']
        outlet_name = recordListStr['outlet_name']
        posm_code = recordListStr['posm_code']
        posm_type = recordListStr['posm_type']
        brand = recordListStr['brand']
        stock_usage = recordListStr['stock_usage']
        usage_qty = recordListStr['usage_qty']
        sft = recordListStr['sft']
        light = recordListStr['light']
        paint = recordListStr['paint']
        city_cor = recordListStr['city_cor']
        usages_date = recordListStr['usages_date']

        myString+=str(rep_id)+','+str(rep_name)+','+str(mobile_no)+','+str(agency_code)+','+str(agency_name)+','+str(town_code)+','+str(town_name)+','+str(route_name)+','+str(outlet_code)+','+str(outlet_name)+','+str(posm_code)+','+str(posm_type)+','+str(brand)+','+str(stock_usage)+','+str(usage_qty)+','+str(sft)+','+str(light)+','+str(paint)+','+str(city_cor)+','+str(usages_date)+'\n'

    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_SHOPBOARD_NONLIT_shop_sign.csv'
    return str(myString)



def megaHanger_details_download():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    year = str(request.vars.year)
    if year == '':
        session.flash = 'Please Select Year'
        redirect(URL('default', 'mega_hanger'))

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    condition=''
    condition1=''
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                town=str(townList).replace("[","").replace("]","")#.replace("'","")
                condition = condition+"AND usages.town_code in ("+str(town)+")"
                condition1 = condition1+"AND agency_usage.town_code in ("+str(town)+")"
            else:
                condition = condition+"AND usages.town_code ='"+session.town_code+"'"
                condition1 = condition1+"AND agency_usage.town_code ='"+session.town_code+"'"

    #dateRecords="select region as region,brand as brand,posm_code as posm_code,posm_type as posm_type,sum(c_qty) as c_qty FROM((select sm_town.region as region,alc_detail.brand as brand,alc_detail.posm_code as posm_code,alc_detail.posm_type as posm_type,sum(alc_detail.c_qty) as c_qty FROM alc_detail,sm_town where alc_detail.town_code=sm_town.town_code and alc_detail.posm_type='SHOPBOARD_BACKLIT' "+condition+" GROUP BY sm_town.region,alc_detail.posm_type,alc_detail.brand) UNION (select sm_town.region as region,agency_details.brand as brand,agency_details.posm_code as posm_code,agency_details.posm_type as posm_type,sum(agency_details.usages_qty) as c_qty FROM agency_details,sm_town where agency_details.town_code=sm_town.town_code and agency_details.posm_type='SHOPBOARD_BACKLIT' "+condition1+" GROUP BY sm_town.region,agency_details.posm_type,agency_details.brand)) abc GROUP BY region,posm_type,brand"

    # recordsUsage="select rep_id as rep_id,rep_name as rep_name, mobile as mobile_no, '' as agency_code, '' as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, stock_usage as stock_usage, a_qty as usage_qty, posm_type as posm_type, brand as brand, '' as sft, '' as light, '' as paint, '' as city_cor, usages_date as usages_date FROM usages where posm_type='SHOPBOARD_BACKLIT'"
    #
    # recordAgencyUsage="select agency_code as agency_code, agency_name as agency_name, rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no, outlet_id as outlet_code, outlet_name as outlet_name, route as route_name, town_code as town_code, town_name as town_name, posm_code as posm_code, brand as brand, posm_type as posm_type, allocation as stock_usage, qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, agency_date as usages_date FROM agency_usage where posm_type='SHOPBOARD_BACKLIT'"

    dateRecords="select rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no,agency_code as agency_code, agency_name as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, posm_type as posm_type, brand as brand, stock_usage as stock_usage, usage_qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, usages_date as usages_date FROM((select rep_id as rep_id,rep_name as rep_name, mobile as mobile_no, '' as agency_code, '' as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, posm_type as posm_type, brand as brand, stock_usage as stock_usage, a_qty as usage_qty, '' as sft, '' as light, '' as paint, '' as city_cor, usages_date as usages_date FROM usages where posm_type='MEGA_HANGER' and substr(usages_date,1,4)="+str(year)+" "+condition+")UNION(select rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no,agency_code as agency_code, agency_name as agency_name,town_code as town_code, town_name as town_name, route as route_name, outlet_id as outlet_code, outlet_name as outlet_name,  posm_code as posm_code, posm_type as posm_type, brand as brand,  allocation as stock_usage, qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, agency_date as usages_date FROM agency_usage where posm_type='MEGA_HANGER' and substr(agency_date,1,4)="+str(year)+" "+condition1+"))abc"
    #return dateRecords
    recordList=db.executesql(dateRecords,as_dict = True)

    myString='MEGA_HANGER Shop Sign\n'
    # myString+='From Date,`'+str(from_dt)+'\n'
    # myString+='To Date,`'+str(to_dt)+'\n'

    myString+='Rep ID,Rep Name,Mobile No,Agency Code,Agency Name,Town Code,Town Name,Route Name,Outlet Code,Outlet Name,POSM Code,POSM Type,Brand,Stock Execution,Execution Qty,SFT,Light,Paint,Tax Area,Execution Date\n'
    for i in range(len(recordList)):
        recordListStr=recordList[i]

        rep_id=recordListStr['rep_id']
        rep_name=recordListStr['rep_name']
        mobile_no=recordListStr['mobile_no']
        agency_code = recordListStr['agency_code']
        agency_name = recordListStr['agency_name']
        town_code = recordListStr['town_code']
        town_name = recordListStr['town_name']
        route_name = recordListStr['route_name']
        outlet_code = recordListStr['outlet_code']
        outlet_name = recordListStr['outlet_name']
        posm_code = recordListStr['posm_code']
        posm_type = recordListStr['posm_type']
        brand = recordListStr['brand']
        stock_usage = recordListStr['stock_usage']
        usage_qty = recordListStr['usage_qty']
        sft = recordListStr['sft']
        light = recordListStr['light']
        paint = recordListStr['paint']
        city_cor = recordListStr['city_cor']
        usages_date = recordListStr['usages_date']

        myString+=str(rep_id)+','+str(rep_name)+','+str(mobile_no)+','+str(agency_code)+','+str(agency_name)+','+str(town_code)+','+str(town_name)+','+str(route_name)+','+str(outlet_code)+','+str(outlet_name)+','+str(posm_code)+','+str(posm_type)+','+str(brand)+','+str(stock_usage)+','+str(usage_qty)+','+str(sft)+','+str(light)+','+str(paint)+','+str(city_cor)+','+str(usages_date)+'\n'

    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_MEGA_HANGER_shop_sign.csv'
    return str(myString)



def pluginDispenser_details_download():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    year = str(request.vars.year)
    if year=='':
        session.flash = 'Please Select Year'
        redirect(URL('default','plugin_dispenser'))

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    condition=''
    condition1=''
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                town=str(townList).replace("[","").replace("]","")
                condition = condition+"AND usages.town_code in ("+str(town)+")"
                condition1 = condition1+"AND agency_usage.town_code in ("+str(town)+")"
            else:
                condition = condition+"AND usages.town_code ='"+session.town_code+"'"
                condition1 = condition1+"AND agency_usage.town_code ='"+session.town_code+"'"

    dateRecords="select rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no,agency_code as agency_code, agency_name as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, posm_type as posm_type, brand as brand, stock_usage as stock_usage, usage_qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, usages_date as usages_date FROM((select rep_id as rep_id,rep_name as rep_name, mobile as mobile_no, '' as agency_code, '' as agency_name, town_code as town_code, town_name as town_name, route_name as route_name, outlet_code as outlet_code, outlet_name as outlet_name, posm_code as posm_code, posm_type as posm_type, brand as brand, stock_usage as stock_usage, a_qty as usage_qty, '' as sft, '' as light, '' as paint, '' as city_cor, usages_date as usages_date FROM usages where posm_type='PLUGIN_DISPENSER' and substr(usages_date,1,4)="+str(year)+" "+condition+")UNION(select rep_id as rep_id, rep_name as rep_name, mobile_no as mobile_no,agency_code as agency_code, agency_name as agency_name,town_code as town_code, town_name as town_name, route as route_name, outlet_id as outlet_code, outlet_name as outlet_name,  posm_code as posm_code, posm_type as posm_type, brand as brand,  allocation as stock_usage, qty as usage_qty, sft as sft, light as light, paint as paint, city_cor as city_cor, agency_date as usages_date FROM agency_usage where posm_type='PLUGIN_DISPENSER' and substr(agency_date,1,4)="+str(year)+" "+condition1+"))abc"
    #return dateRecords
    recordList=db.executesql(dateRecords,as_dict = True)

    myString='PLUGIN DISPENSER Shop Sign\n'

    myString+='Rep ID,Rep Name,Mobile No,Agency Code,Agency Name,Town Code,Town Name,Route Name,Outlet Code,Outlet Name,POSM Code,POSM Type,Brand,Stock Execution,Execution Qty,SFT,Light,Paint,Tax Area,Execution Date\n'
    for i in range(len(recordList)):
        recordListStr=recordList[i]

        rep_id=recordListStr['rep_id']
        rep_name=recordListStr['rep_name']
        mobile_no=recordListStr['mobile_no']
        agency_code = recordListStr['agency_code']
        agency_name = recordListStr['agency_name']
        town_code = recordListStr['town_code']
        town_name = recordListStr['town_name']
        route_name = recordListStr['route_name']
        outlet_code = recordListStr['outlet_code']
        outlet_name = recordListStr['outlet_name']
        posm_code = recordListStr['posm_code']
        posm_type = recordListStr['posm_type']
        brand = recordListStr['brand']
        stock_usage = recordListStr['stock_usage']
        usage_qty = recordListStr['usage_qty']
        sft = recordListStr['sft']
        light = recordListStr['light']
        paint = recordListStr['paint']
        city_cor = recordListStr['city_cor']
        usages_date = recordListStr['usages_date']

        myString+=str(rep_id)+','+str(rep_name)+','+str(mobile_no)+','+str(agency_code)+','+str(agency_name)+','+str(town_code)+','+str(town_name)+','+str(route_name)+','+str(outlet_code)+','+str(outlet_name)+','+str(posm_code)+','+str(posm_type)+','+str(brand)+','+str(stock_usage)+','+str(usage_qty)+','+str(sft)+','+str(light)+','+str(paint)+','+str(city_cor)+','+str(usages_date)+'\n'

    #-----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_PLUGIN_DISPENSER_shop_sign.csv'
    return str(myString)




def shopboardNonlit():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    response.title = 'Shopboard Nonlit'

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    #recCount=0
    # qset=db()
    # if session.town_code!='':
    #     if session.town_code!='ALL':
    #         if len(town_code)>1:
    #             qset = qset(db.alc_detail.town_code.belongs(townList))
    #         else:
    #             qset = qset(db.alc_detail.town_code==session.town_code)
    #
    # qset=qset(db.alc.id==db.alc_detail.alc_id)
    # qset = qset(db.alc_detail.town_code==db.sm_town.town_code)
    # qset=qset(db.alc.posm_type=='SHOPBOARD_NONLIT')
    # #SHOPBOARD_NONLIT
    # record = qset.select(db.sm_town.region,db.alc_detail.brand,db.alc_detail.posm_code,db.alc_detail.c_qty.sum(),db.alc.posm_type, groupby=db.alc.posm_type|db.alc.brand, orderby=db.alc.brand)

    condition=''
    condition1=''
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                town=str(townList).replace("[","").replace("]","")#.replace("'","")
                condition = condition+"AND alc_detail.town_code in ("+str(town)+")"
                condition1 = condition1+"AND agency_details.town_code in ("+str(town)+")"
            else:
                condition = condition+"AND alc_detail.town_code ='"+session.town_code+"'"
                condition1 = condition1+"AND agency_details.town_code ='"+session.town_code+"'"

    dateRecords="select region as region,brand as brand,posm_code as posm_code,posm_type as posm_type,sum(c_qty) as c_qty FROM((select sm_town.region as region,alc_detail.brand as brand,alc_detail.posm_code as posm_code,alc_detail.posm_type as posm_type,sum(alc_detail.c_qty) as c_qty FROM alc_detail,sm_town where alc_detail.town_code=sm_town.town_code and alc_detail.posm_type='SHOPBOARD_NONLIT' "+condition+" GROUP BY sm_town.region,alc_detail.posm_type,alc_detail.brand) UNION (select sm_town.region as region,agency_details.brand as brand,agency_details.posm_code as posm_code,agency_details.posm_type as posm_type,sum(agency_details.usages_qty) as c_qty FROM agency_details,sm_town where agency_details.town_code=sm_town.town_code and agency_details.posm_type='SHOPBOARD_NONLIT' "+condition1+" GROUP BY sm_town.region,agency_details.posm_type,agency_details.brand)) abc GROUP BY region,posm_type,brand"
    recordList=db.executesql(dateRecords,as_dict = True)
    # return dateRecords

    return dict(recordList=recordList)

def mega_hanger():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    response.title = 'Mega Hanger'

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    #recCount=0
    # qset=db()
    # if session.town_code!='':
    #     if session.town_code!='ALL':
    #         if len(town_code)>1:
    #             qset = qset(db.alc_detail.town_code.belongs(townList))
    #         else:
    #             qset = qset(db.alc_detail.town_code==session.town_code)
    #
    # qset=qset(db.alc.id==db.alc_detail.alc_id)
    # qset=qset(db.alc_detail.town_code==db.sm_town.town_code)
    # qset=qset(db.alc.posm_type=='MEGA_HANGER')
    # #MEGA_HANGER
    # record = qset.select(db.sm_town.region,db.alc.posm_type,db.alc_detail.c_qty.sum(), groupby=db.alc.posm_type|db.alc.brand|db.sm_town.region, orderby=db.alc.brand)

    condition=''
    condition1=''
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                town=str(townList).replace("[","").replace("]","")#.replace("'","")
                condition = condition+"AND alc_detail.town_code in ("+str(town)+")"
                condition1 = condition1+"AND agency_details.town_code in ("+str(town)+")"
            else:
                condition = condition+"AND alc_detail.town_code ='"+session.town_code+"'"
                condition1 = condition1+"AND agency_details.town_code ='"+session.town_code+"'"

    dateRecords="select region as region,brand as brand,posm_code as posm_code,posm_type as posm_type,sum(c_qty) as c_qty FROM((select sm_town.region as region,alc_detail.brand as brand,alc_detail.posm_code as posm_code,alc_detail.posm_type as posm_type,sum(alc_detail.c_qty) as c_qty FROM alc_detail,sm_town where alc_detail.town_code=sm_town.town_code and alc_detail.posm_type='MEGA_HANGER' "+condition+" GROUP BY sm_town.region,alc_detail.posm_type,alc_detail.brand) UNION (select sm_town.region as region,agency_details.brand as brand,agency_details.posm_code as posm_code,agency_details.posm_type as posm_type,sum(agency_details.usages_qty) as c_qty FROM agency_details,sm_town where agency_details.town_code=sm_town.town_code and agency_details.posm_type='MEGA_HANGER' "+condition1+" GROUP BY sm_town.region,agency_details.posm_type,agency_details.brand)) abc GROUP BY region,posm_type,brand"
    recordList=db.executesql(dateRecords,as_dict = True)
    # return dateRecords

    return dict(recordList=recordList)

def plugin_dispenser():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    response.title = 'Plugin Dispenser'

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    #recCount=0
    # qset=db()
    # if session.town_code!='':
    #     if session.town_code!='ALL':
    #         if len(town_code)>1:
    #             qset = qset(db.alc_detail.town_code.belongs(townList))
    #         else:
    #             qset = qset(db.alc_detail.town_code==session.town_code)
    #
    # qset=qset(db.alc.id==db.alc_detail.alc_id)
    # qset=qset(db.alc_detail.town_code==db.sm_town.town_code)
    # qset=qset(db.alc.posm_type=='PLUGIN_DISPENSER')
    # #PLUGIN_DISPENSER
    # record = qset.select(db.sm_town.region,db.alc.brand,db.alc.posm_type,db.alc_detail.c_qty.sum(), groupby=db.alc.posm_type|db.alc.brand|db.sm_town.region, orderby=db.alc.brand)

    condition=''
    condition1=''
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                town=str(townList).replace("[","").replace("]","")#.replace("'","")
                condition = condition+"AND alc_detail.town_code in ("+str(town)+")"
                condition1 = condition1+"AND agency_details.town_code in ("+str(town)+")"
            else:
                condition = condition+"AND alc_detail.town_code ='"+session.town_code+"'"
                condition1 = condition1+"AND agency_details.town_code ='"+session.town_code+"'"

    dateRecords="select region as region,brand as brand,posm_code as posm_code,posm_type as posm_type,sum(c_qty) as c_qty FROM((select sm_town.region as region,alc_detail.brand as brand,alc_detail.posm_code as posm_code,alc_detail.posm_type as posm_type,sum(alc_detail.c_qty) as c_qty FROM alc_detail,sm_town where alc_detail.town_code=sm_town.town_code and alc_detail.posm_type='PLUGIN_DISPENSER' "+condition+" GROUP BY sm_town.region,alc_detail.posm_type,alc_detail.brand) UNION (select sm_town.region as region,agency_details.brand as brand,agency_details.posm_code as posm_code,agency_details.posm_type as posm_type,sum(agency_details.usages_qty) as c_qty FROM agency_details,sm_town where agency_details.town_code=sm_town.town_code and agency_details.posm_type='PLUGIN_DISPENSER' "+condition1+" GROUP BY sm_town.region,agency_details.posm_type,agency_details.brand)) abc GROUP BY region,posm_type,brand"
    recordList=db.executesql(dateRecords,as_dict = True)
    # return dateRecords

    return dict(recordList=recordList)

def mt_posm():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    response.title = 'MT POSM'

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])



    qset=db()
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code==session.town_code)

    qset=qset(db.alc.id==db.alc_detail.alc_id)
    qset=qset(db.alc_detail.town_code==db.sm_town.town_code)

    qset=qset(db.alc.posm_type.contains('MT_'))
    record = qset.select(db.sm_town.region,db.alc.brand,db.alc.posm_type,db.alc_detail.c_qty.sum(), groupby=db.alc.brand|db.sm_town.region, orderby=db.alc.brand)
    # return db._lastsql
    return dict(record=record)

def brand():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    brand_id=request.vars.brand_id
    reqPage = len(request.args)

    # --------paging
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)


    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    #recCount=0
    qset=db()
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code==session.town_code)


    qset=qset(db.alc_detail.posm_code == db.alc.posm_code)
    qset=qset(db.alc_detail.brand==brand_id)
    record = qset.select(db.alc_detail.brand, db.alc_detail.a_qty.sum(),db.alc_detail.due_qty.sum(), db.alc_detail.r_qty.sum(), db.alc_detail.c_qty.sum(), db.alc_detail.balance_qty.sum(), db.alc.posm_type,groupby=db.alc_detail.brand | db.alc.posm_type,orderby=~db.alc_detail.id)

    return dict(brand_id=brand_id,record=record,items_per_page=items_per_page,page=page)


def brand_details_download():
    if (session.user_id == '' or session.user_id == None):
        redirect(URL('index'))

    brand_id = request.vars.brand_id

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    # recCount=0
    qset = db()
    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code == session.town_code)

    qset = qset(db.alc_detail.posm_code == db.alc.posm_code)
    qset = qset(db.alc_detail.brand == brand_id)

    record = qset.select(db.alc_detail.brand, db.alc_detail.a_qty.sum(), db.alc_detail.due_qty.sum(),db.alc_detail.r_qty.sum(), db.alc_detail.c_qty.sum(), db.alc_detail.balance_qty.sum(),db.alc_detail.posm_type, groupby=db.alc_detail.brand | db.alc.posm_type, orderby=~db.alc_detail.id)

    myString='Brand :'+brand_id+'\n'
    myString += 'Brand,POSM Type,Allocation Qty,Due Qty,Receive Qty,Execution Qty,Balance Qty\n'
    for rec in record:
        brand = rec[db.alc_detail.brand]
        posm_type = rec[db.alc_detail.posm_type]
        a_qty = rec[db.alc_detail.a_qty.sum()]
        due_qty = rec[db.alc_detail.due_qty.sum()]
        r_qty = rec[db.alc_detail.r_qty.sum()]
        c_qty = rec[db.alc_detail.c_qty.sum()]
        balance_qty = rec[db.alc_detail.balance_qty.sum()]

        myString += str(brand)+','+str(posm_type)+','+str(a_qty)+','+str(due_qty)+','+str(r_qty)+','+str(c_qty)+','+str(balance_qty)+'\n'

    # -----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_Current_Activities_shop_sign.csv'
    return str(myString)

    return dict(recordList=recordList)



#========================================== Logout
def log_out():

    if (session.user_id == None):
        redirect(URL('index'))
    else:

        logRows=db(db.login_out_log.user_id==session.user_id).select(db.login_out_log.id,orderby=~db.login_out_log.log_in,limitby=(0,1))
        if logRows:
            logRows[0].update_record(log_out=datetime_fixed)

        session.clear()
        
        if ((session.cid == None) or (session.user_id == None)):
            redirect(URL('index'))
        else:
            db.rollback()
            redirect(URL('home'))


    return dict()



#============= Device user list
def get_device_user_list():
    retStr = ''
    cid = session.cid
    
    rows = db(db.banbeis_login_device.cid == cid).select(db.banbeis_login_device.user_id, orderby=db.banbeis_login_device.user_id, groupby=db.banbeis_login_device.user_id)
    for row in rows:
        user_id = str(row.user_id)        
        if retStr == '':
            retStr = user_id
        else:
            retStr += ',' + user_id
    return retStr


#============= Device name list
def get_device_name_list():
    retStr = ''
    cid = session.cid
    
    rows = db(db.banbeis_login_device.cid == cid).select(db.banbeis_login_device.device_name, orderby=db.banbeis_login_device.device_name, groupby=db.banbeis_login_device.device_name)
    for row in rows:
        device_name = str(row.device_name)        
        if retStr == '':
            retStr = device_name
        else:
            retStr += ',' + device_name
    return retStr




def admin_reports(): 
    task_id='userLogM'
    access_permission=check_role(task_id)
    if (access_permission==False):
        session.flash='Access is Denied'
        redirect (URL('default','home'))
        
    c_id=session.cid
    #----------
    response.title='User Log'
    #----------
    
    search_form =SQLFORM(db.banbeis_search_date)
        
    session.btn_login_report=''        
    session.from_date_rpt=''
    session.to_date_rpt=''
    
    userRows=''
    userRows=db(db.sm_user.cid==c_id).select(db.sm_user.user_id,db.sm_user.name,orderby=db.sm_user.user_id)
    
    return dict(message="Admin Reports",search_form=search_form,userRows=userRows)

def posm_archive():
    response.title = 'POSM Archive'
    monthName = request.vars.monthName
    currentYear = request.vars.currentYear

    currentMonth=str(datetime.datetime.strptime(currentYear+'-'+monthName+'-'+'01', "%Y-%b-%d"))[:7]

    #return archive_id
    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    qset=db()
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                qset(db.alc_detail.posm_code == db.alc.posm_code)
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset(db.alc_detail.posm_code == db.alc.posm_code)
                qset = qset(db.alc_detail.town_code==session.town_code)


    qset = db(db.alc.due_date[:7] == currentMonth)

    records = qset.select(db.alc.ALL, orderby=~db.alc.id)
    #return db._lastsql

    return dict(records=records,currentYear=currentYear,monthName=monthName)


def posm_archive_download():
    monthName = request.vars.monthName
    currentYear = request.vars.currentYear
    response.title = 'POSM Archive'
    #return monthName
    currentMonth = str(datetime.datetime.strptime(currentYear + '-' + monthName + '-' + '01', "%Y-%b-%d"))[:7]

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    # recCount=0
    qset = db()
    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code == session.town_code)

    qset = db(db.alc.due_date[:7] == currentMonth)

    records = qset.select(db.alc.ALL, orderby=~db.alc.id)

    myString='POSM Archive List\n'
    myString += 'POSM Code,POSM Type,Brand,Agency_Code,Agency_Name \n'
    for rec in records:
        agencyName = ''
        posm_code = rec[db.alc.posm_code]
        posm_type = rec[db.alc.posm_type]
        brand = rec[db.alc.brand]
        agency_code = rec[db.alc.agency]

        agency_name = db(db.agency.agency_code == agency_code).select(db.agency.agency_name)
        if agency_name:
            agencyName = agency_name[0].agency_name


        myString += str(posm_code)+','+str(posm_type)+','+str(brand)+','+str(agency_code)+','+str(agencyName)+'\n'

    # -----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_POSM_Archive.csv'
    return str(myString)

    return dict(recordList=recordList)

def posm_archive_details():

    response.title = 'POSM Archive Details'
    monthName = request.vars.monthName
    currentYear = request.vars.currentYear
    posm_code=request.vars.posm_code

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    #recCount=0
    qset=db()
    if session.town_code!='':
        if session.town_code!='ALL':
            if len(town_code)>1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code==session.town_code)

    qset=qset(db.alc_detail.posm_code==posm_code)
    qset = qset(db.alc_detail.posm_code==db.alc.posm_code)
    records = qset.select(db.alc_detail.ALL,db.alc.ALL, orderby=~db.alc_detail.id)

    return dict(records=records,currentYear=currentYear,monthName=monthName,posm_code=posm_code)

def posm_archive_details_download():
    monthName = request.vars.monthName
    currentYear = request.vars.currentYear
    posm_code = request.vars.posm_code
    #return posm_code
    response.title = 'POSM Archive'

    currentMonth = str(datetime.datetime.strptime(currentYear + '-' + monthName + '-' + '01', "%Y-%b-%d"))[:7]

    townList = []
    town_code = str(session.town_code)[1:-1].split('|')
    if len(town_code) > 1:
        for i in range(len(town_code)):
            townList.append(town_code[i])

    # recCount=0
    qset = db()
    if session.town_code != '':
        if session.town_code != 'ALL':
            if len(town_code) > 1:
                qset = qset(db.alc_detail.town_code.belongs(townList))
            else:
                qset = qset(db.alc_detail.town_code == session.town_code)

    qset = qset(db.alc_detail.posm_code == posm_code)

    records = qset.select(db.alc_detail.ALL, orderby=~db.alc_detail.id)

    myString='POSM Archive Details\n'
    myString += 'POSM Code,POSM Type,Brand,Town Code,Town Name,Allocation_Qty,Due_Qty,Receive_Qty,Defective_Qty,Execution_Qty,Balance_Qty \n'
    for rec in records:

        posm_code = rec[db.alc_detail.posm_code]
        posm_type = rec[db.alc_detail.posm_type]
        brand = rec[db.alc_detail.brand]
        town_code = rec[db.alc_detail.town_code]
        town_name = rec[db.alc_detail.town_name]
        allocation_qty = rec[db.alc_detail.a_qty]
        due_qty = rec[db.alc_detail.due_qty]
        receive = rec[db.alc_detail.r_qty]
        defective_qty = rec[db.alc_detail.defective_qty]
        usage = rec[db.alc_detail.c_qty]
        balance_qty = rec[db.alc_detail.balance_qty]

        myString += str(posm_code)+','+str(posm_type)+','+str(brand)+','+str(town_code)+','+str(town_name)+','+str(allocation_qty)+','+str(due_qty)+','+str(receive)+','+str(defective_qty)+','+str(usage)+','+str(balance_qty)+'\n'

    # -----------
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_POSM_Archive_Details.csv'
    return str(myString)
    # return dict(recordList=recordList)


def clear_filter():
    session.btn_filter=None
    session.searchType=None
    session.ftrRef=None
    session.searchValue=None        
    session.rec_status=None
    return 'ok'


