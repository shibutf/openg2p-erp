odoo.define("openg2p_program.CustomAllActionButtons", function(require){
    "use strict";
    var ListController = require('web.ListController');

    ListController.include({
        init: function () {
            this._super.apply(this, arguments);
        },
        renderButtons: function () {
            this._super.apply(this, arguments);
            if (!this.$buttons) {
                return;
            }
            var self = this;
            this.$buttons.on('click', '.o_button_exportall', function () {
                console.log("Entered SOMETHING");
            });
        }
    })
})