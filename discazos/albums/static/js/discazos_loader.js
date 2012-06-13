//Object in charge of doing the Discazo loading process
var DiscazosLoader = {
  
  getFHs: function(sourcesListUrl) {
    var showBox = function(url) {
      $.get(url, function(response) {
        $.colorbox({ html: response });
      });
    };
    
    if(ExtensionHandler.extensionLoaded) {
      showBox(sourcesListUrl);
    } else {
      showBox(ExtensionHandler.installationUrl);
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
    $("#download-sources-wrapper").hide();
    $("#fh-info-msg").html(
      "<p>Please wait while the source loads...</p>"+
      "<p>A popup will open and close after a few seconds automatically, just wait.</p>"
    );
    $.colorbox.resize();
  },
 
  downloadLinkReady: function(url) {
    $.colorbox.close();
    
    //Start loading the discazo
    console.log("Sending url to the Discazos player...");
    console.log("URL:" + url);
    
    DiscazosPlayer.load(url);
  },
  
}

//Communication between the extension and the site
var ExtensionHandler = {
  
  init: function(theInstallUrl) {
    this.extensionLoaded = false;
    this.extensionVersion = "unknown";
    this.installationUrl = theInstallUrl;
    this.listenToExtensionLoading();
  },
  
  listenToExtensionLoading: function() {
    extensionHandler = this;
    window.addEventListener("ExtensionLoading", function(e) {
      extensionHandler.extensionLoaded = true;
      extensionHandler.extensionVersion = e.detail.version;
      console.log("Extension loaded! Version "+extensionHandler.extensionVersion);
      extensionHandler.sendSiteUrlToExtension();
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
    FHContentScriptBridge.listenToDownloadLinkInfoFromFH(this.downloadLinkInfoAvailable);
    //FIX: Should get the link from an AJAX request
    sourceUrl += '/ref=discazos';
    FHCommon.openFHPopup(sourceUrl);
  },
  
  //When the download information is available, this fires up
  downloadLinkInfoAvailable: function(downloadLinkInfo) {
    console.log("Got download link information! Please wait... ");
    
    FHCommon.closeFHPopup();
    
    //Start countdown
    if(downloadLinkInfo.countdown > 0) {
      FHCommon.waitForCountdown(downloadLinkInfo, DiscazosLoader.downloadLinkReady)
    } else {
      DiscazosLoader.downloadLinkReady(downloadLinkInfo.url);
    }
  },

}

//FH generic actions to get the download link
var FHCommon = {

  openFHPopup: function(sourceUrl) {
    w = 400;
    h = 200;
    
    wLeft = window.screenLeft ? window.screenLeft : window.screenX;
    wTop = window.screenTop ? window.screenTop : window.screenY;
  
    var left = wLeft + (window.innerWidth / 2) - (w / 2);
    var top = wTop - (h / 2);
    
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
  
}

//Generic comunication with the FH content script
var FHContentScriptBridge = {

  //Listener to the event that gets sent by the FH-specific script
  //when the download information is available (link and counter)  
  listenToDownloadLinkInfoFromFH: function(infoAvailableCallback) {
    window.addEventListener("message", function(e) {
      if(e.data.name == 'FH_DL_INFO_AVAILABLE') {
        infoAvailableCallback(e.data.content);
      }
    });
  },

}
