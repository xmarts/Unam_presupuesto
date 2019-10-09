# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date, timedelta
import tempfile
import base64
import os
import binascii
import xlrd
from random import randint


class budget_program(models.Model):
    _name = 'budget.program'

    code =  fields.Char(string='Código',required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
    budget_subprogam_id = fields.Many2one('budget.subprogram',string="Subprograma")

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.program'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class budget_subprogram(models.Model):#se crea este modelo  SubPrograma (SP) con los siguientes campos 
    _name = 'budget.subprogram'

    code =  fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
    branch_id = fields.Many2one('res.branch',string="Dependencia",required=True,)
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencia",required=True)
    program_id = fields.Many2one('budget.program',string="Programa",required=True)
    
    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.subprogram'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class campos_nuevos_branch(models.Model):#Este es un inherit al modelo del branch ,Dependencia (DEP).
    _inherit = 'res.branch'

    code = fields.Char(string="Código",required=True,size=3)
    head = fields.Many2one('hr.employee',string="Titular",required=True)
    secretary = fields.Many2one('hr.employee',string="Secretario Administrativo",required=True)
    No_dependence = fields.Char(string="No. entidad o dependencia",required=True)
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencias")

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '00'+obj.code
                if len(val)==2:
                    obj.code = '0'+obj.code 
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['res.branch'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class  budget_subdependence(models.Model):#Modelo Subdependencia (SD)
    _name = 'budget.subdependence'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
    branch_id = fields.Many2one('res.branch',string="Dependencia",required=True,)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.subdependence'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único por dependencia'))

class budget_item(models.Model):#Modelo para Partida de Gasto (PAR).
    _name = 'budget.item'

    code = fields.Char(string="Partida",required=True,size=3)
    name = fields.Char(string="Nombre",required=True)
    type_item = fields.Selection([('Regulada','R'),('Centralizada','C'),('Directa','D')],string="Tipo de ejercicio",required=True)
    description = fields.Char(string="Descripción")
    cogconac_id  = fields.Many2one('budget.cog.conac',string="COG CONAC",required=True)
    cogshcp_id = fields.Many2one('budget.item.conversion',string="COG SHCP",required=True)
    expense_account = fields.Many2one('account.account',string="Cuenta de gastos",required=True)
    debtor_account = fields.Many2one('account.account', string="Cuenta pasivo deudora",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '00'+obj.code
                if len(val)==2:
                    obj.code = '0'+obj.code 
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.item'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class budget_resource_origin(models.Model):#Modelo para Origen del Recurso(OR).
    _name = 'budget.resource.origin'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
    is_income_owne = fields.Boolean(string='Si')
    is_income_owne2 = fields.Boolean(string='No')
    observations = fields.Char(string="Observaciones")

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.resource.origin'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

    #funcion para solo selecionar u solo boleano         
    @api.onchange('is_income_owne','is_income_owne2')
    def _onchange_seletion(self):
        if  self.is_income_owne == True:
            self.is_income_owne2 = False
        elif self.is_income_owne ==False: 
            self.is_income_owne2 == True    

class budget_institutional_activity(models.Model):# Modelo para Actividad Institucional(AI).
    _name = 'budget.institutional.activity'

    code = fields.Char(string="Código",required=True,size=5)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '0000'+obj.code
                if len(val)==2:
                    obj.code = '000'+obj.code 
                if len(val)==3:
                    obj.code = '00'+obj.code
                if len(val)==4:
                    obj.code ='0'+obj.code        
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.institutional.activity'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))


class budget_program_conversion(models.Model):#modelo para Conversión de Programa Presupuestario(CONPP).
    _name = 'budget.program.conversion'

    code = fields.Char(string="Código",required=True,size=4)
    name = fields.Char(string="Nombre",required=True)
    cogshcp_id = fields.Many2one('budget.item.conversion',string="PP SHCP",required=True)
    activity = fields.Selection([('bachillerato','Bachillerato'),('licenciatura','Licenciatura'),('posgrado','Posgrado'),('becas','Becas'),('cultura','Cultura'),('mantenimiento','Mantenimiento'),('obras','Obras')],string="Actividad",required=True)

    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit()==False:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.program.conversion'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))



class budget_item_conversion(models.Model):#modelo para Conversión con partida (CONPA).
    _name = 'budget.item.conversion'

    code = fields.Char(string="Código (partida)",required=True,size=5)
    name = fields.Char(string="Nombre",required=True)
    item_number = fields.Many2one('budget.item',string="Partida")
    type_item = fields.Selection([('Regulada','R'),('Centralizada','C'),('Directa','D')],string="Tipo de ejercicio",required=True)
    cogconac_id = fields.Many2one('budget.cog.conac',string="COG CONAC",required=True)


    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '0000'+obj.code
                if len(val)==2:
                    obj.code = '000'+obj.code 
                if len(val)==3:
                    obj.code = '00'+obj.code
                if len(val)==4:
                    obj.code ='0'+obj.code        
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.item.conversion'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único por partida.'))


