if (document.getElementById('captchaform')) {
	var capForm = document.getElementById('captchaform');
	var captchacode = capForm.elements[0].value;
	var megavar = capForm.elements[1].value;
	var captchaimage = capForm.parentNode.getElementsByTagName('img')[0].src;
	var capHTML = '<div align="center">Por favor, ingresa el código debajo para ver el video:</div><div style="background: url(http://www.cuevana.tv/img/captcha_bg.gif) repeat-x;text-align:center;width:200px;margin:15px 220px;padding:10px;-webkit-border-radius:3px;-moz-border-radius:3px"><form method="POST" id="captchaform" style="padding:0;margin:0"><input type="hidden" name="captchacode" value="'+captchacode+
	'"><input type="hidden" name="megavar" value="'+megavar+
	'"><div><img src="'+captchaimage+
	'" border="0" style="background-color:white"></div><div style="margin-top:10px"><input type="text" name="captcha" id="captchafield" maxlength="4" style="text-transform:capitalize; text-transform:uppercase; font-size:20px; border:solid 1px; background-color:#FFFFFF; text-align:center; width:80px; height:30px; border:0; color:#000"></div><div align="center" style="margin-top:20px;"></div><input type="submit" value="Enviar código" style="font-size:11px;font-weight:bold;color:#000000;background:#CCCCC;border:0;border-right:1px solid #999999;border-bottom:1px solid #999999;-webkit-border-radius:3px;-moz-border-radius:3px;padding:3px 7px;" /></form></div></div>';
  alert(capHTML);
} else if (document.getElementById('downloadlink') || getElementByClass('down_ad_butt1')) {
	var d = document.getElementById('downloadlink');
	var downloadlink;
	if (d) {
		downloadlink = d.firstChild.href;
	} else {
		d = getElementByClass('down_ad_butt1');
		downloadlink = d.href;
		hashes += "&premium=true";
	}
	var count = document.getElementById("countdown") ? document.getElementById("countdown").innerHTML : 45;
	
	//Saves the link information
	var downloadLinkInfo = {
		url: downloadlink,
		countdown: count
	};
	//Send a message to the parent frame
	//with the download information
	//(listener is fh_bridge.js)
	var message = {
		name: 'FH_DL_INFO_AVAILABLE',
		content: downloadLinkInfo
	};
	window.parent.postMessage(message, '*');

} else {
	var pag = document.body.innerHTML;
	if (pag.match(/Unfortunately, the link you have clicked is not available/i) || pag.match(/El archivo al que está intentando acceder está temporalmente desactivado/i)) {
		alert("Error!");
	}
}

function getElementByClass(theClass) {
	var allHTMLTags=document.getElementsByTagName("*");
	for (i=0; i<allHTMLTags.length; i++) {
		if (allHTMLTags[i].className==theClass) {
			return allHTMLTags[i];
		}
	}
	return false;
}