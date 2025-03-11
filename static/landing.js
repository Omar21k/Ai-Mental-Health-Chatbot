document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scroll functionality
    document.querySelectorAll('.scroll-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100, // Offset for nav bar
                    behavior: 'smooth'
                });
            }
        });
    });

    // Smooth scroll sections
    gsap.registerPlugin(ScrollTrigger);

    // Hero section animation
    gsap.from('.hero-content', {
        y: 100,
        opacity: 0,
        duration: 1,
        ease: "power4.out"
    });

    // Animate use cases on scroll
    gsap.from('.use-case-card', {
        scrollTrigger: {
            trigger: '.use-cases-section',
            start: 'top center'
        },
        y: 100,
        opacity: 0,
        duration: 1,
        stagger: 0.2,
        ease: "power4.out"
    });

    // Continuous testimonial carousel
    const testimonialTrack = document.querySelector('.testimonials-track');
    if (testimonialTrack) {
        const testimonials = document.querySelectorAll('.testimonial-card');
        const trackWidth = testimonials.length * 420; // card width + margin
        
        // Clone testimonials for infinite scroll
        testimonials.forEach(card => {
            const clone = card.cloneNode(true);
            testimonialTrack.appendChild(clone);
        });

        gsap.to(testimonialTrack, {
            x: -trackWidth,
            duration: 20,
            ease: "none",
            repeat: -1,
            modifiers: {
                x: gsap.utils.unitize(x => parseFloat(x) % trackWidth)
            }
        });
    }

    // Feature cards stagger animation
    gsap.from('.feature-card', {
        scrollTrigger: {
            trigger: '.features-section',
            start: 'top center'
        },
        y: 50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.15,
        ease: "power3.out"
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            targetSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    });
});
