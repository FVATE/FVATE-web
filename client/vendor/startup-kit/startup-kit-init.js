
/**
 * init startup-kit components
 */
(function($) {
  $(function() {


    /* init headers */
    // -----------------------------------------------------------------------
    for (var header in startupKit.uiKitHeader) {
      headerNumber = header.slice(6);
      if (jQuery('.header-' + headerNumber).length) {
        startupKit.uiKitHeader[header]();
      }
    }


    /* init contents */
    // -----------------------------------------------------------------------
    // for (var content in startupKit.uiKitContent) {
    //   contentNumber = content.slice(7);
    //   if (jQuery('.content-' + contentNumber).length) {
    //     startupKit.uiKitContent[content]();
    //   }
    // }


    /* init blogs */
    // -----------------------------------------------------------------------
    // for (var blog in startupKit.uiKitBlog) {
    //   blogNumber = blog.slice(4);
    //   if (jQuery('.blog-' + blogNumber).length) {
    //     startupKit.uiKitBlog[blog]();
    //   }
    // }


    /* init projects */
    // -----------------------------------------------------------------------
    // for (var project in startupKit.uiKitProjects) {
    //   projectNumber = project.slice(7);
    //   if (jQuery('.projects-' + projectNumber).length) {
    //     startupKit.uiKitProjects[project]();
    //   }
    // }


    // // replace project img to background-image
    // $('.project .photo img').each(function() {
    //   $(this).hide().parent().css('background-image', 'url("' + this.src + '")');
    // });


    /* init crew */
    // -----------------------------------------------------------------------
    // startupKit.uiKitCrew();


    /* init footers */
    // -----------------------------------------------------------------------
    // for (var footer in startupKit.uiKitFooter) {
    //   footerNumber = footer.slice(6);
    //   if (jQuery('.footer-' + footerNumber).length) {
    //     startupKit.uiKitFooter[footer]();
    //   }
    // }



    /* function on load */
    var $w = $(window);
    $w.load(function() {
      $('html').addClass('loaded');
      $w.resize();
    });


    /* ie fix images */
    if (/msie/i.test(navigator.userAgent)) {
      $('img').each(function() {
        $(this).css({
          width : $(this).attr('width') + 'px',
          height : 'auto'
        });
      });
    }


    // focus state for append/prepend inputs
    // $('.input-prepend, .input-append').on('focus', 'input', function() {
    //   $(this).closest('.control-group, form').addClass('focus');
    // }).on('blur', 'input', function() {
    //   $(this).closest('.control-group, form').removeClass('focus');
    // });


    /* init tiles */
    // -----------------------------------------------------------------------
    // var tiles = $('.tiles');

    // // tiles phone mode
    // $(window).resize(function() {
    //   if ($(this).width() < 768) {
    //     if (!tiles.hasClass('phone-mode')) {
    //       $('td[class*="tile-"]', tiles).each(function() {
    //         $('<div />').addClass(this.className).append($(this).contents()).appendTo(tiles);
    //       });

    //       tiles.addClass('phone-mode');
    //     }
    //   } else {
    //     if (tiles.hasClass('phone-mode')) {
    //       $('> [class*="tile-"]', tiles).each(function(idx) {
    //         $('td[class*="tile-"]', tiles).eq(idx).append($(this).contents());
    //         $(this).remove();
    //       });

    //       tiles.removeClass('phone-mode');
    //     }
    //   }
    // });

    // tiles.on('mouseenter', '[class*="tile-"]', function() {
    //   $(this).removeClass('faded').closest('.tiles').find('[class*="tile-"]').not(this).addClass('faded');
    // }).on('mouseleave', '[class*="tile-"]', function() {
    //   $(this).closest('.tiles').find('[class*="tile-"]').removeClass('faded');
    // });


  });

})(jQuery);
