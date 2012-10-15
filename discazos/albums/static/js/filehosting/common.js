var ContentScriptCommmon = {
  
  startDownloadLinkCapture: function(fhSpecific) {
    this.messageOverlay = document.getElementById("fh-message-overlay");
    this.messageOverlay.innerHTML =
      "<p>Obteniendo el enlace para la carga del album...</p>"+
      "<p>Por favor espere ...</p>";
    this.listenToMessage('FH_DL_FETCH_INIT_LOGGED', function() { 
      setTimeout(fhSpecific.getDownloadLink, 500); //Wait 0.5 so the user can receive some feedback 
    });
    this.sendMessage('FH_DL_FETCH_START');
  },
  
  showCaptcha: function(captchaElement) {
    ContentScriptCommmon.messageOverlay.innerHTML = "";
    ContentScriptCommmon.messageOverlay.appendChild(captchaElement);
  },
  
  retryLinkCapture: function() {
    this.messageOverlay.innerHTML =
      "<p>El link provisto está caído</p>"+
      "<p>Reintentando otro en 3 segundos... espere</p>";
    setTimeout(window.location.reload(), 4000);
  },

  downloadLinkNotFound: function() {
    this.messageOverlay.innerHTML =
      "<p>Lamentablemente, el enlace de carga no es encuentra disponible.</p>"+
      "<p>Cierre la ventana e intente seleccionando otra fuente.</p>"+
      "<p>Sepa disculpar la molestia.</p>";
    ContentScriptCommmon.sendMessage('FH_DL_NOT_AVAILABLE');
  },

  sendDownloadLink: function(downloadLink) {
    ContentScriptCommmon.sendMessage('FH_DL_AVAILABLE', downloadLink);
  },
  
  //Send a message to the opener window
  sendMessage: function(name, content) {
    if(!content) {
      var content = "";
    }
    var message = {
      name: name,
      content: content
    }
    window.opener.postMessage(message, '*');
  },

  listenToMessage: function(name, callback) {
    window.addEventListener("message", function(e) {
      if(e.data.name == name) {
        callback();
      }
    });
  }

}

var DOMHelper = {

  getElementByClass: function(theClass) {
    var allHTMLTags=document.getElementsByTagName("*");
    for (i=0; i<allHTMLTags.length; i++) {
      if (allHTMLTags[i].className==theClass) {
        return allHTMLTags[i];
      }
    }
    return false;
  },

}

