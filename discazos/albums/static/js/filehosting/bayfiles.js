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
      var noStartButtonTimeout = setTimeout(ContentScriptCommmon.unhandledError, 20000); //Fire unhandled error if there's no start button in 20 secs
      var startDownloadButtonArea = $("#content-inner");
      // Create an observer to watch for the start download button to load inside #content-inner
      MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
      var startDownloadButtonAreaObserver = new MutationObserver(function(mutations, observer) {
        var startDownloadButton = startDownloadButtonArea.find("input[value='Start Download']");
        if(startDownloadButton.length) {
          clearTimeout(noStartButtonTimeout);
          observer.disconnect();
          var j = startDownloadButton.attr('onclick');
          var downloadLink = j.substring(j.indexOf("'") + 1, j.length - 2);
          //if(downloadLink.match(/s6\.baycdn\.com/)) { //This server is known to fail (29/09/2012) rev. 27/11/2012
          //  ContentScriptCommmon.retryLinkCapture();
          //} else {
          ContentScriptCommmon.sendDownloadLink(downloadLink);
        }
      });
      startDownloadButtonAreaObserver.observe(startDownloadButtonArea.get(0), { childList: true, subtree: false, attributes: false });
    },
  
  }
  
  ContentScriptCommmon.startDownloadLinkCapture(BayFilesContentScript);
});