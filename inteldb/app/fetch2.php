<?php
session_start();

// =========================
// SESSION CHECK
// =========================
if (!isset($_SESSION['username']) || !isset($_SESSION['perms'])) {
    header("Location: /app/auth/login.php");
    exit;
}

$user_perm = (int)$_SESSION['perms'];

// =========================
// DATABASE CONNECTION
// =========================
$pdo = new PDO(
    "mysql:host=sql113.infinityfree.com;dbname=if0_41226934_gossipdb;charset=utf8",
    "if0_41226934",
    "bathrooM09"
);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// =========================
// ERROR / DENY FUNCTION
// =========================
function deny($message = "Information not available or insufficient auth level"){
    echo "<p style='color:red; font-weight:bold;'>$message</p>";
    exit;
}

// =========================
// SAFE PERMISSION WRAPPER
// =========================
function safePerm($value){
    return isset($value) ? (int)$value : 0;
}

// =========================
// AJAX LIVE SEARCH
// =========================
if(isset($_GET['ajax_search'])){
    $search = "%".$_GET['ajax_search']."%";

    if($user_perm == 9){
        $stmt = $pdo->prepare("SELECT personid,name,surname FROM people WHERE name LIKE ? OR surname LIKE ? LIMIT 10");
        $stmt->execute([$search,$search]);
    } else {
        $stmt = $pdo->prepare("
            SELECT personid,name,surname FROM people
            WHERE (name LIKE ? OR surname LIKE ?)
            AND IFNULL(perms,0) <= ?
            AND IFNULL(perms,0) != 9
            LIMIT 10
        ");
        $stmt->execute([$search,$search,$user_perm]);
    }

    echo json_encode($stmt->fetchAll(PDO::FETCH_ASSOC));
    exit;
}
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Gossip Database</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background:#f5f5f5; color:#333; }
        h1, h2, h3 { color:#222; }
        .card { background:white; border-radius:8px; padding:12px; margin:10px 0; box-shadow:0 2px 5px rgba(0,0,0,0.1);}
        button { margin:5px 5px 5px 0; padding:8px 12px; border:none; border-radius:5px; cursor:pointer; background:#007BFF; color:white;}
        button:hover { background:#0056b3;}
        input[type=text] { padding:8px; width:300px; border-radius:5px; border:1px solid #ccc; margin-bottom:10px;}
        a { text-decoration:none; color:#007BFF; }
        a:hover { text-decoration:underline; }
        hr { margin:20px 0; border:none; border-top:1px solid #ccc; }
    </style>
</head>
<body>

<h1>Gossip Database</h1>

<?php
$perm_labels = [
    0 => "Public Domain",
    1 => "Token Required",
    2 => "Token Required",
    3 => "Year 11",
    4 => "Year 12",
    5 => "Full ICS Database Access",
    6 => "Full Relationships Access",
    7 => "Concern Privacy Clearance",
    8 => "Top Clearance",
    9 => "Administrator"
];
?>

<p>
Logged in as: <strong><?php echo htmlspecialchars($_SESSION['username']); ?></strong><br>
Permission Level: <?php echo $user_perm; ?><br>
Access Level: <?php echo $perm_labels[$user_perm] ?? "Unknown"; ?>
</p>

<hr>

<button onclick="location.href='/app/new.php'">New Entry</button>
<?php if($user_perm >= 7): ?><button onclick="location.href='/app/editor.php'">Editor Panel</button><?php endif; ?>
<?php if($user_perm >= 8): ?><button onclick="location.href='/app/reportswizard.php'">Reports Wizard</button><?php endif; ?>

<hr>

<input type="text" id="liveSearch" placeholder="Search people...">
<div id="results"></div>

<script>
document.getElementById("liveSearch").addEventListener("keyup", function(){
    let query = this.value;
    if(query.length < 2){
        document.getElementById("results").innerHTML = "";
        return;
    }
    fetch("?ajax_search=" + encodeURIComponent(query))
        .then(res => res.json())
        .then(data => {
            let html = "";
            data.forEach(person => {
                html += `<div class='card'>
                            ${person.name} ${person.surname}
                            <a href='?view=${person.personid}'>View</a>
                         </div>`;
            });
            document.getElementById("results").innerHTML = html;
        });
});
</script>

<?php
// =========================
// PROFILE VIEW
// =========================
if(isset($_GET['view'])){

    $personid = (int)$_GET['view'];

    $stmt = $pdo->prepare("SELECT * FROM people WHERE personid=? AND IFNULL(perms,0) <= ?");
    $stmt->execute([$personid,$user_perm]);
    $person = $stmt->fetch();
    if(!$person) deny();

    echo "<hr><h2>".htmlspecialchars($person['name'])." ".htmlspecialchars($person['surname'])."</h2>";
    echo "<p>DOB: ".$person['dob']."</p>";
    echo "<p>Address: ".$person['address']."</p>";
    echo "<p>History: ".$person['history']."</p>";

    // =========================
    // RELATIONSHIPS (VISIBLE BASED ON CURRENT USER PERM)
    // =========================
    $stmt = $pdo->prepare("
        SELECT r.*, 
               p1.name AS p1name, p1.surname AS p1surname,
               p2.name AS p2name, p2.surname AS p2surname
        FROM relationships r
        JOIN people p1 ON r.person1 = p1.personid
        JOIN people p2 ON r.person2 = p2.personid
        WHERE (r.person1=? OR r.person2=?)
        AND IFNULL(r.perms,0) <= ?
    ");
    $stmt->execute([$personid,$personid,$user_perm]);
    $relationships = $stmt->fetchAll();

    echo "<h3>Relationships</h3>";
    if($relationships){
        foreach($relationships as $rel){
            echo "<div class='card'>";
            echo $rel['p1name']." ".$rel['p1surname']." & ".$rel['p2name']." ".$rel['p2surname']."<br>";
            echo "Start: ".$rel['start_date']." | End: ".$rel['end_date']."<br>";
            echo "<a href='?relationship=".$rel['relid']."'>View Full Relationship</a>";
            echo "</div>";
        }
    } else {
        echo "<p style='color:#666;'>No visible relationships.</p>";
    }

    // =========================
    // GOSSIP ENTRIES
    // =========================
    $stmt = $pdo->prepare("SELECT * FROM gossip_entries WHERE personid=? AND IFNULL(perms,0) <= ? ORDER BY gossip_date DESC");
    $stmt->execute([$personid,$user_perm]);
    $gossips = $stmt->fetchAll();

    echo "<h3>Gossip Entries</h3>";
    if($gossips){
        foreach($gossips as $g){
            echo "<div class='card'>";
            echo "<strong>".htmlspecialchars($g['title'])."</strong><br>";
            echo "Date: ".$g['gossip_date']."<br><br>";
            echo nl2br(htmlspecialchars($g['content']));
            echo "</div>";
        }
    } else {
        echo "<p style='color:#666;'>No visible gossip entries.</p>";
    }
}

// =========================
// FULL RELATIONSHIP VIEW
// =========================
if(isset($_GET['relationship'])){
    $relid = (int)$_GET['relationship'];
    $stmt = $pdo->prepare("
        SELECT r.*, 
               p1.name AS p1name, p1.surname AS p1surname,
               p2.name AS p2name, p2.surname AS p2surname
        FROM relationships r
        JOIN people p1 ON r.person1 = p1.personid
        JOIN people p2 ON r.person2 = p2.personid
        WHERE r.relid=? AND IFNULL(r.perms,0) <= ?
    ");
    $stmt->execute([$relid,$user_perm]);
    $rel = $stmt->fetch();
    if(!$rel) deny();

    echo "<hr><h2>Relationship Details</h2>";
    echo "<p><strong>".$rel['p1name']." ".$rel['p1surname']." & ".$rel['p2name']." ".$rel['p2surname']."</strong></p>";
    echo "<p>Start Date: ".$rel['start_date']."</p>";
    echo "<p>End Date: ".$rel['end_date']."</p>";
    echo "<p>Stage: ".$rel['relstage']."</p>";
    echo "<p>Quick Notes: ".$rel['relquicknotes']."</p>";
    echo "<p>History: ".$rel['relhistory']."</p>";
}
?>
</body>
</html>