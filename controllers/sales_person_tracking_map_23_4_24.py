# import urllib2
# Validation

def index():
    # task_id = 'rm_analysis_view'
    # access_permission = check_role(task_id)
    # if (access_permission == False):
    #     session.flash = 'Access is Denied'
    #     redirect (URL('default', 'home'))

    response.title = 'Map'

    # search_form = SQLFORM(db.sm_search_date)
    # return dict(search_form=search_form)
    # return "hello"
    return locals()


# def outletMap_mobile():

#     cid = session.cid

#     btn_outlet_map = request.vars.btn_outlet_map
# #     btn_path_map = request.vars.btn_path_map
# #     return btn_outlet_map
#     if (btn_outlet_map != None):
#         search_valueOutlet_map = request.vars.search_value.strip()

#         session.search_valueOutlet_map = str(
#             search_valueOutlet_map).split('|')[0]
#         # return dict()

#         if ((session.search_valueOutlet_map == '') or (session.search_valueOutlet_map == None)):
#             session.flash = 'Please Select Type and Value'
#             redirect(URL('index'))
# #
# #        # Set query based on search type
#         qset = db()
#         qset = qset(db.sm_client.cid == cid)

#         qset = qset(db.sm_client.area_id == session.search_valueOutlet_map)
#         qset = qset(db.sm_client.latitude != '0')
#         qset = qset(db.sm_client.longitude != '0')

#         records = qset.select(db.sm_client.ALL, orderby=db.sm_client.client_id)

# #         return db._lastsql
#         check_total = len(records)
# #    #     return check_total
#         total = 0
#         middle = 1
#         if check_total:
#             total = check_total
#             middle = int(round(total / 2))
#         start_flag = 0
#         map_string_name = ''
#         map_string_name_in = ''
#         center_point = ''
#         c = 0
#         x = 0

#         for row in records:
#             c = c + 1
#             point_view = str(row.latitude) + ',' + str(row.longitude)
#             #             point_view = str(row.sm_client.field1)
#             pSName = str(row.name)
#             if (c == middle):
#                 center_point = point_view
#             if (start_flag == 0):
#                 map_string_name = map_string_name + pSName + \
#                     "," + str(point_view) + ',' + str(x) + 'rdrd'
#                 start_flag = 1
#             else:
#                 map_string_name = map_string_name + pSName + \
#                     "," + str(point_view) + ',' + str(x) + 'rdrd'
#             x = x + 1
# #
# # #         return map_string_name
#         if (map_string_name == ''):
#             map_string_name = 'No Outlet Available' + "," + \
#                 '23.811991,90.422952' + ',' + '0' + 'rdrd'
#             center_point = '23.811991, 90.422952'

# #         return map_string_name
#         return (map_string_name, center_point)


# ===============map show
def outletMap():

    cid = session.cid

    btn_outlet_map = request.vars.btn_outlet_map
#     btn_path_map = request.vars.btn_path_map
#     return btn_outlet_map
    if (btn_outlet_map != None):
        search_valueOutlet_map = request.vars.search_value.strip()

        session.search_valueOutlet_map = str(search_valueOutlet_map).split('|')[-1]
#         return session.search_valueOutlet_map
        session.search_valueOutlet_map_area_name = search_valueOutlet_map

        if ((session.search_valueOutlet_map == '')  or (session.search_valueOutlet_map == None)):
             session.flash = 'Please Select Type and Value'
             redirect(URL('index'))
    # SQL Query    
        area_id = session.search_valueOutlet_map
        # all_record_area_wise_sql = "SELECT * FROM `sm_client` WHERE cid='"+cid+"' and area_id= '"+area_id+"' and latitude IS NOT NULL and longitude IS NOT NULL order by client_id;"
        # return all_record_area_wise_sql

        all_record_area_wise_sql = f"SELECT * FROM `sm_client` WHERE cid = '{cid}' AND area_id = '{area_id}' AND latitude != '' AND longitude != '' ORDER BY client_id;"

        records = db.executesql(all_record_area_wise_sql,as_dict=True)

