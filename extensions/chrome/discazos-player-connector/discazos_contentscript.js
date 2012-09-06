/*
 * --Code to be executed within the Discazos Website--
 * 'window' object refers to the Discazos website window itself. The object
 * can be used to send and receive information from the site.
 * 
 * Upon loading, the extension sends an 'ExtensionLoading' notification to the site.
 * The site replies with its current URL and the extension saves it on local
 * storage. 
 */

var DiscazosContentScript = {

  init: function() {
    this.listenToSiteUrlSending();
    this.requestExtensionVersion(this.notifyExtensionIsLoaded);
  },
  
  requestExtensionVersion: function(afterRequestCallback) {
    chrome.extension.sendRequest({ action: "getExtensionVersion" }, function(response) {
      var extensionVersion = response.version;
      
      afterRequestCallback(extensionVersion);
    });
  },
  
  notifyExtensionIsLoaded: function(extensionVersion)  {
    var e = document.createEvent("CustomEvent");
    e.initCustomEvent("ExtensionLoading", true, true, { version: extensionVersion });
    window.dispatchEvent(e);
  },
  
  listenToSiteUrlSending: function() {
    window.addEventListener("SiteUrlSending", function(e) {
      chrome.extension.sendRequest({ action: "saveDiscazosUrl", url: e.detail });
    });
  },
  
}

DiscazosContentScript.init();
