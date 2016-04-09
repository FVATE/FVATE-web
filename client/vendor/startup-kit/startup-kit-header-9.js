/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 9 */
startupKit.uiKitHeader.header9 = function() {

  startupKit.uiKitHeader._inFixedMode('.header-9');

  $(window).resize(function() {
    var h = 0;
    $('body > section:not(.header-9-sub)').each(function() {
      h += $(this).outerHeight();
    });
    $('.sidebar-content').css('height', h + 'px');
  });
};
