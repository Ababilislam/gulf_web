
var imagePathA='';
var imagePathB='';

var imageName='';
var imageName2='';

var select_town='';
var townCode='';
var townName='';
var posmCode='';

var step_flag=0; 
var temp_image_div='';
var temp_image_div_promo='';

url ="";

$(document).ready(function(){	
	$('#bufferImageSync').hide();
	
	if (localStorage.synced=='YES' ){
		$('#showList').empty();
		$('#showList').append(localStorage.listr).trigger('create');
		
		$('#ongoingProgram').empty();
		$('#ongoingProgram').append(localStorage.proStr).trigger('create');
		
		$("#profileId").text(localStorage.repId);
		$("#profileName").text(localStorage.repName);
	
		url = "#homePage";					
		$.mobile.navigate(url);
	
	}else{
		$(".errorChk").text('');
		url = "#pagesync";	
		$.mobile.navigate(url);
	}
});

function clear_autho(){
	$(".errorMsg").hide();	
}
function backClick(){
	$(".errorMsg").text("");
	$(".errorChk").text("");
}

function syncBasic(){
	
	var apipath_base_dm ='http://w05.yeapps.com/lafarge_tlp/syncmobile/dmpath?HTTPPASS=e99business321cba'
	//var apipath_base_dm ='http://127.0.0.1:8000/lafarge_tlp/syncmobile/dmpath?HTTPPASS=e99business321cba'
	//alert(apipath_base_dm);
	localStorage.selectedRoute='';
	$("#bufferImageSelectTown").hide();
	$(".errorMsg").hide();
	var sync_version = 'Lafarge.20220220'
	
	var mobile=$("#mobile").val();
	var password=$("#password").val();
	if (mobile=="" || password==""){
		$('#bufferImageSync').hide();
		$(".errorMsg").show();
		$(".errorMsg").html("Required mobile no and password");	
	}else{
		$('#bufferImageSync').show();	
		$('#syncBasicBtn').hide();	
		$(".errorMsg").show();
		$(".errorMsg").html("Sync in progress. Please wait...");
		if(localStorage.p_sync_code==undefined || localStorage.p_sync_code==""){
			localStorage.p_sync_code=0;
		}
		
		$.ajax(apipath_base_dm,{
			type: 'POST',
			timeout: 30000,
			error: function(xhr) {
				$("#bufferImageSync").hide();
				$(".errorMsg").html('Network Timeout. Please check your Internet connection..');
			},
			success:function(data, status,xhr){
				if (status=='success'){
					localStorage.base_url='';
					
					var dtaStr=data.replace('<start>','').replace('<end>','')
					var resultArray = dtaStr.split('<fd>');		
					if(resultArray.length>2){
						var base_url=resultArray[0];
						var photo_submit_url=resultArray[1];
						var photo_web_url=resultArray[2];
						//-------------
						if(base_url=='' || photo_web_url==''){	
							$("#bufferImageSync").hide();
							$("#syncBasicBtn").show();
							$(".errorMsg").html('Base URL not available');	
						}else{
							localStorage.base_url='';
							localStorage.photo_submit_url='';
							localStorage.photo_web_url='';	
							
							localStorage.base_url=base_url;
							localStorage.photo_submit_url=photo_submit_url;
							localStorage.photo_web_url=photo_web_url;
							
													
					
		
	alert(localStorage.base_url+'user_check?mobile='+mobile+'&password='+encodeURIComponent(password)+'&sync_code='+localStorage.p_sync_code+'&sync_version='+sync_version);		

							$.ajax(localStorage.base_url+'user_check?mobile='+mobile+'&password='+encodeURIComponent(password)+'&sync_code='+localStorage.p_sync_code+'&sync_version='+sync_version,{
								success: function(result) { 
								var syncResultArray = result.split('rdrd');
									localStorage.synced=syncResultArray[0];
									if (localStorage.synced=='YES'){
										
										$('#bufferImageSync').hide();	
										localStorage.synced="YES"
										localStorage.syncMobile=mobile;
										localStorage.syncPass=password;
										localStorage.sync_code=syncResultArray[1];										
										localStorage.repId=syncResultArray[2];					
										localStorage.repName=syncResultArray[3];
										localStorage.mobile=syncResultArray[4];	
										localStorage.retEnrollment=syncResultArray[5];
										localStorage.ongoingProgram=syncResultArray[6];										
										//alert(localStorage.retEnrollment);
										//localStorage.sync_date=get_date();										
										$("#profileId").text(localStorage.repId);		
										$("#profileName").text(localStorage.repName);						
										
										if (localStorage.retEnrollment !=''){
											var retEnrollment = localStorage.retEnrollment.split('||');	
											//alert(retEnrollment);
											var liStr=''
											for (var i=0; i < retEnrollment.length; i++){	
												enrolS=retEnrollment[i].split('|');
												liStr +='<li data-role="list-divider" role="heading" class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child">'+enrolS[1]+' <span class="ui-li-count ui-body-inherit">'+enrolS[2]+'</span> </li>'
											
											if (enrolS[5]==undefined){
												liStr +='<li><a onclick="higherSlab(\''+ enrolS[0]+'|'+ enrolS[1]+'|'+ enrolS[2]+'\');" class="ui-btn ui-btn-icon-right ui-icon-carat-r"><p ><strong>Target Monthly '+enrolS[6]+' bag Total '+enrolS[7]+' bag</strong></p><p>Ach '+enrolS[8]+' bag</p></a></li>'	
												
											}else{
												liStr +='<li><a class="ui-btn ui-btn-icon-right ui-icon-carat-r" onclick="higherSlab(\''+ enrolS[0]+'|'+ enrolS[1]+'|'+ enrolS[2]+'\');"><img height="100px" width="120px" src="'+ localStorage.photo_web_url+'images/gift/'+enrolS[5]+'" alt="Gift" style="margin:10px 0px 0px 5px;"/><p>Target Monthly '+enrolS[6]+' bag Total '+enrolS[7]+' bag <br>Ach '+enrolS[8]+' bag</p><p>'+enrolS[3]+' <br> '+enrolS[4]+'</p></a></li>'	
												
												//liStr=liStr+'<a onclick="present_enrollment(\''+ enrolS[0]+'|'+ enrolS[1]+'|'+ enrolS[2]+'\');" class="ui-btn ui-btn-icon-right ui-icon-carat-r"><table width="100%" class="ui-body-d ui-shadow table-stripe ui-responsive" style="cell-spacing:0px; color:#002E5B; background-color:#FFFFFF; font-size:14px; border:0px solid #00803C; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"  data-role="table" data-theme="d"  data-mode="display:none"><tr><td><p >Target Monthly 250 bag Total 6500 bag</p><p>Ach 200 bag. Total  4500 bag</p></td></tr><tr><td width="20%"><img height="100px" width="100px" src="'+ localStorage.photo_web_url+'images/gift/'+enrolS[5]+'" alt="Gift" /></td><td width="70%"> <p style="margin:5px 25px 0px 10px;">'+enrolS[3]+' <br> '+enrolS[4]+'</p></td></tr></table></a>';		
											}
											}
											localStorage.listr=liStr;
											$('#showList').empty();
											$('#showList').append(localStorage.listr).trigger('create');
										}else{
											
											localStorage.listr='';
											$('#showList').empty();	
										}
										
										//alert(localStorage.ongoingProgram);
										if (localStorage.ongoingProgram !=''){
											var ongoingProgram = localStorage.ongoingProgram.split('||');
											var proStr=''
											for (var i=0; i < ongoingProgram.length; i++){	
												enrolS=ongoingProgram[i].split('|');
												proStr +='<li data-role="list-divider" role="heading" class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child">'+enrolS[1]+' </li>'
												proStr +='<li ><a onclick="ongoingProgram(\''+ enrolS[0]+'|'+ enrolS[1]+'\');" class="ui-btn ui-btn-icon-right ui-icon-carat-r"><p ><strong>'+ enrolS[3]+'</strong></p></a></li>'	//<p>Ach 200 bag. Total  4500 bag</p>		
												
											}
											localStorage.proStr=proStr;
											$('#ongoingProgram').empty();
											$('#ongoingProgram').append(localStorage.proStr).trigger('create');
										}else{
											
											localStorage.proStr='';
											$('#ongoingProgram').empty();	
										}
										
										$('#syncBasicBtn').show();
															
										location.reload();									
										var url = "#homePage";
										$.mobile.navigate(url);
										$(url).trigger('create');		
										}													
												
								},error:function(){
								  $(".errorMsg").text("Please check internet connection");
								 }
							});//------/ajax			
						}
					}
				}
			}
		})
		
			
	}	
}

