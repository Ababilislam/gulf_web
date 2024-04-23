
# http://127.0.0.1:8000/ipi_report/track_mobile/tracking_index?cid=IBNSINA&rep_id=ITRSM&rep_pass=1234

# http://127.0.0.1:8000/ipi_report/track_mobile/tracking_index?cid=IBNSINA&rep_id=ITZM&rep_pass=1234

# http://127.0.0.1:8000/ipi_report/track_mobile/tracking_index?cid=IBNSINA&rep_id=ITFM&rep_pass=1234

# http://127.0.0.1:8000/ipi_report/track_mobile/tracking_index?cid=IBNSINA&rep_id=IT03&rep_pass=1234

##############
# (National depth - 0)
# http://127.0.0.1:8000/gulf_web/track_mobile/tracking_index?cid=GULF&rep_id=100097&rep_pass=12345

# Depth(Division - 1)
# http://127.0.0.1:8000/gulf_web/track_mobile/tracking_index?cid=GULF&rep_id=100102&rep_pass=12345

# Depth(Distributor - 2)
# http://127.0.0.1:8000/gulf_web/track_mobile/tracking_index?cid=GULF&rep_id=100055&rep_pass=12345

# rep
# http://127.0.0.1:8000/gulf_web/track_mobile/tracking_index?cid=GULF&rep_id=100117&rep_pass=12345

# http://127.0.0.1:8000/gulf_web/track_mobile/tracking_index?cid=GULF&rep_id=100097&rep_pass=12345

