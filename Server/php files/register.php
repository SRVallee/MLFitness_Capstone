<?php
$conn = mysqli_connect("localhost", "root", "", "ml_fitness");
$username = $_POST['username'];
$name = $_POST['name'];
$email = $_POST['email'];
$password = password_hash($_POST['password'], PASSWORD_DEFAULT);
$isTrainer = $_POST['isTrainer'];
if($conn){
    //TODO: Check if email already in database
    $sql = "insert into user(user_id, username, password, name, email, is_trainer) values(default,'".$username."','".$password."','".$name."','".$email."','".$isTrainer."');";
    if(mysqli_query($conn, $sql)){
        $sql = "select * from user where email = '".$email."'";
        $res = mysqli_query($conn, $sql);
        if(mysqli_num_rows($res) != 0){                               //if user exists      
            $row = mysqli_fetch_assoc($res);
            echo $row["user_id"];
        }
    }
}

else echo "Connection to database failed";