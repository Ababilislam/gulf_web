# -*- coding: utf-8 -*-
#########################################################################
#if request.env.web2py_runtime_gae:            # if running on Google App Engine
#    db = DAL('gae')                           # connect to Google BigTable
#    session.connect(request, response, db = db) # and store sessions and tickets there
#else:                                         # else use a normal relational database
#    db = DAL('sqlite://mrep_2.db')       # if not, use SQLite or other DB
    

#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc
plugins = PluginManager()

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:dmath160708-08e3-4217-bd7e-e9a550109a8d'   # before define_tables()
#auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL('default','user',args=['reset_password'])+'/%(key)s to reset your password'

#########################################################################

crud.settings.auth = None                      # =auth to enforce authorization on crud

#########################################################################
# Common Variable
mreporting_http_pass='abC321'
# ' " / \ < > ( ) [ ] { } , 

#======================date========================
import datetime
import os

datetime_fixed=str(date_fixed)[0:19]    # default datetime 2012-07-01 11:48:10
current_date=str(date_fixed)[0:10]   # default date 2012-07-01
first_currentDate = datetime.datetime.strptime(str(current_date)[0:7] + '-01', '%Y-%m-%d')

#---------------------------signature
signature=db.Table(db,'signature',
                Field('field1','string',default=''), 
                Field('field2','integer',default=0),
                Field('note','string',default=''),  
                Field('created_on','datetime',default=date_fixed),
                Field('created_by',default=session.user_id),
                Field('updated_on','datetime',update=date_fixed),
                Field('updated_by',update=session.user_id),
                )



#----------------------------------user--------------
db.define_table('sm_user',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('user_id','string',requires=[IS_NOT_EMPTY(),IS_ALPHANUMERIC(error_message=T('must be alphanumeric!')),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('user_name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')]),
                Field('password','string',requires=IS_LENGTH(minsize=8,maxsize=32),default='12345678'),
                Field('mobile','bigint',requires=IS_LENGTH(13,error_message='enter maximum 13 character'),default=0),
                Field('email','string'),
                Field('email_notification','string',requires=IS_IN_SET(('YES','NO')),default='YES'),
                Field('user_type','string',requires=IS_IN_SET(('Admin','Viewer'),error_message=T('select a value'))),
                Field('user_role','string',default=''),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                Field('sync_code','integer',default=0),
                Field('updated_on','datetime',update=date_fixed),
                Field('updated_by',update=session.user_id),

                migrate=False
                )
db.define_table('login_out_log',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('user_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('user_name','string',default=''),
                Field('user_role','string',default=''),
                Field('email', 'string',default=''),
                Field('mobile','bigint',default=0),
                Field('log_in','datetime'),
                Field('log_out','datetime'),
                migrate=False
                )
db.define_table('sm_settings',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('s_key','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='enter maximum 20 character')]),
                Field('s_value','string',default=''),
                Field('activity_id_list','text',default=''),
                Field('status','string',default=''),
                migrate=False
                )

db.define_table('sm_apptask',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('taskid','string',requires=IS_NOT_EMPTY()),
                Field('taskname','string',requires=IS_NOT_EMPTY()),
                signature,
                migrate=False
                )

#---------------------------
db.define_table('sm_roletask',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('roleid','string',requires=IS_NOT_EMPTY()),
                Field('taskid','string',requires=IS_NOT_EMPTY()),
                signature,
                migrate=False
                )

#---------------------------
db.define_table('sm_userrole',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('roleid','string',requires=IS_NOT_EMPTY()),
                Field('roleName','string',requires=IS_NOT_EMPTY()),
                Field('role_type','string',requires=IS_IN_SET(('Admin','General'),error_message=T('select a value'))),
                signature,
                migrate=False
                )

db.define_table('sm_rep',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('rep_id','string',requires=IS_NOT_EMPTY()),
                Field('name','string',requires=IS_NOT_EMPTY()),
                Field('mobile_no','bigint',default=0),
                migrate=False
                )

db.define_table('sm_item',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('item_id','string',requires=IS_NOT_EMPTY()),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')]),
                Field('pack_size','string',requires=IS_NOT_EMPTY()),
                Field('des','string',default=''),
                Field('category_id','string',default=''),
                Field('category_id_sp','string',default=''),
                Field('unit_type', 'string', default=''),
                Field('manufacturer', 'string', default=''),
                Field('item_carton', 'integer', default=0),
                Field('price', 'float', default=0),
                Field('dist_price', 'float', default=0),
                Field('vat_amt', 'float', default=0),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                migrate=False
                )

db.define_table('sm_retailer',
                Field('cid','string',requires=IS_NOT_EMPTY()),
                Field('customer_id','string',requires=IS_NOT_EMPTY()),
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(100,error_message='enter maximum 100 character')]),
                Field('distributor','string',requires=IS_NOT_EMPTY()),
                Field('area_id','string',default=''),
                Field('balance','string',default=''),
                Field('credit_limit','string',default=''),
                Field('credit_duration', 'string', default=''),
                Field('payment_mode', 'string', default=''),
                Field('bank_account_no', 'string', default=0),
                Field('address', 'string', default=0),
                Field('depot_id', 'string', default=0),
                Field('store_id', 'string', default=0),
                Field('category_id', 'string', default=0),
                Field('sub_category_id', 'string', default=0),
                Field('market_id', 'string', default=0),
                Field('owner_name', 'string', default=0),
                Field('contact_no1', 'string', default=0),
                Field('nid', 'integer', default=0),
                Field('thana', 'string', default=0),
                Field('district', 'string', default=0),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
                migrate=False
                )


            
