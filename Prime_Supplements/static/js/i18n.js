// i18n.js - Handles fetching and applying translations dynamically

const SUPPORTED_LANGUAGES = ['en', 'ar', 'fr'];
const DEFAULT_LANGUAGE = 'en';

// Fallback inlined English so that if fetch fails or takes time, we have defaults.
const fallbackEN = {
  "header": { "shop_now": "Shop Now" },
  "nav": { "brand_prime": "Prime", "brand_supplements": "Supplements", "home": "Home", "shop": "Shop", "about": "About", "welcome": "Welcome,", "reviews": "Reviews", "sign_out": "Sign out", "cart": "Cart", "login": "Login", "sign_up": "Sign Up" },
  "home": { "site_name": "Prime Supplements", "site_desc": "Prime Supplements is a specialized store dedicated to helping athletes reach their peak performance with a wide range of high-quality products. From protein powders and amino acids to pre-workouts, recovery formulas, and vitamins, Prime Supplements offers everything athletes need to build strength, boost endurance, and support overall wellness. With expert staff providing personalized guidance and a welcoming atmosphere, Prime Supplements is more than just a store — it's a trusted partner in every athlete’s journey to success.", "our_products": "Our products", "new_title": "New", "new_desc": "Be among the first to experience our newest Products.", "browse": "Browse", "popular_title": "Popular", "popular_desc": "Join the countless individuals who have fallen in love with our quality.", "special_title": "Special", "special_desc": "Experience the magic and delight in the unforgettable Health that await you.", "vision_title": "Vision", "vision_desc": "At Prime Supplements, our vision is to empower athletes and fitness enthusiasts to reach their full potential with top-quality supplements and expert guidance. We aim to be a trusted destination for those seeking better performance, faster recovery, and a healthier lifestyle, building a strong community driven by passion, integrity, and results.", "mission_title": "Mission", "mission_desc": "At Prime Supplements, our mission is to provide athletes and fitness enthusiasts with the highest quality supplements, trusted advice, and unmatched service. We are committed to helping every customer find the right products to support their goals, improve their performance, and enhance their overall well-being, while creating a welcoming community focused on growth, strength, and success.", "hot_deals_title": "Hot Deals", "hot_deals_desc": "Unlock exclusive benefits and discounts by becoming part of our community.", "join_community": "Join our Community", "login_now": "Login Now!" },
  "about": { "heading": "About us", "about_p": "Where Ambition Meets Performance! Born from our passion for empowering athletes, we provide top-quality supplements to fuel your journey. Success isn’t just about talent—it’s about discipline, dedication, and the right support. Our science-backed products help you train harder, recover faster, and perform at your best. Gear up with us and take your game to the next level!", "free_shipping": "Free Shipping", "free_shipping_desc": "On All Orders Over 1500 EGP", "easy_returns": "Easy Returns", "easy_returns_desc": "14 Day Returns Policy", "secure_payment": "Secure Payment", "secure_payment_desc": "100% Secure Guarantee", "special_support": "Special Support", "special_support_desc": "24/7 Dedicated Support" },
  "shop": { "search_placeholder": "Search products...", "search_btn": "Search", "all_categories": "All Categories", "filter_btn": "Filter", "add_to_cart": "Add to cart", "login_to_add": "Please log in to add items to cart", "no_products": "No products found matching your search or filter.", "category_label": "Category:", "related_products": "Related Products" },
  "cart": { "shopping_cart": "Shopping Cart", "for": "for", "clear_cart": "Clear Cart", "quantity": "Quantity:", "price": "Price:", "empty_cart": "Your shopping cart is empty.", "total": "Total:", "pay": "Pay", "with_paypal": "with PayPal", "pay_with_paypal": "Pay with PayPal" },
  "login": { "legend": "Log In", "email_label": "Email", "password_label": "Password", "login_btn": "Log In", "remember_label": "Remember Me", "need_account": "Need An Account?", "sign_up_here": "Sign Up Here" },
  "signup": { "legend": "Create an Account", "username_label": "Username", "email_label": "Email", "phone_label": "Phone Number", "password_label": "Password", "confirm_password_label": "Confirm Password", "submit_btn": "Sign Up", "already_account": "Already have an Account?", "sign_in": "Sign in" },
  "reviews": { "your_reviews": "Your Reviews", "title_label": "Title", "content_label": "Content", "submit_btn": "Submit Review", "login": "Login", "to_post": "to post a review.", "by": "by", "edit_btn": "Edit", "delete_btn": "Delete", "no_reviews": "No reviews yet—be the first to leave one!" },
  "footer": { "prime": "Prime", "supplements": "supplements", "home": "Home", "shop": "Shop", "about": "About", "copyright": "© 2025 Prime Supplements. All rights reserved." },
  "categories": { "digestive_health": "Digestive Health", "vitamins": "Vitamins", "organ_support": "Organ Support", "minerals": "Minerals", "heart_health": "Heart Health", "protein": "Protein" },
  "products": {
    "gut_health+": { "name": "Gut Health+", "desc": "Improve Digestion" },
    "b_complex": { "name": "B Complex", "desc": "Essential B Vitamins" },
    "fiber": { "name": "Fiber", "desc": "Promote Digestive Health" },
    "liver": { "name": "Liver", "desc": "Support Optimal Liver Health" },
    "multi_mineral": { "name": "Multi Mineral", "desc": "Support Healthy Bones and Joints" },
    "multi_vitamin": { "name": "Multi Vitamin", "desc": "Provide Essential Micronutrients" },
    "thyroid_support": { "name": "Thyroid Support", "desc": "Keep Thyroid Operating at Optimal Rate" },
    "omega_3": { "name": "Omega 3", "desc": "Support Cardiovascular Health" },
    "zinc_picolinate": { "name": "Zinc Picolinate", "desc": "Highly Bioavailable Zinc for Immune Support" },
    "magnesium_glycinate": { "name": "Magnesium Glycinate", "desc": "Relaxation and Muscle Recovery" },
    "vitamin_d3+k2": { "name": "Vitamin D3+K2", "desc": "Bone Health and Immune Support" },
    "whey_protein_isolate": { "name": "Whey Protein Isolate", "desc": "Fast Absorbing Protein for Muscle Growth" }
  }
};

