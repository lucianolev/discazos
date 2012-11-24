require.config({
    paths:{
      'jquery': '//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min',
    }
});

require(["jquery", "common"], function($) {
  
  var BayFilesContentScript = {
  
    getDownloadLink: function() {
      downloadHeader = $("#download-header");
      downloadButton = downloadHeader.find("li.limited .btn");
      messagesBox = $("#content-inner");
      
      if(downloadButton.length) {
        //Click the non-premium download button wrapper
        downloadButton.get(0).click();
        ContentScriptCommmon.startCountdown($("#countDown")); // Can this fail?
      } else if(messagesBox.length && messagesBox.html().match(/has recently downloaded a file/i)) {
        ContentScriptCommmon.waitInEffect(5);
      } else if(downloadHeader.length && downloadHeader.html().match(/the requested file could not be found/i)) {
        ContentScriptCommmon.downloadLinkNotFound();
      } else {
        ContentScriptCommmon.unknownError();
      }
    },
    
    afterCountdown: function() {
      setTimeout(function() {
        var startDownloadButton = $("#content-inner input[value='Start Download']");
        if(startDownloadButton.length) {
          var j = startDownloadButton.attr('onclick');
          var downloadLink = j.substring(j.indexOf("'") + 1, j.length - 2);
          //if(downloadLink.match(/s6\.baycdn\.com/)) { //This server is known to fail (29/09/2012)
          //  ContentScriptCommmon.retryLinkCapture();
          //} else {
          ContentScriptCommmon.sendDownloadLink(downloadLink);
          //}
        } else {
          ContentScriptCommmon.unknownError();
        }
      }, 1000);
    },
  
  }
  
  ContentScriptCommmon.startDownloadLinkCapture(BayFilesContentScript);
});