/*
 * fullscreen block 23
 * src: https://github.com/designmodo/startup-support/issues/46
 */
(function($){
  $(window).resize(function(){
    var sH = $(window).height();
    $('section.header-23-sub').css('height', (sH - $('header').outerHeight()) + 'px');
  });
})(jQuery);
