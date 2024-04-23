def client():#===========my====
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title='Retailer'

    btn_filter_client=request.vars.btn_filter_client
    btn_all=request.vars.btn_all
    c_id=session.cid
    condition = ''
    reqPage = len(request.args)
    # return condition
    if btn_filter_client == "Filter":
        client_id_filter = request.vars.client_id_filter
        dist_id_filter = request.vars.dist_id_filter
        district_id_filter = request.vars.district_id_filter
        tagPerson_filter = request.vars.tagPerson_filter
        approved_filter = request.vars.approved_filter
        
        condition = ''  

        if client_id_filter != '':
            session.client_id_filter = client_id_filter
            try:
                client_id_filter = str(client_id_filter).split('|')[0]
            except:
                session.client_id_filter = ''
            condition = condition + " and client_id = '"+str(client_id_filter)+"'"
        # return condition

        if dist_id_filter != '':
            session.dist_id_filter = dist_id_filter
            try:
                dist_id_filter = str(dist_id_filter).split('|')[0]
            except:
                session.dist_id_filter = ''
            condition = condition + " and area_id = '"+str(dist_id_filter)+"'"

        if district_id_filter != '':
            session.district_id_filter = district_id_filter
            try:
                district_id_filter = str(district_id_filter).split('|')[0]
            except:
                session.district_id_filter=''
            condition = condition + " and district_id = '"+str(district_id_filter)+"'"

        if tagPerson_filter:
            session.tagPerson_filter = tagPerson_filter
            try:
                tagPerson_filter = str(tagPerson_filter).split('|')[0]
            except:
                session.tagPerson_filter =''
            condition += " AND EXISTS (SELECT 1 FROM rep_client rc WHERE rc.client_id = sm_client.client_id AND rc.rep_id = '" + str(tagPerson_filter) + "')"

        if approved_filter != '':
            session.approved_filter = approved_filter
            try:
                approved_filter = str(approved_filter).split('|')[0]
            except:
                session.approved_filter =''
            condition = condition + " and approved_by_sup = '"+str(approved_filter)+"'"
        # return condition
        reqPage=0
        session.client_condition = condition

    if btn_all == "All":
        condition = '' 
        session.client_id_filter = ''
        session.dist_id_filter = ''
        session.district_id_filter = ''
        session.tagPerson_filter = ''
        session.approved_filter = ''
        session.client_condition = condition
        reqPage=0

    # return condition
    #--------paging
    session.clients_per_page = 20
    if reqPage:
        page=int(request.args[0])
    else:
        page=0
    clients_per_page=session.clients_per_page
    limitby=(page*clients_per_page,(page+1)*clients_per_page+1)
    #--------end paging
    
    update_btn=request.vars.update_btn
    if update_btn:
        # return 'fhmn'
        client_id= request.vars.client_id
        update_reset_sql= 'Update sm_client Set latitude="0", longitude="0", approved_by_sup="NO" where client_id="'+str(client_id)+'";'  
        update_reset = db.executesql(update_reset_sql)
        session.flash = 'Reset successfully!'
        redirect(URL('customer','client'))

    condition=session.client_condition
    if condition==None or condition=='None':
        condition=''
    # return condition
    clientRows_sql = "select * from sm_client where cid = '"+str(c_id)+"' "+condition+" ORDER BY id DESC limit %d, %d;" % limitby
    clientRows = db.executesql(clientRows_sql, as_dict=True)
    # session.condition=condition

    total_record_sql = f"SELECT COUNT(id) AS total FROM sm_client WHERE cid='GULF' {condition} ORDER BY id ASC;"
    total_record = db.executesql(total_record_sql, as_dict = True)
    total_rec = total_record[0]['total']
    # return total_rec
    # total_rec=10

    return dict(clientRows=clientRows,total_rec=total_rec,page=page,clients_per_page=clients_per_page)


