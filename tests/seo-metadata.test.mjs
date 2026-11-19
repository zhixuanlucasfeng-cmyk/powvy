import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
test('metadata follows language and returns from a project to the correct homepage',()=>{
 const values=new Map();
 const document={title:'',querySelector:selector=>({setAttribute:(_,value)=>values.set(selector,value)})};
 const context=vm.createContext({document});vm.runInContext(readFileSync(new URL('../assets/seo.js',import.meta.url),'utf8'),context);
 context.updatePowvySEO('en');assert.match(document.title,/Lucas Feng/);assert.match(values.get('meta[name="description"]'),/^Explore AI tools/);
 context.updatePowvySEO('en',{title:'Rest Solar · Powvy',description:'Human and AI support'});assert.equal(document.title,'Rest Solar · Powvy');assert.equal(values.get('meta[property="og:description"]'),'Human and AI support');
 context.updatePowvySEO('zh');assert.match(document.title,/产品/);assert.equal(values.get('meta[property="og:locale"]'),'zh_CN');
});
