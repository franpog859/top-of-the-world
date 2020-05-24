(this["webpackJsonpto-the-top"]=this["webpackJsonpto-the-top"]||[]).push([[0],{14:function(t,e,n){},16:function(t,e,n){},18:function(t,e,n){"use strict";n.r(e);var o=n(0),r=n.n(o),c=n(7),a=n.n(c),i=(n(14),n(1)),u=n.n(i),s=n(2),l=n(4),d=n(5);n(16);var h=function(){var t=Object(o.useState)(void 0),e=Object(l.a)(t,2),n=e[0],c=e[1],a=Object(o.useState)(void 0),i=Object(l.a)(a,2),h=i[0],p=i[1],f=function(){var t=Object(s.a)(u.a.mark((function t(){return u.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:navigator.geolocation.getCurrentPosition((function(t){return c(t)}),(function(t){return console.error("Failed to get current position: ",t)}));case 1:case"end":return t.stop()}}),t)})));return function(){return t.apply(this,arguments)}}(),g=function(){var t=Object(s.a)(u.a.mark((function t(){return u.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:console.log("Warming the backend up..."),fetch("".concat("http://127.0.0.1:5000","/healthz"),{headers:{token:"totalsecuretoken123"}}).then((function(t){return t.json()})).then((function(t){return console.debug(t)})).catch((function(t){return console.error("Failed to warm up the backend: ",t)}));case 2:case"end":return t.stop()}}),t)})));return function(){return t.apply(this,arguments)}}();Object(o.useEffect)((function(){f(),g()}),[]);var m=function(){var t=Object(s.a)(u.a.mark((function t(){return u.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:console.log("Fetching closest top position..."),fetch((e=n,"".concat("http://127.0.0.1:5000","/closestTop/").concat(e.coords.latitude,"/").concat(e.coords.longitude)),{headers:{token:"totalsecuretoken123"}}).then((function(t){return t.json()})).then((function(t){return console.debug(t),t})).then((function(t){return p({latitude:t.latitude,longitude:t.longitude})})).catch((function(t){return console.error("Failed to get closest top: ",t)}));case 2:case"end":return t.stop()}var e}),t)})));return function(){return t.apply(this,arguments)}}();return Object(o.useEffect)((function(){n&&m()}),[n]),r.a.createElement("div",{className:"App"},r.a.createElement("header",{className:"App-header"},r.a.createElement(d.a,{variant:"success",onClick:function(){var t=n.coords.latitude.toString(),e=n.coords.longitude.toString(),o=h.latitude.toString(),r=h.longitude.toString();window.open("https://www.google.be/maps/dir/".concat(t,",").concat(e)+"/".concat(o,",").concat(r,"/data=!3m1!4b1!4m2!4m1!3e2"))},size:"lg",disabled:!(void 0!==n&&void 0!==h)},"Take me to the top!"),r.a.createElement("br",null),r.a.createElement(d.a,{variant:"outline-secondary",onClick:function(){window.open("https://github.com/franpog859/top-of-the-world/blob/master/README.md")},size:"lg"},"Wait, what?")))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));n(17);a.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(h,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(t){t.unregister()})).catch((function(t){console.error(t.message)}))},9:function(t,e,n){t.exports=n(18)}},[[9,1,2]]]);
//# sourceMappingURL=main.ab09dffe.chunk.js.map