#=========Auto Complete=======
def get_client_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    clientlistRows_sql = "select client_id,name,district_id,district from sm_client where cid = '"+c_id+"' group by client_id;"
    clientlistRows = db.executesql(clientlistRows_sql, as_dict=True)

    for i in range(len(clientlistRows)):
        client_list_dict=clientlistRows[i]   
        client_id=str(client_list_dict["client_id"])
        name=str(client_list_dict["name"])
        if retStr == '':
            retStr = client_id+'|'+name
        else:
            retStr += ',' + client_id+'|'+name
    
    return retStr

def get_district_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    clientlistRows_sql = "select district_id,district from sm_client where cid = '"+c_id+"' group by district_id;"
    clientlistRows = db.executesql(clientlistRows_sql, as_dict=True)

    for i in range(len(clientlistRows)):
        client_list_dict=clientlistRows[i]   
        district_id=str(client_list_dict["district_id"])
        district=str(client_list_dict["district"])
        if retStr == '':
            retStr = district_id+'|'+district
        else:
            retStr += ',' + district_id+'|'+district
    
    return retStr

def get_dist_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    distributorRecords_sql = "select level_id,level_name from sm_level where cid='"+ str(c_id) +"' and is_leaf='1' group by level_id;"
    # return distributorRecords_sql
    distributorRows = db.executesql(distributorRecords_sql, as_dict=True)
    for i in range(len(distributorRows)):
        records_dict=distributorRows[i]
        distributor_id=str(records_dict["level_id"])
        distributor_name=str(records_dict["level_name"])
        if retStr == '':
            retStr = distributor_id+'|'+distributor_name
        else:
            retStr += ',' + distributor_id+'|'+distributor_name
    
    return retStr

def get_tagPerson_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    tagPersonRecords_sql = "select rep_id,name from rep_client where cid='"+ str(c_id) +"' group by rep_id;"
    # return distributorRecords_sql
    tagPersonRows = db.executesql(tagPersonRecords_sql, as_dict=True)
    for i in range(len(tagPersonRows)):
        records_dict=tagPersonRows[i]
        rep_id=str(records_dict["rep_id"])
        rep_name=str(records_dict["name"])
        if retStr == '':
            retStr = rep_id+'|'+rep_name
        else:
            retStr += ',' + rep_id+'|'+rep_name
    
    return retStr
#============


#========CLIENT ADD========
def client_add():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title='Retailer'
    submit=request.vars.submit
    c_id=session.cid
    # return c_id
    if submit:
        client_id =request.vars.client_id
        name =request.vars.name
        distributor_id =request.vars.distributor_id
        distributor_name =request.vars.distributor_name
        status =request.vars.status
        # segment =request.vars.segment
        # distributor_rep =request.vars.distributor_rep
        # distributor_emp_id =request.vars.distributor_emp_id
        balance =request.vars.balance
        credit_limit =request.vars.credit_limit
        credit_duration =request.vars.credit_duration
        customer_type =request.vars.customer_type
        payment_mode =request.vars.payment_mode
        bank_account_no =request.vars.bank_account_no
        address =request.vars.address
        # woner_name =request.vars.woner_name
        contact_no1 =request.vars.contact_no1
        nid =request.vars.nid
        thana =request.vars.thana
        district_id =request.vars.district_id
        district =request.vars.district
        
        # return woner_name
        if client_id=='' or client_id==None or client_id=='None':
            response.flash = 'Required ID!'
            # return 10
        else:
            check_item_sql = "select * from sm_client where cid='"+str(c_id)+"'and client_id='"+str(client_id)+"';"
            # return check_item_sql
            check_item = db.executesql(check_item_sql, as_dict=True)
            # return check_item
            if len(check_item)>0:
                response.flash = 'Client id already exists!'
                # return 10 
            else:
                checkArea_sql="select level_id,level_name from sm_level where cid='"+ str(c_id) +"' and is_leaf='1' and level_id='"+ str(distributor_id) +"' and level_name='"+ str(distributor_name) +"' order by id;"
                # return checkArea_sql
                checkArea=db.executesql(checkArea_sql, as_dict=True)
                if len(checkArea)==0:
                    # return 'xlkdhn'
                    response.flash='Invalid Distributor ID/Name!'
                else:
                    insertitem_sql = "INSERT INTO sm_client (cid,client_id,name,area_id,depot_name,customer_type,status,balance,credit_limit,credit_duration,payment_mode,bank_account_no,address,contact_no1,nid,thana,district_id,district) VALUES ('"+str(c_id)+"','"+str(client_id)+"','"+str(name)+"','"+str(distributor_id)+"','"+str(distributor_name)+"','"+str(customer_type)+"','"+str(status)+"','"+str(balance)+"','"+str(credit_limit)+"','"+str(credit_duration)+"','"+str(payment_mode)+"','"+str(bank_account_no)+"','"+str(address)+"','"+str(contact_no1)+"','"+str(nid)+"','"+str(thana)+"','"+str(district_id)+"','"+str(district)+"');"      
                    insertitem = db.executesql(insertitem_sql)
                    response.flash= 'Successfully saved!'
                    redirect(URL('customer','client'))
    return dict()


