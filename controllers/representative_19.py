def rep():
    response.title = 'Representative'
    submit = request.vars.submit
    btn_filter_rep=request.vars.btn_filter_rep
    rep_id_filter = request.vars.rep_id_filter
    btn_all=request.vars.btn_all
    c_id = session.cid
    condition=''
    # return submit
    page = request.vars.page_no
    if page == '' or page == 'None' or page == None:
        page = 1
    page_limit = 20
    page_no = int(page)
    start_index =(page_no-1)*page_limit
    if submit:
        rep_id = request.vars.rep_id
        name = request.vars.name
        mobile_no = request.vars.mobile
        user_type = request.vars.user_type
        designation = request.vars.designation
        password = request.vars.password
        status = request.vars.status
        # return rep_id
        if rep_id=='' or rep_id=="None" or rep_id==None:
            # return 10
            response.flash = 'Required Rep ID'
        else:
            check_rep_sql = "select * from sm_rep where cid='"+str(c_id)+"'and rep_id='"+str(rep_id)+"' and user_type='rep';"
            # return check_rep_sql
            check_rep = db.executesql(check_rep_sql, as_dict=True)
            # return 10
            if len(check_rep)>0:
                response.flash = 'Rep id already exists'
                # return 11
            else:
                # return 12
                insert_rep_sql="INSERT INTO sm_rep (cid,rep_id,name,mobile_no,user_type,designation,password,status) VALUES ('"+str(c_id)+"','"+str(rep_id)+"','"+str(name)+"','"+str(mobile_no)+"','"+str(user_type)+"','"+str(designation)+"','"+str(password)+"','"+str(status)+"'); "
                insert_rep=db.executesql(insert_rep_sql)
                response.flash='Representative insert successfully!'
                # return insert_rep_sql

    if btn_filter_rep == "Filter":
        # return 10
        if rep_id_filter !='':
            # return 11
            session.rep_id_filter = rep_id_filter
            rep_id_filter = str(rep_id_filter).split('|')[0]
            condition = condition + " and rep_id = '"+str(rep_id_filter)+"'"
            # return condition
    if btn_all == "All":
        # return 22
        condition = ''
        session.rep_id_filter = ''

    repRows_sql = "select * from sm_rep where cid = '"+str(c_id)+"' "+condition+" and user_type='rep' limit "+str(start_index)+","+str(page_limit)+";"
    repRows = db.executesql(repRows_sql, as_dict=True)
    session.condition = condition
    # return 22

    # total_record_sql = f"SELECT COUNT(id) AS total FROM sm_rep WHERE cid='GULF' {condition} ORDER BY id ASC;"
    # total_record = db.executesql(total_record_sql, as_dict = True)
    # total_rec = total_record[0]['total']
  
    return dict(repRows=repRows,page=page)

def get_rep_id_list():
    c_id = session.cid
    retStr = ''

    replistRows_sql = "select rep_id,name from sm_rep where cid = '"+c_id+"';"
    replistRows = db.executesql(replistRows_sql, as_dict=True)

    for i in range(len(replistRows)):
        rep_list_dict=replistRows[i]   
        rep_id=str(rep_list_dict["rep_id"])
        name=str(rep_list_dict["name"])   
        if retStr == '':
            retStr = rep_id+'|'+name
        else:
            retStr += ',' + rep_id+'|'+name
    
    return retStr


def rep_Download():
    c_id = session.cid 
    condition=session.condition
    download_sql = "select * from sm_rep where cid = '"+str(c_id)+"' "+condition+";"
    download_records = db.executesql(download_sql, as_dict=True)
    
    myString = 'Representative \n\n'
    myString += 'Rep ID,Rep Name,Mobile no,Designation,Password,Status\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len( download_records)):
        recordsStr =  download_records[i]
        rep_id=str(recordsStr["rep_id"])
        name=str(recordsStr["name"])
        mobile_no=str(recordsStr["mobile_no"])
        designation=str(recordsStr["designation"])
        password=str(recordsStr["password"])
        status=str(recordsStr["status"])

        myString += str(rep_id) + ',' + str(name) + ',' + str(mobile_no) + ',' + str(designation) + ',' + str(password) + ',' + str(status) +'\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_Rep.csv'
    return str(myString)



