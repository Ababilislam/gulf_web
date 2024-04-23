def sup():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    # return dict()
    # return rep_id
    response.title = 'Supervisor'
    submit = request.vars.submit
    btn_filter_rep=request.vars.btn_filter_rep
    rep_id_filter = request.vars.rep_id_filter
    btn_all=request.vars.btn_all
    c_id = session.cid
    condition=''
    # return submit
    reqPage = len(request.args)
    if submit:
        # return rep_id
        rep_id = request.vars.rep_id
        name = request.vars.name
        mobile_no = request.vars.mobile
        designation = request.vars.designation
        password = request.vars.password
        # user_type= request.vars.user_type
        status = request.vars.status
        # return rep_id
        if rep_id=='' or rep_id==None :

            response.flash='Sup Id required'
        else :
            # return rep_id
            # return 10
            check_rep_sql = "select * from sm_rep where cid='"+str(c_id)+"'and rep_id='"+str(rep_id)+"' ;"
            # return check_rep_sql
            check_rep = db.executesql(check_rep_sql, as_dict=True)
            # return 10
            if len(check_rep)>0:
                response.flash = 'Sup id already exists'
                # return 11
            else:
                # return 12
                insert_rep_sql="INSERT INTO sm_rep (cid,rep_id,name,mobile_no,designation,password,status,user_type) VALUES ('"+str(c_id)+"','"+str(rep_id)+"','"+str(name)+"','"+str(mobile_no)+"','"+str(designation)+"','"+str(password)+"','"+str(status)+"','sup'); "
                insert_rep=db.executesql(insert_rep_sql)
                response.flash='Supervisor insert successfully!'
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

    # --------paging
    session.sup_per_page = 20
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    sup_per_page = session.sup_per_page
    limitby = (page * sup_per_page, (page + 1) * sup_per_page + 1)
    # return limitby
    # --------end paging

    supRows_sql = "select * from sm_rep where cid = '"+str(c_id)+"' and user_type = 'sup' "+condition+" limit %d, %d;" % limitby
    supRows = db.executesql(supRows_sql, as_dict=True)
   
    session.condition = condition
   
  
    return dict(supRows=supRows,page=page,sup_per_page=sup_per_page)


def sup_Download():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid 
    condition=session.condition
    download_sql = "select * from sm_rep where cid = '"+str(c_id)+"' and user_type = 'sup' "+condition+";"
    download_records = db.executesql(download_sql, as_dict=True)
    
    myString = 'Supervisor \n\n'
    myString += 'Sup ID,Sup Name,Mobile no,Designation,Password,Status\n'
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
    response.headers['Content-disposition'] = 'attachment; filename=download_Sup.csv'
    return str(myString)



def supervisor_batch_upload():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title = 'Supervisor Batch Upload'
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
                # user_type_excel=str(coloum_list[6]).strip()
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
                            insert_sql = "INSERT INTO sm_rep (cid,rep_id,name,mobile_no,designation,password,status,user_type) VALUES ('"+str(c_id)+"','"+str(repToId_excel)+"','"+str(name_excel)+"', '"+str(mobileNo_excel)+"','"+str(designation_excel)+"','"+str(password_excel)+"','"+str(status_excel)+"','sup');"
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


# #=========REPRESENTATIVE EDIT & DELETE=======
def sup_edit():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
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

        redirect(URL('supervisor','sup'))

    if delete_btn:
        delete_sql = f"DELETE FROM sm_rep WHERE rep_id='{rep_id}' LIMIT 1;"
        delete = db.executesql(delete_sql)

        session.flash = 'Deleted Successfully!'

        redirect(URL('supervisor','sup'))
            
    return dict(rep_id=rep_id,name=name,mobile_no=mobile_no,designation=designation,password=password,status=status)
#     