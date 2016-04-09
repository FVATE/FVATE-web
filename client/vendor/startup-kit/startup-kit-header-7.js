/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 7*/
startupKit.uiKitHeader.header7 = function() {
  startupKit.uiKitHeader._inFixedMode('.header-7');
  $(window).resize(function() {
    var maxH = 0;
    $('.header-7-sub section').css('height', $(this).height() + 'px').each(function() {
      var h = $(this).outerHeight();
      if (h > maxH) maxH = h;
    }).css('height', maxH + 'px');
    $('.header-7-sub .page-transitions').css('height', maxH + 'px');
    var ctrlsHeight = $('.header-7-sub .pt-controls').height();
    $('.header-7-sub .pt-controls').css('margin-top', (-1) * (maxH) / 2 - ctrlsHeight + 'px');
    $('.header-7-sub .pt-controls').css('padding-bottom', (maxH) / 2 - ctrlsHeight + 'px');
  });


  // PageTransitions
  var pt = PageTransitions();
  pt.init('#h-7-pt-main');


  $('.header-7-sub .pt-controls .pt-indicators > *').on('click', function() {

    if ($(this).hasClass('active')) return false;

    var curPage = $(this).parent().children('.active').index();
    var nextPage = $(this).index();
    $('.header-7-sub').css('background-color',$('#h-7-pt-main').children('.pt-page').eq(nextPage).find('section').css('background-color'));
    var ani = 5;
    if (curPage < nextPage) {
      ani = 6;
    }

    pt.gotoPage(ani, nextPage);
    $(this).addClass('active').parent().children().not(this).removeClass('active');
    return false;

  });

};
