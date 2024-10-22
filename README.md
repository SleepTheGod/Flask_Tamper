# Overview
This application will do the following.
Capture HTTP requests and headers.
Provide real-time request modification.
Support proxying and SSL/TLS interception (HTTPS support).
Allow users to filter, modify, and inject payloads.
Use WebSockets for real-time traffic analysis.

# Project Structure
```bash
/Flaks_Tamper
│
├── app.py
├── capture_proxy.py
├── ml_detection.py
├── requirements.txt
├── vulnerability_scanner.py
├──interceptors.py
|
├── fuzzing
│   └── payloads.json
│
├── models
│   └── anomaly_model.pkl
│
├── static
│   ├── js
│   └── style
│
└── templates
    ├── fuzz_results.html
    ├── index.html
    ├── layout.html
    └── scan_results.html

```

