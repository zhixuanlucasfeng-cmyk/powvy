import {chromium} from 'playwright-core';
import assert from 'node:assert/strict';
const browser=await chromium.launch({channel:'chrome'});
try{for(const [name,width,height] of [['desktop',1280,900],['phone',390,844]]){
 const page=await browser.newPage({viewport:{width,height}});let mode='success';
 await page.route('https://powvy-site-chat.zhixuanlucasfeng.workers.dev/chat',async r=>{if(r.request().method()==='OPTIONS')return r.fulfill({status:204,headers:{'Access-Control-Allow-Origin':'*','Access-Control-Allow-Methods':'POST','Access-Control-Allow-Headers':'Content-Type'}});await r.fulfill({status:mode==='success'?200:429,headers:{'Access-Control-Allow-Origin':'*'},json:mode==='success'?{reply:'Power 是一个本地 AI Agent 桌面工具。<img src=x onerror=alert(1)>'}:{error:'rate_limited'}})});
 await page.goto('http://127.0.0.1:8778/',{waitUntil:'domcontentloaded'});await page.evaluate(()=>{document.documentElement.lang='zh-CN'});
 await page.locator('.chat-launch').click();await page.locator('#powvy-chat').waitFor({state:'visible'});await page.locator('#chat-input').fill('介绍 Power');await page.locator('.chat-send').click();await page.waitForFunction(()=>document.querySelector('.chat-log').textContent.includes('桌面工具'));
 assert.equal(await page.locator('.chat-log img').count(),0);assert.equal(await page.locator('.chat-log .user').count(),1);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 const rect=await page.locator('#powvy-chat').boundingBox();assert.ok(rect.x>=0&&rect.y>=0&&rect.x+rect.width<=width&&rect.y+rect.height<=height);
 await page.screenshot({path:'/tmp/powvy-chat-'+name+'.png'});
 mode='limit';await page.locator('#chat-input').fill('再说一下');await page.locator('.chat-send').click();await page.waitForFunction(()=>document.querySelector('.chat-status').classList.contains('error'));assert.equal(await page.locator('#chat-input').inputValue(),'再说一下');
 await page.locator('.chat-actions button').click();assert.equal(await page.locator('.chat-log .user').count(),0);await page.keyboard.press('Escape');assert.equal(await page.locator('#powvy-chat').isVisible(),false);
 await page.evaluate(()=>document.documentElement.lang='en');await page.locator('.chat-launch').click();assert.equal(await page.locator('#chat-title').textContent(),'Powvy AI');assert.match(await page.locator('.chat-log').textContent(),/Hi!/);await page.close();console.log('PASS '+name+': bilingual, modal, safe rendering, errors, clear, layout');
}}finally{await browser.close()}