function homeBtn(){

	var url = "#homePage";
	$.mobile.navigate(url);
	$(url).trigger('create');	
}



function present_enrollment(id){
	var programStr=id.split('|');
	
	$("#progName").empty();
	$("#progName").append(programStr[1]);
	$("#progSlab").empty();
	$("#progSlab").append(programStr[2]);
	//alert(localStorage.base_url+'get_gift?programId='+programStr[0]+'&programSlab='+programStr[2]);
	$.ajax(localStorage.base_url+'get_gift?programId='+programStr[0]+'&	programSlab='+programStr[2],
		{
		success: function(result) { 
		var resultArray = result.split('rdrd');
			if (resultArray[0]=='Success'){
								
				var programGift=resultArray[1].split('||');
				var giftStr=''
				for (var i=0; i < programGift.length; i++){	
					giftS=programGift[i].split('|');
					//giftStr +='<li class="ui-li-static ui-body-inherit ui-li-has-thumb ui-last-child"><img src="'+ localStorage.photo_web_url+'images/gift/'+giftS[2]+'" alt="Gift" /></br><h2>'+giftS[0]+'</h2><p>1.8 ltr CL-01 - VE</p></li>'
					
					giftStr +='<li class="ui-li-static ui-body-inherit ui-li-has-thumb ui-last-child"><img style="margin:20px 25px 0px 18px;" src="'+ localStorage.photo_web_url+'images/gift/'+giftS[2]+'" alt="Gift" /><h2 style="margin:10px 25px 0px 10px;">'+giftS[0]+'</h2><p style="margin:5px 25px 0px 10px;">'+giftS[1]+'</p></br></li>'
					
					
									
				}
					giftStr +='<ul data-role="listview" data-inset="true" class="ui-listview ui-listview-inset ui-corner-all ui-shadow"><li class="ui-first-child ui-last-child"><a class="ui-btn ui-btn-icon-right ui-icon-carat-r" style="background-color:#b3e4ff;" onclick="higherSlab(\''+ programStr[0]+'|'+ programStr[1]+'|'+ programStr[2]+'\');" ><p><strong>Feeling Strong go for Higher Slab</strong></p></a></li></ul>'
				
				localStorage.giftStr=giftStr;
				$('#giftShow').empty();
				$('#giftShow').append(localStorage.giftStr).trigger('create');
									
				
				
			}
		}
	});
	
	var url = "#present_enrollment_upgrade";
	$.mobile.navigate(url);
	$(url).trigger('create');	
}


