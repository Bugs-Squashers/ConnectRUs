document.getElementById('showPassword').onclick = function() {
    if ( this.checked ) {
       document.getElementById('password').type = "text";
	   document.getElementById('password2').type = "text";
    } else {
       document.getElementById('password').type = "password";
	   document.getElementById('password2').type = "password";
    }
};
function checkSimilarity() {
	var firstInput = document.getElementById("password").value;
	var secondInput = document.getElementById("password2").value;

	if (firstInput == secondInput) {
		alert('The inputs are the same');
		return false;
	} 
	else {
		alert('The inputs are not the same');
		return false;
	}
}