######################  view  ##############################
# db.define_table('sm_search_date',
#                 Field('from_dt','date',default=first_currentDate),
#                 Field('to_dt','date',default=date_fixed),
#                 Field('from_date','datetime'),
#                 Field('to_date','datetime'),
                
#                 # Field('from_dt_2','date',default=first_currentDate),
#                 # Field('to_dt_2','date',default=date_fixed),
#                 # Field('from_dt_3','date',default=first_currentDate),
#                 # Field('to_dt_3','date',default=date_fixed),
#                 # Field('from_dt_4','date',default=first_currentDate),
#                 # Field('to_dt_4','date',default=date_fixed),
#                 # Field('from_dt_5','date',default=first_currentDate),
#                 # Field('to_dt_5','date',default=date_fixed),
                
#                 migrate=False
#                 )


db.define_table('sm_client',
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('client_id','string',default=''),
                Field('client_old_id','string',default=''),#ACCPAC ID
                
                Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='enter maximum 50 character')]),
                Field('area_id','string',requires=IS_NOT_EMPTY()),
                Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE'),zero=None),default='ACTIVE'),
                Field('op_balance','double',requires=IS_NOT_EMPTY(),default=0.0),#change type from integer
                Field('balance','double',requires=IS_NOT_EMPTY(),default=0.0),  #change type from integer
                Field('credit_limit','double',requires=IS_NOT_EMPTY(),default=0.0),#change type from integer
                
                Field('credit_duration','integer',default=0),
                Field('payment_mode','string',requires=IS_IN_SET(('CASH','CHEQUE'),zero=None),default='CASH'),
                Field('bank_account_no','string',default=''),
                # Field('no_of_doctor','integer',default=0),
                # Field('avg_patient','integer',default=0),
                # Field('has_drug_store','string',requires=IS_IN_SET(('NO','YES'),zero=None),default='NO'),
                                
                Field('address','string',default=''),
                Field('latitude','string',default='0'),
                Field('longitude','string',default='0'),
                Field('depot_id','string',requires=IS_NOT_EMPTY()),
                Field('depot_name','string',default=''),
                Field('store_id','string',requires=IS_NOT_EMPTY()),
                Field('store_name','string',default=''),
                
                Field('depot_belt_name','string',default='Default'),#depot/brance belt
                Field('category_id','string',default=''),
                Field('category_name','string',default=''),
                Field('sub_category_id','string',default=''),
                Field('sub_category_name','string',default=''),
                Field('market_id','string',requires=IS_NOT_EMPTY(),default='DEFAULT'),
                Field('market_name','string','string',default='Default'),
                
                Field('owner_name','string',default=''),
                Field('nid','integer',default=''),
                Field('passport','string',default=''),
                Field('trade_license','string',default=''),#Yes/No
                Field('trade_license_no','string',default=''),
                Field('vat_registration','string',default=''),#Yes/No
                Field('vat_registration_no','string',default=''),
                # Field('drug_registration_num','string','string',default=''),
                # Field('doctor','string',requires=IS_IN_SET(('NO','YES'),zero=None),default='NO'),
                Field('contact_no1','integer',default=''),
                Field('contact_no2','integer',default=''),
                Field('dob','date'),
                Field('dom','date'),
                Field('kids_info','string',default=''),
                Field('hobby','string',default=''),
                
                Field('manager_name','string',default=''),
                Field('manager_contact_no','integer',default=''),
                
                Field('starting_year','integer',default=''),                
                Field('monthly_sales_capacity','integer',default=0),
                Field('monthly_sales','integer',default=0),
                Field('shop_owner_status','string',default=''),#Rented/Own
                
                Field('warehouse_capacity','integer',default=0),#number of bag Qty
                Field('shop_size','integer',default=0), #sft
                Field('shop_front_size','integer',default=0),                
                Field('photo','string',default=''),#'upload',autodelete=True,uploadfolder=os.path.join(request.folder,'static/client_pic')),
                Field('photo_str','string',default=''),
                
                Field('thana_id','integer'),#not used                
                Field('thana','string',requires=IS_NOT_EMPTY()),
                Field('district_id','string',requires=IS_NOT_EMPTY()),
                Field('district','string',default=''),
                
                signature,
                migrate=False      
                )

