// Event Tracker Module
// Handles all user interaction tracking and sends to server

const Tracker = (function () {
    // Generate or retrieve user ID
    function getUserId() {
        let userId = localStorage.getItem('ecom_user_id');
        if (!userId) {
            userId = 'anonymous_' + Math.random().toString(36).substring(2, 15);
            localStorage.setItem('ecom_user_id', userId);
        }
        return userId;
    }

    // Get current page name from URL
    function getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('product.html')) return 'product';
        if (path.includes('cart.html')) return 'cart';
        if (path.includes('about.html')) return 'about';
        return 'home';
    }

    // Log event to server
    async function logEvent(eventType, element, productId = null, additionalData = {}) {
        const eventData = {
            event_type: eventType,
            page: getCurrentPage(),
            element: element,
            product_id: productId,
            user_id: getUserId(),
            ...additionalData
        };

        try {
            const response = await fetch('/api/log-event', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(eventData)
            });

            if (!response.ok) {
                console.warn('[Tracker] Failed to log event:', response.statusText);
            } else {
                console.log('[Tracker] Event logged:', eventType, element, productId);
            }
        } catch (error) {
            console.warn('[Tracker] Error logging event:', error.message);
        }
    }

    // Track page visit
    function trackPageVisit() {
        const page = getCurrentPage();
        const productId = new URLSearchParams(window.location.search).get('id');
        logEvent('page_visit', 'page_load', productId);
    }

    // Track navigation click
    function trackNavClick(linkName) {
        logEvent('click', 'nav_' + linkName.toLowerCase().replace(/\s+/g, '_'));

        if (typeof GATracker !== 'undefined') {
            GATracker.trackNavigation(linkName);
        }
    }

    // Track View Details button
    function trackViewDetails(productId) {
        logEvent('view_details', 'view_details_button', productId);

        if (typeof GATracker !== 'undefined') {
            GATracker.trackViewItem(productId);
        }
    }

    // Track Add to Cart button
    function trackAddToCart(productId) {
        logEvent('add_to_cart', 'add_to_cart_button', productId);

        if (typeof GATracker !== 'undefined') {
            GATracker.trackAddToCart(productId);
        }
    }

    // Track Remove from Cart button
    function trackRemoveFromCart(productId) {
        logEvent('remove_from_cart', 'remove_from_cart_button', productId);

        if (typeof GATracker !== 'undefined') {
            GATracker.trackRemoveFromCart(productId);
        }
    }

    // Track generic button click
    function trackButtonClick(buttonName, productId = null) {
        logEvent('click', buttonName, productId);

        if (typeof GATracker !== 'undefined') {
            GATracker.trackClick(buttonName, { product_id: productId });
        }
    }

    // Initialize event listeners
    function init() {
        // Track page visit on load
        document.addEventListener('DOMContentLoaded', trackPageVisit);
        // Note: GATracker handles its own page view tracking via its own init

        // Track navigation clicks
        document.addEventListener('click', (e) => {
            // Navigation links
            const navLink = e.target.closest('.nav-links a');
            if (navLink) {
                trackNavClick(navLink.textContent.trim());
            }

            // Logo click
            if (e.target.closest('.logo')) {
                trackNavClick('logo');
            }

            // Cart icon click
            if (e.target.closest('.cart-icon')) {
                trackNavClick('cart_icon');
            }
        });
    }

    // Public API
    return {
        init,
        logEvent,
        trackPageVisit,
        trackNavClick,
        trackViewDetails,
        trackAddToCart,
        trackRemoveFromCart,
        trackButtonClick,
        getUserId,
        getCurrentPage
    };
})();

// Auto-initialize
Tracker.init();
