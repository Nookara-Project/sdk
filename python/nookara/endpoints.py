"""Named methods generated from the Nookara API catalogue."""

class Endpoints:

    def post_bonfire_instance_token(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/instance-token. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_instance_token', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_keys(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/keys. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_keys', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_keys(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/keys. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_keys', query=query, json=json, data=data, files=files, raw=raw)

    def delete_bonfire_keys_by_kid(self, *, kid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /bonfire/keys/:kid. See the API reference for scopes and payloads."""
        return self.call('delete_bonfire_keys_by_kid', kid=kid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_keys_kid_by_kid(self, *, kid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/keys/kid/:kid. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_keys_kid_by_kid', kid=kid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_keys_user_by_userid(self, *, userId, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/keys/user/:userId. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_keys_user_by_userid', userId=userId, query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_instances(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/instances. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_instances', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_instances_default_joined(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/instances/default-joined. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_instances_default_joined', query=query, json=json, data=data, files=files, raw=raw)

    def put_bonfire_instances(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PUT /bonfire/instances. See the API reference for scopes and payloads."""
        return self.call('put_bonfire_instances', query=query, json=json, data=data, files=files, raw=raw)

    def patch_bonfire_instances_prefs(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /bonfire/instances/prefs. See the API reference for scopes and payloads."""
        return self.call('patch_bonfire_instances_prefs', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_instances_challenge(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/instances/challenge. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_instances_challenge', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_instances_register(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/instances/register. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_instances_register', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_instances_payout(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/instances/payout. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_instances_payout', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_instances_payout(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/instances/payout. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_instances_payout', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_signing_key(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/signing-key. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_signing_key', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_signing_key_rotate(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/signing-key/rotate. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_signing_key_rotate', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_signing_key_info(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/signing-key/info. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_signing_key_info', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_import_platforms(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/import/platforms. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_import_platforms', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_import_by_platform_guilds(self, *, platform, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/import/:platform/guilds. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_import_by_platform_guilds', platform=platform, query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_import_by_platform_guilds_by_gid(self, *, platform, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/import/:platform/guilds/:gid. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_import_by_platform_guilds_by_gid', platform=platform, gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_import(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/import. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_import', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_import_by_job_id(self, *, job_id, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/import/:job_id. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_import_by_job_id', job_id=job_id, query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_directory(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/directory. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_directory', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_pay_requests_by_id_approve(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/pay-requests/:id/approve. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_pay_requests_by_id_approve', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_pay_requests_by_id_decline(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/pay-requests/:id/decline. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_pay_requests_by_id_decline', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_hosting_plans(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/hosting/plans. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_hosting_plans', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_hosting_slug_by_slug(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/hosting/slug/:slug. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_hosting_slug_by_slug', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_hosting_servers(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/hosting/servers. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_hosting_servers', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_hosting_servers(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/hosting/servers. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_hosting_servers', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_hosting_servers_by_url(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/hosting/servers/by-url. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_hosting_servers_by_url', query=query, json=json, data=data, files=files, raw=raw)

    def put_bonfire_hosting_servers_by_slug_address(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """PUT /bonfire/hosting/servers/:slug/address. See the API reference for scopes and payloads."""
        return self.call('put_bonfire_hosting_servers_by_slug_address', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_hosting_servers_by_slug_weeks(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/hosting/servers/:slug/weeks. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_hosting_servers_by_slug_weeks', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def patch_bonfire_hosting_servers_by_slug(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /bonfire/hosting/servers/:slug. See the API reference for scopes and payloads."""
        return self.call('patch_bonfire_hosting_servers_by_slug', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_hosting_servers_by_slug_restart(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/hosting/servers/:slug/restart. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_hosting_servers_by_slug_restart', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_hosting_backups_upload(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/hosting/backups/upload. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_hosting_backups_upload', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_hosting_servers_by_slug_backup(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/hosting/servers/:slug/backup. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_hosting_servers_by_slug_backup', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_hosting_backups(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/hosting/backups. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_hosting_backups', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_hosting_backups_by_id_download(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/hosting/backups/:id/download. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_hosting_backups_by_id_download', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_bonfire_hosting_backups_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /bonfire/hosting/backups/:id. See the API reference for scopes and payloads."""
        return self.call('delete_bonfire_hosting_backups_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_bonfire_hosting_servers_by_slug(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /bonfire/hosting/servers/:slug. See the API reference for scopes and payloads."""
        return self.call('delete_bonfire_hosting_servers_by_slug', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_ext_code(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/ext-code. See the API reference for scopes and payloads."""
        return self.call('post_auth_ext_code', query=query, json=json, data=data, files=files, raw=raw)

    def get_auth_ext_code_heartbeat(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /auth/ext-code/heartbeat. See the API reference for scopes and payloads."""
        return self.call('get_auth_ext_code_heartbeat', query=query, json=json, data=data, files=files, raw=raw)

    def get_auth_ext_code_info(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /auth/ext-code/info. See the API reference for scopes and payloads."""
        return self.call('get_auth_ext_code_info', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_ext_code_check(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/ext-code/check. See the API reference for scopes and payloads."""
        return self.call('post_auth_ext_code_check', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_ext_code_complete(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/ext-code/complete. See the API reference for scopes and payloads."""
        return self.call('post_auth_ext_code_complete', query=query, json=json, data=data, files=files, raw=raw)

    def get_auth_ext_code_status(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /auth/ext-code/status. See the API reference for scopes and payloads."""
        return self.call('get_auth_ext_code_status', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_ext_code_exchange(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/ext-code/exchange. See the API reference for scopes and payloads."""
        return self.call('post_auth_ext_code_exchange', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_register(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/register. See the API reference for scopes and payloads."""
        return self.call('post_auth_register', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_register_verify(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/register/verify. See the API reference for scopes and payloads."""
        return self.call('post_auth_register_verify', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_register_verify_link(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/register/verify-link. See the API reference for scopes and payloads."""
        return self.call('post_auth_register_verify_link', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_register_status(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/register/status. See the API reference for scopes and payloads."""
        return self.call('post_auth_register_status', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_register_resend(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/register/resend. See the API reference for scopes and payloads."""
        return self.call('post_auth_register_resend', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_login(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/login. See the API reference for scopes and payloads."""
        return self.call('post_auth_login', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_verify_new_ip(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/verify-new-ip. See the API reference for scopes and payloads."""
        return self.call('post_auth_verify_new_ip', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_verify_email_link(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/verify-email-link. See the API reference for scopes and payloads."""
        return self.call('post_auth_verify_email_link', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_verify_ip_link(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/verify-ip-link. See the API reference for scopes and payloads."""
        return self.call('post_auth_verify_ip_link', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_resend_new_ip(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/resend-new-ip. See the API reference for scopes and payloads."""
        return self.call('post_auth_resend_new_ip', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_validate(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/validate. See the API reference for scopes and payloads."""
        return self.call('post_auth_validate', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_accept_tos(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/accept-tos. See the API reference for scopes and payloads."""
        return self.call('post_auth_accept_tos', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_logout(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/logout. See the API reference for scopes and payloads."""
        return self.call('post_auth_logout', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_set_email(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/set-email. See the API reference for scopes and payloads."""
        return self.call('post_auth_set_email', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_verify_email(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/verify-email. See the API reference for scopes and payloads."""
        return self.call('post_auth_verify_email', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_resend_verification(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/resend-verification. See the API reference for scopes and payloads."""
        return self.call('post_auth_resend_verification', query=query, json=json, data=data, files=files, raw=raw)

    def delete_auth_sessions_by_sessionid(self, *, sessionId, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /auth/sessions/:sessionId. See the API reference for scopes and payloads."""
        return self.call('delete_auth_sessions_by_sessionid', sessionId=sessionId, query=query, json=json, data=data, files=files, raw=raw)

    def get_auth_sessions(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /auth/sessions. See the API reference for scopes and payloads."""
        return self.call('get_auth_sessions', query=query, json=json, data=data, files=files, raw=raw)

    def get_auth_login_history(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /auth/login-history. See the API reference for scopes and payloads."""
        return self.call('get_auth_login_history', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_forgot_password(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/forgot-password. See the API reference for scopes and payloads."""
        return self.call('post_auth_forgot_password', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_reset_password(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/reset-password. See the API reference for scopes and payloads."""
        return self.call('post_auth_reset_password', query=query, json=json, data=data, files=files, raw=raw)

    def get_auth_oauth_providers(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /auth/oauth/providers. See the API reference for scopes and payloads."""
        return self.call('get_auth_oauth_providers', query=query, json=json, data=data, files=files, raw=raw)

    def get_auth_oauth_by_p_start(self, *, p, query=None, json=None, data=None, files=None, raw=False):
        """GET /auth/oauth/:p/start. See the API reference for scopes and payloads."""
        return self.call('get_auth_oauth_by_p_start', p=p, query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_oauth_by_p_link(self, *, p, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/oauth/:p/link. See the API reference for scopes and payloads."""
        return self.call('post_auth_oauth_by_p_link', p=p, query=query, json=json, data=data, files=files, raw=raw)

    def get_auth_oauth_by_p_callback(self, *, p, query=None, json=None, data=None, files=None, raw=False):
        """GET /auth/oauth/:p/callback. See the API reference for scopes and payloads."""
        return self.call('get_auth_oauth_by_p_callback', p=p, query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_oauth_exchange(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/oauth/exchange. See the API reference for scopes and payloads."""
        return self.call('post_auth_oauth_exchange', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_oauth_set_password(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/oauth/set-password. See the API reference for scopes and payloads."""
        return self.call('post_auth_oauth_set_password', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_oauth_signup(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/oauth/signup. See the API reference for scopes and payloads."""
        return self.call('post_auth_oauth_signup', query=query, json=json, data=data, files=files, raw=raw)

    def get_auth_oauth_linked(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /auth/oauth/linked. See the API reference for scopes and payloads."""
        return self.call('get_auth_oauth_linked', query=query, json=json, data=data, files=files, raw=raw)

    def patch_auth_oauth_by_p(self, *, p, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /auth/oauth/:p. See the API reference for scopes and payloads."""
        return self.call('patch_auth_oauth_by_p', p=p, query=query, json=json, data=data, files=files, raw=raw)

    def delete_auth_oauth_by_p(self, *, p, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /auth/oauth/:p. See the API reference for scopes and payloads."""
        return self.call('delete_auth_oauth_by_p', p=p, query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_child_token_approval(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/child-token/approval. See the API reference for scopes and payloads."""
        return self.call('post_auth_child_token_approval', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_child_token_approval_status(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/child-token/approval/status. See the API reference for scopes and payloads."""
        return self.call('post_auth_child_token_approval_status', query=query, json=json, data=data, files=files, raw=raw)

    def post_auth_child_token(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /auth/child-token. See the API reference for scopes and payloads."""
        return self.call('post_auth_child_token', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_app_login(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/app-login. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_app_login', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_scopes_json(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/scopes.json. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_scopes_json', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_session(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/session. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_session', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_app_exchange(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/app-exchange. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_app_exchange', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_replace_token(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/replace-token. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_replace_token', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_sign_out(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/sign-out. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_sign_out', query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_app_code(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/app-code. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_app_code', query=query, json=json, data=data, files=files, raw=raw)

    def get_account_notifications(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/notifications. See the API reference for scopes and payloads."""
        return self.call('get_account_notifications', query=query, json=json, data=data, files=files, raw=raw)

    def get_account_notifications_unread_count(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/notifications/unread-count. See the API reference for scopes and payloads."""
        return self.call('get_account_notifications_unread_count', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_notifications_read(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/notifications/read. See the API reference for scopes and payloads."""
        return self.call('post_account_notifications_read', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_notifications_unread(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/notifications/unread. See the API reference for scopes and payloads."""
        return self.call('post_account_notifications_unread', query=query, json=json, data=data, files=files, raw=raw)

    def delete_account_notifications_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /account/notifications/:id. See the API reference for scopes and payloads."""
        return self.call('delete_account_notifications_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_account_notification_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/notification-settings. See the API reference for scopes and payloads."""
        return self.call('get_account_notification_settings', query=query, json=json, data=data, files=files, raw=raw)

    def patch_account_notification_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /account/notification-settings. See the API reference for scopes and payloads."""
        return self.call('patch_account_notification_settings', query=query, json=json, data=data, files=files, raw=raw)

    def get_account_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/me. See the API reference for scopes and payloads."""
        return self.call('get_account_me', query=query, json=json, data=data, files=files, raw=raw)

    def get_account_birthday(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/birthday. See the API reference for scopes and payloads."""
        return self.call('get_account_birthday', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_birthday(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/birthday. See the API reference for scopes and payloads."""
        return self.call('post_account_birthday', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_change_username(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/change-username. See the API reference for scopes and payloads."""
        return self.call('post_account_change_username', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_onboarding_complete(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/onboarding/complete. See the API reference for scopes and payloads."""
        return self.call('post_account_onboarding_complete', query=query, json=json, data=data, files=files, raw=raw)

    def get_account_export(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/export. See the API reference for scopes and payloads."""
        return self.call('get_account_export', query=query, json=json, data=data, files=files, raw=raw)

    def delete_account_sessions_by_tokenid(self, *, tokenId, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /account/sessions/:tokenId. See the API reference for scopes and payloads."""
        return self.call('delete_account_sessions_by_tokenid', tokenId=tokenId, query=query, json=json, data=data, files=files, raw=raw)

    def get_account_blocks(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/blocks. See the API reference for scopes and payloads."""
        return self.call('get_account_blocks', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_blocks(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/blocks. See the API reference for scopes and payloads."""
        return self.call('post_account_blocks', query=query, json=json, data=data, files=files, raw=raw)

    def delete_account_blocks_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /account/blocks/:username. See the API reference for scopes and payloads."""
        return self.call('delete_account_blocks_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_account_dm_privacy(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/dm-privacy. See the API reference for scopes and payloads."""
        return self.call('get_account_dm_privacy', query=query, json=json, data=data, files=files, raw=raw)

    def patch_account_dm_privacy(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /account/dm-privacy. See the API reference for scopes and payloads."""
        return self.call('patch_account_dm_privacy', query=query, json=json, data=data, files=files, raw=raw)

    def get_account_dm_requests(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/dm-requests. See the API reference for scopes and payloads."""
        return self.call('get_account_dm_requests', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_dm_requests_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/dm-requests/settings. See the API reference for scopes and payloads."""
        return self.call('post_account_dm_requests_settings', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_dm_requests_by_id_by_answer_accept_decline(self, *, id, answer, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/dm-requests/:id/:answer(accept|decline). See the API reference for scopes and payloads."""
        return self.call('post_account_dm_requests_by_id_by_answer_accept_decline', id=id, answer=answer, query=query, json=json, data=data, files=files, raw=raw)

    def get_account_notices(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/notices. See the API reference for scopes and payloads."""
        return self.call('get_account_notices', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_notices_by_id_seen(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/notices/:id/seen. See the API reference for scopes and payloads."""
        return self.call('post_account_notices_by_id_seen', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_account_search(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/search. See the API reference for scopes and payloads."""
        return self.call('get_account_search', query=query, json=json, data=data, files=files, raw=raw)

    def get_account_lookup_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/lookup/:username. See the API reference for scopes and payloads."""
        return self.call('get_account_lookup_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_account_lookup(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/lookup. See the API reference for scopes and payloads."""
        return self.call('post_account_lookup', query=query, json=json, data=data, files=files, raw=raw)

    def get_account_lookup(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/lookup. See the API reference for scopes and payloads."""
        return self.call('get_account_lookup', query=query, json=json, data=data, files=files, raw=raw)

    def patch_account_update(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /account/update. See the API reference for scopes and payloads."""
        return self.call('patch_account_update', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_lang(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/lang. See the API reference for scopes and payloads."""
        return self.call('post_account_lang', query=query, json=json, data=data, files=files, raw=raw)

    def post_account_change_password(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /account/change-password. See the API reference for scopes and payloads."""
        return self.call('post_account_change_password', query=query, json=json, data=data, files=files, raw=raw)

    def delete_account_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /account/me. See the API reference for scopes and payloads."""
        return self.call('delete_account_me', query=query, json=json, data=data, files=files, raw=raw)

    def get_account_cursor_ticket(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /account/cursor-ticket. See the API reference for scopes and payloads."""
        return self.call('get_account_cursor_ticket', query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_info_usage(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage/info/usage. See the API reference for scopes and payloads."""
        return self.call('get_storage_info_usage', query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_by_storageid(self, *, storageId, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage/:storageId. See the API reference for scopes and payloads."""
        return self.call('get_storage_by_storageid', storageId=storageId, query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_by_storageid_keys(self, *, storageId, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage/:storageId/keys. See the API reference for scopes and payloads."""
        return self.call('get_storage_by_storageid_keys', storageId=storageId, query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_by_storageid_values(self, *, storageId, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage/:storageId/values. See the API reference for scopes and payloads."""
        return self.call('get_storage_by_storageid_values', storageId=storageId, query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_by_storageid_by_key(self, *, storageId, key, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage/:storageId/:key. See the API reference for scopes and payloads."""
        return self.call('get_storage_by_storageid_by_key', storageId=storageId, key=key, query=query, json=json, data=data, files=files, raw=raw)

    def put_storage_by_storageid_by_key(self, *, storageId, key, query=None, json=None, data=None, files=None, raw=False):
        """PUT /storage/:storageId/:key. See the API reference for scopes and payloads."""
        return self.call('put_storage_by_storageid_by_key', storageId=storageId, key=key, query=query, json=json, data=data, files=files, raw=raw)

    def delete_storage_by_storageid_by_key(self, *, storageId, key, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /storage/:storageId/:key. See the API reference for scopes and payloads."""
        return self.call('delete_storage_by_storageid_by_key', storageId=storageId, key=key, query=query, json=json, data=data, files=files, raw=raw)

    def delete_storage_by_storageid(self, *, storageId, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /storage/:storageId. See the API reference for scopes and payloads."""
        return self.call('delete_storage_by_storageid', storageId=storageId, query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_info_info_usage(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage-info/info/usage. See the API reference for scopes and payloads."""
        return self.call('get_storage_info_info_usage', query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_info_by_storageid(self, *, storageId, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage-info/:storageId. See the API reference for scopes and payloads."""
        return self.call('get_storage_info_by_storageid', storageId=storageId, query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_info_by_storageid_keys(self, *, storageId, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage-info/:storageId/keys. See the API reference for scopes and payloads."""
        return self.call('get_storage_info_by_storageid_keys', storageId=storageId, query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_info_by_storageid_values(self, *, storageId, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage-info/:storageId/values. See the API reference for scopes and payloads."""
        return self.call('get_storage_info_by_storageid_values', storageId=storageId, query=query, json=json, data=data, files=files, raw=raw)

    def get_storage_info_by_storageid_by_key(self, *, storageId, key, query=None, json=None, data=None, files=None, raw=False):
        """GET /storage-info/:storageId/:key. See the API reference for scopes and payloads."""
        return self.call('get_storage_info_by_storageid_by_key', storageId=storageId, key=key, query=query, json=json, data=data, files=files, raw=raw)

    def put_storage_info_by_storageid_by_key(self, *, storageId, key, query=None, json=None, data=None, files=None, raw=False):
        """PUT /storage-info/:storageId/:key. See the API reference for scopes and payloads."""
        return self.call('put_storage_info_by_storageid_by_key', storageId=storageId, key=key, query=query, json=json, data=data, files=files, raw=raw)

    def delete_storage_info_by_storageid_by_key(self, *, storageId, key, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /storage-info/:storageId/:key. See the API reference for scopes and payloads."""
        return self.call('delete_storage_info_by_storageid_by_key', storageId=storageId, key=key, query=query, json=json, data=data, files=files, raw=raw)

    def delete_storage_info_by_storageid(self, *, storageId, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /storage-info/:storageId. See the API reference for scopes and payloads."""
        return self.call('delete_storage_info_by_storageid', storageId=storageId, query=query, json=json, data=data, files=files, raw=raw)

    def post_im_send(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /im/send. See the API reference for scopes and payloads."""
        return self.call('post_im_send', query=query, json=json, data=data, files=files, raw=raw)

    def get_im_status_reply_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /im/status-reply/:username. See the API reference for scopes and payloads."""
        return self.call('get_im_status_reply_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_im_conversations(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /im/conversations. See the API reference for scopes and payloads."""
        return self.call('get_im_conversations', query=query, json=json, data=data, files=files, raw=raw)

    def get_im_with_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /im/with/:username. See the API reference for scopes and payloads."""
        return self.call('get_im_with_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_im_with_by_username_read(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """POST /im/with/:username/read. See the API reference for scopes and payloads."""
        return self.call('post_im_with_by_username_read', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_im(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /im. See the API reference for scopes and payloads."""
        return self.call('get_im', query=query, json=json, data=data, files=files, raw=raw)

    def get_im_inbox(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /im/inbox. See the API reference for scopes and payloads."""
        return self.call('get_im_inbox', query=query, json=json, data=data, files=files, raw=raw)

    def get_im_sent(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /im/sent. See the API reference for scopes and payloads."""
        return self.call('get_im_sent', query=query, json=json, data=data, files=files, raw=raw)

    def get_im_unread_count(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /im/unread-count. See the API reference for scopes and payloads."""
        return self.call('get_im_unread_count', query=query, json=json, data=data, files=files, raw=raw)

    def patch_im_by_id_read(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /im/:id/read. See the API reference for scopes and payloads."""
        return self.call('patch_im_by_id_read', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def patch_im_by_id_edit(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /im/:id/edit. See the API reference for scopes and payloads."""
        return self.call('patch_im_by_id_edit', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_im_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /im/:id. See the API reference for scopes and payloads."""
        return self.call('delete_im_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def put_im_by_id_pin(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PUT /im/:id/pin. See the API reference for scopes and payloads."""
        return self.call('put_im_by_id_pin', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_im_by_id_pin(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /im/:id/pin. See the API reference for scopes and payloads."""
        return self.call('delete_im_by_id_pin', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_im_with_by_username_pins(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /im/with/:username/pins. See the API reference for scopes and payloads."""
        return self.call('get_im_with_by_username_pins', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def delete_im(self, *, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /im. See the API reference for scopes and payloads."""
        return self.call('delete_im', query=query, json=json, data=data, files=files, raw=raw)

    def get_friends(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /friends. See the API reference for scopes and payloads."""
        return self.call('get_friends', query=query, json=json, data=data, files=files, raw=raw)

    def get_friends_requests(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /friends/requests. See the API reference for scopes and payloads."""
        return self.call('get_friends_requests', query=query, json=json, data=data, files=files, raw=raw)

    def post_friends_request(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /friends/request. See the API reference for scopes and payloads."""
        return self.call('post_friends_request', query=query, json=json, data=data, files=files, raw=raw)

    def patch_friends_request_by_id_accept(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /friends/request/:id/accept. See the API reference for scopes and payloads."""
        return self.call('patch_friends_request_by_id_accept', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def patch_friends_request_by_id_decline(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /friends/request/:id/decline. See the API reference for scopes and payloads."""
        return self.call('patch_friends_request_by_id_decline', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_friends_request_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /friends/request/:id. See the API reference for scopes and payloads."""
        return self.call('delete_friends_request_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_friends_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /friends/:username. See the API reference for scopes and payloads."""
        return self.call('delete_friends_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_friends_status_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /friends/status/:username. See the API reference for scopes and payloads."""
        return self.call('get_friends_status_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_groups(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /groups. See the API reference for scopes and payloads."""
        return self.call('get_groups', query=query, json=json, data=data, files=files, raw=raw)

    def post_groups(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /groups. See the API reference for scopes and payloads."""
        return self.call('post_groups', query=query, json=json, data=data, files=files, raw=raw)

    def get_groups_by_room(self, *, room, query=None, json=None, data=None, files=None, raw=False):
        """GET /groups/:room. See the API reference for scopes and payloads."""
        return self.call('get_groups_by_room', room=room, query=query, json=json, data=data, files=files, raw=raw)

    def get_groups_by_room_messages(self, *, room, query=None, json=None, data=None, files=None, raw=False):
        """GET /groups/:room/messages. See the API reference for scopes and payloads."""
        return self.call('get_groups_by_room_messages', room=room, query=query, json=json, data=data, files=files, raw=raw)

    def post_groups_by_room_messages(self, *, room, query=None, json=None, data=None, files=None, raw=False):
        """POST /groups/:room/messages. See the API reference for scopes and payloads."""
        return self.call('post_groups_by_room_messages', room=room, query=query, json=json, data=data, files=files, raw=raw)

    def delete_groups_by_room_messages_by_id(self, *, room, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /groups/:room/messages/:id. See the API reference for scopes and payloads."""
        return self.call('delete_groups_by_room_messages_by_id', room=room, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def patch_groups_by_room_messages_by_id(self, *, room, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /groups/:room/messages/:id. See the API reference for scopes and payloads."""
        return self.call('patch_groups_by_room_messages_by_id', room=room, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def put_groups_by_room_messages_by_id_reactions_by_emoji(self, *, room, id, emoji, query=None, json=None, data=None, files=None, raw=False):
        """PUT /groups/:room/messages/:id/reactions/:emoji. See the API reference for scopes and payloads."""
        return self.call('put_groups_by_room_messages_by_id_reactions_by_emoji', room=room, id=id, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def delete_groups_by_room_messages_by_id_reactions_by_emoji(self, *, room, id, emoji, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /groups/:room/messages/:id/reactions/:emoji. See the API reference for scopes and payloads."""
        return self.call('delete_groups_by_room_messages_by_id_reactions_by_emoji', room=room, id=id, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def put_groups_by_room_messages_by_id_pin(self, *, room, id, query=None, json=None, data=None, files=None, raw=False):
        """PUT /groups/:room/messages/:id/pin. See the API reference for scopes and payloads."""
        return self.call('put_groups_by_room_messages_by_id_pin', room=room, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_groups_by_room_messages_by_id_pin(self, *, room, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /groups/:room/messages/:id/pin. See the API reference for scopes and payloads."""
        return self.call('delete_groups_by_room_messages_by_id_pin', room=room, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_groups_by_room_pins(self, *, room, query=None, json=None, data=None, files=None, raw=False):
        """GET /groups/:room/pins. See the API reference for scopes and payloads."""
        return self.call('get_groups_by_room_pins', room=room, query=query, json=json, data=data, files=files, raw=raw)

    def post_groups_by_room_members(self, *, room, query=None, json=None, data=None, files=None, raw=False):
        """POST /groups/:room/members. See the API reference for scopes and payloads."""
        return self.call('post_groups_by_room_members', room=room, query=query, json=json, data=data, files=files, raw=raw)

    def delete_groups_by_room_members_by_username(self, *, room, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /groups/:room/members/:username. See the API reference for scopes and payloads."""
        return self.call('delete_groups_by_room_members_by_username', room=room, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def patch_groups_by_room(self, *, room, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /groups/:room. See the API reference for scopes and payloads."""
        return self.call('patch_groups_by_room', room=room, query=query, json=json, data=data, files=files, raw=raw)

    def delete_groups_by_room(self, *, room, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /groups/:room. See the API reference for scopes and payloads."""
        return self.call('delete_groups_by_room', room=room, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_game_downloads(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/game/downloads. See the API reference for scopes and payloads."""
        return self.call('get_chat_game_downloads', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_game_servers_by_sid_instances(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/game/servers/:sid/instances. See the API reference for scopes and payloads."""
        return self.call('get_chat_game_servers_by_sid_instances', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_game_servers_by_sid_instances_by_iid(self, *, sid, iid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/game/servers/:sid/instances/:iid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_game_servers_by_sid_instances_by_iid', sid=sid, iid=iid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_game_unclaimed(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/game/unclaimed. See the API reference for scopes and payloads."""
        return self.call('get_chat_game_unclaimed', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_game_claims(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/game/claims. See the API reference for scopes and payloads."""
        return self.call('post_chat_game_claims', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_game_claims_by_code(self, *, code, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/game/claims/:code. See the API reference for scopes and payloads."""
        return self.call('get_chat_game_claims_by_code', code=code, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_game_channels_by_cid_status(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/game/channels/:cid/status. See the API reference for scopes and payloads."""
        return self.call('get_chat_game_channels_by_cid_status', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_game_channels_by_cid_console(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/game/channels/:cid/console. See the API reference for scopes and payloads."""
        return self.call('get_chat_game_channels_by_cid_console', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_game_channels_by_cid_console(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/game/channels/:cid/console. See the API reference for scopes and payloads."""
        return self.call('post_chat_game_channels_by_cid_console', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_game_servers_by_sid_audit(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/game/servers/:sid/audit. See the API reference for scopes and payloads."""
        return self.call('get_chat_game_servers_by_sid_audit', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_invite_by_code(self, *, code, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/invite/:code. See the API reference for scopes and payloads."""
        return self.call('get_chat_invite_by_code', code=code, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_identities(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/identities. See the API reference for scopes and payloads."""
        return self.call('get_chat_identities', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_server_creation_policy(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/server-creation-policy. See the API reference for scopes and payloads."""
        return self.call('get_chat_server_creation_policy', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_servers(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/servers. See the API reference for scopes and payloads."""
        return self.call('get_chat_servers', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_discover(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/discover. See the API reference for scopes and payloads."""
        return self.call('get_chat_discover', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/servers/:sid. See the API reference for scopes and payloads."""
        return self.call('get_chat_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/servers/:sid. See the API reference for scopes and payloads."""
        return self.call('patch_chat_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_servers_by_sid_layout(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/servers/:sid/layout. See the API reference for scopes and payloads."""
        return self.call('put_chat_servers_by_sid_layout', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_roles(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/roles. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_roles', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_servers_by_sid_roles_order(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/servers/:sid/roles/order. See the API reference for scopes and payloads."""
        return self.call('put_chat_servers_by_sid_roles_order', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_servers_by_sid_roles_by_rid(self, *, sid, rid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/servers/:sid/roles/:rid. See the API reference for scopes and payloads."""
        return self.call('patch_chat_servers_by_sid_roles_by_rid', sid=sid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid_roles_by_rid(self, *, sid, rid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid/roles/:rid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid_roles_by_rid', sid=sid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_servers_by_sid_members_by_username_roles_by_rid(self, *, sid, username, rid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/servers/:sid/members/:username/roles/:rid. See the API reference for scopes and payloads."""
        return self.call('put_chat_servers_by_sid_members_by_username_roles_by_rid', sid=sid, username=username, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid_members_by_username_roles_by_rid(self, *, sid, username, rid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid/members/:username/roles/:rid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid_members_by_username_roles_by_rid', sid=sid, username=username, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_roles_by_rid_icon(self, *, sid, rid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/roles/:rid/icon. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_roles_by_rid_icon', sid=sid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid_roles_by_rid_icon(self, *, sid, rid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid/roles/:rid/icon. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid_roles_by_rid_icon', sid=sid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_channels_by_cid_icon(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/channels/:cid/icon. See the API reference for scopes and payloads."""
        return self.call('post_chat_channels_by_cid_icon', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_servers_by_sid_export(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/servers/:sid/export. See the API reference for scopes and payloads."""
        return self.call('get_chat_servers_by_sid_export', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_export_to_account(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/export-to-account. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_export_to_account', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_join(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/join. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_join', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_join_by_code(self, *, code, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/join/:code. See the API reference for scopes and payloads."""
        return self.call('post_chat_join_by_code', code=code, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_leave(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/leave. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_leave', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_servers_by_sid_members(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/servers/:sid/members. See the API reference for scopes and payloads."""
        return self.call('get_chat_servers_by_sid_members', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid_members_by_username(self, *, sid, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid/members/:username. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid_members_by_username', sid=sid, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid_bans_by_username(self, *, sid, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid/bans/:username. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid_bans_by_username', sid=sid, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_icon(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/icon. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_icon', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_banner(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/banner. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_banner', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid_icon(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid/icon. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid_icon', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid_banner(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid/banner. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid_banner', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_channels(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/channels. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_channels', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_channels_by_cid(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/channels/:cid. See the API reference for scopes and payloads."""
        return self.call('patch_chat_channels_by_cid', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_channels_by_cid(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/channels/:cid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_channels_by_cid', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_channels_by_cid_cloudlink(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/channels/:cid/cloudlink. See the API reference for scopes and payloads."""
        return self.call('get_chat_channels_by_cid_cloudlink', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_channels_by_cid_cloudlink_reconnect(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/channels/:cid/cloudlink/reconnect. See the API reference for scopes and payloads."""
        return self.call('post_chat_channels_by_cid_cloudlink_reconnect', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_channels_by_cid_messages(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/channels/:cid/messages. See the API reference for scopes and payloads."""
        return self.call('get_chat_channels_by_cid_messages', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_channels_by_cid_messages(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/channels/:cid/messages. See the API reference for scopes and payloads."""
        return self.call('post_chat_channels_by_cid_messages', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_channels_by_cid_read(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/channels/:cid/read. See the API reference for scopes and payloads."""
        return self.call('post_chat_channels_by_cid_read', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_channels_by_cid_search(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/channels/:cid/search. See the API reference for scopes and payloads."""
        return self.call('get_chat_channels_by_cid_search', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_messages_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/messages/:id. See the API reference for scopes and payloads."""
        return self.call('patch_chat_messages_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_messages_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/messages/:id. See the API reference for scopes and payloads."""
        return self.call('delete_chat_messages_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_upload(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/upload. See the API reference for scopes and payloads."""
        return self.call('post_chat_upload', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_notify(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/notify. See the API reference for scopes and payloads."""
        return self.call('get_chat_notify', query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_notify_by_target(self, *, target, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/notify/:target. See the API reference for scopes and payloads."""
        return self.call('put_chat_notify_by_target', target=target, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/settings. See the API reference for scopes and payloads."""
        return self.call('get_chat_settings', query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/settings. See the API reference for scopes and payloads."""
        return self.call('patch_chat_settings', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_open(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/open. See the API reference for scopes and payloads."""
        return self.call('get_chat_open', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_users_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/users/:username. See the API reference for scopes and payloads."""
        return self.call('get_chat_users_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_bots(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/bots. See the API reference for scopes and payloads."""
        return self.call('get_chat_bots', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_bots(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/bots. See the API reference for scopes and payloads."""
        return self.call('post_chat_bots', query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_bots_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/bots/:id. See the API reference for scopes and payloads."""
        return self.call('patch_chat_bots_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_bots_by_id_avatar(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/bots/:id/avatar. See the API reference for scopes and payloads."""
        return self.call('post_chat_bots_by_id_avatar', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_bots_by_id_token(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/bots/:id/token. See the API reference for scopes and payloads."""
        return self.call('post_chat_bots_by_id_token', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_bots_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/bots/:id. See the API reference for scopes and payloads."""
        return self.call('delete_chat_bots_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_bots_by_name_by_username_add(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/bots/by-name/:username/add. See the API reference for scopes and payloads."""
        return self.call('post_chat_bots_by_name_by_username_add', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_presence_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/presence/:username. See the API reference for scopes and payloads."""
        return self.call('get_chat_presence_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_presence_status(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/presence/status. See the API reference for scopes and payloads."""
        return self.call('post_chat_presence_status', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_presence_custom(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/presence/custom. See the API reference for scopes and payloads."""
        return self.call('post_chat_presence_custom', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_presence_activity(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/presence/activity. See the API reference for scopes and payloads."""
        return self.call('post_chat_presence_activity', query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_presence_activity_by_key(self, *, key=None, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/presence/activity/:key?. See the API reference for scopes and payloads."""
        return self.call('delete_chat_presence_activity_by_key', key=key, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_gifs(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/gifs. See the API reference for scopes and payloads."""
        return self.call('get_chat_gifs', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_media(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/media. See the API reference for scopes and payloads."""
        return self.call('get_chat_media', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_media_save(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/media/save. See the API reference for scopes and payloads."""
        return self.call('post_chat_media_save', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_klipy_by_kind_by_slug(self, *, kind, slug, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/klipy/:kind/:slug. See the API reference for scopes and payloads."""
        return self.call('get_chat_klipy_by_kind_by_slug', kind=kind, slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_media_gif(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/media/gif. See the API reference for scopes and payloads."""
        return self.call('post_chat_media_gif', query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_media_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/media/:id. See the API reference for scopes and payloads."""
        return self.call('delete_chat_media_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_media(self, *, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/media. See the API reference for scopes and payloads."""
        return self.call('delete_chat_media', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_media_limits(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/media/limits. See the API reference for scopes and payloads."""
        return self.call('get_chat_media_limits', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_media_upload(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/media/upload. See the API reference for scopes and payloads."""
        return self.call('post_chat_media_upload', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_emojis(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/emojis. See the API reference for scopes and payloads."""
        return self.call('get_chat_emojis', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_emojis_by_eid_info(self, *, eid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/emojis/:eid/info. See the API reference for scopes and payloads."""
        return self.call('get_chat_emojis_by_eid_info', eid=eid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_servers_by_sid_emojis(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/servers/:sid/emojis. See the API reference for scopes and payloads."""
        return self.call('get_chat_servers_by_sid_emojis', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_emojis(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/emojis. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_emojis', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_servers_by_sid_emojis_by_eid(self, *, sid, eid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/servers/:sid/emojis/:eid. See the API reference for scopes and payloads."""
        return self.call('patch_chat_servers_by_sid_emojis_by_eid', sid=sid, eid=eid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid_emojis_by_eid(self, *, sid, eid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid/emojis/:eid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid_emojis_by_eid', sid=sid, eid=eid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_personal_emojis(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/personal-emojis. See the API reference for scopes and payloads."""
        return self.call('get_chat_personal_emojis', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_personal_emojis(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/personal-emojis. See the API reference for scopes and payloads."""
        return self.call('post_chat_personal_emojis', query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_personal_emojis_by_eid(self, *, eid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/personal-emojis/:eid. See the API reference for scopes and payloads."""
        return self.call('patch_chat_personal_emojis_by_eid', eid=eid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_personal_emojis_by_eid(self, *, eid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/personal-emojis/:eid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_personal_emojis_by_eid', eid=eid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_bridge_platforms(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/bridge/platforms. See the API reference for scopes and payloads."""
        return self.call('get_chat_bridge_platforms', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_bridge_by_platform_guilds(self, *, platform, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/bridge/:platform/guilds. See the API reference for scopes and payloads."""
        return self.call('get_chat_bridge_by_platform_guilds', platform=platform, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_bridge_by_platform_guilds_by_gid(self, *, platform, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/bridge/:platform/guilds/:gid. See the API reference for scopes and payloads."""
        return self.call('get_chat_bridge_by_platform_guilds_by_gid', platform=platform, gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_bridge_by_platform_guilds_by_gid_import(self, *, platform, gid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/bridge/:platform/guilds/:gid/import. See the API reference for scopes and payloads."""
        return self.call('post_chat_bridge_by_platform_guilds_by_gid_import', platform=platform, gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_bridge_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/bridge/servers/:sid. See the API reference for scopes and payloads."""
        return self.call('get_chat_bridge_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_bridge_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/bridge/servers/:sid. See the API reference for scopes and payloads."""
        return self.call('put_chat_bridge_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_bridge_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/bridge/servers/:sid. See the API reference for scopes and payloads."""
        return self.call('patch_chat_bridge_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_bridge_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/bridge/servers/:sid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_bridge_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_bridge_servers_by_sid_channels_by_cid(self, *, sid, cid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/bridge/servers/:sid/channels/:cid. See the API reference for scopes and payloads."""
        return self.call('put_chat_bridge_servers_by_sid_channels_by_cid', sid=sid, cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_media_temp(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/media/temp. See the API reference for scopes and payloads."""
        return self.call('post_chat_media_temp', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_media_external(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/media/external. See the API reference for scopes and payloads."""
        return self.call('post_chat_media_external', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_media_account(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/media/account. See the API reference for scopes and payloads."""
        return self.call('post_chat_media_account', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_media_destinations(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/media/destinations. See the API reference for scopes and payloads."""
        return self.call('get_chat_media_destinations', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_servers_by_sid_search(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/servers/:sid/search. See the API reference for scopes and payloads."""
        return self.call('get_chat_servers_by_sid_search', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_channels_by_cid_starboard(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/channels/:cid/starboard. See the API reference for scopes and payloads."""
        return self.call('get_chat_channels_by_cid_starboard', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_messages_by_id_reactions_by_emoji(self, *, id, emoji, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/messages/:id/reactions/:emoji. See the API reference for scopes and payloads."""
        return self.call('put_chat_messages_by_id_reactions_by_emoji', id=id, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_messages_by_id_reactions_by_emoji(self, *, id, emoji, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/messages/:id/reactions/:emoji. See the API reference for scopes and payloads."""
        return self.call('delete_chat_messages_by_id_reactions_by_emoji', id=id, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_dm_by_id_reactions_by_emoji(self, *, id, emoji, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/dm/:id/reactions/:emoji. See the API reference for scopes and payloads."""
        return self.call('put_chat_dm_by_id_reactions_by_emoji', id=id, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_dm_by_id_reactions_by_emoji(self, *, id, emoji, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/dm/:id/reactions/:emoji. See the API reference for scopes and payloads."""
        return self.call('delete_chat_dm_by_id_reactions_by_emoji', id=id, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_channels_by_cid_perms(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/channels/:cid/perms. See the API reference for scopes and payloads."""
        return self.call('put_chat_channels_by_cid_perms', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_modmail(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/modmail. See the API reference for scopes and payloads."""
        return self.call('get_chat_modmail', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_modmail_read(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/modmail/read. See the API reference for scopes and payloads."""
        return self.call('post_chat_modmail_read', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_modmail_staff(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/modmail/staff. See the API reference for scopes and payloads."""
        return self.call('get_chat_modmail_staff', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_modmail_with_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/modmail/with/:username. See the API reference for scopes and payloads."""
        return self.call('get_chat_modmail_with_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_modmail_with_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/modmail/with/:username. See the API reference for scopes and payloads."""
        return self.call('post_chat_modmail_with_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_sounds(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/sounds. See the API reference for scopes and payloads."""
        return self.call('get_chat_sounds', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_servers_by_sid_sounds(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/servers/:sid/sounds. See the API reference for scopes and payloads."""
        return self.call('get_chat_servers_by_sid_sounds', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_servers_by_sid_sounds(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/servers/:sid/sounds. See the API reference for scopes and payloads."""
        return self.call('post_chat_servers_by_sid_sounds', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_servers_by_sid_sounds_by_id(self, *, sid, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/servers/:sid/sounds/:id. See the API reference for scopes and payloads."""
        return self.call('patch_chat_servers_by_sid_sounds_by_id', sid=sid, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_servers_by_sid_sounds_by_id(self, *, sid, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/servers/:sid/sounds/:id. See the API reference for scopes and payloads."""
        return self.call('delete_chat_servers_by_sid_sounds_by_id', sid=sid, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_messages_by_id_pin(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/messages/:id/pin. See the API reference for scopes and payloads."""
        return self.call('put_chat_messages_by_id_pin', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_messages_by_id_pin(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/messages/:id/pin. See the API reference for scopes and payloads."""
        return self.call('delete_chat_messages_by_id_pin', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_channels_by_cid_pins(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/channels/:cid/pins. See the API reference for scopes and payloads."""
        return self.call('get_chat_channels_by_cid_pins', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_translate(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/translate. See the API reference for scopes and payloads."""
        return self.call('post_chat_translate', query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_saved_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/saved/:id. See the API reference for scopes and payloads."""
        return self.call('delete_chat_saved_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_saved(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/saved. See the API reference for scopes and payloads."""
        return self.call('post_chat_saved', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_saved_check(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/saved/check. See the API reference for scopes and payloads."""
        return self.call('post_chat_saved_check', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_saved(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/saved. See the API reference for scopes and payloads."""
        return self.call('get_chat_saved', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_inbox_mentions(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/inbox/mentions. See the API reference for scopes and payloads."""
        return self.call('get_chat_inbox_mentions', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_beta(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/beta. See the API reference for scopes and payloads."""
        return self.call('get_chat_beta', query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_beta_refresh(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/beta/refresh. See the API reference for scopes and payloads."""
        return self.call('post_chat_beta_refresh', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_channels_by_cid_viewers(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/channels/:cid/viewers. See the API reference for scopes and payloads."""
        return self.call('get_chat_channels_by_cid_viewers', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_unfurl(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/unfurl. See the API reference for scopes and payloads."""
        return self.call('get_chat_unfurl', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_hf_game_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/hf-game/:id. See the API reference for scopes and payloads."""
        return self.call('get_chat_hf_game_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_calls(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/calls. See the API reference for scopes and payloads."""
        return self.call('post_chat_calls', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_channels_by_cid_shop(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/channels/:cid/shop. See the API reference for scopes and payloads."""
        return self.call('get_chat_channels_by_cid_shop', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_channels_by_cid_shop_by_rid(self, *, cid, rid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/channels/:cid/shop/:rid. See the API reference for scopes and payloads."""
        return self.call('post_chat_channels_by_cid_shop_by_rid', cid=cid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_channels_by_cid_shop_by_rid(self, *, cid, rid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/channels/:cid/shop/:rid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_channels_by_cid_shop_by_rid', cid=cid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_channels_by_cid_webhooks(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/channels/:cid/webhooks. See the API reference for scopes and payloads."""
        return self.call('get_chat_channels_by_cid_webhooks', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_channels_by_cid_webhooks(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/channels/:cid/webhooks. See the API reference for scopes and payloads."""
        return self.call('post_chat_channels_by_cid_webhooks', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_hooks_by_wid(self, *, wid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/hooks/:wid. See the API reference for scopes and payloads."""
        return self.call('patch_chat_hooks_by_wid', wid=wid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_hooks_by_wid(self, *, wid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/hooks/:wid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_hooks_by_wid', wid=wid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_hooks_by_wid_avatar(self, *, wid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/hooks/:wid/avatar. See the API reference for scopes and payloads."""
        return self.call('post_chat_hooks_by_wid_avatar', wid=wid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_discovery(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/discovery. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_discovery', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_gateway(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/gateway. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_gateway', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_gateway_bot(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/gateway/bot. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_gateway_bot', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_users_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/users/@me. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_users_me', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_oauth2_applications_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/oauth2/applications/@me. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_oauth2_applications_me', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_users_me_guilds(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/users/@me/guilds. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_users_me_guilds', query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_api_v1_users_me_guilds_by_gid(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/api/v1/users/@me/guilds/:gid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_api_v1_users_me_guilds_by_gid', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_users_by_uid(self, *, uid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/users/:uid. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_users_by_uid', uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_api_v1_users_me_channels(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/api/v1/users/@me/channels. See the API reference for scopes and payloads."""
        return self.call('post_chat_api_v1_users_me_channels', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_guilds_by_gid(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/guilds/:gid. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_guilds_by_gid', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_guilds_by_gid_roles(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/guilds/:gid/roles. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_guilds_by_gid_roles', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_guilds_by_gid_channels(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/guilds/:gid/channels. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_guilds_by_gid_channels', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_guilds_by_gid_members_by_uid(self, *, gid, uid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/guilds/:gid/members/:uid. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_guilds_by_gid_members_by_uid', gid=gid, uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_guilds_by_gid_members(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/guilds/:gid/members. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_guilds_by_gid_members', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_channels_by_cid(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/channels/:cid. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_channels_by_cid', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_api_v1_channels_by_cid_typing(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/api/v1/channels/:cid/typing. See the API reference for scopes and payloads."""
        return self.call('post_chat_api_v1_channels_by_cid_typing', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_channels_by_cid_messages(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/channels/:cid/messages. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_channels_by_cid_messages', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_api_v1_channels_by_cid_messages_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/api/v1/channels/:cid/messages/:mid. See the API reference for scopes and payloads."""
        return self.call('get_chat_api_v1_channels_by_cid_messages_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_api_v1_channels_by_cid_messages(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/api/v1/channels/:cid/messages. See the API reference for scopes and payloads."""
        return self.call('post_chat_api_v1_channels_by_cid_messages', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_chat_api_v1_channels_by_cid_messages_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /chat/api/v1/channels/:cid/messages/:mid. See the API reference for scopes and payloads."""
        return self.call('patch_chat_api_v1_channels_by_cid_messages_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_api_v1_channels_by_cid_messages_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/api/v1/channels/:cid/messages/:mid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_api_v1_channels_by_cid_messages_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_api_v1_channels_by_cid_messages_by_mid_reactions_by_emoji_me(self, *, cid, mid, emoji, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/api/v1/channels/:cid/messages/:mid/reactions/:emoji/@me. See the API reference for scopes and payloads."""
        return self.call('put_chat_api_v1_channels_by_cid_messages_by_mid_reactions_by_emoji_me', cid=cid, mid=mid, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_api_v1_channels_by_cid_messages_by_mid_reactions_by_emoji_me(self, *, cid, mid, emoji, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/api/v1/channels/:cid/messages/:mid/reactions/:emoji/@me. See the API reference for scopes and payloads."""
        return self.call('delete_chat_api_v1_channels_by_cid_messages_by_mid_reactions_by_emoji_me', cid=cid, mid=mid, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_api_v1_channels_by_cid_pins_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/api/v1/channels/:cid/pins/:mid. See the API reference for scopes and payloads."""
        return self.call('put_chat_api_v1_channels_by_cid_pins_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_api_v1_channels_by_cid_pins_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/api/v1/channels/:cid/pins/:mid. See the API reference for scopes and payloads."""
        return self.call('delete_chat_api_v1_channels_by_cid_pins_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def post_bot_payment_requests(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bot/payment-requests. See the API reference for scopes and payloads."""
        return self.call('post_bot_payment_requests', query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_payment_requests(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/payment-requests. See the API reference for scopes and payloads."""
        return self.call('get_bot_payment_requests', query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_payment_requests_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/payment-requests/:id. See the API reference for scopes and payloads."""
        return self.call('get_bot_payment_requests_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_bot_payment_requests_by_id_cancel(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /bot/payment-requests/:id/cancel. See the API reference for scopes and payloads."""
        return self.call('post_bot_payment_requests_by_id_cancel', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_bot_carts(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bot/carts. See the API reference for scopes and payloads."""
        return self.call('post_bot_carts', query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_carts(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/carts. See the API reference for scopes and payloads."""
        return self.call('get_bot_carts', query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_carts_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/carts/:id. See the API reference for scopes and payloads."""
        return self.call('get_bot_carts_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_bot_carts_by_id_cancel(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /bot/carts/:id/cancel. See the API reference for scopes and payloads."""
        return self.call('post_bot_carts_by_id_cancel', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_webhooks_by_wid_by_token(self, *, wid, token, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/webhooks/:wid/:token. See the API reference for scopes and payloads."""
        return self.call('get_chat_webhooks_by_wid_by_token', wid=wid, token=token, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_webhooks_by_wid_by_token(self, *, wid, token, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/webhooks/:wid/:token. See the API reference for scopes and payloads."""
        return self.call('post_chat_webhooks_by_wid_by_token', wid=wid, token=token, query=query, json=json, data=data, files=files, raw=raw)

    def delete_chat_webhooks_by_wid_by_token(self, *, wid, token, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /chat/webhooks/:wid/:token. See the API reference for scopes and payloads."""
        return self.call('delete_chat_webhooks_by_wid_by_token', wid=wid, token=token, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_yt_by_id_prepare(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/yt/:id/prepare. See the API reference for scopes and payloads."""
        return self.call('post_chat_yt_by_id_prepare', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_yt_by_id_status(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/yt/:id/status. See the API reference for scopes and payloads."""
        return self.call('get_chat_yt_by_id_status', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_yt_by_id_save(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/yt/:id/save. See the API reference for scopes and payloads."""
        return self.call('post_chat_yt_by_id_save', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_yt_stream_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/yt/stream/:id. See the API reference for scopes and payloads."""
        return self.call('get_chat_yt_stream_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_achievements(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /achievements. See the API reference for scopes and payloads."""
        return self.call('get_achievements', query=query, json=json, data=data, files=files, raw=raw)

    def post_achievements_by_id_grant(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /achievements/:id/grant. See the API reference for scopes and payloads."""
        return self.call('post_achievements_by_id_grant', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_achievements_by_id_revoke(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /achievements/:id/revoke. See the API reference for scopes and payloads."""
        return self.call('post_achievements_by_id_revoke', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_currency_balance(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /currency/balance. See the API reference for scopes and payloads."""
        return self.call('get_currency_balance', query=query, json=json, data=data, files=files, raw=raw)

    def get_currency_economy(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /currency/economy. See the API reference for scopes and payloads."""
        return self.call('get_currency_economy', query=query, json=json, data=data, files=files, raw=raw)

    def get_currency_captcha_status(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /currency/captcha-status. See the API reference for scopes and payloads."""
        return self.call('get_currency_captcha_status', query=query, json=json, data=data, files=files, raw=raw)

    def post_currency_transfer(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /currency/transfer. See the API reference for scopes and payloads."""
        return self.call('post_currency_transfer', query=query, json=json, data=data, files=files, raw=raw)

    def get_currency_transactions(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /currency/transactions. See the API reference for scopes and payloads."""
        return self.call('get_currency_transactions', query=query, json=json, data=data, files=files, raw=raw)

    def post_currency_subscribe(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /currency/subscribe. See the API reference for scopes and payloads."""
        return self.call('post_currency_subscribe', query=query, json=json, data=data, files=files, raw=raw)

    def delete_currency_subscribe_user_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /currency/subscribe/user/:username. See the API reference for scopes and payloads."""
        return self.call('delete_currency_subscribe_user_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_currency_subscriptions_outgoing(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /currency/subscriptions/outgoing. See the API reference for scopes and payloads."""
        return self.call('get_currency_subscriptions_outgoing', query=query, json=json, data=data, files=files, raw=raw)

    def get_currency_subscriptions_incoming(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /currency/subscriptions/incoming. See the API reference for scopes and payloads."""
        return self.call('get_currency_subscriptions_incoming', query=query, json=json, data=data, files=files, raw=raw)

    def post_currency_daily_claim(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /currency/daily-claim. See the API reference for scopes and payloads."""
        return self.call('post_currency_daily_claim', query=query, json=json, data=data, files=files, raw=raw)

    def get_currency_credit_sub(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /currency/credit-sub. See the API reference for scopes and payloads."""
        return self.call('get_currency_credit_sub', query=query, json=json, data=data, files=files, raw=raw)

    def post_currency_credit_sub_buy(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /currency/credit-sub/buy. See the API reference for scopes and payloads."""
        return self.call('post_currency_credit_sub_buy', query=query, json=json, data=data, files=files, raw=raw)

    def post_currency_credit_sub_cancel(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /currency/credit-sub/cancel. See the API reference for scopes and payloads."""
        return self.call('post_currency_credit_sub_cancel', query=query, json=json, data=data, files=files, raw=raw)

    def post_currency_credit_sub_ack(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /currency/credit-sub/ack. See the API reference for scopes and payloads."""
        return self.call('post_currency_credit_sub_ack', query=query, json=json, data=data, files=files, raw=raw)

    def post_currency_transfer_request(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /currency/transfer-request. See the API reference for scopes and payloads."""
        return self.call('post_currency_transfer_request', query=query, json=json, data=data, files=files, raw=raw)

    def get_currency_transfer_request_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /currency/transfer-request/:id. See the API reference for scopes and payloads."""
        return self.call('get_currency_transfer_request_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_currency_transfer_request_by_id_confirm(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /currency/transfer-request/:id/confirm. See the API reference for scopes and payloads."""
        return self.call('post_currency_transfer_request_by_id_confirm', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_currency_transfer_request_by_id_cancel(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /currency/transfer-request/:id/cancel. See the API reference for scopes and payloads."""
        return self.call('post_currency_transfer_request_by_id_cancel', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_badges_user_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /badges/user/:username. See the API reference for scopes and payloads."""
        return self.call('get_badges_user_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_badges_all(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /badges/all. See the API reference for scopes and payloads."""
        return self.call('get_badges_all', query=query, json=json, data=data, files=files, raw=raw)

    def get_badges_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /badges/:id. See the API reference for scopes and payloads."""
        return self.call('get_badges_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_media_pfp(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /media/pfp. See the API reference for scopes and payloads."""
        return self.call('post_media_pfp', query=query, json=json, data=data, files=files, raw=raw)

    def post_media_banner(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /media/banner. See the API reference for scopes and payloads."""
        return self.call('post_media_banner', query=query, json=json, data=data, files=files, raw=raw)

    def delete_media_pfp(self, *, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /media/pfp. See the API reference for scopes and payloads."""
        return self.call('delete_media_pfp', query=query, json=json, data=data, files=files, raw=raw)

    def delete_media_banner(self, *, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /media/banner. See the API reference for scopes and payloads."""
        return self.call('delete_media_banner', query=query, json=json, data=data, files=files, raw=raw)

    def post_media_image(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /media/image. See the API reference for scopes and payloads."""
        return self.call('post_media_image', query=query, json=json, data=data, files=files, raw=raw)

    def post_media_audio(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /media/audio. See the API reference for scopes and payloads."""
        return self.call('post_media_audio', query=query, json=json, data=data, files=files, raw=raw)

    def post_media_video_chunk(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /media/video/chunk. See the API reference for scopes and payloads."""
        return self.call('post_media_video_chunk', query=query, json=json, data=data, files=files, raw=raw)

    def post_media_video_finalize(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /media/video/finalize. See the API reference for scopes and payloads."""
        return self.call('post_media_video_finalize', query=query, json=json, data=data, files=files, raw=raw)

    def post_media_video(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /media/video. See the API reference for scopes and payloads."""
        return self.call('post_media_video', query=query, json=json, data=data, files=files, raw=raw)

    def get_media_list(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /media/list. See the API reference for scopes and payloads."""
        return self.call('get_media_list', query=query, json=json, data=data, files=files, raw=raw)

    def delete_media_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /media/:id. See the API reference for scopes and payloads."""
        return self.call('delete_media_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_notifications(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /notifications. See the API reference for scopes and payloads."""
        return self.call('get_notifications', query=query, json=json, data=data, files=files, raw=raw)

    def get_notifications_count(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /notifications/count. See the API reference for scopes and payloads."""
        return self.call('get_notifications_count', query=query, json=json, data=data, files=files, raw=raw)

    def patch_notifications_read_all(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /notifications/read-all. See the API reference for scopes and payloads."""
        return self.call('patch_notifications_read_all', query=query, json=json, data=data, files=files, raw=raw)

    def delete_notifications_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /notifications/:id. See the API reference for scopes and payloads."""
        return self.call('delete_notifications_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_products_mine(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /products/mine. See the API reference for scopes and payloads."""
        return self.call('get_products_mine', query=query, json=json, data=data, files=files, raw=raw)

    def get_products_limits(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /products/limits. See the API reference for scopes and payloads."""
        return self.call('get_products_limits', query=query, json=json, data=data, files=files, raw=raw)

    def post_products_limits_apply(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /products/limits/apply. See the API reference for scopes and payloads."""
        return self.call('post_products_limits_apply', query=query, json=json, data=data, files=files, raw=raw)

    def get_products_sales(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /products/sales. See the API reference for scopes and payloads."""
        return self.call('get_products_sales', query=query, json=json, data=data, files=files, raw=raw)

    def post_products_sales_by_line_refund(self, *, line, query=None, json=None, data=None, files=None, raw=False):
        """POST /products/sales/:line/refund. See the API reference for scopes and payloads."""
        return self.call('post_products_sales_by_line_refund', line=line, query=query, json=json, data=data, files=files, raw=raw)

    def post_products_members_by_id_end(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /products/members/:id/end. See the API reference for scopes and payloads."""
        return self.call('post_products_members_by_id_end', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_products(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /products. See the API reference for scopes and payloads."""
        return self.call('get_products', query=query, json=json, data=data, files=files, raw=raw)

    def post_products(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /products. See the API reference for scopes and payloads."""
        return self.call('post_products', query=query, json=json, data=data, files=files, raw=raw)

    def get_products_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /products/:id. See the API reference for scopes and payloads."""
        return self.call('get_products_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_products_by_id_access(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /products/:id/access. See the API reference for scopes and payloads."""
        return self.call('get_products_by_id_access', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def patch_products_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /products/:id. See the API reference for scopes and payloads."""
        return self.call('patch_products_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_products_by_id_archive(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /products/:id/archive. See the API reference for scopes and payloads."""
        return self.call('post_products_by_id_archive', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_products_by_id_restore(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /products/:id/restore. See the API reference for scopes and payloads."""
        return self.call('post_products_by_id_restore', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_products_by_id_members(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /products/:id/members. See the API reference for scopes and payloads."""
        return self.call('get_products_by_id_members', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_products_by_id_icon(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /products/:id/icon. See the API reference for scopes and payloads."""
        return self.call('post_products_by_id_icon', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_products_by_id_icon(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /products/:id/icon. See the API reference for scopes and payloads."""
        return self.call('delete_products_by_id_icon', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_cart(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /cart. See the API reference for scopes and payloads."""
        return self.call('get_cart', query=query, json=json, data=data, files=files, raw=raw)

    def get_cart_shared_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /cart/shared/:id. See the API reference for scopes and payloads."""
        return self.call('get_cart_shared_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_cart_items(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /cart/items. See the API reference for scopes and payloads."""
        return self.call('post_cart_items', query=query, json=json, data=data, files=files, raw=raw)

    def patch_cart_items_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /cart/items/:id. See the API reference for scopes and payloads."""
        return self.call('patch_cart_items_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_cart_items_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /cart/items/:id. See the API reference for scopes and payloads."""
        return self.call('delete_cart_items_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_cart(self, *, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /cart. See the API reference for scopes and payloads."""
        return self.call('delete_cart', query=query, json=json, data=data, files=files, raw=raw)

    def post_checkout_pay(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /checkout/pay. See the API reference for scopes and payloads."""
        return self.call('post_checkout_pay', query=query, json=json, data=data, files=files, raw=raw)

    def post_checkout_shared_by_id_pay(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /checkout/shared/:id/pay. See the API reference for scopes and payloads."""
        return self.call('post_checkout_shared_by_id_pay', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_checkout_direct_quote(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /checkout/direct/quote. See the API reference for scopes and payloads."""
        return self.call('post_checkout_direct_quote', query=query, json=json, data=data, files=files, raw=raw)

    def post_checkout_direct(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /checkout/direct. See the API reference for scopes and payloads."""
        return self.call('post_checkout_direct', query=query, json=json, data=data, files=files, raw=raw)

    def get_purchases(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /purchases. See the API reference for scopes and payloads."""
        return self.call('get_purchases', query=query, json=json, data=data, files=files, raw=raw)

    def get_purchases_memberships(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /purchases/memberships. See the API reference for scopes and payloads."""
        return self.call('get_purchases_memberships', query=query, json=json, data=data, files=files, raw=raw)

    def post_purchases_memberships_by_id_cancel(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /purchases/memberships/:id/cancel. See the API reference for scopes and payloads."""
        return self.call('post_purchases_memberships_by_id_cancel', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_purchases_memberships_by_id_keep(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /purchases/memberships/:id/keep. See the API reference for scopes and payloads."""
        return self.call('post_purchases_memberships_by_id_keep', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_purchases_memberships_by_id_pay(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /purchases/memberships/:id/pay. See the API reference for scopes and payloads."""
        return self.call('post_purchases_memberships_by_id_pay', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_store_game_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /store/game/:id. See the API reference for scopes and payloads."""
        return self.call('get_store_game_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_store_game_by_id_buy(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /store/game/:id/buy. See the API reference for scopes and payloads."""
        return self.call('post_store_game_by_id_buy', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_store_game_by_id_refund(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /store/game/:id/refund. See the API reference for scopes and payloads."""
        return self.call('post_store_game_by_id_refund', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_report_search_users(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/report/search-users. See the API reference for scopes and payloads."""
        return self.call('get_api_report_search_users', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_report_search_bots(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/report/search-bots. See the API reference for scopes and payloads."""
        return self.call('get_api_report_search_bots', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_report_submit(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/report/submit. See the API reference for scopes and payloads."""
        return self.call('post_api_report_submit', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_report_dm_message(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/report/dm-message. See the API reference for scopes and payloads."""
        return self.call('post_api_report_dm_message', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_report_ban_guest_ip(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/report/ban-guest-ip. See the API reference for scopes and payloads."""
        return self.call('get_api_report_ban_guest_ip', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_feedback_by_type_submit(self, *, type, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/feedback/:type/submit. See the API reference for scopes and payloads."""
        return self.call('post_api_feedback_by_type_submit', type=type, query=query, json=json, data=data, files=files, raw=raw)

    def get_hyperfocus_profile_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /hyperfocus/profile/:username. See the API reference for scopes and payloads."""
        return self.call('get_hyperfocus_profile_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_hyperfocus_achievements_stats_by_game(self, *, game, query=None, json=None, data=None, files=None, raw=False):
        """GET /hyperfocus/achievements/stats/:game. See the API reference for scopes and payloads."""
        return self.call('get_hyperfocus_achievements_stats_by_game', game=game, query=query, json=json, data=data, files=files, raw=raw)

    def get_hyperfocus_friends(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /hyperfocus/friends. See the API reference for scopes and payloads."""
        return self.call('get_hyperfocus_friends', query=query, json=json, data=data, files=files, raw=raw)

    def post_hyperfocus_bug_report(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /hyperfocus/bug-report. See the API reference for scopes and payloads."""
        return self.call('post_hyperfocus_bug_report', query=query, json=json, data=data, files=files, raw=raw)

    def get_connect_spotify_status(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /connect/spotify/status. See the API reference for scopes and payloads."""
        return self.call('get_connect_spotify_status', query=query, json=json, data=data, files=files, raw=raw)

    def post_connect_spotify_link(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /connect/spotify/link. See the API reference for scopes and payloads."""
        return self.call('post_connect_spotify_link', query=query, json=json, data=data, files=files, raw=raw)

    def get_connect_spotify_callback(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /connect/spotify/callback. See the API reference for scopes and payloads."""
        return self.call('get_connect_spotify_callback', query=query, json=json, data=data, files=files, raw=raw)

    def patch_connect_spotify_profile(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /connect/spotify/profile. See the API reference for scopes and payloads."""
        return self.call('patch_connect_spotify_profile', query=query, json=json, data=data, files=files, raw=raw)

    def delete_connect_spotify(self, *, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /connect/spotify. See the API reference for scopes and payloads."""
        return self.call('delete_connect_spotify', query=query, json=json, data=data, files=files, raw=raw)

    def get_push_vapid(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /push/vapid. See the API reference for scopes and payloads."""
        return self.call('get_push_vapid', query=query, json=json, data=data, files=files, raw=raw)

    def get_push_state(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /push/state. See the API reference for scopes and payloads."""
        return self.call('get_push_state', query=query, json=json, data=data, files=files, raw=raw)

    def post_push_subscribe(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /push/subscribe. See the API reference for scopes and payloads."""
        return self.call('post_push_subscribe', query=query, json=json, data=data, files=files, raw=raw)

    def post_push_unsubscribe(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /push/unsubscribe. See the API reference for scopes and payloads."""
        return self.call('post_push_unsubscribe', query=query, json=json, data=data, files=files, raw=raw)

    def patch_push_prefs(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /push/prefs. See the API reference for scopes and payloads."""
        return self.call('patch_push_prefs', query=query, json=json, data=data, files=files, raw=raw)

    def post_push_test(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /push/test. See the API reference for scopes and payloads."""
        return self.call('post_push_test', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_sim_js(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/sim.js. See the API reference for scopes and payloads."""
        return self.call('get_arcade_sim_js', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_sim_sig(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/sim.sig. See the API reference for scopes and payloads."""
        return self.call('get_arcade_sim_sig', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_sim_version(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/sim-version. See the API reference for scopes and payloads."""
        return self.call('get_arcade_sim_version', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_physics_js(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/physics.js. See the API reference for scopes and payloads."""
        return self.call('get_arcade_physics_js', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_physics_sig(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/physics.sig. See the API reference for scopes and payloads."""
        return self.call('get_arcade_physics_sig', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_planck_js(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/planck.js. See the API reference for scopes and payloads."""
        return self.call('get_arcade_planck_js', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_showcase(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/showcase. See the API reference for scopes and payloads."""
        return self.call('get_arcade_showcase', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_atlas_index(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/atlas/index. See the API reference for scopes and payloads."""
        return self.call('get_arcade_atlas_index', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_atlas_by_v_by_page_png(self, *, v, page, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/atlas/:v/:page.png. See the API reference for scopes and payloads."""
        return self.call('get_arcade_atlas_by_v_by_page_png', v=v, page=page, query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_thumb(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/thumb. See the API reference for scopes and payloads."""
        return self.call('get_arcade_thumb', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_state(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/state. See the API reference for scopes and payloads."""
        return self.call('get_arcade_state', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_machine_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/machine/:id. See the API reference for scopes and payloads."""
        return self.call('get_arcade_machine_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_arcade_machine_by_id_play(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /arcade/machine/:id/play. See the API reference for scopes and payloads."""
        return self.call('post_arcade_machine_by_id_play', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_arcade_machine_by_id_reset(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /arcade/machine/:id/reset. See the API reference for scopes and payloads."""
        return self.call('post_arcade_machine_by_id_reset', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_arcade_check(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /arcade/check. See the API reference for scopes and payloads."""
        return self.call('post_arcade_check', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_news(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/news. See the API reference for scopes and payloads."""
        return self.call('get_arcade_news', query=query, json=json, data=data, files=files, raw=raw)

    def post_arcade_tutorial(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /arcade/tutorial. See the API reference for scopes and payloads."""
        return self.call('post_arcade_tutorial', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_book(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/book. See the API reference for scopes and payloads."""
        return self.call('get_arcade_book', query=query, json=json, data=data, files=files, raw=raw)

    def post_arcade_showcase(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /arcade/showcase. See the API reference for scopes and payloads."""
        return self.call('post_arcade_showcase', query=query, json=json, data=data, files=files, raw=raw)

    def put_arcade_board(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PUT /arcade/board. See the API reference for scopes and payloads."""
        return self.call('put_arcade_board', query=query, json=json, data=data, files=files, raw=raw)

    def post_arcade_buy(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /arcade/buy. See the API reference for scopes and payloads."""
        return self.call('post_arcade_buy', query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_purchase_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/purchase/:id. See the API reference for scopes and payloads."""
        return self.call('get_arcade_purchase_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_arcade_purchase_by_id_cancel(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /arcade/purchase/:id/cancel. See the API reference for scopes and payloads."""
        return self.call('post_arcade_purchase_by_id_cancel', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_arcade_profile_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /arcade/profile/:username. See the API reference for scopes and payloads."""
        return self.call('get_arcade_profile_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_bots_gallery(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/bots/gallery. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_bots_gallery', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_bots_gallery_tags(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/bots/gallery/tags. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_bots_gallery_tags', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_bots_gallery_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/bots/gallery/:id. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_bots_gallery_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_bonfire_bots_gallery_by_id_ticket(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /bonfire/bots/gallery/:id/ticket. See the API reference for scopes and payloads."""
        return self.call('post_bonfire_bots_gallery_by_id_ticket', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_bots_self_installs(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/bots/self/installs. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_bots_self_installs', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_bots_by_id_gallery(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/bots/:id/gallery. See the API reference for scopes and payloads."""
        return self.call('get_chat_bots_by_id_gallery', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def put_chat_bots_by_id_gallery(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PUT /chat/bots/:id/gallery. See the API reference for scopes and payloads."""
        return self.call('put_chat_bots_by_id_gallery', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_bots_by_id_gallery_submit(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/bots/:id/gallery/submit. See the API reference for scopes and payloads."""
        return self.call('post_chat_bots_by_id_gallery_submit', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_chat_bots_by_id_gallery_withdraw(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /chat/bots/:id/gallery/withdraw. See the API reference for scopes and payloads."""
        return self.call('post_chat_bots_by_id_gallery_withdraw', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_config(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/config. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_config', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/me. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_me', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_items(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/items. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_items', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_recent(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/recent. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_recent', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_search(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/search. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_search', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_folders(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/folders. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_folders', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_tree(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/tree. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_tree', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_bin(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/bin. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_bin', query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_folders(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/folders. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_folders', query=query, json=json, data=data, files=files, raw=raw)

    def patch_drive_api_items_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /drive/api/items/:id. See the API reference for scopes and payloads."""
        return self.call('patch_drive_api_items_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_items_by_id_trash(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/items/:id/trash. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_items_by_id_trash', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_items_by_id_restore(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/items/:id/restore. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_items_by_id_restore', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_drive_api_items_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /drive/api/items/:id. See the API reference for scopes and payloads."""
        return self.call('delete_drive_api_items_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_bin_empty(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/bin/empty. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_bin_empty', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_items_by_id_shares(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/items/:id/shares. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_items_by_id_shares', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_items_by_id_shares(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/items/:id/shares. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_items_by_id_shares', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_drive_api_items_by_id_shares_by_username(self, *, id, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /drive/api/items/:id/shares/:username. See the API reference for scopes and payloads."""
        return self.call('delete_drive_api_items_by_id_shares_by_username', id=id, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def put_drive_api_items_by_id_share_link(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PUT /drive/api/items/:id/share-link. See the API reference for scopes and payloads."""
        return self.call('put_drive_api_items_by_id_share_link', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_drive_api_items_by_id_share(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /drive/api/items/:id/share. See the API reference for scopes and payloads."""
        return self.call('delete_drive_api_items_by_id_share', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_shared(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/shared. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_shared', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_shared_with_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/shared-with-me. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_shared_with_me', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_s_by_token(self, *, token, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/s/:token. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_s_by_token', token=token, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_s_by_token_items_by_id_link(self, *, token, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/s/:token/items/:id/link. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_s_by_token_items_by_id_link', token=token, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_s_by_token_items_by_id_thumb(self, *, token, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/s/:token/items/:id/thumb. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_s_by_token_items_by_id_thumb', token=token, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_s_by_token_items_by_id_text(self, *, token, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/s/:token/items/:id/text. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_s_by_token_items_by_id_text', token=token, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_s_by_token_join(self, *, token, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/s/:token/join. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_s_by_token_join', token=token, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_uploads(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/uploads. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_uploads', query=query, json=json, data=data, files=files, raw=raw)

    def put_drive_api_uploads_by_id_by_n(self, *, id, n, query=None, json=None, data=None, files=None, raw=False):
        """PUT /drive/api/uploads/:id/:n. See the API reference for scopes and payloads."""
        return self.call('put_drive_api_uploads_by_id_by_n', id=id, n=n, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_uploads_by_id_finish(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/uploads/:id/finish. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_uploads_by_id_finish', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_drive_api_uploads_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /drive/api/uploads/:id. See the API reference for scopes and payloads."""
        return self.call('delete_drive_api_uploads_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_items_by_id_link(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/items/:id/link. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_items_by_id_link', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_items_by_id_thumb(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/items/:id/thumb. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_items_by_id_thumb', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_items_by_id_text(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/items/:id/text. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_items_by_id_text', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_dl(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/dl. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_dl', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_media(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/media. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_media', query=query, json=json, data=data, files=files, raw=raw)

    def post_drive_api_media_by_id_thumb(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /drive/api/media/:id/thumb. See the API reference for scopes and payloads."""
        return self.call('post_drive_api_media_by_id_thumb', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_drive_api_media_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /drive/api/media/:id. See the API reference for scopes and payloads."""
        return self.call('delete_drive_api_media_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_app_files(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/app-files. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_app_files', query=query, json=json, data=data, files=files, raw=raw)

    def get_drive_api_app_file(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /drive/api/app-file. See the API reference for scopes and payloads."""
        return self.call('get_drive_api_app_file', query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_config(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/config. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_config', query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/me. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_me', query=query, json=json, data=data, files=files, raw=raw)

    def patch_forums_api_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /forums/api/me. See the API reference for scopes and payloads."""
        return self.call('patch_forums_api_me', query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_home(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/home. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_home', query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_directory(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/directory. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_directory', query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_categories(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/categories. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_categories', query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_search(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/search. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_search', query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_u_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/u/:username. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_u_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_t_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/t/:id. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_t_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_posts_by_id_where(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/posts/:id/where. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_posts_by_id_where', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_c_by_slug(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/c/:slug. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_c_by_slug', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_c_by_slug_topics(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/c/:slug/topics. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_c_by_slug_topics', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_communities(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/communities. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_communities', query=query, json=json, data=data, files=files, raw=raw)

    def patch_forums_api_c_by_slug(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /forums/api/c/:slug. See the API reference for scopes and payloads."""
        return self.call('patch_forums_api_c_by_slug', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def delete_forums_api_c_by_slug(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /forums/api/c/:slug. See the API reference for scopes and payloads."""
        return self.call('delete_forums_api_c_by_slug', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_restore(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/restore. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_restore', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_transfer(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/transfer. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_transfer', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_report(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/report. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_report', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_c_by_slug_mods(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/c/:slug/mods. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_c_by_slug_mods', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_mods(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/mods. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_mods', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def delete_forums_api_c_by_slug_mods_by_username(self, *, slug, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /forums/api/c/:slug/mods/:username. See the API reference for scopes and payloads."""
        return self.call('delete_forums_api_c_by_slug_mods_by_username', slug=slug, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_join(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/join. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_join', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def delete_forums_api_c_by_slug_join(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /forums/api/c/:slug/join. See the API reference for scopes and payloads."""
        return self.call('delete_forums_api_c_by_slug_join', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_tags(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/tags. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_tags', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def patch_forums_api_tags_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /forums/api/tags/:id. See the API reference for scopes and payloads."""
        return self.call('patch_forums_api_tags_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_forums_api_tags_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /forums/api/tags/:id. See the API reference for scopes and payloads."""
        return self.call('delete_forums_api_tags_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_c_by_slug_allowed(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/c/:slug/allowed. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_c_by_slug_allowed', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_allowed(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/allowed. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_allowed', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def delete_forums_api_c_by_slug_allowed_by_username(self, *, slug, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /forums/api/c/:slug/allowed/:username. See the API reference for scopes and payloads."""
        return self.call('delete_forums_api_c_by_slug_allowed_by_username', slug=slug, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_c_by_slug_bans(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/c/:slug/bans. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_c_by_slug_bans', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_bans(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/bans. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_bans', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def delete_forums_api_c_by_slug_bans_by_username(self, *, slug, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /forums/api/c/:slug/bans/:username. See the API reference for scopes and payloads."""
        return self.call('delete_forums_api_c_by_slug_bans_by_username', slug=slug, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_c_by_slug_queue(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/c/:slug/queue. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_c_by_slug_queue', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_reports_by_id(self, *, slug, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/reports/:id. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_reports_by_id', slug=slug, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_c_by_slug_log(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/c/:slug/log. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_c_by_slug_log', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_c_by_slug_topics(self, *, slug, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/c/:slug/topics. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_c_by_slug_topics', slug=slug, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_t_by_id_posts(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/t/:id/posts. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_t_by_id_posts', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def patch_forums_api_t_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /forums/api/t/:id. See the API reference for scopes and payloads."""
        return self.call('patch_forums_api_t_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_t_by_id_vote(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/t/:id/vote. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_t_by_id_vote', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def patch_forums_api_posts_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /forums/api/posts/:id. See the API reference for scopes and payloads."""
        return self.call('patch_forums_api_posts_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_forums_api_posts_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /forums/api/posts/:id. See the API reference for scopes and payloads."""
        return self.call('delete_forums_api_posts_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_posts_by_id_restore(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/posts/:id/restore. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_posts_by_id_restore', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_posts_by_id_approve(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/posts/:id/approve. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_posts_by_id_approve', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_posts_by_id_reject(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/posts/:id/reject. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_posts_by_id_reject', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_posts_by_id_report(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/posts/:id/report. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_posts_by_id_report', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_upload(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/upload. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_upload', query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_bans(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/bans. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_bans', query=query, json=json, data=data, files=files, raw=raw)

    def get_forums_api_bans(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /forums/api/bans. See the API reference for scopes and payloads."""
        return self.call('get_forums_api_bans', query=query, json=json, data=data, files=files, raw=raw)

    def delete_forums_api_bans_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /forums/api/bans/:username. See the API reference for scopes and payloads."""
        return self.call('delete_forums_api_bans_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_forums_api_categories(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /forums/api/categories. See the API reference for scopes and payloads."""
        return self.call('post_forums_api_categories', query=query, json=json, data=data, files=files, raw=raw)

    def patch_forums_api_categories_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /forums/api/categories/:id. See the API reference for scopes and payloads."""
        return self.call('patch_forums_api_categories_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_forums_api_categories_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /forums/api/categories/:id. See the API reference for scopes and payloads."""
        return self.call('delete_forums_api_categories_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_devices_app_login(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /devices/app-login. See the API reference for scopes and payloads."""
        return self.call('get_devices_app_login', query=query, json=json, data=data, files=files, raw=raw)

    def post_devices_app_exchange(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /devices/app-exchange. See the API reference for scopes and payloads."""
        return self.call('post_devices_app_exchange', query=query, json=json, data=data, files=files, raw=raw)

    def post_devices_app_sign_out(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /devices/app-sign-out. See the API reference for scopes and payloads."""
        return self.call('post_devices_app_sign_out', query=query, json=json, data=data, files=files, raw=raw)

    def get_devices(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /devices. See the API reference for scopes and payloads."""
        return self.call('get_devices', query=query, json=json, data=data, files=files, raw=raw)

    def post_devices_register(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /devices/register. See the API reference for scopes and payloads."""
        return self.call('post_devices_register', query=query, json=json, data=data, files=files, raw=raw)

    def patch_devices_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /devices/:id. See the API reference for scopes and payloads."""
        return self.call('patch_devices_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_devices_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /devices/:id. See the API reference for scopes and payloads."""
        return self.call('delete_devices_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def put_devices_by_id_wallpaper(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PUT /devices/:id/wallpaper. See the API reference for scopes and payloads."""
        return self.call('put_devices_by_id_wallpaper', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_devices_by_id_wallpaper(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /devices/:id/wallpaper. See the API reference for scopes and payloads."""
        return self.call('get_devices_by_id_wallpaper', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_devices_by_id_health(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /devices/:id/health. See the API reference for scopes and payloads."""
        return self.call('post_devices_by_id_health', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_devices_by_id_command(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /devices/:id/command. See the API reference for scopes and payloads."""
        return self.call('post_devices_by_id_command', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_devices_nearby(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /devices/nearby. See the API reference for scopes and payloads."""
        return self.call('get_devices_nearby', query=query, json=json, data=data, files=files, raw=raw)

    def get_devices_ice(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /devices/ice. See the API reference for scopes and payloads."""
        return self.call('get_devices_ice', query=query, json=json, data=data, files=files, raw=raw)

    def post_devices_upload_temp(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /devices/upload/temp. See the API reference for scopes and payloads."""
        return self.call('post_devices_upload_temp', query=query, json=json, data=data, files=files, raw=raw)

    def post_devices_upload_account(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /devices/upload/account. See the API reference for scopes and payloads."""
        return self.call('post_devices_upload_account', query=query, json=json, data=data, files=files, raw=raw)

    def get_devices_temp(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /devices/temp. See the API reference for scopes and payloads."""
        return self.call('get_devices_temp', query=query, json=json, data=data, files=files, raw=raw)

    def delete_devices_temp_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /devices/temp/:id. See the API reference for scopes and payloads."""
        return self.call('delete_devices_temp_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_apps_public_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /apps/public/:id. See the API reference for scopes and payloads."""
        return self.call('get_apps_public_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_apps_scopes(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /apps/scopes. See the API reference for scopes and payloads."""
        return self.call('get_apps_scopes', query=query, json=json, data=data, files=files, raw=raw)

    def get_apps_connected(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /apps/connected. See the API reference for scopes and payloads."""
        return self.call('get_apps_connected', query=query, json=json, data=data, files=files, raw=raw)

    def delete_apps_connected(self, *, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /apps/connected. See the API reference for scopes and payloads."""
        return self.call('delete_apps_connected', query=query, json=json, data=data, files=files, raw=raw)

    def get_apps(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /apps. See the API reference for scopes and payloads."""
        return self.call('get_apps', query=query, json=json, data=data, files=files, raw=raw)

    def post_apps(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /apps. See the API reference for scopes and payloads."""
        return self.call('post_apps', query=query, json=json, data=data, files=files, raw=raw)

    def get_apps_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /apps/:id. See the API reference for scopes and payloads."""
        return self.call('get_apps_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def patch_apps_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /apps/:id. See the API reference for scopes and payloads."""
        return self.call('patch_apps_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_apps_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /apps/:id. See the API reference for scopes and payloads."""
        return self.call('delete_apps_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_apps_by_id_logo(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /apps/:id/logo. See the API reference for scopes and payloads."""
        return self.call('post_apps_by_id_logo', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_apps_by_id_insights(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /apps/:id/insights. See the API reference for scopes and payloads."""
        return self.call('get_apps_by_id_insights', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_apps_by_id_users(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /apps/:id/users. See the API reference for scopes and payloads."""
        return self.call('get_apps_by_id_users', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_apps_by_id_users_by_username_disconnect(self, *, id, username, query=None, json=None, data=None, files=None, raw=False):
        """POST /apps/:id/users/:username/disconnect. See the API reference for scopes and payloads."""
        return self.call('post_apps_by_id_users_by_username_disconnect', id=id, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_apps_by_id_users_by_username_ban(self, *, id, username, query=None, json=None, data=None, files=None, raw=False):
        """POST /apps/:id/users/:username/ban. See the API reference for scopes and payloads."""
        return self.call('post_apps_by_id_users_by_username_ban', id=id, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def delete_apps_by_id_users_by_username_ban(self, *, id, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /apps/:id/users/:username/ban. See the API reference for scopes and payloads."""
        return self.call('delete_apps_by_id_users_by_username_ban', id=id, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_apps_by_id_testers(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /apps/:id/testers. See the API reference for scopes and payloads."""
        return self.call('post_apps_by_id_testers', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_apps_by_id_testers_by_username(self, *, id, username, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /apps/:id/testers/:username. See the API reference for scopes and payloads."""
        return self.call('delete_apps_by_id_testers_by_username', id=id, username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_apps_by_id_submit(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /apps/:id/submit. See the API reference for scopes and payloads."""
        return self.call('post_apps_by_id_submit', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_apps_by_id_withdraw(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /apps/:id/withdraw. See the API reference for scopes and payloads."""
        return self.call('post_apps_by_id_withdraw', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_my_reports(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /my-reports. See the API reference for scopes and payloads."""
        return self.call('get_my_reports', query=query, json=json, data=data, files=files, raw=raw)

    def post_my_reports_claims(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /my-reports/claims. See the API reference for scopes and payloads."""
        return self.call('post_my_reports_claims', query=query, json=json, data=data, files=files, raw=raw)

    def post_my_reports_claims_by_id_messages(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /my-reports/claims/:id/messages. See the API reference for scopes and payloads."""
        return self.call('post_my_reports_claims_by_id_messages', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_moderator_applications_state(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /moderator-applications/state. See the API reference for scopes and payloads."""
        return self.call('get_moderator_applications_state', query=query, json=json, data=data, files=files, raw=raw)

    def get_moderator_applications_mine(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /moderator-applications/mine. See the API reference for scopes and payloads."""
        return self.call('get_moderator_applications_mine', query=query, json=json, data=data, files=files, raw=raw)

    def post_moderator_applications(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /moderator-applications. See the API reference for scopes and payloads."""
        return self.call('post_moderator_applications', query=query, json=json, data=data, files=files, raw=raw)

    def get_health(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /health. See the API reference for scopes and payloads."""
        return self.call('get_health', query=query, json=json, data=data, files=files, raw=raw)

    def get_stats(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /stats. See the API reference for scopes and payloads."""
        return self.call('get_stats', query=query, json=json, data=data, files=files, raw=raw)

    def get_stats_random_usernames(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /stats/random-usernames. See the API reference for scopes and payloads."""
        return self.call('get_stats_random_usernames', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_tos_current(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/tos/current. See the API reference for scopes and payloads."""
        return self.call('get_api_tos_current', query=query, json=json, data=data, files=files, raw=raw)

    def get_chat_dl(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /chat/dl. See the API reference for scopes and payloads."""
        return self.call('get_chat_dl', query=query, json=json, data=data, files=files, raw=raw)

    def get_well_known_bonfire_jwks_json(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /.well-known/bonfire/jwks.json. See the API reference for scopes and payloads."""
        return self.call('get_well_known_bonfire_jwks_json', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_server_latest_json(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/server-latest.json. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_server_latest_json', query=query, json=json, data=data, files=files, raw=raw)

    def get_bonfire_profiles(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bonfire/profiles. See the API reference for scopes and payloads."""
        return self.call('get_bonfire_profiles', query=query, json=json, data=data, files=files, raw=raw)
