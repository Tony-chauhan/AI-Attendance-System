document.addEventListener('DOMContentLoaded', () => {
    const listElement = document.getElementById('attendance-list');

    // Function to fetch recent attendance logs and update the UI
    const fetchLogs = async () => {
        try {
            const response = await fetch('/api/attendance');
            if (!response.ok) throw new Error("Could not fetch data");
            const records = await response.json();

            // Clear current list
            listElement.innerHTML = '';

            // Populate the table
            if (records.length === 0) {
                listElement.innerHTML = '<tr><td colspan="3" style="text-align:center;">No recent attendance logged yet.</td></tr>';
            } else {
                records.forEach(record => {
                    const row = document.createElement('tr');
                    
                    // Format timestamp
                    const date = new Date(record.timestamp);
                    const timeString = date.toLocaleTimeString() + ' (' + date.toLocaleDateString() + ')';
                    
                    row.innerHTML = `
                        <td><strong>${record.name}</strong></td>
                        <td>${timeString}</td>
                        <td><span class="status-badge"><i class="fa-solid fa-check"></i> Present</span></td>
                    `;
                    listElement.appendChild(row);
                });
            }

        } catch (error) {
            console.error("Error fetching attendance logs:", error);
        }
    };

    // Initial fetch
    fetchLogs();

    // Poll server every 3 seconds for updates
    setInterval(fetchLogs, 3000);
});
