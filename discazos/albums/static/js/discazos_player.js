var DiscazosPlayer = {};

$(document).ready(function() {
  DiscazosPlayer.swf = swfobject.getObjectById("discazos-player-swf");
  DiscazosPlayer.html = $("#discazos-player-html");
  
  DiscazosPlayer.data = { 
    albumLength: DiscazosPlayer.html.find("#album-length").html(), 
    currentTrack: false,
  };
  
  /** Initialize UI **/
  
  $("#play-button").button({
    text: false,
    icons: {
      primary: "ui-icon-play"
    }
  }).click(function() {
    var options;
    if($(this).text() === "Play") {
      DiscazosPlayer.play();
      options = {
        label: "Pause",
        icons: {
          primary: "ui-icon-pause"
        }
      };
    } else {
      DiscazosPlayer.pause();
      options = {
        label: "Play",
        icons: {
          primary: "ui-icon-play"
        }
      };
    }
    $(this).button("option", options);
  });
  $("#prev-button").button({
    text: false,
    icons: {
      primary: "ui-icon-seek-start"
    }
  }).click(function() { 
    DiscazosPlayer.playPrevious(); 
  });
  $("#next-button").button({
    text: false,
    icons: {
      primary: "ui-icon-seek-end"
    }
  }).click(function() { 
    DiscazosPlayer.playNext(); 
  });
  
  DiscazosPlayer.html.find("#player-wrapper div.main div.left").alternateScroll();
  
  DiscazosPlayer.html.find("#loading-discazo").progressbar();
  
  DiscazosPlayer.html.find("#progressbar").slider({
    range: 'min',
    change: function(event, ui) {
      if(event.originalEvent && event.originalEvent.type == "mouseup") {
        //TODO
        /*var seekPercentage = event.originalEvent.clientX;
                DiscazosPlayer.trackSeek(seekPercentage);*/
      }
    }
  });
  
  DiscazosPlayer.html.find("#playlist tr").each(function() {
    $(this).click(function() { DiscazosPlayer.playTrack(this); });
  });

});

/***** JS Player ******/

/* Actions */

DiscazosPlayer.load = function(url) {
  var albumCover = DiscazosPlayer.html.find("a.load-link");
  albumCover.find("span.load-button").remove();
  albumCover.find("#album-cover").unwrap();
  
  this.swf.load(url);
}

DiscazosPlayer.play = function() {
  if(!this.data.currentTrack) {
    this.playTrack(this.html.find('#playlist tr:first'))
  } else {
    this.swf.play();
  }
}

DiscazosPlayer.pause = function() {
  this.swf.pause();
}

DiscazosPlayer.playTrack = function(trackItem) {
  //Update track information
  this.currentTrackChanged(trackItem);
  
  //Start playing the track
  newMsPosition = this.data.currentTrack.offset * 1000;
  //If it's the starting position, seek to 1
  if(newMsPosition == 0) newMsPosition = 1;
  this.swf.seek(newMsPosition);
}

DiscazosPlayer.playNext = function() {
  this.playTrack($(this.data.currentTrack.item).next());
}

DiscazosPlayer.playPrevious = function() {
  this.playTrack($(this.data.currentTrack.item).prev());
}

DiscazosPlayer.currentTrackChanged = function(trackItem) {
  this.data.currentTrack = { 
    item: $(trackItem),
    offset: parseInt($(trackItem).find('.track-number').attr('rel')),
    length: parseInt($(trackItem).find('.track-length').attr('rel')),
  }
  //Set progress bar to 0
  this.html.find('#progressbar').progressbar("value", 0);
  //Update track name
  this.html.find('#current-track').html($(trackItem).find('.track-name').html());
}

DiscazosPlayer.updateTrackProgress = function(currentProgress) {
  this.updateTrackProgressbar(currentProgress);
}

DiscazosPlayer.updateTrackProgressbar = function(currentProgress) {
  var percentage = Math.round((currentProgress / this.data.currentTrack.length) * 100);
  this.html.find('#progressbar').slider("value", percentage);
}

/* Flash player events */

DiscazosPlayer.updateBufferProgress = function(msLoaded, msTotal) {
  var secondsLoaded = msLoaded / 1000;
  var percentage = Math.round((secondsLoaded / this.data.albumLength) * 100);
  this.html.find('#loading-discazo').progressbar("value", percentage);
}

DiscazosPlayer.currentPlaybackPositionChanged = function(currentMs) {
  var currentSeconds = currentMs / 1000;
  var currentTrackProgress = currentSeconds - this.data.currentTrack.offset;
  var currentTrackHasFinish = currentTrackProgress >= this.data.currentTrack.length;
  if(currentTrackHasFinish) {
    this.currentTrackChanged($(this.data.currentTrack.item).next());
  } else {
    this.updateTrackProgress(currentTrackProgress);
  }
}

/*DiscazosPlayer.convertToMMSS = function(ms) {
  var seconds = ms / 1000;
  var minutes = seconds / 60;
  var MMSS = Math.round(minutes) + ":" + Math.round(seconds);
  return MMSS;
}*/
