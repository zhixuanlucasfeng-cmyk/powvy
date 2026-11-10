import test from'node:test';import assert from'node:assert/strict';import{proxy}from'../project-gateway/worker.mjs';
test('fixed origin; preserve auth/CSRF origin; rewrite only own redirects',async()=>{
 const req=new Request('https://jc.powvy.org/login?target=https://evil.example',{method:'POST',headers:{Cookie:'session=test',Origin:'https://evil.example','X-Forwarded-Host':'attacker.example',Forwarded:'host=attacker.example'},body:'test'});
 const response=await proxy(req,'jc-sports-day-scoring.vercel.app',async(url,init)=>{assert.equal(new URL(url).hostname,'jc-sports-day-scoring.vercel.app');assert.equal(init.headers.get('host'),'jc-sports-day-scoring.vercel.app');assert.equal(init.headers.get('origin'),'https://evil.example');assert.equal(init.headers.get('cookie'),'session=test');assert.equal(init.headers.get('x-forwarded-host'),'jc.powvy.org');assert.equal(init.headers.has('forwarded'),false);assert.equal(init.redirect,'manual');return new Response(null,{status:303,headers:{Location:'https://jc-sports-day-scoring.vercel.app/scoreboard','Set-Cookie':'session=test; Secure; HttpOnly; SameSite=Lax'}})});
 assert.equal(response.headers.get('Location'),'https://jc.powvy.org/scoreboard');assert.match(response.headers.get('set-cookie'),/HttpOnly/);
 const other=await proxy(new Request('https://jc.powvy.org/'),'jc-sports-day-scoring.vercel.app',async()=>new Response(null,{status:302,headers:{Location:'https://vercel.com/login'}}));assert.equal(other.headers.get('Location'),'https://vercel.com/login');
});
test('preserve upstream auth errors and streamed responses; give visible failure',async()=>{
 const req=new Request('https://solar-agent.powvy.org/api/chat');const denied=await proxy(req,'rest-solar-agent-cm.onrender.com',async()=>new Response('Sign in',{status:401}));assert.equal(denied.status,401);
 const stream=await proxy(req,'rest-solar-agent-cm.onrender.com',async()=>new Response('data: hello\n\n',{headers:{'Content-Type':'text/event-stream'}}));assert.equal(await stream.text(),'data: hello\n\n');assert.match(stream.headers.get('Content-Type'),/event-stream/);
 const down=await proxy(req,'rest-solar-agent-cm.onrender.com',async()=>{throw Error('private diagnostic')});assert.equal(down.status,503);assert.equal((await down.text()).includes('private diagnostic'),false);
});

test('translate only exact same-origin requests, never null or foreign origins',async()=>{
 for(const origin of ['https://jc.powvy.org','null','https://jc.powvy.org.evil.example','http://jc.powvy.org']){
 await proxy(new Request('https://jc.powvy.org/login',{method:'POST',headers:{Origin:origin}}),'jc-sports-day-scoring.vercel.app',async(_,init)=>{assert.equal(init.headers.get('origin'),origin==='https://jc.powvy.org'?'https://jc-sports-day-scoring.vercel.app':origin);return new Response('ok')});
 }
});
test('navigation errors stay errors with usable guidance; API and challenges unchanged',async()=>{
 const nav=new Request('https://solar-agent.powvy.org/chat',{headers:{Accept:'text/html'}});
 const busy=await proxy(nav,'rest-solar-agent-cm.onrender.com',async()=>new Response('Too Many Requests',{status:429}));assert.equal(busy.status,429);assert.match(await busy.text(),/Original service/);
 const challenge=await proxy(nav,'rest-solar-agent-cm.onrender.com',async()=>new Response('challenge',{status:429,headers:{'cf-mitigated':'challenge'}}));assert.equal(await challenge.text(),'challenge');
 const api=await proxy(new Request('https://solar-agent.powvy.org/api/chat',{method:'POST'}),'rest-solar-agent-cm.onrender.com',async()=>new Response('busy',{status:429}));assert.equal(await api.text(),'busy');
});