function giftOption(id){
	$(".errorChk").text("");
	var programStr=id.split('|');
	
	/*$("#progName").empty();
	$("#progName").append(programStr[1]);
	$("#progSlab").empty();
	$("#progSlab").append(programStr[2]);*/
	//alert(localStorage.base_url+'gift_option?programId='+programStr[0]+'&programName='+programStr[1]+'&programSlab='+programStr[2]);
	$.ajax(localStorage.base_url+'gift_option?programId='+programStr[0]+'&programName='+programStr[1]+'&programSlab='+programStr[2],
		{
		success: function(result) { 
		var resultArray = result.split('rdrd');
			if (resultArray[0]=='Success'){
				
				var programGift=resultArray[1].split('||');
				var giftStr=''
				var giftStr=giftStr+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;"><span>Slab</span></li>'
				for (var i=0; i < programGift.length; i++){	
					giftS=programGift[i].split('|');
				
						
						giftStr=giftStr+'<table width="100%" class="ui-body-d ui-shadow table-stripe ui-responsive" style="cell-spacing:0px; color:#002E5B; background-color:#FFFFFF; font-size:14px; border:0px solid #00803C; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"  data-role="table" data-theme="d"  data-mode="display:none"><tr><td width="30%"><img style="margin:10px 5px 0px 10px;" height="100px" width="120px" src="'+ localStorage.photo_web_url+'images/gift/'+giftS[5]+'" alt="Gift" /></td><td width="70%"><h3 style="margin:10px 25px 0px 10px;">'+giftS[3]+'</h3><p style="margin:5px 25px 0px 10px;">'+giftS[4]+'</p></td></tr><tr><td width="20%" style="vertical-align:middle;" class="ui-checkbox ui-mini"><input type="checkbox" name="checkbox-mini-1" id="checkbox-mini-1" data-mini="true"></td><td width="30%" style="vertical-align:middle;"><a class="ui-btn ui-mini" onclick="selectGift(\''+ giftS[0]+'|'+ giftS[1]+'|'+ giftS[2]+'\');">Confirm</a></td></tr></table>';			
					
									
				}
					
				
				localStorage.giftItemStr=giftStr;
				$('#giftItemShow').empty();
				$('#giftItemShow').append(localStorage.giftItemStr).trigger('create');
									
				
				
			}
		}
	});
	
	var url = "#gift_option_page";
	$.mobile.navigate(url);
	$(url).trigger('create');	
}



