/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};
startupKit.uiKitHeader = startupKit.uiKitHeader || {};


/* header 5 */
startupKit.uiKitHeader.header5 = function() {

  startupKit.uiKitHeader._inFixedMode('.header-5');
  // PageTransitions
  $(window).resize(function() {
    var maxH = 0;
    $('.header-5-sub .pt-page').css('height', 'auto').each(function() {
      var h = $(this).outerHeight();
      if (h > maxH) maxH = h;
    }).css('height', maxH + 'px');
    $('.header-5-sub .page-transitions').css('height', maxH + 'px');
  });

  var pt1 = PageTransitions();
  pt1.init('#h-5-pt-1');

  $('#h-5-pt-1 .pt-control-prev').on('click', function() {
    pt1.gotoPage(5, 'prev');
    return false;
  });

  $('#h-5-pt-1 .pt-control-next').on('click', function() {
    pt1.gotoPage(6, 'next');
    return false;
  });

  var navbar = $('.header-5 .navbar');
  $('.search', navbar).click(function() {
    if (!navbar.hasClass('search-mode')) {
      navbar.addClass('search-mode');
      setTimeout(function() {
        $('header .navbar .navbar-search input[type="text"]').focus();
      }, 1000);
    } else {

    }
    return false;
  });

  $('.close-search', navbar).click(function() {
    navbar.removeClass('search-mode');
    return false;
  });
};
