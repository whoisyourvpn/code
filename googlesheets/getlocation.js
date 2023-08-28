function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Custom Menu')
      .addItem('Get location', 'getLocation')
      .addToUi();
}

function getLocation() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var range = sheet.getActiveRange();
  var data = range.getValues();
  var startRow = range.getRow();

  for (var i = 0; i < data.length; i++) {
    var ip = data[i][0];
    var location = GET_LOCATION(ip);
    // Write the country into column D, the region into column E, the city into column F, the ISP into column G, and the ASN into column H
    sheet.getRange(startRow + i, 4).setValue(location[0]); // Country
    sheet.getRange(startRow + i, 5).setValue(location[1]); // Region
    sheet.getRange(startRow + i, 6).setValue(location[2]); // City
    sheet.getRange(startRow + i, 7).setValue(location[3]); // ISP (without ASN)
    sheet.getRange(startRow + i, 8).setValue(location[4]); // ASN
  }
}

function GET_LOCATION(ip) {
  var url = 'https://ipinfo.io/' + ip + '/json?token=xxxxx';
  var response = UrlFetchApp.fetch(url);
  var json = JSON.parse(response.getContentText());
  var orgParts = json.org ? json.org.split(' ') : ['', ''];
  var asnNumber = orgParts[0].replace('AS', ''); // Extract ASN number
  var ispName = orgParts.slice(1).join(' '); // Extract ISP name (without ASN)
  return [json.country, json.region, json.city, ispName, asnNumber];
}
