let $resume = $('.pdf')[0];
let $bio = $('.bio')[0];
let $info = $('.person-card')[0];
let resumeOpacity = 1;
let opacityUpdate = 0.1;
let disappearPoint = 400;
let scrolled = 0;

$info.onscroll = scroll;
function scroll() {
  $resume.style.opacity = "" + ((disappearPoint - scrolled) / disappearPoint);
  $bio.style.opacity = "" + (scrolled / disappearPoint);
  scrolled = $info.scrollTop;
}