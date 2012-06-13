var discazosSiteRegexp = new RegExp("^http:\/\/([^.]+)\.discazos.net", "i");

var hasReferrer = location.href.match(/ref=discazos/i);

var scriptsDir = "/static/js/filehosting/"

if (location.href.match(discazosSiteRegexp)) {
  //Listen for the Discazos website url
  window.addEventListener("SiteUrlSending", function(e) {
    chrome.extension.sendRequest({ action: "saveDiscazosUrl", url: e.detail });
  });
  //Request version to extension
  chrome.extension.sendRequest({ action: "getExtensionVersion" }, function(response) {
    var extensionVersion = response.version;
    //Notify the website that the extension is available and loaded
    var e = document.createEvent("CustomEvent");
    e.initCustomEvent("ExtensionLoading", true, true, { version: extensionVersion });
    window.dispatchEvent(e);
  });
}

if (location.href.match(/^http:\/\/(www\.)?mediafire\.com/i) && hasReferrer) {
  chrome.extension.sendRequest({ action: "getDiscazosUrl" }, function(response) {
    if(response.url) {
      addScript("common.js", response.url);
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
