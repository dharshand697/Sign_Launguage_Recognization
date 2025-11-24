// bg.js — subtle orbiting light blobs & soft particles - low CPU
const canvas = document.getElementById("bgCanvas");
if (canvas) {
  const ctx = canvas.getContext("2d");
  let w = canvas.width = innerWidth;
  let h = canvas.height = innerHeight;

  const blobs = [];
  const particles = [];
  const BLOB_COUNT = Math.max(2, Math.floor(w / 600));

  function rand(min, max){ return Math.random() * (max - min) + min; }

  for (let i = 0; i < BLOB_COUNT; i++) {
    blobs.push({
      x: rand(0, w),
      y: rand(0, h),
      r: rand(180, 360),
      vx: rand(-0.1, 0.1),
      vy: rand(-0.05, 0.05),
      hue: rand(180, 210),
      alpha: rand(0.06, 0.14)
    });
  }

  function draw() {
    ctx.clearRect(0,0,w,h);
    // faint dark gradient base
    const g = ctx.createLinearGradient(0,0,w,h);
    g.addColorStop(0, "rgba(2,6,10,0.75)");
    g.addColorStop(1, "rgba(6,8,12,0.9)");
    ctx.fillStyle = g;
    ctx.fillRect(0,0,w,h);

    // blobs
    for (let b of blobs) {
      b.x += b.vx; b.y += b.vy;
      if (b.x < -200) b.x = w + 200;
      if (b.x > w + 200) b.x = -200;
      if (b.y < -200) b.y = h + 200;
      if (b.y > h + 200) b.y = -200;

      const rg = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, b.r);
      rg.addColorStop(0, `hsla(${b.hue}, 80%, 50%, ${b.alpha})`);
      rg.addColorStop(0.3, `hsla(${b.hue}, 70%, 45%, ${b.alpha * 0.6})`);
      rg.addColorStop(1, `rgba(0,0,0,0)`);
      ctx.fillStyle = rg;
      ctx.beginPath();
      ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
      ctx.fill();
    }

    requestAnimationFrame(draw);
  }

  draw();

  window.addEventListener("resize", () => {
    w = canvas.width = innerWidth;
    h = canvas.height = innerHeight;
  });
}
