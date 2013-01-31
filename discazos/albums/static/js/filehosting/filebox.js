require.config({
    paths:{
      'jquery': '//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min',
    }
});

require(["jquery", "common", "countdown"], function($) {
  
  var FileboxContentScript = {
  
    getDownloadLink: function() {
      var downloadLink = $("#Midcontainerdf-in").find("a");
      var countdownString = $("#countdown_str");
      
      if(downloadLink.length) {
        var downloadLinkUrl = downloadLink.get(0).href;
        ContentScriptCommmon.sendDownloadLink(downloadLinkUrl);
      } else if(countdownString.length) {
        var countdown = countdownString.children();
        ContentScriptCommmon.startCountdown(countdown, true);
      } else if($("#header").html().match(/(Archive no Encontrado|File Not Found)/i)) {
        ContentScriptCommmon.downloadLinkNotFound();
      } else {
        ContentScriptCommmon.unhandledError();
      }
    },
    
    afterCountdown: function() {
      setTimeout(function() {
        freeDownloadButton = $("#btn_download");
        freeDownloadButton.get(0).click();
      }, 1000);
    },
  
  }
  
  ContentScriptCommmon.startDownloadLinkCapture(FileboxContentScript);
});