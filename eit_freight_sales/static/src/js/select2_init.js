/** @odoo-module **/

// import { _t } from "@web/core/l10n/translation";
// import publicWidget from "@web/legacy/js/public/public_widget";

// publicWidget.registry.Select2ToInit = publicWidget.Widget.extend({
//         selector: '#to_port_cities',
//         start: function () {
//             this._super.apply(this, arguments);
//             this.$el.find('.select').select({
//                 placeholder: "Select Port/Cities...",
//                 allowClear: true
//             });
//         },
//     });

// publicWidget.registry.Select2FromInit = publicWidget.Widget.extend({
//         selector: '#from_port_cities',
//         start: function () {
//             this._super.apply(this, arguments);
//             this.$el.find('.select').select({
//                 placeholder: "Select Port/Cities...",
//                 allowClear: true
//             });
//         },
//     });


$(document).ready(function() {
    $('.select_from_port_cities').select2()
    $('.select_to_port_cities').select2()

    
});
    