def representative_batch_upload():
    response.title = 'Representative Batch Upload'
    c_id = session.cid
    btn_upload = request.vars.btn_upload
    count_inserted = 0
    count_error = 0
    error_str = ''
    total_row = 0
    slNo = 0
    # return slNo
    if btn_upload == 'Upload':
        excel_data = str(request.vars.excel_data)
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)

        rep_id_list_excel = []

        valid_rep_id_list = []
        excelList = []

        ins_list = []
        ins_dict = {}
        # return total_row
        for i in range(total_row):
            # return 10
            if i >= 1000:
                # return 101
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 6:
                    rep_id_list_excel.append(str(coloum_list[0]).strip().upper())

        # create list
        for i in range(total_row):
            if i >= 1000:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')

            if len(coloum_list) != 6:
                error_data = row_data + '(6 columns need in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue
            else:

                repToId_excel = str(coloum_list[0]).strip()
                name_excel = str(coloum_list[1]).strip()
                mobileNo_excel = str(coloum_list[2]).strip()
                designation_excel = str(coloum_list[3]).strip()
                password_excel = str(coloum_list[4]).strip()
                status_excel = str(coloum_list[5]).strip()
                # return status_excel

                if (repToId_excel==''or repToId_excel == 'NONE') and (name_excel=='' or name_excel== 'NONE') and (mobileNo_excel=='' or mobileNo_excel == 'NONE') and (designation_excel=='' or designation_excel == 'NONE') and (password_excel=='' or password_excel== 'NONE'):
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue 
                else:
                    existCheckRows= " SELECT * FROM sm_rep WHERE cid='"+str(c_id)+"' and rep_id = '"+repToId_excel+"';"
                    # return existCheckRows
                    existCheck = db.executesql(existCheckRows)
                    # return existCheck

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate User!!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        try:
                            insert_sql = "INSERT INTO sm_rep (cid,rep_id,name,mobile_no,designation,password,status) VALUES ('"+str(c_id)+"','"+str(repToId_excel)+"','"+str(name_excel)+"', '"+str(mobileNo_excel)+"','"+str(designation_excel)+"','"+str(password_excel)+"','"+str(status_excel)+"');"
                            # return insert_sql
                            update_ff_list = db.executesql(insert_sql)
                            # return update_ff_list
                            count_inserted+=1
                        except Exception as e:
                            error_str = 'Please do not insert special charachter.'
                            # return error_str


        if error_str == '':
            error_str = 'No error'

    return dict(count_inserted=count_inserted, count_error=count_error, error_str=error_str, total_row=total_row)


#=========REPRESENTATIVE EDIT & DELETE=======
def rep_edit():
    # return 'flhj'
    rep_id =request.args(0)
    
    update_btn = request.vars.update_btn
    delete_btn = request.vars.delete_btn

    select_rep_record_sql = f"SELECT * FROM sm_rep WHERE rep_id ='"+str(rep_id)+"' GROUP BY rep_id LIMIT 1;"
    # return select_ret_record_sql
    selected_rep_record = db.executesql(select_rep_record_sql, as_dict = True)

    # if len(selected_ret_record) != 0 :
    for i in range(len(selected_rep_record)):
        ret = selected_rep_record[i]
        rowId = str(ret["id"])
        rep_id = str(ret["rep_id"])
        name = str(ret["name"])
        mobile_no = str(ret["mobile_no"])
        designation = str(ret["designation"])
        password = str(ret["password"])
        status = str(ret["status"])
    
    if update_btn:
        name_up = str(request.vars.name)
        mobile_no_up = str(request.vars.mobile_no)
        designation_up = str(request.vars.designation)
        password_up = str(request.vars.password)
        status_up = str(request.vars.status)  

        update_sql = f"UPDATE sm_rep SET name = '{str(name_up)}',  mobile_no = '{str(mobile_no_up)}', designation = '{str(designation_up)}', password = '{str(password_up)}', status = '{str(status_up)}' WHERE rep_id = '"+str(rep_id)+"' LIMIT 1;"
        up_date = db.executesql(update_sql)

        session.flash = 'Update Successfully!'

        redirect(URL('representative','rep'))

    if delete_btn:
        delete_sql = f"DELETE FROM sm_rep WHERE rep_id='{rep_id}' LIMIT 1;"
        delete = db.executesql(delete_sql)

        session.flash = 'Deleted Successfully!'

        redirect(URL('representative','rep'))
            
    return dict(rep_id=rep_id,name=name,mobile_no=mobile_no,designation=designation,password=password,status=status)
    


