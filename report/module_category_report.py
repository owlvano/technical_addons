# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models

class ModuleCategoryReport(models.Model):
    _name = "tech.add.module.category.report"
    _description = "Module Category Overview"
    _auto = False

    category_id = fields.Many2one('ir.module.category', string='Application', readonly=True)
    group_id = fields.Many2one('res.groups', string='Groups', readonly=True)
    user_id = fields.Many2one('res.users', "Users", readonly=True)

    def _query_module_category(self):
        query_str = """
            SELECT
                a.id as category_id,
                g.id as group_id,
                u.id as user_id
            FROM (
            	ir_module_category a
            		left join res_groups g on (g.category_id=a.id)
                    left join res_groups_users_rel rel on (rel.gid=g.id)
            		left join res_users u on (u.id=rel.uid)
            )
            GROUP BY
                a.id,
                g.id,
                u.id
        """
        return query_str
    
    @api.model_cr
    def init(self):
        # self._table = price_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE OR REPLACE VIEW %s AS (
            WITH result AS (
                %s
            )
            SELECT row_number() OVER () AS id, * 
            FROM  result
        )
        """ % (self._table, self._query_module_category()))
