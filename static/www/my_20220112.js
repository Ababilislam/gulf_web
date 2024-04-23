
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
}

function syncBasic(){
	
	//var apipath_base_dm ='http://w05.yeapps.com/hawkseye/syncmobile_he_20210808/dmpath?HTTPPASS=e99business321cba'
	var apipath_base_dm ='http://127.0.0.1:8000/lafarge_tlp/syncmobile/dmpath?HTTPPASS=e99business321cba'
	//alert(apipath_base_dm);
	localStorage.selectedRoute='';
	$("#bufferImageSelectTown").hide();
	$(".errorMsg").hide();
	var sync_version = 'Lafarge.20210808'
	
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
							
													
					
		
	//alert(localStorage.base_url+'user_check?mobile='+mobile+'&password='+encodeURIComponent(password)+'&sync_code='+localStorage.p_sync_code+'&sync_version='+sync_version);		

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
																		
										
										var retEnrollment = localStorage.retEnrollment.split('||');	
										var liStr=''
										for (var i=0; i < retEnrollment.length; i++){	
											enrolS=retEnrollment[i].split('|');
											liStr +='<li data-role="list-divider" role="heading" class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child">'+enrolS[1]+' <span class="ui-li-count ui-body-inherit">'+enrolS[2]+'</span></li>'
											liStr +='<li ><a onclick="present_enrollment(\''+ enrolS[0]+'|'+ enrolS[1]+'|'+ enrolS[2]+'\');" class="ui-btn ui-btn-icon-right ui-icon-carat-r"><p ><strong>Target Monthly 250 bag Total 6500 bag</strong></p><p>Ach 200 bag. Total  4500 bag</p></a></li>'			
											
										}
										localStorage.listr=liStr;
										$('#showList').empty();
										$('#showList').append(localStorage.listr).trigger('create');
										
										
										var ongoingProgram = localStorage.ongoingProgram.split('||');
										var proStr=''
										for (var i=0; i < ongoingProgram.length; i++){	
											enrolS=ongoingProgram[i].split('|');
											proStr +='<li data-role="list-divider" role="heading" class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child">'+enrolS[1]+' </li>'
											proStr +='<li ><a onclick="ongoingProgram(\''+ enrolS[0]+'|'+ enrolS[1]+'\');" class="ui-btn ui-btn-icon-right ui-icon-carat-r"><p ><strong>Mega Winter October to December 2021</strong></p><p>Ach 200 bag. Total  4500 bag</p></a></li>'			
											
										}
										localStorage.proStr=proStr;
										$('#ongoingProgram').empty();
										$('#ongoingProgram').append(localStorage.proStr).trigger('create');
										
										$('#syncBasicBtn').show();
															
																				
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

function profile_edit(){

	var url = "#profile";
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
					
					giftStr +='<li class="ui-li-static ui-body-inherit ui-li-has-thumb ui-last-child"><img style="margin:20px 25px 0px 18px;" src="'+ localStorage.photo_web_url+'images/gift/'+giftS[2]+'" alt="Gift" /><h2 style="margin:10px 25px 0px 10px;">'+giftS[0]+'</h2><p style="margin:5px 25px 0px 10px;">1.8 ltr CL-01 - VE</p></br></li>'
					
					
									
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
		var resultArray = result.split('rdrd');
			if (resultArray[0]=='Success'){
				
				//$('#bufferImageSync').hide();	
				
				var higherSlab=resultArray[1];
				var progArray = higherSlab.split('</pList>');									
				progList = progArray[0].replace("<pList>","");
				
				var progSlabArray = progList.split('</slab>');
				var progSlabTotal = progSlabArray.length;
				
				
				var fdisplayStringShow=''
				fdisplayStringShow=fdisplayStringShow+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;">'+programStr[1]+'</li></br>';
					
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
						
						fdisplayStringShow=fdisplayStringShow+'<table width="100%" class="ui-body-d ui-shadow table-stripe ui-responsive" style="cell-spacing:0px; color:#002E5B; background-color:#FFFFFF; font-size:14px; border:0px solid #00803C; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"  data-role="table" data-theme="d"  data-mode="display:none"><tr><td class="ui-checkbox ui-mini"><input type="checkbox" name="checkbox-mini-0" id="checkbox-mini-0" data-mini="true"><label for="checkbox-mini-0" style="font-size:12px; font-weight:700; margin-left:35px;">Confirm</label></td><td><a class="ui-btn ui-mini" style="" onclick="upgradeHigherSlab(\''+ progId+'|'+ progName+'|'+ progSlab+'\');">Upgrade</a></td></tr></table>';
						
					}
					
				}
				
				localStorage.fdisplayStringShow=fdisplayStringShow;
				$("#higherSlabShow").html(localStorage.fdisplayStringShow);
								
			}
		}
	});
	
	
	var url = "#higher_slab";
	$.mobile.navigate(url);
	$(url).trigger('create');	
}



function ongoingProgram(id){
	var programStr=id.split('|');

	//alert(localStorage.base_url+'ongoingProgramOffer?programId='+programStr[0]+'&programName='+programStr[1]);
	$.ajax(localStorage.base_url+'ongoingProgramOffer?programId='+programStr[0]+'&programName='+programStr[1],
		{
		success: function(result) { 
		var resultArray = result.split('rdrd');
			if (resultArray[0]=='Success'){
							
				var higherSlab=resultArray[1];
				var progArray = higherSlab.split('</pList>');									
				progList = progArray[0].replace("<pList>","");
				
				var progSlabArray = progList.split('</slab>');
				var progSlabTotal = progSlabArray.length;
				
				
				var fdisplayStringShow=''
				fdisplayStringShow=fdisplayStringShow+'<li class="ui-li-divider ui-bar-inherit ui-li-has-count ui-first-child" data-role="list-divider" style="background-color:#b3e4ff;">'+programStr[1]+'</li></br>';
					
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
					
				}
				localStorage.fdisplayStringShow=fdisplayStringShow
				$("#programOfferShow").html(localStorage.fdisplayStringShow);
								
			}
		}
	});
	
	
	var url = "#program_offer";
	$.mobile.navigate(url);
	$(url).trigger('create');	
}


function upgradeHigherSlab(id){
	var programStr=id.split('|');
	
	var confirmUpgrade=$("input[name='checkbox-mini-0']:checked").val();
	if(confirmUpgrade==undefined || confirmUpgrade==""){
		$(".errorChk").text("Please Confirm ");
	}else{
		//alert(localStorage.base_url+'ongoingProgramOffer?programId='+programStr[0]+'&programName='+programStr[1]);
		$.ajax(localStorage.base_url+'upgradeSlab?programId='+programStr[0]+'&programName='+programStr[1]+'&progSlab='+programStr[2],
			{
			success: function(result) { 
				if (result=='Success'){
								
					syncBasic();
				}
			}
		})
	}
}


