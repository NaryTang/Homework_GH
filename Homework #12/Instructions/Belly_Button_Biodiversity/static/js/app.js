function buildMetadata(sample) {
  console.log(sample);
  // @TODO: Complete the following function that builds the metadata panel

  // Use `d3.json` to fetch the metadata for a sample
  var url = "/metadata/"+ sample;
  d3.json(url).then(function(sample) {
    // Use d3 to select the panel with id of `#sample-metadata`
    var sample_metadata = d3.select("#sample-metadata");
    // Use `.html("") to clear any existing metadata
    sample_metadata.html("");
    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(sample).forEach(([key, value]) => {
      sample_metadata.append("p").text(`${key}: ${value}`);
    })
  })
};

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  var url = "/samples/" + sample;
  d3.json(url).then(function(data) {
    // @TODO: Build a Bubble Chart using the sample data
    var xValues = data.otu_ids;
    var yValues = data.sample_values;
    var mSize = data.sample_values;
    var mColors = data.otu_ids;
    var tValues = data.otu_labels;

    var traceBubble = [{
      x: xValues,
      y: yValues,
      text: tValues,
      mode: "markers",
      marker: {
        size: mSize,
        color: mColors
      }
    }];

    var layout = {
      xaxis: {title: "OTU ID"}
    };

    Plotly.newPlot("bubble", traceBubble, layout);  
    

  // @TODO: Build a Pie Chart
  // HINT: You will need to use slice() to grab the top 10 sample_values,
  // otu_ids, and labels (10 each).

    var pValue = data.sample_values.slice(0,10);
    var pLabels = data.otu_ids.slice(0,10);
    var hText = data.otu_labels.slice(0,10);

    var pieData = [{
      values: pValue,
      labels: pLabels,
      hovertext: hText,
      type: "pie"
    }];

    Plotly.newPlot("pie", pieData);

  });
};

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
