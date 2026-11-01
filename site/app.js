const cat=document.querySelector('#demo-cat');
const bubble=document.querySelector('#demo-bubble');
cat.addEventListener('click',()=>{bubble.hidden=!bubble.hidden;cat.setAttribute('aria-expanded',String(!bubble.hidden));});
document.querySelectorAll('[data-action]').forEach(button=>button.addEventListener('click',()=>{cat.classList.remove('jump','wave');void cat.offsetWidth;cat.classList.add(button.dataset.action);}));
cat.addEventListener('animationend',()=>cat.classList.remove('jump','wave'));
document.querySelector('#demo-reset').addEventListener('click',()=>{bubble.hidden=false;cat.classList.remove('jump','wave');cat.setAttribute('aria-expanded','true');});
document.querySelector('.hero-cat').addEventListener('click',()=>{document.body.classList.remove('boop');void document.body.offsetWidth;document.body.classList.add('boop');});
fetch('release.json').then(r=>r.ok?r.json():null).then(r=>{if(r&&r.size){document.querySelector('#download-size').textContent=r.size;}}).catch(()=>{});