class budget_expense_type(models.Model):# modelo para Tipo de gasto (TG).
    _name = 'budget.expense.type'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
    
    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.expense.type'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class budget_geographic_location(models.Model):#modelo para Ubicación Geográfica (UG).
    _name = 'budget.geographic.location'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)
    
    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.geographic.location'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class budget_key_portfolio(models.Model):#modelo Clave cartera(CC).
    _name = 'budget.key.portfolio'

    code = fields.Char(string="Código",required=True,size=4)
    name = fields.Char(string="Nombre",required=True)
    description = fields.Char(string="Descripción")
    entity_id = fields.Many2one('budget.geographic.location',string="Entidad",required=True)
    type_program = fields.Selection([('1','Proyecto de Inversión de Infraestructura social'),('2','Programa de Inversión de Mantenimiento'),('3','Programa de Inversión de Adquisiciones')],string="Tipo de programa o proyecto",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '000'+obj.code
                if len(val)==2:
                    obj.code = '00'+obj.code
                if len(val)==3:
                    obj.code ='0'+obj.code    
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.key.portfolio'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))
class budget_project_type(models.Model):#modelo para el Tipo de proyecto(TP).
    _name = 'budget.project.type'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocomplementar y que solo sean esnteros y la duplicidad 
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit()==False:
                raise ValidationError(_('Valor Invalido.'))
            else:
                if  val.isdigit():
                    if len(val)<=1:
                        raise ValidationError(_('Falta completar los caracteres necesarios del código.'))    
        rec = self.env['budget.project.type'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))


class project_project_Modificar(models.Model):# modelo para Proyectos (NP). haciendo inherit al modelo project.project
    _inherit = 'project.project'


    code = fields.Char(string="Código",required=True, size=5 )#aki falta lo relacionado al account.analityc.accoun
    type_project_id = fields.Many2one('budget.project.type',string="Tipo de proyecto",required=True)
    sub_type = fields.Selection([('spp','(SPP) Sistema de pagos a proveedores de bienes y prestadores de servicio.'),('cbc','(CBC) Cuenta bancaria con chequera.')],string="Subtipo de proyecto",required=True)
    amount_allocated = fields.Monetary(string="Monto asignado",required=True)
    consumed_amount = fields.Monetary(string="Monto ejercido",required=True)
    date_start1 = fields.Date(string='Fecha de inicio del proyecto',required=True)
    date1 = fields.Date(string='Fecha final del proyecto',required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)==1:
                    obj.code = '0000'+obj.code
                if len(val)==2:
                    obj.code = '000'+obj.code
                if len(val)==3:
                    obj.code = '00'+obj.code
                if len(val)==4:
                    obj.code = '0'+obj.code 
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['project.project'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class budget_stage(models.Model):#modelo para Etapa(E).
    _name = 'budget.stage'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.stage'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class  budget_agreement_type(models.Model):#modelo para Tipo de convenio(TC).
    _name = 'budget.agreement.type'

    code = fields.Char(string="Código",required=True,size=2)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.agreement.type'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))


class agreement_agreement(models.Model):#modelo para Convenios(NC)
    _name = 'agreement.agreement'

    code = fields.Char(string="Código",required=True,size=6)
    name = fields.Char(string="Nombre",required=True)
    agreement_type_id = fields.Many2one('budget.agreement.type',string="Tipo de convenio",required=True)
    branch_id = fields.Many2one('res.branch',string="Dependencia",required=True)
    budget_subdependence_id = fields.Many2one('budget.subdependence',string="Subdepencencia",required=True)

    #funcion para autocomplementar y que solo sean esnteros y la duplicidad 
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit()==False:
                raise ValidationError(_('Valor Invalido.'))
            else:
                if  val.isdigit():
                    if len(val)<=5:
                        raise ValidationError(_('Falta completar los caracteres necesarios del código.'))    
        rec = self.env['agreement.agreement'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))



