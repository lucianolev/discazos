//Object in charge of doing the Discazo loading process
var DiscazosLoader = {
  
  getFHs: function(sourcesListUrl) {
    if(ExtensionHandler.extensionLoaded) {
      if(ExtensionHandler.extensionUpToDate) {
        //Show in overlay
        $.get(sourcesListUrl, function(response) {
          $('#player-wrapper div.main').append(response);
          $('.close').click(function() { $('.loading-overlay').remove(); });
        });
      } else {
        //Show in colorbox
        $.get(ExtensionHandler.updateUrl, function(response) {
          $.colorbox({ html: response });
        });
      }
    } else {
      //Show in colorbox
      $.get(ExtensionHandler.installationUrl, function(response) {
        $.colorbox({ html: response });
      });
    }
  },
  
  selectFH: function(dlSourceId, sourceUrl) {
    FHCSConnector.openFHPopup();
    Dajaxice.discazos.albums.add_log_album_playback(function(data) {
      DiscazosLoader.apleId = data.apleId;
      FHCSConnector.loadSource(sourceUrl);
    }, { 'album_release_dl_source_id': dlSourceId });
    console.log("DOWNLOAD_SOURCE_OPENED");
  },
 
  downloadLinkAvailable: function(url) {
    console.log("Sending url to the Discazos player...");
    console.log("URL: " + url);
    //Start loading the discazo
    DiscazosPlayer.load(url, DiscazosLoader.apleId);
  },
  
  linkFetchingStarted: function() {
    Dajaxice.discazos.albums.update_log_album_playback(function() {
      FHCSConnector.sendMessageToCS('FH_DL_FETCH_INIT_LOGGED');
    }, {
      'aple_id': DiscazosLoader.apleId,
      'loading_status':  'DL_FETCH_INIT',
    });
    console.log("DL_FETCH_INIT");
  },
  
  logFetchingStatus: function(status) {
    Dajaxice.discazos.albums.update_log_album_playback(jQuery.noop, { 
      'aple_id': DiscazosLoader.apleId,
      'loading_status': status,
    });
    console.log(status);
  },
  
}

/* Communication between the extension (background and discazos CS) and the site
 * It's initialized when the Discazos album view is loaded.
 * Upon initialization, it starts listening for the extension to notify loading
 * After receiving the notification, the extension is marked as loaded and 
 * it sends current site URL to the extension.
 * After sending the url, it initializes the FHCSConnector
 */
var ExtensionHandler = {
  
  init: function(theInstallUrl, theUpdateUrl, latestVersion) {
    this.latestVersion = latestVersion;
    this.extensionLoaded = false;
    this.extensionUpToDate = null;
    this.installationUrl = theInstallUrl;
    this.updateUrl = theUpdateUrl;
    this.listenToExtensionLoading();
  },
  
  listenToExtensionLoading: function() {
    var extensionHandler = this;
    window.addEventListener("ExtensionLoading", function(e) {
      extensionHandler.extensionLoaded = true;
      if(e.detail.version == extensionHandler.latestVersion) {
        console.log("Extension loaded and up-to-date! Version "+e.detail.version);
        extensionHandler.extensionUpToDate = true;
        extensionHandler.sendSiteUrlToExtension();
        FHCSConnector.init();
      } else {
        extensionHandler.extensionUpToDate = false;
        console.log("Extension is outdated! Version "+extensionHandler.latestVersion+" is needed.");
      }
    });
  },
  
  sendSiteUrlToExtension: function() {
    var e = document.createEvent("CustomEvent");
    var siteUrl = window.location.host; //eg. www.discazos.net
    e.initCustomEvent("SiteUrlSending", true, true, siteUrl);
    window.dispatchEvent(e);
  },
  
  //Callback called by the browser upon extension installation OK
  showRefreshButton: function() {
    $("#extension-install-box #install-message").hide();
    $("#extension-install-box #success-message").show();
    $.colorbox.resize();
  },
  
  //Callback called by the browser upon extension installation failed
  installationFailed: function(message) { 
    console.log(message); 
  }

}

/*
 * Communication between the CS scripts injected by the extension 
 * on the filehosting site and the Discazos website.
 * Handles first origin checking verification and then the 
 * FH link fetching process
 */
var FHCSConnector = {
  
  init: function() {
    this.listenToCSMessages();
  },
  
  listenToCSMessages: function() {
    window.addEventListener("message", function(e) {
      console.log("FH CS message: "+e.data.name);
      switch(e.data.name) {
        case 'FH_CHECK_OPENED_FROM_DISCAZOS':
          FHCSConnector.sendMessageToCS('FH_CHECK_ORIGIN_RESPONSE', 'YES');
          break;
        case 'FH_DL_FETCH_START':
          DiscazosLoader.linkFetchingStarted();
          break;
        case 'FH_DL_AVAILABLE':
          FHCSConnector.closeFHPopup();
          DiscazosLoader.downloadLinkAvailable(e.data.content);
          break;
        case 'FH_LOG_FETCHING_STATUS':
          DiscazosLoader.logFetchingStatus(e.data.content);
          break;
      }
    });
  },
  
  sendMessageToCS: function(aMessage, theContent) {
    if(!theContent) {
      var theContent = "";
    }
    if(FHCSConnector.fhPopup) {
      FHCSConnector.fhPopup.postMessage({ name: aMessage, content: theContent }, '*');
    } else {
      console.log("ERROR: No popup was opened.");
    }
  },

  loadSource: function(sourceUrl) {
    FHCSConnector.fhPopup.location = sourceUrl;
    FHCSConnector.fhPopup.focus();
  },

  openFHPopup: function() {
    var w = 600;
    var h = 250;
    
    var wLeft = window.screenLeft ? window.screenLeft : window.screenX;
    var wTop = window.screenTop ? window.screenTop : window.screenY;
  
    var left = wLeft + (window.innerWidth / 2) - (w / 2);
    var top = wTop - (h / 2) + 450;
    
    FHCSConnector.fhPopup = window.open('', "ProcessingSource", 
      'toolbar=no, location=no, menubar=no, scrollbars=no, resizable=no,' + 
      'width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
  },
  
  closeFHPopup: function() {
    FHCSConnector.fhPopup.close();
  },
  
  /*waitForCountdown: function(downloadLinkInfo, readyCallback) {
    var fhCountdown = new Countdown({  
      seconds: downloadLinkInfo.countdown,  // number of seconds to count down
      onUpdateStatus: function(sec) { $("#fh-countdown").html(sec); }, // callback for each second
      onCounterEnd: function() { readyCallback(downloadLinkInfo.url); }, // final action
    });
    //Starts the countdown
    fhCountdown.start();
  },*/

}
