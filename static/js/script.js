document.addEventListener("DOMContentLoaded", function () {
    const socket = io();

    // Listen for new request log entries
    socket.on("new_request", function (data) {
        const logTable = document.getElementById('traffic_log').getElementsByTagName('tbody')[0];
        const newRow = logTable.insertRow();
        newRow.insertCell(0).innerText = data.url;
        newRow.insertCell(1).innerText = data.method;
        newRow.insertCell(2).innerText = JSON.stringify(data.headers, null, 2);
        newRow.insertCell(3).innerText = data.body;

        // Create Modify & Replay button
        const replayButton = document.createElement('button');
        replayButton.innerText = 'Modify & Replay';
        replayButton.addEventListener('click', function () {
            document.getElementById('url').value = data.url;
            document.getElementById('method').value = data.method;
            document.getElementById('headers').value = JSON.stringify(data.headers, null, 2); // Pretty print
            document.getElementById('body').value = data.body;
        });
        newRow.insertCell(4).appendChild(replayButton);
    });

    // Handle the Modify & Replay form submission
    document.getElementById('modify_form').addEventListener('submit', function (e) {
        e.preventDefault();
        const url = document.getElementById('url').value;
        const method = document.getElementById('method').value;
        const headers = parseHeaders(document.getElementById('headers').value);
        const body = document.getElementById('body').value;

        fetch('/modify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, method, headers, body })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                document.getElementById('response_display').innerText = `
                    Status Code: ${data.response.status_code}
                    Headers: ${JSON.stringify(data.response.headers, null, 2)}
                    Body: ${data.response.body}
                `;
            } else {
                document.getElementById('response_display').innerText = "No response returned.";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response_display').innerText = "An error occurred while processing the request.";
        });
    });

    // Handle scanning form submission
    document.getElementById('scan_form').addEventListener('submit', function (e) {
        e.preventDefault();
        const url = document.getElementById('scan_url').value;

        fetch('/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('scan_result').innerText = JSON.stringify(data.result, null, 2);
            window.location.href = "/scan_results";  // Redirect to results page
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('scan_result').innerText = "An error occurred during the scan.";
        });
    });

    // Function to parse headers from JSON string
    function parseHeaders(headersString) {
        try {
            return JSON.parse(headersString);
        } catch (error) {
            console.error('Invalid headers format:', error);
            alert("Invalid headers format. Please enter valid JSON.");
            return {};
        }
    }
});