class budget_cog_conac(models.Model):#modelo para Catálogo COG CONAC ()
    _name = 'budget.cog.conac'

    code = fields.Char(string="Código",required=True)
    name = fields.Char(string="Nombre",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('code')
    def _check_code(self):
        for obj in self: 
            val = obj.code
            if val.isdigit():
                if len(val)<=1:
                    obj.code = '0'+obj.code
            else:
                raise ValidationError(_('Valor Invalido'))
        rec = self.env['budget.cog.conac'].search(
        [('code', '=', self.code),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))

class budget_structure(models.Model):#modelo para Orden del código programático.
    _name = 'budget.structure'

    sequence = fields.Char(string="Secuencia",required=True)
    name = fields.Char(string="Nombre",required=True)
    catalog_id = fields.Many2one('ir.model',string="catalog_id")
    position_from  = fields.Integer(string='Posición inicial',required=True)
    position_to  = fields.Integer(string="Posición final",required=True)

    #funcion para autocompletar con un cero ala izquierda y validar que el codigo no se repirta y sea unico.
    @api.constrains('sequence')
    def _check_code(self):
        for obj in self: 
            val = obj.sequence

            if val.isdigit()==False:
                raise ValidationError(_('Valor Invalido'))
            if val.isdigit():
                busca = self.env['budget.structure'].search(
                    [('catalog_id','=',self.catalog_id.id),('sequence', '!=', self.sequence)],limit=1)
                if busca:
                    raise ValidationError(_('Catálogo duplicado, solo puede haber un registro por catálogo '))   

        rec = self.env['budget.structure'].search(
        [('sequence', '=', self.sequence),('id', '!=', self.id)])
        if rec:
            raise ValidationError(_('Valor duplicado, el código debe ser único.'))
 

class c_nuevos_asientos_contables(models.Model):#modelo para Asientos contables,el cual hace un inherit al modelo  account.move.lines agregando los siguientes campos
    _inherit ='account.move.line'

    branch_id = fields.Many2one('branch',string="Dependencia")
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencia")
    program_id = fields.Many2one('budget.program',string="Programa")
    subprogram_id = fields.Many2one('budget.subprogram',string="Subprograma")
    item_id = fields.Many2one('budget.item',string="Partida")
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso")
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad institucional")
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuestario")
    conpa_id = fields.Many2one('budget.item.conversion',string="Conversión con partida")
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto")
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación geográfica")
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera")
    type_project_id =fields.Many2one('budget.project.type',string="Tipo de proyecto")
    project_number_id = fields.Many2one('project.project',string="Número de proyecto")


class campos_nuevos_crossovered_budget(models.Model):# modelo el cual hace un inherit al modelo crossovered.budget
    _inherit = 'crossovered.budget'

    file_import  = fields.Binary(string='Archivo de importación')
    filename = fields.Char('file name') 
    total_budget = fields.Integer(string="Total de presupuesto",readonly=True)
    record_numbers = fields.Integer(string="Número de registros",readonly=True)
    imported_registration_numbers = fields.Integer(string="Número de registros importados",readonly=True)
    budget_of_project_dgpo = fields.Boolean(string="Presupuesto de DGPO")
    move_id = fields.Many2one('account.move',string="Asiento contable",readonly=True)

    #funcion para leer archivos txt 
    @api.onchange('filename')
    def onchange_archivo(self):
        ext = str(self.filename.split('.')[1])
        if ext != 'txt':
            raise ValidationError('El archivo adjunto no es compatible para la importación')
                


    @api.one
    def leer_archivo(self):
        if self.file_import:
            data = base64.decodestring(self.file_import)
            fobj = tempfile.NamedTemporaryFile(delete=False)
            fname = fobj.name
            fobj.write(data)
            fobj.close()
            image = open(fname,"r")
            contvalid = 0
            aray = 0
            araysubp = 0
            araydep = 0
            araysudep = 0
            araypar = 0
            arayact = 0
            arayconv = 0
            arayconpar = 0
            araytipo = 0
            arayubic = 0
            ararcart = 0
            araytipo_pro = 0
            arayno_proye = 0
            arayetapa = 0
            araytip_conv = 0
            arayt_conv = 0
            
            

            modpro =self.env['ir.model'].search([('model','=','budget.program')])
            prog =self.env['budget.structure'].search([('catalog_id','=',modpro.id)])

            modsubp=self.env['ir.model'].search([('model','=','budget.subprogram')])
            subprog =self.env['budget.structure'].search([('catalog_id','=',modsubp.id)])

            moddep = self.env['ir.model'].search([('model','=','res.branch')])
            dep = self.env['budget.structure'].search([('catalog_id','=',moddep.id)])

            modesubp = self.env['ir.model'].search([('model','=','budget.subdependence')])
            subdep = self.env['budget.structure'].search([('catalog_id','=',modesubp.id)])

            modpar = self.env['ir.model'].search([('model','=','budget.item')])
            part = self.env['budget.structure'].search([('catalog_id','=',modpar.id)])

            modact = self.env['ir.model'].search([('model','=','budget.institutional.activity')])
            acti = self.env['budget.structure'].search([('catalog_id','=',modact.id)])

            modconv = self.env['ir.model'].search([('model','=','budget.program.conversion')])
            conv = self.env['budget.structure'].search([('catalog_id','=',modconv.id)])

            modconpart = self.env['ir.model'].search([('model','=','budget.item.conversion')])
            convpar = self.env['budget.structure'].search([('catalog_id','=',modconpart.id)])

            modtipo = self.env['ir.model'].search([('model','=','budget.expense.type')])
            tipgt =  self.env['budget.structure'].search([('catalog_id','=',modtipo.id)])

            modubica =  self.env['ir.model'].search([('model','=','budget.geographic.location')])
            ubica_g = self.env['budget.structure'].search([('catalog_id','=',modubica.id)])

            modcart =  self.env['ir.model'].search([('model','=','budget.key.portfolio')])
            cart =  self.env['budget.structure'].search([('catalog_id','=',modcart.id)])

            modtipo_pro =  self.env['ir.model'].search([('model','=','budget.project.type')])
            tipo_pro = self.env['budget.structure'].search([('catalog_id','=',modtipo_pro.id)]) 

            modno_proy = self.env['ir.model'].search([('model','=','project.project')])
            no_proy = self.env['budget.structure'].search([('catalog_id','=',modno_proy.id)])

            modetapa = self.env['ir.model'].search([('model','=','budget.stage')])
            etapa = self.env['budget.structure'].search([('catalog_id','=',modetapa.id)])

            mod_tip_conv = self.env['ir.model'].search([('model','=','budget.agreement.type')])
            tip_convenio  = self.env['budget.structure'].search([('catalog_id','=',mod_tip_conv.id)])

            modet_conv = self.env['ir.model'].search([('model','=','agreement.agreement')])
            t_conv =  self.env['budget.structure'].search([('catalog_id','=',modet_conv.id)])


            if prog:
                inicial = prog.position_from
                final = prog.position_to
            if subprog:
                inisub = subprog.position_from
                finsub = subprog.position_to
            if dep:
                indep = dep.position_from
                fidep = dep.position_to
            if subdep:
                insubdep =subdep.position_from
                fisubdep = subdep.position_to
            if part:
                inipar = part.position_from
                finpar = part.position_to
            if acti:
                iniact = acti.position_from
                finact = acti.position_to
            if conv:
                iniconv = conv.position_from
                finconv = conv.position_to 
            if convpar:
                inicop = convpar.position_from
                fincop = convpar.position_to  
            if tipgt:
                initipo = tipgt.position_from
                fintipo = tipgt.position_to 
            if  ubica_g:
                iniubi = ubica_g.position_from
                finubi = ubica_g.position_to
            if cart:
                inicart = cart.position_from
                fincart = cart.position_to
            if tipo_pro:
                inipro = tipo_pro.position_from
                finapro = tipo_pro.position_to 
            if no_proy:
                inicialnop = no_proy.position_from
                finalnop = no_proy.position_to 
            if etapa:
                inicialet = etapa.position_from
                finalet = etapa.position_to
            if tip_convenio:
                init_c = tip_convenio.position_from
                fin_c = tip_convenio.position_to
                
            if t_conv:
                intcov = t_conv.position_from
                fincov = t_conv.position_to


            b_programa = self.env['budget.program']
            b_subpro = self.env['budget.subprogram']
            b_depen =self.env['res.branch']
            b_sebdep = self.env['budget.subdependence']
            b_part = self.env['budget.item']
            b_act = self.env['budget.institutional.activity']
            b_conv = self.env['budget.program.conversion']
            b_convpar = self.env['budget.item.conversion']
            b_tipo = self.env['budget.expense.type']
            b_ubic = self.env['budget.geographic.location']
            b_cart = self.env['budget.key.portfolio']
            b_tip_pro = self.env['budget.project.type']
            b_no_proy = self.env['project.project']
            b_etapa = self.env['budget.stage']
            b_t_convenio = self.env['budget.agreement.type']
            b_tipo_conv = self.env['agreement.agreement']
            tot_reg = 0
            for x in image:
                aray =x[inicial:final]
                araysubp = x[inisub:finsub]
                araydep = x[indep:fidep]
                araysudep =x[insubdep:fisubdep]
                araypar = x[inipar:finpar]
                arayact = x[iniact:finact]
                arayconv = x[iniconv:finconv]
                arayconpar = x[inicop:fincop]
                araytipo = x[initipo:fintipo]
                arayubic = x[iniubi:finubi]
                ararcart = x[inicart:fincart]
                araytipo_pro = x[inipro:finapro]
                arayno_proye = x[inicialnop:finalnop]
                arayetapa = x[inicialet:finalet]
                araytip_conv =x[init_c:fin_c]
                arayt_conv = x[intcov:fincov]
                if aray:
                    con = b_programa.search_count([('code','=',str(aray))])
                    if con:
                        if araysubp:
                            subp = b_subpro.search_count([('code','=',str(araysubp))])
                            if subp:
                                if araydep:
                                    depn = b_depen.search_count([('code','=',str(araydep))])
                                    if depn:
                                        if araysudep:
                                            depen  = b_sebdep.search_count([('code','=',str(araysudep))])                         
                                            if depen:
                                                if araypar:
                                                    partida = b_part.search_count([('code','=',str(araypar))])
                                                    if partida:
                                                        if arayact:
                                                            activ= b_act.search_count([('code','=',str(arayact))])
                                                            if activ:
                                                                if arayconv:
                                                                    convp = b_conv.search_count([('code','=',str(arayconv))])
                                                                    if convp:
                                                                        if arayconpar:
                                                                            parconv = b_convpar.search_count([('code','=',str(arayconpar))])
                                                                            if parconv:
                                                                                if araytipo:
                                                                                    tipo_gasto = b_tipo.search_count([('code','=',str(araytipo))])
                                                                                    if tipo_gasto:
                                                                                        if arayubic:
                                                                                            ubi_g = b_ubic.search_count([('code','=',str(arayubic))])
                                                                                            if ubi_g:
                                                                                                if ararcart:
                                                                                                    b_carte = b_cart.search_count([('code','=',str(ararcart))])
                                                                                                    if b_carte:
                                                                                                        if araytipo_pro:
                                                                                                            tipo_proye = b_tip_pro.search_count([('code','=',str(araytipo_pro))])
                                                                                                            if tipo_proye:
                                                                                                                if arayno_proye:
                                                                                                                    no_proyecto = b_no_proy.search_count([('code','=',str(arayno_proye))])
                                                                                                                    if no_proyecto:
                                                                                                                        if arayetapa:
                                                                                                                            etapa_e = b_etapa.search_count([('code','=',str(arayetapa))])
                                                                                                                            if etapa_e:
                                                                                                                                if araytip_conv:
                                                                                                                                    tipo_convenio =b_t_convenio.search_count([('code','=',str(araytip_conv))])
                                                                                                                                    if tipo_convenio:
                                                                                                                                        if arayt_conv:
                                                                                                                                            tip_conv = b_tipo_conv.search_count([('code','=',str(arayt_conv))])
                                                                                                                                            if tip_conv:
                                                                                                                                                contvalid += 1  
                tot_reg += 1                
            self.record_numbers = tot_reg
            self.imported_registration_numbers = contvalid

                            


class campos_adiccionales_presupuesto(models.Model):# modelo en el cual se hace un inherit al modedlo existente crossovered.budget.lines pag del doc 24
    _inherit = 'crossovered.budget.lines'
    #campos replazables que utilice para ocultarlos
    paid_date = fields.Date('Paid Date')
    theoritical_amount = fields.Monetary(
    compute='_compute_theoritical_amount', string='Theoretical Amount',
    help="Amount you are supposed to have earned/spent at this date.")
    percentage = fields.Float(
    compute='_compute_percentage', string='Achievement',
    help="Comparison between practical and theoretical amount. This measure tells you if you are below or over budget.")

    #campos nuevos del diseño de unam
    authorized_amount = fields.Float(string="Autorizado")# en comentario dice si  falta checar aque se refiere este campo
    amount_allocate = fields.Float(string="Asignado",digits=(12,2))
    amount_committed = fields.Float(string="Comprometido",digits=(12,2))
    accrued_amount = fields.Float(string="Devengado",digits=(12,2))
    amount_available = fields.Float(string="Por ejercer",digits=(12,2))
    amount_paid = fields.Float(string="Pagado",digits=(12,2))
    amount_applied = fields.Float(string="Ejercido",digits=(12,2))
    amount_modified = fields.Float(string="Modificado",digits=(12,2))
    amount_available2 = fields.Float(string="Disponible",digits=(12,2))
    programmatic_account = fields.Char(string="Código programático")#El valor debe estar separado por (.) por cada segmento del código programático
    branch_id = fields.Many2one('branch',string="Dependencia")
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencia")
    program_id = fields.Many2one('budget.program',string="Programa")
    subprogram_id = fields.Many2one('budget.subprogram',string="Subprograma")
    item_id = fields.Many2one(' budget.item',string="Partida")
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso")
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad institucional")
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuestario")
    conpa_id = fields.Many2one('budget.item.conversion',string="Conversión con partida")
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto")
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación geográfica")
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera")

class budget_amount_allocated(models.Model):# modelo para Control de montos asignados pag 24 doc
    _name = 'budget.amount.allocated'
    state = fields.Selection([('draft', 'Borrador'),('approve','Aprovado'),('solicitud','Solicitud'),('reject','Rechazado'),('cancel','Cancelado')], default="draft")
    code = fields.Char(string="Folio",required=True)
    budget_id = fields.Many2one('crossovered.budget',string="Presupuesto",required=True)
    description = fields.Char(string="Observaciones")
    date_import = fields.Date(string="Fecha de importación",required=True)
    file_amount_allocated  = fields.Binary(string="Archivo estacionalidad",required=True)
    user_id = fields.Many2one('res.users',string="Realizado por",required=True)
    reason_for_rejection = fields.Char(string="Motivo del rechazo")

    tabla_control = fields.One2many('tabla.control.depositos', 'relacion')


class tabla_control_depositos(models.Model):#tabla control de montos 
    _name = 'tabla.control.depositos'

    relacion = fields.Many2one('budget.amount.allocated', ondelete="cascade")
    currency_id = fields.Many2one('res.currency', string='Currency')
    assigment_amount = fields.Monetary(string="Monto asignado",digits=(12,2),required=True)
    deposit_amount = fields.Monetary(string="Monto depositado",required=True,readonly=True)
    pending_amount = fields.Monetary(string="Monto pendiente",digits=(12,2),readonly=True)
    deposit_date = fields.Date(string="Fecha depósito")
    deposit_account_bank_id = fields.Many2one('account.journal',string="Cuenta del depósito")
    Comments = fields.Char(string="Observaciones")
    move_id = fields.Many2one('account.move',string="Asiento contable")

class budget_amount_allocated_lines(models.Model): #parte del modelo budget.amount.allocated.lines que esta  Control de montos asignados pag 24 doc
    _name = 'budget.amount.allocated.lines'


    allocated_deposit_id = fields.Many2one('budget.amount.allocated',string="Control de monto asignado",required=True)
    programmatic_code = fields.Char(string="Código programático",required=True)
    amount = fields.Float(string="Monto",required=True)
    date  = fields.Date(string="Fecha",required=True)
    branch_id = fields.Many2one('res.branch',string="Dependencia")
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencia")
    program_id = fields.Many2one('budget.program',string="Programa")
    subprogram_id = fields.Many2one('budget.subprogram',string="Subprograma")
    item_id = fields.Many2one('budget.item',string="Partida")
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso")
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad instituciona")
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuestario")
    conpa_id = fields.Many2one('budget.item.conversion',string="Conversión con partida")
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto")
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación geográfica")
    key_portfolio_id = fields.Many2one('budget_key_portfolio',string="Clave cartera")

class budget_adjustement(models.Model):#modelo para las Adecuaciones 6.1
    _name='budget.adjustement'


    state = fields.Selection([('draft', 'Borrador'),('approve','Aprovado'),('solicitud','Solicitud'),('reject','Rechazado'),('cancel','Cancelado')], default="draft")
    code = fields.Char(string="Folio",required=True)
    movement_date = fields.Date(string="Fecha",default=fields.Date.today(),required=True)
    budget_id = fields.Many2one('crossovered.budget',string="Presupuesto",required=True)
    description = fields.Char(string="Observaciones")
    file = fields.Binary(string="Archivo adecuación")
    reason_for_rejection = fields.Char(string="Motivo del rechazo")
    move_id = fields.Many2one('account.move',string="Asiento contable")

    tabla_ade= fields.One2many('tabla.budget.adjustement.line','relacion')

class tabla_budget_adjustement_line(models.Model):#modelo el cual se muestra en una pestaña con el nombre líneas de adecuación relacionada al budegte adjustement
    _name ='tabla.budget.adjustement.line'

    relacion = fields.Many2one('budget.adjustement',ondelete="cascade")

    adjustement_id = fields.Many2one('budget.adjustement',string="Adecuación",required=True)

    programmatic_code = fields.Char(string="Código programático",required=True)
    type = fields.Selection([('a','Aumento'),('d','Disminución')],string="Tipo",required=True)
    amount = fields.Float(string="Importe",required=True)
    branch_id = fields.Many2one('res.branch',string="Dependencia",required=True)
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdepencencia",required=True)
    program_id = fields.Many2one('budget.program',string="Programa",required=True)
    subprogram_id = fields.Many2one('budget.subprogram',string="Subprograma",required=True)
    item_id = fields.Many2one('budget.item',string="Partida",required=True)
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso",required=True)
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad institucional",required=True)
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuestario",required=True)
    conpa_id = fields.Many2one('budget.item.conversion',string="Conversión con partida",required=True)
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto", required=True)
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación Geográfica",required=True)
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera",required=True)

class budget_import_recalendarization(models.Model):#modelo para Recalendarizaciones pag 33
    _name = 'budget.import.recalendarization'

    state = fields.Selection([('draft','Borrador'),('import','Importado'),('reject','Rechazado'),('cancel','Cancelado')],default="draft")
    code = fields.Char(string="Folio",required=True)
    budget_id = fields.Many2one('crossovered.budget',string="Presupuesto",required=True)
    file = fields.Binary(string="Archivo recalendarización",required=True)
    description = fields.Char(string="Observaciones")
    record_number = fields.Integer(string="Numeros de registros",default=0,readonly=True)
    records_number_imported = fields.Integer(string="Número de registros importados",default=0,readonly=True)
    reason_for_rejection = fields.Char(string="Motivo del rechazo")

class budget_rescheduling(models.Model):# modelo para Control de recalendarizaciones. pag35
    _name = 'budget.rescheduling'

    state = fields.Selection([('draft','Borrador'),('import','Importado'),('reject','Rechazado'),('cancel','Cancelado')],default="draft")
    code = fields.Char(string="Folio",required=True)
    budget_id = fields.Many2one('crossovered.budget',string="Presupuesto",readonly=True)
    programmatic_code = fields.Char(string="Código programático",required=True)
    date = fields.Date(string="Fecha",default=fields.Date.today(),required=True)
    to_period = fields.Selection([('t1','Trimestre 1'),('t2','Trimestre 2'),('t3','Trimestre 3'),('t4','Trimestre 4')],string="Enviar a",required=True)
    reason_for_rejection = fields.Char(string="Motivo del rechazo")
    import_recalendarization_id = fields.Many2one('budget.import.recalendarization',string="Recalendarización",required=True)
    branch_id =fields.Many2one('res.branch',string="Dependencia",required=True)
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdependencia",required=True)
    program_id = fields.Many2one('budget.program',string="Programa",required=True)
    subprogram_id = fields.Many2one('budget.subprogram',string="Subprograma",required=True)
    item_id = fields.Many2one('budget.item',string="Partida",required=True)
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso",required=True)
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad institucional",required=True)
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuestario",required=True)
    conpa_id = fields.Many2one('budget.item.conversion',string="Conversión con partida",required=True)
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto",required=True)
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación geográfica",required=True)
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera",required=True)
    move_id = fields.Many2one('account.move',string="Asiento contable")

class inherit_campos_nuevos_account(models.Model):#campos adicionales a este modelo Validación del presupuesto, solicitudes de pago.
    _inherit = 'account.invoice.line'

    programmatic_code = fields.Char(string="Código programático",required=True)
    branch_id = fields.Many2one('res.branch',string="Dependencia")
    subdependence_id = fields.Many2one('budget.subdependence',string="Subdepencencia")
    program_id = fields.Many2one('budget.program',string="Programa")
    subprogram_id = fields.Many2one('budget.subprogram',string="SubPrograma")
    item_id = fields.Many2one('budget.item',string="Partida")
    check_digit_id = fields.Char(string="Dígito verificador")
    resource_origin_id = fields.Many2one('budget.resource.origin',string="Origen del recurso")
    institutional_activity_id = fields.Many2one('budget.institutional.activity',string="Actividad institucional")
    conpp_id = fields.Many2one('budget.program.conversion',string="Conversión de programa presupuesto")
    conpa_id = fields.Many2one('budget.program.conversion',string="Conversión de partida")
    expense_type_id = fields.Many2one('budget.expense.type',string="Tipo de gasto")
    geographic_location_id = fields.Many2one('budget.geographic.location',string="Ubicación geográfica")
    key_portfolio_id = fields.Many2one('budget.key.portfolio',string="Clave cartera")
    type_project_id = fields.Many2one('budget.project.type',string="Tipo de proyecto")
    project_number = fields.Many2one('project.project',string="Numeros de proyecto")
    stage = fields.Many2one('budget.stage',string="Etapa")
    agreement_type_id = fields.Many2one('budget.agreement.type',string="Tipo de convenio")
    agreement_number = fields.Many2one('agreement.agreement',string="Número de convenio")

class caampos_accon_inhe(models.Model):
    _inherit  = 'account.invoice'

    
    sub_state = fields.Selection([('so','Solicitud'),('ap','Aprovado'),('app','Aprovado para pago'),('ma','Medio de pago asignado'),('pa','Pagado'),('re','Rechazado'),('ca','Cancelado'),('pna','Pago no aplicado'),('mpc','Medio de pago cancelado'),('rpp','Rechazado por pago')],string="Sub-Estado",required=True)









