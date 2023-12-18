$portName = "COM3"

$serialPort = new-object System.IO.Ports.SerialPort $portName, 230400, None, 8, One
$serialPort.ReadTimeout = 2000
$serialPort.WriteTimeout = 1000

Function Send-Command($command) {
    $serialPort.DiscardInBuffer()  
    $serialPort.WriteLine($command + "`r")
    Start-Sleep -Milliseconds 1000 
}

try {
    $serialPort.Open()

    while ($true) {
        $colors = @(
            @{Name="Red";   Command="ir tx RAW F:38000 DC:33 9224 4565 621 533 620 533 621 533 618 533 619 532 621 532 620 532 593 558 616 1648 620 1648 619 1647 621 1646 619 532 620 1648 620 1648 619 1647 619 532 620 533 618 532 621 1647 619 533 621 533 618 531 621 532 619 1648 616 1647 614 1647 588 557 614 1647 617 1647 617 1646 618 1647 621 41223 9231 2275 616 96785 9166 2275 616 96777 9131 2275 614 96806 9121 2274 614 96858 9208 2282 618"},
            @{Name="Pink";  Command="ir tx RAW F:38000 DC:33 9245 4579 596 560 590 558 591 558 591 560 588 559 590 559 590 559 590 559 590 1680 591 1680 594 1679 591 1681 589 559 591 1680 592 1680 593 1680 593 1681 595 1681 594 560 594 559 595 1681 594 559 594 558 597 559 595 559 595 560 592 1681 591 1681 590 559 591 1681 590 1679 591 1681 590 41468 9159 2287 590 97307 9215 2286 595 97358 9268 2287 596 97293 9260 2288 595 97310 9243 2286 596 97293 9236 2288 593 97318 9237 2286 595 97320 9281 2286 598"},
            @{Name="Purple";Command="ir tx RAW F:38000 DC:33 9395 4581 602 559 600 560 606 561 604 560 604 557 608 561 609 562 606 561 608 1683 599 1678 601 1679 594 1678 592 557 591 1679 592 1678 597 1682 592 556 595 1678 594 556 594 557 593 1678 595 557 595 557 594 558 594 1678 604 559 601 1680 601 1679 601 560 599 1680 599 1679 595 1679 594 41501 9245 2288 597 97349 9296 2286 598"}
        )

        foreach ($color in $colors) {
            Send-Command $color.Command

            Write-Output ("Displaying " + $color.Name + " color. Next color shift in 15 minutes.")

            for ($i = 15; $i -gt 0; $i--) {
                Write-Output ("Time until next color shift: " + $i + " minutes remaining.")
                Start-Sleep -Seconds 60  
            }
        }
    }

} catch {
    Write-Error "Failed to communicate with the device on $portName"
} finally {
    if ($serialPort.IsOpen) {
        $serialPort.Close()
    }
}
