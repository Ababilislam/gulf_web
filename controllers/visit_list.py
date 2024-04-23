#http://127.0.0.1:8000/gulf_web/visit_list/show_visit_list?cid=GULF&user_id=100078&user_pass=123456Aa@&visit_type=NO_ORDER


# http://127.0.0.1:8001/gulf_web/visit_list/show_visit_list_url?cid=GULF&user_id=100078&user_pass=1234&call_type=NO ORDER

# http://127.0.0.1:8001/gulf_web/visit_list/show_visit_list_url?cid=GULF&user_id=100078&user_pass=1234&call_type=VISIT

# http://192.168.0.108:8000/gulf_web/visit_list/show_visit_list_url?cid=GULF&user_id=100078&user_pass=12345&call_type=VISIT


# http://192.168.0.108:8000/gulf_web/visit_list/show_visit_list_url?cid=GULF&user_id=100078&user_pass=12345&call_type=VISIT
# http://192.168.0.108:8000/gulf_web/visit_list/show_visit_list_url?cid=GULF&user_id=100078&user_pass=12345&call_type=NO ORDER



import datetime
def show_visit_list_url():
    cid = request.vars.cid
    user_id = request.vars.user_id
    password = request.vars.user_pass
    call_type = request.vars.call_type
    session.cid = cid
    session.user_id = user_id
    session.password = password
    session.call_type = call_type
    from_date =str(date_fixed).split(' ')[0]
    to_date =str(date_fixed).split(' ')[0]
    session.from_date = from_date
    session.to_date = to_date
    # return session.call_type
    
    if (cid == '' or cid == 'NONE' or cid is None) or (user_id == '' or user_id == 'None' or user_id is None) or (password == '' or password == 'None' or password is None):
        response.flash ="required all fields"
      
    elif call_type == "" or call_type == "None" or call_type == None:
        response.flash ="call type required"
        
        
    userRecords = 'SELECT rep_id, name as rep_name FROM sm_rep WHERE cid = "'+cid+'" AND rep_id = "' +str(user_id)+ '" AND password = "' +str(password)+ '" AND status = "ACTIVE" LIMIT 0,1;' 
    # return userRecords
   
    
    userRecords = db.executesql(userRecords, as_dict=True)
    if len(userRecords) == 0:
        response.flash ="Invalid User" 
         
    else:
        redirect(URL(c='visit_list',f='show_visit_list'))
        


def show_visit_list():
    cid = session.cid
    user_id = session.user_id
    call_type = session.call_type
    from_date=session.from_date 
    to_date=session.to_date
    # return session.from_date, session.to_date
    # return call_type

    date_condition = "AND visit_date BETWEEN '"+str(from_date)+"' AND '"+str(to_date)+"' "
    visit_data_record = ''
    btn_filter =str(request.vars.btn_filter)
    btn_all =str(request.vars.btn_all)
    if btn_filter == 'Filter':
        from_date = str(request.vars.from_date).strip().replace('None', '')
        to_date= str(request.vars.to_date).strip().replace('None', '')
        session.from_date = from_date
        session.to_date = to_date
        if from_date != "" and to_date != "":
            date_condition = "AND visit_date BETWEEN '"+str(from_date)+"' AND '"+str(to_date)+"' " 

    elif btn_all == 'All':
        current_date=date_fixed
        from_date =(current_date - datetime.timedelta(days=current_date.day)).replace(day=current_date.day).strftime('%Y-%m-%d')
        to_date = str(date_fixed).split(' ')[0]
        session.from_date =from_date
        session.to_date = to_date
        date_condition ="AND visit_date BETWEEN '"+str(from_date)+"' AND '"+str(to_date)+"' "
    
    #visit_data_record_sql = "SELECT area_id,area_name, rep_id, rep_name, visited_id, visited_name, visit_Type, visit_date, location_detail FROM sm_tracking_table WHERE cid = '"+cid+"'  "+date_condition+" and call_type = '"+str(call_type)+"';"
    visit_data_record_sql = "SELECT area_id,area_name, rep_id, rep_name, territory_id, territory_name, zone_id, zone_name, call_type, visit_date, location_detail FROM sm_tracking_live2 WHERE cid = '"+cid+"'  "+date_condition+" and call_type = '"+str(call_type)+"';"
    visit_data_record = db.executesql(visit_data_record_sql, as_dict=True)
    # return call_type     
    return dict(visit_data_record=visit_data_record, cid=cid,rep_id=user_id,call_type=call_type)



    
