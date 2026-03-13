<?php
session_start();

/* =========================
   AUTH CHECK
========================= */
if (!isset($_SESSION['username']) || !isset($_SESSION['perms'])) {
    header("Location: /app/auth/login.php");
    exit;
}

$user_perm = (int)$_SESSION['perms'];

if ($user_perm < 5) {
    die("Not Found or Insufficient Permissions");
}

/* =========================
   DATABASE
========================= */
$pdo = new PDO(
    "mysql:host=sql113.infinityfree.com;dbname=if0_41226934_gossipdb;charset=utf8",
    "if0_41226934",
    "bathrooM09"
);
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


/* =========================
   SEARCH PERSON
========================= */
if (isset($_GET['search'])) {

    $search = "%" . $_GET['search'] . "%";

    $stmt = $pdo->prepare("
        SELECT * FROM people
        WHERE (name LIKE ? OR surname LIKE ?)
        AND perms <= ?
    ");
    $stmt->execute([$search,$search,$user_perm]);

    $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
}


/* =========================
   LOAD PERSON DATA
========================= */
if (isset($_GET['edit'])) {

    $personid = (int)$_GET['edit'];

    $stmt = $pdo->prepare("SELECT * FROM people WHERE personid=? AND perms <= ?");
    $stmt->execute([$personid,$user_perm]);
    $person = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$person) {
        die("Not Found or Insufficient Permissions");
    }

    /* GOSSIP */
    $stmt = $pdo->prepare("SELECT * FROM gossip_entries WHERE personid=? AND perms <= ?");
    $stmt->execute([$personid,$user_perm]);
    $gossips = $stmt->fetchAll(PDO::FETCH_ASSOC);

    /* RELATIONSHIPS */
    $stmt = $pdo->prepare("
        SELECT r.*, 
        p1.name AS p1name, p2.name AS p2name
        FROM relationships r
        JOIN people p1 ON r.person1 = p1.personid
        JOIN people p2 ON r.person2 = p2.personid
        WHERE (r.person1=? OR r.person2=?)
        AND r.perms <= ?
    ");
    $stmt->execute([$personid,$personid,$user_perm]);
    $relationships = $stmt->fetchAll(PDO::FETCH_ASSOC);
}


/* =========================
   SAVE UPDATES
========================= */
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $personid = (int)$_POST['personid'];

    // Update Person
    $stmt = $pdo->prepare("
        UPDATE people
        SET name=?, surname=?, dob=?, address=?, history=?, perms=?
        WHERE personid=? AND perms <= ?
    ");
    $stmt->execute([
        $_POST['name'],
        $_POST['surname'],
        $_POST['dob'],
        $_POST['address'],
        $_POST['history'],
        $_POST['perms'],
        $personid,
        $user_perm
    ]);

    // Update Gossip
    if (isset($_POST['gossip'])) {
        foreach ($_POST['gossip'] as $gid => $data) {

            $stmt = $pdo->prepare("
                UPDATE gossip_entries
                SET title=?, content=?, gossip_date=?, perms=?
                WHERE gossipid=? AND perms <= ?
            ");
            $stmt->execute([
                $data['title'],
                $data['content'],
                $data['gossip_date'],
                $data['perms'],
                $gid,
                $user_perm
            ]);
        }
    }

    // Update Relationships
    if (isset($_POST['relationship'])) {
        foreach ($_POST['relationship'] as $rid => $data) {

            $stmt = $pdo->prepare("
                UPDATE relationships
                SET start_date=?, end_date=?, relstage=?, relquicknotes=?, relhistory=?, perms=?
                WHERE relid=? AND perms <= ?
            ");
            $stmt->execute([
                $data['start_date'],
                $data['end_date'],
                $data['relstage'],
                $data['relquicknotes'],
                $data['relhistory'],
                $data['perms'],
                $rid,
                $user_perm
            ]);
        }
    }

    echo "<p style='color:green;'>Changes Saved Successfully</p>";
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Editor</title>
<style>
body { font-family: Arial; margin:40px; }
.card { border:1px solid #ccc; padding:15px; margin:15px 0; border-radius:8px; }
input, textarea { width:100%; margin-bottom:10px; }
</style>
</head>
<body>

<h2>Editor Panel</h2>

<!-- SEARCH -->
<form method="GET">
<input type="text" name="search" placeholder="Search person">
<button type="submit">Search</button>
</form>

<?php
if (isset($results)) {
    foreach ($results as $row) {
        echo "<div class='card'>";
        echo $row['name']." ".$row['surname'];
        echo " <a href='?edit=".$row['personid']."'>Edit</a>";
        echo "</div>";
    }
}
?>

<?php if (isset($person)): ?>
<hr>
<form method="POST">
<input type="hidden" name="personid" value="<?php echo $person['personid']; ?>">

<h3>Person Info</h3>
Name: <input name="name" value="<?php echo htmlspecialchars($person['name']); ?>">
Surname: <input name="surname" value="<?php echo htmlspecialchars($person['surname']); ?>">
DOB: <input name="dob" value="<?php echo $person['dob']; ?>">
Address: <input name="address" value="<?php echo htmlspecialchars($person['address']); ?>">
History: <textarea name="history"><?php echo htmlspecialchars($person['history']); ?></textarea>
Permission Level: <input type="number" name="perms" value="<?php echo $person['perms']; ?>">

<h3>Gossip Entries</h3>
<?php foreach ($gossips as $g): ?>
<div class="card">
Title: <input name="gossip[<?php echo $g['gossipid']; ?>][title]" value="<?php echo htmlspecialchars($g['title']); ?>">
Date: <input name="gossip[<?php echo $g['gossipid']; ?>][gossip_date]" value="<?php echo $g['gossip_date']; ?>">
Content:
<textarea name="gossip[<?php echo $g['gossipid']; ?>][content]"><?php echo htmlspecialchars($g['content']); ?></textarea>
Permission Level:
<input type="number" name="gossip[<?php echo $g['gossipid']; ?>][perms]" value="<?php echo $g['perms']; ?>">
</div>
<?php endforeach; ?>

<h3>Relationships</h3>
<?php foreach ($relationships as $rel): ?>
<div class="card">
<strong><?php echo $rel['p1name']; ?> & <?php echo $rel['p2name']; ?></strong><br>
Start: <input name="relationship[<?php echo $rel['relid']; ?>][start_date]" value="<?php echo $rel['start_date']; ?>">
End: <input name="relationship[<?php echo $rel['relid']; ?>][end_date]" value="<?php echo $rel['end_date']; ?>">
Stage: <input name="relationship[<?php echo $rel['relid']; ?>][relstage]" value="<?php echo htmlspecialchars($rel['relstage']); ?>">
Quick Notes:
<textarea name="relationship[<?php echo $rel['relid']; ?>][relquicknotes]"><?php echo htmlspecialchars($rel['relquicknotes']); ?></textarea>
History:
<textarea name="relationship[<?php echo $rel['relid']; ?>][relhistory]"><?php echo htmlspecialchars($rel['relhistory']); ?></textarea>
Permission Level:
<input type="number" name="relationship[<?php echo $rel['relid']; ?>][perms]" value="<?php echo $rel['perms']; ?>">
</div>
<?php endforeach; ?>

<button type="submit">Save All Changes</button>
</form>
<?php endif; ?>

</body>
</html>