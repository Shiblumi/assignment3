"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

function format_list(item_list) {
    let formatted_item_list = [];
    item_list.forEach((e) => {
        if (e.is_purchased) {
            formatted_item_list.push(e); // Add purchased items to the front
        } else {
            formatted_item_list.unshift(e); // Add non-purchased items to the end
        }
    });
    return formatted_item_list;
}

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

        toggle_item: function(item) {
            item.is_purchased = !item.is_purchased;
            axios.post(toggle_item_url, {
                id: item.id,
                is_purchased: item.is_purchased,
            }).then(function (r) {
                app.load_data();
            });
        },
    }
};

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    axios.get(load_data_url).then(function (r) {
        let formatted_item_list = format_list(r.data.item_list);
        app.vue.item_list = formatted_item_list;
        app.vue.user_email = r.data.user_email;
    });
}

// This is the initial data load.
app.load_data();