def catagory():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    return dict()

def sub_catagory():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    return dict()


#==========CLIENT DOWNLOAD========
def client_Download():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    distributor_id=''
    distributor_name=''
    rep_id=''
    rep_name=''
    condition = ''
    condition=session.client_condition
    if condition==None or condition=='None':
        condition=''
    # return condition
    download_sql = "select * from sm_client where cid = '"+c_id+"' "+condition+";"
    download_records = db.executesql(download_sql, as_dict=True)
    
    myString = 'Client \n\n'
    myString += 'Client ID,Name,Distributor ID,Distributor Name,Contact No1,District ID,District Name,Tag-person ID,Tag-person Name,Type,Location,Approved\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len( download_records)):
        recordsStr =  download_records[i]
        client_id=str(recordsStr["client_id"])
        name=str(recordsStr["name"])
        distributor_id=str(recordsStr["area_id"])
        distributor_name=str(recordsStr["depot_name"])
        customer_type=str(recordsStr["customer_type"])
        contact_no1=str(recordsStr["contact_no1"])
        district_id=str(recordsStr["district_id"])
        district=str(recordsStr["district"])
        approved=str(recordsStr["approved_by_sup"])
        latitude = str(recordsStr["latitude"])
        longitude = str(recordsStr["longitude"])
        location = f"https://maps.google.com/?q={latitude},{longitude}"

        repRecords_sql = 'select rep_id,name from rep_client where cid="' + c_id + '" and client_id="' + client_id + '"  order by id;'
        repRows = db.executesql(repRecords_sql, as_dict=True)
        for i in range(len(repRows)):
            records_dict=repRows[i]
            rep_id=str(records_dict["rep_id"])
            rep_name=str(records_dict["name"])

        myString += str(client_id) + ',' + str(name) + ',' + str(distributor_id) + ',' + str(distributor_name) + ','  + str(contact_no1) + ',' + str(district_id) + ',' + str(district) + ',' + str(rep_id) + ',' + str(rep_name) + ',' + str(customer_type) + ',"' + str(location) + '",' + str(approved) +'\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_Client.csv'
    return str(myString)


