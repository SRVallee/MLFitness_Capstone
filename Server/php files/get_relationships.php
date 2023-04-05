<?php
$id = $_POST['id'];
$id2 = $_POST['id2'];
$apiKey = $_POST['apiKey'];
$type = $_POST["type"]; //0 friends, 1 trainers/trainees, 2 both

$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
if($id == $id2){
    $sql = "SELECT user_id, api_key from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
}else{
    $sql = "SELECT user_id, api_key from user where (user_id = '".$id."' and api_key = '".$apiKey."') or user_id = ".$id2.";";
    }
$res = mysqli_query($conn, $sql);
if((mysqli_num_rows($res) == 2 && $id != $id2) || (mysqli_num_rows($res) == 1 && $id == $id2)){
    if($type == 0 or $type == 1){
        $sql = "SELECT * from relationships WHERE (user_id = ".$id2." or user_id_2 = ".$id2.") and training_relationship = ".$type.";";
    }else{
        $sql = "SELECT * from relationships WHERE (user_id = ".$id2." or user_id_2 = ".$id2.");";
    }
    $res = mysqli_query($conn, $sql);
    $array = array();
    while($row = mysqli_fetch_assoc($res)){
        $array[] = $row;
    }
    $result = array("status" => "success", "relationships" => $array, "test" => $sql);
    
}else{
    $result = array("status" => "Denied");
}

echo json_encode($result, JSON_PRETTY_PRINT);