def tracking_index():

    c_id=request.vars.cid
    rep_id=request.vars.rep_id
    rep_pass=request.vars.rep_pass
    # session.level_depth = 1
    dictData={}
    level_user_list=[]
    level_depth_no=''
    session.rep_id=str(rep_id).upper()
    if rep_id=='WEB':
        repRecords=db((db.sm_rep.cid==c_id)).select(db.sm_rep.id,db.sm_rep.rep_id,db.sm_rep.name,db.sm_rep.user_type,orderby=db.sm_rep.name,)
        for repRecords in repRecords:
            rep_id=str(repRecords.rep_id)
            name=str(repRecords.name) 
            user_type=str(repRecords.user_type) 
            
            dictData={'u_id':rep_id,'u_name':name,'user_type':user_type}
            level_user_list.append(dictData)


        session.level_user_list=level_user_list  
        
        redirect(URL(c='track_mobile',f='track_home_web')) 
    else:
        #---------------------- rep check
        userRecords=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==rep_id)& (db.sm_rep.password==rep_pass)& (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
        # return db._lastsql
        if not userRecords:
            response.flash = 'Invalid/Inactive User'
        else:
            name=userRecords[0].name
            user_type=userRecords[0].user_type
            
            session.cid=c_id
            session.user_id=rep_id
            session.rep_id=rep_id
            session.user_type=user_type
            session.rep_pass=rep_pass
            session.items_per_page=15 
            
            level_user_list=[]
            
            if user_type=='sup':                
                supLevelRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.level_depth_no,db.sm_supervisor_level.level_id)
                # return db._lastsql
                if not supLevelRows:
                    response.flash = 'Supervisor Level Not Available'
                else:
                    sup_level_id_list=[]
                    for sRow in supLevelRows:                    
                        level_depth_no=sRow.level_depth_no
                        level_id=sRow.level_id 
                        sup_level_id_list.append(level_id)  
                        session.depth_no=level_depth_no
                    # return level_depth_no
                    
                    if level_depth_no==0:
                        # session.level_heading='Divission'
                        session.level_heading='National'
                        
                        level1Rows=db((db.sm_level.cid==c_id) & (db.sm_level.level_id.belongs(sup_level_id_list))).select(db.sm_level.level_id,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
                        # return db._lastsql
                        level1_list=[]
                        for dRow in level1Rows:
                            level_id=dRow.level_id
                            level1_list.append(level_id)

                        supRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.level_id== level_id) & (db.sm_supervisor_level.level_depth_no=='0') & (db.sm_supervisor_level.sup_id==rep_id) ).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_name,db.sm_supervisor_level.level_depth_no,orderby=db.sm_supervisor_level.level_depth_no|db.sm_supervisor_level.sup_name)
                        # return db._lastsql
                        for row in supRows:
                            sup_id=str(row.sup_id)
                            sup_name=str(row.sup_name)
                            area_id=str(row.level_id) 
                            area_name=str(row.level_name) 
                            level_depth_no=str(row.level_depth_no)
                            if level_depth_no=='1': 
                                # session.level_heading='Zone' 
                                session.level_heading='Divisional' 
                            dictData={'u_id':sup_id,'u_name':sup_name,'area_id':area_id,'area_name':area_name,'user_type':level_depth_no}
                            level_user_list.append(dictData)
                            
                           

                                                   
                    elif level_depth_no==1:
                        # session.level_depth = level_depth_no
                        # session.level_heading='Zone'
                        session.level_heading='Divisional'
                        level2Rows=db((db.sm_level.cid==c_id) & (db.sm_level.level_id.belongs(sup_level_id_list)) & (db.sm_level.depth>0)).select(db.sm_level.level_id,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
                        # return db._lastsql
                        level2_list=[]
                        for dRow in level2Rows:
                            level_id=dRow.level_id
                            level2_list.append(level_id)
                        
                        
                        supRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.level_id== level_id) & (db.sm_supervisor_level.level_depth_no=='1') & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_name,db.sm_supervisor_level.level_depth_no,orderby=db.sm_supervisor_level.level_depth_no|db.sm_supervisor_level.sup_name)
                        # return db._lastsql
                        for row in supRows:
                            sup_id=str(row.sup_id)
                            sup_name=str(row.sup_name)
                            area_id=str(row.level_id) 
                            area_name=str(row.level_name)
                            level_depth_no=str(row.level_depth_no)
                            # return area_name

                            if level_depth_no=='2': 
                                # session.level_heading='Area' 
                                session.level_heading='Distributor' 
                            dictData={'u_id':sup_id,'u_name':sup_name,'area_id':area_id,'area_name':area_name,'user_type':level_depth_no}
                            level_user_list.append(dictData)

                    
                    elif level_depth_no==2:
                        # session.level_depth = level_depth_no
                        session.level_heading='Distributor'                                                                                            
                        level3Rows=db((db.sm_level.cid==c_id) & (db.sm_level.level_id.belongs(sup_level_id_list)) & (db.sm_level.depth>1) ).select(db.sm_level.level_id,orderby=db.sm_level.level_id,groupby=db.sm_level.level_id)
                        # return db._lastsql
                        level3_list=[]
                        for dRow in level3Rows:
                            level_id=dRow.level_id
                            level3_list.append(level_id)
                        
                        supRows=db((db.sm_supervisor_level.cid==c_id) & (db.sm_supervisor_level.level_id== level_id) & (db.sm_supervisor_level.level_depth_no=='2') & (db.sm_supervisor_level.sup_id==rep_id)).select(db.sm_supervisor_level.sup_id,db.sm_supervisor_level.sup_name,db.sm_supervisor_level.level_id,db.sm_supervisor_level.level_name,db.sm_supervisor_level.level_depth_no,orderby=db.sm_supervisor_level.level_depth_no|db.sm_supervisor_level.sup_name)
                        # return db._lastsql
                        for row in supRows:
                            sup_id=str(row.sup_id)
                            sup_name=str(row.sup_name)
                            area_id=str(row.level_id) 
                            area_name=str(row.level_name)    
                            level_depth_no=str(row.level_depth_no)
                            # return area_name
                            if level_depth_no=='2': 
                                # session.level_heading='Area'
                                session.level_heading='Distributor'
                                # return 'sdf'
                            dictData={'u_id':sup_id,'u_name':sup_name,'area_id':area_id,'area_name':area_name,'user_type':level_depth_no}
                            level_user_list.append(dictData)
                          
                    session.level_user_list=level_user_list                      

                    redirect(URL(c='track_mobile',f='track_home'))
            

            if user_type=='rep':
                session.level_heading='Market'  
                area_list=[]
                areaRows=db((db.sm_rep_area.cid==c_id) & (db.sm_rep_area.rep_id==session.user_id)).select(db.sm_rep_area.area_id,orderby=db.sm_rep_area.area_id,groupby=db.sm_rep_area.area_id)
                
                for areaRows in areaRows:
                    area_id=areaRows.area_id
                    area_list.append(area_id)


                repRows=db((db.sm_rep_area.cid==c_id) & (db.sm_rep_area.area_id.belongs(area_list)) & (db.sm_rep_area.rep_id==rep_id)).select(db.sm_rep_area.rep_id,db.sm_rep_area.rep_name,db.sm_rep_area.area_id,db.sm_rep_area.area_name)
                # return repRows
                for row1 in repRows:
                    rep_id=str(row1.rep_id)
                    rep_name=str(row1.rep_name) 
                    area_id=str(row1.area_id) 
                    area_name=str(row1.area_name) 
                    dictData={'u_id':rep_id,'u_name':rep_name,'area_id':area_id,'area_name':area_name,'user_type':'3'}
                    level_user_list.append(dictData)
                session.level_user_list=level_user_list  
                redirect(URL(c='track_mobile',f='track_home'))          
    return dict()



def track_home():
    if session.cid=='' or session.cid==None:
        redirect(URL(c='track_mobile',f='tracking_index'))
    level_user_list=session.level_user_list                  
    # return level_user_list
    return dict(level_user_list=level_user_list)

