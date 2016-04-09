/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 3 */
startupKit.uiKitHeader.header3 = function() {
  if ($('.header-3 .navbar').hasClass('navbar-fixed-top')) {
    $('.header-3').css('position', 'fixed').addClass('fake-header');
  }
  startupKit.uiKitHeader._inFixedMode('.header-3');
};
