<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
$sql = "SELECT user_id, api_key from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $sql = "SELECT * from relationships WHERE user_id = (".$id." or user_id_2 = ".$id.") and training_relationship = 1;";
    $res = mysqli_query($conn, $sql);
    $array = [];
    while($row = mysqli_fetch_assoc($res)){
        if ($row["user_id"] == $id){
            $array[] = $row["user_id_2"];
        }else{
            $array[] = $row["user_id"];
        }
    }
    $result = array("status" => "success", "trainers" => $array);
}else{
    $result = array("status" => "Denied");
}

echo json_encode($result, JSON_PRETTY_PRINT);