#========CLIENT BATCH UPLOAD========
def client_batch_upload():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title = 'Client Batch Upload'

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
        # return excel_data
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)
        # return total_row

        item_id_list_excel = []

        valid_item_id_list = []
        excelList = []

        ins_list = []
        ins_dict = {}
        # return total_row
        for i in range(total_row):
            # return 10
            if i >= 100:
                # return 101
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 17:
                    item_id_list_excel.append(str(coloum_list[0]).strip().upper())

        # create list

        for i in range(total_row):
            if i >= 100:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')
            # return len(coloum_list)

            if len(coloum_list) != 17:
                error_data = row_data + '(17 columns need in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue
            else:

                clientToId_excel = str(coloum_list[0]).strip()
                name_excel = str(coloum_list[1]).strip()
                area_id_excel = str(coloum_list[2]).strip()
                distributor_excel = str(coloum_list[3]).strip()
                status_excel = str(coloum_list[4]).strip()
                # segment_excel = str(coloum_list[5]).strip()
                # distributor_rep_excel = str(coloum_list[6]).strip()
                # distributor_emp_id_excel = str(coloum_list[7]).strip()
                balance_excel = str(coloum_list[5]).strip()
                credit_limit_excel = str(coloum_list[6]).strip()
                credit_duration_excel = str(coloum_list[7]).strip()
                customer_type_excel = str(coloum_list[8]).strip()
                payment_mode_excel = str(coloum_list[9]).strip()
                bank_account_no_excel = str(coloum_list[10]).strip()
                address_excel = str(coloum_list[11]).strip()
                # owner_name_excel = str(coloum_list[14]).strip()
                contact_no1_excel = str(coloum_list[12]).strip()
                nid_excel = str(coloum_list[13]).strip()
                thana_excel = str(coloum_list[14]).strip()
                district_id_excel = str(coloum_list[15]).strip()
                district_excel = str(coloum_list[16]).strip()
                # return status_excel

                if clientToId_excel==''or name_excel=='' or distributor_excel=='' or contact_no1_excel=='' or district_id_excel=='' or district_excel=='' or status_excel=='' or area_id_excel=='' or customer_type_excel=='':
                    error_data=row_data+'(Required all value!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue 
                else:
                    existCheckRows= " SELECT * FROM sm_client WHERE cid='"+str(c_id)+"' and client_id = '"+str(clientToId_excel)+"' and status='ACTIVE';"
                    # return existCheckRows
                    existCheck = db.executesql(existCheckRows, as_dict=True)
                    # return existCheck

                    if len(existCheck) > 0:
                        error_data=row_data+'(Duplicate User!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        checkArea_sql="select level_id,level_name from sm_level where cid='"+ str(c_id) +"' and is_leaf='1' and level_id='"+ str(area_id_excel) +"' and level_name='"+ str(distributor_excel) +"' order by id;"
                        # return checkArea_sql
                        checkArea=db.executesql(checkArea_sql, as_dict=True)
                        # return len(checkArea)
                        if len(checkArea)==0:
                            # return 'xlkdhn'
                            error_data=row_data+'(Invalid Distributor ID/Name!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            typeRecords_sql = "select type from customer_type where cid='"+ str(c_id) +"' and type='"+ str(customer_type_excel) +"' order by id;"
                            # return typeRecords_sql
                            typeRows = db.executesql(typeRecords_sql, as_dict=True)
                            # return len(typeRows)
                            if len(typeRows)==0:
                                # return 'xlkdhn'
                                error_data=row_data+'(Invalid Type!)\n'
                                error_str=error_str+error_data
                                count_error+=1
                                continue
                            else:
                                try:
                                    insert_sql = "INSERT INTO sm_client (cid,client_id,name,area_id,depot_name,customer_type,status,balance,credit_limit,credit_duration,payment_mode,bank_account_no,address,contact_no1,nid,thana,district_id,district) VALUE ('"+str(c_id)+"','"+str(clientToId_excel)+"','"+str(name_excel)+"', '"+str(area_id_excel)+"','"+str(distributor_excel)+"','"+str(customer_type_excel)+"','"+str(status_excel)+"','"+str(balance_excel)+"', '"+str(credit_limit_excel)+"','"+str(credit_duration_excel)+"','"+str(payment_mode_excel)+"', '"+str(bank_account_no_excel)+"','"+str(address_excel)+"','"+str(contact_no1_excel)+"','"+str(nid_excel)+"','"+str(thana_excel)+"','"+str(district_id_excel)+"','"+str(district_excel)+"');"
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



