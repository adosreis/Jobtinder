var people = [
    {name: 'Johnny Appleseed', accepted: true},
    {name: 'someone else', accepted: false},
    {name: 'a third person', accepted: false}
]

function generateTable(){
  var template = Handlebars.compile(document.getElementById('table-template').innerHTML);
  document.getElementById('table-body').innerHTML = template({ people: people })
}
generateTable()

