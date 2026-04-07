// Healthcare Forecasting Dashboard - Interactive Script

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
const html = document.documentElement;
const themeIcon = themeToggle.querySelector('.theme-icon');
const themeText = themeToggle.querySelector('span');

// Load saved theme
const savedTheme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', savedTheme);
updateThemeButton(savedTheme);

themeToggle.addEventListener('click', () => {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeButton(newTheme);
    
    // Reinitialize Lucide icons after theme change
    setTimeout(() => lucide.createIcons(), 100);
});

function updateThemeButton(theme) {
    if (theme === 'dark') {
        themeIcon.setAttribute('data-lucide', 'sun');
        themeText.textContent = 'Light Mode';
    } else {
        themeIcon.setAttribute('data-lucide', 'moon');
        themeText.textContent = 'Dark Mode';
    }
    lucide.createIcons();
}

// Sidebar Toggle (Mobile)
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

// Close sidebar when clicking outside (mobile)
document.addEventListener('click', (e) => {
    if (window.innerWidth <= 1024) {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    }
});

// Smooth Scroll for Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (href.startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                // Update active state
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
                
                // Close sidebar on mobile
                if (window.innerWidth <= 1024) {
                    sidebar.classList.remove('active');
                }
            }
        }
    });
});

// Intersection Observer for Section Highlighting
const sections = document.querySelectorAll('.content-section');
const navLinks = document.querySelectorAll('.nav-link');

const observerOptions = {
    root: null,
    rootMargin: '-100px',
    threshold: 0.1
};

const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const sectionId = entry.target.getAttribute('id');
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
}, observerOptions);

sections.forEach(section => sectionObserver.observe(section));

// Animate Stats on Scroll
const statCards = document.querySelectorAll('.stat-card');

const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '0';
            entry.target.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                entry.target.style.transition = 'all 0.6s ease';
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }, 100);
            
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

statCards.forEach((card, index) => {
    card.style.transitionDelay = `${index * 0.1}s`;
    statsObserver.observe(card);
});

// Image Zoom on Click
document.querySelectorAll('.chart-container img, .viz-card img').forEach(img => {
    img.style.cursor = 'pointer';
    img.addEventListener('click', () => {
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            cursor: pointer;
            padding: 40px;
        `;
        
        const modalImg = document.createElement('img');
        modalImg.src = img.src;
        modalImg.style.cssText = `
            max-width: 100%;
            max-height: 100%;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        `;
        
        modal.appendChild(modalImg);
        document.body.appendChild(modal);
        
        modal.addEventListener('click', () => {
            modal.remove();
        });
    });
});

// Maximize Chart Button
document.querySelectorAll('.icon-btn-small').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const chartCard = btn.closest('.chart-card');
        const img = chartCard.querySelector('img');
        
        if (img) {
            img.click(); // Trigger the zoom modal
        }
    });
});

// View Toggle (Grid/List)
const toggleBtns = document.querySelectorAll('.toggle-btn');
const vizGrid = document.querySelector('.viz-grid');

toggleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        toggleBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        const icon = btn.querySelector('i').getAttribute('data-lucide');
        if (icon === 'list') {
            vizGrid.style.gridTemplateColumns = '1fr';
        } else {
            vizGrid.style.gridTemplateColumns = 'repeat(auto-fit, minmax(450px, 1fr))';
        }
    });
});

// Add Loading Animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});

// Refresh Data Button (if exists)
const refreshBtn = document.querySelector('[data-action="refresh"]');
if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
        refreshBtn.style.transform = 'rotate(360deg)';
        refreshBtn.style.transition = 'transform 0.6s ease';
        
        setTimeout(() => {
            refreshBtn.style.transform = 'rotate(0deg)';
        }, 600);
        
        // Add your data refresh logic here
        console.log('Refreshing data...');
    });
}

// Export Report Button
const exportBtn = document.querySelector('.btn-primary');
if (exportBtn) {
    exportBtn.addEventListener('click', () => {
        // Create a simple notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 24px;
            background: linear-gradient(135deg, #059669, #34d399);
            color: white;
            padding: 16px 24px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(5, 150, 105, 0.3);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 600;
            animation: slideIn 0.3s ease;
        `;
        
        notification.innerHTML = `
            <i data-lucide="check-circle" style="width: 20px; height: 20px;"></i>
            Report exported successfully!
        `;
        
        document.body.appendChild(notification);
        lucide.createIcons();
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    });
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Console welcome message
console.log('%c🏥 Healthcare Forecasting Dashboard', 'color: #059669; font-size: 20px; font-weight: bold;');
console.log('%cDeveloped with ❤️ using Glass Admin Template', 'color: #d4a574; font-size: 14px;');
console.log('%cTheme: ' + html.getAttribute('data-theme'), 'color: #e07a5f; font-size: 12px;');
