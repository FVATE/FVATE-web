/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 21 */
startupKit.uiKitHeader.header21 = function() {
  startupKit.uiKitHeader._inFixedMode('.header-21');
  maxH = $(window).height();

  if($('.navbar-fixed-top').length){
    maxH = maxH - $('.navbar-fixed-top').outerHeight();
  }

  if($('.header-21').length){
    maxH = maxH - $('.header-21').outerHeight();
  }

  if((maxH / 90) < 3){
    $('.header-21-sub .control-btn').css('bottom', 0);
  }

  $('.header-21-sub').height(maxH);

  $('.header-21-sub .control-btn').on('click', function() {
    $.scrollTo($(this).closest('section').next(), {
      axis : 'y',
      duration : 500
    });
    return false;
  });

};
