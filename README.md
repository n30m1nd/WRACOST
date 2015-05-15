# WRACOST
Web Race Condition &amp; Stress Tester

### Usage
* Help: python wracost.py --help
* Test against url: python wracost.py http://url.to.test[:8080/path?with=params] number_of_threads verbosity_level
  * Example:**python wracost.py http://localhost:1234/wracost.php?coupon=QWE123 10 -vv**

### TODO
* Add SSL support
* Implement *param* and *payload* command line arguments
* Write a good readme
