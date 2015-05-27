document.getElementById("overlay").addEventListener('click',function(){
  document.getElementById('overlay').style.opacity = "0";
  setTimeout(function(){
    document.getElementById('overlay').style.visibility = 'hidden';
  }, 300);
});
document.getElementById("full_desc").addEventListener('click',function(){
    event.stopPropagation();
});
projects = document.getElementsByClassName("pjct_cover");
for (var i = 0; i < projects.length; i++) {
    projects[i].addEventListener('click',ajax,false);
}
function ajax() {
  document.getElementById('overlay').style.visibility = "visible";
  document.getElementById('overlay').style.opacity = "1";
  project = this.parentNode.dataset.project
  var httpRequest;
  if (window.XMLHttpRequest) { // Mozilla, Safari, IE7+ ...
      httpRequest = new XMLHttpRequest();
  } else if (window.ActiveXObject) { // IE 6 and older
      httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
  }
  httpRequest.onreadystatechange = function(){
    if (httpRequest.readyState === 4) {
      document.getElementById('full_desc').innerHTML = httpRequest.responseText;
    }
  };
  httpRequest.open('GET', 'desc?'+'project='+project, true);
  httpRequest.send();
}
