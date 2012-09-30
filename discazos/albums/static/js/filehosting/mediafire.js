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
        var form_inside = DOMHelper.getElementByClass("inside");
        //Removes the upper file name text
        form_inside.removeChild(DOMHelper.getElementByClass("download_file_title"));
        //Removes upper text before the captcha box
        form_inside.removeChild(form_inside.children[0]);
        //Removes the bottom mediafire controls"
        form_inside.removeChild(DOMHelper.getElementByClass("dl-controls cf"));
        var captcha_box = DOMHelper.getElementByClass("captcha_box");
        //Removes bottom "why this captcha" text
        captcha_box.removeChild(captcha_box.children[3]);
        var authorize_dl_btn = document.getElementById("authorize_dl_btn");
        /*
         * THIS NEEDS TESTING, IT MAY WORK
         */
        /*
        //Save the authorize button onclick event before removing the button
        var authorize_dl_btn_onclick = document.getElementById("authorize_dl_btn").onclick;
        //Remove the authorize button box
        form_captcha.removeChild(DOMHelper.getElementByClass("inset-box"));
        //Creates a link with the authorize button action
        var submit_captcha_link = document.createElement("a");
        submit_captcha_link.setAttribute("href", "javascript:void(0);");
        submit_captcha_link.onclick = authorize_dl_btn_onclick;
        submit_captcha_link.innerHTML = "Aceptar";
        //Apend the link to the captcha form
        form_captcha.appendChild(submit_captcha_link);
        */
        authorize_dl_btn.innerHTML = "Aceptar";
        //Show the captcha
        ContentScriptCommmon.showCaptcha(form_captcha);
      } else {
        ContentScriptCommmon.downloadLinkNotFound();
      }
    }
    
  },

}
 
ContentScriptCommmon.startDownloadLinkCapture(MediafireContentScript);