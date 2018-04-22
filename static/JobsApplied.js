let jobs = [
  {jobTitle: "CTO", companyName: "Google inc.", accepted: true},
  {jobTitle: "Managing Intern", companyName: "Phone.com", accepted: true},
  {jobTitle: "Some Position", companyName: "Some Company", accepted: false}
];

function generateTable() {
  let template = Handlebars.compile(document.getElementById('table-template').innerHTML);
  document.getElementById('table-body').innerHTML = template({jobs: jobs})
}
generateTable();