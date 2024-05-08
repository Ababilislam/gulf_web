# import urllib2
# Validation

def index():
    response.title = 'Map'
    return locals()


# ===============map show
def outletMap():

    cid = session.cid

    btn_outlet_map = request.vars.btn_outlet_map
#     btn_path_map = request.vars.btn_path_map
#     return btn_outlet_map
    if (btn_outlet_map != None):
        search_valueOutlet_map = request.vars.search_value.strip()

        session.search_valueOutlet_map = str(
            search_valueOutlet_map).split('|')[-1]
#         return session.search_valueOutlet_map
        session.search_valueOutlet_map_area_name = search_valueOutlet_map

        if ((session.search_valueOutlet_map == '') or (session.search_valueOutlet_map == None)):
            session.flash = 'Please Select Type and Value'
            redirect(URL('index'))
    # SQL Query
        area_id = session.search_valueOutlet_map
        # all_record_area_wise_sql = "SELECT * FROM `sm_client` WHERE cid='"+cid+"' and area_id= '"+area_id+"' and latitude IS NOT NULL and longitude IS NOT NULL order by client_id;"
        # return all_record_area_wise_sql

        all_record_area_wise_sql = f"SELECT * FROM `sm_client` WHERE cid = '{cid}' AND area_id = '{area_id}' AND latitude != '' AND longitude != '' ORDER BY client_id;"

        records = db.executesql(all_record_area_wise_sql, as_dict=True)


#         return db._lastsql
        check_total = len(records)
#    #     return check_total
        # x=type(records)
        # return x
        total = 0
        middle = 1
        if check_total:
            total = check_total
            middle = int(round(total,2))
        start_flag = 0
        map_string_name = ''
        map_string_name_in = ''
        center_point = ''
        c = 0
        x = 0

        for row in records:
            c = c + 1
            # total_rec = str(row["name"])+ " " +"("+str(row['client_id']) +")" +"()"+ str(row['latitude'])
            # return total_rec
            point_view = str(row['latitude']) + ',' + str(row['longitude'])
            #             point_view = str(row.sm_client.field1)
            # return point_view
            pSName = str(row['name'])

            # pSName = str(row[name])
            client_id = str(row['client_id'])
            # return client_id
            client_name = str(row['name'])
            # return client_name
            c_info = client_name + "(" + client_id + ")"
            # return c_info


#                show_str = """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.client_id) + """')" value=" """ + c_info + """ ">""" + """</p>""" + link_path + """</br>""" + """StartTime: """ + str(row.start_time) + """</br>""" + """EndTime: """ + str(row.end_time)
            if (c == middle):
                center_point = point_view
            if (start_flag == 0):
                map_string_name = map_string_name + """<input type="submit" style="width:400px" """ + \
                    client_id + """ value=" """ + c_info + """ ">""" + \
                    """,""" + point_view + """,""" + str(x) + """rdrd"""
#                map_string_name = map_string_name + """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.client_id) + """')" value=" """ + c_info + """ ">""" + """,""" + str(point_view) + """,""" + str(x) + """rdrd"""
                start_flag = 1
                # return (point_view)
            else:
                map_string_name = map_string_name + """<input type="submit" style="width:400px" """ + \
                    client_id + """ value=" """ + c_info + """ ">""" + \
                    """,""" + str(point_view) + """,""" + str(x) + """rdrd"""
            x = x + 1
#
#         return map_string_name
        if (map_string_name == ''):
            #             map_string_name = 'No Outlet Available' + "," + '23.811991,90.422952' + ',' + '0' + 'rdrd'
            #             center_point = '23.811991, 90.422952'
            session.flash = 'Result Not Available'
            redirect(URL('index'))
        # return map_string_name
        return dict(map_string_name=map_string_name, center_point=center_point)


# function for form auto complete
def get_all_area_list():
    c_id = session.cid
    retStr = ''
    if (session.cid == '' or session.cid == None):
        redirect(URL('default', 'index'))

    itemlistRows_sql = "SELECT rep_id,area_id FROM `sm_rep_area` WHERE cid= '"+c_id+"';"
    itemlistRows = db.executesql(itemlistRows_sql, as_dict=True)
    # return itemlistRows
    for i in range(len(itemlistRows)):
        item_list_dict = itemlistRows[i]
        # print(item_list_dict)                # checking in this point next day start from this point.
        # return itemlistRows
        item_id = str(item_list_dict["rep_id"])
        area_id = str(item_list_dict["area_id"])
        if retStr == '':
            retStr = item_id+'|'+area_id
        else:
            retStr += ',' + item_id+'|'+area_id

    return retStr

# ## auto complete function end

# function for form auto complete


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

# ## auto complete function end


