var DiscazosPlayer = {};
var DiscazosPlayerUI = {}

DiscazosPlayer.MIN_FILE_OK_BYTES = 51200; //50KB
DiscazosPlayer.MIN_BYTES_TO_LOAD = 491520; //30 seconds of 128kbps audio
DiscazosPlayer.GET_TIMEOUT = 15000; //15 secs before timing out for GET request

$(document).ready(function() {
  DiscazosPlayer.swf = swfobject.getObjectById("discazos-player-swf");
  DiscazosPlayerUI.html = $("#discazos-player-html");
  
  DiscazosPlayer.data = { 
    audioFileSize: DiscazosPlayerUI.html.find("#album-audiofile-size").html(),
    currentTrack: false,
    minFileOKLoaded: false,
    minLoadedTriggered: false,
    bufferLoadingStarted: false,
    apleId: null,
    bytesLoaded: 0,
  };
  
  /** Initialize UI **/
 DiscazosPlayerUI.init();

});

/* Player UI */

DiscazosPlayerUI.init = function() {
  //Setup player control buttons
  this.html.find("#play-button").button({
    text: false,
    icons: {
      primary: "ui-icon-play"
    }
  }).click(function() {
    if($(this).text() === "Play") {
      DiscazosPlayer.pressPlay();
    } else {
      DiscazosPlayer.pressPause();
    }
  });
  this.html.find("#prev-button").button({
    text: false,
    icons: {
      primary: "ui-icon-seek-start"
    },
    disabled: true,
  }).click(function() { 
    DiscazosPlayer.playPrevious(); 
  });
  this.html.find("#next-button").button({
    text: false,
    icons: {
      primary: "ui-icon-seek-end"
    },
    disabled: true,
  }).click(function() { 
    DiscazosPlayer.playNext(); 
  });
  
  //Setup playlist scrolling
  this.html.find("#player-wrapper div.main div.left").alternateScroll();
  
  //Setup loading progressbar
  this.html.find("#album-loading-progressbar").progressbar();
  
  //Setup track seek/progress bar
  this.html.find("#progressbar").slider({
    range: 'min',
    change: function(event, ui) {
      if(event.originalEvent && event.originalEvent.type == "mouseup") {
        var seekPercentage = ui.value;
        console.log("Seek: "+seekPercentage);
        DiscazosPlayer.seekTrack(seekPercentage);
      }
    },
    start: function(event, ui) {
      $(this).data('is_being_slided', true);
    },
    stop: function(event, ui) {
      $(this).data('is_being_slided', false);
    }
  }).data('is_being_slided', false);
 
  //Bind Discazos Player events to UI
  this.html.bind("bufferInitLoadingError", DiscazosPlayerUI.showMessageOnLoadingFail);
  this.html.bind("bufferLoadingStarted", DiscazosPlayerUI.showPreloadingStatus);
  this.html.bind("minLoaded", DiscazosPlayerUI.activatePlayerControls);
}

DiscazosPlayerUI.setButtonPlay = function() {
  var options = {
    label: "Play",
    icons: {
      primary: "ui-icon-play"
    }
  };
  this.html.find("#play-button").button("option", options);
}

DiscazosPlayerUI.setButtonPause = function() {
  var options = {
    label: "Pause",
    icons: {
      primary: "ui-icon-pause"
    }
  }
  this.html.find("#play-button").button("option", options);
}

DiscazosPlayerUI.disablePrevButton = function() {
  this.html.find("#prev-button").button("disable");
}

DiscazosPlayerUI.disableNextButton = function() {
  this.html.find("#next-button").button("disable");
}

DiscazosPlayerUI.enablePrevButton = function() {
  this.html.find("#prev-button").button("enable");
}

DiscazosPlayerUI.enableNextButton = function() {
  this.html.find("#next-button").button("enable");
}

DiscazosPlayerUI.showPreloadInitMessage = function() {
  var albumCover = this.html.find("a.load-link");
  albumCover.find("span.load-button").remove();
  albumCover.find("#album-cover").unwrap(); //Removes the loading link
  
  var loadingOverlay = DiscazosPlayerUI.html.find("#player-wrapper div.main div.loading-overlay");
  loadingOverlay.find("#download-sources-frame #download-sources-wrapper").hide();
  loadingOverlay.find("#download-sources-frame #link-available-box").show();
}

DiscazosPlayerUI.showMessageOnLoadingFail = function() {
  var loadingOverlay = DiscazosPlayerUI.html.find("#player-wrapper div.main div.loading-overlay");
  loadingOverlay.find("#download-sources-frame .preload-init").show();
  loadingOverlay.find("#download-sources-frame .preloading").hide();
  loadingOverlay.find("#download-sources-frame #link-available-box").hide();
  loadingOverlay.find("#download-sources-frame #buffer-error-text").show();
  loadingOverlay.find("#download-sources-frame #download-sources-wrapper").show();
}

