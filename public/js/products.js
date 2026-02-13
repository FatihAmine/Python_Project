// Product Data - 30 Products with Unsplash Images
const products = [
    {
        id: "P001",
        name: "Wireless Bluetooth Headphones",
        category: "Electronics",
        description: "Premium noise-cancelling wireless headphones with 30-hour battery life. Crystal clear audio with deep bass and comfortable over-ear design for extended listening sessions.",
        price: 199.99,
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop",
        badge: "Best Seller"
    },
    {
        id: "P002",
        name: "Smart Watch Pro",
        category: "Electronics",
        description: "Advanced smartwatch with health monitoring, GPS tracking, and seamless smartphone integration. Water-resistant design with vibrant AMOLED display.",
        price: 349.99,
        image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",
        badge: "New"
    },
    {
        id: "P003",
        name: "Minimalist Leather Wallet",
        category: "Accessories",
        description: "Slim genuine leather wallet with RFID blocking technology. Features 6 card slots and a sleek money clip design.",
        price: 79.99,
        image: "https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P004",
        name: "Designer Sunglasses",
        category: "Accessories",
        description: "UV400 protection polarized sunglasses with titanium frame. Lightweight yet durable with anti-scratch coating.",
        price: 159.99,
        image: "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop",
        badge: "Popular"
    },
    {
        id: "P005",
        name: "Premium Coffee Maker",
        category: "Home & Kitchen",
        description: "Programmable drip coffee maker with thermal carafe. Brew up to 12 cups with precision temperature control.",
        price: 129.99,
        image: "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P006",
        name: "Wireless Charging Pad",
        category: "Electronics",
        description: "Fast wireless charger compatible with all Qi-enabled devices. Sleek aluminum design with LED indicator.",
        price: 39.99,
        image: "https://images.unsplash.com/photo-1586816879360-004f5b0c51e3?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P007",
        name: "Vintage Mechanical Keyboard",
        category: "Electronics",
        description: "Retro-style mechanical keyboard with Cherry MX switches. RGB backlit with customizable key layouts.",
        price: 149.99,
        image: "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=400&fit=crop",
        badge: "Hot"
    },
    {
        id: "P008",
        name: "Portable Bluetooth Speaker",
        category: "Electronics",
        description: "Waterproof portable speaker with 360-degree sound. 20-hour playtime with built-in power bank feature.",
        price: 89.99,
        image: "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P009",
        name: "Ergonomic Office Chair",
        category: "Furniture",
        description: "Premium mesh office chair with lumbar support and adjustable armrests. Breathable design for all-day comfort.",
        price: 449.99,
        image: "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400&h=400&fit=crop",
        badge: "Top Rated"
    },
    {
        id: "P010",
        name: "Canvas Backpack",
        category: "Bags",
        description: "Durable canvas backpack with laptop compartment. Water-resistant exterior with multiple organizational pockets.",
        price: 69.99,
        image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P011",
        name: "Stainless Steel Water Bottle",
        category: "Lifestyle",
        description: "Vacuum insulated bottle keeps drinks cold 24hrs or hot 12hrs. BPA-free with leak-proof lid.",
        price: 34.99,
        image: "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop",
        badge: "Eco-Friendly"
    },
    {
        id: "P012",
        name: "Running Sneakers",
        category: "Footwear",
        description: "Lightweight running shoes with responsive cushioning. Breathable mesh upper with durable rubber outsole.",
        price: 129.99,
        image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
        badge: "Athletic"
    },
    {
        id: "P013",
        name: "Ceramic Desk Lamp",
        category: "Home & Kitchen",
        description: "Modern ceramic table lamp with adjustable brightness. Touch-sensitive controls with warm LED lighting.",
        price: 59.99,
        image: "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P014",
        name: "Noise Cancelling Earbuds",
        category: "Electronics",
        description: "True wireless earbuds with active noise cancellation. 8-hour battery with compact charging case.",
        price: 179.99,
        image: "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop",
        badge: "Premium"
    },
    {
        id: "P015",
        name: "Leather Messenger Bag",
        category: "Bags",
        description: "Genuine leather messenger bag with padded laptop sleeve. Adjustable shoulder strap with brass hardware.",
        price: 199.99,
        image: "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P016",
        name: "Smart Home Hub",
        category: "Electronics",
        description: "Voice-controlled smart home hub compatible with 1000+ devices. Built-in speaker with premium sound.",
        price: 129.99,
        image: "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=400&h=400&fit=crop",
        badge: "Smart Home"
    },
    {
        id: "P017",
        name: "Yoga Mat Premium",
        category: "Fitness",
        description: "Extra thick yoga mat with alignment lines. Non-slip surface with carrying strap included.",
        price: 49.99,
        image: "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P018",
        name: "Digital Camera Mirrorless",
        category: "Electronics",
        description: "24MP mirrorless camera with 4K video recording. Compact body with professional image quality.",
        price: 899.99,
        image: "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400&h=400&fit=crop",
        badge: "Pro"
    },
    {
        id: "P019",
        name: "Aromatherapy Diffuser",
        category: "Home & Kitchen",
        description: "Ultrasonic essential oil diffuser with LED mood lighting. Covers up to 300 sq ft with whisper-quiet operation.",
        price: 44.99,
        image: "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=400&h=400&fit=crop",
        badge: "Relaxation"
    },
    {
        id: "P020",
        name: "Polaroid Instant Camera",
        category: "Electronics",
        description: "Retro instant camera with built-in flash. Create lasting memories with classic square prints.",
        price: 119.99,
        image: "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400&h=400&fit=crop",
        badge: "Vintage"
    },
    {
        id: "P021",
        name: "Gaming Mouse RGB",
        category: "Electronics",
        description: "High-precision gaming mouse with 16000 DPI sensor. Customizable RGB lighting with 8 programmable buttons.",
        price: 79.99,
        image: "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop",
        badge: "Gaming"
    },
    {
        id: "P022",
        name: "Minimalist Wall Clock",
        category: "Home & Kitchen",
        description: "Modern Scandinavian-style wall clock with silent movement. Natural wood frame with clean design.",
        price: 54.99,
        image: "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P023",
        name: "Leather Belt Classic",
        category: "Accessories",
        description: "Genuine leather dress belt with brushed metal buckle. Reversible design: black and brown.",
        price: 59.99,
        image: "https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P024",
        name: "Portable Power Bank",
        category: "Electronics",
        description: "20000mAh portable charger with fast charging. Dual USB outputs with LED battery indicator.",
        price: 49.99,
        image: "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400&h=400&fit=crop",
        badge: "Essential"
    },
    {
        id: "P025",
        name: "Cotton Throw Blanket",
        category: "Home & Kitchen",
        description: "Soft organic cotton blanket with decorative fringe. Perfect for cozy nights on the couch.",
        price: 79.99,
        image: "https://images.unsplash.com/photo-1580301762395-21ce84d00bc6?w=400&h=400&fit=crop",
        badge: "Cozy"
    },
    {
        id: "P026",
        name: "Copper Moscow Mule Set",
        category: "Home & Kitchen",
        description: "Set of 4 handcrafted copper mugs. Perfect for cocktails with authentic hammered finish.",
        price: 44.99,
        image: "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=400&h=400&fit=crop",
        badge: null
    },
    {
        id: "P027",
        name: "Fitness Tracker Band",
        category: "Electronics",
        description: "Slim fitness tracker with heart rate monitoring. Water-resistant with 7-day battery life.",
        price: 69.99,
        image: "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=400&fit=crop",
        badge: "Health"
    },
    {
        id: "P028",
        name: "Wooden Phone Stand",
        category: "Accessories",
        description: "Handcrafted walnut wood phone/tablet stand. Multi-angle viewing with cable management.",
        price: 29.99,
        image: "https://images.unsplash.com/photo-1586105251261-72a756497a11?w=400&h=400&fit=crop",
        badge: "Handmade"
    },
    {
        id: "P029",
        name: "Luxury Scented Candle",
        category: "Home & Kitchen",
        description: "Hand-poured soy wax candle with essential oils. 60-hour burn time in elegant glass jar.",
        price: 38.99,
        image: "https://images.unsplash.com/photo-1602028915047-37269d1a73f7?w=400&h=400&fit=crop",
        badge: "Aromatherapy"
    },
    {
        id: "P030",
        name: "Retro Vinyl Record Player",
        category: "Electronics",
        description: "Vintage-style turntable with built-in speakers. Bluetooth connectivity with 3-speed playback.",
        price: 179.99,
        image: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop",
        badge: "Classic"
    }
];

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = products;
}
