/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 20 */
startupKit.uiKitHeader.header20 = function() {
  if ($('.header-20 .navbar').hasClass('navbar-fixed-top')) {
    $('.header-20').css('position', 'fixed').addClass('fake-header');
  }
  startupKit.uiKitHeader._inFixedMode('.header-20');
};