DiscazosPlayerUI.showPreloadingStatus = function() {
  var loadingOverlay = DiscazosPlayerUI.html.find("#player-wrapper div.main div.loading-overlay");
  loadingOverlay.find("#download-sources-frame .preload-init").hide();
  loadingOverlay.find("#download-sources-frame .preloading").show();
}

DiscazosPlayerUI.activatePlayerControls = function() {
  var loadingOverlay = DiscazosPlayerUI.html.find("#player-wrapper div.main div.loading-overlay");
  loadingOverlay.remove();
  DiscazosPlayerUI.html.find('#album-loading-progressbar span.caption').show();
  DiscazosPlayerUI.html.find("#player-controls").slideDown('slow');
  DiscazosPlayerUI.html.find(".playlist tr.track").each(function() {
    $(this).hover(function() { $(this).addClass("hover") }, 
                  function() { $(this).removeClass("hover") });
    $(this).click(function() { DiscazosPlayer.playTrack(this); });
  });
}

/***** JS Player ******/

/* Actions */

DiscazosPlayer.load = function(url, apleId) {
  this.data.apleId = apleId; //For logging
  
  this.swf.load(url);
  DiscazosPlayerUI.showPreloadInitMessage();
  
  //If the SWF player does not trigger buffer start or error event after 
  //a certain threshold, log the error and trigger a bufferInitLoadingError
  this.loadTimeout = setTimeout(function() {
    DiscazosPlayer.updatePlaybackLog('DL_LOAD_TIMEOUT');
    DiscazosPlayerUI.html.trigger("bufferInitLoadingError");
  }, DiscazosPlayer.GET_TIMEOUT);
}

DiscazosPlayer.pressPlay = function() {
  //Play first tracks if there's no current, 
  //else continue playing the current
  if(!this.data.currentTrack) {
    this.playTrack(DiscazosPlayerUI.html.find('.playlist tr.track:first'))
  } else {
    DiscazosPlayerUI.setButtonPause();
    this.swf.play();
  }
}

DiscazosPlayer.pressPause = function() {
  this.swf.pause();
  DiscazosPlayerUI.setButtonPlay();
}

DiscazosPlayer.playTrack = function(trackItem) {
  //Update track information
  this.currentTrackChanged(trackItem);
  
  //Start playing the track
  var newMsPosition = this.data.currentTrack.offset;
  if(newMsPosition == 0) newMsPosition = 1; //If it's the starting position, seek to 1
  this.swf.seek(newMsPosition);
  
  DiscazosPlayerUI.setButtonPause();
}

DiscazosPlayer.seekTrack = function(seekPercentage) {
  var trackStart = this.data.currentTrack.offset;
  var seekOffset = Math.round(this.data.currentTrack.length * seekPercentage / 100);
  var newMsPosition = trackStart + seekOffset;
  this.swf.seek(newMsPosition);
  DiscazosPlayerUI.setButtonPause();
}

DiscazosPlayer.playNext = function() {
  this.playTrack($(this.data.currentTrack.item).next());
}

DiscazosPlayer.playPrevious = function() {
  this.playTrack($(this.data.currentTrack.item).prev());
}

DiscazosPlayer.currentTrackIsLast = function() {
  return $(this.data.currentTrack.item).next().length == 0;
}

DiscazosPlayer.currentTrackNumber = function() {
  return this.data.currentTrack.item.find('.track-number').html();
}

DiscazosPlayer.currentTrackChanged = function(trackItem) {
  this.data.currentTrack = { 
    item: $(trackItem),
    offset: parseInt($(trackItem).find('.track-number').attr('rel')),
    length: parseInt($(trackItem).find('.track-length').attr('rel')),
  }
  //Set progress bar to 0
  DiscazosPlayerUI.html.find('#progressbar').progressbar("value", 0);
  //Update track name
  DiscazosPlayerUI.html.find('#current-track').html($(trackItem).find('.track-name').html());
  
  if(this.currentTrackNumber() == 1) {
    DiscazosPlayerUI.disablePrevButton();
    DiscazosPlayerUI.enableNextButton();
  } else if(this.currentTrackIsLast()) {
    DiscazosPlayerUI.disableNextButton();
    DiscazosPlayerUI.enablePrevButton();
  } else {
    DiscazosPlayerUI.enablePrevButton();
    DiscazosPlayerUI.enableNextButton();
  }
}

DiscazosPlayer.updateTrackProgress = function(currentProgress) {
  this.updateTrackTimeElapsed(currentProgress);
  this.updateTrackProgressbar(currentProgress);
}

DiscazosPlayer.updateTrackProgressbar = function(currentProgress) {
  var progressbar = DiscazosPlayerUI.html.find('#progressbar');
  if(!progressbar.data('is_being_slided')) { //This is to prevent the slider to 
                                            //move while being slided for seeking
    var percentage = Math.round((currentProgress / this.data.currentTrack.length) * 100);
    progressbar.slider("value", percentage);
  }
}

