<?php
//TODO: set contents
$contents = file_get_contents('http://localhost:50030/pithy/members/q');
echo $_REQUEST['callback'] . "(" . $contents . ")";
?>
