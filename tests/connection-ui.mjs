import {chromium} from 'playwright-core';import assert from 'node:assert/strict';
const b=await chromium.launch({channel:'chrome'});
try{const p=await b.newPage({viewport:{width:390,height:844}});let requests=[];p.on('requestfailed',r=>console.log('network:',r.url(),r.failure()?.errorText));
await p.route('https://jc.powvy.org/**',async r=>{requests.push(r.request().method());await r.abort('connectionfailed')});
await p.route('https://alevel-survival-bureau.vercel.app/**',async r=>{requests.push(r.request().method());await r.fulfill({status:200,body:'Filter or application page'})});
await p.route('https://solar-agent.powvy.org/**',async r=>{requests.push(r.request().method());await r.abort('connectionfailed')});
await p.goto('http://127.0.0.1:8778/connection.html');await p.locator('#run').click();await p.waitForFunction(()=>!document.querySelector('#run').disabled);const text=await p.locator('#report').innerText();assert.match(text,/HTTP 200/);assert.match(text,/FAILED/);assert.match(text,/HTTP response received; status and page content cannot be inspected/);assert.match(text,/NOT proof/);assert.deepEqual(requests,['HEAD','HEAD','HEAD']);assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await p.locator('#language').click();await p.screenshot({path:'/tmp/powvy-connection-mobile.png'});
await p.unroute('https://alevel-survival-bureau.vercel.app/**');await p.route('https://alevel-survival-bureau.vercel.app/**',()=>{});await p.locator('#run').click();await p.waitForFunction(()=>!document.querySelector('#run').disabled,{},{timeout:15000});assert.match(await p.locator('#report').innerText(),/TIMEOUT \(12 seconds\)/);
const n=await b.newPage({javaScriptEnabled:false});await n.goto('http://127.0.0.1:8778/connection.html');assert.equal(await n.locator('a[href*="scoreboard"]').isVisible(),true);assert.equal(await n.locator('noscript').isVisible(),true);
await p.goto('http://127.0.0.1:8778/#/product/alevel');await p.locator('#dBody a[href="connection.html"]').waitFor({state:'visible'});console.log('PASS reachable/failed/timeout reporting, no-JS fallback, mobile, and project help link.');
}finally{await b.close()}
