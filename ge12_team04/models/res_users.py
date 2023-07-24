import logging

from odoo import models, _
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_partner import now

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = ['res.users']
    
    def action_reset_kawiil_password(self):
        if self.env.context.get('installmode', False):
            return
        if self.env['res.users'].filtered(lambda user: not user.active):
            raise UserError(("You cannot perform this action on an archived user."))
        create_mode = bool(self.env.context.get('create_user'))

        expiration = False if create_mode else now(days=+1)
        self.mapped('partner_id').signup_prepare(signup_type="reset", expiration=expiration)
        
        template = False
        if not template:
            template = self.env.ref('ge12_team04.set_password_email_registry')
        assert template._name == 'mail.template'

        email_values = {
            'email_cc': False,
            'auto_delete': True,
            'message_type': 'user_notification',
            'recipient_ids': [],
            'partner_ids': [],
        }

        for user in self:
            if not user.email:
                raise UserError(("Cannot send email: user %s has no email address.", user.name))
            email_values['email_to'] = user.email
            with self.env.cr.savepoint():
                force_send = not(self.env.context.get('import_file', False))
                template.send_mail(user.id, force_send=force_send, raise_exception=True, email_values=email_values)
            _logger.info("Password reset email sent for user <%s> to <%s>", user.login, user.email)
