/* Must include common.js for usage */

var MediafireContentScript = {

  getDownloadLink: function() {
    //Get the download link wrapper
    var dwrapper = DOMHelper.getElementByClass("download_link");
    
    if(dwrapper) {
      //Get the link  
      var downloadLink = dwrapper.childNodes[2].href; //childNodes[1] is the first child
    }

    if(downloadLink) {
      ContentScriptCommmon.sendDownloadLink(downloadLink);
    } else {
      var form_captcha = document.getElementById("form_captcha");
      if(form_captcha) {
        ContentScriptCommmon.showCaptcha(form_captcha);
      } else {
        ContentScriptCommmon.downloadLinkNotFound();
      }
    }
    
  },

}
 
ContentScriptCommmon.startDownloadLinkCapture(MediafireContentScript);