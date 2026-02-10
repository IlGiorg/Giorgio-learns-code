<?php
include "db.php";

$message = "";
$error = "";

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    try {
        if (!empty($_POST['cableid'])) {
            $stmt = $conn->prepare(
                "INSERT INTO cables (cableid, cabletype, cablebucket, cabledesc, cablestatus)
                 VALUES (?,?,?,?,?)"
            );
            $stmt->bind_param(
                "issss",
                $_POST['cableid'],
                $_POST['type'],
                $_POST['bucket'],
                $_POST['desc'],
                $_POST['status']
            );
        } else {
            $stmt = $conn->prepare(
                "INSERT INTO cables (cabletype, cablebucket, cabledesc, cablestatus)
                 VALUES (?,?,?,?)"
            );
            $stmt->bind_param(
                "ssss",
                $_POST['type'],
                $_POST['bucket'],
                $_POST['desc'],
                $_POST['status']
            );
        }

        $stmt->execute();
        $message = "✅ Cable added successfully";
    } catch (mysqli_sql_exception $e) {
        $error = "❌ Error: " . $e->getMessage();
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Add Cable</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f4f8;
        }

        .container {
            max-width: 500px;
            margin: 50px auto;
            background: #ffffff;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        h2 {
            text-align: center;
            margin-bottom: 20px;
        }

        label {
            font-weight: bold;
            display: block;
            margin-top: 12px;
        }

        input, select {
            width: 100%;
            padding: 8px;
            margin-top: 4px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }

        button {
            margin-top: 20px;
            width: 100%;
            padding: 10px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #0056b3;
        }

        .msg {
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 4px;
        }

        .success {
            background: #d4edda;
            color: #155724;
        }

        .error {
            background: #f8d7da;
            color: #721c24;
        }

        .back {
            text-align: center;
            margin-top: 15px;
        }

        .back a {
            color: #007bff;
            text-decoration: none;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Add New Cable (Bulk Mode)</h2>

    <?php if ($message): ?>
        <div class="msg success"><?= $message ?></div>
    <?php endif; ?>

    <?php if ($error): ?>
        <div class="msg error"><?= $error ?></div>
    <?php endif; ?>

    <form method="post">
        <label>Cable ID (optional)</label>
        <input type="number" name="cableid" value="">

        <label>Type</label>
        <select name="type">
            <option value="power">power</option>
            <option value="data">data</option>
            <option value="audio">audio</option>
            <option value="internet">internet</option>
        </select>

        <label>Bucket</label>
        <select name="bucket">
            <option value="audio">audio</option>
            <option value="usb">usb</option>
            <option value="power">power</option>
            <option value="gear">gear</option>
            <option value="circuits">circuits</option>
            <option value="gray1">gray 1</option>
            <option value="other/unsorted">other/unsorted</option>
        </select>

        <label>Status</label>
        <select name="status">
            <option value="in use">in use</option>
            <option value="borrowedbys">borrowedbys</option>
            <option value="borrowedbycv">borrowedbycv</option>
            <option value="stored">stored</option>
            <option value="unknown">unknown</option>
        </select>

        <label>Description</label>
        <input type="text" name="desc" maxlength="255">

        <button type="submit">Add Cable</button>
    </form>

    <div class="back">
        <a href="index.php">⬅ Back to inventory</a>
    </div>
</div>

</body>
</html>
