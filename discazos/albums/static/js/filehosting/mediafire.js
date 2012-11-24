require.config({
    paths:{
      'jquery': '//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min',
    }
});

/* TODO: Clean up and refactor to use more jQuery methods */

require(["jquery", "common"], function() {
  var MediafireContentScript = {
  
    getDownloadLink: function() {
      //Get the download link wrapper
      var dwrapper = $(".download_link");
      
      if(dwrapper.length) {
        //Get the link  
        var downloadLink = dwrapper.get(0).childNodes[2].href; //childNodes[1] is the first child
      }
  
      if(downloadLink) {
        ContentScriptCommmon.sendDownloadLink(downloadLink);
      } else {
        var form_captcha = $("#form_captcha");
        if(form_captcha.length) {
          var form_inside = $(".inside");
          //Removes the upper file name text
          form_inside.remove(".download_file_title");
          //Removes upper text before the captcha box
          form_inside.get(0).removeChild(form_inside.get(0).children[0]);
          //Removes the bottom mediafire controls"
          form_inside.remove(".dl-controls cf");
          var captcha_box = $(".captcha_box");
          //Removes bottom "why this captcha" text
          captcha_box.get(0).removeChild(captcha_box.get(0).children[3]);
          var authorize_dl_btn = $("#authorize_dl_btn");
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
          authorize_dl_btn.html("Aceptar");
          //Show the captcha
          ContentScriptCommmon.showCaptcha(form_captcha);
        } else {
          ContentScriptCommmon.downloadLinkNotFound();
        }
      }
      
    },
  
  }
   
  ContentScriptCommmon.startDownloadLinkCapture(MediafireContentScript);
});