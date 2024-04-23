def Item():
    if (session.cid=='' or session.cid==None):
        # return 'dgngn'
        redirect (URL('default','index'))
    # return session.cid
    response.title='Item'
    submit=request.vars.submit
    btn_filter_item=request.vars.btn_filter_item
    item_id_filter = request.vars.item_id_filter
    btn_all=request.vars.btn_all
    c_id=session.cid
    condition = ''
    reqPage = len(request.args)
    # return c_id
    
    if submit:
        item_id =request.vars.item_id
        name =request.vars.name
        pack_size =request.vars.pack_size
        description =request.vars.description
        category_id =request.vars.category_id
        category_id_sp =request.vars.category_id_sp
        unit_type =request.vars.unit_type
        manufacture =request.vars.manufacture
        item_carton =request.vars.item_carton
        price =request.vars.price
        dist_price =request.vars.dist_price
        vat_amount =request.vars.vat_amount
        status =request.vars.status
        # return status
        if item_id=='' or item_id==None or item_id=='None':
            response.flash = 'Required Item ID'
            # return 10
        else:
            check_item_sql = "select * from sm_item where cid='"+str(c_id)+"'and item_id='"+str(item_id)+"';"
            # return check_item_sql
            check_item = db.executesql(check_item_sql, as_dict=True)
            # return check_item
            if len(check_item)>0:
                response.flash = 'Item id already exists'
                # return 10
                
            else:
                # return 11
                insertitem_sql = "INSERT INTO sm_item (cid,item_id,name,pack_size,des,category_id,category_id_sp,unit_type,manufacturer,item_carton,price,dist_price,vat_amt,status) VALUES ('"+str(c_id)+"','"+str(item_id)+"','"+str(name)+"','"+str(pack_size)+"','"+str(description)+"','"+str(category_id)+"','"+str(category_id_sp)+"','"+str(unit_type)+"','"+str(manufacture)+"','"+str(item_carton)+"','"+str(price)+"','"+str(dist_price)+"','"+str(vat_amount)+"','"+str(status)+"');"      
                insertitem = db.executesql(insertitem_sql)
                response.flash= 'Successfully saved!'

    # --------paging
    session.items_per_page = 20
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # return limitby
    # --------end paging

    if btn_filter_item == "Filter":
        if item_id_filter !='':
            # return 10
            session.item_id_filter = item_id_filter
            item_id_filter = str(item_id_filter).split('|')[0]
            condition = condition + " and item_id = '"+str(item_id_filter)+"'"
            # return condition
    if btn_all == "All":
        # return 10
        condition = ''
        session.item_id_filter = ''

    itemRows_sql = "select * from sm_item where cid = '"+str(c_id)+"'  "+condition+" ORDER BY id DESC limit %d, %d;" % limitby
    # return itemRows_sql
    itemRows = db.executesql(itemRows_sql, as_dict=True)
    session.condition = condition
    # return 22

    total_record_sql = f"SELECT COUNT(id) AS total FROM sm_item WHERE cid='GULF' {condition} ORDER BY id ASC;"
    total_record = db.executesql(total_record_sql, as_dict = True)
    total_rec = total_record[0]['total']

    cat_type_sql="select * from sm_category_type where cid='"+str(c_id)+"';"
    # return cat_type_sql
    cat_type=db.executesql(cat_type_sql, as_dict=True)


    return dict(itemRows=itemRows,page=page,items_per_page=items_per_page,total_rec=total_rec,cat_type=cat_type)

def get_item_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    itemlistRows_sql = "select item_id,name from sm_item where cid = '"+c_id+"';"
    itemlistRows = db.executesql(itemlistRows_sql, as_dict=True)

    for i in range(len(itemlistRows)):
        item_list_dict=itemlistRows[i]   
        item_id=str(item_list_dict["item_id"])
        name=str(item_list_dict["name"])   
        if retStr == '':
            retStr = item_id+'|'+name
        else:
            retStr += ',' + item_id+'|'+name
    
    return retStr

