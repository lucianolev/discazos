var ContentScriptCommmon = {
  
  startDownloadLinkCapture: function(fhSpecific) {
    this.fhSpecific = fhSpecific;
    this.messageOverlay = $("#fh-message-overlay");
    this.messageOverlay.html(
      "<p>Obteniendo el enlace para la carga del album...</p>"+
      "<p>Por favor espere ...</p>"
    );
    this.listenToMessage('FH_DL_FETCH_INIT_LOGGED', function() {
      $(function() { setTimeout(fhSpecific.getDownloadLink, 500); }); //Wait 0.5 so the user can receive some feedback 
    });
    this.sendMessage('FH_DL_FETCH_START');
  },
  
  startCountdown: function(countdownElement) {
    // Starts the message with the initial value
    var overlayCounter = $("<p style='font-size:25px;'>"+countdownElement.html()+"</p>");
    this.messageOverlay.html("<p>La descarga comenzará en...</p>");
    this.messageOverlay.append(overlayCounter);

    // Create an observer to watch for countdown value update and update 
    // the overlay counter until the countdown finishes
    MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
    var countdownObserver = new MutationObserver(function(mutations, observer) {
      // Some sites (eg. Bayfiles) reset the counter before 0, so check for != 1
      if(parseInt(countdownElement.html()) != 1) {
        overlayCounter.html(countdownElement.html());
      } else {
        overlayCounter.html(countdownElement.html()); //Show the '1'
        observer.disconnect(); //Disconnects the observer for preventing counter reset
        // Wait the remaining second and call the afterCountdown on the file hosting
        setTimeout(function() {
          $(ContentScriptCommmon.messageOverlay).html(
            "<p>Obteniendo el enlace...</p>"
          );
          ContentScriptCommmon.fhSpecific.afterCountdown();
        }, 1000);
      }
    });
    countdownObserver.observe(countdownElement.get(0), { childList: true, subtree: false, attributes: false });
  },
  
  waitInEffect: function(minutes) {
    this.messageOverlay.html(
      "<p>Realizó una descarga desde esta fuente hace poco.</p>"+
      "<p>Debe esperar "+minutes+" minutos antes de poder efectuar otra descarga.</p>"+
      "<p>Sepa disculpar la molestia.</p>"
    );
  },
  
  showCaptcha: function(captchaElement) {
    ContentScriptCommmon.messageOverlay.empty().append(captchaElement);
  },
  
  retryLinkCapture: function() {
    this.messageOverlay.html(
      "<p>El link provisto está caído</p>"+
      "<p>Reintentando otro en 3 segundos... espere</p>"
    );
    setTimeout(window.location.reload(), 4000);
  },

  downloadLinkNotFound: function() {
    this.messageOverlay.html(
      "<p>Lamentablemente, el enlace de carga no es encuentra disponible.</p>"+
      "<p>Cierre la ventana e intente seleccionando otra fuente.</p>"+
      "<p>Sepa disculpar la molestia.</p>"
    );
    ContentScriptCommmon.sendMessage('FH_DL_NOT_AVAILABLE');
  },

  sendDownloadLink: function(downloadLink) {
    ContentScriptCommmon.sendMessage('FH_DL_AVAILABLE', downloadLink);
  },
  
  unknownError: function() {
    this.messageOverlay.html(
      "<p>Lamentablemente ocurrió un error inesperado al intentar obtener el link de carga.</p>"+
      "<p>Cierre la ventana e intente seleccionando otra fuente o nuevamente más tarde.</p>"+
      "<p>Sepa disculpar la molestia.</p>"
    );
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
