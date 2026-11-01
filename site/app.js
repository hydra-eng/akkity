const cat=document.querySelector('#demo-cat');
const bubble=document.querySelector('#demo-bubble');
cat.addEventListener('click',()=>{bubble.hidden=!bubble.hidden;cat.setAttribute('aria-expanded',String(!bubble.hidden));});
document.querySelectorAll('[data-action]').forEach(button=>button.addEventListener('click',()=>{cat.classList.remove('jump','wave');void cat.offsetWidth;cat.classList.add(button.dataset.action);}));
cat.addEventListener('animationend',()=>cat.classList.remove('jump','wave'));
document.querySelector('#demo-reset').addEventListener('click',()=>{bubble.hidden=false;cat.classList.remove('jump','wave');cat.setAttribute('aria-expanded','true');});
document.querySelector('.hero-cat').addEventListener('click',()=>{document.body.classList.remove('boop');void document.body.offsetWidth;document.body.classList.add('boop');});
fetch('release.json').then(r=>r.ok?r.json():null).then(r=>{if(r&&r.size){document.querySelector('#download-size').textContent=r.size;}}).catch(()=>{});
let treats=0;
const careCat=document.querySelector('#care-cat');
const careMessage=document.querySelector('#care-message');
const careEffect=document.querySelector('#care-effect');
const careCopy={play:'One tiny jump for a cat. One big distraction for you.',nap:'Five minutes of quiet in the app. Here, a little pretend snooze. zzz',wake:'Awake! Ready for a little mischief?'};
document.querySelectorAll('[data-care]').forEach(button=>button.addEventListener('click',()=>{
  const action=button.dataset.care;
  careCat.classList.remove('jump','wave','sleepy');void careCat.offsetWidth;
  careCat.classList.add(action==='play'?'jump':action==='nap'?'sleepy':'wave');
  careEffect.textContent=action==='nap'?'zzz':action==='play'?'✳':'♡';
  careMessage.textContent=action==='treat'?`A virtual treat? Purr-fect. ♡ ${++treats} treats in this preview.`:careCopy[action];
}));
document.querySelectorAll('[data-play]').forEach(button=>button.addEventListener('click',()=>{
  const action=button.dataset.play;const playing=button.getAttribute('aria-pressed')!=='true';
  document.querySelector(`[data-motion="${action}"]`).src=`assets/${action}${playing?'':'-still'}.webp`;
  button.setAttribute('aria-pressed',String(playing));button.textContent=playing?'Ⅱ Pause':'▶ Play';
}));
