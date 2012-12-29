require.config({
    paths:{
      'jquery': '//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min',
    }
});

require(["jquery", "common"], function($) {
  
  var BayFilesContentScript = {
  
    getDownloadLink: function() {
      downloadNotFoundHeader = $("#download-header.not-found");
      downloadInfoBox = $("#content-inner");
      downloadButton = downloadInfoBox.find(".limited .btn");
      
      if(downloadButton.length) {
        downloadButton.get(0).click(); //Click the non-premium download button wrapper
        ContentScriptCommmon.startCountdown($("#countDown"));
      } else if(downloadInfoBox.length && downloadInfoBox.html().match(/already downloading/i)) {
        ContentScriptCommmon.alreadyDownloading();
      } else if(downloadInfoBox.length && downloadInfoBox.html().match(/has recently downloaded a file/i)) {
        ContentScriptCommmon.waitInEffect(5);
      } else if(downloadNotFoundHeader.length && downloadNotFoundHeader.html().match(/the requested file could not be found/i)) {
        ContentScriptCommmon.downloadLinkNotFound();
      } else {
        ContentScriptCommmon.unhandledError();
      }
    },
    
    afterCountdown: function() {
      setTimeout(function() {
        var startDownloadButton = $("#content-inner input[value='Start Download']");
        if(startDownloadButton.length) {
          var j = startDownloadButton.attr('onclick');
          var downloadLink = j.substring(j.indexOf("'") + 1, j.length - 2);
          //if(downloadLink.match(/s6\.baycdn\.com/)) { //This server is known to fail (29/09/2012) rev. 27/11/2012
          //  ContentScriptCommmon.retryLinkCapture();
          //} else {
          ContentScriptCommmon.sendDownloadLink(downloadLink);
          //}
        } else {
          ContentScriptCommmon.unhandledError();
        }
      }, 1000);
    },
  
  }
  
  ContentScriptCommmon.startDownloadLinkCapture(BayFilesContentScript);
});