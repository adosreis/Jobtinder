let $card, $resume, $bio;
let disappearPoint = 300;
let scrolled = 0;
let personId = 0;

function scroll() {
  scrolled = $card[0].scrollTop;
  let opacity = ((disappearPoint - scrolled) / disappearPoint);
  if (opacity <= 0.2) opacity = 0.2;
  $resume.style.opacity = "" + opacity;
  $bio.style.opacity = "" + (scrolled / disappearPoint);
}

function nope() {
  $card.addClass('noped');
  sendSwipe(0);
  //setTimeout(function () { generateCard('last was noped') }, 500);
}

function like() {
  $card.addClass('liked');
  sendSwipe(1);
  //setTimeout(function () { generateCard('last was liked') }, 500);
}

function sendSwipe(swipe){
  $.ajax({
    url: location.href + '/swipe',
    data: {'status': swipe, 'applicantId': personId},
    method: 'POST',
    success: function(data){
      generateCard(JSON.parse(data));
    }
  });
}

function generateCard(person) {
  console.log(person)
  let template = Handlebars.compile(document.getElementById('card-template').innerHTML);
  document.getElementById('card-spot').innerHTML = template({ name: person.firstName + ' ' + person.lastName, skills: person.skills, location: person.address_city + ', ' + person.address_state + ', ' + person.address_country });
  personId = person.id;

  $card = $('#card');
  $resume = $('.pdf')[0];
  $bio = $('.bio')[0];
  $card[0].onscroll = scroll;
}

//generateCard('first');
