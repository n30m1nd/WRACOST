<?php
/****************************************************************
 * Test 2: Race condition in a voting system                    *
 * ------------------------------------------------------------ *
 * This test will use the visitor IP to prevent multiple votes  *
 * from the same user, emulating the behaviour of a database    *
 *                                                              *
 * WRACOST Testing command:                                     *
 * wracost.py http://localhost:80/testcases/wracost_test_2.php  *
 *              POST -p band -y 0:opt1 0:opt2 0:opt2 0:opt3     *
 ****************************************************************
 */
 $data_folder = "./data/test2_voting/";
 
?>

<html>
<head><title>Test Case 2</head></title>
<body>
    <?php
    if (!empty($_POST)){
        if (file_exists($data_folder."localhost")){
            echo 'Sorry, you can vote more than once...<br />'; // No missing ['t] here ;)
        } else {
            // This way we simulate what could happen in a real database
            // We need FILE_APPEND in case all request arrived here, but we still want to see
            // the outcome of our multiple requests with different "band" option set
            file_put_contents($data_folder."localhost", 'voted:'.$_POST['band']."\n", FILE_APPEND);
        }
    }
    ?>
    <form method="post">
            <fieldset>
                    <legend>Who's your favourite band?</legend>
                            <input type="radio" name="band" value="opt1" />2Pc SHACurl<br />
                            <input type="radio" name="band" value="opt2" />Dual Core<br />
                            <input type="radio" name="band" value="opt3" />Slip\x90<br />
							<br />
                            <input type="submit" value="Submit vote" />
            </fieldset>
    </form>
</body>
</html>