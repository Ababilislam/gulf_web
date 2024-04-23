
# ================================================ NO ORDER SHOW ====================================================#

def no_order():
    c_id=session.cid
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    response.title='Order'
    btn_filter = request.vars.btn_filter
    btn_all=request.vars.btn_all
    condition = ''
    reqPage = len(request.args)
    from_date = ''
    to_date =''
    condition=''
    rep_id_filter=''
    region_id_filter=''
    zone_id_filter=''
    area_id_filter=''
    if btn_filter == "Filter":
        from_date = str(request.vars.from_dt_filter).strip().replace('None', '')
        to_date = str(request.vars.to_dt_filter).strip().replace('None', '')
        rep_id_filter = request.vars.rep_id_filter
        region_id_filter = request.vars.region_id_filter
        zone_id_filter = request.vars.zone_id_filter
        area_id_filter = request.vars.area_id_filter
        approved_filter = request.vars.approved_filter
        
        # condition = "AND visit_date BETWEEN '"+str(from_date)+"' AND '"+str(to_date)+"' AND '"+str(retailer_id_filter)+"'  AND '"+str(retailer_id_filter)+"' AND '"+str(area_id_filter)+"' "
        
        if from_date != "" and to_date != "":
            session.from_date = from_date
            session.to_date = to_date
            condition = "AND visit_date BETWEEN '"+str(from_date)+"' AND '"+str(to_date)+"' "

        if rep_id_filter != '':
            session.rep_id_filter = rep_id_filter
            try:
                rep_id_filter = str(rep_id_filter).split('|')[0]
            except:
                rep_id_filter = ''
            condition = condition + " and rep_id = '"+str(rep_id_filter)+"'"

        if region_id_filter != '':
            session.region_id_filter = region_id_filter
            try:
                region_id_filter = str(region_id_filter).split('|')[0]
            except:
                session.region_id_filter = ''
            condition = condition + " and region_id = '"+str(region_id_filter)+"'"

        if zone_id_filter != '':
            session.zone_id_filter = zone_id_filter
            try:
                zone_id_filter = str(zone_id_filter).split('|')[0]
            except:
                session.zone_id_filter=''
            condition = condition + " and zone_id = '"+str(zone_id_filter)+"'"

        if area_id_filter:
            session.area_id_filter = area_id_filter
            try:
                area_id_filter = str(area_id_filter).split('|')[0]
            except:
                session.area_id_filter =''
            condition = condition + " and area_id = '"+str(area_id_filter)+"'"
        reqPage=0
        session.condition = condition


    if btn_all == "All":
        condition = '' 
        from_date =''
        to_date = ''
        session.rep_id_filter = ''
        session.region_id_filter = ''
        session.zone_id_filter = ''
        session.area_id_filter = ''
        session.from_date =''
        session.to_date = ''
        session.condition = condition
        reqPage=0
    
     # --------paging
    session.clients_per_page = 20
    if reqPage:
        page = int(request.args[0])
    else:
        page = 0
    clients_per_page = session.clients_per_page
    limitby = (page * clients_per_page, (page + 1) * clients_per_page + 1)
    # --------end paging
    
    condition = session.condition
    if condition==None or condition=='None':
        condition=''
    visit_data_record_sql = "SELECT * FROM sm_tracking_live2 WHERE cid = '"+str(c_id)+"'  "+str(condition)+" and call_type = 'NO ORDER VISIT' order by id desc limit %d, %d" % limitby
    # return visit_data_record_sql
    visit_data_record = db.executesql(visit_data_record_sql, as_dict=True)

    total_record_sql = f"SELECT COUNT(id) AS total FROM sm_tracking_live2 WHERE cid = '"+str(c_id)+"'  "+str(condition)+" and call_type = 'NO ORDER VISIT';"
    total_record = db.executesql(total_record_sql, as_dict = True)
    total_rec = total_record[0]['total']

    
    return dict(visit_data_record=visit_data_record,total_rec=total_rec,page=page,clients_per_page=clients_per_page)


# ================================================ NO ORDER DOWNLOAD ====================================================#

