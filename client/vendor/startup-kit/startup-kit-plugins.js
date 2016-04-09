
window.isRetina = (function() {
  var root = ( typeof exports == 'undefined' ? window : exports);
  var mediaQuery = "(-webkit-min-device-pixel-ratio: 1.5),(min--moz-device-pixel-ratio: 1.5),(-o-min-device-pixel-ratio: 3/2),(min-resolution: 1.5dppx)";
  if (root.devicePixelRatio > 1) return true;
  if (root.matchMedia && root.matchMedia(mediaQuery).matches) return true;
  return false;
})();


//nextOrFirst? prevOrLast?
jQuery.fn.nextOrFirst = function(selector) { var next = this.next(selector); return (next.length) ? next : this.prevAll(selector).last(); };
jQuery.fn.prevOrLast = function(selector){ var prev = this.prev(selector); return (prev.length) ? prev : this.nextAll(selector).last(); };


//preload images
$.fn.preload = function() {
  this.each(function(){
    $("<img/>")[0].src = this;
  });
};
