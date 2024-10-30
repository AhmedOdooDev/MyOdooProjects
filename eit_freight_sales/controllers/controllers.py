import base64

from odoo import http, _
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.exceptions import AccessError
import logging

_logger = logging.getLogger(__name__)

class FreightController(AuthSignupHome):
    @http.route('/web/shipping-request', type='http', auth='public', website=True,
                sitemap=False)
    def web_shipping_request(self, *args, **kw):
        air_id = request.env['transport.type'].sudo().search([('code', '=', 'AIR')], limit=1).id
        sea_id = request.env['transport.type'].sudo().search([('code', '=', 'SEA')], limit=1).id
        inland_id = request.env['transport.type'].sudo().search([('code', '=', 'LND')], limit=1).id
        user = request.env.user
        is_public_user = user._is_public()
        tag_type_air_id = request.env['package.tag.type'].sudo().search([
            ('name', 'in', ['AIR'])
        ])
        tag_type_lcl_id = request.env['package.tag.type'].sudo().search([
            ('name', 'in', ['LCL'])
        ])
        package_type = request.env['package.type'].sudo().search([('tag_type_ids', 'in', tag_type_air_id.ids)], order='name ASC')
        package_type_lcl = request.env['package.type'].sudo().search([('tag_type_ids', 'in', tag_type_lcl_id.ids)], order='name ASC')
        _logger.error("------------IT IS Error-----------")
        return request.render('eit_freight_sales.request_quote',
                              {
                                  'transport_type': request.env['transport.type'].sudo().search([]),
                                  'equipment_type_for_sea': request.env['shipment.scop'].sudo().search(
                                      [('type', '=', 'sea')]),
                                  'equipment_type_for_inland': request.env['shipment.scop'].sudo().search(
                                      [('type', '=', 'inland')]),
                                  'container_type': request.env['container.type'].sudo().search([]),
                                  'tag_type_air_id': tag_type_air_id.id,
                                  'tag_type_lcl_id': tag_type_lcl_id.id,
                                  'package_type': package_type,
                                  'package_type_lcl': package_type_lcl,
                                  'package_type_ltl': package_type_lcl,
                                  'from_port_cities': request.env['port.cites'].sudo().search([]),
                                  'to_port_cities': request.env['port.cites'].sudo().search([]),
                                  'service_needed_list': request.env['service.scope'].sudo().search([]),
                                  'air_id': air_id,
                                  'sea_id': sea_id,
                                  'inland_id': inland_id,
                                  'is_public_user': is_public_user,
                                  'commodity': request.env['commodity.group'].sudo().search([]),
                                  'company': request.env['res.company'].sudo().search([])
                              })

    @http.route('/web/shipping-request', type='http', auth="public", methods=['POST'], website=True)
    def shipping_request(self, **kwargs):
        # Extract form data
        transport_type_id = kwargs.get('transport_type') or ''
        service_needed = request.httprequest.form.getlist('service_needed[]')
        dimensions_l = request.httprequest.form.getlist('dimensions_l[]')
        dimensions_w = request.httprequest.form.getlist('dimensions_w[]')
        dimensions_h = request.httprequest.form.getlist('dimensions_h[]')
        quantity = request.httprequest.form.getlist('quantity[]')
        weight = request.httprequest.form.getlist('weight[]')
        by_unit = True if kwargs.get('by_unit_checkbox') == 'on' else False
        by_unit_lcl = True if kwargs.get('by_unit_lcl_checkbox') == 'on' else False
        by_unit_ltl = True if kwargs.get('by_unit_ltl_checkbox') == 'on' else False
        weight_for_volume = request.httprequest.form.getlist('weight_for_volume[]')
        volume_for_volume = request.httprequest.form.getlist('volume_for_volume[]')
        quantity_for_volume_fcl = request.httprequest.form.getlist('quantity_for_volume_fcl[]')
        weight_for_volume_fcl = request.httprequest.form.getlist('weight_for_volume_fcl[]')
        weight_for_volume_ltl = request.httprequest.form.getlist('weight_for_volume_ltl[]')
        volume_for_volume_ltl = request.httprequest.form.getlist('volume_for_volume_ltl[]')
        weight_for_volume_lcl = request.httprequest.form.getlist('weight_for_volume_lcl[]')
        volume_for_volume_lcl = request.httprequest.form.getlist('volume_for_volume_lcl[]')
        equipment_type_for_sea = kwargs.get('equipment_type_for_sea')
        equipment_type_for_inland = kwargs.get('equipment_type_for_inland')
        container_type_id = request.httprequest.form.getlist('container_type[]')
        container_type_ftl_inland_id = request.httprequest.form.getlist('container_type_ftl_inland[]')
        dimensions_l_lcl = request.httprequest.form.getlist('dimensions_l_lcl[]')
        dimensions_w_lcl = request.httprequest.form.getlist('dimensions_w_lcl[]')
        dimensions_h_lcl = request.httprequest.form.getlist('dimensions_h_lcl[]')
        quantity_lcl = request.httprequest.form.getlist('quantity_lcl[]')
        weight_lcl = request.httprequest.form.getlist('weight_lcl[]')
        package_type_air_id = request.httprequest.form.getlist('package_type_air[]') or ''
        package_type_ltl_id = request.httprequest.form.getlist('package_type_ltl[]') or ''
        package_type_lcl_id = request.httprequest.form.getlist('package_type_lcl[]') or ''
        dimensions_l_ltl = request.httprequest.form.getlist('dimensions_l_ltl[]')
        dimensions_w_ltl = request.httprequest.form.getlist('dimensions_w_ltl[]')
        dimensions_h_ltl = request.httprequest.form.getlist('dimensions_h_ltl[]')
        quantity_ltl = request.httprequest.form.getlist('quantity_ltl[]')
        weight_ltl = request.httprequest.form.getlist('weight_ltl[]')
        quantity_ftl = request.httprequest.form.getlist('quantity_ftl[]')
        weight_ftl = request.httprequest.form.getlist('weight_ftl[]')
        cbm_ltl = request.httprequest.form.getlist('cbm_ltl[]')
        cbm_lcl = request.httprequest.form.getlist('cbm_lcl[]')
        chw = request.httprequest.form.getlist('chw[]')
        from_port_cities_id = kwargs.get('from_port_cities')
        to_port_cities_id = kwargs.get('to_port_cities')
        commodity_id = kwargs.get('commodity')
        cargo_readiness_date = kwargs.get('cargo_readiness_date')
        additional_information = kwargs.get('additional_information')
        contact_name = kwargs.get('contact_name')
        contact_email = kwargs.get('contact_email')
        contact_company = kwargs.get('contact_company')
        country_code = kwargs.get('country_code')
        contact_phone = kwargs.get('contact_phone')

        try:

            # Create CRM Lead
            lead_vals = {
                'transport_type_id': int(transport_type_id),
                'additional_information': additional_information,
                'pol_id': int(from_port_cities_id),
                'pod_id': int(to_port_cities_id),
                'commodity_group_id': int(commodity_id),
                'cargo_readiness_date': cargo_readiness_date,
                'email_from': contact_email,
                'partner_name': contact_company,
                'phone': f"{country_code} {contact_phone}",
                'type': 'opportunity',
                'is_from_website': True,
            }
            print ("lead_valslead_vals", lead_vals)
            shipping_info_vals = []

            transport_type = request.env['transport.type'].sudo().browse(int(transport_type_id))
            if transport_type.code == 'LND':
                equipment_type = request.env['shipment.scop'].sudo().search([('code', '=', equipment_type_for_inland)],
                                                                            limit=1)
                lead_vals['shipment_scope_id'] = equipment_type.id
                if equipment_type.code == 'FTL':
                    for i in range(len(container_type_ftl_inland_id)):
                        shipping_info_vals.append((0, 0, {
                            'container_type_id': int(container_type_ftl_inland_id[i]) if container_type_ftl_inland_id[
                                i] else False,
                            'qty': int(quantity_ftl[i]) if quantity_ftl[i] else 0.0,
                            'gw_kg': float(weight_ftl[i]) if weight_ftl[i] else 0.0,
                        }))
                elif equipment_type.code == 'LTL':
                    lead_vals['by_unit'] = by_unit_ltl
                    if by_unit_ltl:
                        for i in range(len(package_type_ltl_id)):
                            shipping_info_vals.append((0, 0, {
                                'package_type_id': int(package_type_ltl_id[i]) if package_type_ltl_id[i] else False,
                                'length_cm': float(dimensions_l_ltl[i]) if dimensions_l_ltl[i] else 0.0,
                                'width_cm': float(dimensions_w_ltl[i]) if dimensions_w_ltl[i] else 0.0,
                                'height_cm': float(dimensions_h_ltl[i]) if dimensions_h_ltl[i] else 0.0,
                                'qty': int(quantity_ltl[i]) if quantity_ltl[i] else 0.0,
                                'gw_kg': float(weight_ltl[i]) if weight_ltl[i] else 0.0,
                                'cbm': float(cbm_ltl[i]) if cbm_ltl[i] else 0.0,
                            }))
                    else:
                        for i in range(len(weight_for_volume_ltl)):
                            shipping_info_vals.append((0, 0, {
                                'gw_kg': float(weight_for_volume_ltl[i]) if weight_for_volume_ltl[i] else 0.0,
                                'cbm': float(volume_for_volume_ltl[i]) if volume_for_volume_ltl[i] else 0.0,
                            }))
            elif transport_type.code == 'SEA':
                equipment_type = request.env['shipment.scop'].sudo().search([('code', '=', equipment_type_for_sea)],
                                                                            limit=1)
                lead_vals['shipment_scope_id'] = equipment_type.id
                if equipment_type.code == 'FCL':
                    for i in range(len(container_type_id)):
                        shipping_info_vals.append((0, 0, {
                            'container_type_id': int(container_type_id[i]),
                            'qty': int(quantity_for_volume_fcl[i]) if quantity_for_volume_fcl[i] else 0.0,
                            'gw_kg': float(weight_for_volume_fcl[i]) if weight_for_volume_fcl[i] else 0.0,
                        }))
                elif equipment_type.code == 'LCL':
                    lead_vals['by_unit'] = by_unit_lcl
                    if by_unit_lcl:
                        for i in range(len(package_type_lcl_id)):
                            shipping_info_vals.append((0, 0, {
                                'package_type_id': int(package_type_lcl_id[i]) if package_type_lcl_id[i] else False,
                                'length_cm': float(dimensions_l_lcl[i]) if dimensions_l_lcl[i] else 0.0,
                                'width_cm': float(dimensions_w_lcl[i]) if dimensions_w_lcl[i] else 0.0,
                                'height_cm': float(dimensions_h_lcl[i]) if dimensions_h_lcl[i] else 0.0,
                                'qty': int(quantity_lcl[i]) if quantity_lcl[i] else 0.0,
                                'gw_kg': float(weight_lcl[i]) if weight_lcl[i] else 0.0,
                                'cbm': float(cbm_lcl[i]) if cbm_lcl[i] else 0.0,
                            }))
                    else:
                        for i in range(len(weight_for_volume_lcl)):
                            shipping_info_vals.append((0, 0, {
                                'weight': float(weight_for_volume_lcl[i]) if weight_for_volume_lcl[i] else 0.0,
                                'cbm': float(volume_for_volume_lcl[i]) if volume_for_volume_lcl[i] else 0.0,
                            }))
            elif transport_type.code == 'AIR':
                lead_vals['by_unit'] = by_unit
                if by_unit:
                    for i in range(len(package_type_air_id)):
                        length_cm = float(dimensions_l[i]) if dimensions_l[i] else 0.0
                        width_cm = float(dimensions_w[i]) if dimensions_w[i] else 0.0
                        height_cm = float(dimensions_h[i]) if dimensions_h[i] else 0.0
                        shipping_info_vals.append((0, 0, {
                            'package_type_id': int(package_type_air_id[i]) if package_type_air_id[i] else False,
                            'length_cm': length_cm,
                            'width_cm': width_cm,
                            'height_cm': height_cm,
                            'qty': int(quantity[i]) if quantity[i] else 0.0,
                            'cbm': length_cm * width_cm * height_cm / 1000,
                            'gw_kg': float(weight[i]) if weight[i] else 0.0,
                            'chw': float(chw[i]) if chw[i] else 0.0,
                        }))
                else:
                    for i in range(len(weight_for_volume)):
                        shipping_info_vals.append((0, 0, {
                            'weight': float(weight_for_volume[i]) if weight_for_volume[i] else 0.0,
                            'volume': float(volume_for_volume[i]) if volume_for_volume[i] else 0.0,
                        }))

            # Create a new CRM opportunity record and link the shipping info
            # Search for an existing partner or create a new one

            is_public_user = request.env.user._is_public()
            partner = request.env.user.partner_id if not is_public_user else None
            if is_public_user and contact_email:
                partner = request.env['res.partner'].sudo().search([('email', '=', contact_email)], limit=1)
                if not partner:
                    partner = request.env['res.partner'].sudo().create({
                        'name': contact_name,
                        'email': contact_email,
                        'company_name': contact_company,
                        'phone': f'{country_code} {contact_phone}'
                    })
                existing_user = request.env['res.users'].sudo().search([('partner_id', '=', partner.id)], limit=1)
                if not existing_user:
                    user = request.env['res.users'].sudo().create({
                        'name': contact_name,
                        'login': contact_email,
                        'password': 'password',
                        'email': contact_email,
                        'partner_id': partner.id,
                        'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
                    })
                    # Generate a signup token for the user
                    try:
                        user.sudo().action_reset_password()
                    except AccessError:
                        pass

                    # Send the password reset email
                    template = request.env.ref('auth_signup.mail_template_user_signup_account_created')
                    if template:
                        template.sudo().send_mail(user.id, force_send=True)

            lead_vals['partner_id'] = partner.id
            if transport_type.code == 'AIR':
                lead_vals['air_package_type_ids'] = shipping_info_vals
            else:
                if transport_type.code == 'LND':
                    equipment_type = request.env['shipment.scop'].sudo().search(
                        [('code', '=', equipment_type_for_inland)],
                        limit=1)
                    lead_vals['shipment_scope_id'] = equipment_type.id
                    if equipment_type.code == 'FTL':
                        lead_vals['container_type_ids'] = shipping_info_vals
                    else:
                        lead_vals['non_air_package_type_ids'] = shipping_info_vals
                elif transport_type.code == 'SEA':
                    equipment_type = request.env['shipment.scop'].sudo().search([('code', '=', equipment_type_for_sea)],
                                                                                limit=1)
                    lead_vals['shipment_scope_id'] = equipment_type.id
                    if equipment_type.code == 'FCL':
                        lead_vals['container_type_ids'] = shipping_info_vals
                    else:
                        lead_vals['non_air_package_type_ids'] = shipping_info_vals
            # lead_vals['container_lines_ids'] = shipping_info_vals
            # Convert service_needed to the correct format
            service_needed_ids = [int(item) for item in service_needed]
            lead_vals['service_needed_ids'] = [(6, 0, service_needed_ids)]
            crm_lead = request.env['crm.lead'].sudo().create(lead_vals)

            # Handle file upload
            uploaded_file = request.httprequest.files.get('file_upload')
            attachment_id = False
            if uploaded_file:
                file_name = uploaded_file.filename
                file_content = uploaded_file.read()
                attachment_id = request.env['ir.attachment'].sudo().create({
                    'name': file_name,
                    'type': 'binary',
                    'datas': base64.b64encode(file_content),
                    'store_fname': file_name,
                    'res_model': 'crm.lead',
                    'res_id': crm_lead.id,
                    'public': True,
                }).id

            # Attach the uploaded file to the lead
            if attachment_id:
                crm_lead.sudo().message_post(
                    body="attachments from online request a quote",
                    subject="File Upload",
                    message_type='comment',
                    subtype_id=request.env.ref('mail.mt_comment').id,
                    attachment_ids=[attachment_id]
                )

            return request.redirect('/thank-you')
        except Exception as e:
            return False

    @http.route('/thank-you', type='http', auth='public', website=True, sitemap=False)
    def thank_you(self, *args, **kw):
        return request.render('eit_freight_sales.thank_you_page')
