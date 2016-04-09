/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};


/*
 * video background
 */

startupKit.attachBgVideo = function() {
  var $videobg = $('#bgVideo');
  if (!isMobile.any() && $videobg.length) {

    // see:
    // https://console.developers.google.com/project/apps~souterrain-prod/storage
    new $.backgroundVideo($videobg, {
      "holder": "#bgVideo",
      "align" : "centerXY",
      "path" : "http://storage.googleapis.com/souterrain-video/",
      "width": 1200,
      "height": 720,
      "filename" : "souterrain-v3",
      "types" : ["mp4", "ogg", "webm"]
    });

    // mobile device background-video hack
    // $(document).delegate('video', 'touchstart', function(e) {
    //   console.info('e:', e);

    //   var video = document.getElementById('bgVideo');
    //   video.play();
    // });

  }
};
