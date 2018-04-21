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