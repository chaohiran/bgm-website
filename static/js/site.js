// เผื่อไว้สำหรับเพิ่มลูกเล่น/analytics ภายหลัง
console.log("BGM site loaded");
// Reveal on scroll (iOS style)
const reveals = document.querySelectorAll(".reveal");

const revealObserver = new IntersectionObserver(
  entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
      }
    });
  },
  { threshold: 0.2 }
);

reveals.forEach(el => revealObserver.observe(el));