let currentTranslations = fallbackEN;

// Initialize language on load
document.addEventListener('DOMContentLoaded', () => {
    let lang = localStorage.getItem('lang');
    if (!lang || !SUPPORTED_LANGUAGES.includes(lang)) {
        lang = DEFAULT_LANGUAGE;
    }
    setLanguage(lang);
    
    // Bind switcher buttons
    const langButtons = document.querySelectorAll('[data-lang-switcher]');
    langButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const selectedLang = e.currentTarget.getAttribute('data-lang-switcher');
            setLanguage(selectedLang);
        });
    });
});

async function setLanguage(lang) {
    localStorage.setItem('lang', lang);
    
    // Update HTML attributes
    document.documentElement.lang = lang;
    if (lang === 'ar') {
        document.documentElement.dir = 'rtl';
    } else {
        document.documentElement.dir = 'ltr';
    }
    
    // Update active state in UI
    updateActiveSwitcher(lang);
    
    // Load translations
    if (lang === 'en') {
        currentTranslations = fallbackEN;
        applyTranslations();
    } else {
        try {
            const response = await fetch(`/static/i18n/${lang}.json`);
            if (response.ok) {
                currentTranslations = await response.json();
                applyTranslations();
            } else {
                console.error(`Failed to load translations for ${lang}`);
            }
        } catch (error) {
            console.error('Error fetching translations:', error);
        }
    }
}

function updateActiveSwitcher(lang) {
    // Optional: highlight current language in the dropdown
    const langButtons = document.querySelectorAll('[data-lang-switcher]');
    langButtons.forEach(btn => {
        if(btn.getAttribute('data-lang-switcher') === lang) {
            btn.classList.add('active', 'fw-bold');
        } else {
            btn.classList.remove('active', 'fw-bold');
        }
    });
    
    // Update the main dropdown text if you have a span for it
    const activeLangText = document.getElementById('activeLangText');
    if (activeLangText) {
        if (lang === 'en') activeLangText.innerHTML = '🇺🇸 EN';
        else if (lang === 'ar') activeLangText.innerHTML = '🇸🇦 AR';
        else if (lang === 'fr') activeLangText.innerHTML = '🇫🇷 FR';
    }
}

function applyTranslations() {
    const elements = document.querySelectorAll('[data-i18n], [data-i18n-title]');
    
    // Add smooth transition class to body if not present
    if(!document.body.classList.contains('i18n-transition')) {
        document.body.classList.add('i18n-transition');
    }
    
    elements.forEach(element => {
        if (element.hasAttribute('data-i18n')) {
            const key = element.getAttribute('data-i18n');
            const translation = getNestedTranslation(currentTranslations, key);
            
            if (translation) {
                if (element.hasAttribute('placeholder') && (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA')) {
                    element.placeholder = translation;
                } else if (element.tagName === 'INPUT' && (element.type === 'submit' || element.type === 'button')) {
                    element.value = translation;
                } else {
                    element.innerHTML = translation;
                }
            }
        }
        
        if (element.hasAttribute('data-i18n-title')) {
            const titleKey = element.getAttribute('data-i18n-title');
            const titleTranslation = getNestedTranslation(currentTranslations, titleKey);
            if (titleTranslation) {
                element.title = titleTranslation;
            }
        }
    });
}

function getNestedTranslation(obj, path) {
    return path.split('.').reduce((acc, part) => acc && acc[part], obj);
}