#=========ITEM DOWNLOAD=========
def item_Download():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    condition = ''
    condition = session.condition

    download_sql = "select * from sm_item where cid = '"+c_id+"' "+condition+";"
    download_records = db.executesql(download_sql, as_dict=True)
    
    myString = 'Item \n\n'
    myString += 'item_id,name,des,category_id,category_id_sp,unit_type,item_carton,dist_price,vat_amt,status\n'
    total=0
    attTime = ''
    totalCount = 0
    for i in range(len( download_records)):
        recordsStr =  download_records[i]
        item_id=str(recordsStr["item_id"])
        name=str(recordsStr["name"])
        description=str(recordsStr["des"])
        category_id=str(recordsStr["category_id"])
        category_id_sp=str(recordsStr["category_id_sp"])
        unit_type=str(recordsStr["unit_type"])
        item_carton=str(recordsStr["item_carton"])
        dist_price=str(recordsStr["dist_price"])
        vat_amount=str(recordsStr["vat_amt"])
        status=str(recordsStr["status"]) 


        myString += str(item_id) + ',' + str(name) + ',' + str(description) + ',' + str(category_id) + ',' + str(category_id_sp) + ',' + str(unit_type) + ',' + str(item_carton) + ',' + str(dist_price) + ',' + str(vat_amount) + ',' + str(status) +'\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_Item.csv'
    return str(myString)    




def item_batch_upload():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title = 'Item Batch Upload'

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
                if len(coloum_list) == 13:
                    item_id_list_excel.append(str(coloum_list[0]).strip().upper())

        # create list
        for i in range(total_row):
            if i >= 100:
                break
            else:
                row_data = row_list[i]
            coloum_list = row_data.split('\t')

            if len(coloum_list) != 13:
                error_data = row_data + '(13 columns need in a row)\n'
                error_str = error_str + error_data
                count_error += 1
                continue
            else:

                itemToId_excel = str(coloum_list[0]).strip()
                name_excel = str(coloum_list[1]).strip()
                packSize_excel = str(coloum_list[2]).strip()
                des_excel = str(coloum_list[3]).strip()
                categoryId_excel = str(coloum_list[4]).strip()
                categoryIdsp_excel = str(coloum_list[5]).strip()
                unitType_excel = str(coloum_list[6]).strip()
                manufacturer_excel = str(coloum_list[7]).strip()
                itemCarton_excel = str(coloum_list[8]).strip()
                price_excel = str(coloum_list[9]).strip()
                distPrice_excel = str(coloum_list[10]).strip()
                vatAmt_excel = str(coloum_list[11]).strip()
                status_excel = str(coloum_list[12]).strip()
                # return status_excel

                if (itemToId_excel==''or itemToId_excel == 'NONE') and (name_excel=='' or name_excel== 'NONE') and (unitType_excel=='' or unitType_excel == 'NONE') and (itemCarton_excel=='' or itemCarton_excel == 'NONE') and (price_excel==''or price_excel == 'NONE') and (distPrice_excel=='' or distPrice_excel== 'NONE') and (vatAmt_excel=='' or vatAmt_excel == 'NONE') and (status_excel=='' or status_excel == 'NONE'):
                    error_data=row_data+'(Required all value)\n'
                    error_str=error_str+error_data
                    count_error+=1
                    continue 
                else:
                    existCheckRows= " SELECT * FROM sm_item WHERE cid='"+str(c_id)+"' and item_id = '"+itemToId_excel+"';"
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
                            insert_sql = "INSERT INTO sm_item (cid,item_id,name,pack_size,des,category_id,category_id_sp,unit_type,manufacturer,item_carton,price,dist_price,vat_amt,status) VALUE ('"+str(c_id)+"','"+str(itemToId_excel)+"','"+str(name_excel)+"', '"+str(packSize_excel)+"','"+str(des_excel)+"','"+str(categoryId_excel)+"', '"+str(categoryIdsp_excel)+"','"+str(unitType_excel)+"','"+str(manufacturer_excel)+"', '"+str(itemCarton_excel)+"','"+str(price_excel)+"','"+str(distPrice_excel)+"', '"+str(vatAmt_excel)+"','"+str(status_excel)+"');"
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


