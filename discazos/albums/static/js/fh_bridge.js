FHBridge = {}

$(document).ready(function() {
  FHBridge.initEventHandlers();
  
  /* 
  //Hack to prevent iframe breakout
  var prevent_bust = 0;
  window.onbeforeunload = function() { prevent_bust++ }
  setInterval(function() {
    if (prevent_bust > 0) {
      prevent_bust -= 2;
      window.top.location = 'http://discazos.localhost:8000/dummy_response';
    }
  }, 1);
  */
});

FHBridge.initEventHandlers = function() {
  //Listener to the event sended by the extension 
  //to inform that it's available
  window.addEventListener("extensionLoaded", function() { 
    $("#fh-status").html("Extension loaded!");
  });
  
  //Listener to the event that gets sended by the FH-specific script
  //when the dowload information is available (link and counter)
  window.addEventListener("message", function(e) {
    if(e.data.name == 'FH_DL_INFO_AVAILABLE') {
      FHBridge.dlLinkInfoAvailableHandler(e.data.content);
    }
  });
}

//User ENTRY Point: This gets called when the user selects the source
FHBridge.loadSource = function(url) {
  //FIX: Should get the link from an AJAX request
  url += '/ref=discazos';
  FHBridge.openSourcePopup(url);
  
  $("#fh-status").html("Loading source...");
  //FHBridge.sendDlUrlToIframe(url);
}

FHBridge.openSourcePopup = function(sourceUrl) {
  w = 400;
  h = 200;
  
  wLeft = window.screenLeft ? window.screenLeft : window.screenX;
  wTop = window.screenTop ? window.screenTop : window.screenY;

  var left = wLeft + (window.innerWidth / 2) - (w / 2);
  var top = wTop + (window.innerHeight / 2) - (h / 2);
  
  FHBridge.popupSource = window.open(sourceUrl, "ProcessingSource", 
    'toolbar=no, location=no, menubar=no, scrollbars=no, resizable=no,' + 
    'width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
}

//Sends the download url of the FH service to the iframe
/*FHBridge.sendDlUrlToIframe = function(url) {
  var message = {
    name: 'FH_URL_SEND',
    content: url,
  }
  window.frames[0].postMessage(message, '*');
  
  $("#fh-status").html("Download URL sent to iframe!");
}*/

//When the download information is available, this fires up to 
//process the information gotten from the source
FHBridge.dlLinkInfoAvailableHandler = function(dlLinkInfo) {
  $("#fh-status").html("Got download link information! Please wait... ");
  
  //Close the popup used for processing
  FHBridge.popupSource.close();
  
  //Removes the iframe
  //$("#fh-bridge-frame").remove();
 
  //Start countdown (if the FH use this)
  if(dlLinkInfo.countdown > 0) {
    var fhCountdown = new Countdown({  
      seconds: dlLinkInfo.countdown,  // number of seconds to count down
      onUpdateStatus: function(sec) { $("#fh-countdown").html(sec); }, // callback for each second
      onCounterEnd: function() { FHBridge.dlLinkReadyEvent(dlLinkInfo.url); }, // final action
    });
    //Starts the countdown
    fhCountdown.start();
  } else {
    FHBridge.dlLinkReadyEvent(dlLinkInfo.url);
  }
}

//The final process performed when the download link is finally ready 
//(after countdown)
FHBridge.dlLinkReadyEvent = function(dlLink) {
  $("#fh-status").html("The download link is ready! Loading the Discazo...")
  
  //Start loading the discazo
  console.log("Sending url to the Discazos player...");
  console.log("URL:" + dlLink);
  DiscazosPlayer.load(dlLink);
}
