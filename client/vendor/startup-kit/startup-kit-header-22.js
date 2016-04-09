/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 22 */
startupKit.uiKitHeader.header22 = function() {
  if ($('.header-22 .navbar').hasClass('navbar-fixed-top')) {
    $('.header-22').css('position', 'fixed').addClass('fake-header');
  }
  startupKit.uiKitHeader._inFixedMode('.header-22');
};
