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


function AddComment(postid,comment){
	var xhttp = new XMLHttpRequest();
	alert("Hello comment");
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {

    	var comment = document.getElementById("comment").innerHTML;
    	var newvalue = document.getElementById("commentnumber").innerHTML+1;
    	document.getElementById("commentnumber").innerHTML= newvalue;
    	alert(comment);
      
    }
  };
  
  xhttp.open("GET", "/AddComment?postid="+postid+"&comment="+comment, true);
  xhttp.send();
}



function PostShare(postid) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      document.getElementById("postsave").innerHTML = xhttp.responseText;
    }
  };
  alert("In post PostShare");
  xhttp.open("GET", "/PostSave?postid="+postid, true);
  xhttp.send();
}

//Jquery

$(document).ready(function(){
    $("commentsubmit").click(function(){
        $("#div1").load("demo_test.txt");
    });
});



