from datetime import datetime

def level():
    if (session.cid=='' or session.cid==None):
        redirect (URL('default','index'))
    depth = request.vars.depth
    if depth ==None or depth =='None':
        depth = 0
    depth = int(depth)
    
    response.title='Area Structure'
    c_id= session.cid
    
    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    btn_search =request.vars.btn_search
    if btn_search:
        level_id = request.vars.level_search
        if level_id == "" or level_id == None:
            response.flash='Please select level !'
        else:
            search_level_sql = f"select * from sm_level where level_id ='{level_id}' limit 1;"
            session.level_search=level_id
            try:
                search_level = db.executesql(search_level_sql,as_dict=True)
                if len(search_level) > 0:
                    search_level=search_level[0]
            
                depth = search_level["depth"]
                
                if depth == 0:
                    item_id = search_level["id"]
                    
                    parent_id= search_level["parent_level_id"]
                    parent_name= search_level["parent_level_name"]
                    
                    national_id= search_level["level_id"]
                    national_name= search_level["level_name"]
                    get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id='0'  GROUP BY level0;"
                    level_records = db.executesql(get_level_list_sql, as_dict = True)
                    return dict(level_records = level_records,parent_id=parent_id,parent_name=parent_name,national_id=national_id,national_name=national_name,depth = depth,item_id=item_id)
                    
                if depth == 1:
                    item_id = search_level["id"]
                    
                    parent_id= search_level["parent_level_id"]
                    parent_name= search_level["parent_level_name"]
                    
                    national_id= search_level["parent_level_id"]
                    national_name= search_level["parent_level_name"]
                    
                    divisional_id= search_level["level_id"]
                    divisional_name= search_level["level_name"]
                    get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id='"+str(parent_id)+"'  GROUP BY level1,level0;"
                    # return get_level_list_sql
                    level_records = db.executesql(get_level_list_sql, as_dict = True)
                    return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,national_id=national_id,national_name=national_name,divisional_id=divisional_id,divisional_name=divisional_name,item_id=item_id)

                if depth == 2:
                    item_id = search_level["id"]
                    
                    parent_id= search_level["parent_level_id"]
                    parent_name= search_level["parent_level_name"]
                    
                    national_id= search_level["level0"]
                    national_name= search_level["level0_name"]
                    
                    divisional_id= search_level["parent_level_id"]
                    divisional_name= search_level["parent_level_name"]
                    
                    distributor_id= search_level["level_id"]
                    distributor_name= search_level["level_name"]
                    get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id = '"+str(parent_id)+"' GROUP BY level2,level1,level0;"
                    # return get_level_list_sql
                    level_records = db.executesql(get_level_list_sql, as_dict = True)
                    return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,national_id=national_id,national_name=national_name,divisional_id=divisional_id,divisional_name=divisional_name,distributor_id=distributor_id,distributor_name=distributor_name,item_id=item_id)
            except:
                response.flash=f'Invalid level ID: {level_id} !'
                
    
    if depth == 0:
        submit_btn=request.vars.submit
        update_btn=request.vars.update_btn
        delete_btn=request.vars.delete_btn
        
        parent_id= 0
        parent_name= ''
        
        
        national_id= request.vars.national_id
        national_name= request.vars.national_name
        
        if submit_btn:
            if national_id == '' or national_id == 'None' or national_id==None:
                response.flash='Please enter the national ID!'
            elif national_name == '' or national_name == 'None' or national_name==None:
                response.flash='Please enter the national Name!'
            elif check_level_id(national_id) == True:
                response.flash='Level id already exists!'
            else:
                insert_national_sql="INSERT INTO sm_level (cid,level_id,level_name,parent_level_id,parent_level_name,is_leaf,depth,level0,level0_name,created_on,created_by) VALUES ('"+str(c_id)+"','"+str(national_id)+"','"+str(national_name)+"','0','','0','0','"+str(national_id)+"','"+str(national_name)+"','"+str(current_date_time)+"','"+str(session.user_id)+"');"
                inset_national=db.executesql(insert_national_sql)
                response.flash='Successfully saved!'

        if update_btn:
            item_id = request.vars.item_id
            update_level_sql = "UPDATE sm_level SET level_name = '"+str(national_name)+"' , level0_name = '"+str(national_name)+"', updated_on = '"+str(current_date_time)+"', updated_by = '"+str(session.user_id)+"' WHERE id = '"+str(item_id)+"' ;"
            db.executesql(update_level_sql)
            response.flash='Update Successfully!'
        if delete_btn:
            item_id = request.vars.item_id
            child_level = check_child_level(depth,national_id)
            if child_level:
                response.flash='Delete child level first !'
            else:
                delete_level_sql = "DELETE FROM sm_level WHERE id = '"+str(item_id)+"' ;"
                db.executesql(delete_level_sql)
                response.flash='Delete Successfully!'

        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id='0'  GROUP BY level0;"
        level_records = db.executesql(get_level_list_sql, as_dict = True)
        return dict(level_records = level_records,parent_id=parent_id,parent_name=parent_name,national_id=national_id,national_name=national_name,depth = depth)
    elif depth == 1:
        submit_btn=request.vars.submit
        update_btn=request.vars.update_btn
        delete_btn=request.vars.delete_btn
        
        parent_id= request.vars.national_id
        parent_name= request.vars.national_name
        
        national_id= request.vars.national_id
        national_name= request.vars.national_name
        
        divisional_id= request.vars.divisional_id
        divisional_name= request.vars.divisional_name

        if submit_btn:
            
            if divisional_id == '' or divisional_id == 'None' or divisional_id==None:
                response.flash='Please enter the divisional ID!'
            elif divisional_name == '' or divisional_name == 'None' or divisional_name==None:
                response.flash='Please enter the divisional Name!'
            elif check_level_id(divisional_id) == True:
                response.flash='Level id already exists!'
            else:
                insert_nat_sql="INSERT INTO sm_level (cid,level_id,level_name,parent_level_id,parent_level_name,is_leaf,depth,level0,level0_name,level1,level1_name,created_on,created_by) VALUES ('"+str(c_id)+"','"+str(divisional_id)+"','"+str(divisional_name)+"','"+str(parent_id)+"','"+str(parent_name)+"','0','1','"+str(parent_id)+"','"+str(parent_name)+"','"+str(divisional_id)+"','"+str(divisional_name)+"','"+str(current_date_time)+"','"+str(session.user_id)+"');"
                inset_nat=db.executesql(insert_nat_sql)
                response.flash='Successfully saved!'
                   

        if update_btn:
            item_id = request.vars.item_id
            update_level_sql = "UPDATE sm_level SET level_name = '"+str(divisional_name)+"',level1_name = '"+str(divisional_name)+"', updated_on = '"+str(current_date_time)+"', updated_by = '"+str(session.user_id)+"' WHERE id = '"+str(item_id)+"' ;"
            db.executesql(update_level_sql)
            response.flash='Update Successfully!'
        if delete_btn:
            item_id = request.vars.item_id
            child_level = check_child_level(depth,divisional_id)
            if child_level:
                response.flash='Delete child level first !'
            else:
                delete_level_sql = "DELETE FROM sm_level WHERE id = '"+str(item_id)+"' ;"
                db.executesql(delete_level_sql)
                response.flash='Delete Successfully!'  

        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id='"+str(parent_id)+"'  GROUP BY level1,level0;"
        # return get_level_list_sql
        level_records = db.executesql(get_level_list_sql, as_dict = True)
        return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,national_id=national_id,national_name=national_name,divisional_id=divisional_id,divisional_name=divisional_name)
    elif depth == 2:
        submit_btn=request.vars.submit
        update_btn=request.vars.update_btn
        delete_btn=request.vars.delete_btn
        
        parent_id= request.vars.divisional_id
        parent_name= request.vars.divisional_name
        
        national_id= request.vars.national_id
        national_name= request.vars.national_name
        
        divisional_id= request.vars.divisional_id
        divisional_name= request.vars.divisional_name
        
        distributor_id= request.vars.distributor_id
        distributor_name= request.vars.distributor_name


        if submit_btn:
            
            if distributor_id == '' or distributor_id == 'None' or distributor_id==None:
                response.flash='Please enter the distributor ID!'
            elif distributor_name == '' or distributor_name == 'None' or distributor_name==None:
                response.flash='Please enter the distributor Name!'
            elif check_level_id(distributor_id) == True:
                response.flash='Level id already exists!'
            else:
                insert_nat_sql="INSERT INTO sm_level (cid,level_id,level_name,parent_level_id,parent_level_name,is_leaf,depth,level0,level0_name,level1,level1_name,level2,level2_name,created_on,created_by) VALUES ('"+str(c_id)+"','"+str(distributor_id)+"','"+str(distributor_name)+"','"+str(parent_id)+"','"+str(parent_name)+"','1','2','"+str(national_id)+"','"+str(national_name)+"','"+str(divisional_id)+"','"+str(divisional_name)+"','"+str(distributor_id)+"','"+str(distributor_name)+"','"+str(current_date_time)+"','"+str(session.user_id)+"');"
                inset_nat=db.executesql(insert_nat_sql)
                response.flash='Successfully saved!'

        if update_btn:
            item_id = request.vars.item_id
            distributor_name= request.vars.distributor_name
            update_level_sql = "UPDATE sm_level SET level_name = '"+str(distributor_name)+"',level2_name = '"+str(distributor_name)+"', updated_on = '"+str(current_date_time)+"', updated_by = '"+str(session.user_id)+"' WHERE id = '"+str(item_id)+"' ;"
            update_level=db.executesql(update_level_sql)
            response.flash='Update Successfully!'
        if delete_btn:
            item_id = request.vars.item_id
            child_level = check_child_level(depth,distributor_id)
            if child_level:
                response.flash='Delete child level first !'
            else:
                delete_level_sql = "DELETE FROM sm_level WHERE id = '"+str(item_id)+"' ;"
                db.executesql(delete_level_sql)
                response.flash='Delete Successfully!'

        get_level_list_sql = "SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and parent_level_id = '"+str(parent_id)+"' GROUP BY level2,level1,level0;"
        # return get_level_list_sql
        level_records = db.executesql(get_level_list_sql, as_dict = True)
        return dict(level_records=level_records,depth = depth,parent_id=parent_id,parent_name=parent_name,national_id=national_id,national_name=national_name,divisional_id=divisional_id,divisional_name=divisional_name,distributor_id=distributor_id,distributor_name=distributor_name)
        


