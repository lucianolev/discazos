/* Must include common.js for usage */

var BayFilesContentScript = {

  getDownloadLink: function() {
    //Get the download link wrapper
    var downloadButton = DOMHelper.getElementByClass("highlighted-btn");
    
    if(downloadButton) {
      //Get the link  
      var downloadLink = downloadButton.href;
    }

    if(downloadLink) {
      if(downloadLink.match(/s6\.baycdn\.com/)) { //This server is known to fail (29/09/2012)
        ContentScriptCommmon.retryLinkCapture();
      } else {
        ContentScriptCommmon.sendDownloadLink(downloadLink);
      }
    } else {
      ContentScriptCommmon.downloadLinkNotFound();
    }
  },

}
 
ContentScriptCommmon.startDownloadLinkCapture(BayFilesContentScript);