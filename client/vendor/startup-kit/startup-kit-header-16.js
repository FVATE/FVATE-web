/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 16 */
startupKit.uiKitHeader.header16 = function() {
  startupKit.uiKitHeader._inFixedMode('.header-16');

  var pt = PageTransitions();
  pt.init('#h-16-pt-main');

  $('#h-16-pt-main .pt-control-prev').on('click', function() {
    pt.gotoPage(2, 'prev');
    return false;
  });
  $('#h-16-pt-main .pt-control-next').on('click', function() {
    pt.gotoPage(1, 'next');
    return false;
  });

  $('.header-16-sub .scroll-btn a').on('click', function(e) {
    e.preventDefault();
    $.scrollTo($(this).closest('section').next(), {
      axis : 'y',
      duration : 500
    });
    return false;
  });
  $(window).resize(function() {
    $('.header-16-sub').css('height', $(this).height() + 'px');
  });
  $(window).resize().scroll();
};
