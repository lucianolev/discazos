//Listen to the content script
chrome.extension.onRequest.addListener(function(request, sender, sendResponse) {
    switch (request.action) {
      case "getExtensionVersion":
        details = chrome.app.getDetails();
        sendResponse({version: details.version});
        break;
      case "saveDiscazosUrl":
        localStorage['discazos_url'] = request.url;
        sendResponse({});
        break;
      case "getDiscazosUrl":
        console.log("Getting website URL: " + localStorage['discazos_url']);
        sendResponse({url: localStorage['discazos_url']});
        break;
      default:
        sendResponse({});
    }
});