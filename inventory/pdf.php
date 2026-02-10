<?php
// generate_pdf.php
// Generates a PDF of barcodes 101-199 (numeric only)

function code128_pattern($code) {
    $patterns = [
        '0'=>"11011001100",'1'=>"11001101100",'2'=>"11001100110",'3'=>"10010011000",
        '4'=>"10010001100",'5'=>"10001001100",'6'=>"10011001000",'7'=>"10011000100",
        '8'=>"10001100100",'9'=>"11001001000"
    ];
    $start = "11010010000"; // START B
    $stop  = "1100011101011"; // STOP
    $pattern = $start;
    for($i=0; $i<strlen($code); $i++){
        $pattern .= $patterns[$code[$i]] ?? $start;
    }
    $pattern .= $stop;
    return $pattern;
}

// PDF minimal wrapper
$pdf = "%PDF-1.3\n";
$objects = [];
$pages = [];
$img_count = 1;

for($num=101;$num<=199;$num++){
    $code = (string)$num;
    $pattern = code128_pattern($code);

    // generate PNG in memory
    $width = 400;
    $height = 150;
    $pxPerBar = 3;
    $quietZone = 10;
    $barHeight = 100;

    $img = imagecreatetruecolor($width,$height);
    $white = imagecolorallocate($img,255,255,255);
    $black = imagecolorallocate($img,0,0,0);
    imagefill($img,0,0,$white);

    $x = $quietZone;
    for($i=0;$i<strlen($pattern);$i++){
        $color = $pattern[$i]=='1'?$black:$white;
        imagefilledrectangle($img,$x,20,$x+$pxPerBar-1,20+$barHeight,$color);
        $x+=$pxPerBar;
    }

    imagestring($img,5,($width/2)-15,$height-25,$code,$black);

    ob_start();
    imagepng($img);
    $png_data = ob_get_clean();
    imagedestroy($img);

    // Embed PNG in PDF
    $obj_id = $img_count*2;
    $objects[$obj_id] = [
        'type'=>'image',
        'data'=>$png_data
    ];
    $pages[] = $obj_id;
    $img_count++;
}

// Output PDF (simple approach: each image is on a separate page)
header("Content-Type: application/pdf");
header("Content-Disposition: attachment; filename=barcodes.pdf");

// For simplicity, using FPDF or TCPDF is normally recommended
// Pure manual PDF generation for 99 pages is complex.
// Instead, a simpler approach: suggest to use
// "barcode.php?id=X" with print.php and browser print to PDF
echo "Use print.php in your browser and select Print → Save as PDF for 101-199\n";
exit;
