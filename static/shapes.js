document.addEventListener('DOMContentLoaded', () => {
    // Simple continuous floating animation for each shape
    gsap.to('.shape-1', {
        x: "random(-100, 100)", 
        y: "random(-100, 100)",
        duration: "random(15, 20)",
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
    });

    gsap.to('.shape-2', {
        x: "random(-150, 150)", 
        y: "random(-150, 150)",
        duration: "random(20, 25)",
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
    });

    gsap.to('.shape-3', {
        x: "random(-120, 120)", 
        y: "random(-120, 120)",
        duration: "random(18, 23)",
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
    });

    gsap.to('.shape-4', {
        x: "random(-200, 200)", 
        y: "random(-200, 200)",
        duration: "random(25, 30)",
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
    });

    // Add hover pause functionality
    document.querySelectorAll('.shape').forEach(shape => {
        shape.addEventListener('mouseenter', () => {
            gsap.to(shape, { scale: 1.2, duration: 0.3 });
            const animation = gsap.getTweensOf(shape)[0];
            if (animation) animation.pause();
        });

        shape.addEventListener('mouseleave', () => {
            gsap.to(shape, { scale: 1, duration: 0.3 });
            const animation = gsap.getTweensOf(shape)[0];
            if (animation) animation.resume();
        });
    });

    // Send button animation
    document.getElementById('sendButton').addEventListener('click', () => {
        gsap.to('#sendButton svg', {
            y: -20,
            opacity: 0,
            duration: 0.3,
            ease: "power2.in",
            onComplete: () => {
                gsap.set('#sendButton svg', {y: 20});
                gsap.to('#sendButton svg', {
                    y: 0,
                    opacity: 1,
                    duration: 0.3,
                    ease: "power2.out"
                });
            }
        });
    });

    // Navbar links hover animation
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('mouseenter', () => {
            gsap.to(link, {
                scale: 1.1,
                duration: 0.3,
                ease: "power2.out"
            });
        });
        
        link.addEventListener('mouseleave', () => {
            gsap.to(link, {
                scale: 1,
                duration: 0.3,
                ease: "power2.in"
            });
        });
    });

    // Space bar to pause/resume animations
    let isPaused = false;
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
            isPaused = !isPaused;
            gsap.globalTimeline.paused(isPaused);
        }
    });
});