function selectGift(id){
	$(".errorChk").text("");
	var programStr=id.split('|');
	
	var confirmUpgrade=$("input[name='checkbox-mini-1']:checked").val();
	if(confirmUpgrade==undefined || confirmUpgrade==""){
		$(".errorChk").text("Please Confirm ");
	}else{
		//alert(localStorage.base_url+'selectGift?rowId='+id);
		$.ajax(localStorage.base_url+'selectGift?rowId='+programStr[0]+'&programName='+programStr[1]+'&programSlab='+programStr[2],
			{
			success: function(result) { 
				if (result=='Success'){
						
					var url = "#homePage";
					$.mobile.navigate(url);
					$(url).trigger('create');
				}
			}
		});
	}
		
}


function higherSlab(id){
	var programStr=id.split('|');
	
	$("#progName").empty();
	$("#progName").append(programStr[1]);
	$("#progSlab").empty();
	$("#progSlab").append(programStr[2]);
	//alert(localStorage.base_url+'higher_slab?programId='+programStr[0]+'&programName='+programStr[1]+'&programSlab='+programStr[2]);
	$.ajax(localStorage.base_url+'higher_slab?programId='+programStr[0]+'&programName='+programStr[1]+'&programSlab='+programStr[2],
		{
		success: function(result) { 
		var resultArray = result.split('|||');
			if (resultArray[0]=='Success'){
				
				//$('#bufferImageSync').hide();	
				
				var higherSlab=resultArray[1];
				var progArray = higherSlab.split('</pList>');									
				progList = progArray[0].replace("<pList>","");
				
				var progSlabArray = progList.split('</slab>');
				var progSlabTotal = progSlabArray.length;				
				
				var fdisplayStringShow=''
				fdisplayStringShow=fdisplayStringShow+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;">'+programStr[1]+'</li></br>';
					//alert(progSlabTotal);
				for (var i=0; i < progSlabTotal-1; i++){
					var progSlabList = progSlabArray[i].replace("<slab>","");
					var progSlab_1Array = progList.split('<slab>');
					var proId = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[0];
					var proName = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[1];
					var proSlab = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[2];
					var monthlyPoint = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[3];
					var targetPoint = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[4];
						//alert(proId+'=='+proName+'=='+proSlab+'=='+pointMonth+'=='+totalPointReq);					
					
					var progSingleArray = progSlabList.split('rdrd');
					//alert(progSingleArray);		
					var progSingleTotal = progSingleArray.length;					
					localStorage.progTotal=progSingleTotal;
					//alert(progSingleTotal);
					fdisplayStringShow=fdisplayStringShow+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;"><span >'+proSlab+'</span></li><li class="ui-li-static ui-body-inherit"><p><strong>Target Monthly '+monthlyPoint+' bag Total '+targetPoint+' bag</strong></p><p>Ach 0 bag. Total 0 bag</p></li>';
					for (var j=0; j< progSingleTotal-1; j++){
						var progStr=progSingleArray[j].replace(progSlabArray[i].split('<slab>')[0],"");
						//alert(progStr);
						progStrArray = progStr.split('fdfd');
						giftId=progStrArray[0];
						giftName=progStrArray[1];
						imgDis=progStrArray[2];
						imageLink=progStrArray[3];
								
						fdisplayStringShow=fdisplayStringShow+'<table width="100%" class="ui-body-d ui-shadow table-stripe ui-responsive" style="cell-spacing:0px; color:#002E5B; background-color:#FFFFFF; font-size:14px; border:0px solid #00803C; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"  data-role="table" data-theme="d"  data-mode="display:none"><tr><td width="10%" class="ui-checkbox ui-mini" style="vertical-align:middle;"><input type="radio" name="radio-choice" id="radio-choice-1" value="'+giftId+'"></td><td width="20%"><img height="100px" width="100px" src="'+ localStorage.photo_web_url+'images/gift/'+imageLink+'" alt="Gift" /></td><td width="70%"><h3 style="margin:10px 25px 0px 10px;">'+giftName+'</h3><p style="margin:5px 25px 0px 10px;">'+imgDis+'</p> </td></tr></table>';
						        
					}
					fdisplayStringShow=fdisplayStringShow+'<a class="ui-btn ui-mini" style="color:#FFF;background-color:#4fb074;" onclick="upgradeHigherSlab(\''+ proId+'|'+ proName+'|'+ proSlab+'\');">Upgrade</a>';
					
				}
				
				localStorage.fdisplayStringShow=fdisplayStringShow;
				$("#higherSlabShow").html(localStorage.fdisplayStringShow);
				
				var url = "#higher_slab";
				$.mobile.navigate(url);
				$(url).trigger('create');			
			}else{
				
			}
		}
	});
	
	
	
}

