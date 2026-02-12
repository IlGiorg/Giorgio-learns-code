<?php
// -----------------------------
// barcode.php
// Generates a scanner-readable Code128 barcode PNG
// -----------------------------

if (!isset($_GET['id']) || $_GET['id'] === '') {
    die("No ID provided");
}

$code = (string) $_GET['id'];

// -----------------------------
// Simple numeric Code128 patterns (subset B, for letters/numbers extend if needed)
// -----------------------------
$patterns = [
    '0'=>"11011001100",'1'=>"11001101100",'2'=>"11001100110",'3'=>"10010011000",
    '4'=>"10010001100",'5'=>"10001001100",'6'=>"10011001000",'7'=>"10011000100",
    '8'=>"10001100100",'9'=>"11001001000"
];

// START and STOP patterns
$start = "11010010000";  // START B
$stop  = "1100011101011";

// -----------------------------
// Build barcode pattern
// -----------------------------
$pattern = $start;
for($i=0; $i<strlen($code); $i++){
    $pattern .= $patterns[$code[$i]] ?? "11010010000"; // fallback
}
$pattern .= $stop;

// -----------------------------
// Settings
// -----------------------------
$width = 800;      // total width
$height = 200;     // total height
$pxPerBar = 4;     // width per module (scanner readable)
$quietZone = 20;   // left/right margin
$barHeight = 120;  // height of bars

// Create image
$img = imagecreatetruecolor($width, $height);
$white = imagecolorallocate($img, 255,255,255);
$black = imagecolorallocate($img, 0,0,0);
imagefill($img,0,0,$white);

// Draw bars
$x = $quietZone;
for($i=0; $i<strlen($pattern); $i++){
    $color = $pattern[$i] == '1' ? $black : $white;
    imagefilledrectangle($img, $x, 20, $x + $pxPerBar - 1, 20 + $barHeight, $color);
    $x += $pxPerBar;
}

// Draw human-readable text
imagestring($img, 5, ($width/2)-30, $height-30, $code, $black);

// Output PNG
header("Content-Type: image/png");
imagepng($img);
imagedestroy($img);
exit;
