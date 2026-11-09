// Visitors explicitly submit messages; chat is never saved automatically.
const KEEP_DAYS=180;
function fail(status,code){throw Object.assign(new Error(code),{status});}
export function validateMessage(data){
 if(data?.consent!==true)fail(400,'consent_required');
 if(typeof data.id!=='string'||!/^[0-9a-f-]{36}$/i.test(data.id))fail(400,'invalid_request');
 const field=(key,max,required=false)=>{const value=data[key]??'';if(typeof value!=='string'||value.length>max||(required&&!value.trim()))fail(400,'invalid_request');return value.trim();};
 const name=field('name',80),contact=field('contact',200,true),message=field('message',3000,true);
 const transcript=data.transcript??[];if(!Array.isArray(transcript)||transcript.length>20)fail(400,'invalid_request');let chars=0;
 const clean=transcript.map(m=>{if(!m||!['user','assistant'].includes(m.role)||typeof m.content!=='string'||m.content.length>1200)fail(400,'invalid_request');chars+=m.content.length;return {role:m.role,content:m.content};});
 if(chars>8000)fail(413,'too_long');return {id:data.id,name,contact,message,transcript:clean,lang:data.lang==='zh'?'zh':'en'};
}
async function authorized(req,env){
 if(!env.INBOX_KEY)fail(503,'unavailable');
 const token=req.headers.get('Authorization')||'';if(token.length>250)return false;
 const digest=s=>crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));
 const [a,b]=await Promise.all([digest(token),digest('Bearer '+env.INBOX_KEY)]);const x=new Uint8Array(a),y=new Uint8Array(b);let diff=0;for(let i=0;i<x.length;i++)diff|=x[i]^y[i];return diff===0;
}
export async function inbox(req,env,{json,quota,hash,now,reply}){
 const url=new URL(req.url),hour=Math.floor(now/3600000),day=Math.floor(now/86400000);
 if(url.pathname==='/messages'&&req.method==='POST'){
  const data=validateMessage(await json(req));
  await quota(env,`message-ip:${day}:${hash}`,5,(day+1)*86400000);
  await quota(env,`message-day:${day}`,100,(day+1)*86400000);
  await env.DB.prepare('DELETE FROM messages WHERE created<?').bind(now-KEEP_DAYS*86400000).run();
  await env.DB.prepare('INSERT INTO messages(submission_id,name,contact,message,transcript,lang,created) VALUES (?,?,?,?,?,?,?) ON CONFLICT(submission_id) DO NOTHING').bind(data.id,data.name,data.contact,data.message,JSON.stringify(data.transcript),data.lang,now).run();
  return reply({ok:true,id:data.id},201);
 }
 if(!await authorized(req,env)){
  await quota(env,`auth:${hour}:${hash}`,20,(hour+1)*3600000);fail(401,'unauthorized');
 }
 if(url.pathname==='/messages'&&req.method==='GET'){
  const before=url.searchParams.get('before')||String(Number.MAX_SAFE_INTEGER);if(!/^\d{1,16}$/.test(before)||!Number.isSafeInteger(Number(before)))fail(400,'invalid_request');
  await env.DB.prepare('DELETE FROM messages WHERE created<?').bind(now-KEEP_DAYS*86400000).run();
  const result=await env.DB.prepare('SELECT id,name,contact,message,transcript,lang,created FROM messages WHERE id<? ORDER BY id DESC LIMIT 50').bind(Number(before)).all();
  return reply({messages:result.results.map(m=>({...m,transcript:JSON.parse(m.transcript)})),next:result.results.length===50?result.results.at(-1).id:null});
 }
 const match=url.pathname.match(/^\/messages\/(\d+)$/);
 if(match&&req.method==='DELETE'){await env.DB.prepare('DELETE FROM messages WHERE id=?').bind(Number(match[1])).run();return reply({ok:true});}
 return reply({error:'method_not_allowed'},405);
}