def sales_person_tracking_map_date():
    cid = session.cid

    search_value_person = request.vars.search_value_person
    search_date = str(request.vars.search_date)
    search_date_to = str(request.vars.search_date_to)
    btn_sp_visit_map = request.vars.btn_sp_visit_map
    call_type = "VISIT"
    # return search_value_person
    # return search_date
    # return search_date_to
    # return btn_sp_visit_map

    if (btn_sp_visit_map != None):
        sale_person_outlet_map = request.vars.search_value_person.strip()
        # return sale_person_outlet_map+ "  "+ search_date

        session.sale_person_id_name = sale_person_outlet_map
        session.sale_person_id = str(
            sale_person_outlet_map).split('|')[0]
        session.sale_person_name = str(
            sale_person_outlet_map).split('|')[1]
        # return session.sale_person_id
        # return session.sale_person_name
        # session.sale_person_name = sale_person_name

        if ((sale_person_outlet_map == '') or (sale_person_outlet_map == None)):
            session.flash = 'Please Select a Value for Sale person'
            redirect(URL('index'))
    # SQL Query
        rep_id = session.sale_person_id
        # return rep_id
        # all_visit_info_lat_long_sql = f'SELECT rep_id, rep_name, visited_to_id, visited_to_name, call_type, visit_date, visited_latlong FROM sm_tracking_live2 WHERE rep_id = "{rep_id}" and call_type = "{call_type}" and visit_date = "{search_date}" AND visited_latlong != "" AND visited_to_id != "";'
        # SELECT rep_id, rep_name, visited_to_id, visited_to_name, call_type, visit_date, visited_latlong FROM sm_tracking_live2 WHERE rep_id = "100078" and call_type = "VISIT" and visit_date BETWEEN "2024-02-25"and "2024-02-28" AND visited_latlong != "" AND visited_to_id != "";

        all_visit_info_lat_long_sql = f'SELECT rep_id, rep_name, visited_to_id, visited_to_name, call_type, visit_date, visited_latlong FROM sm_tracking_live2 WHERE rep_id = "{rep_id}" and call_type = "{call_type}" and visit_date BETWEEN "{search_date}" and "{search_date_to}" AND visited_latlong != "" AND visited_to_id != "";'
        # return all_visit_info_lat_long_sql
        all_visit_info_records = db.executesql(
            all_visit_info_lat_long_sql, as_dict=True)

#         return db._lastsql
        check_total_rec = len(all_visit_info_records)
        # return check_total_rec
        session.no_of_record = check_total_rec
        # return  session.no_of_record

        total = 0
        middle = 1
        if check_total_rec:
            total = check_total_rec
            # return total
            middle = int(round(total , 2))
            # return round(total,2)
            # return middle
        start_flag = 0
        map_string_name = ''
        map_string_name_in = ''
        center_point = ''
        c = 0
        x = 0

        for row in all_visit_info_records:
            c = c + 1
            total_rec = str(row["rep_id"]) + " " + row["rep_name"] + " " + ""+str(row['visited_to_id']) + "" + \
                "" + ""+str(row['visited_to_name']) + "" + \
                str(row['visited_latlong']) + str(row['visit_date'])
            # return total_rec
        # ===================till this point work.
            lat_long = str(row['visited_latlong'])
            # return lat_long
            # point_view = str(row['latitude']) + ',' + str(row['longitude'])
            point_view = lat_long
            #             point_view = str(row.sm_client.field1)
            # return point_view
            pSName = str(row['rep_name'])

            # pSName = str(row[name])
            client_id = str(row['visited_to_id'])
            # return client_id
            client_name = str(row['visited_to_name'])
            # return client_name
            c_info = client_name + "(" + client_id + ")"
            # return c_info


#                show_str = """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.client_id) + """')" value=" """ + c_info + """ ">""" + """</p>""" + link_path + """</br>""" + """StartTime: """ + str(row.start_time) + """</br>""" + """EndTime: """ + str(row.end_time)
            if (c == middle):
                center_point = point_view
            if (start_flag == 0):
                map_string_name = map_string_name + """<input type="submit" style="width:400px" """ + \
                    client_id + """ value=" """ + c_info + """ ">""" + \
                    """,""" + point_view + """,""" + str(x) + """rdrd"""
#                map_string_name = map_string_name + """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.client_id) + """')" value=" """ + c_info + """ ">""" + """,""" + str(point_view) + """,""" + str(x) + """rdrd"""
                start_flag = 1
                # return (point_view)
            else:
                map_string_name = map_string_name + """<input type="submit" style="width:400px" """ + \
                    client_id + """ value=" """ + c_info + """ ">""" + \
                    """,""" + str(point_view) + """,""" + str(x) + """rdrd"""
            x = x + 1
#
        # return map_string_name
        if (map_string_name == ''):
            session.flash = 'Result Not Available'
            redirect(URL('index'))
        # return map_string_name
        return dict(map_string_name=map_string_name, center_point=center_point)
