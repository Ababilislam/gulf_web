# import urllib2

# import urllib2
# Validation
def index():
    task_id = 'rm_analysis_view'
    access_permission = check_role(task_id)
    if (access_permission == False):
        session.flash = 'Access is Denied'
        redirect (URL('default', 'home'))

    response.title = 'Map'

    search_form = SQLFORM(db.sm_search_date)
    return dict(search_form=search_form)



def outletMap_mobile():

    cid = session.cid

    btn_outlet_map = request.vars.btn_outlet_map
#     btn_path_map = request.vars.btn_path_map
#     return btn_outlet_map
    if (btn_outlet_map != None):
        search_valueOutlet_map = request.vars.search_value.strip()

        session.search_valueOutlet_map = str(search_valueOutlet_map).split('|')[0]
#         return session.search_valueOutlet_map


        if ((session.search_valueOutlet_map == '')  or (session.search_valueOutlet_map == None)):
             session.flash = 'Please Select Type and Value'
             redirect(URL('index'))

        
        qset = db()
        qset = qset(db.sm_client.cid == cid)
        qset = qset(db.sm_client.area_id == session.search_valueOutlet_map)
        qset = qset(db.sm_client.latitude != '0')
        qset = qset(db.sm_client.longitude != '0')

        records = qset.select(db.sm_client.ALL, orderby=db.sm_client.client_id)

        check_total = len(records)

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
            point_view = str(row.latitude) + ',' + str(row.longitude)            
            pSName = str(row.name)
            
            if (c == middle):
                center_point = point_view
            
            if (start_flag == 0):
                map_string_name = map_string_name + pSName + "," + str(point_view) + ',' + str(x) + 'rdrd'
                start_flag = 1
            else:
                map_string_name = map_string_name + pSName + "," + str(point_view) + ',' + str(x) + 'rdrd'
            x = x + 1

        
        if (map_string_name == ''):
            map_string_name = 'No Outlet Available' + "," + '23.811991,90.422952' + ',' + '0' + 'rdrd'
            center_point = '23.811991, 90.422952'

        return (map_string_name, center_point)




# ===============map show
def outletMap():

    cid = session.cid

    btn_outlet_map = request.vars.btn_outlet_map
#     btn_path_map = request.vars.btn_path_map
#     return btn_outlet_map
    if (btn_outlet_map != None):
        search_valueOutlet_map = request.vars.search_value.strip()

        session.search_valueOutlet_map = str(search_valueOutlet_map).split('|')[0]
#         return session.search_valueOutlet_map
        session.search_valueOutlet_map_show = search_valueOutlet_map

        if ((session.search_valueOutlet_map == '')  or (session.search_valueOutlet_map == None)):
             session.flash = 'Please Select Type and Value'
             redirect(URL('index'))
#
#        # Set query based on search type
        qset = db()
        qset = qset(db.sm_client.cid == cid)

        qset = qset(db.sm_client.area_id == session.search_valueOutlet_map)
        qset = qset(db.sm_client.latitude != '0')
        qset = qset(db.sm_client.longitude != '0')

        records = qset.select(db.sm_client.ALL, orderby=db.sm_client.client_id)

#         return db._lastsql
        check_total = len(records)
#    #     return check_total
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
            point_view = str(row.latitude) + ',' + str(row.longitude)
            #             point_view = str(row.sm_client.field1)
            pSName = str(row.name)
            c_info = str(row.name) + "(" + str(row.client_id) + ")"


#                show_str = """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.client_id) + """')" value=" """ + c_info + """ ">""" + """</p>""" + link_path + """</br>""" + """StartTime: """ + str(row.start_time) + """</br>""" + """EndTime: """ + str(row.end_time)
            if (c == middle):
                center_point = point_view
            if (start_flag == 0):
                map_string_name = map_string_name + """<input type="submit" style="width:400px" """+ str(row.client_id) + """ value=" """ + c_info + """ ">""" + """,""" + str(point_view) + """,""" + str(x) + """rdrd"""
#                map_string_name = map_string_name + """<input type="submit" style="width:400px" onClick="show_dialog('""" + str(row.client_id) + """')" value=" """ + c_info + """ ">""" + """,""" + str(point_view) + """,""" + str(x) + """rdrd"""
                start_flag = 1
            else:
                map_string_name = map_string_name + """<input type="submit" style="width:400px" """ + str(row.client_id) + """ value=" """ + c_info + """ ">""" + """,""" + str(point_view) + """,""" + str(x) + """rdrd"""
            x = x + 1
#
#         return map_string_name
        if (map_string_name == ''):
#             map_string_name = 'No Outlet Available' + "," + '23.811991,90.422952' + ',' + '0' + 'rdrd'
#             center_point = '23.811991, 90.422952'
            session.flash = 'Result Not Available'
            redirect(URL('index'))

        return dict(map_string_name=map_string_name, center_point=center_point)







def arrow_new():
    
    btn_path_map = request.vars.btn_path_map
    
    if (btn_path_map != None):

        session.search_date_map = request.vars.to_dt
        search_rep_map = request.vars.rep_id

        session.search_rep_map = str(search_rep_map).split('|')[0]

        records_rep = db((db.sm_rep.cid == session.cid) & (db.sm_rep.rep_id == session.search_rep_map)).select(db.sm_rep.name, limitby=(0, 1))
        search_repname_map = ''
        town_code = ''
        for record_rep in records_rep:
            search_repname_map = str(record_rep.name)

        session.search_repname_map = search_repname_map


        qset = db()
        qset = qset(db.sm_tracking_live2.cid == session.cid)

        if ((session.search_date_map == '') and (session.search_date_map == None) and (session.search_rep_map == '') and (session.search_rep_map == None)):
            session.flash = 'Please Select a Date and Rep'
            redirect(URL('index'))

