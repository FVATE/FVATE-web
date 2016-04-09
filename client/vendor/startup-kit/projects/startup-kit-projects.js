/**
 * namespace for all ui-kit components.
 */
window.startupKit = window.startupKit || {};

/**
 * projects
 */
startupKit.uiKitProjects = startupKit.uiKitProjects || {};


/* project-1 */
startupKit.uiKitProjects.project1 = function() {};

/* project-2 */
startupKit.uiKitProjects.project2 = function() {};

/* project-3 */
startupKit.uiKitProjects.project3 = function() {};

/* project-4 */
startupKit.uiKitProjects.project4 = function() {
  $('.overlay').on('hover', function() {
    $(this).closest('.project').find('.name').toggleClass('hover');
  });
};
