var siteDomain = "discazos.localhost:8000";

var discazosSiteRegexp = new RegExp("^http:\/\/" + siteDomain, "i");

var hasReferrer = location.href.match(/ref=discazos/i);

var scriptsDir = "/static/js/filehosting/"

if (location.href.match(discazosSiteRegexp)) {
  //Notify the website that the extension is available and loaded
  var extensionLoaded = document.createEvent('Event');
  extensionLoaded.initEvent('extensionLoaded', true, false);
  window.dispatchEvent(extensionLoaded);
}

//if (location.href.match(/^http:\/\/(www\.)?megaupload\.com/i) && hasReferrer) {
//	//Load the filehosting script
//	addScript("megaupload.js");
//}

if (location.href.match(/^http:\/\/(www\.)?mediafire\.com/i) && hasReferrer) {
  //Load the filehosting script
  addScript("mediafire.js");
}

function addScript(scriptFilename) {
	var s = document.createElement('script');
	s.setAttribute("type","text/javascript");
	s.setAttribute("src", "http://" + siteDomain + scriptsDir + scriptFilename);
	document.getElementsByTagName("head")[0].appendChild(s);
}
