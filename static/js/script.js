document.addEventListener("DOMContentLoaded", function () {
    const socket = io();

    socket.on("new_request", function (data) {
        const logTable = document.getElementById('traffic_log').getElementsByTagName('tbody')[0];
        const newRow = logTable.insertRow();
        newRow.insertCell(0).innerText = data.url;
        newRow.insertCell(1).innerText = data.method;
        newRow.insertCell(2).innerText = JSON.stringify(data.headers);
        newRow.insertCell(3).innerText = data.body;
        const replayButton = document.createElement('button');
        replayButton.innerText = 'Modify & Replay';
        replayButton.addEventListener('click', function () {
            document.getElementById('url').value = data.url;
            document.getElementById('method').value = data.method;
            document.getElementById('headers').value = JSON.stringify(data.headers);
            document.getElementById('body').value = data.body;
        });
        newRow.insertCell(4).appendChild(replayButton);
    });

    document.getElementById('modify_form').addEventListener('submit', function (e) {
        e.preventDefault();
        const url = document.getElementById('url').value;
        const method = document.getElementById('method').value;
        const headers = JSON.parse(document.getElementById('headers').value);
        const body = document.getElementById('body').value;

        fetch('/modify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, method, headers, body })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response_display').innerText = `
                Status Code: ${data.response.status_code}
                Headers: ${JSON.stringify(data.response.headers)}
                Body: ${data.response.body}
            `;
        });
    });
});
