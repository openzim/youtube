
window.onload = genplaylist();

function genplaylist() {
  setupLanguageFilter();
  // Load the initial data. 
  // This will display all data without any language filter.
  videoDB.resetPage();
  videoDB.getjson();
  videoDB.loadData(undefined, function() {
    var data = videoDB.getPage(videoDB.getPageNumber());
    firstVideos(data);
    refreshVideos(data);

  });

  setupPagination();
  refreshPagination();
  return false;
}

/** 
 * Apply a language filter, that is selected by the
 * drop down options <select> menu. 
 * This will then only display items that have
 * subtitles in the selected language.
 */
function setupLanguageFilter() {
  $('.chosen-select').chosen({width: "380px"}).change(function(){
    language = arguments[1].selected;

    // If 'lang-all' is selected the user wants to
    // display videos in all languages. 
    // This removes the previously set filter (if any).
    if (language == 'lang-all') {
      language = undefined;
    }

    // Load the data for the selected language and 
    // generate the video list.
    videoDB.resetPage();
    videoDB.loadData(language, function() {
      var data = videoDB.getPage(videoDB.getPageNumber());
      refreshVideos(data);
      refreshPagination();
    });
  });
}

/**
* This function handles the pagination:
* Clicking the back and forward button.
*/
function setupPagination() {

    function handlePagination(shouldChange){
	var data = videoDB.getPage(videoDB.getPageNumber());
	refreshVideos(data);
	refreshPagination();
	window.scrollTo(0, 0);
    }

    for (var i = 0 ; i<2 ; i++) {
	var leftArrow = document.getElementsByClassName('left-arrow')[i];
	var rightArrow = document.getElementsByClassName('right-arrow')[i];
	var pageText = document.getElementsByClassName('pagination-text')[i];
	
	leftArrow.onclick = function() {
	    videoDB.pageBackwards(function() {
		handlePagination();
	    });
	}
	
	rightArrow.onclick = function() {
	    videoDB.pageForward(function(){
		handlePagination();
	    });
	}
    }
}

/**
 * Reset the page text on the pagination widget, 
 * if a new language has been applied.
 */
function refreshPagination() {
    var pageCount = videoDB.getPageCount();

    for (var i = 0 ; i<2 ; i++) {
	var pageBox = document.getElementsByClassName('pagination')[i];
	var leftArrow = document.getElementsByClassName('left-arrow')[i];
	var rightArrow = document.getElementsByClassName('right-arrow')[i];
	
	if (pageCount > 1) {
	    var pageText = document.getElementsByClassName('pagination-text')[i];
	    var pageNumber = videoDB.getPageNumber();
	    pageText.innerHTML = 'Page ' + pageNumber + '/' + pageCount;

	    if (videoDB.getPageNumber() == 1) {
		leftArrow.style.visibility = 'hidden';
		rightArrow.style.visibility = 'visible';
	    } else if (pageNumber == pageCount) {
		leftArrow.style.visibility = 'visible';
		rightArrow.style.visibility = 'hidden';	
	    } else {
		leftArrow.style.visibility = 'visible';
		rightArrow.style.visibility = 'visible';	
	    }
	    
	    pageBox.style.visibility = 'visible';
	    pageBox.style.display = '';
	    leftArrow.style.display = '';
	    rightArrow.style.display = '';
	} else {
	    pageBox.style.display = 'none';
	    leftArrow.style.display = 'none';
	    rightArrow.style.display = 'none';
	}
    }
}

/**
 * Dynamically generate the video item out of 
 * the passed in {pageData} parameter.
 * @param {pageData} Video data for the current page.
 */
function refreshVideos(pageData) {  
    var videoList = document.getElementById('video-items');
    videoList.innerHTML = '';
    
    for (i in pageData) {
      var video = pageData[i];
      var li = document.createElement('li');
      
      var a = document.createElement('a')
      a.href =  video['id']+'/index.html';
      a.className = 'nostyle'

      var img = document.createElement('img');
      /*img.src = video['id']+'/thumbnail.jpg';*/
      img.src = '../I/'+video['id']+'/thumbnail.jpg'; 

      var title = document.createElement('p');
      title.id = 'title';
      title.innerHTML = video['title'];

      a.appendChild(img);
      a.appendChild(title);
      li.appendChild(a);
      videoList.appendChild(li);
    }
}


function firstVideos(pageData) {  
    var videoDetails = document.getElementById('video-details');
    videoDetails.innerHTML = '';
    var video = pageData[0];

    var video_js = videojs("video");
    /* video_js.src(video['id'] + "/video.{{ format }}"); */
    video_js.src("../I/" + video['id'] + "/video.{{ format }}");
    video_js.load();
    video_js.play();

    var title = document.createElement('h4')
    title.id = 'title';
    title.innerHTML = video['title'];
    videoDetails.appendChild(title);

    var description = document.createElement('p');
    description.innerHTML = video['description'];
    videoDetails.appendChild(description);

}
