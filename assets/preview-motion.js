/* GSAP is local; all content remains visible if the library cannot load. */
(() => {
  const art = document.querySelector('#heroArt');
  if (!art) return;
  const en = document.documentElement.lang === 'en';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'motion-toggle';
  art.after(button);
  let paused = reduced.matches, visible = true, rev;
  const speed = {rate: 1};
  const animations = () => [...document.querySelectorAll('.chain-tooth')].flatMap(el => el.getAnimations());
  function sync() {
    const stopped = paused || !visible || document.hidden;
    animations().forEach(animation => stopped ? animation.pause() : animation.play());
    button.textContent = paused ? (en ? '▶ Play chainsaws' : '▶ 播放电锯动画') : (en ? 'Ⅱ Pause chainsaws' : 'Ⅱ 暂停电锯动画');
    button.setAttribute('aria-pressed', String(paused));
  }
  function updateSpeed() { animations().forEach(a => a.updatePlaybackRate(speed.rate)); }
  button.addEventListener('click', () => { paused = !paused; sync(); });
  reduced.addEventListener('change', () => { paused = reduced.matches; sync(); });
  document.addEventListener('visibilitychange', sync);
  const observer = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; sync(); });
  observer.observe(art);
  art.addEventListener('click', () => {
    if (paused || reduced.matches || !window.gsap) return;
    rev?.kill();
    rev = gsap.timeline().to(speed, {rate:4,duration:.18,ease:'power2.out',onUpdate:updateSpeed})
      .to(speed,{rate:1,duration:1.1,ease:'power2.inOut',onUpdate:updateSpeed},'+=.35');
  });
  sync();
  if (!window.gsap) return;
  const media = gsap.matchMedia();
  media.add('(prefers-reduced-motion: no-preference)', () => {
    gsap.timeline({defaults:{duration:.65,ease:'power3.out',clearProps:'transform,opacity'}})
      .from('.hero h1 > *',{y:24,opacity:0,stagger:.09})
      .from('.hero p, .hero .tags, .hero-actions',{y:14,opacity:0,stagger:.08},'-.35')
      .from('.hero .art',{y:20,opacity:0,duration:.85},.18);
  });
  addEventListener('pagehide', () => { rev?.kill(); media.revert(); observer.disconnect(); });
  addEventListener('pageshow', () => { observer.observe(art); sync(); });
})();
