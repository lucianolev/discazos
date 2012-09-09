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
  
  selectFH: function(sourceUrl, fhService) {
    switch(fhService) {
      case "MF":
        MediafireFH.sourceSelected(sourceUrl);
        break;
      default:
        console.log("Unsupported download source!");
        return false;
    }
  },
 
  downloadLinkReady: function(url) {
    //Start loading the discazo
    console.log("Sending url to the Discazos player...");
    console.log("URL:" + url);
    
    DiscazosPlayer.load(url);
  },
  
}

/* Communication between the extension and the site
 * It's initialized when the Discazos album view is loaded.
 * Upon initialization, it starts listening for the extension to notify loading
 * After receiving the notification, the extension is marked as loaded and 
 * it sends current site URL to the extension.
 */
var ExtensionHandler = {
  
  init: function(theInstallUrl, theUpdateUrl) {
    this.latestVersion = "0.4.1";
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
        FHCommon.listenToOriginCheck(); //Listen to the origin check script 
                                        //after loading the extension
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

}

//Mediafire-specific actions to get the download link
var MediafireFH = {

  sourceSelected: function(sourceUrl) {
    FHCommon.listenToDownloadLinkInfoFromFHsCS(this);
    //FIX: Should get the link from an AJAX request
    FHCommon.openFH(sourceUrl);
  },
  
  //When the download information is available, this fires up
  downloadLinkInfoAvailable: function(downloadLinkInfo) {
    FHCommon.closeFHPopup();
    DiscazosLoader.downloadLinkReady(downloadLinkInfo.url);
    
    /*
    //Start countdown
    if(downloadLinkInfo.countdown > 0) {
      FHCommon.waitForCountdown(downloadLinkInfo, DiscazosLoader.downloadLinkReady)
    } else {
      DiscazosLoader.downloadLinkReady(downloadLinkInfo.url);
    }
    */
  },

}

//FH generic actions to get the download link
var FHCommon = {

  openFH: function(sourceUrl) {
    this.openPopup(sourceUrl);
  },

  openPopup: function(sourceUrl) {
    w = 600;
    h = 250;
    
    wLeft = window.screenLeft ? window.screenLeft : window.screenX;
    wTop = window.screenTop ? window.screenTop : window.screenY;
  
    var left = wLeft + (window.innerWidth / 2) - (w / 2);
    var top = wTop - (h / 2) + 450;
    
    this.fhPopup = window.open(sourceUrl, "ProcessingSource", 
      'toolbar=no, location=no, menubar=no, scrollbars=no, resizable=no,' + 
      'width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
  },
  
  closeFHPopup: function() {
    this.fhPopup.close();
  },
  
  waitForCountdown: function(downloadLinkInfo, readyCallback) {
    var fhCountdown = new Countdown({  
      seconds: downloadLinkInfo.countdown,  // number of seconds to count down
      onUpdateStatus: function(sec) { $("#fh-countdown").html(sec); }, // callback for each second
      onCounterEnd: function() { readyCallback(downloadLinkInfo.url); }, // final action
    });
    //Starts the countdown
    fhCountdown.start();
  },

  listenToOriginCheck: function() {
    window.addEventListener("message", function(e) {
      if(e.data.message == 'FromDiscazos?') {
        FHCommon.fhPopup.postMessage({ response: 'YES' }, '*');
      }
    });
  },
  
  //Listener to the event that gets sent by the FH-specific content script
  //when the download information is available (link and counter)  
  listenToDownloadLinkInfoFromFHsCS: function(FH) {
    window.addEventListener("message", function(e) {
      //console.log("FH CS Message: "+e.data.name);
      switch(e.data.name) {
        case 'FH_DL_INFO_AVAILABLE':
          FH.downloadLinkInfoAvailable(e.data.content);
          break;
      }
    });
  },

}
