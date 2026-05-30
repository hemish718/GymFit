window.addEventListener("load", () => {

    // 🏋️ Floating animation (smooth gym feel)
    gsap.to("#dumbbell", {
        y: -25,
        duration: 1.8,
        repeat: -1,
        yoyo: true,
        ease: "power1.inOut"
    });

    // 🔄 Whole dumbbell slow rotation (premium feel)
    gsap.to("#dumbbell", {
        rotation: 12,
        duration: 2.5,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut",
        transformOrigin: "center center"
    });

    // 💥 Login box entrance animation
    gsap.from(".login-box", {
        x: 150,
        opacity: 0,
        duration: 1,
        ease: "power3.out"
    });

    // ✨ Left text animation
    gsap.from(".left h1", {
        y: -30,
        opacity: 0,
        duration: 1,
        delay: 0.3
    });

    gsap.from(".left p", {
        y: 20,
        opacity: 0,
        duration: 1,
        delay: 0.5
    });

    // ✨ Register link subtle animation
    gsap.from(".register-link", {
        opacity: 0,
        y: 20,
        duration: 0.8,
        delay: 0.7
    });

    // 🔥 Button hover effect
    const loginBtn = document.querySelector('.login-box button');
    if (loginBtn) {
        loginBtn.addEventListener('mouseenter', () => {
            gsap.to(loginBtn, { scale: 1.02, duration: 0.2 });
        });
        loginBtn.addEventListener('mouseleave', () => {
            gsap.to(loginBtn, { scale: 1, duration: 0.2 });
        });
    }

    // 🎯 Input focus glow effect
    const inputs = document.querySelectorAll('.login-box input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            gsap.to(input, { borderColor: '#FFD700', boxShadow: '0 0 8px rgba(255,215,0,0.3)', duration: 0.2 });
        });
        input.addEventListener('blur', () => {
            gsap.to(input, { borderColor: '#333', boxShadow: '0 0 0px', duration: 0.2 });
        });
    });
});