#         return db._lastsql
        check_total = len(records)
#    #     return check_total
        # x=type(records)
        # return x
        total = 0
        middle = 1
        if check_total:
            total = check_total
            middle = int(round(total / 2))
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

# def arrow_new():
    btn_path_map = request.vars.btn_path_map
    if (btn_path_map != None):

        session.search_date_map = request.vars.to_dt
        search_rep_map = request.vars.rep_id

        session.search_rep_map = str(search_rep_map).split('|')[0]

        records_rep = db((db.sm_rep.cid == session.cid) & (
            db.sm_rep.rep_id == session.search_rep_map)).select(db.sm_rep.name, limitby=(0, 1))
        search_repname_map = ''
        town_code = ''
        for record_rep in records_rep:
            search_repname_map = str(record_rep.name)
#             town_code = str(record_rep.towncode)

#         records_rep_town = db((db.sm_route.cid == session.cid) & (db.sm_route.towncode == town_code)).select(db.sm_route.town, limitby=(0, 1))
#         town_name = ''
#         for record_rep_town in records_rep_town:
#             town_name = str(record_rep_town.town)

        session.search_repname_map = search_repname_map
#        session.search_repname_map = str(search_rep_map).split(':')[1]

#         return session.search_rep_map
        qset = db()
        qset = qset(db.sm_doctor_visit.cid == session.cid)

        if ((session.search_date_map == '') and (session.search_date_map == None) and (session.search_rep_map == '') and (session.search_rep_map == None)):
            session.flash = 'Please Select a Date and Rep'
            redirect(URL('index'))


# ===============Visit path start===============
        qset = qset(db.sm_doctor_visit.visit_date == session.search_date_map)
        qset = qset(db.sm_doctor_visit.rep_id == session.search_rep_map)
#         qset = qset(db.sm_order_head.lastVisitFlag == 1)
        records = qset.select(db.sm_doctor_visit.latitude, db.sm_doctor_visit.longitude,
                              db.sm_doctor_visit.doc_id, db.sm_doctor_visit.doc_name, orderby=db.sm_doctor_visit.id)
#        return db._lastsql
        middle = 1

        map_string_in = ''
        start_flag = 0

        map_string = ''
        map_string_name = ''
        map_string_name_in = ''
        center_point = ''
        show_str_show = ''
        map_string_name_show = ''
        c = 0
        x = 0
    #    return middle
        for row in records:
            #            return  str(row.field1)

            c = c + 1
            end_time = 0
            start_time = 0
            point_view = str(row.latitude)+','+str(row.longitude)
            if (point_view != '0'):
                c_info = str(row.doc_name) + "(" + str(row.doc_id) + ")"
    #           local
#                link_path = """<a href="/""" + str(request.application) + """/showMap/visit_detail/""" + str(row.client_id) + """ " target="_blank"> Show Visit</a>"""
#                show_str = """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.client_id) + """')" value=" """ + c_info + """ ">""" + """</p>""" + link_path + """</br>""" + """StartTime: """ + str(row.start_time) + """</br>""" + """EndTime: """ + str(row.end_time)


#                show_str = """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.doc_id) + """')" value=" """ + c_info + """ ">""" + """</p><a href="http://127.0.0.1:8000/lscmreporting/showMap/visit_detail/""" + str(row.doc_id) + """ " target="_blank">Show Visit</a>""" + """</br>""" + """StartTime: """ + str(start_time) + """</br>""" + """EndTime: """ + str(end_time)

                show_str = str(row.doc_name) + "(" + str(row.doc_id) + ")   "

    #            online
