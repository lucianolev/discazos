var FHContentScript = {
  
  init: function() {
    this.siteScripts = {
      "^http:\/\/(([^.]+)\.)?mediafire.com": "mediafire.js",
      "^http:\/\/(([^.]+)\.)?bayfiles.com": "bayfiles.js",
    }
    this.scriptsDir = "/static/js/filehosting/";
    this.checkLoadedFromDiscazos();
  },

  checkLoadedFromDiscazos: function() {
    //Listen to check_origin script response
    //If the FH website was loaded from discazos, set the overlay and inject
    //the corresponding FH-specific script
    window.addEventListener("LoadedFromDiscazos", function(e) {
      console.log("Loaded from Discazos! Injecting FH CS script...");
      DOMHelper.setOverlay(FHContentScript.injectFHConnectorScript);
    });
    
    //Inject check_origin in FH website to check if discazos opened the site
    console.log("Checking origin...");
    DOMHelper.addScriptFromExtension("check_origin.js");
  },
  
  injectFHConnectorScript: function() {
    chrome.extension.sendRequest({ action: "getDiscazosUrl" }, function(response) {
      if(response.url) {
        for(var site in FHContentScript.siteScripts) {
          if(location.href.match(new RegExp(site, "i"))) {
            var fhScriptFile = FHContentScript.siteScripts[site];
            DOMHelper.addExternalScript(FHContentScript.scriptsDir + fhScriptFile, response.url);
            break;
          }
        }
      }
    });
  },

}

var DOMHelper = {
  
  addExternalScript: function(scriptPath, host) {
    var s = document.createElement('script');
    s.setAttribute("type","text/javascript");
    scriptPathBase = "http://" + host;
    s.setAttribute("data-main", scriptPathBase + scriptPath);
    s.setAttribute("src", scriptPathBase + "/static/js/require.js");
    document.getElementsByTagName("head")[0].appendChild(s);
  },
  
  addScriptFromExtension: function(scriptName) {
    var s = document.createElement('script');
    s.setAttribute("type","text/javascript");
    s.setAttribute("src", chrome.extension.getURL(scriptName));
    document.getElementsByTagName("head")[0].appendChild(s);
  },
  
  setOverlay: function(callback) {
    document.body.style.overflow = "hidden"; //Hide the scrollbars
    var newOverlay = document.createElement("div");
    newOverlay.style.position = "fixed";
    newOverlay.style.top = "0px";
    newOverlay.style.left = "0px";
    newOverlay.style.backgroundColor = "grey";
    newOverlay.style.height = "100%";
    newOverlay.style.width = "100%";
    newOverlay.style.zIndex = "9999999";
    newOverlay.style.display = "table";
    
    var newTextbox = document.createElement("div");
    newTextbox.id = "fh-message-overlay";
    newTextbox.style.display = "table-cell";
    newTextbox.style.verticalAlign =  "middle";
    newTextbox.style.textAlign = "center";
    newTextbox.style.fontSize = "120%";
    newTextbox.style.color = "white";
    
    newOverlay.appendChild(newTextbox);
    
    document.body.insertBefore(newOverlay);
    
    callback();
  },
  
}

FHContentScript.init();

