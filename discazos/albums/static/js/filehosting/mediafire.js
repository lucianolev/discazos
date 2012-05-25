console.log("Loading script!");
//Get the download link wrapper
var dwrapper = getElementByClass("download_link");

if(dwrapper) {
  //Get the link  
  var downloadlink = dwrapper.childNodes[2].href; //childNodes[1] is the first child
  
  //Saves the link information
  var downloadLinkInfo = {
    url: downloadlink,
    countdown: 0 //Mediafire do not use countdown
  };
  
  //Send a message to the opener window
  //with the download information
  //(listener is fh_bridge.js/initEventHandlers)
  var message = {
    name: 'FH_DL_INFO_AVAILABLE',
    content: downloadLinkInfo
  };

  window.opener.postMessage(message, '*');
}

//Aux function
function getElementByClass(theClass) {
  var allHTMLTags=document.getElementsByTagName("*");
  for (i=0; i<allHTMLTags.length; i++) {
    if (allHTMLTags[i].className==theClass) {
      return allHTMLTags[i];
    }
  }
  return false;
}