function profile_edit(){
	$("#retailarId").val(localStorage.syncMobile);
	$("#userName").val(localStorage.repName);
	$("#userMobile").val(localStorage.mobile);
	
	
	var url = "#profile";
	$.mobile.navigate(url);
	$(url).trigger('create');	
}
	


function profile_update(){
	$(".sucMsg").text("");
	$(".errorChk").text("");
	var retailarId=$("#retailarId").val();
	var userName=$("#userName").val();
	var userMobile=$("#userMobile").val();
	var userPass=$("#userPass").val();
	if(userName==""){
		$(".errorChk").text("Required Name ");
	}else if(userMobile==''){
		$(".errorChk").text("Required Mobile No ");
	}else if(userPass==''){
		$(".errorChk").text("Required userPass ");	
	}else{
		//alert(localStorage.base_url+'updateProfile?userName='+userName+'&retailarId='+retailarId+'&userMobile='+userMobile+'&userPass='+userPass);
		$.ajax(localStorage.base_url+'updateProfile?userName='+userName+'&retailarId='+retailarId+'&userMobile='+userMobile+'&userPass='+userPass,
			{
			success: function(result) { 
				if (result=='Success'){
					$(".sucMsg").text('Updated Successfully');
					
					$("#retailarId").val('');
					$("#userName").val('');
					$("#userMobile").val('');
					$("#userPass").val('');
					
					/*var url = "#homePage";
					$.mobile.navigate(url);
					$(url).trigger('create');*/	
				}else{
					$(".errorChk").text(result);
				}
			}
		})
	}
}

