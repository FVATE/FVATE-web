/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 8 */
startupKit.uiKitHeader.header8 = function() {
  if ($('.header-8 .navbar').hasClass('navbar-fixed-top')) {
    $('.header-8').css('position', 'fixed').addClass('fake-header');
  }
  startupKit.uiKitHeader._inFixedMode('.header-8');
};
