<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$workout_id["workout_id"];

$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
$sql = "SELECT user_id, api_key from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $sql = "SELECT * FROM feedback WHERE workout_workout_id = ".$workout_id.";";
    $res = mysqli_query($conn, $sql);
    if(mysqli_num_rows($res) != 0){
        $row = mysqli_fetch_assoc($res);
        $result = array("status" => "success", "feedback" => $row);
    }else{
        $result = array("status" => "No feedback yet");
    }
}else{
    $result = array("status" => "Denied");
}

echo json_encode($result, JSON_PRETTY_PRINT);