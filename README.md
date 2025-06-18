# Anarchy
**Anarchy** is an advanced multithreaded brute-forcer for web login forms.<br>
It supports `POST` and `GET` methods, custom parameter keys and multiple verbosity levels.<br>
Designed for penetration testing and research in ethical hacking environments.<br>

Current Version: **1.0 (Alpha Test)**

**!!!WARNING!!! The project is not finished.**

## DISCLAIMER
This tool is intended for **educational and authorized penetration testing** only. Unauthorized use against systems you do not own or have explicit permission to test is illegal.

## Features
- Supports `GET` and `POST` login methods
- Multi-threaded (default: 200 workers)
- Custom username/password parameter keys
- Custom "failure condition" string detection
- User-Agent randomization for stealth
- Bypass cookies and headers (optional)
- Retry mechanism for failed attempts
- Verbose logging with adjustable levels (`-v`, `-vv`, `-vvv`)

## Requirements
- Python 3.x
- requests
- socks
- argparse
- threading
- concurrect.futures

## Installation
```bash
git clone https://github.com/therustymate/Anarchy.git
cd Anarchy
pip install -r requirements.txt
```

## Usage
```bash
python Anarchy.py -t [TARGET] -u [USER] -l [PWD_LIST] -p [PARAM] -m [METHOD] -f [FAILED]
```

### Arguments
| Argument              | Description                                                   |
|:----------------------|:--------------------------------------------------------------|
| `-t`, `--target`      | Target login URL (e.g., http://example.com/login)             |
| `-u`, `--user`        | Username to brute force (e.g., root, admin)                   |
| `-l`, `--list`        | Path to password list (e.g. rockyou.txt)                      |
| `-p`, `--parameters`  | POST/GET parameters (e.g. username/password)                  |
| `-m`, `--method`      | HTTP method (`POST` or `GET`)                                 |
| `-f`, `--failed`      | Failure string to detect unsuccessful login (e.g. invalid)    |

### Optional Flags
| Flag             | Description                                        |
| ---------------- | -------------------------------------------------- |
| `-w`, `--worker` | Number of threads (default: 200)                   |
| `-v`             | Verbose logging (`-v`, `-vv`, `-vvv`)              |
| `--bypass`       | Bypass cookies and headers from initial response   |

## Example
```bash
python anarchy.py \
    -t http://localhost:8080/login \
    -u admin \
    -l passwords.txt \
    -p username/password \
    -m POST \
    -f "Login failed" \
    -w 300 -vv
```
Target: http://localhost:8080/login<br>
Uesrname: admin<br>
Password List: password.txt<br>
Parameters: username & password<br>
Method: POST<br>
Failed String: "Login failed"<br>
Workers: 300 (max threads)<br>
Verbose Level: 2<br>

## Notes
- `--bypass` ignores headers and cookies from the first GET request to the target (Recon).
- Random user-agents are used for each request to help avoid detection.
- If a password attempt fails due to an exception, it will retry up to **20** times.

## License
This project is released under the `GNU General Public License`. Use responsibly.