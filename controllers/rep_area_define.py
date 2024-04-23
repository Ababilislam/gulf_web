def rep_area() :
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))
	response.title = 'Rep-Dis area'
	submit = request.vars.submit
	btn_filter_rep=request.vars.btn_filter_rep
	rep_id_filter_1 = request.vars.rep_id_filter_1
	btn_all=request.vars.btn_all
	c_id = session.cid
	condition=''
	delete_btn=request.vars.delete_btn
	
	if submit:
	    # return rep_id
		try:
			rep_id = str(request.vars.rep_id_filter).split('|')[0]
			rep_name= str(request.vars.rep_id_filter).split('|')[1]
		except:
			rep_id=''
			rep_name=''
		try:
			area_id = str(request.vars.area_id_filter).split('|')[0]
			area_name= str(request.vars.area_id_filter).split('|')[1]
		except:
			area_id=''
			area_name=''
		check_rep_sql = "select * from sm_rep where cid='"+str(c_id)+"'and rep_id='"+str(rep_id)+"' and user_type='rep';"
		# return check_rep_sql
		check_rep = db.executesql(check_rep_sql, as_dict=True)

		if len(check_rep)>0:

			chk_area_sql="select * from sm_level where cid='"+str(c_id)+"'and level_id='"+str(area_id)+"' and is_leaf='1' and depth ='2';"
			# return chk_area_sql
			check_area = db.executesql(chk_area_sql, as_dict=True)

			if len (check_area)==0:
				response.flash = 'area is not valid!'

			else:
				check_dup_sql = "select * from sm_rep_area where cid='"+str(c_id)+"'and rep_id='"+str(rep_id)+"' and area_id='"+str(area_id)+"';"
				# return check_rep_sql
				check_dup = db.executesql(check_dup_sql, as_dict=True)
				if len(check_dup)>0:
					response.flash = 'Duplicate Area Entry!'
				else:

					insertArea_sql = "INSERT INTO  sm_rep_area (cid, rep_id , rep_name, area_id ,area_name) VALUES ('"+str(c_id)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(area_id)+"','"+str(area_name)+"');"      
					#return insertCrud_sql
					insertArea = db.executesql(insertArea_sql)
					response.flash= 'Inserted Successfully'
		else:
			response.flash = 'Representative is not valid!'


	if btn_filter_rep == "Filter":
	    # return 10
	    if rep_id_filter_1 !='':
	        # return 11
	        session.rep_id_filter_1 = rep_id_filter_1
	        rep_id_filter_1 = str(rep_id_filter_1).split('|')[0]
	        condition = condition + " and rep_id = '"+str(rep_id_filter_1)+"'"
	        # return condition
	if btn_all == "All":
	    # return 22
	    condition = ''
	    session.rep_id_filter_1 = ''

	if delete_btn: 
	    rep_Id= request.args(0)
	    area_Id= request.args(1)

	    # return area_Id
	    delete_sql = "DELETE from sm_rep_area where cid = '"+c_id+"' and rep_id='"+str(rep_Id)+"' and area_id='"+str(area_Id)+"'   limit 1 ;"
	    # return delete_sql
	    records = db.executesql(delete_sql)
	    session.flash = 'Deleted Successfully'
	    redirect (URL('rep_area_define','rep_area'))


	repArea_sql = "select * from sm_rep_area where cid = '"+str(c_id)+"' "+condition+" ;"
	repArea = db.executesql(repArea_sql, as_dict=True)
	session.condition = condition

	return dict(repArea=repArea)

