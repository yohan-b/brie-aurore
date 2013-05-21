from tg import session
from tg.controllers import redirect
from tg.decorators import expose, validate
from brie.lib.base import BaseController

from brie.config import ldap_config
from brie.config import groups_enum
from brie.lib.ldap_helper import *
from brie.lib.aurore_helper import *
from brie.model.ldap import *

from brie.controllers import auth
from brie.controllers.auth import AuthenticatedBaseController, AuthenticatedRestController

class MembersController(AuthenticatedBaseController):
	require_group = groups_enum.admin

	add = None

	def __init__(self):
		self.add = MembersAddController()

	def sort_name(self, name_items):
		return sorted(name_items, key=lambda t:t[0].cn.first())        
	
	@expose("brie.templates.members.index")
	def index(self, residence_name):
		members = list();

		residence_dn = Residences.get_dn_by_name(self.user, residence_name)
		if residence_dn is None:
			raise Exception("unknown residence")
		#end if

		for member in Member.get_all(self.user, residence_dn):
			members.append(member);

		rooms = Room.get_rooms(self.user, residence_dn)
		if rooms is None:
			raise Exception("unable to retrieve rooms")
		#end if
		rooms = sorted(rooms, key=lambda t:t.cn.first())

		for m in members:
			for r in rooms:
				if r.has("x-memberIn"):
					if r.get("x-memberIn").first() == m.dn:
						m.room = r


		return {
			"members" : members, 
			"residence" : residence_name
		}
	#end def


class MembersAddController(AuthenticatedRestController):
	require_group = groups_enum.admin

	""" Fonction de gestion de requete post sur le controller d'ajout """
	@expose()
	def post(self, residence, prenom, nom, mail):

		member_uid = prenom.lower() + "." + nom.lower()
		member = Member.entry_attr(member_uid, prenom, nom, mail, 1)

		residence_dn = Residences.get_dn_by_name(self.user, residence)

		member_dn = "uid=" + member_uid + "," + ldap_config.username_base_dn + residence_dn
		self.user.ldap_bind.add_entry(member_dn, member)
		

		#preview = member, room
		#index_result["preview"] = preview

		redirect("/edit/member/" + residence + "/" + member_uid)
	#end def
#end class
