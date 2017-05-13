Vue.component("item-todo", {
  template: "<p>这是个待办项</p>"
});

Vue.component("show", {
  template: "<button v-on:click='display'>show all</button>",
  methods: {
    display: function () {
      for (i of vm.$data.items) {
        i.isDisplay = true
      }
    }
  }
});

Vue.component("hide", {
  template: "<button v-on:click='conceal'>hide all</button>",
  methods: {
    conceal: function () {
      for (i of vm.$data.items) {
        i.isDisplay = false
      }
    }
  }
});

var vm = new Vue({
  el: "#app",
  data: {
message: "",
items: [
]
  },
  methods: {
add: function () {
  var e1 = document.getElementById("e1");
  var x = { content: e1.value, isDisplay: true};
  this.items.push(x);
  e1.value = "";
}
  }
})
