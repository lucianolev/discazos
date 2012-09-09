var FHContentScript = {
  
  init: function() {
    this.scriptsDir = "/static/js/filehosting/";
    this.checkLoadedFromDiscazos();
  },

  checkLoadedFromDiscazos: function() {
    //Listen to check_origin script response
    //If the FH website was loaded from discazos, set the overlay and inject
    //the corresponding FH-specific script
    window.addEventListener("LoadedFromDiscazos", function(e) {
      console.log("Loaded from Discazos!");
      DOMHelper.setOverlay(FHContentScript.injectFHConnectorScript);
    });
    
    //Inject check_origin in FH website to check if discazos opened the site
    var checkOriginScript = chrome.extension.getURL("check_origin.js");
    DOMHelper.addScript(checkOriginScript);
  },
  
  injectFHConnectorScript: function() {
    chrome.extension.sendRequest({ action: "getDiscazosUrl" }, function(response) {
      if(response.url) {
        DOMHelper.addScript(FHContentScript.scriptsDir + "common.js", response.url);
        DOMHelper.addScript(FHContentScript.scriptsDir + "mediafire.js", response.url);
      }
    });
  },

}

var DOMHelper = {
  
  addScript: function(scriptPath, host) {
    var s = document.createElement('script');
    s.setAttribute("type","text/javascript");
    if(host) {
      scriptPath = "http://" + host + scriptPath;
    }
    s.setAttribute("src", scriptPath);
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

