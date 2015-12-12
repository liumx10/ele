function link_by_post(path, params, method, new_window) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);
    if (new_window){
        form.setAttribute("target", "_blank")
    }
    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

function postJson(url, param, success){
    $.ajax({url: url, 
                type: "post",
                data:JSON.stringify(param),
                dataType:"json",
                contentType:"application/json",
                success: success,
                error: function(){
                }
    })
}

function download_file(url, filename){
        $.post(url, {}, function(data){
             var alink =  document.createElement('a');
             var evt = document.createEvent("MouseEvents");
             evt.initEvent("click", false, false);

             alink.href = data;
             alink.download = filename; 
             console.log(alink);
             alink.dispatchEvent(evt);
        })   
}

function getDate(tm){
    var tt=new Date(parseInt(tm) * 1000).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " ")
    return tt;
}
