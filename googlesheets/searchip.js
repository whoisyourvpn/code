function searchForIP() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var range = sheet.getDataRange();
  var values = range.getValues();

  var results = [];

  for (var i = 0; i < values.length; i++) {
    // Assuming IPs are in the first column, change 0 to another index if they are in another column
    if (values[i][0].toString().startsWith('143.244.45.')) {
      results.push(values[i]);
    }
  }

  // Output results to console
  if (results.length > 0) {
    console.log("Matching IP addresses found:");
    for (var i = 0; i < results.length; i++) {
      console.log(results[i][0]);
    }
  } else {
    console.log('No matching IP addresses found.');
  }
}