def track_home_web():
    if session.cid=='' or session.cid==None:
        redirect(URL(c='track_mobile',f='tracking_index'))
    level_user_list=session.level_user_list                  
    return dict(level_user_list=level_user_list)


def activity():
    if session.cid=='' or session.cid==None:
        redirect(URL(c='track_mobile',f='tracking_index'))        
    u_id=request.vars.u_id    
    
    qset=db()
    qset=qset(db.sm_tracking_live2.cid==session.cid)
    qset=qset(db.sm_tracking_live2.rep_id==u_id)
    # records=qset.select(db.sm_tracking_live2.visit_time,db.sm_tracking_live2.call_type,db.sm_tracking_live2.visited_id,db.sm_tracking_live2.visited_name,db.sm_tracking_live2.visited_latlong,orderby=~db.sm_tracking_live2.visit_time,limitby=(0,50))
    records=qset.select(db.sm_tracking_live2.visit_time,db.sm_tracking_live2.call_type,db.sm_tracking_live2.visited_latlong,orderby=~db.sm_tracking_live2.visit_time,limitby=(0,50))
    
    # records1=qset(db.sm_tracking_live2.visit_date==current_date).select(db.sm_tracking_live2.visit_time,db.sm_tracking_live2.call_type,db.sm_tracking_live2.visited_id,db.sm_tracking_live2.visited_name,db.sm_tracking_live2.visited_latlong,db.sm_tracking_live2.rep_id,db.sm_tracking_live2.rep_name,orderby=~db.sm_tracking_live2.visit_time)
    records1=qset(db.sm_tracking_live2.visit_date==current_date).select(db.sm_tracking_live2.visit_time,db.sm_tracking_live2.call_type,db.sm_tracking_live2.visited_latlong,db.sm_tracking_live2.rep_id,db.sm_tracking_live2.rep_name,orderby=~db.sm_tracking_live2.visit_time)
    
    dcrCount=0
    ordCount=0
    chkCount=0
    rep_id=''
    rep_name=''
    for row in records1:
        call_type=row.call_type
        if call_type=='SELL':
            ordCount+=1
        elif call_type=='DCR':
            dcrCount+=1
        elif call_type=='CHECKIN':
            chkCount+=1
        rep_id =row.rep_id
        rep_name =row.rep_name
    return dict(records=records,ordCount=ordCount,dcrCount=dcrCount,chkCount=chkCount,rep_id=rep_id,rep_name=rep_name)

def activity_web():
    if session.cid=='' or session.cid==None:
        redirect(URL(c='track_mobile',f='tracking_index'))
        
    u_id=request.vars.u_id    
    
    qset=db()
    qset=qset(db.sm_tracking_live2.cid==session.cid)
    qset=qset(db.sm_tracking_live2.rep_id==u_id)
    records=qset.select(db.sm_tracking_live2.visit_time,db.sm_tracking_live2.call_type,db.sm_tracking_live2.visited_id,db.sm_tracking_live2.visited_name,db.sm_tracking_live2.visited_latlong,orderby=~db.sm_tracking_live2.visit_time,limitby=(0,50))
    
    records1=qset(db.sm_tracking_live2.visit_date==current_date).select(db.sm_tracking_live2.visit_time,db.sm_tracking_live2.call_type,db.sm_tracking_live2.visited_id,db.sm_tracking_live2.visited_name,db.sm_tracking_live2.visited_latlong,orderby=~db.sm_tracking_live2.visit_time)
    
    dcrCount=0
    ordCount=0
    chkCount=0
    for row in records1:
        call_type=row.call_type
        if call_type=='SELL':
            ordCount+=1
        elif call_type=='DCR':
            dcrCount+=1
        elif call_type=='CHECKIN':
            chkCount+=1
    return dict(records=records,ordCount=ordCount,dcrCount=dcrCount,chkCount=chkCount)



def tracking_drilldown_home():
    if session.cid=='' or session.cid==None:
        redirect(URL(c='track_mobile',f='tracking_index'))
    level_user_list=session.level_user_list   
    # return level_user_list                  
    return dict(level_user_list=level_user_list)

