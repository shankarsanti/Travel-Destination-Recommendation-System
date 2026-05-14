/* Main JavaScript - Travel Destination Recommendation System */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initFlashMessages();
  initStarRating();
  initAnimations();
  initChatbot();
  initContactForm();
});

/* ---- Navbar scroll & toggle ---- */
function initNavbar() {
  const navbar = document.querySelector('.navbar');
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');

  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 50);
    });
  }
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      links.classList.toggle('active');
      toggle.textContent = links.classList.contains('active') ? '✕' : '☰';
    });
    links.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => { links.classList.remove('active'); toggle.textContent = '☰'; });
    });
  }
}

/* ---- Auto-dismiss flash messages ---- */
function initFlashMessages() {
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => { flash.style.opacity = '0'; flash.style.transform = 'translateX(100%)'; setTimeout(() => flash.remove(), 300); }, 4000);
  });
}

/* ---- Star rating input ---- */
function initStarRating() {
  const starInputs = document.querySelectorAll('.star-input');
  starInputs.forEach(container => {
    container.querySelectorAll('label').forEach(label => {
      label.addEventListener('click', () => {
        const input = document.getElementById(label.getAttribute('for'));
        if (input) input.checked = true;
      });
    });
  });
}

/* ---- Scroll fade-up animation ---- */
function initAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('fade-up'); observer.unobserve(entry.target); }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.animate-on-scroll').forEach(el => observer.observe(el));
}

/* ---- Wishlist toggle via AJAX ---- */
function toggleWishlist(destId, btn) {
  fetch(`/wishlist/toggle/${destId}`, {
    method: 'POST',
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(r => r.json())
  .then(data => {
    if (btn) {
      btn.classList.toggle('active');
      btn.innerHTML = data.in_wishlist ? '❤️' : '🤍';
    }
  })
  .catch(() => { window.location.href = '/login'; });
}

/* ---- Live search ---- */
let searchTimeout;
function liveSearch(query) {
  clearTimeout(searchTimeout);
  const resultsBox = document.getElementById('search-results');
  if (!resultsBox) return;
  if (query.length < 2) { resultsBox.classList.add('hidden'); return; }
  searchTimeout = setTimeout(() => {
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
      .then(r => r.json())
      .then(results => {
        if (results.length === 0) { resultsBox.classList.add('hidden'); return; }
        resultsBox.innerHTML = results.map(r => `<a href="/destination/${r.id}" class="search-result-item"><strong>${r.name}</strong><span>${r.state}</span></a>`).join('');
        resultsBox.classList.remove('hidden');
      });
  }, 300);
}

/* ---- Chatbot ---- */
function initChatbot() {
  const toggleBtn = document.getElementById('chatbotToggle');
  const panel = document.getElementById('chatbotPanel');
  const closeBtn = document.getElementById('chatbotClose');
  const input = document.getElementById('chatInput');
  const sendBtn = document.getElementById('chatSend');
  const messages = document.getElementById('chatMessages');

  if (!toggleBtn || !panel) return;

  toggleBtn.addEventListener('click', () => {
    panel.classList.toggle('open');
    if (panel.classList.contains('open')) input.focus();
  });

  closeBtn.addEventListener('click', () => panel.classList.remove('open'));

  function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;

    // Add user message
    const userDiv = document.createElement('div');
    userDiv.className = 'chat-msg user';
    userDiv.textContent = msg;
    messages.appendChild(userDiv);
    input.value = '';
    messages.scrollTop = messages.scrollHeight;

    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-msg bot';
    typingDiv.innerHTML = '<div class="spinner" style="width:20px;height:20px;border-width:2px"></div>';
    messages.appendChild(typingDiv);
    messages.scrollTop = messages.scrollHeight;

    // Send to API
    fetch('/api/chatbot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    })
    .then(r => r.json())
    .then(data => {
      typingDiv.remove();
      const botDiv = document.createElement('div');
      botDiv.className = 'chat-msg bot';
      let html = data.message.replace(/\n/g, '<br>');

      // Add destination cards
      if (data.destinations && data.destinations.length > 0) {
        html += '<div style="margin-top:8px">';
        data.destinations.forEach(d => {
          const imgSrc = d.image_url && d.image_url.startsWith('http') ? d.image_url : `/static/images/${d.image_url || 'default_dest.jpg'}`;
          html += `<a href="/destination/${d.id}" class="chat-dest-card"><img src="${imgSrc}" alt="${d.name}"><div class="chat-dest-info"><strong>${d.name}</strong><span>📍 ${d.state} · ⭐ ${d.rating} · ₹${Number(d.cost_estimate).toLocaleString('en-IN')}</span></div></a>`;
        });
        html += '</div>';
      }
      botDiv.innerHTML = html;
      messages.appendChild(botDiv);
      messages.scrollTop = messages.scrollHeight;
    })
    .catch(() => {
      typingDiv.remove();
      const errDiv = document.createElement('div');
      errDiv.className = 'chat-msg bot';
      errDiv.textContent = '❌ Sorry, something went wrong. Try again!';
      messages.appendChild(errDiv);
    });
  }

  sendBtn.addEventListener('click', sendMessage);
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
}

/* ---- Contact Form Handler ---- */
function initContactForm() {
  // Check if we're on the contact section after form submission
  if (window.location.hash === '#contact') {
    // Scroll to contact section smoothly
    setTimeout(() => {
      const contactSection = document.getElementById('contact');
      if (contactSection) {
        contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  }
}
