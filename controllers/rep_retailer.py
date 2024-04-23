def rep_ret():
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))

	response.title = 'Rep-retailer'
	submit = request.vars.submit
	btn_filter_rep=request.vars.btn_filter_rep
	rep_id_filter_1 = request.vars.rep_id_filter_1
	client_id_filter_1 = request.vars.client_id_filter_1
	btn_all=request.vars.btn_all
	c_id = session.cid
	condition=''
	delete_btn=request.vars.delete_btn
	reqPage = len(request.args)
	
	if submit:
	    # return rep_id
		try:
			rep_id = str(request.vars.rep_id_filter).split('|')[0]
			rep_name= str(request.vars.rep_id_filter).split('|')[1]
		except:
			rep_id=''
			rep_name=''
		try:
			client_id = str(request.vars.client_id_filter).split('|')[0]
			client_name= str(request.vars.client_id_filter).split('|')[1]
		except:
			client_id=''
			client_name=''
		check_rep_sql = "select * from sm_rep where cid='"+str(c_id)+"'and rep_id='"+str(rep_id)+"' and user_type='rep';"
		# return check_rep_sql
		check_rep = db.executesql(check_rep_sql, as_dict=True)

		if len(check_rep)>0:

			chk_area_sql="select * from sm_client where cid='"+str(c_id)+"'and client_id='"+str(client_id)+"';"
			# return chk_area_sql
			check_area = db.executesql(chk_area_sql, as_dict=True)

			if len (check_area)==0:
				response.flash = 'Retailer is not valid!'

			else:
				check_dup_sql = "select * from rep_client where cid='"+str(c_id)+"'and client_id='"+str(client_id)+"';"
				# return check_rep_sql
				check_dup = db.executesql(check_dup_sql, as_dict=True)
				if len(check_dup)>0:
					response.flash = 'Duplicate Client Entry!'
				else:

					insertArea_sql = "INSERT INTO  rep_client (cid, rep_id ,name, client_id ,client_name) VALUES ('"+str(c_id)+"','"+str(rep_id)+"','"+str(rep_name)+"','"+str(client_id)+"','"+str(client_name)+"');"      
					#return insertCrud_sql
					insertArea = db.executesql(insertArea_sql)
					response.flash= 'Inserted Successfully'
		else:
			response.flash = 'Representative is not valid!'


	if btn_filter_rep == "Filter":
		# return 10
		if rep_id_filter_1 != '':
			# return 11
			session.rep_id_filter_1 = rep_id_filter_1
			rep_id_filter_1 = str(rep_id_filter_1).split('|')[0]
			condition = condition + " and rep_id = '" + str(rep_id_filter_1) + "'"
			# return condition

		if client_id_filter_1 != '':
			# return 11
			session.client_id_filter_1 = client_id_filter_1
			client_id_filter_1 = str(client_id_filter_1).split('|')[0]
			condition = condition + " and client_id = '" + str(client_id_filter_1) + "'"
			# return condition
		reqPage=0
		session.client_condition = condition

	if btn_all == "All":
		# return 22
		condition = ''
		session.rep_id_filter_1 = ''
		session.client_id_filter_1 = ''
		session.client_condition = condition
		reqPage=0

	#--------paging
	session.clients_per_page = 20
	if reqPage:
		page=int(request.args[0])
	else:
		page=0
	clients_per_page=session.clients_per_page
	limitby=(page*clients_per_page,(page+1)*clients_per_page+1)
    #--------end paging


	if delete_btn: 
	    rep_Id= request.args(0)
	    client_Id= request.args(1)

	    # return area_Id
	    delete_sql = "DELETE from rep_client where cid = '"+c_id+"' and rep_id='"+str(rep_Id)+"' and client_id='"+str(client_Id)+"'   limit 1 ;"
	    # return delete_sql
	    records = db.executesql(delete_sql)
	    session.flash = 'Deleted Successfully'
	    redirect (URL('rep_retailer','rep_ret'))

	condition=session.client_condition
	if condition==None or condition=='None':
		condition=''

	repRet_sql = "select * from rep_client where cid = '"+str(c_id)+"' "+condition+" ORDER BY id DESC limit %d, %d;" % limitby
	repRet = db.executesql(repRet_sql, as_dict=True)
	# session.condition = condition

	total_record_sql = f"SELECT COUNT(id) AS total FROM rep_client WHERE cid='GULF' {condition} ORDER BY id ASC;"
	# return total_record_sql
	total_record = db.executesql(total_record_sql, as_dict = True)
	total_rec = total_record[0]['total']
	# return total_rec

	return dict(repRet=repRet,total_rec=total_rec,page=page,clients_per_page=clients_per_page)

	


def get_client_id_list():
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))
	c_id = session.cid
	retStr = ''

	replistRows_sql = "select * from sm_client where cid = '"+c_id+"';"
	replistRows = db.executesql(replistRows_sql, as_dict=True)

	for i in range(len(replistRows)):
		rep_list_dict=replistRows[i]   
		client_id=str(rep_list_dict["client_id"])
		client_name=str(rep_list_dict["name"])   
		if retStr == '':
			retStr = client_id+'|'+client_name
		else:
			retStr += ',' + client_id+'|'+client_name
    
	return retStr



def get_rep_id_list():
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))
	c_id = session.cid
	retStr = ''

	replistRows_sql = "select * from sm_rep where cid = '"+c_id+"' and user_type='rep';"
	replistRows = db.executesql(replistRows_sql, as_dict=True)

	for i in range(len(replistRows)):
		rep_list_dict=replistRows[i]   
		rep_id=str(rep_list_dict["rep_id"])
		rep_name=str(rep_list_dict["name"])   
		if retStr == '':
			retStr = rep_id+'|'+rep_name
		else:
			retStr += ',' + rep_id+'|'+rep_name
    
	return retStr



