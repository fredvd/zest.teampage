function get_random_teammember() {
    viewlet = document.getElementById("teammember_viewlet");
    if (viewlet != null) {
	var xmlDoc = null ;
	if (typeof window.ActiveXObject != 'undefined' ) {
            xmlDoc = new ActiveXObject("Microsoft.XMLHTTP");
	}
	else {
            xmlDoc = new XMLHttpRequest();
	}
	xmlDoc.open("GET", "@@random_teammember/get_random_teammember", false);
	xmlDoc.send(null);
	var url = xmlDoc.responseText;
	if (url != '') {
	    xmlDoc.open( "GET", url, false);
	    xmlDoc.send(null);
	    value = xmlDoc.responseText;
	    var start = value.indexOf('<div id="teammember_introduction">');
	    var end = value.lastIndexOf('</body>');
	    var introduction = value.substring(start, end);
	    viewlet.innerHTML=introduction;
	}
    }
}

registerPloneFunction(get_random_teammember);