# ----------------------------------------------------
def rep_area_validation(form):
    
    rep_id=str(request.vars.rep_id).strip().upper().split('|')[0]
    area_id=str(request.vars.area_id).strip().upper().split('|')[0]
    rep_category=str(request.vars.rep_category).strip().upper()
    
    if ((rep_id!='') and (area_id!='') and (session.cid!='')):
        check_rep=db((db.sm_rep.cid==session.cid) & (db.sm_rep.rep_id==rep_id) & (db.sm_rep.user_type=='rep')).select(db.sm_rep.id,db.sm_rep.rep_id,db.sm_rep.name,limitby=(0,1))
        
        if check_rep:
            rep_name=check_rep[0].name
            
            area_name=''
            if session.user_type=='Depot':
                check_area=db((db.sm_level.cid==session.cid) & (db.sm_level.depot_id==session.depot_id) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.level_id,db.sm_level.level_name,limitby=(0,1))
            else:
                check_area=db((db.sm_level.cid==session.cid) & (db.sm_level.level_id==area_id) & (db.sm_level.is_leaf == '1') ).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depot_id,limitby=(0,1))
            
            if check_area:
                area_name=check_area[0].level_name
                
                rows_check=db((db.sm_rep_area.cid==session.cid) & (db.sm_rep_area.rep_id==rep_id) & (db.sm_rep_area.area_id==area_id)).select(db.sm_rep_area.rep_id,limitby=(0,1))
                if rows_check:
                    form.errors.rep_id=''
                    response.flash = 'please choose a new '
                else:
                    form.vars.rep_id=rep_id
                    form.vars.rep_name=rep_name
                    
                    form.vars.area_id=area_id
                    form.vars.area_name=area_name                    
            else:
                form.errors.area_id=''
                response.flash = 'Invalid Market/Route '
        else:
            form.errors.rep_id=''
            response.flash = 'Invalid Rep '
    else:
        form.errors.rep_id=''
        response.flash = 'enter accurate value '
def rep_area():
    task_id='rm_reparea_manage'
    task_id_view='rm_reparea_view'
    # access_permission=check_role(task_id)
    # access_permission_view=check_role(task_id_view)
    
    # if (access_permission==False) and (access_permission_view==False):
    #     session.flash='Access is Denied !'
    #     redirect (URL('default','home'))
    
    response.title='Rep-Market'
    c_id=session.cid
    
    form =SQLFORM(db.sm_rep_area,
                  fields=['rep_id','area_id','rep_category'],
                  submit_button='Save'         
                  )

    #=== general territory list for special territory
    rep_id = str(request.vars.rep_id).strip().upper().split('|')[0]
    area_id = str(request.vars.area_id).strip().upper().split('|')[0]
    rep_category = str(request.vars.rep_category).strip().upper()
    ins_list = []

    general_area_list = []
    check_rep = db((db.sm_rep.cid == session.cid) & (db.sm_rep.rep_id == rep_id) & (db.sm_rep.user_type == 'rep')).select(db.sm_rep.id, db.sm_rep.rep_id, db.sm_rep.name, limitby=(0, 1))

    if check_rep:
        rep_name = check_rep[0].name

        checkSpTrRow = db((db.sm_level.cid == session.cid) & (db.sm_level.level_id != area_id) & (db.sm_level.special_territory_code == area_id) & (db.sm_level.is_leaf == '1') & (db.sm_level.depth == 3)).select(db.sm_level.level_id, db.sm_level.level_name,db.sm_level.depot_id)

        for sRow in checkSpTrRow:
            general_area_id = str(sRow.level_id)
            general_area_name = str(sRow.level_name)
            general_depot_id = str(sRow.depot_id)

            ins_dict = {'cid': session.cid, 'rep_id': rep_id, 'rep_name': rep_name, 'rep_category': rep_category, 'area_id': general_area_id,'area_name': general_area_name, 'depot_id': general_depot_id}
            ins_list.append(ins_dict)

            general_area_list.append(sRow.level_id)



    #Insert with validation
    if form.accepts(request.vars,session,onvalidation=rep_area_validation):
        if len(general_area_list)>0:
            deleteSql=db((db.sm_rep_area.cid == session.cid) & (db.sm_rep_area.rep_id == rep_id) & (db.sm_rep_area.area_id.belongs(general_area_list))).delete()

            if deleteSql:
                db.sm_rep_area.bulk_insert(ins_list)


        response.flash = 'Submitted Successfully'

    #----------delete rep area---
    btn_delete=request.vars.btn_delete    
    if btn_delete:
        id_delete=request.vars.record_id

        # ----------------
        recList = []
        sql = "SELECT GROUP_CONCAT(`rep_id`,',', `rep_name`,',', `rep_category`,',', `area_id`,',', `area_name`,',', `depot_id`,',', `field1`,',', `field2`,',', `note`,',', `created_on`,',', `created_by`,',', `updated_on`,',', `updated_by`) as description FROM sm_rep_area WHERE id='" + id_delete + "';"
        recList = db.executesql(sql, as_dict=True)
        desc = ''
        for i in range(len(recList)):
            recStr = recList[i]
            desc = str(recStr['description'])

        tblName = 'sm_rep_area'
        refId = id_delete

        insert_log(tblName, refId, desc)
        # ------------

        db((db.sm_rep_area.id == id_delete)).delete()
        response.flash = 'Update Successfully'
    
    #------------------------
    btn_filter_rep_area=request.vars.btn_filter
    btn_rep_area_all=request.vars.btn_rep_area_all
    if btn_filter_rep_area:
        session.btn_filter_rep_area=btn_filter_rep_area
        
        session.search_type_reparea=request.vars.search_type
        session.search_value_reparea=str(request.vars.search_value).strip()
        
    elif btn_rep_area_all:
        session.btn_filter_rep_area=None
        session.search_type_reparea=None
        session.search_value_reparea=None

    #--------paging
    if len(request.args):
        page=int(request.args[0])
    else:
        page=0
    items_per_page=session.items_per_page
    limitby=(page*items_per_page,(page+1)*items_per_page+1)
    #--------end paging    
    
    qset=db()
    qset=qset(db.sm_rep_area.cid==c_id)   
    
