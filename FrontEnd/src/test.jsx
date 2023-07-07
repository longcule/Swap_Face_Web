import $ from 'jquery'; 
function fileChange(){
  var file = "https://raw.githubusercontent.com/spiderdassness/anh_raw/main/GettyImages-11652961201-2ec5455265ad4fa488585980fe3123d1.jpg";
  var form = new FormData();
  form.append("image", file)
  
  var settings = {
    "url": "https://api.imgbb.com/1/upload?key=8d5867a9512390fb5e5dc97839aa36f6",
    "method": "POST",
    "timeout": 0,
    "processData": false,
    "mimeType": "multipart/form-data",
    "contentType": false,
    "data": form
  };
  
  
  $.ajax(settings).done(function (response) {
    console.log(response);
    var jx = JSON.parse(response);
    console.log(jx.data.url);
  
  });
}