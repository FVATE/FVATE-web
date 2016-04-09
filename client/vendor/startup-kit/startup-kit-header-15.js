/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 15 */
startupKit.uiKitHeader.header15 = function() {
  if ($('.header-15 .navbar').hasClass('navbar-fixed-top')) {
    $('.header-15').css('position', 'fixed').addClass('fake-header');
  }
  startupKit.uiKitHeader._inFixedMode('.header-15');
};
