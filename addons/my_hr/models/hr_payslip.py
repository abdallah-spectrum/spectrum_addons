from odoo import api, fields, models, _
from pprint import pprint
from datetime import datetime,timedelta
import calendar

class HrPayslip(models.Model): 
  _inherit = 'hr.payslip'

  
  def compute_tax(self,payslip,contract,categories):
    if  bool(contract.tax_id) is not False:
        rules = contract.env["hr.salary.rule"].search_read([("code", "=", 'prin')])
        taxed_yearly_income =0 	
        tax_values = []        
        tax_segments2 = contract.env["tax.detail"].search_read(['&', ("tax_id", "=", contract.tax_id.id),('ultimate_flag', '=', False)])
        ultimate_val = contract.env["tax.main"].search_read([("id", "=", contract.tax_id.id)], fields=["max_val"])[0]['max_val']
        segment_max = 0
        if taxed_yearly_income < ultimate_val:
          for i, tax_segment in enumerate(tax_segments2):
            if taxed_yearly_income < tax_segment['min_val']:
              segment_max = i
            else:
              segment_max = len(tax_segments2)
          for j in range(len(tax_segments2)):
            value = tax_segments2[j]
            min_val = value['min_val'] 
            max_val = value['max_val'] 
            percentage = value['percentage']
            difference = min(taxed_yearly_income,(max_val - min_val))
            taxed_yearly_income -= difference
            tax_value = difference * percentage 
            tax_values.append(tax_value)  
        else:
          ultimate_segments = contract.env["tax.detail"].search_read(['&', ("tax_id", "=", contract.tax_id.id),('ultimate_flag', '=', True)], fields=["name","min_val","max_val","starting_from","ultimate_flag"])
          for ultimate_segment in ultimate_segments:
            ultimate_max_val = ultimate_segment['max_val']
            ultimate_min_val = ultimate_segment['min_val']
            starting_from = ultimate_segment['starting_from']
            if ultimate_min_val <= taxed_yearly_income < ultimate_max_val:
              segment_max = starting_from            
          curr_value = tax_segments2[segment_max]
          curr_max_val = curr_value['max_val'] 
          curr_percentage = curr_value['percentage'] 
          taxed_yearly_income -= curr_max_val
          curr_tax_value = curr_max_val * curr_percentage 
          tax_values.append(curr_tax_value)

          for j in range(segment_max+1,len(tax_segments2)):
            value = tax_segments2[j]
            min_val = value['min_val'] 
            max_val = value['max_val'] 
            percentage = value['percentage'] 
            difference = min(taxed_yearly_income,(max_val - min_val))
            taxed_yearly_income -= difference
            tax_value = difference * percentage 
            tax_values.append(tax_value)

        result=sum(tax_values) / 12
    else:
        result=0
    return result