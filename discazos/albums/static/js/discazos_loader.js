//Object in charge of doing the Discazo loading process
var DiscazosLoader = {
  
  getFHs: function(sourcesListUrl) {
    if(ExtensionHandler.extensionLoaded) {
      if(ExtensionHandler.extensionUpToDate) {
        //Show in overlay
        $.get(sourcesListUrl, function(response) {
          $('#player-wrapper div.main').append(response);
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
  
  selectFH: function(sourceUrl) {
    FHCSConnector.sourceSelected(sourceUrl);
  },
 
  downloadLinkReady: function(url) {
    //Start loading the discazo
    console.log("Sending url to the Discazos player...");
    console.log("URL:" + url);
    
    DiscazosPlayer.load(url);
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
    extensionHandler = this;
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
  
  showRefreshButton: function() {
    $("#extension-install-box #install-message").hide();
    $("#extension-install-box #success-message").show();
    $.colorbox.resize();
  },
  
  installationFailed: function(message) { 
    console.log(message); 
  }

}

//FH CS extension connection
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
        case 'FH_DL_AVAILABLE':
          FHCSConnector.downloadLinkAvailable(e.data.content);
          break;
      }
    });
  },
  
  sendMessageToCS: function(aMessage, theContent) {
    if(FHCSConnector.fhPopup) {
      FHCSConnector.fhPopup.postMessage({ name: aMessage, content: theContent }, '*');
    } else {
      console.log("ERROR: No popup was opened.");
    }
  },

  sourceSelected: function(sourceUrl) {
    FHCSConnector.openPopup(sourceUrl);
  },

  openPopup: function(sourceUrl) {
    w = 600;
    h = 250;
    
    wLeft = window.screenLeft ? window.screenLeft : window.screenX;
    wTop = window.screenTop ? window.screenTop : window.screenY;
  
    var left = wLeft + (window.innerWidth / 2) - (w / 2);
    var top = wTop - (h / 2) + 450;
    
    FHCSConnector.fhPopup = window.open(sourceUrl, "ProcessingSource", 
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

  //When the download information is available, this fires up
  downloadLinkAvailable: function(downloadLinkUrl) {
    FHCSConnector.closeFHPopup();
    DiscazosLoader.downloadLinkReady(downloadLinkUrl);
  },

}
