//Listen to the content script for set/get discazos url
chrome.extension.onRequest.addListener(function(request, sender, sendResponse) {
    switch (request.action) {
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