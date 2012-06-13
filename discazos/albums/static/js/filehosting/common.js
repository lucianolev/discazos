//Aux functions
function getElementByClass(theClass) {
  var allHTMLTags=document.getElementsByTagName("*");
  for (i=0; i<allHTMLTags.length; i++) {
    if (allHTMLTags[i].className==theClass) {
      return allHTMLTags[i];
    }
  }
  return false;
}