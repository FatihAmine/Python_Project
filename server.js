const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const LOGS_DIR = path.join(__dirname, 'logs');

if (!fs.existsSync(LOGS_DIR)) {
    fs.mkdirSync(LOGS_DIR, { recursive: true });
}

function formatTimestamp(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}${month}${day}${hours}${minutes}${seconds}`;
}

function formatDateFolder(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}${month}${day}`;
}

app.post('/api/log-event', (req, res) => {
    try {
        const now = new Date();
        const timestamp = formatTimestamp(now);
        const dateFolder = formatDateFolder(now);

        const dateFolderPath = path.join(LOGS_DIR, dateFolder);
        if (!fs.existsSync(dateFolderPath)) {
            fs.mkdirSync(dateFolderPath, { recursive: true });
        }

        const eventData = {
            timestamp: timestamp,
            event_type: req.body.event_type || 'unknown',
            page: req.body.page || 'unknown',
            element: req.body.element || 'unknown',
            product_id: req.body.product_id || null,
            user_id: req.body.user_id || 'anonymous'
        };

        const ms = String(now.getMilliseconds()).padStart(3, '0');
        const filename = `${timestamp}${ms}.json`;
        const filepath = path.join(dateFolderPath, filename);

        fs.writeFileSync(filepath, JSON.stringify(eventData, null, 2));

        console.log(`[LOG] Event saved: ${filepath}`);

        res.json({
            success: true,
            message: 'Event logged successfully',
            file: `${dateFolder}/${filename}`
        });
    } catch (error) {
        console.error('[ERROR] Failed to log event:', error);
        res.status(500).json({
            success: false,
            message: 'Failed to log event',
            error: error.message
        });
    }
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on:`);
    console.log(`  Local:   http://127.0.0.1:${PORT}`);
    console.log(`  Network: http://192.168.100.254:${PORT}`);
    console.log(`  Logs:    ./logs/YYYYMMDD/`);
});
