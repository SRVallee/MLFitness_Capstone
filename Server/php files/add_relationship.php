<?php
$id = $_POST['id'];
$id2 = $_POST['id2'];
$apiKey = $_POST['apiKey'];
$subscription = $_POST["type"]; //0 for friends, 1 for trainer/trinee relationship

if($id == $id2){
    echo "can't add yourself";
}else{
    $conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
    $sql = "SELECT user_id, api_key from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
    $res = mysqli_query($conn, $sql);
    if(mysqli_num_rows($res) == 2){
        $row = mysqli_fetch_assoc($res);
        $row2 = mysqli_fetch_assoc($res);
        $sql = "SELECT * FROM relationships WHERE (user_id = ".$id." and user_id_2 = ".$id2.") or (user_id = ".$id2." and user_id_2 = ".$id.");";
        $res = mysqli_query($conn, $sql);
        if(mysqli_num_rows($res) != 0){  // If relationship existed before
            $sql = "UPDATE relationships SET end_date = ".date('Y-m-d').";";
            mysqli_query($conn, $sql);
            echo "success";
        }else{                          //else make new one
            $sql = "INSERT INTO relationships(user_id, user_id_2, log_location, training_relationship, start_date) values(".$id.", ".$id2.", 'none', ".$subscription.", ".date('Y-m-d').");";
            mysqli_query($conn, $sql);
            echo "success";
        }
    }
    echo "Failed to subscribe";
}