def no_order_Download():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    cid = session.cid
    condition = session.condition
    if condition==None or condition=='None':
        condition=''
    visit_data_record_sql = "SELECT * FROM sm_tracking_live2 WHERE cid = '"+str(cid)+"'  "+str(condition)+" and call_type = 'NO ORDER VISIT' order by id desc ;"
    # return visit_data_record_sql
    visit_data_record = db.executesql(visit_data_record_sql, as_dict=True)

    myString = 'No Order Visit List\n\n'
    myString += ' Employee ID, Employee Name, Retailer ID, Retailer Name, Region ID, Region Name, Zone ID, Zone Name, Area ID, Area Name, Call Type,Visit Date, Visit DateTime, Location, Visited Lat, Visited Longitude \n'
    total=0
    attTime = ''
    totalCount = 0
    retailer_id = ''
    retailer_name = ''
    for i in range(len(visit_data_record)):
        recordsStr = visit_data_record[i]
        rep_id = str(recordsStr['rep_id'])
        rep_name = str(recordsStr['rep_name'])
        region_id = str(recordsStr['region_id'])
        region_name = str(recordsStr['region_name'])
        zone_id = str(recordsStr['zone_id'])
        zone_name = str(recordsStr['zone_name'])
        area_id = str(recordsStr['area_id'])
        area_name = str(recordsStr['area_name'])
        call_type = str(recordsStr['call_type'])
        visit_date = str(recordsStr['visit_date'])
        visit_time = str(recordsStr['visit_time'])
        try:
            visit_time = str(recordsStr['visit_time']).split(' ')[1]
        except:
            visit_time = visit_time
        location_detail = str(recordsStr['location_detail'])
        latlong = str(recordsStr['visited_latlong'])
        retailer_id = str(recordsStr['visited_to_id'])
        retailer_name = str(recordsStr['visited_to_name'])
        if retailer_id == '' or retailer_id == 'None' or retailer_id == None:
            try:
                lat = str(latlong).split(',')[0]
                longitude = str(latlong).split(',')[1]
            except:
                lat = 0
                longitude = 0

            get_retailer_info_sql = "SELECT client_id, name FROM sm_client where latitude = '"+lat+"' and longitude ='"+longitude+"' group by client_id limit 1 ;"
            get_retailer_info = db.executesql(get_retailer_info_sql, as_dict = True)
            for r in range(len(get_retailer_info)):
                retailer_records = get_retailer_info[r]
                retailer_id = str(retailer_records["client_id"])
                retailer_name = str(retailer_records["name"])

        myString += str(rep_id) + ','+str(rep_name) + ',' + str(retailer_id) + ',' +str(retailer_name) + ',' + str(region_id) + ',' +str(region_name) + ',' + str(zone_id) + ',' + str(zone_name) + ',' + str(area_id) + ',' + str(area_name)+ ',' + str(call_type) + ',' + str(visit_date) + ',' + str(visit_time) + ','+ str(location_detail) + ','+ str(latlong) + ',\n'

    # Save as csv
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=no_order_visit_List.csv'
    return str(myString)


#=========Auto Complete=======
def get_rep_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    replistRows_sql = "select rep_id, name from sm_rep where cid = '"+c_id+"' group by rep_id;"
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




def get_region_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    regionlistRows_sql = "select level_id, level_name from sm_level where cid = '"+c_id+"' and depth = 0 group by level_id;"
    regionlistRows = db.executesql(regionlistRows_sql, as_dict=True)

    for i in range(len(regionlistRows)):
        region_list_dict=regionlistRows[i]   
        region_id=str(region_list_dict["level_id"])
        region=str(region_list_dict["level_name"])
        if retStr == '':
            retStr = region_id+'|'+region
        else:
            retStr += ',' + region_id+'|'+region
    
    return retStr




def get_zone_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    zonelistRows_sql = "select level_id, level_name from sm_level where cid = '"+c_id+"' and depth = 1 group by level_id;"
    zonelistRows = db.executesql(zonelistRows_sql, as_dict=True)

    for i in range(len(zonelistRows)):
        zone_list_dict=zonelistRows[i]   
        zone_id=str(zone_list_dict["level_id"])
        zone=str(zone_list_dict["level_name"])
        if retStr == '':
            retStr = zone_id+'|'+zone
        else:
            retStr += ',' + zone_id+'|'+zone
    
    return retStr




def get_area_id_list():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    c_id = session.cid
    retStr = ''

    arealistRows_sql = "select area_id, area_name from sm_rep_area where cid = '"+c_id+"'  group by area_id;"
    arealistRows = db.executesql(arealistRows_sql, as_dict=True)

    for i in range(len(arealistRows)):
        area_list_dict=arealistRows[i]   
        area_id=str(area_list_dict["area_id"])
        area=str(area_list_dict["area_name"])
        if retStr == '':
            retStr = area_id+'|'+area
        else:
            retStr += ',' + area_id+'|'+area
    
    return retStr

