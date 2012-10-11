var DiscazosPlayer = {};
var DiscazosPlayerUI = {}

DiscazosPlayer.MIN_BYTES_TO_LOAD = 491520; //30 seconds of 128kbps audio

$(document).ready(function() {
  DiscazosPlayer.swf = swfobject.getObjectById("discazos-player-swf");
  DiscazosPlayerUI.html = $("#discazos-player-html");
  
  DiscazosPlayer.data = { 
    audioFileSize: DiscazosPlayerUI.html.find("#album-audiofile-size").html(),
    currentTrack: false,
    minLoadedTriggered: false,
    bufferLoadingStarted: false,
    selectedDownloadSourceId: null,
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
  this.html.find("#loading-discazo").progressbar();
  
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

/***** JS Player ******/

/* Actions */

DiscazosPlayer.load = function(url) {
  var albumCover = DiscazosPlayerUI.html.find("a.load-link");
  albumCover.find("span.load-button").remove();
  albumCover.find("#album-cover").unwrap(); //Removes the loading link
  
  this.swf.load(url);
  
  var loadingOverlay = DiscazosPlayerUI.html.find("#player-wrapper div.main div.loading-overlay");
  loadingOverlay.find("#download-sources-frame #download-sources-wrapper").hide();
  loadingOverlay.find("#download-sources-frame #link-available-box").show();

  DiscazosPlayerUI.html.bind("bufferInitLoadingError", function() {
    loadingOverlay.find("#download-sources-frame #link-available-box").hide();
    loadingOverlay.find("#download-sources-frame #buffer-error-text").show();
    loadingOverlay.find("#download-sources-frame #download-sources-wrapper").show();
  });

  DiscazosPlayerUI.html.bind("bufferLoadingStarted", function() {
    loadingOverlay.find("#download-sources-frame .preload-init").hide()
    loadingOverlay.find("#download-sources-frame .preloading").show();
  });
  
  //After the preload has finished, activate the player controls
  DiscazosPlayerUI.html.bind("minLoaded", function() {
    loadingOverlay.remove();
    DiscazosPlayerUI.html.find('#loading-discazo span.caption').show();
    DiscazosPlayerUI.html.find("#player-controls").slideDown('slow');
    DiscazosPlayerUI.html.find(".playlist tr.track").each(function() {
      $(this).hover(function() { $(this).addClass("hover") }, 
                    function() { $(this).removeClass("hover") });
      $(this).click(function() { DiscazosPlayer.playTrack(this); });
    });
  });
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
  newMsPosition = this.data.currentTrack.offset;
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

/* Flash player events */

DiscazosPlayer.bufferLoadingStarted = function() {
  this.data.bufferLoadingStarted = true;
  Dajaxice.discazos.albums.log_album_playback(jQuery.noop, {
    'album_release_dl_source_id': this.data.selectedDownloadSourceId,
    'output_message': 'SUCCESSFUL'
  });
  DiscazosPlayerUI.html.trigger("bufferLoadingStarted");
}

DiscazosPlayer.bufferError = function(errorText) {
  if(!this.bufferLoadingStarted) {
    Dajaxice.discazos.albums.log_album_playback(jQuery.noop, {
      'album_release_dl_source_id': this.data.selectedDownloadSourceId,
      'output_message': 'DL_INIT_BUFFER_ERROR'
    });
    DiscazosPlayerUI.html.trigger("bufferInitLoadingError");
  }
  console.log("SWF loading buffer error: "+errorText);
}

DiscazosPlayer.updateBufferProgress = 
  function(bytesLoaded, bytesTotal) { //bytesTotal is not reliable until loading finishes
    if(bytesLoaded >= DiscazosPlayer.MIN_BYTES_TO_LOAD) {
      if(!this.data.minLoadedTriggered) {
         this.data.minLoadedTriggered = true;
         DiscazosPlayerUI.html.trigger("minLoaded");
      }
      var percentage = (bytesLoaded / this.data.audioFileSize) * 100;
      var progressbarWidget = DiscazosPlayerUI.html.find('#loading-discazo');
      progressbarWidget.children('span.caption').html(percentage.toFixed(1) + ' %');
      progressbarWidget.progressbar("value", percentage);
    } else {
      var preloadPercentage = Math.round((bytesLoaded / DiscazosPlayer.MIN_BYTES_TO_LOAD) * 100);
      DiscazosPlayerUI.html.find('#preload-percentage').html(preloadPercentage);
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
