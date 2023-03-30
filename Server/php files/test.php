<?php
$command = escapeshellcmd("python3 /home/ubuntu/CapstoneFiles/MLFitness_Capstone/Server/ComputerVision/hello.py");
$output = shell_exec($command);
echo $output;