#                 path_l={{=URL(c='showMap',f='showMap',args=[str(row.client_id)])}}
#                 show_str = """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.client_id) + """')" value=" """ + c_info + """ ">""" + """</p><a href="URL(c='showMap',f='showMap',args=[""" + str(row.client_id) + """])" target="_blank">Show Visit</a>""" + """</br>""" + """StartTime: """ + str(row.start_time) + """</br>""" + """EndTime: """ + str(row.end_time)
#                 show_str = """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.client_id) + """')" value=" """ + c_info + """ ">""" + """</p><a href="e.businesssolutionapps.com/lscmreporting/showMap/visit_detail/""" + str(row.client_id) + """ " target="_blank">Show Visit</a>""" + """</br>""" + """StartTime: """ + str(row.start_time) + """</br>""" + """EndTime: """ + str(row.end_time)

                show_str_show = str(row.doc_name) + "(" + str(row.doc_id) + ")   " + "</br>" + \
                    "StartTime: " + str(start_time) + \
                    "</br>" + "EndTime: " + str(end_time)
                time_show = ""
                time_show = show_str

                if (c == middle):
                    center_point = point_view
        #            return str(point_view)
                if (start_flag == 0):
                    map_string_in = map_string_in + \
                        'new google.maps.LatLng(' + str(point_view) + ')'
                    map_string_name = map_string_name + \
                        str(time_show) + "," + str(point_view) + \
                        ',' + str(x) + 'rdrd'

                    map_string_name_show = map_string_name_show + \
                        str(show_str_show) + "," + \
                        str(point_view) + ',' + str(x) + 'rdrd'

        #                map_string_name_in=map_string_name_in+"['nandini',"+str(point_view)+","+str(c)+"]"
                    start_flag = 1
                else:
                    map_string_in = map_string_in + \
                        ',new google.maps.LatLng(' + str(point_view) + ')'
                    map_string_name = map_string_name + \
                        str(time_show) + "," + str(point_view) + \
                        ',' + str(x) + 'rdrd'

                    map_string_name_show = map_string_name_show + \
                        str(show_str_show) + "," + \
                        str(point_view) + ',' + str(x) + 'rdrd'

        #                map_string_name_in=map_string_name_in+",['nandini',"+str(point_view)+","+str(c)+"]"
                x = x + 1

        map_string = '[' + map_string_in + ']'

#        return map_string

#         return dict(map_string=map_string, map_string_name=map_string_name, center_point=center_point)
# ==============Visit path End=======================


# ==============All outlet of visited and actual route=============


#        rows_check_route = db((db.sm_visit_plan.cid == session.cid) & (db.sm_visit_plan.rep_id == session.search_rep_map) & (db.sm_visit_plan.schedule_date == session.search_date_map)) .select(db.sm_visit_plan.route_id, groupby=db.sm_visit_plan.route_id , orderby=db.sm_visit_plan.route_id)
#
        route_list = []
#        planned_route = ''
#        for row_visit in rows_check_route:
#            if (planned_route == ''):
#                planned_route = str(row_visit.route_id).strip().upper()
#            else:
#                planned_route = planned_route + ',' + str(row_visit.route_id).strip().upper()
#            route_list.append(str(row_visit.route_id).strip().upper())


#        routeRows = db((db.sm_order_head.cid == session.cid) & (db.sm_order_head.rep_id == session.search_rep_map) & (db.sm_order_head.order_date == session.search_date_map) & (db.sm_order_head.visit_type == 'Unscheduled')) .select(db.sm_order_head.area_id, groupby=db.sm_order_head.area_id , orderby=db.sm_order_head.area_id)
# return db._lastsql
#        visit_route = ''
#        for routeRow in routeRows:
#            if (visit_route == ''):
#                visit_route = str(routeRow.area_id).strip().upper()
#            else:
#                visit_route = visit_route + ',' + str(routeRow.area_id).strip().upper()
#            route_list.append(str(routeRow.area_id).strip().upper())
# return planned_route
#        rows_check_station = db((db.sm_doctor.cid == session.cid) & (db.sm_client.latitude != '0') & (db.sm_client.longitude != '0') & (db.sm_client.area_id.belongs(route_list))).select(db.sm_client.client_id, db.sm_client.name, db.sm_client.latitude, db.sm_client.longitude, orderby=db.sm_client.client_id)
        rows_check_station = db((db.sm_doctor_area.cid == session.cid) & (db.sm_doctor_area.field1 != '0')).select(
            db.sm_doctor_area.doc_id, db.sm_doctor_area.doc_name, db.sm_doctor_area.field1, orderby=db.sm_doctor_area.doc_id)
        start_flag_p = 0
        map_string_name_p = ''

        p = 0

        for row_p in rows_check_station:
            point_view = str(row_p.field1)
            c_info_ps = str(row_p.doc_name) + "( " + str(row_p.doc_id) + " )"

