let $card, $resume, $bio;
let disappearPoint = 300;
let scrolled = 0;

function scroll() {
  scrolled = $card[0].scrollTop;
  let opacity = ((disappearPoint - scrolled) / disappearPoint);
  if (opacity <= 0.2) opacity = 0.2;
  $resume.style.opacity = "" + opacity;
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

function generateCard(person) {
  let template = Handlebars.compile(document.getElementById('card-template').innerHTML);
  document.getElementById('card-spot').innerHTML = template({ name: person.firstName + ' ' + person.lastName });

  $card = $('#card');
  $resume = $('.pdf')[0];
  $bio = $('.bio')[0];
  $card[0].onscroll = scroll;
}

generateCard('first');
