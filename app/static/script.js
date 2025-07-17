const socket = io();

// Fetch and display public IP
fetch("/get_public_ip")
    .then(response => response.text())
    .then(ip => {
        document.getElementById("public_ip").textContent = ip;
    })
    .catch(() => {
        document.getElementById("public_ip").textContent = "Unavailable";
    });

function startScan() {
    document.getElementById("results_textarea").value = "";
    document.getElementById("progress_textarea").value = "";

    const scanType = document.querySelector('input[name="scan_type"]:checked').value;
    const ports = document.getElementById("port_input").value;
    socket.emit("start_scan", { scan_type: scanType, ports: ports });
}

socket.on("scan_result", data => {
    const li = document.createElement("li");
    li.textContent = `${data.type} port ${data.port} is ${data.status}`;

    const resultsTextarea = document.getElementById("results_textarea");
    resultsTextarea.value += `${data.type} port ${data.port} is ${data.status}\n`;
});

socket.on("scan_progress", progress => {
    const progressTextarea = document.getElementById("progress_textarea");
    progressTextarea.value += `Scanning port ${progress.port}...\n`;
});

socket.on("scan_complete", () => {
    const li = document.createElement("li");
    li.textContent = "Scan complete.";

    const progressTextarea = document.getElementById("progress_textarea");
    progressTextarea.value += "Scan complete.\n";
});
