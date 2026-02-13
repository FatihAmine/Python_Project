
const GA_CONFIG = {
    MEASUREMENT_ID: 'G-8K7ZLGSQKP',
    DEBUG_MODE: false
};

const GATracker = (function () {


    function isGtagAvailable() {
        return typeof gtag === 'function';
    }


    function debugLog(message, data = null) {
        if (GA_CONFIG.DEBUG_MODE) {
            console.log(`[GA4] ${message}`, data || '');
        }
    }

    // Send event to GA4
    function sendEvent(eventName, params = {}) {
        if (!isGtagAvailable()) {
            debugLog('gtag not available - skipping event:', eventName);
            return;
        }

        // Add common parameters
        const eventParams = {
            ...params,
            send_to: GA_CONFIG.MEASUREMENT_ID,
            timestamp: new Date().toISOString()
        };

        gtag('event', eventName, eventParams);
        debugLog(`Event sent: ${eventName}`, eventParams);
    }


    function trackPageView(pageName, pageTitle = null) {
        sendEvent('page_view', {
            page_title: pageTitle || document.title,
            page_location: window.location.href,
            page_path: window.location.pathname,
            custom_page: pageName
        });
    }


    function trackAddToCart(productId, productName = null, price = null) {
        const product = typeof products !== 'undefined'
            ? products.find(p => p.id === productId)
            : null;

        sendEvent('add_to_cart', {
            currency: 'USD',
            value: price || (product ? product.price : 0),
            items: [{
                item_id: productId,
                item_name: productName || (product ? product.name : productId),
                price: price || (product ? product.price : 0),
                quantity: 1
            }]
        });
    }


    function trackViewItem(productId, productName = null, price = null) {
        const product = typeof products !== 'undefined'
            ? products.find(p => p.id === productId)
            : null;

        sendEvent('view_item', {
            currency: 'USD',
            value: price || (product ? product.price : 0),
            items: [{
                item_id: productId,
                item_name: productName || (product ? product.name : productId),
                price: price || (product ? product.price : 0)
            }]
        });
    }

    function trackRemoveFromCart(productId, productName = null, price = null) {
        const product = typeof products !== 'undefined'
            ? products.find(p => p.id === productId)
            : null;

        sendEvent('remove_from_cart', {
            currency: 'USD',
            value: price || (product ? product.price : 0),
            items: [{
                item_id: productId,
                item_name: productName || (product ? product.name : productId),
                price: price || (product ? product.price : 0),
                quantity: 1
            }]
        });
    }


    function trackNavigation(linkName) {
        sendEvent('navigation_click', {
            link_name: linkName,
            link_url: window.location.href
        });
    }


    function trackClick(elementName, additionalParams = {}) {
        sendEvent('click', {
            element_name: elementName,
            ...additionalParams
        });
    }


    function init() {
        // Auto-track page view on load
        document.addEventListener('DOMContentLoaded', function () {
            const pageName = window.location.pathname.includes('product') ? 'product' :
                window.location.pathname.includes('cart') ? 'cart' : 'home';
            trackPageView(pageName);
        });

        debugLog('GA4 Tracker initialized', { measurementId: GA_CONFIG.MEASUREMENT_ID });
    }

    // Public API
    return {
        init,
        trackPageView,
        trackAddToCart,
        trackViewItem,
        trackRemoveFromCart,
        trackNavigation,
        trackClick,
        sendEvent,
        config: GA_CONFIG
    };
})();

// Auto-initialize
GATracker.init();