#                pSName = """<input type="submit" style="width:400px;height=40px" onClick="show_dialog('""" + str(row_p.doc_id) + """')" value=" """ + c_info_ps + """ ">"""

            pSName = c_info_ps

            if (start_flag_p == 0):
                map_string_name_p = map_string_name_p + pSName + \
                    "," + str(point_view) + ',' + str(x) + 'rdrd'
                start_flag_p = 1
            else:
                map_string_name_p = map_string_name_p + pSName + \
                    "," + str(point_view) + ',' + str(x) + 'rdrd'

#         return map_string_name
#         return dict(map_string=map_string, map_string_name=map_string_name, center_point=center_point, map_string_ac=map_string_ac, map_string_name_ac=map_string_name_ac)

        if (map_string_name == ''):
            session.flash = 'Result Not Available'
            redirect(URL(c='showMap_doctor', f='index'))
#        return map_string_ac
#        return map_string_name
#        return dict(map_string=map_string, map_string_name=map_string_name, center_point=center_point ,map_string_name_p=map_string_name_p)
        map_string_name_ac = ''
        map_string_name_po = ''
        map_string_name_pl = ''
        map_string_name_unpl = ''
        map_string_name_show = map_string_name
        return dict(map_string=map_string, map_string_name=map_string_name, center_point=center_point, map_string_name_p=map_string_name_p, map_string_name_ac=map_string_name_ac, map_string_name_po=map_string_name_po, map_string_name_pl=map_string_name_pl, map_string_name_unpl=map_string_name_unpl)


# def visit_detail():
    client_id = request.args[0]
#    return client_id
    visit_checks = db((db.sm_order_head.cid == session.cid) & (db.sm_order_head.order_date == session.search_date_map) & (
        db.sm_order_head.rep_id == session.search_rep_map) & (db.sm_order_head.client_id == client_id)).select(db.sm_order_head.id, orderby=~db.sm_order_head.id)

    visit_id = '0'
    page = 0
    for visit_check in visit_checks:
        visit_id = str(visit_check.id).strip()
    if (visit_id == '0'):
        session.flash = 'Result Not Available'
        redirect(URL(c='showMap', f='index'))
    else:
        redirect(URL(c='client_visit', f='visit_details',
                 args=[page], vars=dict(vsl=visit_id)))
#        lacal
#         redirect ('http://127.0.0.1:8000/lscmreporting/client_visit/visit_details/0?vsl=' + visit_id)
#        online
#         redirect ('e.businesssolutionapps.com/lscmreporting/client_visit/visit_details/0?vsl=' + visit_id)


#                (URL(c='client_visit',f='visit_details',args=[page,visit_id],vars=dict(vsl=visit_id))

# def client_detail():
    client_id = request.args[0]
#    return client_id
    client_checks = db((db.sm_client.cid == session.cid) & (db.sm_client.client_id == client_id)).select(
        db.sm_client.ALL, orderby=~db.sm_client.id, limitby=(0, 1))
