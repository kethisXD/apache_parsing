
path_log_config = [ "/var/log/apache2/access.log", "/var/log/apache2/access.log.1" ]
pattern_config = r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\]'
user_db = {
    'host' : 'localhost',
    'user': 'qwe',
    'password': '11111111',
    'database': 'apache_parsing'
}
last_check_date = {"date_check": None}
