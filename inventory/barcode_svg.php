<?php
$code = (string)($_GET['code'] ?? '');

header("Content-Type: image/svg+xml");

$barWidth = 2;
$height = 60;
$x = 10;

echo '<svg xmlns="http://www.w3.org/2000/svg" height="'.$height.'">';

foreach (str_split($code) as $char) {
    $bars = ord($char) % 2 ? 4 : 2;
    echo "<rect x='$x' y='0' width='".($bars * $barWidth)."' height='$height' fill='black'/>";
    $x += ($bars * $barWidth) + 2;
}

echo '</svg>';