function ongoingProgram(id){
	var programStr=id.split('|');

	//alert(localStorage.base_url+'ongoingProgramOffer?programId='+programStr[0]+'&programName='+programStr[1]);
	$.ajax(localStorage.base_url+'ongoingProgramOffer?programId='+programStr[0]+'&programName='+programStr[1],
		{
		success: function(result) { 
		var resultArray = result.split('|||');
		//alert(resultArray);
			if (resultArray[0]=='Success'){
							
				var higherSlab=resultArray[1];
				var progArray = higherSlab.split('</pList>');									
				progList = progArray[0].replace("<pList>","");
				
				var progSlabArray = progList.split('</slab>');
				var progSlabTotal = progSlabArray.length;
				
				
				var programOffer=''
				/*fdisplayStringShow=fdisplayStringShow+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;">'+programStr[1]+'</li></br>';
					
				for (var i=0; i < progSlabTotal-1; i++){
					var progSlabList = progSlabArray[i].replace("<slab>","");
					var progSlab_1Array = progList.split('<slab>');
					
											
					
					var progSingleArray = progSlabList.split('rdrd');										
					var progSingleTotal = progSingleArray.length;
					
					localStorage.progTotal=progSingleTotal;
					//alert(localStorage.fdisplayTotal);
					for (var j=0; j< progSingleTotal; j++){
						var progStr=progSingleArray[j]//.replace(progSlabArray[i].split('<slab>')[0],"");
						
						progStrArray = progStr.split('<fdfd>');
						progId=progStrArray[0]
						progName=progStrArray[1];
						progSlab=progStrArray[2];
						monthlyPoint=progStrArray[3];
						targetPoint=progStrArray[4];
						giftName=progStrArray[5];
						imgDis=progStrArray[6];
						imgLink=progStrArray[7];						
						
						fdisplayStringShow=fdisplayStringShow+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;"><span >'+progSlab+'</span></li><li class="ui-li-static ui-body-inherit"><p><strong>Target Monthly '+monthlyPoint+' bag Total '+targetPoint+' bag</strong></p><p>Ach 0 bag. Total 0 bag</p></li><li class="ui-li-static ui-body-inherit ui-li-has-thumb"><img style="margin:20px 25px 0px 18px;" src="'+ localStorage.photo_web_url+'images/gift/'+imgLink+'" alt="Gift" /><h2 style="margin:10px 25px 0px 10px;">'+giftName+'</h2><p style="margin:5px 25px 0px 10px;">'+imgDis+'</p></li>';
						
						fdisplayStringShow=fdisplayStringShow+'<table width="100%" class="ui-body-d ui-shadow table-stripe ui-responsive" style="cell-spacing:0px; color:#002E5B; background-color:#FFFFFF; font-size:14px; border:0px solid #00803C; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"  data-role="table" data-theme="d"  data-mode="display:none"><tr><td class="ui-checkbox ui-mini"><input type="checkbox" name="checkbox-mini-1" id="checkbox-mini-1" data-mini="true"><label for="checkbox-mini-0" style="font-size:12px; font-weight:700; margin-left:35px;">Confirm</label></td><td><a class="ui-btn ui-mini" style="">Upgrade</a></td></tr></table>';
						
					}
					
				}*/
				
				
				/*programOffer=programOffer+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;"><span >'+proSlab+'</span></li><li class="ui-li-static ui-body-inherit"><p><strong>Target Monthly '+monthlyPoint+' bag Total '+targetPoint+' bag</strong></p><p>Ach 0 bag. Total 0 bag</p></li>';
					for (var j=0; j< progSingleTotal-1; j++){
						var progStr=progSingleArray[j].replace(progSlabArray[i].split('<slab>')[0],"");
						//alert(progStr);
						progStrArray = progStr.split('fdfd');
						giftId=progStrArray[0];
						giftName=progStrArray[1];
						imgDis=progStrArray[2];
						imageLink=progStrArray[3];
								
						programOffer=programOffer+'<table width="100%" class="ui-body-d ui-shadow table-stripe ui-responsive" style="cell-spacing:0px; color:#002E5B; background-color:#FFFFFF; font-size:14px; border:0px solid #00803C; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"  data-role="table" data-theme="d"  data-mode="display:none"><tr><td width="10%" class="ui-checkbox ui-mini" style="vertical-align:middle;"><input type="radio" name="radio-choice" id="radio-choice-1" value="'+giftId+'"></td><td width="20%"><img height="100px" width="100px" src="'+ localStorage.photo_web_url+'images/gift/'+imageLink+'" alt="Gift" /></td><td width="70%"><h2 style="margin:10px 25px 0px 10px;">'+giftName+'</h2><p style="margin:5px 25px 0px 10px;">'+imgDis+'</p> </td></tr></table>';
						        
					}
					programOffer=programOffer+'<a class="ui-btn ui-mini" style="color:#FFF;background-color:#4fb074;" onclick="upgradeHigherSlab(\''+ proId+'|'+ proName+'|'+ proSlab+'\');">Enroll</a>';
					
				}
				
				localStorage.programOffer=programOffer;
				$("#programOfferShow").html(localStorage.programOffer);*/
				
				
				programOffer=programOffer+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;">'+programStr[1]+'</li></br>';
					//alert(progSlabTotal);
				for (var i=0; i < progSlabTotal-1; i++){
					var progSlabList = progSlabArray[i].replace("<slab>","");
					var progSlab_1Array = progList.split('<slab>');
					var proId = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[0];
					var proName = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[1];
					var proSlab = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[2];
					var monthlyPoint = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[3];
					var targetPoint = progSlabArray[i].split('<slab>')[0].split('<fdfd>')[4];
						//alert(proId+'=='+proName+'=='+proSlab+'=='+pointMonth+'=='+totalPointReq);					
					
					var progSingleArray = progSlabList.split('rdrd');
					//alert(progSingleArray);		
					var progSingleTotal = progSingleArray.length;					
					localStorage.progTotal=progSingleTotal;
					//alert(progSingleTotal);
					programOffer=programOffer+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;"><span >'+proSlab+'</span></li><li class="ui-li-static ui-body-inherit"><p><strong>Target Monthly '+monthlyPoint+' bag Total '+targetPoint+' bag</strong></p><p>Ach 0 bag. Total 0 bag</p></li>';
					for (var j=0; j< progSingleTotal-1; j++){
						var progStr=progSingleArray[j].replace(progSlabArray[i].split('<slab>')[0],"");
						//alert(progStr);
						progStrArray = progStr.split('fdfd');
						giftId=progStrArray[0];
						giftName=progStrArray[1];
						imgDis=progStrArray[2];
						imageLink=progStrArray[3];
								
						programOffer=programOffer+'<table width="100%" class="ui-body-d ui-shadow table-stripe ui-responsive" style="cell-spacing:0px; color:#002E5B; background-color:#FFFFFF; font-size:14px; border:0px solid #00803C; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"  data-role="table" data-theme="d"  data-mode="display:none"><tr><td width="10%" class="ui-checkbox ui-mini" style="vertical-align:middle;"><input type="radio" name="radio-choice2" id="radio-choice-1" value="'+giftId+'"></td><td width="20%"><img height="100px" width="100px" src="'+ localStorage.photo_web_url+'images/gift/'+imageLink+'" alt="Gift" /></td><td width="70%"><h2 style="margin:10px 25px 0px 10px;">'+giftName+'</h2><p style="margin:5px 25px 0px 10px;">'+imgDis+'</p> </td></tr></table>';
						        
					}
					programOffer=programOffer+'<a class="ui-btn ui-mini" style="color:#FFF;background-color:#4fb074;" onclick="enroll(\''+ proId+'|'+ proName+'|'+ proSlab+'\');">Enroll</a>';
					
				}
				
				localStorage.programOffer=programOffer;
				$("#programOfferShow").html(localStorage.programOffer);
		}
			
		}
	});
	
	
	var url = "#program_offer";
	$.mobile.navigate(url);
	$(url).trigger('create');	
}


