from datetime import datetime

def index():
    response.title = 'Representative Stay report'
    cid = session.cid

    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))

    btn_filter = request.vars.btn_filter
    btn_clear = request.vars.btn_clear

    condition_info = ''
    data_list =[]
    total_rec=0

    reqPage = len(request.args)
     # --------paging
    page = 0
    session.rep_per_page = 20
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    # return page
    rep_per_page = session.rep_per_page
    # return rep_per_page
    if(page==0):
        limitby = (page * rep_per_page, (page + 1) * rep_per_page)
    else:
        limitby = ((page* rep_per_page), rep_per_page)
    # --------end paging
    if btn_clear:
        session.representative = ''
        session.date = ''
        session.customer = ''
        session.condition_info = ''
        session.flash = "All data has been clear"
        return redirect(URL("sales_person_tracking_stay_time","index"))

    if btn_filter:
        representative = request.vars.representative_filter
        customer = request.vars.customer_filter
        date = str(request.vars.date_filter)
        # return date

        if (representative =="" or representative ==None or representative =="None") or (date =="" or None): 
            session.flash = "Please Insert a Representative and Date"
            return redirect(URL("sales_person_tracking_stay_time","index"))                         #aikhan a issue acea
        
        # return representative+" "+date
        
        representative_id = representative.split('|')[0]
        representative_name = representative.split('|')[-1]
        customer_id = customer.split("|")[0]
        customer_name = customer.split("|")[-1]
 
        
        if session.representative != '' or representative_id != '':
            condition_info += f" AND rep_id = '{str(representative_id)}'"
            session.representative = representative

        # return date
        if session.date != '' or date !="":
            condition_info += f" AND visit_date = '{str(date)}'"
            session.date = date

        if session.customer!="" or customer!="":
            condition_info = condition_info+ " AND visited_to_id ='"+str(customer_id)+"'"
            session.customer = customer
        
        session.condition_info = condition_info
        # return session.condition_info

        # if session.condition == None:
        #     session.condition =""
        # condition=session.condition
        # return session.condition

    # return session.condition_info


    if condition_info!="" or session.condition_info!="" :
        all_row_sql = f"SELECT rep_id,rep_name,area_id,area_name,visited_to_id,visited_to_name,visited_latlong,visit_date,start_time,visit_time FROM `sm_tracking_live2` WHERE cid = '{str(cid)}' {session.condition_info} ORDER BY start_time ASC limit %d, %d" % limitby;
        # return all_row_sql
        all_visited_record = db.executesql(all_row_sql, as_dict=True)

        
        
        # ================================always work to find out all rows in table=======================
        all_rec_sql = f"SELECT rep_id,rep_name,area_id,area_name,visited_to_id,visited_to_name,visited_latlong,visit_date,start_time,visit_time FROM `sm_tracking_live2` WHERE cid = '{str(cid)}' {session.condition_info};"
        # return all_rec_sql
        all_record = db.executesql(all_rec_sql)
        total_rec = len(all_record)
        # return session.condition
        # return len(all_visited_record)
        # =================================for table rows(total_record)===================================================
        # return total_rec

        for row in all_visited_record:
            
            rep_id = row['rep_id']
            rep_name = row['rep_name']
            rep = rep_id+"|"+rep_name

            area_id = row['area_id']
            area_name = row['area_name']
            area = area_id+"|"+area_name

            customer_d_id = row['visited_to_id']
            customer_d_name = row['visited_to_name']
            customer_info = customer_d_id+"|"+customer_d_name

            location = row['visited_latlong']
            visited_date = row['visit_date']

            start_time = row['start_time']
            v_time = row['visit_time']
            end_time = v_time.split(" ")[-1]
            end_time = end_time.split(".")[0]
            # time_format = "%S:%M:%H"
            # print(type(end_time))
            time_start = datetime.strptime(start_time, '%H:%M:%S')

            time_end = datetime.strptime(end_time, '%H:%M:%S') 
            # print(time_end)
            time_stay = time_end - time_start
        # return time_stay
            data_list.append({"rep": rep,"area":area, "customer_info":customer_info, "location":location, "date":visited_date,"start_time":start_time,"visit_time":end_time,"time_stay":time_stay})
        
    # if
    # return len(data_list)
    # return dict(data_list=data_list,page=page,rep_per_page=rep_per_page)
    return dict(data_list=data_list, total_rec=total_rec,page=page,rep_per_page=rep_per_page)

    return locals()
    







def get_all_rep_list():
    c_id = session.cid
    retStr = ''
    if (session.cid == '' or session.cid == None):
        redirect(URL('default', 'index'))

    itemlist_rep_Rows_sql = "SELECT rep_id,name FROM `sm_rep` WHERE cid= '" + \
        c_id+"' order by rep_id;"
    # return itemlist_rep_Rows_sql
    itemlist_rep_Rows = db.executesql(itemlist_rep_Rows_sql, as_dict=True)
    # return itemlistRows
    for i in range(len(itemlist_rep_Rows)):
        item_list_dict = itemlist_rep_Rows[i]
        # print(item_list_dict)                # checking in this point next day start from this point.
        # return item_list_dict
        rep_id = str(item_list_dict["rep_id"])
        rep_name = str(item_list_dict["name"])

        # return item_id
        if retStr == '':
            retStr += rep_id+'|'+rep_name
        else:
            retStr += ',' + rep_id+'|'+rep_name

    return retStr

# ## auto complete get_all_rep_list end


def get_all_client_list():
    c_id = session.cid
    restStr = ''
    if (session.cid == '' or session.cid == None):
        redirect(URL('default', 'index'))

    itemlist_cl_Rows_sql = f"SELECT client_id,name FROM sm_client WHERE cid= '{c_id}' order by client_id;"

    # return itemlist_rep_Rows_sql
    itemliscl_Rows = db.executesql(itemlist_cl_Rows_sql, as_dict=True)
    # return itemlistRows
    for i in range(len(itemliscl_Rows)):
        item_list_dict = itemliscl_Rows[i]

        client_id = str(item_list_dict["client_id"])
        client_name = str(item_list_dict["name"])

        # return item_id
        if restStr == '':
            restStr += client_id+'|'+client_name
        else:
            restStr += ',' + client_id+'|'+client_name

    return restStr

# ## auto complete get_all_rep_list end