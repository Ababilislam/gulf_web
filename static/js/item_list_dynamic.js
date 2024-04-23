// JavaScript Document
require(["dojo/store/Memory","dojo/_base/xhr","dojo/dom","dojo/domReady!"], function(Memory,xhr,dom){			
	//if (localStorage.stateStore!='undefined'){
		//alert("ok");
		var current_url = location.href;
		var baseURL = url.substring(0, current_url.indexOf('/', 14));
		
		
		xhr.get({
			// url: "http://127.0.0.1:8000/mreporting/depot/getItem.json",
			url: "http://www.businesssolutionapps.com/mreporting/depot/get_item.json",
			
			handleAs: "json"
		}).then(function(data){
			
			var store = new Memory({ data: data.records, idProperty: "id"});					
			
			var itemStr=""; 
			store.query().forEach(function(row){
					itemStr+="<option value='"+row.name+"-"+row.item_id+"-"+row.dist_price+"-"+row.category_id+"'>"+row.name+"</option>";
			});//end loop
			
			localStorage.stateStore=itemStr;
		});//xhr function				
	//};
	
});