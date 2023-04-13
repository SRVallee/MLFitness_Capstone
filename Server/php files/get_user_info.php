<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$user_id = $_POST["id2"];
$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
$sql = "SELECT user_id, api_key from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $sql = "SELECT * FROM user WHERE user_id = ".$user_id.";";
    $res = mysqli_query($conn, $sql);
    if(mysqli_num_rows($res) != 0){
        $row = mysqli_fetch_assoc($res);
    
        $result = array("status" => "success", 
        "username" => $row["username"],
        "name" => $row["name"],
        "isTrainer" => $row["is_trainer"]);
    }else{
        $result = array("status" => "User not found");
    }
}else{
    $result = array("status" => "Denied");
}

echo json_encode($result, JSON_PRETTY_PRINT);