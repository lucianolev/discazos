var ContentScriptCommmon = {
  
  startDownloadLinkCapture: function(fhSpecific) {
    this.messageOverlay = document.getElementById("fh-message-overlay");
    this.messageOverlay.innerHTML =
      "<p>Obteniendo el enlace para la carga del album...</p>"+
      "<p>Por favor espere ...</p>";
    setTimeout(fhSpecific.getDownloadLink, 1000);
  },
  
  showCaptcha: function(captchaElement) {
    ContentScriptCommmon.messageOverlay.innerHTML = "";
    ContentScriptCommmon.messageOverlay.appendChild(captchaElement);
  },

  downloadLinkNotFound: function() {
    this.messageOverlay.innerHTML =
      "<p>Lamentablemente, el enlace de carga no es encuentra disponible.</p>"+
      "<p>Cierre la ventana e intente seleccionando otra fuente.</p>"+
      "<p>Sepa disculpar la molestia.</p>";
  },

  sendDownloadLink: function(downloadLink) {
    var message = {
      name: 'FH_DL_AVAILABLE',
      content: downloadLink
    }
    //Send a message to the opener window
    window.opener.postMessage(message, '*');
  },

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

