webpackJsonp([2],{79:function(t,e,n){var a=n(27)(n(85),n(96),null,null);t.exports=a.exports},85:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0}),e.default={data:function(){return{hostData:[{ip:"172.16.20.119",process:"wechat",message:"专门用于抓取微信内容"}]}},methods:{handleStart:function(t,e){console.log(t,e)}}}},96:function(t,e){t.exports={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("el-table",{staticStyle:{width:"100%"},attrs:{data:t.hostData,border:""}},[n("el-table-column",{attrs:{label:"主机",width:"180"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("span",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(e.row.ip))])]}}])}),t._v(" "),n("el-table-column",{attrs:{label:"进程名",width:"180"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("el-popover",{attrs:{trigger:"hover",placement:"top"}},[n("p",[t._v("描述: "+t._s(e.row.message))]),t._v(" "),n("div",{staticClass:"name-wrapper",slot:"reference"},[n("el-tag",[t._v(t._s(e.row.process))])],1)])]}}])}),t._v(" "),n("el-table-column",{attrs:{label:"操作",width:"280"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("el-button",{attrs:{size:"small",type:"success"},on:{click:function(n){t.handleStart(e.$index,e.row)}}},[t._v("启动")]),t._v(" "),n("el-button",{attrs:{size:"small",type:"danger"},on:{click:function(n){t.handleStart(e.$index,e.row)}}},[t._v("停止")]),t._v(" "),n("el-button",{attrs:{size:"small",type:"info"},on:{click:function(n){t.handleStart(e.$index,e.row)}}},[t._v("重启")]),t._v(" "),n("el-button",{attrs:{size:"small",type:"warning"},on:{click:function(n){t.handleStart(e.$index,e.row)}}},[t._v("状态")])]}}])})],1)},staticRenderFns:[]}}});
//# sourceMappingURL=2.ea74622fd0ebb0c1824d.js.map