def rep_ret_batch() :
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))
	response.title = 'Rep-retailer Batch Upload'
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
				client_idExcel = str(coloum_list[2]).strip().upper()               
				client_nameExcel = str(coloum_list[3]).strip().upper()               
	                
				if rep_idExcel==''or rep_idExcel == 'NONE' or nameExcel=='' or nameExcel== 'NONE' or client_idExcel=='' or client_idExcel == 'NONE' or client_nameExcel=='' or client_nameExcel == 'NONE':
					error_data=row_data+'(Required all value)\n'
					error_str=error_str+error_data
					count_error+=1
					continue                    
	            
				else:
					check_rep_sql = "select * from sm_rep where cid='"+str(cid)+"'and rep_id='"+str(rep_idExcel)+"' and user_type='rep' LIMIT 0,1; "
					# return check_rep_sql
					check_rep = db.executesql(check_rep_sql, as_dict=True)

					if len(check_rep)>0:

						chk_client_sql="select * from sm_client where cid='"+str(cid)+"'and client_id='"+str(client_idExcel)+"';"
						# return chk_area_sql
						check_client = db.executesql(chk_client_sql, as_dict=True)

						if len (check_client)==0:
							error_data=row_data+'(Client not valid!!)\n'
							error_str=error_str+error_data
							count_error+=1
						else:
							existCheckRows= " select * FROM rep_client WHERE cid='"+str(cid)+"' and client_id= '"+str(client_idExcel)+"' LIMIT 0,1"
							# return existCheckRows
							existCheck = db.executesql(existCheckRows)

							if len(existCheck) > 0:
								error_data=row_data+'(Duplicate Client!!)\n'
								error_str=error_str+error_data
								count_error+=1
								continue
							else:
								try:
									insert_sql = "INSERT INTO rep_client (cid, rep_id, name, client_id, client_name) VALUES ('"+str(cid)+"','"+str(rep_idExcel)+"','"+str(nameExcel)+"', '"+str(client_idExcel)+"','"+str(client_nameExcel)+"');"
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

def client_list_Download():
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))
	c_id = session.cid
	condition=''
	condition=session.client_condition
	if condition==None or condition=='None':
		condition=''
	repAreaRows_sql = "select * from rep_client where cid = '"+c_id+"' "+condition+" ;"
    # return crudRows_sql
	rep_area = db.executesql(repAreaRows_sql, as_dict=True)
	# return record
	myString = 'Rep-Retailer List\n\n'
	myString += 'REP ID, REP Name, Client Id, Client Name\n'
	total=0
	attTime = ''
	totalCount = 0
	for i in range(len(rep_area)):
		recordsStr = rep_area[i]
		rep_id = str(recordsStr['rep_id'])
		rep_name = str(recordsStr['name'])
		client_id = str(recordsStr['client_id'])
		client_name = str(recordsStr['client_name'])

		myString += str(rep_id) + ',' + str(rep_name) + ',' + str(client_id) + ',' + str(client_name) + ',\n'

    # Save as csv
	import gluon.contenttype
	response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
	response.headers['Content-disposition'] = 'attachment; filename=download_rep_retailer.csv'
	return str(myString)

#========
def rep_replacement():
	if (session.cid=='' or session.cid==None):
		redirect (URL('default','index'))
	response.title = 'Rep-replacement'
	c_id=session.cid
	update_btn = request.vars.update_btn
	session.rep_old_id = ''
	session.rep_old_name = ''
	session.rep_new_id = ''
	session.rep_new_name = ''


	if update_btn:
		rep_old_id = str(request.vars.rep_old_id).strip()
		rep_old_name = str(request.vars.rep_old_name).strip()
		rep_new_id = str(request.vars.rep_new_id).strip()
		rep_new_name = str(request.vars.rep_new_name).strip()

		session.rep_old_id = rep_old_id
		session.rep_old_name = rep_old_name
		session.rep_new_id = rep_new_id
		session.rep_new_name = rep_new_name

		if (rep_old_id=='' or rep_old_id=='None' or rep_old_id==None) or (rep_new_id=='' or rep_new_id=='None' or rep_new_id==None) or (rep_new_name=='' or rep_new_name=='None' or rep_new_name==None):
			response.flash = 'Required All Values'

		else:
			check_rep_sql = f"select * from sm_rep where cid='{c_id}'and rep_id='{rep_old_id}' and user_type='rep' and status='ACTIVE';"
			# return check_rep_sql
			check_rep = db.executesql(check_rep_sql, as_dict=True)
   
			check_new_rep_sql = f"select * from sm_rep where cid='{c_id}'and rep_id='{rep_new_id}' and user_type='rep' and status='ACTIVE';"
			# return check_new_rep_sql
			check_new_rep = db.executesql(check_new_rep_sql, as_dict=True)

			if len(check_rep)==0:
				response.flash = 'Representative is not valid!'

			elif len(check_new_rep) == 0:
				response.flash = 'New Representative is not valid!'	
			
			else:
				update_sql = f"UPDATE rep_client SET rep_id = '{str(rep_new_id)}', name = '{str(rep_new_name)}' WHERE rep_id = '"+str(rep_old_id)+"';"      
				#return insertCrud_sql
				up_date = db.executesql(update_sql)

				session.rep_old_id = ''
				session.rep_old_name = ''
				session.rep_new_id = ''
				session.rep_new_name = ''

				session.flash = 'Update Successfully!'
				redirect(URL('rep_retailer','rep_ret'))


	return dict()