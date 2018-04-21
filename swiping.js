var $card, $resume, $bio, $info;


let resumeOpacity = 1;
let opacityUpdate = 0.1;
let disappearPoint = 400;
let scrolled = 0;

function scroll() {
  $resume.style.opacity = "" + ((disappearPoint - scrolled) / disappearPoint);
  $bio.style.opacity = "" + (scrolled / disappearPoint);
  scrolled = $info.scrollTop;
}

function nope() {
  $card.addClass('noped')
  setTimeout(function () { generateCard('last was noped') }, 500);
}

function like() {
  $card.addClass('liked')
  setTimeout(function () { generateCard('last was liked') }, 500);
}

function generateCard(name) {
  var template = Handlebars.compile(document.getElementById('card-template').innerHTML);
  document.getElementById('card-spot').innerHTML = template({ name: name })

  $card = $('#card');
  $resume = $('.pdf')[0];
  $bio = $('.bio')[0];
  $card.onscroll = scroll;
}

generateCard('first')
