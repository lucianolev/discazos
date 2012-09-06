/* Must include common.js for usage */

var MediafireContentScript = {

  getDownloadLinkInfo: function() {
    //Get the download link wrapper
    var dwrapper = DOMHelper.getElementByClass("download_link");
    
    if(dwrapper) {
      //Get the link  
      var downloadlink = dwrapper.childNodes[2].href; //childNodes[1] is the first child
      
      if(downloadlink) {
        //Saves the link information
        var downloadLinkInfo = {
          url: downloadlink,
          countdown: 0 //Mediafire do not use countdown
        }
      }
    }

    if(downloadLinkInfo) {
      ContentScriptCommmon.sendDownloadLinkInfo(downloadLinkInfo);
    } else {
      var form_captcha = document.getElementById("form_captcha");
      if(form_captcha) {
        ContentScriptCommmon.messageOverlay.innerHTML = "";
        ContentScriptCommmon.messageOverlay.appendChild(form_captcha);
      } else {
        ContentScriptCommmon.downloadLinkNotFound();
      }
    }
    
  },

}
 
ContentScriptCommmon.startDownloadLinkCapture(MediafireContentScript);