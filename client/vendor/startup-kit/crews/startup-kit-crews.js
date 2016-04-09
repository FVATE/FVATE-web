/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};

/**
 * crews
 */
startupKit.uiKitCrew = startupKit.uiKitCrew ||

// ---------------------------------------------------------------------------


function() {
  $('.member .photo img').each(function() {
    $(this).hide().parent().css('background-image', 'url("' + this.src + '")');
  });
};
