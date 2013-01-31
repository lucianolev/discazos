var ContentScriptCommmon = {
  
  startDownloadLinkCapture: function(fhSpecific) {
    this.listenToMessage('FH_DL_FETCH_INIT_LOGGED', function() {
      $(function() { setTimeout(fhSpecific.getDownloadLink, 500); }); //Wait 0.5 so the user can receive some feedback 
    });
    this.sendMessage('FH_DL_FETCH_START');
    
    this.fhSpecific = fhSpecific;
    this.messageOverlay = $("#fh-message-overlay");
    this.messageOverlay.css();
    this.messageOverlay.html(
      "<p>Obteniendo el enlace para la carga del album...</p>"+
      "<p>Por favor espere ...</p>"
    );
  },
  
  startCountdown: function(countdownElement, unobserved) {
    this.sendMessage('FH_LOG_FETCHING_STATUS', 'COUNTDOWN_INIT');
    
    // Starts the message with the initial value
    var overlayCounter = $("<p style='font-size:25px;'>"+countdownElement.html()+"</p>");
    this.messageOverlay.html("<p>La descarga comenzará en...</p>");
    this.messageOverlay.append(overlayCounter);

    var onCounterEnd = function() {
      $(ContentScriptCommmon.messageOverlay).html(
        "<p>Obteniendo el enlace...</p>"
      );
      ContentScriptCommmon.fhSpecific.afterCountdown();
      ContentScriptCommmon.sendMessage('FH_LOG_FETCHING_STATUS', 'COUNTDOWN_END');
    }

    if(unobserved) {
        countdown = new Countdown({
          seconds: parseInt(countdownElement.html()),
          onUpdateStatus: function(seconds) {
            overlayCounter.html(seconds);
          },
          onCounterEnd: onCounterEnd,
        });
        countdown.start();
    } else {
      // Create an observer to watch for countdown value update and update 
      // the overlay counter until the countdown finishes
      MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
      var countdownObserver = new MutationObserver(function(mutations, observer) {
        console.log(countdownElement);
        // Some sites (eg. Bayfiles) reset the counter before 0, so check for != 1
        if(parseInt(countdownElement.html()) != 1) {
          overlayCounter.html(countdownElement.html());
        } else {
          overlayCounter.html(countdownElement.html()); //Show the '1'
          observer.disconnect(); //Disconnects the observer for preventing counter reset
          // Wait the remaining second and call the afterCountdown on the file hosting
          setTimeout(onCounterEnd, 1000);
        }
      });
      countdownObserver.observe(countdownElement.get(0), { childList: true, subtree: false, attributes: false });
    }
  },

  alreadyDownloading: function() {
    this.sendMessage('FH_LOG_FETCHING_STATUS', 'ALREADY_DOWNLOADING');
    
    this.messageOverlay.html(
      "<p>Se encuentra descargando actualmente otro archivo desde esta fuente.</p>"+
      "<p>Si está cargando otro álbum en el sitio, espere a que finalice la carga e intente nuevamente o bien interrumpa dicha carga cerrando la ventana.</p>"+
      "<p>Por último, puede probar eligiendo otra fuente de descarga (si la hubiese).</p>"+
      "<p>Sepa disculpar la molestia.</p>"
    );
  },

  waitInEffect: function(minutes) {
    this.sendMessage('FH_LOG_FETCHING_STATUS', 'WAITING_IN_EFFECT');
    
    this.messageOverlay.html(
      "<p>Realizó una descarga desde esta fuente hace poco.</p>"+
      "<p>Debe esperar "+minutes+" minutos antes de poder efectuar otra descarga.</p>"+
      "<p>Sepa disculpar la molestia.</p>"
    );
  },
  
  showCaptcha: function(captchaElement) {
    this.sendMessage('FH_LOG_FETCHING_STATUS', 'CAPTCHA');
    
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
    this.sendMessage('FH_LOG_FETCHING_STATUS', 'DL_NOT_AVAILABLE');
    
    this.messageOverlay.html(
      "<p>Lamentablemente, el enlace de carga no es encuentra disponible.</p>"+
      "<p>Cierre la ventana e intente seleccionando otra fuente.</p>"+
      "<p>Sepa disculpar la molestia.</p>"
    );
  },

  sendDownloadLink: function(downloadLink) {
    this.sendMessage('FH_DL_AVAILABLE', downloadLink);
  },
  
  unhandledError: function() {
    this.sendMessage('FH_LOG_FETCHING_STATUS', 'UNHANDLED_ERROR');
    
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
