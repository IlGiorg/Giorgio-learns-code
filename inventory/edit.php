<?php
include "db.php";

$id = $_GET['id'];

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $stmt = $conn->prepare(
        "UPDATE cables
         SET cabletype=?, cablebucket=?, cabledesc=?, cablestatus=?
         WHERE cableid=?"
    );
    $stmt->bind_param(
        "ssssi",
        $_POST['type'],
        $_POST['bucket'],
        $_POST['desc'],
        $_POST['status'],
        $id
    );
    $stmt->execute();
    header("Location: index.php");
}

$stmt = $conn->prepare("SELECT * FROM cables WHERE cableid=?");
$stmt->bind_param("i", $id);
$stmt->execute();
$cable = $stmt->get_result()->fetch_assoc();
?>

<!DOCTYPE html>
<html>
<head><title>Edit Cable</title></head>
<body>

<h2>Edit Cable #<?= $id ?></h2>

<form method="post">
    Type:
    <select name="type">
        <?php foreach (['power','data','audio','internet'] as $t): ?>
            <option <?= $cable['cabletype']==$t?'selected':'' ?>><?= $t ?></option>
        <?php endforeach; ?>
    </select><br><br>

    Bucket:
    <select name="bucket">
        <?php foreach (['audio','usb','power','gear','circuits'] as $b): ?>
            <option <?= $cable['cablebucket']==$b?'selected':'' ?>><?= $b ?></option>
        <?php endforeach; ?>
    </select><br><br>

    Status:
    <select name="status">
        <?php foreach (['in use','borrowedbys','borrowedbycv','unknown'] as $s): ?>
            <option <?= $cable['cablestatus']==$s?'selected':'' ?>><?= $s ?></option>
        <?php endforeach; ?>
    </select><br><br>

    Description:<br>
    <input type="text" name="desc" value="<?= htmlspecialchars($cable['cabledesc']) ?>" style="width:300px;"><br><br>

    <button type="submit">Save Changes</button>
</form>

<a href="index.php">⬅ Back</a>

</body>
</html>
