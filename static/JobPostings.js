let jobPostings = [
  {jobTitle:"HR Intern", applicants:[]},
  {jobTitle:"QA Manager", applicants:[]}
];

function generateTable() {
  let template = Handlebars.compile(document.getElementById('table-template').innerHTML);
  document.getElementById('table-body').innerHTML = template({jobPostings: jobPostings})
}
generateTable();