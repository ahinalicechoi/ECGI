
const fadeWidget = document.querySelectorAll(".fade-text");
const fadeWidget2 = document.querySelectorAll(".fade-custom");
const fadeImg = document.querySelectorAll(".fade-img");

const onscreenReqs = {
  threshold: 0.25,
  rootMargin: "0px 0px -25px 0px"
};

const onscreenSelf = new IntersectionObserver(function(
    entries,
    onscreenSelf) {
  entries.forEach(entry => {
    if (!entry.isIntersecting) {
      return;
    } else {
      entry.target.classList.add("onscreen");
      onscreenSelf.unobserve(entry.target);
    }
  });
},
onscreenReqs);

fadeWidget.forEach(w => {
  onscreenSelf.observe(w);
});

fadeWidget2.forEach(w => {
  onscreenSelf.observe(w);
});

fadeImg.forEach(w => {
  onscreenSelf.observe(w);
});

//sliders.forEach(slider => {
//  onscreenSelf.observe(slider);
//});