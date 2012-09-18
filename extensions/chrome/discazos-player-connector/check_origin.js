var CheckOriginInjectScript = {
  
  init: function() {
    this.listenToOpenerResponse();
    this.askPopupOpenerIfItIsDiscazos();
  },
  
  askPopupOpenerIfItIsDiscazos: function() {
    if(window.opener) {
      window.opener.postMessage({ name: 'FH_CHECK_OPENED_FROM_DISCAZOS' }, '*');
    }
  },
  
  listenToOpenerResponse: function() {
    window.addEventListener("message", function(e) {
      if(e.data.name == 'FH_CHECK_ORIGIN_RESPONSE' && e.data.content == 'YES') {
        //CheckOriginInjectScript.hideFHInformation();
        CheckOriginInjectScript.sendOriginOkNotificationToFhContentScript();
      }
    });
  },
  
  sendOriginOkNotificationToFhContentScript: function() {
    var e = document.createEvent("CustomEvent");
    e.initCustomEvent("LoadedFromDiscazos", true, true);
    window.dispatchEvent(e);
  },
  
  //Really necessary? Breaks reloading
  /*hideFHInformation: function() {
    window.history.pushState('HideUrl', 'Getting album loading link...', '/discazos-album-link');
  },*/
  
}

CheckOriginInjectScript.init();


