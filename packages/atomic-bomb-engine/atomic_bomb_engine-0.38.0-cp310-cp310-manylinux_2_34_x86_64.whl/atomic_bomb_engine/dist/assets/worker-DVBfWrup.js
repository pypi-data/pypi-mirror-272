(function(){"use strict";self.addEventListener("message",function(n){const{action:s,baseURL:a,nanoid:r}=n.data,e=new WebSocket(`ws://${a}/ws/${r}`);let o;if(s==="start"){const c=()=>{o&&clearInterval(o),o=setInterval(()=>{e.readyState===WebSocket.OPEN&&e.send("PING")},3e3)};e.onopen=()=>{console.log("WebSocket connection opened in worker"),c(),postMessage({type:"open"})},e.onmessage=t=>{postMessage({type:"message",data:t.data})},e.onerror=t=>{console.error("WebSocket error in worker:",t),postMessage({type:"error",error:t.toString()})},e.onclose=()=>{clearInterval(o),console.log("WebSocket connection closed in worker"),postMessage({type:"close"})},self.addEventListener("message",function(t){t.data.action==="close"&&e.close()})}else s==="close"&&e&&(e.close(),clearInterval(o))})})();
