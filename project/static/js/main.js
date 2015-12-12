$(function(){
	/*$("#submit").click(function(){
		postJson("/get_info", {'restaurant_id': $("#restaurant_id").val()}, function(data){
			if (data.status == 0){
				console.log(data)
			}
		})
	}) */

	$("a[rel*=leanModal]").leanModal({top:200})
})