<?php
require('fpdf.php');

$pdo = new PDO(
    "mysql:host=sql113.infinityfree.com;dbname=if0_41226934_gossipdb;charset=utf8",
    "if0_41226934",
    "bathrooM09"
);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


/* =======================
   GENERATE PDF FUNCTIONS
======================= */
function headerPDF($pdf,$title){
    $pdf->AddPage();
    $pdf->SetFont('Arial','B',16);
    $pdf->Cell(0,10,$title,0,1);
    $pdf->Ln(5);
}


/* =======================
   ALL PEOPLE PDF
======================= */
if(isset($_GET['pdf_people'])){

    $pdf = new FPDF();
    headerPDF($pdf,"ALL PEOPLE REPORT");

    $people = $pdo->query("SELECT * FROM people")->fetchAll();

    foreach($people as $p){
        $pdf->SetFont('Arial','B',12);
        $pdf->Cell(0,8,$p['name']." ".$p['surname'],0,1);
        $pdf->SetFont('Arial','',11);
        $pdf->MultiCell(0,8,"DOB: ".$p['dob']." | Address: ".$p['address']);
        $pdf->MultiCell(0,8,"History: ".$p['history']);
        $pdf->Ln(5);
    }

    $pdf->Output();
    exit;
}


/* =======================
   ALL RELATIONSHIPS PDF
======================= */
if(isset($_GET['pdf_relationships'])){

    $pdf = new FPDF();
    headerPDF($pdf,"ALL RELATIONSHIPS REPORT");

    $rels = $pdo->query("
        SELECT r.*, 
        p1.name AS p1name, p1.surname AS p1surname,
        p2.name AS p2name, p2.surname AS p2surname
        FROM relationships r
        JOIN people p1 ON r.person1 = p1.personid
        JOIN people p2 ON r.person2 = p2.personid
    ")->fetchAll();

    foreach($rels as $r){
        $pdf->SetFont('Arial','B',12);
        $pdf->Cell(0,8,$r['p1name']." ".$r['p1surname']." & ".$r['p2name']." ".$r['p2surname'],0,1);
        $pdf->SetFont('Arial','',11);
        $pdf->MultiCell(0,8,"Start: ".$r['start_date']." | End: ".$r['end_date']);
        $pdf->MultiCell(0,8,"Stage: ".$r['relstage']);
        $pdf->MultiCell(0,8,"History: ".$r['relhistory']);
        $pdf->Ln(5);
    }

    $pdf->Output();
    exit;
}


/* =======================
   EVERYTHING PDF
======================= */
if(isset($_GET['pdf_all'])){

    $pdf = new FPDF();
    headerPDF($pdf,"FULL DATABASE REPORT");

    /* PEOPLE */
    $people = $pdo->query("SELECT * FROM people")->fetchAll();

    foreach($people as $p){
        $pdf->SetFont('Arial','B',14);
        $pdf->Cell(0,8,$p['name']." ".$p['surname'],0,1);
        $pdf->SetFont('Arial','',11);
        $pdf->MultiCell(0,8,"DOB: ".$p['dob']." | Address: ".$p['address']);
        $pdf->MultiCell(0,8,"History: ".$p['history']);

        /* GOSSIP */
        $gossips = $pdo->prepare("SELECT * FROM gossip_entries WHERE personid=?");
        $gossips->execute([$p['personid']]);

        foreach($gossips as $g){
            $pdf->SetFont('Arial','B',11);
            $pdf->Cell(0,8,"GOSSIP: ".$g['title'],0,1);
            $pdf->SetFont('Arial','',10);
            $pdf->MultiCell(0,8,$g['content']);
        }

        $pdf->Ln(8);
    }

    $pdf->Output();
    exit;
}

echo "<h1>ADMIN REPORT PANEL</h1>";
echo "<a href='?pdf_people=1'>📄 Print ALL People</a><br><br>";
echo "<a href='?pdf_relationships=1'>📄 Print ALL Relationships</a><br><br>";
echo "<a href='?pdf_all=1'>📄 Print EVERYTHING</a><br><br>";

echo "<hr>";

echo "<h2>All People</h2>";
$people = $pdo->query("SELECT * FROM people")->fetchAll();
foreach($people as $p){
    echo $p['name']." ".$p['surname']."<br>";
}

echo "<h2>All Relationships</h2>";
$rels = $pdo->query("
    SELECT r.*, 
    p1.name AS p1name, p1.surname AS p1surname,
    p2.name AS p2name, p2.surname AS p2surname
    FROM relationships r
    JOIN people p1 ON r.person1 = p1.personid
    JOIN people p2 ON r.person2 = p2.personid
")->fetchAll();

foreach($rels as $r){
    echo $r['p1name']." & ".$r['p2name']."<br>";
}
?>