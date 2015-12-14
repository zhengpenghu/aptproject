function PostSave(postid) {
  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function(){

    if (xhttp.readyState == 4 && xhttp.status == 200) {
      	var oldvalue = document.getElementById("postsave").innerHTML;
    	var newvalue = xhttp.responseText
      	document.getElementById("postsave").innerHTML = newvalue;
      	if(oldvalue > newvalue){
      		document.getElementById("postsave").style.color = "grey";
      	}
  		else{
  			document.getElementById("postsave").style.color = "red";
  		}
    }
  };

  xhttp.open("GET", "/PostSave?postid="+postid, true);
  xhttp.send();
  
}

// function PostSaveDelete(postid) {
//   var xhttp = new XMLHttpRequest();
//   xhttp.onreadystatechange = function() {
//     if (xhttp.readyState == 4 && xhttp.status == 200) {
//     	var oldvalue = document.getElementById("postsave").innerHTML;
//     	var newvalue = xhttp.responseText
//       document.getElementById("postsave").innerHTML = newvalue;
//       if(oldvalue > newvalue)
//       document.getElementById("postsave").style = "color: grey";
//   	else{
//   		document.getElementById("postsave").style = "color: red";
//   	}

//     }
//   };
//   alert("In postsavedelete"+postid);
//   xhttp.open("GET", "/PostSaveDelete?postid="+postid, true);
//   xhttp.send();
// }


// $(document).ready(function(){
// // this is the id of the form
// $("#commentform").submit(function(e) {

//     var url = "/AddComment"; // the script where you handle the form input.
// alert("hello Jquery");
//     $.ajax({
//            type: "POST",
//            url: url,
//            data: $("#idForm").serialize(), // serializes the form's elements.
//            success: function(data)
//            {
//                alert(data); // show response from the php script.
//            }
//          });

//     e.preventDefault(); // avoid to execute the actual submit of the form.
// });

	
// };
function newComment(creater,time,content){
  var html =  "<div class='col-xs-12 col-md-8'><h4><small>"+creater+time+"</small></h4><div>"+content+"</div><hr></div>";
  return html;
};

function AddComment(postid){
	
  {
      //if (xhttp.readyState == 4 && xhttp.status == 200) 
    {
    	var comment = document.getElementById("comment").value;  //got
      document.getElementById("comment").value="";
      var time = new Date().toString();
      var user = document.getElementById("userid").innerHTML;

      var userandtimerdiv = document.createElement('div');
      userandtimerdiv.innerHTML = user+""+time+'h';
      var commentdiv = document.createElement('div');
      commentdiv.innerHTML = comment;
      var cc=document.createElement('div');
      cc.appendChild(userandtimerdiv);
      cc.appendChild(commentdiv);

/*
      var successful = document.createElement('div');
      successful.innerHTML = "comment submitted successful!";
 */   

    var fullhtml = newComment(user,time,comment);
    var newdiv = document.createElement('div');
    newdiv.innerHTML= fullhtml;
    newdiv.setAttribute('class', 'row'); 
      document.getElementById('commentlist').insertBefore(newdiv, document.getElementById('commentlist').firstChild);     
    }
  };

  $("#commentform").submit();


}



function PostShare(postid) {
  var xhttp = new XMLHttpRequest();
  alert("in PostShare");
  console.log("IN PostShare");
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      document.getElementById("postsave").innerHTML = xhttp.responseText;
    }
  };
  alert("In post PostShare");
  xhttp.open("GET", "/PostShare?postid="+postid, true);
  xhttp.send();
}

//Jquery

$(document).ready(function(){
    $("commentsubmit").click(function(){
        $("#div1").load("demo_test.txt");
    });
    //alert("submit");
    $("#commentform").submit(function(e){
    var postData = $(this).serializeArray();
    alert("postdata"+postData);
    var formURL = $(this).attr("action");
    $.ajax(
    {
        url : formURL,
        type: "POST",
        data : postData,
        success:
        {
            //data: return data from server
        },
        error: 
        {
            //if fails

        }
    });
    e.preventDefault(); //STOP default action
    //e.unbind(); //unbind. to stop multiple form submit.
});

});



