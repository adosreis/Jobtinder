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

function nope(){
    var $card = $('#card');
    $card.addClass('noped')
    setTimeout(function(){generateCard('last was noped')}, 500);
}

function like(){
    var $card = $('#card');
    $card.addClass('liked')
    setTimeout(function(){generateCard('last was liked')}, 500);
}

function generateCard(name){
    var template = Handlebars.compile(document.getElementById('card-template').innerHTML);
    document.getElementById('card-spot').innerHTML = template({name: name})
}

generateCard('first')