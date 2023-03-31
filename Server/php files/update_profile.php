<?php
$id = $_POST['id'];
$apiKey = $_POST['apiKey'];
$username = $_POST['username'];
$name = $_POST['name'];
$email = $_POST['email'];        
$isTrainer = $_POST['isTrainer'];
$conn = mysqli_connect("localhost", "root", "FitnessPassword@123", "ml_fitness"); //connect
$sql = "SELECT user_id, api_key from user where (user_id = '".$id."' and api_key = '".$apiKey."');";
$res = mysqli_query($conn, $sql);
if(mysqli_num_rows($res) != 0){
    $row = mysqli_fetch_assoc($res);
    if(!empty($_POST['old_password'])){
        if(password_verify($_POST['old_password'], $row["password"])){
            if($_POST['new_password']){
	        $newPassword = password_hash($_POST['new_password'], PASSWORD_DEFAULT);
            $sql = "UPDATE user SET username = '".$username."', name = '".$name."', email = '".$email."', password = '".$newPassword."' WHERE user_id = '".$id."';";
            $res = mysqli_query($conn, $sql); 
            echo "success";
            }else{
                $sql = "UPDATE user SET username = '".$username."', name = '".$name."', email = '".$email."' WHERE user_id = '".$id."';";
                $res = mysqli_query($conn, $sql); 
                echo "success";
            }
        }else{
            echo "Wrong Password";
        }
    }else{
	    echo "No Password";
    }
}else{
    echo "An Error Ocurred";
}