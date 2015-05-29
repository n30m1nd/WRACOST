# WRACOST
Web Race Condition &amp; Stress Tester

### Usage
* **RUN THE HELP COMMAND**: python wracost.py --help
* Test url: python wracost.py http://url.to.test[:8080/path?with=params] METHOD number_of_threads verbosity_level
  * Example:**python wracost.py http://localhost:1234/wracost.php?coupon=QWE123 GET 10 -vv**
  * Example:**python wracost.py http://localhost:1234/wracost.php --params foo bar red --payloads 1:f 1:more 2:b 3:r 3:params**
* See "__main__" in some files to get more info for now

### TODO
* Add SSL support
* Write a good readme