def item_edit():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    # return 'flhj'
    item_id =request.args(0)
    
    update_btn = request.vars.update_btn
    delete_btn = request.vars.delete_btn

    select_item_record_sql = f"SELECT * FROM sm_item WHERE item_id ='"+str(item_id)+"' GROUP BY item_id LIMIT 1;"
    # return select_item_record_sql
    selected_item_record = db.executesql(select_item_record_sql, as_dict = True)
    # return 11

    # if len(selected_ret_record) != 0 :
    for i in range(len(selected_item_record)):
        item = selected_item_record[i]
        rowId = str(item["id"])
        item_id = str(item["item_id"])
        name = str(item["name"])
        pack_size = str(item["pack_size"])
        description = str(item["des"])
        category_id = str(item["category_id"])
        category_id_sp = str(item["category_id_sp"])
        unit_type = str(item["unit_type"])
        manufacture = str(item["manufacturer"])
        item_carton = str(item["item_carton"])
        price = str(item["price"])
        dist_price = str(item["dist_price"])
        vat_amount = str(item["vat_amt"])
        status = str(item["status"])
        # return status
    
    if update_btn:
        name_up = str(request.vars.name)
        pack_size_up = str(request.vars.pack_size)
        description_up = str(request.vars.description)
        category_id_up = str(request.vars.category_id)
        category_id_sp_up = str(request.vars.category_id_sp)
        unit_type_up = str(request.vars.unit_type)
        manufacture_up = str(request.vars.manufacture)
        item_carton_up = str(request.vars.item_carton)
        price_up = str(request.vars.price)
        dist_price_up = str(request.vars.dist_price) 
        vat_amount_up = str(request.vars.vat_amount)
        status_up = str(request.vars.status)
        # return  price_up 

        update_sql = f"UPDATE sm_item SET name = '"+str(name_up)+"',  pack_size = '"+str(pack_size_up)+"', des = '"+str(description_up)+"', category_id = '"+str(category_id_up)+"', category_id_sp = '"+str(category_id_sp_up)+"',unit_type = '"+str(unit_type_up)+"',  manufacturer = '"+str(manufacture_up)+"', item_carton = '"+str(item_carton_up)+"', price = '"+str(price_up)+"', dist_price = '"+str(dist_price_up)+"' ,vat_amt = '"+str(vat_amount_up)+"', status = '"+str(status_up)+"'  WHERE item_id = '"+str(item_id)+"' LIMIT 1;"
        # return update_sql
        up_date = db.executesql(update_sql)

        session.flash = 'Update Successfully!'

        redirect(URL('item','Item'))

    if delete_btn:
        delete_sql = f"DELETE FROM sm_item WHERE item_id='{item_id}' LIMIT 1;"
        delete = db.executesql(delete_sql)

        session.flash = 'Deleted Successfully!'

        redirect(URL('item','Item'))
            
    return dict(item_id=item_id,name=name,pack_size=pack_size,description=description,category_id=category_id,category_id_sp=category_id_sp,unit_type=unit_type,manufacture=manufacture,item_carton=item_carton,price=price,dist_price=dist_price,vat_amount=vat_amount,status=status)
    

def unit():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title='Unit Type'
    c_id = session.cid
    # cat_type_id=request.args(0)
    # return cat_type_id
    submit=request.vars.submit
    delete_btn=request.vars.delete_btn
    reqPage = len(request.args)
    
    # return submit
    if submit:
        # return 10
        cat_type_id=request.vars.cat_type_id
        # return cat_type_id    
        if cat_type_id=='' or cat_type_id=='None' or cat_type_id==None:
            response.flash = 'Required Unit Type!'    
        else:
            insertUnit_sql = "INSERT INTO sm_category_type (cid,cat_type_id) VALUES ('"+str(c_id)+"','"+str(cat_type_id)+"');" 
            # return insertUnit_sql     
            insertUnit = db.executesql(insertUnit_sql)
            response.flash= 'Successfully saved!'
    # session.cat_type_id=cat_type_id
    if delete_btn: 
        row_id = request.args(0)
        # return row_id
        delete_sql = "DELETE from sm_category_type where cid = '"+str(c_id)+"' and id='"+str(row_id)+"' limit 1 ;"
        # return delete_sql
        records = db.executesql(delete_sql)
        session.flash = 'Deleted Successfully'
        redirect (URL('item','unit'))

     # --------paging
    session.items_per_page = 20
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    items_per_page = session.items_per_page
    limitby = (page * items_per_page, (page + 1) * items_per_page + 1)
    # return limitby
    # --------end paging

    unitRows_sql = "select * from sm_category_type where cid = '"+str(c_id)+"'limit %d, %d;" % limitby
    # # return itemRows_sql
    unitRows = db.executesql(unitRows_sql, as_dict=True)

    total_record_sql = f"SELECT COUNT(id) AS total FROM sm_category_type WHERE cid='GULF' ORDER BY id ASC;"
    total_record = db.executesql(total_record_sql, as_dict = True)
    total_rec = total_record[0]['total']

    return dict(unitRows=unitRows,page=page,items_per_page=items_per_page,total_rec=total_rec)