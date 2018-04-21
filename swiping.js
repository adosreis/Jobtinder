let $card, $resume, $bio;
let resumeOpacity = 1;
let opacityUpdate = 0.1;
let disappearPoint = 400;
let scrolled = 0;

function scroll() {
  console.log("scrolled");
  scrolled = $card[0].scrollTop;
  $resume.style.opacity = "" + ((disappearPoint - scrolled) / disappearPoint);
  $bio.style.opacity = "" + (scrolled / disappearPoint);
}

function nope() {
  $card.addClass('noped');
  setTimeout(function () { generateCard('last was noped') }, 500);
}

function like() {
  $card.addClass('liked');
  setTimeout(function () { generateCard('last was liked') }, 500);
}

function generateCard(name) {
  let template = Handlebars.compile(document.getElementById('card-template').innerHTML);
  document.getElementById('card-spot').innerHTML = template({ name: name });

  $card = $('#card');
  $resume = $('.pdf')[0];
  $bio = $('.bio')[0];
  console.log($card);
  $card[0].onscroll = scroll;
}

generateCard('first');
