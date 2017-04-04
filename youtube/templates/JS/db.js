/**
 * videoDB is responsible for loading
 * and managing the video data from the data.js file.
 */
var videoDB = (function() {
  var ITEMS_PER_PAGE = 40;
  var db = {};
  var data;
  var page;
  var selected_playlist
  var  i
  var json_selected
  /**
   * Load the data with or without an 
   * applied language filter. 
   * The data will be loaded from the json in 
   * the data.js file.
   * @param {language} Language filter that you want
   *                   to apply to the data set. 
   *                   Pass in 'undefined' if you don't 
   *                   want any language filter.
   * @param {callback} This callback will be called 
   *                   when the data is loaded.
   */
  db.getjson = function(){
	i = document.playlist.list.selectedIndex;
	selected_playlist = document.playlist.list.options[i].value;
	json_selected = window["json_".concat(selected_playlist)];
  }
  db.loadData = function(language, callback){
    if (typeof language === 'undefined'){
      data = json_selected;
    }
    else {

      // Clear the previously loaded data.
      data = [];

      // Iterate through the whole data set and 
      // add the video objects that have the language 
      // that we want to the data array.
      for (i in json_selected){
        if (json_selected[i].languages.indexOf(language) > -1) {
          data.push(json_selected[i]);
        }
      }
    }
    callback();
  }

  /**
   * Get the count pages that we need to set up.
   */
  db.getPageCount = function() {
    return Math.ceil(data.length / ITEMS_PER_PAGE);
  }

  /**
   * Move one page forward. 
   * @param {callback} This callback is called when 
   *                   you have to load a new page. 
   */
  db.pageForward = function(callback) {
    if (page < db.getPageCount()) {
      page++;
      window.location.hash = '#' + page;  
      callback();
    }
  }

  /**
   * Move one page back. 
   * @param {callback} This callback is called when 
   *                   you have to load a new page. 
   */
  db.pageBackwards = function(callback) {
    if (page != 1) {
      page--;
      window.location.hash = '#' + page;
      callback();
    }
  }

  /**
   * Reset the page count to 1.
   */
  db.resetPage = function() {
    page = 1;
    window.location.hash = '#' + page;
  }

  /**
   * Get the current page number.
   */
  db.getPageNumber = function() {
      if ( !page ) {
	  page = location.hash.replace( '#', '' );
      }

      return page || 1;
  }

  /**
   * Get the video data for a certain page.
   * @param {page} Page number for the page 
   *               you want the data for.
   */
  db.getPage = function(page) {
    var pageStart = (page-1)*ITEMS_PER_PAGE;
    var pageEnd = page*ITEMS_PER_PAGE;
    return data.slice(pageStart, pageEnd);
  }

  return db;

}());
