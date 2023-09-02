function analyzeIPs() {
  // Get the spreadsheet and the sheet in question
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  // Fetch all values in column A
  var columnA = sheet.getRange("A:A").getValues();
  
  // Dictionary to store subnet and its frequency
  var subnetFrequency = {};
  
  // Loop through each row in column A
  for (var i = 0; i < columnA.length; i++) {
    var ip = columnA[i][0];
    
    // Extract subnet from IP address
    var subnet = ip.substring(0, ip.lastIndexOf('.'));
    
    // Count the frequency
    if (subnet in subnetFrequency) {
      subnetFrequency[subnet]++;
    } else {
      subnetFrequency[subnet] = 1;
    }
  }
  
  // Convert the dictionary into an array of arrays for sorting
  var sortable = [];
  for (var subnet in subnetFrequency) {
    sortable.push([subnet, subnetFrequency[subnet]]);
  }
  
  // Sort by frequency, ascending
  sortable.sort(function(a, b) {
    return a[1] - b[1];
  });
  
  // Pick the top 15 least occurring subnets
  var top15LeastOccurring = sortable.slice(0, 15);
  
  // Output the results to the console
  console.log("Top 15 Least Occurring IP Subnets:");
  for (var i = 0; i < top15LeastOccurring.length; i++) {
    console.log(top15LeastOccurring[i][0] + ": " + top15LeastOccurring[i][1]);
  }
}
