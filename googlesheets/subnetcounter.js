function extractUniqueSubnets() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var inputSheet = spreadsheet.getSheetByName("IPDB");
  var outputSheet = spreadsheet.getSheetByName("Output");

  var data = inputSheet.getRange("A:A").getValues();
  var subnets = {};

  // Loop through each IP and extract the subnet
  for (var i = 0; i < data.length; i++) {
    if (data[i][0]) {
      var subnet = data[i][0].substr(0, data[i][0].lastIndexOf('.'));
      Logger.log('Processing subnet: ' + subnet);  // Log the current subnet
      if (subnet in subnets) {
        subnets[subnet] += 1;  // increment the count for this subnet
      } else {
        subnets[subnet] = 1;  // start a new count for this subnet
      }
    }
  }

  // Write the unique subnets and their counts to the output sheet
  var row = 1;
  for (var subnet in subnets) {
    outputSheet.getRange(row, 1).setValue(subnet);
    outputSheet.getRange(row, 2).setValue(subnets[subnet]);
    row++;
  }

  Logger.log('Script finished. Processed ' + (row - 1) + ' subnets.');  // Log the total number of processed subnets
}
