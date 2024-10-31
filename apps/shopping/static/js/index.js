"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


app.data = {
    data: function() {
        return {
            // Complete as you see fit.
             item_list: [],
             user_email: "",
             item_name: "",
        };
    },
    methods: {
        // Complete as you see fit.
        load_data: function() {
            axios.get(load_data_url).then(function (r) {
                app.vue.item_list = r.data.item_list;
                app.vue.user_email = r.data.user_email;
            });
        },


        add_item: function() {
            axios.post(add_item_url, {
                item_name: this.item_name,
                user_email: this.user_email,
            }).then(function (r) {
                app.load_data();
                app.vue.item_name = "";
            });
        },

        del_item: function(id) {
            axios.post(del_item_url, {
                id: id,
            }).then(function (r) {
                app.load_data();
            });
        },
    }
};

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    axios.get(load_data_url).then(function (r) {
        app.vue.item_list = r.data.item_list;
        app.vue.user_email = r.data.user_email;
    });
}

// This is the initial data load.
app.load_data();