def check_level_id(level_id):
    c_id=session.cid
    level_id_sql="SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and level_id='"+str(level_id)+"' ;"
    # return level_id_sql
    level_id_records=db.executesql(level_id_sql, as_dict=True)
    if len(level_id_records)>0:
        return True
    else:
        return False
    
def check_child_level(depth,parent_id):
    depth = depth + 1
    c_id=session.cid
    level_id_sql="SELECT * FROM sm_level WHERE cid='"+str(c_id)+"' and depth = '"+str(depth)+"' and parent_level_id = '"+str(parent_id)+"' GROUP BY level2,level1,level0;"
    level_id_records=db.executesql(level_id_sql, as_dict=True)
    if len(level_id_records)>0:
        return True
    else:
        return False


def get_level_id_list():
    c_id = session.cid
    retStr = ''

    levellistRows_sql = "select level_id from sm_level where cid = '"+c_id+"';"
    levellistRows = db.executesql(levellistRows_sql, as_dict=True)

    for i in range(len(levellistRows)):
        level_list_dict=levellistRows[i]   
        level_id=str(level_list_dict["level_id"])   
        if retStr == '':
            retStr = level_id
        else:
            retStr += ',' + level_id
    
    return retStr


def download_level():
    c_id=session.cid
    records=''
    myString='Area Structure\n\n'
    myString+= 'National,Divisional,Distributor\n'

    download_sql = "select * from sm_level where cid = '"+c_id+"';"
    download_records = db.executesql(download_sql, as_dict=True)

    records1_sql="select * from sm_level where cid = '"+str(c_id)+"' and parent_level_id = '0' ;"
    records1=db.executesql(records1_sql, as_dict=True)
    for i in range(len(records1)):
        row1=records1[i]
        level_id_1=row1['level_id']
        level_name_1=row1['level_name']
        
        myString+=str(level_name_1)+'-'+str(level_id_1)+'\n'
        
        for i in range(len(download_records)):
            levelData=download_records[i]
            level_id_2=levelData['level_id']
            level_name_2=levelData['level_name']
            parent_level_id_2=levelData['parent_level_id']
            if (parent_level_id_2==level_id_1):    
                myString+=','+str(level_name_2)+'-'+str(level_id_2)+'\n'

                for i in range(len(download_records)):
                    levelData=download_records[i]
                    level_id_3=levelData['level_id']
                    level_name_3=levelData['level_name']
                    parent_level_id_3=levelData['parent_level_id']
                    if (parent_level_id_3==level_id_2):    
                        myString+=',,'+str(level_name_3)+'-'+str(level_id_3)+'\n'
                                                
                                                
    #-----------                                
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_level.csv'   
    return str(myString)




    #===========
