var discazosSiteRegexp = new RegExp("^http:\/\/([^.]+)\.discazos.net", "i");

var hasReferrer = location.href.match(/ref=discazos/i);

var scriptsDir = "/static/js/filehosting/"

if (location.href.match(discazosSiteRegexp)) {
  //Listen for the Discazos website url
  window.addEventListener("SendDiscazosUrl", function(e) {
    chrome.extension.sendRequest({ action: "saveDiscazosUrl", url: e.detail });
  });
  //Notify the website that the extension is available and loaded
  var extensionLoaded = document.createEvent('Event');
  extensionLoaded.initEvent('extensionLoaded', true, false);
  window.dispatchEvent(extensionLoaded);
}

if (location.href.match(/^http:\/\/(www\.)?mediafire\.com/i) && hasReferrer) {
  chrome.extension.sendRequest({ action: "getDiscazosUrl" }, function(response) {
    if(response.url) {
      addScript("mediafire.js", response.url);
    }
  });
}

function addScript(scriptFilename, host) {
	var s = document.createElement('script');
	s.setAttribute("type","text/javascript");
	s.setAttribute("src", "http://" + host + scriptsDir + scriptFilename);
	document.getElementsByTagName("head")[0].appendChild(s);
}
