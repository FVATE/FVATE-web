/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


var plugin_settings_width = 1200;
var plugin_settings_height = 720;
var plugin_settings_align = "centerXY";
var $videoEl = null;


/* header 23 */

startupKit.uiKitHeader.header23 = function() {

  // startupKit.attachBgVideo();
  startupKit.uiKitHeader._inFixedMode('.header-23');
  startupKit.uiKitHeader.$holder = $('#bgVideo');
  $videoEl = $('#vimeo_embed');

  // $('body').prepend($('.mask, .popup-video').not('pre .mask, pre .popup-video'));
  // $('header-23 .mask, header-23 .popup-video').not('pre .mask, pre .popup-video').detach();

  // center + proportion the background video
  $(window).resize(function() {
    startupKit.uiKitHeader.header23.setProportion();
  });
};


startupKit.uiKitHeader.header23.setProportion = function () {
  var proportion = startupKit.uiKitHeader.header23.getProportion();
  var height = proportion * plugin_settings_height;
  var width = proportion * plugin_settings_width;

  $videoEl.width(width);
  $videoEl.height(height);

  if (typeof plugin_settings_align !== 'undefined') {
    startupKit.uiKitHeader.header23.centerVideo();
  }
};


startupKit.uiKitHeader.header23.getProportion = function () {
  var windowWidth = startupKit.uiKitHeader.$holder.width();
  var windowHeight = startupKit.uiKitHeader.$holder.height();
  var windowProportion = windowWidth / windowHeight;
  var origProportion = plugin_settings_width / plugin_settings_height;
  var proportion = windowHeight / plugin_settings_height;

  if (windowProportion >= origProportion) {
    proportion = windowWidth / plugin_settings_width;
  }

  return proportion;
};


startupKit.uiKitHeader.header23.centerVideo = function() {
  var centerX = ((startupKit.uiKitHeader.$holder.width() >> 1) - ($videoEl.width() >> 1)) | 0;
  var centerY = ((startupKit.uiKitHeader.$holder.height() >> 1) - ($videoEl.height() >> 1)) | 0;

  if (plugin_settings_align == 'centerXY') {
    $videoEl.css({ 'left': centerX, 'top': centerY });
    return;
  }

  if (plugin_settings_align == 'centerX') {
    $videoEl.css('left', centerX);
    return;
  }

  if (plugin_settings_align == 'centerY') {
    $videoEl.css('top', centerY);
    return;
  }
};


// iframe messaging interface to hack sending a play signal for mobile
// see: http://jsfiddle.net/bdougherty/UTt2K/light/
$(document).ready(function() {
  var f = $('iframe');
  var url = f.attr('src').split('?')[0];

  // listen for messages from the player
  if (window.addEventListener) {
    window.addEventListener('message', onMessageReceived, false);
  }
  else {
    window.attachEvent('onmessage', onMessageReceived, false);
  }

  // handle messages received from the player
  function onMessageReceived(e) {
    var data = JSON.parse(e.data);

    switch (data.event) {
    case 'ready':
      // onReady();
      break;

    case 'playProgress':
      // onPlayProgress(data.data);
      break;

    case 'pause':
      // onPause();
      break;

    case 'finish':
      // onFinish();
      break;
    }
  }

  // function for sending a message to the player
  function post(action, value) {
    var data = { method: action };

    if (value) {
      data.value = value;
    }

    f[0].contentWindow.postMessage(JSON.stringify(data), url);
  }

  var playing = false;

  $(document).bind('touchstart', function() {
    if (playing) return;
    playing = true;
    post('play');
  });

});
