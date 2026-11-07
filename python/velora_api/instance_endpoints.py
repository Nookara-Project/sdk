"""Generated instance REST methods; payloads follow Bonfire PROTOCOL."""
class InstanceEndpoints:

    def get_bot_discovery(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/discovery."""
        return self.call('get_bot_discovery', query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_gateway_bot(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/gateway/bot."""
        return self.call('get_bot_v1_gateway_bot', query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_users_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/users/@me."""
        return self.call('get_bot_v1_users_me', query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_oauth2_applications_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/oauth2/applications/@me."""
        return self.call('get_bot_v1_oauth2_applications_me', query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_users_me_guilds(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/users/@me/guilds."""
        return self.call('get_bot_v1_users_me_guilds', query=query, json=json, data=data, files=files, raw=raw)

    def delete_bot_v1_users_me_guilds_by_gid(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /bot/v1/users/@me/guilds/:gid."""
        return self.call('delete_bot_v1_users_me_guilds_by_gid', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def post_bot_v1_users_me_channels(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /bot/v1/users/@me/channels."""
        return self.call('post_bot_v1_users_me_channels', query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_users_by_uid(self, *, uid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/users/:uid."""
        return self.call('get_bot_v1_users_by_uid', uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_guilds_by_gid(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/guilds/:gid."""
        return self.call('get_bot_v1_guilds_by_gid', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_guilds_by_gid_roles(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/guilds/:gid/roles."""
        return self.call('get_bot_v1_guilds_by_gid_roles', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_guilds_by_gid_channels(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/guilds/:gid/channels."""
        return self.call('get_bot_v1_guilds_by_gid_channels', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_guilds_by_gid_members_by_uid(self, *, gid, uid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/guilds/:gid/members/:uid."""
        return self.call('get_bot_v1_guilds_by_gid_members_by_uid', gid=gid, uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_guilds_by_gid_members(self, *, gid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/guilds/:gid/members."""
        return self.call('get_bot_v1_guilds_by_gid_members', gid=gid, query=query, json=json, data=data, files=files, raw=raw)

    def put_bot_v1_guilds_by_gid_members_by_uid_roles_by_rid(self, *, gid, uid, rid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /bot/v1/guilds/:gid/members/:uid/roles/:rid."""
        return self.call('put_bot_v1_guilds_by_gid_members_by_uid_roles_by_rid', gid=gid, uid=uid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_bot_v1_guilds_by_gid_members_by_uid_roles_by_rid(self, *, gid, uid, rid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /bot/v1/guilds/:gid/members/:uid/roles/:rid."""
        return self.call('delete_bot_v1_guilds_by_gid_members_by_uid_roles_by_rid', gid=gid, uid=uid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_channels_by_cid(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/channels/:cid."""
        return self.call('get_bot_v1_channels_by_cid', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_bot_v1_channels_by_cid_typing(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /bot/v1/channels/:cid/typing."""
        return self.call('post_bot_v1_channels_by_cid_typing', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_channels_by_cid_messages(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/channels/:cid/messages."""
        return self.call('get_bot_v1_channels_by_cid_messages', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_channels_by_cid_messages_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/channels/:cid/messages/:mid."""
        return self.call('get_bot_v1_channels_by_cid_messages_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def post_bot_v1_channels_by_cid_messages(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /bot/v1/channels/:cid/messages."""
        return self.call('post_bot_v1_channels_by_cid_messages', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_bot_v1_channels_by_cid_messages_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /bot/v1/channels/:cid/messages/:mid."""
        return self.call('patch_bot_v1_channels_by_cid_messages_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_bot_v1_channels_by_cid_messages_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /bot/v1/channels/:cid/messages/:mid."""
        return self.call('delete_bot_v1_channels_by_cid_messages_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def put_bot_v1_channels_by_cid_messages_by_mid_reactions_by_emoji_me(self, *, cid, mid, emoji, query=None, json=None, data=None, files=None, raw=False):
        """PUT /bot/v1/channels/:cid/messages/:mid/reactions/:emoji/@me."""
        return self.call('put_bot_v1_channels_by_cid_messages_by_mid_reactions_by_emoji_me', cid=cid, mid=mid, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def delete_bot_v1_channels_by_cid_messages_by_mid_reactions_by_emoji_me(self, *, cid, mid, emoji, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /bot/v1/channels/:cid/messages/:mid/reactions/:emoji/@me."""
        return self.call('delete_bot_v1_channels_by_cid_messages_by_mid_reactions_by_emoji_me', cid=cid, mid=mid, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def put_bot_v1_channels_by_cid_pins_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /bot/v1/channels/:cid/pins/:mid."""
        return self.call('put_bot_v1_channels_by_cid_pins_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_bot_v1_channels_by_cid_pins_by_mid(self, *, cid, mid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /bot/v1/channels/:cid/pins/:mid."""
        return self.call('delete_bot_v1_channels_by_cid_pins_by_mid', cid=cid, mid=mid, query=query, json=json, data=data, files=files, raw=raw)

    def get_bot_v1_gateway(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /bot/v1/gateway."""
        return self.call('get_bot_v1_gateway', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_invite_by_code(self, *, code, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/invite/:code."""
        return self.call('get_api_v1_invite_by_code', code=code, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_identities(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/identities."""
        return self.call('get_api_v1_identities', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/settings."""
        return self.call('get_api_v1_settings', query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/settings."""
        return self.call('patch_api_v1_settings', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_notify(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/notify."""
        return self.call('get_api_v1_notify', query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_notify_by_target(self, *, target, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/notify/:target."""
        return self.call('put_api_v1_notify_by_target', target=target, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers."""
        return self.call('get_api_v1_servers', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_discover(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/discover."""
        return self.call('get_api_v1_discover', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers."""
        return self.call('post_api_v1_servers', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers/:sid."""
        return self.call('get_api_v1_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/servers/:sid."""
        return self.call('patch_api_v1_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_servers_by_sid_layout(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/servers/:sid/layout."""
        return self.call('put_api_v1_servers_by_sid_layout', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid."""
        return self.call('delete_api_v1_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_join(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/join."""
        return self.call('post_api_v1_servers_by_sid_join', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_join_by_code(self, *, code, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/join/:code."""
        return self.call('post_api_v1_join_by_code', code=code, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_leave(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/leave."""
        return self.call('post_api_v1_servers_by_sid_leave', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_icon(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/icon."""
        return self.call('post_api_v1_servers_by_sid_icon', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_banner(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/banner."""
        return self.call('post_api_v1_servers_by_sid_banner', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid_icon(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid/icon."""
        return self.call('delete_api_v1_servers_by_sid_icon', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid_banner(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid/banner."""
        return self.call('delete_api_v1_servers_by_sid_banner', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers_by_sid_members(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers/:sid/members."""
        return self.call('get_api_v1_servers_by_sid_members', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid_members_by_uid(self, *, sid, uid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid/members/:uid."""
        return self.call('delete_api_v1_servers_by_sid_members_by_uid', sid=sid, uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers_by_sid_bans(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers/:sid/bans."""
        return self.call('get_api_v1_servers_by_sid_bans', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid_bans_by_uid(self, *, sid, uid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid/bans/:uid."""
        return self.call('delete_api_v1_servers_by_sid_bans_by_uid', sid=sid, uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers_by_sid_requests(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers/:sid/requests."""
        return self.call('get_api_v1_servers_by_sid_requests', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_requests_by_uid_accept(self, *, sid, uid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/requests/:uid/accept."""
        return self.call('post_api_v1_servers_by_sid_requests_by_uid_accept', sid=sid, uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_requests_by_uid_deny(self, *, sid, uid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/requests/:uid/deny."""
        return self.call('post_api_v1_servers_by_sid_requests_by_uid_deny', sid=sid, uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers_by_sid_invites(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers/:sid/invites."""
        return self.call('get_api_v1_servers_by_sid_invites', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_invites(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/invites."""
        return self.call('post_api_v1_servers_by_sid_invites', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_invites_by_code(self, *, code, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/invites/:code."""
        return self.call('delete_api_v1_invites_by_code', code=code, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_roles(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/roles."""
        return self.call('post_api_v1_servers_by_sid_roles', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_servers_by_sid_roles_order(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/servers/:sid/roles/order."""
        return self.call('put_api_v1_servers_by_sid_roles_order', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_servers_by_sid_roles_by_rid(self, *, sid, rid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/servers/:sid/roles/:rid."""
        return self.call('patch_api_v1_servers_by_sid_roles_by_rid', sid=sid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid_roles_by_rid(self, *, sid, rid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid/roles/:rid."""
        return self.call('delete_api_v1_servers_by_sid_roles_by_rid', sid=sid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_servers_by_sid_members_by_uid_roles_by_rid(self, *, sid, uid, rid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/servers/:sid/members/:uid/roles/:rid."""
        return self.call('put_api_v1_servers_by_sid_members_by_uid_roles_by_rid', sid=sid, uid=uid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid_members_by_uid_roles_by_rid(self, *, sid, uid, rid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid/members/:uid/roles/:rid."""
        return self.call('delete_api_v1_servers_by_sid_members_by_uid_roles_by_rid', sid=sid, uid=uid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_roles_by_rid_icon(self, *, sid, rid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/roles/:rid/icon."""
        return self.call('post_api_v1_servers_by_sid_roles_by_rid_icon', sid=sid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid_roles_by_rid_icon(self, *, sid, rid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid/roles/:rid/icon."""
        return self.call('delete_api_v1_servers_by_sid_roles_by_rid_icon', sid=sid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_channels(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/channels."""
        return self.call('post_api_v1_servers_by_sid_channels', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_channels_by_cid(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/channels/:cid."""
        return self.call('patch_api_v1_channels_by_cid', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_channels_by_cid(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/channels/:cid."""
        return self.call('delete_api_v1_channels_by_cid', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_channels_by_cid_perms(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/channels/:cid/perms."""
        return self.call('put_api_v1_channels_by_cid_perms', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_channels_by_cid_icon(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/channels/:cid/icon."""
        return self.call('post_api_v1_channels_by_cid_icon', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_emojis(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/emojis."""
        return self.call('get_api_v1_emojis', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers_by_sid_emojis(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers/:sid/emojis."""
        return self.call('get_api_v1_servers_by_sid_emojis', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_emojis(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/emojis."""
        return self.call('post_api_v1_servers_by_sid_emojis', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_servers_by_sid_emojis_by_eid(self, *, sid, eid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/servers/:sid/emojis/:eid."""
        return self.call('patch_api_v1_servers_by_sid_emojis_by_eid', sid=sid, eid=eid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid_emojis_by_eid(self, *, sid, eid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid/emojis/:eid."""
        return self.call('delete_api_v1_servers_by_sid_emojis_by_eid', sid=sid, eid=eid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_emojis_by_eid_info(self, *, eid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/emojis/:eid/info."""
        return self.call('get_api_v1_emojis_by_eid_info', eid=eid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_channels_by_cid_shop(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/channels/:cid/shop."""
        return self.call('get_api_v1_channels_by_cid_shop', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_channels_by_cid_shop_by_rid(self, *, cid, rid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/channels/:cid/shop/:rid."""
        return self.call('post_api_v1_channels_by_cid_shop_by_rid', cid=cid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_channels_by_cid_shop_by_rid_status(self, *, cid, rid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/channels/:cid/shop/:rid/status."""
        return self.call('get_api_v1_channels_by_cid_shop_by_rid_status', cid=cid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_channels_by_cid_shop_by_rid(self, *, cid, rid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/channels/:cid/shop/:rid."""
        return self.call('delete_api_v1_channels_by_cid_shop_by_rid', cid=cid, rid=rid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_channels_by_cid_starboard(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/channels/:cid/starboard."""
        return self.call('get_api_v1_channels_by_cid_starboard', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_channels_by_cid_webhooks(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/channels/:cid/webhooks."""
        return self.call('get_api_v1_channels_by_cid_webhooks', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_channels_by_cid_webhooks(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/channels/:cid/webhooks."""
        return self.call('post_api_v1_channels_by_cid_webhooks', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_hooks_by_wid(self, *, wid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/hooks/:wid."""
        return self.call('patch_api_v1_hooks_by_wid', wid=wid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_hooks_by_wid(self, *, wid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/hooks/:wid."""
        return self.call('delete_api_v1_hooks_by_wid', wid=wid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_hooks_by_wid_avatar(self, *, wid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/hooks/:wid/avatar."""
        return self.call('post_api_v1_hooks_by_wid_avatar', wid=wid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_sounds(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/sounds."""
        return self.call('get_api_v1_sounds', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers_by_sid_sounds(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers/:sid/sounds."""
        return self.call('get_api_v1_servers_by_sid_sounds', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_servers_by_sid_sounds(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/servers/:sid/sounds."""
        return self.call('post_api_v1_servers_by_sid_sounds', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_servers_by_sid_sounds_by_id(self, *, sid, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/servers/:sid/sounds/:id."""
        return self.call('patch_api_v1_servers_by_sid_sounds_by_id', sid=sid, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_servers_by_sid_sounds_by_id(self, *, sid, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/servers/:sid/sounds/:id."""
        return self.call('delete_api_v1_servers_by_sid_sounds_by_id', sid=sid, id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_unfurl(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/unfurl."""
        return self.call('get_api_v1_unfurl', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_bots(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/bots."""
        return self.call('get_api_v1_bots', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_bots(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/bots."""
        return self.call('post_api_v1_bots', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_bots_gallery_add(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/bots/gallery/add."""
        return self.call('post_api_v1_bots_gallery_add', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_bots_by_name_by_username(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/bots/by-name/:username."""
        return self.call('get_api_v1_bots_by_name_by_username', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_bots_by_name_by_username_add(self, *, username, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/bots/by-name/:username/add."""
        return self.call('post_api_v1_bots_by_name_by_username_add', username=username, query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_bots_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/bots/:id."""
        return self.call('patch_api_v1_bots_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_bots_by_id_avatar(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/bots/:id/avatar."""
        return self.call('post_api_v1_bots_by_id_avatar', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_bots_by_id_token(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/bots/:id/token."""
        return self.call('post_api_v1_bots_by_id_token', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_bots_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/bots/:id."""
        return self.call('delete_api_v1_bots_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_yt_stream_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/yt/stream/:id."""
        return self.call('get_api_v1_yt_stream_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_yt_by_id_prepare(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/yt/:id/prepare."""
        return self.call('post_api_v1_yt_by_id_prepare', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_yt_by_id_status(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/yt/:id/status."""
        return self.call('get_api_v1_yt_by_id_status', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_yt_by_id_save(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/yt/:id/save."""
        return self.call('post_api_v1_yt_by_id_save', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_webhooks_by_wid_by_token(self, *, wid, token, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/webhooks/:wid/:token."""
        return self.call('get_api_v1_webhooks_by_wid_by_token', wid=wid, token=token, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_webhooks_by_wid_by_token(self, *, wid, token, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/webhooks/:wid/:token."""
        return self.call('post_api_v1_webhooks_by_wid_by_token', wid=wid, token=token, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_webhooks_by_wid_by_token(self, *, wid, token, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/webhooks/:wid/:token."""
        return self.call('delete_api_v1_webhooks_by_wid_by_token', wid=wid, token=token, query=query, json=json, data=data, files=files, raw=raw)

    def get_well_known_bonfire(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /.well-known/bonfire."""
        return self.call('get_well_known_bonfire', query=query, json=json, data=data, files=files, raw=raw)

    def get_health(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /health."""
        return self.call('get_health', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_instance_info(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/instance/info."""
        return self.call('get_api_v1_instance_info', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_auth_velora(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/auth/velora."""
        return self.call('post_api_v1_auth_velora', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_auth_register(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/auth/register."""
        return self.call('post_api_v1_auth_register', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_auth_login(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/auth/login."""
        return self.call('post_api_v1_auth_login', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_auth_logout(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/auth/logout."""
        return self.call('post_api_v1_auth_logout', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_me(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/me."""
        return self.call('get_api_v1_me', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_instance_claim(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/instance/claim."""
        return self.call('post_api_v1_instance_claim', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_instance_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/instance/settings."""
        return self.call('get_api_v1_instance_settings', query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_instance_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/instance/settings."""
        return self.call('patch_api_v1_instance_settings', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_instance_velora_register(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/instance/velora/register."""
        return self.call('post_api_v1_instance_velora_register', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_instance_owner_attestation(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/instance/owner-attestation."""
        return self.call('get_api_v1_instance_owner_attestation', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_import_velora(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/import/velora."""
        return self.call('post_api_v1_import_velora', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_instance_restart(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/instance/restart."""
        return self.call('post_api_v1_instance_restart', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_instance_admins(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/instance/admins."""
        return self.call('get_api_v1_instance_admins', query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_instance_admins_by_uid(self, *, uid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/instance/admins/:uid."""
        return self.call('put_api_v1_instance_admins_by_uid', uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_instance_admins_by_uid(self, *, uid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/instance/admins/:uid."""
        return self.call('delete_api_v1_instance_admins_by_uid', uid=uid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_channels_by_cid_messages(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/channels/:cid/messages."""
        return self.call('get_api_v1_channels_by_cid_messages', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_channels_by_cid_messages(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/channels/:cid/messages."""
        return self.call('post_api_v1_channels_by_cid_messages', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_channels_by_cid_read(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/channels/:cid/read."""
        return self.call('post_api_v1_channels_by_cid_read', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_channels_by_cid_search(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/channels/:cid/search."""
        return self.call('get_api_v1_channels_by_cid_search', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers_by_sid_search(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers/:sid/search."""
        return self.call('get_api_v1_servers_by_sid_search', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_channels_by_cid_pins(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/channels/:cid/pins."""
        return self.call('get_api_v1_channels_by_cid_pins', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_messages_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/messages/:id."""
        return self.call('patch_api_v1_messages_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_messages_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/messages/:id."""
        return self.call('delete_api_v1_messages_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_messages_by_id_reactions_by_emoji(self, *, id, emoji, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/messages/:id/reactions/:emoji."""
        return self.call('put_api_v1_messages_by_id_reactions_by_emoji', id=id, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_messages_by_id_reactions_by_emoji(self, *, id, emoji, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/messages/:id/reactions/:emoji."""
        return self.call('delete_api_v1_messages_by_id_reactions_by_emoji', id=id, emoji=emoji, query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_messages_by_id_pin(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/messages/:id/pin."""
        return self.call('put_api_v1_messages_by_id_pin', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_messages_by_id_pin(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/messages/:id/pin."""
        return self.call('delete_api_v1_messages_by_id_pin', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_media_upload(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/media/upload."""
        return self.call('post_api_v1_media_upload', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_media_import(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/media/import."""
        return self.call('post_api_v1_media_import', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_servers_by_sid_export(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/servers/:sid/export."""
        return self.call('get_api_v1_servers_by_sid_export', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_import(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/import."""
        return self.call('post_api_v1_import', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_instance_backups(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/instance/backups."""
        return self.call('get_api_v1_instance_backups', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_instance_backups(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/instance/backups."""
        return self.call('post_api_v1_instance_backups', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_instance_backups_by_id_download(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/instance/backups/:id/download."""
        return self.call('get_api_v1_instance_backups_by_id_download', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_instance_backups_by_id(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/instance/backups/:id."""
        return self.call('delete_api_v1_instance_backups_by_id', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_instance_backups_by_id_restore(self, *, id, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/instance/backups/:id/restore."""
        return self.call('post_api_v1_instance_backups_by_id_restore', id=id, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_instance_restore(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/instance/restore."""
        return self.call('post_api_v1_instance_restore', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_bridge_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/bridge/settings."""
        return self.call('get_api_v1_bridge_settings', query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_bridge_settings(self, *, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/bridge/settings."""
        return self.call('patch_api_v1_bridge_settings', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_bridge_platforms(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/bridge/platforms."""
        return self.call('get_api_v1_bridge_platforms', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_bridge_by_platform_guilds(self, *, platform, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/bridge/:platform/guilds."""
        return self.call('get_api_v1_bridge_by_platform_guilds', platform=platform, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_bridge_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/bridge/servers/:sid."""
        return self.call('get_api_v1_bridge_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_bridge_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/bridge/servers/:sid."""
        return self.call('put_api_v1_bridge_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def patch_api_v1_bridge_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """PATCH /api/v1/bridge/servers/:sid."""
        return self.call('patch_api_v1_bridge_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_bridge_servers_by_sid(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/bridge/servers/:sid."""
        return self.call('delete_api_v1_bridge_servers_by_sid', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def put_api_v1_bridge_servers_by_sid_channels_by_cid(self, *, sid, cid, query=None, json=None, data=None, files=None, raw=False):
        """PUT /api/v1/bridge/servers/:sid/channels/:cid."""
        return self.call('put_api_v1_bridge_servers_by_sid_channels_by_cid', sid=sid, cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_channels_by_cid_cloudlink(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/channels/:cid/cloudlink."""
        return self.call('get_api_v1_channels_by_cid_cloudlink', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_channels_by_cid_cloudlink_reconnect(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/channels/:cid/cloudlink/reconnect."""
        return self.call('post_api_v1_channels_by_cid_cloudlink_reconnect', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_game_downloads(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/game/downloads."""
        return self.call('get_api_v1_game_downloads', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_game_servers_by_sid_instances(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/game/servers/:sid/instances."""
        return self.call('get_api_v1_game_servers_by_sid_instances', sid=sid, query=query, json=json, data=data, files=files, raw=raw)

    def delete_api_v1_game_servers_by_sid_instances_by_iid(self, *, sid, iid, query=None, json=None, data=None, files=None, raw=False):
        """DELETE /api/v1/game/servers/:sid/instances/:iid."""
        return self.call('delete_api_v1_game_servers_by_sid_instances_by_iid', sid=sid, iid=iid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_game_unclaimed(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/game/unclaimed."""
        return self.call('get_api_v1_game_unclaimed', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_game_connected(self, *, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/game/connected."""
        return self.call('get_api_v1_game_connected', query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_game_connected_by_iid_link(self, *, iid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/game/connected/:iid/link."""
        return self.call('post_api_v1_game_connected_by_iid_link', iid=iid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_game_claims(self, *, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/game/claims."""
        return self.call('post_api_v1_game_claims', query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_game_claims_by_code(self, *, code, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/game/claims/:code."""
        return self.call('get_api_v1_game_claims_by_code', code=code, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_game_channels_by_cid_status(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/game/channels/:cid/status."""
        return self.call('get_api_v1_game_channels_by_cid_status', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_game_channels_by_cid_console(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/game/channels/:cid/console."""
        return self.call('get_api_v1_game_channels_by_cid_console', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def post_api_v1_game_channels_by_cid_console(self, *, cid, query=None, json=None, data=None, files=None, raw=False):
        """POST /api/v1/game/channels/:cid/console."""
        return self.call('post_api_v1_game_channels_by_cid_console', cid=cid, query=query, json=json, data=data, files=files, raw=raw)

    def get_api_v1_game_servers_by_sid_audit(self, *, sid, query=None, json=None, data=None, files=None, raw=False):
        """GET /api/v1/game/servers/:sid/audit."""
        return self.call('get_api_v1_game_servers_by_sid_audit', sid=sid, query=query, json=json, data=data, files=files, raw=raw)
