"use strict";(self.webpackChunkdidi_notebook_extension=self.webpackChunkdidi_notebook_extension||[]).push([[958],{958:(e,o,n)=>{n.r(o),n.d(o,{default:()=>T});var t=n(626),i=n(923),a=n(72),d=n.n(a),s=n(825),r=n.n(s),l=n(659),c=n.n(l),u=n(56),p=n.n(u),m=n(540),f=n.n(m),h=n(113),b=n.n(h),g=n(646),v={};v.styleTagTransform=b(),v.setAttributes=p(),v.insert=c().bind(null,"head"),v.domAPI=r(),v.insertStyleElement=f(),d()(g.A,v),g.A&&g.A.locals&&g.A.locals;var k=n(670),w=n(291);let x="online";-1!==location.hostname.indexOf("notebook-test.bigdata.xiaojukeji.com")?x="test":-1!==location.hostname.indexOf("didiglobal.com")&&(x="global");const y="global"!==x?"2101066":"2824";var j=n(899);const{MainAreaWidget:C}=n(923),{Widget:L}=n(256),T={id:"didi-notebook-extension:plugin",description:"A JupyterLab extension.",autoStart:!0,requires:[k.IFileBrowserFactory,k.IDefaultFileBrowser,i.IWindowResolver,j.IDocumentManager,i.ICommandPalette,w.INotebookTracker],optional:[t.ILabShell],activate:async(e,o,n,t,i,a,d,s)=>{const r=new URLSearchParams(window.location.search),l=r.get("from"),c=r.get("saveId"),u=r.get("hideMenu")||!1;console.log("-----didi-notebook-extension url query----",r);const p=new L;if(p.id="didi-notebook-extension-plugin-window",p.title.label="didi-notebook-extension Window",p.title.closable=!0,"studio"===l){if(console.log("-----didi-notebook-extension----check from studio------"),document.body.classList.add("from-studio"),!await(async()=>{console.log("----------didi-notebook-extensio checkLogin-----------");try{let e=(await fetch("/api/isLogin",{method:"GET"})).body;if(console.log("----------didi-notebook-extensio checkLogin success data-----------",e),10001===(null==e?void 0:e.code)){let o="mis.diditaxi.com.cn";"global"===x&&(o="mis-auth.didiglobal.com"),console.log("----------didi-notebook-extensio checkLogin failed data-----------",e);const n=encodeURIComponent(location.href);window.location.href=`//${o}/auth/sso/login?app_id=${y}&jumpto=${n}&callback_index=2`}else if(0===e.code||1e4===e.code||14001===e.code)return e;return!0}catch(e){return console.error("Failed to check login status:",e),!0}})())return void console.log("-----didi-notebook-extension----check login failed------");console.log("-----didi-notebook-extension----check login success------"),console.log("------from studio  window------",window),p.node.addEventListener("message",(o=>{console.log("---------didi-notebook-extension content node 收到数据啦啦啦啦啦啦---------",o.data),"studio-debug-mode-save"===(o.data||{}).event&&e.commands.execute("docmanager:save")}),!1),window.addEventListener("message",(async o=>{var n,t;console.log("--------didi-notebook-extension window 收到数据啦啦啦啦啦啦---------",o.data);const a=o.data||{};if("studio-debug-mode-save"===a.event){console.log("--------didi-notebook-extension window docmanager:save 保存文件啦---------"),e.commands.execute("docmanager:save");try{const e=null==s?void 0:s.currentWidget;console.log("--------didi-notebook-extension windowcontextForWidget 保存文件啦---------");const o=i.contextForWidget(e);await(null==o?void 0:o.save()),console.log("--------didi-notebook-extension windowcontextForWidget context",o)}catch(e){console.log("--------didi-notebook-extension window 手动保存文件失败啦-----")}console.log("--------didi-notebook-extension windowcontextForWidget 保存成功啦---------"),window.parent.postMessage({event:"studio-debug-mode-save",id:(null==a?void 0:a.id)||c,status:!0},"*")}else if("studio-quit-debug-mode"===a.event){console.log("--------didi-notebook-extension window 手动停止kernel啦---------");try{null===(t=null===(n=e.serviceManager)||void 0===n?void 0:n.sessions)||void 0===t||t.dispose(),console.log("--------------didi-notebook-extension Kernel terminated successfully.------------")}catch(e){console.error("--------------didi-notebook-extensionFailed to terminate kernel:",e)}}}),!1);const n=new C({content:p});s&&(null==s||s.add(n,"main")),o.createFileBrowser("cur-file").model.fileChanged.connect(((e,o)=>{"save"===o.type&&(console.log("---didi-notebook-extension-----File saved-------"),window.parent.postMessage({event:"studio-debug-mode-save",id:c,status:!0},"*"))}))}"true"!==u&&!1===u||(document.body.classList.add("hide-menu"),s&&(s.leftCollapsed&&s.expandLeft(),s.rightCollapsed&&s.expandRight(),s.activeChanged.connect(((e,o)=>{e.leftCollapsed&&e.expandLeft(),e.rightCollapsed&&e.expandRight()})))),console.log("JupyterLab extension didinotebooktest is activated! log",l,u),console.log("JupyterLab extension didi-notebook-extension is activated!",window,e,document.getElementsByClassName("moon")),window.parent.postMessage({event:"notebook-extension-status",status:"loaded",id:c},"*")}}},475:(e,o,n)=>{n.d(o,{A:()=>s});var t=n(601),i=n.n(t),a=n(314),d=n.n(a)()(i());d.push([e.id,'/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n.hide-menu #jp-left-stack, \n.hide-menu #jp-right-stack,\n.hide-menu #jp-top-panel, \n.hide-menu .jp-SideBar,\n.hide-menu #jp-bottom-panel{\n    display: none !important;\n}\n.hide-menu #jp-main-dock-panel {\n    left: 0 !important;\n    width: 100% !important;\n}\n.hide-menu #jq-main-dock-panel #jp-main-dock-panel {\n    width: 100% !important;\n}\n.hide-menu #jp-main-vsplit-panel {\n    left: 0 !important;\n    width: 100% !important;\n}\n.hide-menu #jp-main-split-panel {\n    width: 100% !important;\n    left: 0 !important;\n}\n.hide-menu #jp-main-content-panel{\n    top: 0 !important;\n    left: 0 !important;\n    width: 100% !important;\n}\n.hide-menu .jp-NotebookPanel, .hide-menu .jp-Notebook {\n    width: 100% !important;\n}\n.hide-menu .jp-NotebookPanel  > .jp-NotebookPanel-toolbar,\n.hide-menu .lm-DockPanel  > .lm-DockPanel-tabBar\n {\n    width: 100% !important;\n}\n.from-studio .jp-KernelName, \n.from-studio .lm-DockPanel-tabBar,\n.from-studio .lm-TabBar \n.hide-menu.from-studio .jp-NotebookPanel  > .jp-NotebookPanel-toolbar,\n.hide-menu.from-studio .lm-DockPanel  > .lm-DockPanel-tabBar{\n    display: none !important;\n}\n.from-studio.hide-menu .jp-NotebookPanel, .from-studio.hide-menu .lm-DockPanel {\n    top: 0 !important;\n    border: none !important;\n}\n.from-studio .jp-Notebook-toolbarCellType .jp-Notebook-toolbarCellTypeDropdown option[value="raw"],\n.from-studio .jp-CommandToolbarButton .jp-ToolbarButtonComponent[data-command="docmanager:save"] {\n    display: none !important;\n}\n.from-studio .lm-Menu-item[data-command="notebook:create-console"], \n.from-studio .lm-Menu-item[data-command="inspector:open"],\n.from-studio .lm-Menu-item[data-command="logconsole:open"] {\n    display: none !important;\n}\n.from-studio .lm-TabBar .lm-TabBar-addButton {\n    display: none !important;\n}\n.from-studio {\n    background-color: #fff;\n}',""]);const s=d},646:(e,o,n)=>{n.d(o,{A:()=>l});var t=n(601),i=n.n(t),a=n(314),d=n.n(a),s=n(475),r=d()(i());r.i(s.A),r.push([e.id,"\n",""]);const l=r},314:e=>{e.exports=function(e){var o=[];return o.toString=function(){return this.map((function(o){var n="",t=void 0!==o[5];return o[4]&&(n+="@supports (".concat(o[4],") {")),o[2]&&(n+="@media ".concat(o[2]," {")),t&&(n+="@layer".concat(o[5].length>0?" ".concat(o[5]):""," {")),n+=e(o),t&&(n+="}"),o[2]&&(n+="}"),o[4]&&(n+="}"),n})).join("")},o.i=function(e,n,t,i,a){"string"==typeof e&&(e=[[null,e,void 0]]);var d={};if(t)for(var s=0;s<this.length;s++){var r=this[s][0];null!=r&&(d[r]=!0)}for(var l=0;l<e.length;l++){var c=[].concat(e[l]);t&&d[c[0]]||(void 0!==a&&(void 0===c[5]||(c[1]="@layer".concat(c[5].length>0?" ".concat(c[5]):""," {").concat(c[1],"}")),c[5]=a),n&&(c[2]?(c[1]="@media ".concat(c[2]," {").concat(c[1],"}"),c[2]=n):c[2]=n),i&&(c[4]?(c[1]="@supports (".concat(c[4],") {").concat(c[1],"}"),c[4]=i):c[4]="".concat(i)),o.push(c))}},o}},601:e=>{e.exports=function(e){return e[1]}},72:e=>{var o=[];function n(e){for(var n=-1,t=0;t<o.length;t++)if(o[t].identifier===e){n=t;break}return n}function t(e,t){for(var a={},d=[],s=0;s<e.length;s++){var r=e[s],l=t.base?r[0]+t.base:r[0],c=a[l]||0,u="".concat(l," ").concat(c);a[l]=c+1;var p=n(u),m={css:r[1],media:r[2],sourceMap:r[3],supports:r[4],layer:r[5]};if(-1!==p)o[p].references++,o[p].updater(m);else{var f=i(m,t);t.byIndex=s,o.splice(s,0,{identifier:u,updater:f,references:1})}d.push(u)}return d}function i(e,o){var n=o.domAPI(o);return n.update(e),function(o){if(o){if(o.css===e.css&&o.media===e.media&&o.sourceMap===e.sourceMap&&o.supports===e.supports&&o.layer===e.layer)return;n.update(e=o)}else n.remove()}}e.exports=function(e,i){var a=t(e=e||[],i=i||{});return function(e){e=e||[];for(var d=0;d<a.length;d++){var s=n(a[d]);o[s].references--}for(var r=t(e,i),l=0;l<a.length;l++){var c=n(a[l]);0===o[c].references&&(o[c].updater(),o.splice(c,1))}a=r}}},659:e=>{var o={};e.exports=function(e,n){var t=function(e){if(void 0===o[e]){var n=document.querySelector(e);if(window.HTMLIFrameElement&&n instanceof window.HTMLIFrameElement)try{n=n.contentDocument.head}catch(e){n=null}o[e]=n}return o[e]}(e);if(!t)throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");t.appendChild(n)}},540:e=>{e.exports=function(e){var o=document.createElement("style");return e.setAttributes(o,e.attributes),e.insert(o,e.options),o}},56:(e,o,n)=>{e.exports=function(e){var o=n.nc;o&&e.setAttribute("nonce",o)}},825:e=>{e.exports=function(e){if("undefined"==typeof document)return{update:function(){},remove:function(){}};var o=e.insertStyleElement(e);return{update:function(n){!function(e,o,n){var t="";n.supports&&(t+="@supports (".concat(n.supports,") {")),n.media&&(t+="@media ".concat(n.media," {"));var i=void 0!==n.layer;i&&(t+="@layer".concat(n.layer.length>0?" ".concat(n.layer):""," {")),t+=n.css,i&&(t+="}"),n.media&&(t+="}"),n.supports&&(t+="}");var a=n.sourceMap;a&&"undefined"!=typeof btoa&&(t+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(a))))," */")),o.styleTagTransform(t,e,o.options)}(o,e,n)},remove:function(){!function(e){if(null===e.parentNode)return!1;e.parentNode.removeChild(e)}(o)}}}},113:e=>{e.exports=function(e,o){if(o.styleSheet)o.styleSheet.cssText=e;else{for(;o.firstChild;)o.removeChild(o.firstChild);o.appendChild(document.createTextNode(e))}}}}]);