DiscazosPlayer.updateTrackTimeElapsed = function(currentProgress) {
  DiscazosPlayerUI.html.find('#time-elapsed').html(this.convertToMMSS(currentProgress));
}

DiscazosPlayer.stop = function() {
  this.swf.pause();
  DiscazosPlayerUI.disableNextButton();
  DiscazosPlayerUI.disablePrevButton();
  this.updateTrackTimeElapsed(0);
  this.updateTrackProgressbar(0);
  DiscazosPlayerUI.html.find('#current-track').html("");
  this.data.currentTrack = false;
  DiscazosPlayerUI.setButtonPlay();
}

/* Aux */

DiscazosPlayer.convertToMMSS = function(milliseconds) {
  var seconds = Math.round(milliseconds / 1000);
  var minute = Math.floor(seconds / 60);
  var second = seconds % 60;
  var minuteMM = (minute<10) ? "0"+minute : minute
  var secondSS = (second<10) ? "0"+second : second
  var MMSS = minuteMM + ":" + secondSS;
  return MMSS;
}

DiscazosPlayer.updatePlaybackLog = function(loadingStatus, extraDebugInfo) {
  var log = {
    aple_id: this.data.apleId,
    loading_status: loadingStatus,
  };
  if(extraDebugInfo) {
    log.extra_debug_info = extraDebugInfo;
  }
  Dajaxice.discazos.albums.update_log_album_playback(jQuery.noop, log);
  console.log(loadingStatus);
}

/* Flash player events */

DiscazosPlayer.bufferLoadingStarted = function() {
  clearTimeout(this.loadTimeout);
  this.data.bufferLoadingStarted = true;
  DiscazosPlayerUI.html.trigger("bufferLoadingStarted");
}

DiscazosPlayer.bufferError = function(errorText) {
  clearTimeout(this.loadTimeout);
  if(!this.data.bufferLoadingStarted || this.data.bytesLoaded == 0) {
    DiscazosPlayer.updatePlaybackLog('DL_GET_FAIL', 'SWF Debug Error: '+errorText);
    DiscazosPlayerUI.html.trigger("bufferInitLoadingError");
  } else {
    DiscazosPlayer.updatePlaybackLog('LOADING_INTERRUPTED', 
      'SWF Debug Error: '+errorText+'. Bytes loaded: '+this.data.bytesLoaded);
    //TODO: UI alert
  }
}

DiscazosPlayer.updateBufferProgress = 
  function(bytesLoaded, bytesTotal) { //bytesTotal is not reliable until loading finishes
    this.data.bytesLoaded = bytesLoaded;
    if(this.data.bytesLoaded >= DiscazosPlayer.MIN_FILE_OK_BYTES && !this.data.minFileOKLoaded) {
      this.data.minFileOKLoaded = true;
      DiscazosPlayer.updatePlaybackLog('LOADING_INIT');
    } else if(this.data.bytesLoaded >= DiscazosPlayer.MIN_BYTES_TO_LOAD) {
      if(!this.data.minLoadedTriggered) {
         this.data.minLoadedTriggered = true;
         DiscazosPlayerUI.html.trigger("minLoaded");
      }
      var percentage = (bytesLoaded / this.data.audioFileSize) * 100;
      var progressbarWidget = DiscazosPlayerUI.html.find('#album-loading-progressbar');
      progressbarWidget.children('span.caption').html(percentage.toFixed(1) + ' %');
      progressbarWidget.progressbar("value", percentage);
    } else {
      var preloadPercentage = Math.round((bytesLoaded / DiscazosPlayer.MIN_BYTES_TO_LOAD) * 100);
      DiscazosPlayerUI.html.find('#preload-percentage').html(preloadPercentage);
    }
  }

DiscazosPlayer.bufferLoadingFinish = function() {
  if(this.data.bytesLoaded == this.data.audioFileSize) {
    DiscazosPlayer.updatePlaybackLog('LOADING_FINISHED_OK');
  } else if(this.data.bytesLoaded < DiscazosPlayer.MIN_FILE_OK_BYTES) {
    DiscazosPlayer.updatePlaybackLog('DL_BAD_FILE', 'Bytes loaded: '+this.data.bytesLoaded);
    DiscazosPlayerUI.html.trigger("bufferInitLoadingError");
  } else {
    DiscazosPlayer.updatePlaybackLog('LOADING_SIZE_MISMATCH', 'Bytes loaded: '+this.data.bytesLoaded);
    //TODO: UI alert?
  }
}

DiscazosPlayer.currentPlaybackPositionChanged = function(currentMs) {
  var currentTrackProgress = currentMs - this.data.currentTrack.offset;
  var currentTrackHasFinish = currentTrackProgress >= this.data.currentTrack.length;
  if(currentTrackHasFinish) {
    if(!this.currentTrackIsLast()) {
      this.currentTrackChanged($(this.data.currentTrack.item).next());
    } else {
      DiscazosPlayer.stop();
    }
  } else {
    this.updateTrackProgress(currentTrackProgress);
  }
}