#=========================rep============
# db.define_table('sm_rep',
#                 Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
#                 Field('rep_id','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(20,error_message='Mmaximum 20 character')]),
#                 Field('name','string',requires=[IS_NOT_EMPTY(),IS_LENGTH(50,error_message='Maximum 50 character')]),
#                 Field('mobile_no','bigint',default=''),
#                 Field('password','password',requires=IS_LENGTH(minsize=3,maxsize=12)),
#                 Field('status','string',requires=IS_IN_SET(('ACTIVE','INACTIVE')),default='ACTIVE'),
#                 Field('sync_code','string',default=''),
#                 Field('sync_code_servey','string',default=''),
#                 Field('sync_count','integer',requires=IS_NOT_EMPTY(),default=0),
#                 Field('first_sync_date','datetime',default=''),
#                 Field('last_sync_date','datetime',default=''),
#                 Field('monthly_sms_count','integer',requires=IS_NOT_EMPTY(),default=0),
#                 Field('monthly_voucher_count','integer',requires=IS_NOT_EMPTY(),default=0),
                
#                 Field('java','string',requires=IS_IN_SET(('Yes','No')),default='No'),
#                 Field('wap','string',requires=IS_IN_SET(('Yes','No')),default='No'),
#                 Field('android','string',requires=IS_IN_SET(('Yes','No')),default='No'),
#                 Field('sms','string',requires=IS_IN_SET(('Yes','No')),default='Yes'),
                
#                 Field('user_type','string',default='rep'),
#                 Field('level_id','string',default=''),
#                 Field('depot_id','string',default=''),
                  
#                 # user click on "Sync" will get response lik "You sync request is in que Please try to sync after few minutes" o - > 1
#                 # if already submitted (flag = 1) - "Your request is already in que, please try to sync ... "
#                 # if last sync request is less that 10 minutes before .. your sync data is just processed please try to sync or wait atleast 10 minute to make another "Que to Sync" request
                
#                 Field('sync_req_time','datetime',default=''),#10 min gap in 2 sync
#                 Field('sync_flag','string',default='0'),
#                 Field('sync_data','string',default=''),

#                 Field('sync_code_seen_rx', 'string', default=''),
#                 Field('sync_count_seen_rx', 'integer', requires=IS_NOT_EMPTY(), default=0),
#                 Field('first_sync_date_seen_rx', 'datetime', default=''),
#                 Field('last_sync_date_seen_rx', 'datetime', default=''),

#                 signature,
#                 migrate=False
#                 )#field2 is used for depth

db.define_table('sm_rep_area',   
                Field('cid','string',requires=IS_NOT_EMPTY(),default=session.cid),
                Field('rep_id','string',requires=IS_NOT_EMPTY()),
                Field('rep_name','string',default=''),
                Field('rep_category','string',requires=IS_IN_SET(('A','B','C','Z'))),#MSO Category
                
                Field('area_id','string',requires=IS_NOT_EMPTY()),
                Field('area_name','string',default=''),                
                Field('depot_id','string',default=''),
                signature,
                migrate=False
                )