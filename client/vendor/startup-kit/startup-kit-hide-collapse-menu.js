/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};


startupKit.hideCollapseMenu = function() {
  $('body > .navbar-collapse').css({
    'z-index': 1
  });
  $('html').removeClass('nav-visible');
  setTimeout(function() {
    $('body > .navbar-collapse').addClass('collapse');
    $('body > .colapsed-menu').removeClass('show-menu');
  }, 400);
};


/*
 * hide/collapse menu bar
 */
$(function () {

  $('.page-wrapper, .navbar-fixed-top, .navbar-collapse a, .navbar-collapse button, .navbar-collapse input[type=submit]').on('click', function() {
    if($('html').hasClass('nav-visible')) {
      setTimeout(function(){
        startupKit.hideCollapseMenu();
      }, 200);
    }
  });

  $(window).resize(function() {
    if($(window).width() > 965) {
      startupKit.hideCollapseMenu();
    }
  });


  var menuCollapse = $('#header-dockbar > .colapsed-menu').clone(true);
  $('body').append(menuCollapse);

  $('#open-close-menu').on('click', function () {
    if($('html').hasClass('nav-visible')) {
      startupKit.hideCollapseMenu();
    } else {
      $('body > .colapsed-menu').addClass('show-menu');
      if($('#header-dockbar').length) {
        $('body > .colapsed-menu').css({
          top: $('#header-dockbar').height()
        });
      }
      setTimeout(function() {
        $('html').addClass('nav-visible');
      }, 1);
    }
  });

  if($('.social-btn-facebook').length){
    $('.social-btn-facebook').sharrre({
      share: {
        facebook: true
      },
      enableHover: false,
      enableCounter: false,
      click: function(api, options){
        console.info('options:', options);
        api.simulateClick();
        api.openPopup('facebook');
      }
    });
  }

  if($('.social-btn-twitter').length){
    $('.social-btn-twitter').sharrre({
      share: {
        twitter: true
      },
      enableHover: false,
      enableCounter: false,
      buttons: {
        twitter: {via: 'Designmodo', url: false }
      },

      click: function(api, options){
        console.info('options:', options);
        api.simulateClick();
        api.openPopup('twitter');
      }

    });
  }
});
