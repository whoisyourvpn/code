<?php
$servername = "localhost";
$username = "user";
$password = "pass";
$dbname = "db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

$ip = $conn->real_escape_string($_GET['ip']);

$sql = "SELECT ipdb.IP, ipdb.VPN, ipdb.Hostname, ipdb.Country, ipdb.Region, ipdb.City, ipdb.ISP, ipdb.ASN, vpndata.VPN_LOGO, vpndata.VPN_DESC, countrydata.country_url 
        FROM ipdb 
        INNER JOIN vpndata ON ipdb.VPN_ID = vpndata.VPN_ID 
        LEFT JOIN countrydata ON ipdb.country_id = countrydata.country_id
        WHERE ipdb.IP = '$ip'";

$result = $conn->query($sql);

$data = [];
if ($result->num_rows > 0) {
  // Fetch all rows into the data array
  while($row = $result->fetch_assoc()) {
    $data[] = $row;
  }
}
?>

<?php
if (!empty($data)) {
  foreach ($data as $row) {
    echo '<table class="tg">
    <thead>
      <tr>
        <td class="tg-0lax" rowspan="3"><img src="'.$row["VPN_LOGO"].'" width="75" height="75"></td>
        <td class="tg-0lax"><h2>'.$row["IP"].'</h2><p>'.$row["VPN_DESC"].'</p></td>
      </tr>
      <tr>
        <td class="tg-0lax">
        <ul class="details">';
    if (!empty($row["ASN"])) {
        echo '<li><a href="https://mywebsite.com/asn/'.$row["ASN"].'">'.$row["ASN"].'</a></li>';
    }
    if (!empty($row["ISP"])) {
        echo '<li>'.$row["ISP"].'</li>';
    }
if (!empty($row["Country"])) {
    echo '<li><a href="'.$row["country_url"].'">'.$row["Country"].'</a></li>';
}
    if (!empty($row["Region"])) {
        echo '<li>'.$row["Region"].'</li>';
    }
    if (!empty($row["City"])) {
        echo '<li>'.$row["City"].'</li>';
    }
    echo '</ul>
        </td>
      </tr>
    </thead>
    </table>';
  }
} else {
  echo "0 results";
}
?>

<form id="ipForm">
    Enter IP: <input type="text" id="ipInput">
    <input type="submit" value="Submit">
</form>

<?php 
if (!empty($_GET['ip'])) {
    include 'related.php'; 
}
$conn->close();
?>


<script>
    function isValidIP(ip) {
        // This regular expression checks for four sets of one to three digits, separated by periods
        var ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        return ipRegex.test(ip);
    }

    document.getElementById('ipForm').addEventListener('submit', function(event) {
        event.preventDefault();
        var ip = document.getElementById('ipInput').value;

        // Check if the IP address is valid before redirecting
        if (isValidIP(ip)) {
            location.href = '/ip/' + encodeURIComponent(ip);
        } else {
            alert('Please enter a valid IP address');
        }
    });
</script>