#=========CLIENT EDIT & DELETE=======
def client_edit():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    # return 'flhj'
    response.title='Retailer Edit'
    client_id =request.args(0)
    # return customer_id
    
    update_btn = request.vars.update_btn
    delete_btn = request.vars.delete_btn
    name=''
    distributor_id=''
    distributor_name=''
    status=''
    balance=0 
    credit_limit=0
    credit_duration=''
    customer_type=''
    payment_mode =0
    bank_account_no =0
    address ='' 
    contact_no1 =''
    nid = ''
    thana ='' 
    district_id =''
    district =''


    select_ret_record_sql = f"SELECT * FROM sm_client WHERE client_id ='"+str(client_id)+"' GROUP BY client_id LIMIT 1;"
    # return select_ret_record_sql
    selected_ret_record = db.executesql(select_ret_record_sql, as_dict = True)

    # if len(selected_ret_record) != 0 :
    for i in range(len(selected_ret_record)):
        ret = selected_ret_record[i]
        rowId = str(ret["id"])
        client_id = str(ret["client_id"])
        name = str(ret["name"])
        distributor_id = str(ret["area_id"])
        distributor_name = str(ret["depot_name"])
        status = str(ret["status"])
        # segment = str(ret["segment"])
        # distributor_rep = str(ret["distributor_rep"])
        # distributor_emp_id = str(ret["dis_emp_id"])
        balance = str(ret["balance"])
        credit_limit = str(ret["credit_limit"])
        credit_duration = str(ret["credit_duration"])
        customer_type = str(ret["customer_type"])
        payment_mode = str(ret["payment_mode"])
        bank_account_no = str(ret["bank_account_no"])
        address = str(ret["address"])
        # owner_name = str(ret["owner_name"])
        contact_no1 = str(ret["contact_no1"])
        nid = str(ret["nid"])
        thana = str(ret["thana"])
        district_id = str(ret["district_id"])
        district = str(ret["district"])
    
    if update_btn:
        name_up = str(request.vars.name)
        distributor_id_up = str(request.vars.distributor_id)
        distributor_name_up = str(request.vars.distributor_name)
        status_up = str(request.vars.status)
        # segment_up = str(request.vars.segment)
        # distributor_rep_up = str(request.vars.distributor_rep)
        # distributor_emp_id_up = str(request.vars.distributor_emp_id)
        balance_up = str(request.vars.balance)
        credit_limit_up = str(request.vars.credit_limit)
        credit_duration_up = str(request.vars.credit_duration)
        customer_type_up = str(request.vars.customer_type)
        payment_mode_up = str(request.vars.payment_mode)
        bank_account_no_up = str(request.vars.bank_account_no) 
        address_up = str(request.vars.address)
        # owner_name_up = str(request.vars.owner_name)
        contact_no1_up = str(request.vars.contact_no1)
        nid_up = str(request.vars.nid)
        thana_up = str(request.vars.thana)
        district_id_up = str(request.vars.district_id)
        district_up = str(request.vars.district)      

        update_sql = f"UPDATE sm_client SET name = '{str(name_up)}', area_id = '{str(distributor_id_up)}', depot_name = '{str(distributor_name_up)}', customer_type = '{str(customer_type_up)}', status = '{str(status_up)}', balance = '{str(balance_up)}', credit_limit = '{str(credit_limit_up)}', credit_duration = '{str(credit_duration_up)}', payment_mode = '{str(payment_mode_up)}', bank_account_no = '{str(bank_account_no_up)}', address = '{str(address_up)}', contact_no1 = '{str(contact_no1_up)}', nid = '{str(nid_up)}', thana = '{str(thana_up)}', district_id = '{str(district_id_up)}', district = '{str(district_up)}' WHERE client_id = '"+str(client_id)+"' LIMIT 1;"
        up_date = db.executesql(update_sql)

        session.flash = 'Update Successfully!'

        redirect(URL('customer','client'))

    if delete_btn:
            if (session.cid == '' or session.cid is None):
                redirect(URL('default', 'index'))

            check_client_sql = "SELECT client_id FROM rep_client WHERE client_id ='"+str(client_id)+"' GROUP BY client_id LIMIT 1;"
            check_client = db.executesql(check_client_sql, as_dict=True)
            # return check_client_sql

            if len(check_client) > 0:
                # return 11
                delete_sql = f"DELETE FROM sm_client WHERE client_id='{client_id}' LIMIT 1;"
                db.executesql(delete_sql)
                delete_sql = f"DELETE FROM rep_client WHERE client_id='{client_id}' LIMIT 1;"
                db.executesql(delete_sql)
                session.flash = 'Deleted Successfully!'
                # return delete_sql
            else:
                delete_sql = f"DELETE FROM sm_client WHERE client_id='{client_id}' LIMIT 1;"
                db.executesql(delete_sql)
                session.flash = 'Deleted Successfully!'

            redirect(URL('customer', 'client'))

       
    return dict(client_id=client_id,name=name,distributor_id=distributor_id,distributor_name=distributor_name,customer_type=customer_type,status=status,balance=balance,credit_limit=credit_limit,credit_duration=credit_duration,payment_mode=payment_mode,bank_account_no=bank_account_no,address=address,contact_no1=contact_no1,nid=nid,thana=thana,district_id=district_id,district=district)