#    return db._lastsql
    id = '0'
    client_id = ''
    name = ''
    contact_no1 = ''
    contact_no1 = ''
    shop_size = ''
    shop_front_size = ''
    lsc_covered = ''
    shop_owner_status = ''
    owner_name = ''
    order_date = ''
    address = ''
    area_id = ''
    for client_check in client_checks:
        id = str(client_check.id).strip()
        client_id = str(client_check.client_id).strip()
        name = str(client_check.name).strip()
        contact_no1 = str(client_check.contact_no1).strip()
        contact_no1 = str(client_check.contact_no1).strip()
        shop_size = str(client_check.shop_size).strip()
        shop_front_size = str(client_check.shop_front_size).strip()
        lsc_covered = str(client_check.lsc_covered).strip()
        shop_owner_status = str(client_check.shop_owner_status).strip()
        owner_name = str(client_check.owner_name).strip()
        address = str(client_check.address).strip()
        area_id = str(client_check.area_id).strip()
        photo = str(client_check.photo).strip()

    if (area_id != ''):
        area_name = ''
        area_checks = db((db.sm_level.cid == session.cid) & (db.sm_level.level_id == area_id)).select(
            db.sm_level.level_name, orderby=~db.sm_level.id, limitby=(0, 1))
        for area_check in area_checks:
            area_name = str(area_check.level_name).strip()


#    return order_date
    if (client_id == '0'):
        str_show = 'Result Not Available'

    else:
        str_show = """
                </br>
                <div style=" border:2px #CCCCCC; border-radius:5px; background-color:#000; box-shadow:3px 3px 5px #CCCCCC; text-align:center; color:#E9E9E9;width:150px; height:100px;">""" + """<img src="http://i01.businesssolutionapps.com/lscrmap_image/static/client_pic/""" + photo + """ "   style="width:100px; height:100px;" alt="Image" /></div>
                 </br> 
                  <table width="100%" class="blackCat">
                 
                      <tr>
                        
                        <td style="font-size:14px; font-weight:bold">""" + name + """&nbsp; (&nbsp; """ + client_id + """ &nbsp;) </td>
                        </tr>
                        
                     
                      <tr>
                        
                        <td>""" + area_name + """&nbsp; (&nbsp; """ + area_id + """ &nbsp;) </td>
                        </tr>
                      <tr>
                      
        
                        <td>""" + contact_no1 + """</td>
                        </tr>
                      
                     
                      <tr>
                       
                        <td>""" + owner_name + """</td>
                      </tr>
                      
                      
                      
                      <tr>
                      """
        if (lsc_covered == 'YES'):
            str_show = str_show + """ 
                        <td>LSC Covered <img src="   """ + URL('static', 'images/v_green.png') + """     " /> """ + """</td>"""
        else:
            str_show = str_show + """ 
                        <td>LSC Noncovered <img src="   """ + URL('static', 'images/v_red.png') + """     " /> """ + """</td>"""

        str_show = str_show + """ 
                    </tr>
                      
                      <tr>
                        
                        <td>Shop  -  """ + shop_owner_status + """</td>
                      </tr>

                      <tr>
                        
                        <td>Shop Size (sqft)  """ + shop_size + """</td>
                      </tr>
                      <tr>
                        
                        <td>Shop Front Size (ft)""" + shop_front_size + """</td>
                      </tr>
                      
                    <tr>
                            <td ><strong>Last Visit Info</strong></td>
                           
                        </tr>                  
                        <tr>
                           
                            <td>Visit date: """ + session.search_date_map + """</td>
                        </tr>
                        <tr>
                         
                          <td>Visited by: """ + session.search_repname_map + """(""" + session.search_rep_map + """)""" + """</td>
                        </tr>
                        </table>
                   """


#                        <tr>
#                          <td width="80">Mobile No</td>
#                          <td>: {{=mobile_no}}</td>
#                        </tr>
#                        <tr>
#                          <td width="80">Visit Type</td>
#                          <td>: {{=visit_type}}</td>
#                        </tr>
#                        <tr>
#                          <td width="80">Visit Sl</td>
#                          <td>: {{=sl}}</td>
#                        </tr>
#                    </table>
#                   """

