/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 11 */
startupKit.uiKitHeader.header11 = function() {
  if ($('.header-11 .navbar').hasClass('navbar-fixed-top')) {
    $('.header-11').css('position', 'fixed').addClass('fake-header');
  }
  startupKit.uiKitHeader._inFixedMode('.header-11');

  $(window).resize(function() {

    var headerContainer = $('.header-11-sub').not('pre .header-11-sub');
    var player = headerContainer.find('.player');
    if ($(window).width() < 751) {
      headerContainer.find('.signup-form').before(player);
      headerContainer.find('.player-wrapper').hide();
    } else {
      headerContainer.find('.player-wrapper').append(player).show();
    }
  });
};