#     if session.user_type=='Depot':
#         qset=qset(db.sm_rep_area.depot_id==session.depot_id)
#     else:
#         if (session.btn_filter_rep_area and session.search_type_reparea=='DepotID'):
#             searchValue=str(session.search_value_reparea).split('|')[0]
#             qset=qset(db.sm_rep_area.depot_id==searchValue)
    
    #---- supervisor
    if session.user_type=='Supervisor':
        qset=qset(db.sm_rep_area.area_id.belongs(session.marketList))        
    else:
        pass
    
    if (session.btn_filter_rep_area and session.search_type_reparea=='RepID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_rep_area.rep_id==searchValue)
        
    elif (session.btn_filter_rep_area and session.search_type_reparea=='AreaID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_rep_area.area_id==searchValue)
        
    elif (session.btn_filter_rep_area and session.search_type_reparea=='CategoryID'):
        searchValue=str(session.search_value_reparea).split('|')[0]
        qset=qset(db.sm_rep_area.rep_category==searchValue)
        
    records=qset.select(db.sm_rep_area.ALL,orderby=db.sm_rep_area.rep_name|db.sm_rep_area.area_name,limitby=limitby)
    totalCount=qset.count()
    
    return dict(form=form,records=records,totalCount=totalCount,page=page,items_per_page=items_per_page)
#---------------end  rep_area-----------------------


#====================================== REP AREA BATCH UPLOAD ---------- 
def area_batch_upload():#Rep area batch upload
    response.title='Rep-Market Batch upload'
    c_id=session.cid
    if (c_id=='' or c_id==None):
        redirect(URL('default','index'))
    
    #Check access permission
#----------Task assaign----------
#     task_id='rm_reparea_manage'
#     task_id_view='rm_reparea_view'
#     access_permission=check_role(task_id)
# #    access_permission_view=check_role(task_id_view)

#     if access_permission==False:
#         session.flash='Access is Denied !'
#         redirect (URL('representative','rep'))
        
#   ---------------------  
    btn_upload=request.vars.btn_upload    
    count_inserted=0
    count_error=0
    error_str=''
    total_row=0
    if btn_upload=='Upload':        
        excel_data=str(request.vars.excel_data)
        inserted_count=0
        error_count=0
        error_list=[]
        row_list=excel_data.split( '\n')
        total_row=len(row_list)
        
        rep_list_excel=[]
        rep_area_list_exist=[]
        rep_list_exist=[]
        
        
        area_list_excel=[]
        existLevel_list=[]
        
        ins_list=[]
        ins_dict={}
        
        duplicateExcelList=[]
        
#   ----------------------
        #---------- rep area
        for i in range(total_row):
            if i>=100:
                break
            else:
                row_data=row_list[i]                    
                coloum_list=row_data.split( '\t')
                if len(coloum_list)==3:
                    rep_list_excel.append(str(coloum_list[0]).strip().upper())
                    area_list_excel.append(str(coloum_list[1]).strip().upper())
        
        #Create list of rep already exist in rep area table based on excel sheet
        existRepRows=db((db.sm_rep_area.cid==c_id)&(db.sm_rep_area.rep_id.belongs(rep_list_excel))).select(db.sm_rep_area.rep_id,db.sm_rep_area.area_id,orderby=db.sm_rep_area.rep_id)
        rep_area_list_exist=existRepRows.as_list()
        
        #---------- valid rep list based onexcel sheet                           
        repRows=db((db.sm_rep.cid==c_id)&(db.sm_rep.user_type=='rep')&(db.sm_rep.rep_id.belongs(rep_list_excel))).select(db.sm_rep.rep_id,db.sm_rep.name)
        rep_list_exist=repRows.as_list()
        
        #-------valid area(level) list based onexcel sheet
        if session.user_type=='Depot':
            existLevelRows=db((db.sm_level.cid==c_id) & (db.sm_level.depot_id==session.depot_id)&(db.sm_level.is_leaf=='1')&(db.sm_level.level_id.belongs(area_list_excel))).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depot_id,orderby=db.sm_level.level_id)
        else:
            existLevelRows=db((db.sm_level.cid==c_id) &(db.sm_level.is_leaf=='1')&(db.sm_level.level_id.belongs(area_list_excel))).select(db.sm_level.level_id,db.sm_level.level_name,db.sm_level.depot_id,orderby=db.sm_level.level_id)
        existLevel_list=existLevelRows.as_list()
        
#   --------------------     
        for i in range(total_row):
            if i>=100: 
                break
            else:
                row_data=row_list[i]
            coloum_list=row_data.split( '\t')            

            if len(coloum_list)==3:
                repID_excel=str(coloum_list[0]).strip().upper()
                areaID_excel=str(coloum_list[1]).strip().upper()
                rep_category=str(coloum_list[2]).strip().upper()
                
                try:      
                    valid_rep=False
                    duplicate_rep_area=False
                    valid_level=False  
                    valid_depot=True
                    valid_category=True
                    depotID=''
                    #----------- check valid rep                          
                    for i in range(len(rep_list_exist)):
                        myRowData=rep_list_exist[i]                                
                        rep_id=myRowData['rep_id']
                        rep_name=myRowData['name']                        
                        if (str(rep_id).strip()==str(repID_excel).strip()):
                            valid_rep=True
                            break
                    
                    #----------- check duplicate rep-area   
                    if valid_rep==True:                                                       
                        #Get area of exist rep and check duplicate of rep area 
                        for i in range(len(rep_area_list_exist)):
                            myRowData=rep_area_list_exist[i]                                
                            rep_id_exist=myRowData['rep_id']
                            area_id=myRowData['area_id']
                            if ((str(rep_id_exist).strip()==str(repID_excel).strip())and (str(area_id).strip()==str(areaID_excel).strip())):
                                duplicate_rep_area=True
                                break
                        
                        if duplicate_rep_area==False:#---------- check valid level/depot                                                
                            for i in range(len(existLevel_list)):
                                myRowData=existLevel_list[i]                                
                                level_id=myRowData['level_id']
                                level_name=myRowData['level_name']
                                if (str(level_id).strip()==str(areaID_excel).strip()):                                                                        
                                    valid_level=True                                    
                                    break
                    
                    if valid_level==True:
                        if rep_category not in ['A','B','C']:
                            valid_category=False
                    
                    #-----------------
                    if valid_rep==True:
                        if(duplicate_rep_area==False):                             
                            if valid_level==True:
                                #Create list for bulk insert
                                if valid_category==True:
                                    
                                    repMarket=repID_excel+'-'+areaID_excel
                                    
                                    if repMarket not in duplicateExcelList:
                                        duplicateExcelList.append(repMarket)
                                        
                                        ins_dict= {'cid':c_id,'rep_id':repID_excel,'rep_name':rep_name,'rep_category':rep_category,'area_id':areaID_excel,'area_name':level_name}
                                        ins_list.append(ins_dict)
                                        count_inserted+=1
                                        
                                    else:
                                        error_data=row_data+'(duplicate in excel!)\n'
                                        error_str=error_str+error_data
                                        count_error+=1
                                        continue  
                                        
                                else:
                                    error_data=row_data+'(invalid category!)\n'
                                    error_str=error_str+error_data
                                    count_error+=1
                                    continue                            
                            else:
                                error_data=row_data+'(invalid territory/Route!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                        else:
                            error_data=row_data+'(duplicate mso-territory)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                    else:
                        error_data=row_data+'(Invalid MSO ID!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue

                except:
                    error_data=row_data+'(error in process!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue
            else:
                error_data=row_data+'(3 columns need in a row)\n'
                error_str=error_str+error_data
                count_error+=1
                continue
        
        if error_str=='':
            error_str='No error'
        
        if len(ins_list) > 0:
            inCountList=db.sm_rep_area.bulk_insert(ins_list)             
     
        
        return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)        
    
    return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)