#        str_show='Nadira'
        return str_show


# def client_detail_outlet():

#     client_id = request.args[0]
# #    return client_id
#     client_checks = db((db.sm_client.cid == session.cid) & (db.sm_client.client_id == client_id)).select(
#         db.sm_client.ALL, orderby=~db.sm_client.id, limitby=(0, 1))
# #    return db._lastsql
#     id = '0'
#     client_id = ''
#     name = ''
#     contact_no1 = ''
#     contact_no1 = ''
#     shop_size = ''
#     shop_front_size = ''
#     lsc_covered = ''
#     shop_owner_status = ''
#     owner_name = ''
#     order_date = ''
#     address = ''
#     area_id = ''
#     for client_check in client_checks:
#         id = str(client_check.id).strip()
#         client_id = str(client_check.client_id).strip()
#         name = str(client_check.name).strip()
#         contact_no1 = str(client_check.contact_no1).strip()
#         contact_no1 = str(client_check.contact_no1).strip()
#         shop_size = str(client_check.shop_size).strip()
#         shop_front_size = str(client_check.shop_front_size).strip()
#         lsc_covered = str(client_check.lsc_covered).strip()
#         shop_owner_status = str(client_check.shop_owner_status).strip()
#         owner_name = str(client_check.owner_name).strip()
#         address = str(client_check.address).strip()
#         area_id = str(client_check.area_id).strip()
#         photo = str(client_check.photo).strip()

#     if (area_id != ''):
#         area_name = ''
#         area_checks = db((db.sm_level.cid == session.cid) & (db.sm_level.level_id == area_id)).select(
#             db.sm_level.level_name, orderby=~db.sm_level.id, limitby=(0, 1))
#         for area_check in area_checks:
#             area_name = str(area_check.level_name).strip()


# #    return order_date
#     if (client_id == '0'):
#         str_show = 'Result Not Available'

#     else:
#         str_show = """
#                 </br>
#                 <div style=" border:2px #CCCCCC; border-radius:5px; background-color:#000; box-shadow:3px 3px 5px #CCCCCC; text-align:center; color:#E9E9E9;width:150px; height:100px;">""" + """<img src="http://i01.businesssolutionapps.com/lscrmap_image/static/client_pic/""" + photo + """ "   style="width:100px; height:100px;" alt="Image" /></div>
#                  </br> 
#                   <table width="100%" class="blackCat">
                 
#                       <tr>
                        
#                         <td style="font-size:14px; font-weight:bold">""" + name + """&nbsp; (&nbsp; """ + client_id + """ &nbsp;) </td>
#                         </tr>
                        
                     
#                       <tr>
                        
#                         <td>""" + area_name + """&nbsp; (&nbsp; """ + area_id + """ &nbsp;) </td>
#                         </tr>
#                       <tr>
                      
        
#                         <td>""" + contact_no1 + """</td>
#                         </tr>
                      
                     
#                       <tr>
                       
#                         <td>""" + owner_name + """</td>
#                       </tr>
                      
                      
                      
#                       <tr>
#                       """
#         if (lsc_covered == 'YES'):
#             str_show = str_show + """ 
#                         <td>LSC Covered <img src="   """ + URL('static', 'images/v_green.png') + """     " /> """ + """</td>"""
#         else:
#             str_show = str_show + """ 
#                         <td>LSC Noncovered <img src="   """ + URL('static', 'images/v_red.png') + """     " /> """ + """</td>"""

#         str_show = str_show + """ 
#                     </tr>
                      
#                       <tr>
                        
#                         <td>Shop  -  """ + shop_owner_status + """</td>
#                       </tr>

#                       <tr>
                        
#                         <td>Shop Size (sqft)  """ + shop_size + """</td>
#                       </tr>
#                       <tr>
                        
#                         <td>Shop Front Size (ft)""" + shop_front_size + """</td>
#                       </tr>
                      
                    
#                         </table>
#                    """

#         return str_show


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



