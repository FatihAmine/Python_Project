// Comprehensive test script - simulates multiple user interactions
const http = require('http');

const events = [
    { event_type: 'page_visit', page: 'home', element: 'page_load', product_id: null, user_id: 'test_user_456' },
    { event_type: 'click', page: 'home', element: 'add_to_cart_button', product_id: 'P005', user_id: 'test_user_456' },
    { event_type: 'click', page: 'home', element: 'view_details_button', product_id: 'P010', user_id: 'test_user_456' },
    { event_type: 'page_visit', page: 'product', element: 'page_load', product_id: 'P010', user_id: 'test_user_456' },
    { event_type: 'click', page: 'product', element: 'add_to_cart_button', product_id: 'P010', user_id: 'test_user_456' },
    { event_type: 'click', page: 'home', element: 'nav_cart', product_id: null, user_id: 'test_user_456' },
    { event_type: 'page_visit', page: 'cart', element: 'page_load', product_id: null, user_id: 'test_user_456' },
    { event_type: 'click', page: 'cart', element: 'remove_from_cart_button', product_id: 'P005', user_id: 'test_user_456' },
];

async function sendEvent(event, index) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify(event);
        const options = {
            hostname: 'localhost',
            port: 3000,
            path: '/api/log-event',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };

        const req = http.request(options, (res) => {
            let body = '';
            res.on('data', (chunk) => body += chunk);
            res.on('end', () => {
                const result = JSON.parse(body);
                console.log(`[${index + 1}/${events.length}] ${event.event_type} on ${event.page} -> ${result.file}`);
                // Add small delay to ensure unique timestamps
                setTimeout(() => resolve(result), 50);
            });
        });

        req.on('error', (e) => reject(e));
        req.write(data);
        req.end();
    });
}

async function runTests() {
    console.log('=== Running Event Logging Tests ===\n');

    for (let i = 0; i < events.length; i++) {
        await sendEvent(events[i], i);
    }

    console.log('\n=== All tests completed! ===');
    console.log('Check the logs/ folder for generated JSON files.');
}

runTests();