#========CLIENT BATCH EDIT========
def client_batch_edit():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title = 'Client Batch Edit'

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
        # return excel_data
        inserted_count = 0
        error_count = 0
        error_list = []
        row_list = excel_data.split('\n')
        total_row = len(row_list)
        # return total_row

        item_id_list_excel = []

        valid_item_id_list = []
        excelList = []

        ins_list = []
        ins_dict = {}
        # return total_row
        for i in range(total_row):
            # return 10
            if i >= 100:
                # return 101
                break
            else:
                row_data = row_list[i]
                coloum_list = row_data.split('\t')
                if len(coloum_list) == 3:
                    item_id_list_excel.append(str(coloum_list[0]).strip().upper())

        # create list

        for i in range(total_row):
            if i >= 100:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')
            # return len(coloum_list)

            if len(coloum_list) != 3:
                error_data = row_data + '(3 columns need in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue
            else:

                clientToId_excel = str(coloum_list[0]).strip()
                distributor_id_excel = str(coloum_list[1]).strip()
                distributor_name_excel = str(coloum_list[2]).strip()

                if clientToId_excel==''or distributor_id_excel=='' or distributor_name_excel=='' :
                    error_data=row_data+'(Required all value!)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue 
                else:
                    existCheckRows= " SELECT * FROM sm_client WHERE cid='"+str(c_id)+"' and client_id = '"+str(clientToId_excel)+"';"
                    existCheck = db.executesql(existCheckRows, as_dict=True)

                    if len(existCheck) == 0:
                        error_data=row_data+'(Invalid User!)\n'
                        error_str=error_str+error_data
                        count_error+=1
                        continue
                    else:
                        checkArea_sql="select level_id,level_name from sm_level where cid='"+ str(c_id) +"' and is_leaf='1' and level_id='"+ str(distributor_id_excel) +"' and level_name='"+ str(distributor_name_excel) +"' order by id;"
                        checkArea=db.executesql(checkArea_sql, as_dict=True)
                        if len(checkArea)==0:
                            error_data=row_data+'(Invalid Distributor ID/Name!)\n'
                            error_str=error_str+error_data
                            count_error+=1
                            continue
                        else:
                            try:
                                update_sql = f"UPDATE sm_client SET area_id = '{str(distributor_id_excel)}', depot_name = '{str(distributor_name_excel)}' WHERE client_id = '"+str(clientToId_excel)+"' LIMIT 1;"
                                update_ff_list = db.executesql(update_sql)
                                count_inserted+=1
                            except Exception as e:
                                error_str = 'Please do not insert special charachter.'


        if error_str == '':
            error_str = 'No error'

    return dict(count_inserted=count_inserted, count_error=count_error, error_str=error_str, total_row=total_row)
    


def client_profile():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    return dict()