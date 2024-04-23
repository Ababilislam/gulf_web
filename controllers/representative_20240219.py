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
    