def tracking_drilldown():
    c_id=session.cid
    rep_id=request.vars.u_id
    # return rep_id
        #---------------------- rep check
    userRecords=db((db.sm_rep.cid==c_id) & (db.sm_rep.rep_id==rep_id) & (db.sm_rep.status=='ACTIVE')).select(db.sm_rep.id,db.sm_rep.name,db.sm_rep.user_type,limitby=(0,1))
    if not userRecords:
        session.flash = 'Invalid/Inactive User'
        redirect(URL(c='track_mobile',f='tracking_drilldown_home'))
    else:
        name=userRecords[0].name
        user_type=userRecords[0].user_type 
        session.user_id_drill=rep_id
        session.rep_name_drill=name
        session.user_type_drill=user_type
        session.items_per_page=15
        
        if user_type == 'sup':
            level_depth_no = 0
            dictData = {}
            level_user_list = []
            supLevelRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.sup_id == rep_id)).select(db.sm_supervisor_level.level_depth_no, db.sm_supervisor_level.level_id)
            if not supLevelRows:
                session.flash = 'Supervisor Level Not Available'
                redirect(URL(c='track_mobile',f='tracking_drilldown_home'))
            else:
                sup_level_id_list = []
                for sRow in supLevelRows:
                    level_depth_no = sRow.level_depth_no
                    level_id = sRow.level_id
                    sup_level_id_list.append(level_id)

                if level_depth_no == 0:
                    level1Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level0.belongs(sup_level_id_list))).select(db.sm_level.level_id, orderby=db.sm_level.level_id, groupby=db.sm_level.level_id)
                    level1_list = []
                    for dRow in level1Rows:
                        level_id = dRow.level_id
                        level1_list.append(level_id)

                    supRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.level_id.belongs(level1_list) & (db.sm_supervisor_level.level_depth_no == '1'))).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, db.sm_supervisor_level.level_id, db.sm_supervisor_level.level_name, db.sm_supervisor_level.level_depth_no, orderby=db.sm_supervisor_level.level_depth_no | db.sm_supervisor_level.sup_name)
                    for row in supRows:
                        sup_id = str(row.sup_id)
                        sup_name = str(row.sup_name)
                        area_id = str(row.level_id)
                        area_name = str(row.level_name)
                        level_depth_no = str(row.level_depth_no)
                        if level_depth_no == '1':
                            session.level_heading = 'Divisional'
                        dictData = {'u_id': sup_id, 'u_name': sup_name, 'area_id': area_id, 'area_name': area_name, 'user_type': level_depth_no}
                        level_user_list.append(dictData)

                elif level_depth_no == 1:
                    level2Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level1.belongs(sup_level_id_list)) & (db.sm_level.depth > 0)).select(db.sm_level.level_id, orderby=db.sm_level.level_id, groupby=db.sm_level.level_id)
                    # return db._lastsql
                    
                    level2_list = []
                    for dRow in level2Rows:
                        level_id = dRow.level_id
                        level2_list.append(level_id)

                    # supRows = db((db.sm_supervisor_level.cid == c_id) & (db.sm_supervisor_level.level_id.belongs(level2_list)) & (db.sm_supervisor_level.level_depth_no == '1')).select(db.sm_supervisor_level.sup_id, db.sm_supervisor_level.sup_name, db.sm_supervisor_level.level_id, db.sm_supervisor_level.level_name, db.sm_supervisor_level.level_depth_no, orderby=db.sm_supervisor_level.level_depth_no | db.sm_supervisor_level.sup_name)
                    supRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.area_id.belongs(level2_list))).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name, db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.rep_id | db.sm_rep_area.rep_name)

                    level_depth_no = 2
                    for row in supRows:
                        sup_id = str(row.rep_id)
                        sup_name = str(row.rep_name)
                        area_id = str(row.area_id)
                        area_name = str(row.area_name)
                        # level_depth_no = str(row.level_depth_no)
                        if level_depth_no == 2:
                            session.level_heading = 'Distributor'

                        dictData = {'u_id': sup_id, 'u_name': sup_name, 'area_id': area_id, 'area_name': area_name, 'user_type': level_depth_no}
                        level_user_list.append(dictData)

                elif level_depth_no == 2:
                    level3Rows = db((db.sm_level.cid == c_id) & (db.sm_level.level2.belongs(sup_level_id_list)) & (db.sm_level.depth > 1)).select(db.sm_level.level_id, orderby=db.sm_level.level_id, groupby=db.sm_level.level_id)
                    level3_list = []
                    for dRow in level3Rows:
                        level_id = dRow.level_id
                        level3_list.append(level_id)

                    repRows = db((db.sm_rep_area.cid == c_id) & (db.sm_rep_area.area_id.belongs(level3_list))).select(db.sm_rep_area.rep_id, db.sm_rep_area.rep_name, db.sm_rep_area.area_id, db.sm_rep_area.area_name, orderby=db.sm_rep_area.rep_name)
                    for row1 in repRows:
                        rep_id = str(row1.rep_id)
                        rep_name = str(row1.rep_name)
                        area_id = str(row1.area_id)
                        area_name = str(row1.area_name)
                        dictData = {'u_id': rep_id, 'u_name': rep_name, 'area_id': area_id, 'area_name': area_name, 'user_type': '3'}
                        level_user_list.append(dictData)
                    session.level_heading = 'Market'

            # return level_user_list

            session.level_user_list=level_user_list                      
            redirect(URL(c='track_mobile',f='tracking_drilldown_home'))   
    return dict() 