def download_level_classic():
    c_id=session.cid
    records=''
    maxDepth = 0
    myString='Area Structure\n\n'
    myString+='National Name,National ID,Divisional Name,Divisional Code,Distributor Name,Distributor Code\n'
    
    get_max_sql="select max(depth) as max_depth from sm_level where cid = '"+str(c_id)+"';"
    # return get_max_sql
    get_max=db.executesql(get_max_sql,as_dict=True)
    for m in range(len(get_max)):
        rec = get_max[m]
        maxDepth = rec['max_depth']

    download_sql = "select * from sm_level where cid = '"+str(c_id)+"';"
    download_records = db.executesql(download_sql, as_dict=True)
    
    records1_sql="select * from sm_level where cid = '"+str(c_id)+"' and parent_level_id = '0' ;"
    # return records1_sql
    records1=db.executesql(records1_sql, as_dict=True)
    for i in range(len(records1)):
        row1=records1[i]
        level_id_1=row1['level_id']
        level_name_1=row1['level_name']
        
        if maxDepth==0:
            myString+=str(level_name_1)+','+str(level_id_1)+'\n'
        else:
            pass
        
        for i in range(len(download_records)):
            levelData=download_records[i]
            level_id_2=levelData['level_id']
            level_name_2=levelData['level_name']
            parent_level_id_2=levelData['parent_level_id']
            if (parent_level_id_2==level_id_1):    
                
                if maxDepth==1:
                    myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+'\n'
                else:
                    pass
                
                for i in range(len(download_records)):
                    levelData=download_records[i]
                    level_id_3=levelData['level_id']
                    level_name_3=levelData['level_name']
                    parent_level_id_3=levelData['parent_level_id']
                    if (parent_level_id_3==level_id_2):
                        
                        if maxDepth==2: 
                            myString+=str(level_name_1)+','+str(level_id_1)+','+str(level_name_2)+','+str(level_id_2)+','+str(level_name_3)+','+str(level_id_3)+'\n'
                        else:
                            pass
                         
                                                
    #-----------                                
    import gluon.contenttype
    response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
    response.headers['Content-disposition'] = 'attachment; filename=download_working_area_classic.csv'   
    return str(myString)
   