function enroll(id){
	var progStr=id.split('|');
	var confirmUpgrade=$("input[name='radio-choice2']:checked").val();
	//alert(confirmUpgrade);
	if(confirmUpgrade==undefined || confirmUpgrade==""){
		$(".errorChk").text("Please Confirm ");
	}else{
		//alert(localStorage.base_url+'enroll?programId='+progStr[0]+'&programName='+progStr[1]+'&progSlab='+progStr[2]+'&giftId='+confirmUpgrade);
		$.ajax(localStorage.base_url+'enroll?programId='+progStr[0]+'&programName='+progStr[1]+'&progSlab='+progStr[2]+'&rowId='+confirmUpgrade,
			{
			success: function(result) { 
				if (result=='Success'){
																
				$("#mobile").val(localStorage.syncMobile);
				$("#password").val(localStorage.syncPass);
								
					syncBasic();
				}
			}
		})
	}
		
}


function upgradeHigherSlab(id){
	var programStr=id.split('|');
	
	var confirmUpgrade=$("input[name='radio-choice']:checked").val();
	//alert(confirmUpgrade);
	if(confirmUpgrade==undefined || confirmUpgrade==""){
		$(".errorChk").text("Please Confirm ");
	}else{
		//alert(localStorage.base_url+'upgradeSlab?programId='+programStr[0]+'&programName='+programStr[1]+'&progSlab='+programStr[2]+'&giftId='+confirmUpgrade);
		$.ajax(localStorage.base_url+'upgradeSlab?programId='+programStr[0]+'&programName='+programStr[1]+'&progSlab='+programStr[2]+'&giftId='+confirmUpgrade,
			{
			success: function(result) { 
				if (result=='Success'){
																
				$("#mobile").val(localStorage.syncMobile);
				$("#password").val(localStorage.syncPass);
								
					syncBasic();
				}
			}
		})
	}
}


