// from data.js
let tableData = data;

//select tbody for output
let tbody = d3.select("tbody");


let submit = d3.select("#filter-btn");

submit.on("click", function() {
	// Prevent the page from refreshing
	d3.event.preventDefault();

  // Select the input element and get the raw HTML node
  let inputElement = d3.select("#datetime").property("value");

  //console.log(inputElement);

  let filteredData = tableData.filter(date => date.datetime === inputElement);

  filteredData.forEach((rowData) => {
  	tbody.HTML("")
  	let row = tbody.append("tr");
  	Object.entries(rowData).forEach(([key, value]) => {
		row.append("td").text(value);
  	})
  })
});