def rep_area_batch() :
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))
	response.title = 'Rep-Dis Batch Upload'
	cid=session.cid
	btn_upload=request.vars.btn_upload
	count_inserted=0
	count_error=0
	error_str=''
	total_row=0
	        
	if btn_upload=='Upload':
		excel_data=str(request.vars.excel_data)
		inserted_count=0
		error_count=0

		row_list=excel_data.split( '\n')
		total_row=len(row_list)

		ff_list_exist=[]   
		ff_list_excel=[]

		ins_list=[]
		ins_dict={}

	    # ----------------------
		for i in range(total_row):
			if i>=100:
				break
			else:
				row_data=row_list[i]                    
				coloum_list=row_data.split( '\t')
				if len(coloum_list)==4:
					ffExcel=str(coloum_list[0]).strip().upper()

					if ffExcel!='':
						if ffExcel not in ff_list_excel:

							ff_list_excel.append(ffExcel)       

		for i in range(total_row):
			if i>=100:
				break
			else:
				row_data=row_list[i]
				coloum_list=row_data.split( '\t')            
	        
			if len(coloum_list)!=4:
				error_data=row_data+'(4 columns need in a row)\n'
				error_str=error_str+error_data
				count_error+=1
				continue
			else:
				rep_idExcel = str(coloum_list[0]).strip().upper()
				# return employee_idExcel
				nameExcel = str(coloum_list[1]).strip().upper()
				area_idExcel = str(coloum_list[2]).strip().upper()               
				area_nameExcel = str(coloum_list[3]).strip().upper()               
	                
				if rep_idExcel==''or rep_idExcel == 'NONE' or nameExcel=='' or nameExcel== 'NONE' or area_idExcel=='' or area_idExcel == 'NONE' or area_nameExcel=='' or area_nameExcel == 'NONE':
					error_data=row_data+'(Required all value)\n'
					error_str=error_str+error_data
					count_error+=1
					continue                    
	            
				else:
					check_rep_sql = "select * from sm_rep where cid='"+str(cid)+"'and rep_id='"+str(rep_idExcel)+"' and user_type='rep' LIMIT 0,1; "
					# return check_rep_sql
					check_rep = db.executesql(check_rep_sql, as_dict=True)

					if len(check_rep)>0:

						chk_area_sql="select * from sm_level where cid='"+str(cid)+"'and level_id='"+str(area_idExcel)+"' and is_leaf='1' and depth ='2';"
						# return chk_area_sql
						check_area = db.executesql(chk_area_sql, as_dict=True)

						if len (check_area)==0:
							error_data=row_data+'(Area not valid!!)\n'
							error_str=error_str+error_data
							count_error+=1
						else:
							existCheckRows= " select * FROM sm_rep_area WHERE cid='"+str(cid)+"' and rep_id = '"+str(rep_idExcel)+"' and area_id= '"+str(area_idExcel)+"' LIMIT 0,1"
							# return existCheckRows
							existCheck = db.executesql(existCheckRows)

							if len(existCheck) > 0:
								error_data=row_data+'(Duplicate User!!)\n'
								error_str=error_str+error_data
								count_error+=1
								continue
							else:
								try:
									insert_sql = "INSERT INTO sm_rep_area (cid, rep_id, rep_name, area_id, area_name) VALUES ('"+str(cid)+"','"+str(rep_idExcel)+"','"+str(nameExcel)+"', '"+str(area_idExcel)+"','"+str(area_nameExcel)+"');"
									# return insert_sql
									update_ff_list = db.executesql(insert_sql)
									count_inserted+=1
								except Exception as e:
									error_str = 'Please do not insert special charachter.'
					else:
						error_data=row_data+'(representative not valid!!)\n'
						error_str=error_str+error_data
						count_error+=1
	                            
		if error_str=='':
			error_str='No error'

	return dict(count_inserted=count_inserted,count_error=count_error,error_str=error_str,total_row=total_row)





def get_area_id_list():
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))
	c_id = session.cid
	retStr = ''
	replistRows_sql = "select * from sm_level where cid = '"+c_id+"' and is_leaf='1';"
	replistRows = db.executesql(replistRows_sql, as_dict=True)
	
	for i in range(len(replistRows)):
		rep_list_dict=replistRows[i]   
		level_id=str(rep_list_dict["level_id"])
		name=str(rep_list_dict["level_name"])   
		if retStr == '':
			retStr = level_id+'|'+name
		else:
			retStr += ',' + level_id+'|'+name
	return retStr

def area_list_Download():
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))
	c_id = session.cid
	condition=session.condition
	repAreaRows_sql = "select * from sm_rep_area where cid = '"+c_id+"' "+condition+" ;"
    # return crudRows_sql
	rep_area = db.executesql(repAreaRows_sql, as_dict=True)
    # return record
	myString = 'Rep-Distributor List\n\n'
	myString += 'REP ID, REP Name, Area Id, Area Name\n'
	total=0
	attTime = ''
	totalCount = 0
	for i in range(len(rep_area)):
		recordsStr = rep_area[i]
		rep_id = str(recordsStr['rep_id'])
		rep_name = str(recordsStr['rep_name'])
		area_id = str(recordsStr['area_id'])
		area_name = str(recordsStr['area_name'])
		myString += str(rep_id) + ',' + str(rep_name) + ',' + str(area_id) + ',' + str(area_name) + ',\n'

    # Save as csv
	import gluon.contenttype
	response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
	response.headers['Content-disposition'] = 'attachment; filename=download_rep_area.csv'
	return str(myString)

