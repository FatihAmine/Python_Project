// Main Application Module
// Handles product rendering, cart management, and UI interactions

const App = (function () {
    // Cart management using localStorage
    const Cart = {
        getItems() {
            const cart = localStorage.getItem('ecom_cart');
            return cart ? JSON.parse(cart) : [];
        },

        saveItems(items) {
            localStorage.setItem('ecom_cart', JSON.stringify(items));
            this.updateCartCount();
        },

        addItem(productId) {
            const items = this.getItems();
            const existingItem = items.find(item => item.id === productId);

            if (existingItem) {
                existingItem.quantity += 1;
            } else {
                items.push({ id: productId, quantity: 1 });
            }

            this.saveItems(items);
            return items;
        },

        removeItem(productId) {
            let items = this.getItems();
            items = items.filter(item => item.id !== productId);
            this.saveItems(items);
            return items;
        },

        updateQuantity(productId, quantity) {
            const items = this.getItems();
            const item = items.find(item => item.id === productId);

            if (item) {
                if (quantity <= 0) {
                    return this.removeItem(productId);
                }
                item.quantity = quantity;
                this.saveItems(items);
            }

            return items;
        },

        getTotal() {
            const items = this.getItems();
            return items.reduce((total, item) => {
                const product = products.find(p => p.id === item.id);
                return total + (product ? product.price * item.quantity : 0);
            }, 0);
        },

        getItemCount() {
            const items = this.getItems();
            return items.reduce((count, item) => count + item.quantity, 0);
        },

        updateCartCount() {
            const countElements = document.querySelectorAll('.cart-count');
            const count = this.getItemCount();
            countElements.forEach(el => {
                el.textContent = count;
                el.style.display = count > 0 ? 'flex' : 'none';
            });
        },

        clear() {
            localStorage.removeItem('ecom_cart');
            this.updateCartCount();
        }
    };

    // Toast notifications
    function showToast(message, type = 'success') {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${type === 'success' ? '✓' : '!'}</span>
            <span class="toast-message">${message}</span>
        `;

        container.appendChild(toast);

        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // Render product card
    function renderProductCard(product) {
        return `
            <div class="product-card" data-product-id="${product.id}">
                <div class="product-image">
                    <img src="${product.image}" alt="${product.name}" loading="lazy">
                    ${product.badge ? `<span class="product-badge">${product.badge}</span>` : ''}
                </div>
                <div class="product-info">
                    <h3 class="product-name">${product.name}</h3>
                    <p class="product-category">${product.category}</p>
                    <p class="product-price">$${product.price.toFixed(2)}</p>
                    <div class="product-actions">
                        <a href="product.html?id=${product.id}" class="btn btn-secondary btn-sm view-details-btn">
                            View Details
                        </a>
                        <button class="btn btn-primary btn-sm add-to-cart-btn" data-product-id="${product.id}">
                            Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    // Render products grid
    function renderProductsGrid() {
        const grid = document.getElementById('products-grid');
        if (!grid) return;

        grid.innerHTML = products.map(renderProductCard).join('');

        // Add event listeners
        grid.addEventListener('click', (e) => {
            const viewDetailsBtn = e.target.closest('.view-details-btn');
            const addToCartBtn = e.target.closest('.add-to-cart-btn');

            if (viewDetailsBtn) {
                const productId = viewDetailsBtn.closest('.product-card').dataset.productId;
                Tracker.trackViewDetails(productId);
            }

            if (addToCartBtn) {
                e.preventDefault();
                const productId = addToCartBtn.dataset.productId;
                Cart.addItem(productId);
                Tracker.trackAddToCart(productId);

                const product = products.find(p => p.id === productId);
                showToast(`${product.name} added to cart!`);
            }
        });
    }

    // Render product detail page
    function renderProductDetail() {
        const container = document.getElementById('product-detail');
        if (!container) return;

        const urlParams = new URLSearchParams(window.location.search);
        const productId = urlParams.get('id');
        const product = products.find(p => p.id === productId);

        if (!product) {
            container.innerHTML = `
                <div class="text-center">
                    <h2>Product Not Found</h2>
                    <p class="text-muted mt-1">The product you're looking for doesn't exist.</p>
                    <a href="index.html" class="btn btn-primary mt-2">Back to Home</a>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <a href="index.html" class="back-link">
                ← Back to Products
            </a>
            <div class="product-detail-container">
                <div class="product-detail-image">
                    <img src="${product.image}" alt="${product.name}">
                </div>
                <div class="product-detail-info">
                    <h1>${product.name}</h1>
                    <p class="product-detail-price">$${product.price.toFixed(2)}</p>
                    <p class="product-detail-description">${product.description}</p>
                    
                    <div class="product-detail-meta">
                        <div class="meta-item">
                            <span>Category</span>
                            <strong>${product.category}</strong>
                        </div>
                        <div class="meta-item">
                            <span>Product ID</span>
                            <strong>${product.id}</strong>
                        </div>
                        <div class="meta-item">
                            <span>Availability</span>
                            <strong style="color: var(--success)">In Stock</strong>
                        </div>
                    </div>
                    
                    <button class="btn btn-primary btn-block add-to-cart-detail-btn" data-product-id="${product.id}">
                        🛒 Add to Cart
                    </button>
                </div>
            </div>
        `;

        // Add to cart button
        container.querySelector('.add-to-cart-detail-btn').addEventListener('click', (e) => {
            const productId = e.target.dataset.productId;
            Cart.addItem(productId);
            Tracker.trackAddToCart(productId);
            showToast(`${product.name} added to cart!`);
        });

        // Back link tracking
        container.querySelector('.back-link').addEventListener('click', () => {
            Tracker.trackButtonClick('back_to_products_link');
        });
    }

    // Render cart page
    function renderCart() {
        const container = document.getElementById('cart-items');
        const summaryContainer = document.getElementById('cart-summary');
        if (!container || !summaryContainer) return;

        const cartItems = Cart.getItems();

        if (cartItems.length === 0) {
            container.innerHTML = `
                <div class="cart-empty">
                    <div class="cart-empty-icon">🛒</div>
                    <h2>Your cart is empty</h2>
                    <p class="text-muted mt-1">Looks like you haven't added any items yet.</p>
                    <a href="index.html" class="btn btn-primary mt-2">Continue Shopping</a>
                </div>
            `;
            summaryContainer.style.display = 'none';
            return;
        }

        summaryContainer.style.display = 'block';

        // Render cart items
        container.innerHTML = cartItems.map(item => {
            const product = products.find(p => p.id === item.id);
            if (!product) return '';

            return `
                <div class="cart-item" data-product-id="${product.id}">
                    <div class="cart-item-image">
                        <img src="${product.image}" alt="${product.name}">
                    </div>
                    <div class="cart-item-info">
                        <div>
                            <h3 class="cart-item-name">${product.name}</h3>
                            <p class="text-muted">${product.category}</p>
                        </div>
                        <div class="cart-item-actions">
                            <div class="quantity-control">
                                <button class="quantity-btn decrease-qty" data-product-id="${product.id}">−</button>
                                <span class="quantity-display">${item.quantity}</span>
                                <button class="quantity-btn increase-qty" data-product-id="${product.id}">+</button>
                            </div>
                            <p class="cart-item-price">$${(product.price * item.quantity).toFixed(2)}</p>
                            <button class="btn btn-danger btn-sm remove-item-btn" data-product-id="${product.id}">
                                Remove
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        // Update summary
        const subtotal = Cart.getTotal();
        const shipping = subtotal > 0 ? 9.99 : 0;
        const total = subtotal + shipping;

        summaryContainer.innerHTML = `
            <h2>Order Summary</h2>
            <div class="summary-row">
                <span>Subtotal</span>
                <span>$${subtotal.toFixed(2)}</span>
            </div>
            <div class="summary-row">
                <span>Shipping</span>
                <span>$${shipping.toFixed(2)}</span>
            </div>
            <div class="summary-row total">
                <span>Total</span>
                <span>$${total.toFixed(2)}</span>
            </div>
            <button class="btn btn-primary btn-block mt-2 checkout-btn">
                Proceed to Checkout
            </button>
        `;

        // Event listeners
        container.addEventListener('click', (e) => {
            const productId = e.target.dataset.productId;

            if (e.target.classList.contains('decrease-qty')) {
                const item = cartItems.find(i => i.id === productId);
                if (item) {
                    Cart.updateQuantity(productId, item.quantity - 1);
                    Tracker.trackButtonClick('decrease_quantity', productId);
                    renderCart();
                }
            }

            if (e.target.classList.contains('increase-qty')) {
                const item = cartItems.find(i => i.id === productId);
                if (item) {
                    Cart.updateQuantity(productId, item.quantity + 1);
                    Tracker.trackButtonClick('increase_quantity', productId);
                    renderCart();
                }
            }

            if (e.target.classList.contains('remove-item-btn')) {
                Cart.removeItem(productId);
                Tracker.trackRemoveFromCart(productId);
                const product = products.find(p => p.id === productId);
                showToast(`${product.name} removed from cart`);
                renderCart();
            }
        });

        // Checkout button
        summaryContainer.querySelector('.checkout-btn').addEventListener('click', () => {
            Tracker.trackButtonClick('checkout_button');
            showToast('Checkout coming soon!');
        });
    }

    // Initialize application
    function init() {
        // Update cart count on all pages
        Cart.updateCartCount();

        // Initialize page-specific content
        const page = Tracker.getCurrentPage();

        switch (page) {
            case 'home':
                renderProductsGrid();
                break;
            case 'product':
                renderProductDetail();
                break;
            case 'cart':
                renderCart();
                break;
        }
    }

    // Public API
    return {
        init,
        Cart,
        showToast,
        renderProductsGrid,
        renderProductDetail,
        renderCart
    };
})();

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', App.init);
