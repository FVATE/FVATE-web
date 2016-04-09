/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 1 */
startupKit.uiKitHeader.header1 = function() {
  var pt = PageTransitions();
  pt.init('#pt-main');
  $('#pt-main .control-prev').on('click', function() {
    pt.gotoPage(5, 'prev');
    return false;
  });
  $('#pt-main .control-next').on('click', function() {
    pt.gotoPage(6, 'next');
    return false;
  });

  startupKit.uiKitHeader._inFixedMode('.header-1');

};
