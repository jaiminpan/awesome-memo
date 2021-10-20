# ldap



dn: cn=module,cn=config
cn: module
objectclass: olcModuleList
objectclass: top
olcmoduleload: memberof
olcmodulepath: /usr/lib/ldap

dn: olcOverlay={0}memberof,olcDatabase={1}hdb,cn=config
objectClass: olcConfig
objectClass: olcMemberOf
objectClass: olcOverlayConfig
objectClass: top
olcOverlay: memberof




dn: cn=module,cn=config
cn: module
objectclass: olcModuleList
objectclass: top
olcmoduleload: refint
olcmodulepath: /usr/lib/ldap

dn: olcOverlay={1}refint,olcDatabase={1}hdb,cn=config
objectClass: olcConfig
objectClass: olcMemberOf
objectClass: olcOverlayConfig
objectClass: top
olcOverlay: refint



ldapadd -Y EXTERNAL -H ldapi:///
dn: olcOverlay=memberof,olcDatabase={2}hdb,cn=config
objectClass: olcOverlayConfig
objectClass: olcMemberOf
olcOverlay: memberof
olcMemberOfRefint: TRUE



ldapmodify -Q -Y EXTERNAL -H ldapi:///
dn: cn=module{0},cn=config
changetype: modify
add: olcModuleLoad
olcModuleLoad: memberof.la