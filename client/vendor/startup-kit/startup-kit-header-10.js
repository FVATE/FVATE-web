/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 10*/
startupKit.uiKitHeader.header10 = function() {
  if ($('.header-10 .navbar').hasClass('navbar-fixed-top')) {
    $('.header-10').css('position', 'fixed').addClass('fake-header');
  }
  startupKit.uiKitHeader._inFixedMode('.header-10');

  $('.header-10-sub .control-btn').on('click', function() {
    $.scrollTo($(this).closest('section').next(), {
      axis : 'y',
      duration : 500
    });
    return false;
  });
};
