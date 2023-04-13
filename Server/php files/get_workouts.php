<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$user_id = $_POST["user_id"];
$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
$sql = "SELECT user_id, api_key from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $sql = "SELECT workout_id, user_user_id, exercise_exercise_id, score, date FROM workout WHERE user_user_id = ".$user_id.";";
    $res = mysqli_query($conn, $sql);
    $array = array();
    while($row = mysqli_fetch_assoc($res)){
        $array[] = $row;        
    }
    $result = array("status" => "success", "workouts" => $array);

}else{
    $result = array("status" => "Denied");
}

echo json_encode($result, JSON_PRETTY_PRINT);