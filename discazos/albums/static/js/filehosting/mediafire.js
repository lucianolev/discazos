/* Must include common.js for usage */

var MediafireContentScript = {

  getDownloadLinkInfo: function() {
    //Get the download link wrapper
    var dwrapper = getElementByClass("download_link");
    
    if(dwrapper) {
      //Get the link  
      var downloadlink = dwrapper.childNodes[2].href; //childNodes[1] is the first child
      
      //Saves the link information
      this.downloadLinkInfo = {
        url: downloadlink,
        countdown: 0 //Mediafire do not use countdown
      }
    }
    
    this.sendDownloadLinkInfo();
  },
  
  sendDownloadLinkInfo: function() {
    //Send a message to the opener window
    //with the download information
    //(listener is fh_bridge.js/initEventHandlers)
    var message = {
      name: 'FH_DL_INFO_AVAILABLE',
      content: this.downloadLinkInfo
    };

    window.opener.postMessage(message, '*');
  },

}

MediafireContentScript.getDownloadLinkInfo();