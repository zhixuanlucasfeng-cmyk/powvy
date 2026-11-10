// Fixed upstream per deployment; never accepts a caller-supplied target.
export async function proxy(request, upstreamHost, fetcher=fetch) {
 const incoming=new URL(request.url),target=new URL(request.url);
 target.protocol='https:';target.hostname=upstreamHost;target.port='';
 const headers=new Headers(request.headers);
 // Vercel overwrites X-Forwarded-Host. Translate only our exact same-origin
 // requests; foreign and null origins remain unchanged for upstream CSRF checks.
 if(headers.get('Origin')===incoming.origin)headers.set('Origin',target.origin);
 headers.set('Host',target.host);
 headers.delete('Forwarded');
 headers.set('X-Forwarded-Host',incoming.host);
 headers.set('X-Forwarded-Proto','https');
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),45000);
 try{
  const response=await fetcher(target.href,{method:request.method,headers,body:['GET','HEAD'].includes(request.method)?undefined:request.body,redirect:'manual',signal:controller.signal});
  if(response.status===101)return response; // WebSocket upgrade, unchanged.
  const output=new Headers(response.headers),location=output.get('Location');
  if(location){const redirect=new URL(location,target);if(redirect.hostname===upstreamHost){redirect.protocol=incoming.protocol;redirect.host=incoming.host;output.set('Location',redirect.href);}}
  return new Response(response.body,{status:response.status,statusText:response.statusText,headers:output});
 }catch{
  return new Response('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>暂时无法连接 / Temporarily unavailable</title><main style="font:18px/1.6 system-ui;max-width:600px;margin:10vh auto;padding:24px"><h1>暂时无法连接服务</h1><p>The application did not respond. Please try again shortly.</p><p>服务暂时没有响应，请稍后刷新。没有提交成功的消息请重新发送。</p><a href="https://powvy.org/">返回 Powvy / Back to Powvy</a></main>',{status:503,headers:{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store','Retry-After':'30'}});
 }finally{clearTimeout(timer);}
}
export default {fetch(request,env){return proxy(request,env.UPSTREAM_HOST)}};
