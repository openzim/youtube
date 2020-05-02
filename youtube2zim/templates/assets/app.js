
window.onload = genplaylist();

function genplaylist() {
    // Load the initial data. 
    // This will display all data without any language filter.
    videoDB.resetPage();
    videoDB.getjson();
    videoDB.loadData(undefined, function() {
        var data = videoDB.getPage(videoDB.getPageNumber());
        firstVideo(videoDB.getFirstVideo());
        refreshVideos(data)    
    })    
    setupPagination();
    refreshPagination();
    return false;
}


/**
* This function handles the pagination:
* Clicking the back and forward button.
*/
function setupPagination() {

    function handlePagination(){
        var data = videoDB.getPage(videoDB.getPageNumber());
        refreshVideos(data);
        refreshPagination();
        window.scrollTo(0, 0);
    }

    for (var i = 0 ; i<2 ; i++) {
    var leftArrow = document.getElementsByClassName('left-arrow')[i];
    var rightArrow = document.getElementsByClassName('right-arrow')[i];
    // var pageText = document.getElementsByClassName('pagination-text')[i];
    
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
            pageText.innerHTML = pageText.getAttribute("data-format").replace("{current}", pageNumber).replace("{total}", pageCount);
    
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
      a.href =  video['slug'] + ".html";
      a.className = 'nostyle'

      var img = document.createElement('img');
      img.src = ZIM_IMG_NS + "videos/" + video['id'] + "/video.jpg";

      var title = document.createElement('p');
      title.id = 'title';
      title.innerHTML = video['title'];

      a.appendChild(img);
      a.appendChild(title);
      li.appendChild(a);
      videoList.appendChild(li);
    }
}


function firstVideo(video) {
    var videoIntro = document.getElementById('video-intro');
    var subtitles = '';
    if (video['subtitles'].length > 0) {
        for (i in video['subtitles']) {
            var subtitle = video['subtitles'][i];
            subtitles += '<track kind="subtitles" src="videos/' + video['id'] + '/video.' + subtitle['code'] + '.vtt" srclang="' + subtitle['code'] + '" label="' + subtitle['native'] + '" />';
        }
    }
    var video_desctiption = video['description'].slice(0, 200);
    if (video['description'].length > 200) {
        video_desctiption += '...';
    }
    videoIntro.innerHTML = '' +
        '<video id="video_container" class="video-js vjs-default-skin" ' +
               'width="480px" height="270px" crossorigin ' +
               'data-setup=\'{"techOrder": ["html5", "ogvjs"], ' + 
                            '"ogvjs": {"base": "assets/ogvjs"}, "autoplay": false, ' +
                                      '"preload": true, "controls": true, "controlBar": {"pictureInPictureToggle": false}}\'' +
               'poster="' + ZIM_IMG_NS + 'videos/' + video['id'] + '/video.jpg">' +
            '<source src="' + ZIM_IMG_NS + 'videos/' + video['id'] + '/video.{{ video_format }}" ' +
                    'type="video/{{ video_format }}" />' + subtitles + '</video>' +
            '<div id="video-details">' +
                '<h4 id="title">' +
                    '<a href=\'' + video['slug'] + '.html\'>' +
                        video['title'] +
                    '</a>' +
                '</h4>' + 
                '<p class="description">' +
                    video_desctiption +
                '</p>' +
            '</div>';
}
