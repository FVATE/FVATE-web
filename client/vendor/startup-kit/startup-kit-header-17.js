/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 17 */
startupKit.uiKitHeader.header17 = function() {
  if ($('.header-17 .navbar').hasClass('navbar-fixed-top')) {
    $('.header-17').css('position', 'fixed').addClass('fake-header');
  }
  startupKit.uiKitHeader._inFixedMode('.header-17');

  var pt = PageTransitions();
  pt.init('#h-17-pt-1');

  $('.pt-controls .pt-indicators > *').on('click', function() {
    if ($(this).hasClass('active')) return false;

    var curPage = $(this).parent().children('.active').index();
    var nextPage = $(this).index();
    var ani = 44;
    if (curPage < nextPage) {
      ani = 45;
    }

    pt.gotoPage(ani, nextPage);
    $(this).addClass('active').parent().children().not(this).removeClass('active');
    return false;
  });

  $(window).resize(function() {
    $('.header-17-sub .page-transitions').each(function() {
      var maxH = 0;
      $('.pt-page', this).css('height', 'auto').each(function() {
        var h = $(this).outerHeight();
        if (h > maxH) maxH = h;
      }).css('height', maxH + 'px');
      $(this).css('height', maxH + 'px');
      if(!$(this).hasClass('calculated')){
        $(this).addClass('calculated');
      }
    });
  });

};
