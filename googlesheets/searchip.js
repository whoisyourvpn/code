function searchForIP() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var range = sheet.getDataRange();
  var values = range.getValues();

  var results = [];

  for (var i = 0; i < values.length; i++) {
    // Assuming IPs are in the first column, change 0 to another index if they are in another column
    if (values[i][0].toString().startsWith('185.102.219.')) {
      results.push(values[i]);
    }
  }

  // Output results, this can be customized based on your needs
  if (results.length > 0) {
    var outputSheet = SpreadsheetApp.getActiveSpreadsheet().insertSheet('Search Results');
    outputSheet.getRange(1, 1, results.length, results[0].length).setValues(results);
  } else {
    SpreadsheetApp.getUi().alert('No matching IP addresses found.');
  }
}
