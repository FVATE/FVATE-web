/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 18 */
startupKit.uiKitHeader.header18 = function() {
  $(window).resize(function() {
    maxH = $(window).height();
    $('.header-18 .page-transitions').css('height', maxH + 'px');
  });

  // PageTransitions
  var pt = PageTransitions();
  pt.init('#h-18-pt-main');

  $('.header-18 .pt-control-prev').on('click', function() {
    pt.gotoPage(5, 'prev');
    return false;
  });

  $('.header-18 .pt-control-next').on('click', function() {
    pt.gotoPage(6, 'next');
    return false;
  });

};
