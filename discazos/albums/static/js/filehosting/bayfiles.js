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
      ContentScriptCommmon.sendDownloadLink(downloadLink);
    } else {
      ContentScriptCommmon.downloadLinkNotFound();
    }
  },

}
 
ContentScriptCommmon.startDownloadLinkCapture(BayFilesContentScript);