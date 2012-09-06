var CheckOriginInjectScript = {
  
  init: function() {
    this.listenToOpenerResponse();
    this.askPopupOpenerIfItIsDiscazos();
  },
  
  askPopupOpenerIfItIsDiscazos: function() {
    if(window.opener) {
      window.opener.postMessage({message: 'FromDiscazos?'}, '*');
    }
  },
  
  listenToOpenerResponse: function() {
    window.addEventListener("message", function(e) {
      if(e.data.response == 'YES') {
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


