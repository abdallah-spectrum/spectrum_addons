# -*- coding: utf-8 -*-

from odoo import models, fields, api


class fixDynamicReportBalanceSheet(models.TransientModel):
    _inherit='dynamic.balance.sheet.report'




    # fix dynamic report balance sheet in here
    # make shure the account object contain type
    @api.model
    def view_report(self, option, tag, lang):
        r = self.env['dynamic.balance.sheet.report'].search(
            [('id', '=', option[0])])
        data = {
            'display_account': r.display_account,
            'model': self,
            'journals': r.journal_ids,
            'target_move': r.target_move,
            'accounts': r.account_ids,
            'account_tags': r.account_tag_ids,
            'analytics': r.analytic_ids,
        }
        if r.date_from:
            data.update({
                'date_from': r.date_from,
            })
        if r.date_to:
            data.update({
                'date_to': r.date_to,
            })

        company_ids = self.env.companies.ids
        company_domain = [('company_id', 'in', company_ids)]
        if r.account_tag_ids:
            company_domain.append(
                ('tag_ids', 'in', r.account_tag_ids.ids))
        if r.account_ids:
            company_domain.append(('id', 'in', r.account_ids.ids))

        new_account_ids = self.env['account.account'].search(company_domain)
        data.update({'accounts': new_account_ids, })
        filters = self.get_filter(option)
        records = self._get_report_values(data)

        if filters['account_tags'] != ['All']:
            tag_accounts = list(map(lambda x: x.code, new_account_ids))

            def filter_code(rec_dict):
                if rec_dict['code'] in tag_accounts:
                    return True
                else:
                    return False

            new_records = list(filter(filter_code, records['Accounts']))
            records['Accounts'] = new_records
        # trans_tag = self.env['ir.translation'].search(
        #     [('value', '=', tag), ('module', '=', 'dynamic_accounts_report')],
        #     limit=1).src
        # if trans_tag:
        #     tag_upd = trans_tag
        # else:
        tag_upd = tag

        account_report_id = self.env['account.financial.report'].with_context(
            lang='en_US').search([
            ('name', 'ilike', tag_upd)])

        new_data = {'id': self.id, 'date_from': False,
                    'enable_filter': True,
                    'debit_credit': True,
                    'date_to': False, 'account_report_id': account_report_id,
                    'target_move': filters['target_move'],
                    'view_format': 'vertical',
                    'company_id': self.company_id,
                    'used_context': {'journal_ids': False,
                                     'state': filters['target_move'].lower(),
                                     'date_from': filters['date_from'],
                                     'date_to': filters['date_to'],
                                     'strict_range': False,
                                     'company_id': self.company_id,
                                     'lang': 'en_US'}}

        account_lines = self.get_account_lines(new_data)
        report_lines = self.view_report_pdf(account_lines, new_data)[
            'report_lines']
        move_line_accounts = []
        move_lines_dict = {}

        for rec in records['Accounts']:
            move_line_accounts.append(rec['id'])
            move_lines_dict[rec['id']] = {}
            move_lines_dict[rec['id']]['debit'] = rec['debit']
            move_lines_dict[rec['id']]['credit'] = rec['credit']
            move_lines_dict[rec['id']]['balance'] = rec['balance']
        report_lines_move = []
        parent_list = []

        def filter_movelines_parents(obj):
            for each in obj:
                if each['report_type'] == 'accounts':
                    if each.get('account') and each['account'] in move_line_accounts:
                        report_lines_move.append(each)
                        parent_list.append(each['p_id'])

                elif each['report_type'] == 'account_report':
                    report_lines_move.append(each)
                else:
                    report_lines_move.append(each)

        filter_movelines_parents(report_lines)

        for rec in report_lines_move:
            if rec['report_type'] == 'accounts':
                if rec['account'] in move_line_accounts:
                    rec['debit'] = move_lines_dict[rec['account']]['debit']
                    rec['credit'] = move_lines_dict[rec['account']]['credit']
                    rec['balance'] = move_lines_dict[rec['account']]['balance']

        parent_list = list(set(parent_list))
        max_level = 0
        for rep in report_lines_move:
            if rep['level'] > max_level:
                max_level = rep['level']

        def get_parents(obj):
            for item in report_lines_move:
                for each in obj:
                    if item['report_type'] != 'account_type' and \
                            each in item['c_ids']:
                        obj.append(item['r_id'])
                if item['report_type'] == 'account_report':
                    obj.append(item['r_id'])
                    break

        get_parents(parent_list)
        for i in range(max_level):
            get_parents(parent_list)

        parent_list = list(set(parent_list))
        final_report_lines = []
        for rec in report_lines_move:
            if rec['report_type'] != 'accounts':
                if rec['r_id'] in parent_list:
                    final_report_lines.append(rec)
            else:
                final_report_lines.append(rec)
        def filter_sum(obj):
            sum_list = {}
            for pl in parent_list:
                sum_list[pl] = {}
                sum_list[pl]['s_debit'] = 0
                sum_list[pl]['s_credit'] = 0
                sum_list[pl]['s_balance'] = 0

            for each in obj:
                if each['p_id'] and each['p_id'] in parent_list:
                    sum_list[each['p_id']]['s_debit'] += each['debit']
                    sum_list[each['p_id']]['s_credit'] += each['credit']
                    sum_list[each['p_id']]['s_balance'] += each['balance']
            return sum_list

        def assign_sum(obj):
            for each in obj:
                if each['r_id'] in parent_list and \
                        each['report_type'] != 'account_report':
                    each['debit'] = sum_list_new[each['r_id']]['s_debit']
                    each['credit'] = sum_list_new[each['r_id']]['s_credit']

        for p in range(max_level):
            sum_list_new = filter_sum(final_report_lines)
            assign_sum(final_report_lines)

        company_id = self.env.company
        currency = company_id.currency_id
        symbol = currency.symbol
        rounding = currency.rounding
        position = currency.position

        for rec in final_report_lines:
            rec['debit'] = round(rec['debit'], 2)
            rec['credit'] = round(rec['credit'], 2)
            rec['balance'] = rec['debit'] - rec['credit']
            rec['balance'] = round(rec['balance'], 2)
            if (rec['balance_cmp'] < 0 and rec['balance'] > 0) or (
                    rec['balance_cmp'] > 0 and rec['balance'] < 0):
                rec['balance'] = rec['balance'] * -1

            if position == "before":
                rec['m_debit'] = symbol + " " + "{:,.2f}".format(rec['debit'])
                rec['m_credit'] = symbol + " " + "{:,.2f}".format(
                    rec['credit'])
                rec['m_balance'] = symbol + " " + "{:,.2f}".format(
                    rec['balance'])
            else:
                rec['m_debit'] = "{:,.2f}".format(rec['debit']) + " " + symbol
                rec['m_credit'] = "{:,.2f}".format(
                    rec['credit']) + " " + symbol
                rec['m_balance'] = "{:,.2f}".format(
                    rec['balance']) + " " + symbol
        return {
            'name': tag,
            'type': 'ir.actions.client',
            'tag': tag,
            'filters': filters,
            'report_lines': records['Accounts'],
            'debit_total': records['debit_total'],
            'credit_total': records['credit_total'],
            'debit_balance': records['debit_balance'],
            'currency': currency,
            'bs_lines': final_report_lines,
            'lang': self.env.context.get('lang') or 'en_US'
        }


