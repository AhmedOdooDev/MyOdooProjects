/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.MyHostel = publicWidget.Widget.extend({
    selector: '#request_quote_form',

    events: {
        'submit': '_onSubmit',
        'change #from_port_cities': '_onChangeFromCities',
        'change #to_port_cities': '_onChangeToCities',
        'change #transport_type': '_onChangeTransportType',
        'change #equipment_type_for_sea': '_onChangeEquipmentType',
        'change #equipment_type_for_inland': '_onChangeEquipmentTypeInland',
        'change #by_unit_checkbox': '_onChangeByUnitCheckbox',
        'change #by_unit_lcl_checkbox': '_onChangeByUnitLCLCheckbox',
        'change #by_unit_ltl_checkbox': '_onChangeByUnitLTLCheckbox',
        'change input[name="service_needed[]"]': '_onInsuranceCheckbox',
        'click #addRow': '_onAddRow',
        'click #removeRow_service': '_onRemoveRowService',
        'click #removeRow': '_onRemoveRow',
        'click #addRow_fcl': '_onAddRowFCL',
        'click #removeRow_fcl': '_onRemoveRowFCL',
        'click #addRow_lcl': '_onAddRowLCL',
        'click #removeRow_lcl': '_onRemoveRowLCL',
        'click #addRow_ftl': '_onAddRowFTL',
        'click #removeRow_ftl': '_onRemoveRowFTL',
        'click #addRow_ltl': '_onAddRowLTL',
        'click #addRow_service_needed': '_onAddRowServiceNeeded',
        'click #removeRow_ltl': '_onRemoveRowLTL',
        'input .dimensions_l': '_onInputChange_air',
        'input .dimensions_h': '_onInputChange_air',
        'input .dimensions_w': '_onInputChange_air',
        'input .quantity': '_onInputChange_air',
        'input .weight': '_onInputChange_air',
        'input .dimensions_l_lcl': '_onInputChange_lcl',
        'input .dimensions_h_lcl': '_onInputChange_lcl',
        'input .dimensions_w_lcl': '_onInputChange_lcl',
        'input .quantity_lcl': '_onInputChange_lcl',
        'input .weight_lcl': '_onInputChange_lcl',
        'input .dimensions_l_ltl': '_onInputChange_ltl',
        'input .dimensions_h_ltl': '_onInputChange_ltl',
        'input .dimensions_w_ltl': '_onInputChange_ltl',
        'input .quantity_ltl': '_onInputChange_ltl',
        'input .weight_ltl': '_onInputChange_ltl',
    },
    start: function () {
        var def = this._super.apply(this, arguments);
        this.$tag_type_air_id = this.$('input[name="tag_type_air_id"]').val();
        this.$tag_type_lcl_id = this.$('input[name="tag_type_lcl_id"]').val();
        this.$air_id = this.$('input[name="air_id"]').val();
        this.$sea_id = this.$('input[name="sea_id"]').val();
        this.$inland_id = this.$('input[name="inland_id"]').val();
        this.$show_for_air_div = this.$('div[name="show_for_air_div"]');
        this.$show_for_sea_div = this.$('div[name="show_for_sea_div"]');
        this.$show_for_air_all = this.$('.show_for_air');
        this.$show_for_sea_all = this.$('.show_for_sea');
        this.$show_from_cities_air_sea = this.$('.show_from_cities_air_sea');
        this.$show_from_cities_inland = this.$('.show_from_cities_inland');
        this.$show_for_inland_div = this.$('div[name="show_for_inland_div"]');
        this.$show_for_inland_all = this.$('.show_for_inland');
        this.$equipment_type_select = this.$('select[name="equipment_type_for_sea"]');
        this.$equipment_type_inland_select = this.$('select[name="equipment_type_for_inland"]');
        this.$show_for_fcl_sea_div = this.$('div[name="show_for_fcl_sea_div"]');
        this.$show_for_lcl_sea_div = this.$('div[name="show_for_lcl_sea_div"]');
        this.$show_for_ftl_inland_div = this.$('div[name="show_for_ftl_inland_div"]');
        this.$show_for_ltl_inland_div = this.$('div[name="show_for_ltl_inland_div"]');
        this.$show_for_by_unit_div = this.$('div[name="show_for_by_unit_div"]');
        this.$hide_for_by_unit_div = this.$('div[name="hide_for_by_unit_div"]');
        this.$insurance_textbox_div = this.$('div[name="insurance_textbox_div"]');
        this.$show_for_by_unit_lcl_div = this.$('div[name="show_for_by_unit_lcl_div"]');
        this.$hide_for_by_unit_lcl_div = this.$('div[name="hide_for_by_unit_lcl_div"]');
        this.$show_for_by_unit_ltl_div = this.$('div[name="show_for_by_unit_ltl_div"]');
        this.$hide_for_by_unit_ltl_div = this.$('div[name="hide_for_by_unit_ltl_div"]');
        this.$by_unit_checkbox = this.$('input[id="by_unit_checkbox"]');
        this.$show_for_inland_div.hide();
        this.$show_for_inland_all.hide();
        this.$show_for_air_div.hide();
        this.$show_for_air_all.hide();
        this.$show_for_sea_div.hide();
        this.$show_for_sea_all.hide();
        this.$show_from_cities_air_sea.hide();
        this.$show_from_cities_inland.show();
        //        this.$equipment_type_inland_select.val('FTL');
        //        this.$equipment_type_inland_select.trigger('change');
        this.rowCount = 1;
        this.rowCountLCL = 1;
        this.rowCountFCL = 1;
        this.rowCountFTL = 1;
        this.rowCountLTL = 1;
        this.rpc = rpc;
        this.orm = this.bindService("orm");
        return def;
    },
    _replaceSelect: async function (type_id) {
        const element_from = this.$('select[name="from_port_cities"]');
        const element_to = this.$('select[name="to_port_cities"]');
        const model = 'port.cites';
        const domain = [];
        const fields = ['id', 'display_name'];
        var $select_from = $('<select></select>')
            .attr('id', 'from_port_cities')
            .attr('name', 'from_port_cities')
            .attr('class', 'form-control link-style')
            .attr('style', 'padding-left: 30px;')
        //            .append($('<option></option>')
        //                .attr('value', '').text('Select Port/Cities...')
        //                .attr('disabled', 'disabled')
        //                .attr('selected', 'selected')
        //                .attr('hidden', 'hidden')
        //            );
        var $select_to = $('<select></select>')
            .attr('id', 'to_port_cities')
            .attr('name', 'to_port_cities')
            .attr('class', 'form-control link-style')
            .attr('style', 'padding-left: 30px;')
        // Add "Select..." option
        //        var $defaultOption = $('<option></option>')
        //            .attr('value', '')
        //            .text('Select...');
        //        $select_from.append($defaultOption);
        //        $select_to.append($defaultOption);

        try {
            //            var data = await this.orm.call(model, "search_read", [domain, fields]);
            var data = await this.orm.call(model, "search_read", []);
            console.log(data);
            data.forEach(function (city) {
                var $option = $('<option />').val(city.id).text(city.display_name);
                var $option2 = $('<option />').val(city.id).text(city.display_name);
                $select_to.append($option);
                $select_from.append($option2);
            });
        } catch (error) {
            console.error('Error fetching records:', error);
            return;
        }
        var $existingSelect = element_from;
        $existingSelect.empty();  // Clear existing options
        $existingSelect.append($select_from.html());
        var $existingSelect_to = element_to;
        $existingSelect_to.empty();  // Clear existing options
        $existingSelect_to.append($select_to.html());
    },
    _onChangeTransportType: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var TransportTypeElement = event.target;
        var value = TransportTypeElement.options[TransportTypeElement.selectedIndex].text;
        if (value === 'Air') {
            this.$show_for_air_div.show();
            this.$show_for_air_all.show();
            this.$show_for_sea_div.hide();
            this.$show_for_sea_all.hide();
            this.$show_for_inland_div.hide();
            this.$show_for_inland_all.hide();
            this.$show_from_cities_air_sea.show();
            this.$show_from_cities_inland.hide();
//            this._replaceSelect(this.$air_id);
        } else if (value === 'Sea') {
            this.$show_for_air_div.hide();
            this.$show_for_air_all.hide();
            this.$show_for_sea_div.show();
            this.$show_for_sea_all.show();
            //            this.$equipment_type_select.val('FCL');
            //            this.$equipment_type_select.trigger('change');
            this.$show_for_inland_div.hide();
            this.$show_for_inland_all.hide();
            this.$show_from_cities_air_sea.show();
            this.$show_from_cities_inland.hide();
//            this._replaceSelect(this.$sea_id);
        } else if (value === 'Land') {
            this.$show_for_inland_div.show();
            this.$show_for_inland_all.show();
            //            this.$equipment_type_inland_select.val('FTL');
            //            this.$equipment_type_inland_select.trigger('change');
            this.$show_for_air_div.hide();
            this.$show_for_air_all.hide();
            this.$show_for_sea_div.hide();
            this.$show_for_sea_all.hide();
            this.$show_from_cities_air_sea.hide();
            this.$show_from_cities_inland.show();
//            this._replaceSelect(this.$inland_id);
        } else {
            this.$show_for_air_div.hide();
            this.$show_for_air_all.hide();
            this.$show_for_inland_all.hide();
            this.$show_for_sea_all.hide();
            this.$show_from_cities_air_sea.show();
            this.$show_from_cities_inland.hide();
        }
    },
    _onChangeEquipmentType: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var EquipmentTypeElement = event.target;
        var value = EquipmentTypeElement.options[EquipmentTypeElement.selectedIndex].value;
        if (value === 'FCL') {
            this.$show_for_fcl_sea_div.show();
            this.$show_for_lcl_sea_div.hide();
        } else if (value === 'LCL') {
            this.$show_for_fcl_sea_div.hide();
            this.$show_for_lcl_sea_div.show();
        } else {
            this.$show_for_fcl_sea_div.hide();
            this.$show_for_lcl_sea_div.hide();
        }
    },
    _onChangeFromCities: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var $selectElementFrom = $('#from_port_cities');
        var $selectElementFromLabel = $('.select_from_port_cities_required');

        // Prevent form submission if Select2 field is not selected
        if ($selectElementFrom.val() === null || $selectElementFrom.val() === '' || $selectElementFrom.val() === undefined) {
            event.preventDefault();
            $selectElementFromLabel.addClass('select2-required');
        } else {
            $selectElementFromLabel.removeClass('select2-required');
        }
    },
    _onChangeToCities: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var $selectElementTo = $('#to_port_cities');
        var $selectElementToLabel = $('.select_to_port_cities_required');

        // Prevent form submission if Select2 field is not selected
        if ($selectElementTo.val() === null || $selectElementTo.val() === '' || $selectElementTo.val() === undefined) {
            event.preventDefault();
            $selectElementToLabel.addClass('select2-required');
        } else {
            $selectElementToLabel.removeClass('select2-required');
        }
    },
    _onChangeEquipmentTypeInland: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var EquipmentTypeElement = event.target;
        var value = EquipmentTypeElement.options[EquipmentTypeElement.selectedIndex].value;
        if (value === 'FTL') {
            this.$show_for_ftl_inland_div.show();
            this.$show_for_ltl_inland_div.hide();
        } else if (value === 'LTL') {
            this.$show_for_ftl_inland_div.hide();
            this.$show_for_ltl_inland_div.show();
        } else {
            this.$show_for_ftl_inland_div.hide();
            this.$show_for_ltl_inland_div.hide();
        }
    },
    _onChangeByUnitCheckbox: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var ByUnitCheckboxElement = event.target;
        if (ByUnitCheckboxElement.checked) {
            this.$show_for_by_unit_div.show();
            this.$hide_for_by_unit_div.hide();
        } else {
            this.$show_for_by_unit_div.hide();
            this.$hide_for_by_unit_div.show();
        }
    },
    _onChangeByUnitLCLCheckbox: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var ByUnitCheckboxElement = event.target;
        if (ByUnitCheckboxElement.checked) {
            this.$show_for_by_unit_lcl_div.show();
            this.$hide_for_by_unit_lcl_div.hide();
        } else {
            this.$show_for_by_unit_lcl_div.hide();
            this.$hide_for_by_unit_lcl_div.show();
        }
    },
    _onChangeByUnitLTLCheckbox: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var ByUnitCheckboxElement = event.target;
        if (ByUnitCheckboxElement.checked) {
            this.$show_for_by_unit_ltl_div.show();
            this.$hide_for_by_unit_ltl_div.hide();
        } else {
            this.$show_for_by_unit_ltl_div.hide();
            this.$hide_for_by_unit_ltl_div.show();
        }
    },
    _onAddRow: async function (event) {
        event.preventDefault();
        event.stopPropagation();
        var dynamicTable = this.$('table[id="dynamicTable_by_unit"]');
        this.rowCount = dynamicTable.find('tr').length - 1;
        var rowCount = this.rowCount || 0;
        const domain = [['tag_type_ids', '=', [this.$tag_type_air_id]]];
        const fields = ['id', 'name', 'tag_type_ids'];
        var $select = $('<select></select>').attr('name', 'package_type_air[]').attr('class', 'form-control link-style');

        // Add "Select..." option
        var $defaultOption = $('<option></option>')
            .attr('value', '')
            .text('Select...');
        $select.append($defaultOption);
        try {
            var all_data = await this.orm.call("package.type", "search_read", [domain, fields]);
            var data = all_data.filter(function(container) {
                return container.tag_type_ids.length === 1 && container.tag_type_ids[0] === 2;
            });
            data.forEach(function (container) {
                var $option = $('<option />').val(container.id).text(container.name);
                $select.append($option);
            });
        } catch (error) {
            console.error("Error fetching container types:", error);
            return;
        }
        var newRow = '<tr>' +
        '<td>' + (rowCount + 1) + '</td>' +
        '<td>' +
        $select.prop('outerHTML') + // Convert the jQuery object to a string of HTML
        '</td>' +
        '<td>' +
        '<input type="number" name="dimensions_l[]" class="form-control dimensions_l" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="dimensions_w[]" class="form-control dimensions_w" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="dimensions_h[]" class="form-control dimensions_h" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="quantity[]" class="form-control quantity" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="weight[]" class="form-control weight" />' +
        '</td>' +
        '<td>' +
        '<input name="chw[]" readonly="readonly" class="form-control chw" />' +
        '</td>' +
        '<td>' +
        '<button id="removeRow" class="btn btn-danger removeRow">Remove</button>' +
        '</td>' +
        '</tr>';
        dynamicTable.append(newRow);
        this.rowCount = rowCount + 1;
    },
    _onInsuranceCheckbox: function (event) {
        debugger;
        var checkbox = event.currentTarget;
        if (checkbox.checked && checkbox.dataset.name.toLowerCase() === 'insurance') {
            this.$insurance_textbox_div.show();
        } else {
            this.$insurance_textbox_div.hide();
        }
    },
    _onRemoveRowService: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var removeButton = $(event.target);
        var row = removeButton.closest('tr');
        row.remove();
        this.rowCount = this.rowCount - 1;
    },
    _onRemoveRow: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var removeButton = $(event.target);
        var row = removeButton.closest('tr');
        row.remove();
        this.rowCount = this.rowCount - 1;
    },
    _onAddRowLCL: async function (event) {
        event.preventDefault();
        event.stopPropagation();
        const domain = [['tag_type_ids', 'in', [this.$tag_type_lcl_id]]];
        const fields = ['id', 'name'];
        var dynamicTable = this.$('table[id="dynamicTable_by_unit_lcl"]');
        this.rowCountLCL = dynamicTable.find('tr').length - 1;
        var rowCountLCL = this.rowCountLCL || 0;
        var $select = $('<select></select>').attr('name', 'package_type_lcl[]').attr('class', 'form-control link-style');

        // Add "Select..." option
        var $defaultOption = $('<option></option>')
            .attr('value', '')
            .text('Select...');
        $select.append($defaultOption);
        try {
            var data = await this.orm.call("package.type", "search_read", [domain, fields]);
            data.forEach(function (container) {
                var $option = $('<option />').val(container.id).text(container.name);
                $select.append($option);
            });
        } catch (error) {
            console.error("Error fetching container types:", error);
            return;
        }
        var newRow = '<tr>' +
        '<td>' + (rowCountLCL + 1) + '</td>' +
        '<td>' +
        $select.prop('outerHTML') + // Convert the jQuery object to a string of HTML
        '</td>' +
        '<td>' +
        '<input type="number" name="dimensions_l_lcl[]" class="form-control dimensions_l_lcl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="dimensions_w_lcl[]" class="form-control dimensions_w_lcl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="dimensions_h_lcl[]" class="form-control dimensions_h_lcl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="quantity_lcl[]" class="form-control quantity_lcl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="weight_lcl[]" class="form-control weight_lcl" />' +
        '</td>' +
        '<td>' +
        '<input name="cbm_lcl[]" readonly="readonly" class="form-control cbm_lcl" />' +
        '</td>' +
        '<td>' +
        '<button id="removeRow_lcl[]" class="btn btn-danger removeRow_lcl">Remove</button>' +
        '</td>' +
        '</tr>';
        dynamicTable.append(newRow);
        this.rowCountLCL = rowCountLCL + 1;
    },
    _onRemoveRowLCL: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var removeButton = $(event.target);
        var row = removeButton.closest('tr');
        row.remove();
        this.rowCountLCL = this.rowCountLCL - 1;
    },
    _onAddRowLTL: async function (event) {
        event.preventDefault();
        event.stopPropagation();
        const domain = [['tag_type_ids', 'in', [this.$tag_type_lcl_id]]];
        const fields = ['id', 'name'];
        var dynamicTable = this.$('table[id="dynamicTable_by_unit_ltl"]');
        this.rowCountLTL = dynamicTable.find('tr').length - 1;
        var rowCountLTL = this.rowCountLTL || 0;
        var $select = $('<select></select>').attr('name', 'package_type_ltl[]').attr('class', 'form-control link-style');

        // Add "Select..." option
        var $defaultOption = $('<option></option>')
            .attr('value', '')
            .text('Select...');
        $select.append($defaultOption);
        try {
            var data = await this.orm.call("package.type", "search_read", [domain, fields]);
            data.forEach(function (container) {
                var $option = $('<option />').val(container.id).text(container.name);
                $select.append($option);
            });
        } catch (error) {
            console.error("Error fetching container types:", error);
            return;
        }
        var newRow = '<tr>' +
        '<td>' + (rowCountLTL + 1) + '</td>' +
        '<td>' +
        $select.prop('outerHTML') + // Convert the jQuery object to a string of HTML
        '</td>' +
        '<td>' +
        '<input type="number" name="dimensions_l_ltl[]" class="form-control dimensions_l_ltl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="dimensions_w_ltl[]" class="form-control dimensions_w_ltl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="dimensions_h_ltl[]" class="form-control dimensions_h_ltl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="quantity_ltl[]" class="form-control quantity_ltl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="weight_ltl[]" class="form-control weight_ltl" />' +
        '</td>' +
        '<td>' +
        '<input name="cbm_ltl[]" readonly="readonly" class="form-control cbm_ltl" />' +
        '</td>' +
        '<td>' +
        '<button id="removeRow_ltl" class="btn btn-danger removeRow_ltl">Remove</button>' +
        '</td>' +
        '</tr>';
        dynamicTable.append(newRow);
        this.rowCountLTL = rowCountLTL + 1;
    },
    _onRemoveRowLTL: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var removeButton = $(event.target);
        var row = removeButton.closest('tr');
        row.remove();
        this.rowCountLTL = this.rowCountLTL - 1;
    },
    _onAddRowFCL: async function (event) {
        event.preventDefault();
        event.stopPropagation();

        var dynamicTable = this.$('table[id="dynamicTable_fcl_sea"]');
        this.rowCountFCL = dynamicTable.find('tr').length - 1;
        var rowCountFCL = this.rowCountFCL || 0;
        var $select = $('<select></select>').attr('name', 'container_type[]').attr('class', 'form-control link-style');
        // Add "Select..." option
        var $defaultOption = $('<option></option>')
            .attr('value', '')
            .text('Select...');
        $select.append($defaultOption);

        try {
            var data = await this.orm.call("container.type", "search_read", []);
            data.forEach(function (container) {
                var $option = $('<option />').val(container.id).text(container.name);
                $select.append($option);
            });
        } catch (error) {
            console.error("Error fetching container types:", error);
            return;
        }

        var newRow = '<tr>' +
        '<td>' + (rowCountFCL + 1) + '</td>' +
        '<td>' +
        $select.prop('outerHTML') + // Convert the jQuery object to a string of HTML
        '</td>' +
        '<td>' +
        '<input type="number" name="quantity_for_volume_fcl[]" class="form-control quantity_fcl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="weight_for_volume_fcl[]" class="form-control weight_fcl" />' +
        '</td>' +
        '<td>' +
        '<button id="removeRow_fcl" class="btn btn-danger removeRow_fcl">Remove</button>' +
        '</td>' +
        '</tr>';
        dynamicTable.append(newRow);
        this.rowCountFCL = rowCountFCL + 1;
    },
    _onRemoveRowFCL: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var removeButton = $(event.target);
        var row = removeButton.closest('tr');
        row.remove();
        this.rowCountFCL = this.rowCountFCL - 1;
    },
    _onAddRowFTL: async function (event) {
        event.preventDefault();
        event.stopPropagation();

        var dynamicTable = this.$('table[id="dynamicTable_ftl_inland"]');
        this.rowCountFTL = dynamicTable.find('tr').length - 1;
        var rowCountFTL = this.rowCountFTL || 0;
        var $select = $('<select></select>').attr('name', 'container_type_ftl_inland[]').attr('class', 'form-control link-style');
        // Add "Select..." option
        var $defaultOption = $('<option></option>')
            .attr('value', '')
            .text('Select...');
        $select.append($defaultOption);

        try {
            var data = await this.orm.call("container.type", "search_read", []);
            data.forEach(function (container) {
                var $option = $('<option />').val(container.id).text(container.name);
                $select.append($option);
            });
        } catch (error) {
            console.error("Error fetching container types:", error);
            return;
        }

        var newRow = '<tr>' +
        '<td>' + (rowCountFTL + 1) + '</td>' +
        '<td>' +
        $select.prop('outerHTML') + // Convert the jQuery object to a string of HTML
        '</td>' +
        '<td>' +
        '<input type="number" name="quantity_ftl[]" class="form-control quantity_ftl" />' +
        '</td>' +
        '<td>' +
        '<input type="number" name="weight_ftl[]" class="form-control weight_ftl" />' +
        '</td>' +
        '<td>' +
        '<button id="removeRow_ftl" class="btn btn-danger removeRow_ftl">Remove</button>' +
        '</td>' +
        '</tr>';
        dynamicTable.append(newRow);
        this.rowCountFTL = rowCountFTL + 1;
    },
    _onRemoveRowFTL: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var removeButton = $(event.target);
        var row = removeButton.closest('tr');
        row.remove();
        this.rowCountFTL = this.rowCountFTL - 1;
    },
    _onInputChange_air: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var row = $(event.target).closest('tr');
        this._updateRowTotal_air(row);
    },
    _updateRowTotal_air: function (row) {
        var dimensions_l = parseFloat(row.find('.dimensions_l').val()) || 0;
        var dimensions_w = parseFloat(row.find('.dimensions_w').val()) || 0;
        var dimensions_h = parseFloat(row.find('.dimensions_h').val()) || 0;
        var quantity = parseFloat(row.find('.quantity').val()) || 0;
        var weight = parseFloat(row.find('.weight').val()) || 0;
        var cbm = dimensions_l * dimensions_w * dimensions_h / 1000000;
        var total = cbm / 0.006;
        total = total * quantity;
        if (weight > total){
            total = weight;
        }
        row.find('.chw').val(total.toFixed(2));
    },
    _onInputChange_lcl: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var row = $(event.target).closest('tr');
        this._updateRowTotal_lcl(row);
    },
    _updateRowTotal_lcl: function (row) {
        var dimensions_l = parseFloat(row.find('.dimensions_l_lcl').val()) || 0;
        var dimensions_w = parseFloat(row.find('.dimensions_w_lcl').val()) || 0;
        var dimensions_h = parseFloat(row.find('.dimensions_h_lcl').val()) || 0;
        var quantity = parseFloat(row.find('.quantity_lcl').val()) || 0;
        var weight = parseFloat(row.find('.weight_lcl').val()) || 0;
        var total = dimensions_l * dimensions_w * dimensions_h / 1000000;
        //        var total = vm / 6000;
        //        var gw = weight * quantity;
        //        if (gw > total){
        //            total = gw;
        //        }
        total = total * quantity;
        row.find('.cbm_lcl').val(total.toFixed(2));
    },
    _onInputChange_ltl: function (event) {
        event.preventDefault();
        event.stopPropagation();
        var row = $(event.target).closest('tr');
        this._updateRowTotal_ltl(row);
    },
    _updateRowTotal_ltl: function (row) {
        var dimensions_l = parseFloat(row.find('.dimensions_l_ltl').val()) || 0;
        var dimensions_w = parseFloat(row.find('.dimensions_w_ltl').val()) || 0;
        var dimensions_h = parseFloat(row.find('.dimensions_h_ltl').val()) || 0;
        var quantity = parseFloat(row.find('.quantity_ltl').val()) || 0;
        var weight = parseFloat(row.find('.weight_ltl').val()) || 0;
        var vm = dimensions_l * dimensions_w * dimensions_h;
        var total = vm / 1000000; // divide by million to get cubic meters
        total = total * quantity;
        total = total.toFixed(2); // round to 2 decimal places
        row.find('.cbm_ltl').val(total);
    },
    _onAddRowServiceNeeded: async function (event) {
        event.preventDefault();
        event.stopPropagation();
        const domain = [['active', '=', true]];
        const fields = ['id', 'name'];
        var dynamicTable = this.$('table[id="Table_service_needed"]');
        this.rowCountLTL = dynamicTable.find('tr').length - 1;
        var rowCountLTL = this.rowCountLTL || 0;
        var $select = $('<select></select>').attr('name', 'service_needed[]').attr('class', 'form-control link-style');

        // Add "Select..." option
        var $defaultOption = $('<option></option>')
            .attr('value', '')
            .text('Select...');
        $select.append($defaultOption);
        try {
            var data = await this.orm.call("service.scope", "search_read", [domain, fields]);
            data.forEach(function (container) {
                var $option = $('<option />').val(container.id).text(container.name);
                $select.append($option);
            });
        } catch (error) {
            console.error("Error fetching Service Needed:", error);
            return;
        }
        var newRow = '<tr>' +
        '<td>' + (rowCountLTL + 1) + '</td>' +
        '<td>' +
        $select.prop('outerHTML') + // Convert the jQuery object to a string of HTML
        '</td>' +
        '<td>' +
        '<button id="removeRow_service" class="btn btn-danger removeRow_ftl">Remove</button>' +
        '</td>' +
        '</tr>';
        dynamicTable.append(newRow);
        this.rowCountLTL = rowCountLTL + 1;
    },
    _onSubmit: function (event) {
        debugger;
        var self = this;
        var $form = $(event.currentTarget);
        var $selectedServices = this.$('input[name="service_needed[]"]:checked');
        var $insurance_amount = $('#insurance_details');
        if ($selectedServices.val() === '9') {
            if ($insurance_amount.val() === '' || $insurance_amount.val() === '0' || $insurance_amount.val() === 0) {
                event.preventDefault();
                $insurance_amount.addClass('select2-required');
            } else {
                $insurance_amount.removeClass('select2-required');
            }
        }

        var $selectElementFrom = $('#from_port_cities');
        var $selectElementTo = $('#to_port_cities');
        var $selectElementFromLabel = $('.select_from_port_cities_required');
        var $selectElementToLabel = $('.select_to_port_cities_required');

        // Prevent form submission if Select2 field is not selected
        if ($selectElementFrom.val() === null || $selectElementFrom.val() === '' || $selectElementFrom.val() === undefined) {
            event.preventDefault();
            $selectElementFromLabel.addClass('select2-required');
        } else {
            $selectElementFromLabel.removeClass('select2-required');
        }
        // Prevent form submission if Select2 field is not selected
        if ($selectElementTo.val() === null || $selectElementTo.val() === '' || $selectElementTo.val() === undefined) {
            event.preventDefault();
            $selectElementToLabel.addClass('select2-required');
        } else {
            $selectElementToLabel.removeClass('select2-required');
        }
    },
});