# ===============Visit path start===============

        qset = qset(db.sm_tracking_live2.visit_date == session.search_date_map)
        qset = qset(db.sm_tracking_live2.rep_id == session.search_rep_map)
        # qset = qset(db.sm_tracking_live2.call_type == 'TRACK')
        # return session.search_date_map 
        records = qset.select(db.sm_tracking_live2.visited_latlong,db.sm_tracking_live2.rep_id,db.sm_tracking_live2.rep_name,db.sm_tracking_live2.visit_time, orderby=db.sm_tracking_live2.id)
        # return db._lastsql
        
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
            end_time=0
            start_time=0
            # point_view = str(row.latitude)+','+str(row.longitude)
            point_view = str(row.visited_latlong)
            
            if (point_view != '0'):

                c_info = str(row.rep_name) + "(" + str(row.rep_id) + ")"
  
                show_str =  str(row.visit_time) 
                
                show_str_show = str(row.rep_name) + "(" + str(row.rep_id) + ")   " 
                
                time_show = ""
                time_show = show_str
                
                if (c == middle):
                    center_point = point_view
        #            return str(point_view)
                if (start_flag == 0):
                    map_string_in = map_string_in + 'new google.maps.LatLng(' + str(point_view) + ')'
                    map_string_name = map_string_name + str(time_show) + "," + str(point_view) + ',' + str(x) + 'rdrd'


                    map_string_name_show = map_string_name_show + str(show_str_show) + "," + str(point_view) + ',' + str(x) + 'rdrd'
                    start_flag = 1
                else:
                    map_string_in = map_string_in + ',new google.maps.LatLng(' + str(point_view) + ')'
                    map_string_name = map_string_name + str(time_show) + "," + str(point_view) + ',' + str(x) + 'rdrd'


                    map_string_name_show = map_string_name_show + str(show_str_show) + "," + str(point_view) + ',' + str(x) + 'rdrd'

                
                x = x + 1

        map_string = '[' + map_string_in + ']'


        route_list = []
       

        rows_check_station = db((db.sm_rep_area.cid == session.cid)).select(db.sm_rep_area.rep_id,db.sm_rep_area.rep_name,db.sm_rep_area.field1, orderby=db.sm_rep_area.rep_id)
        
        start_flag_p = 0
        map_string_name_p = ''

        p = 0

        for row_p in rows_check_station:
                point_view = str(row_p.field1)
                c_info_ps = str(row_p.rep_name) + "( " + str(row_p.rep_id) + " )"


                pSName=c_info_ps

                if (start_flag_p == 0):
                    map_string_name_p = map_string_name_p + pSName + "," + str(point_view) + ',' + str(x) + 'rdrd'
                    start_flag_p = 1
                else:
                    map_string_name_p = map_string_name_p + pSName + "," + str(point_view) + ',' + str(x) + 'rdrd'



        if (map_string_name == ''):
            session.flash = 'Result Not Available'
            redirect (URL(c='tracking_emp', f='index'))

       
        map_string_name_ac=''
        map_string_name_po=''
        map_string_name_pl=''
        map_string_name_unpl=''
        map_string_name_show=map_string_name
        
        return dict(map_string=map_string, map_string_name=map_string_name, center_point=center_point ,map_string_name_p=map_string_name_p,map_string_name_ac=map_string_name_ac, map_string_name_po=map_string_name_po, map_string_name_pl=map_string_name_pl,map_string_name_unpl=map_string_name_unpl)




def visit_detail():
    client_id = request.args[0]
#    return client_id
    visit_checks = db((db.sm_order_head.cid == session.cid) & (db.sm_order_head.order_date == session.search_date_map) & (db.sm_order_head.rep_id == session.search_rep_map) & (db.sm_order_head.client_id == client_id)).select(db.sm_order_head.id, orderby= ~db.sm_order_head.id)

    visit_id = '0'
    page = 0
    for visit_check in visit_checks:
        visit_id = str(visit_check.id).strip()
    if (visit_id == '0'):
        session.flash = 'Result Not Available'
        redirect(URL(c='showMap', f='index'))
    else:
        redirect (URL(c='client_visit', f='visit_details', args=[page], vars=dict(vsl=visit_id)))
#        lacal
#         redirect ('http://127.0.0.1:8000/lscmreporting/client_visit/visit_details/0?vsl=' + visit_id)
#        online
#         redirect ('e.businesssolutionapps.com/lscmreporting/client_visit/visit_details/0?vsl=' + visit_id)


#                (URL(c='client_visit',f='visit_details',args=[page,visit_id],vars=dict(vsl=visit_id))

def client_detail():
    client_id = request.args[0]
#    return client_id
    client_checks = db((db.sm_client.cid == session.cid) & (db.sm_client.client_id == client_id)).select(db.sm_client.ALL, orderby= ~db.sm_client.id , limitby=(0, 1))
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
        area_checks = db((db.sm_level.cid == session.cid) & (db.sm_level.level_id == area_id)).select(db.sm_level.level_name, orderby= ~db.sm_level.id , limitby=(0, 1))
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



def client_detail_outlet():
    client_id = request.args[0]
#    return client_id
    client_checks = db((db.sm_client.cid == session.cid) & (db.sm_client.client_id == client_id)).select(db.sm_client.ALL, orderby= ~db.sm_client.id , limitby=(0, 1))
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
        area_checks = db((db.sm_level.cid == session.cid) & (db.sm_level.level_id == area_id)).select(db.sm_level.level_name, orderby= ~db.sm_level.id , limitby=(0, 1))
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
                      
                    
                        </table>
                   """




        return str_show
