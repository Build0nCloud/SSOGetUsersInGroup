#SSOGetUsersInGroup


This lambda function is designed to return the users in an SSO group.  Currently, some products cannot get the group memebership from the SAML assertion, so this function can be used to map the user->group relationships, allowing for complete authorization.

This function is designed to be used in conjunction with API gateway with a GET method.  It expects the query string to be &q=<group name>.

This is the DisplayName in SSO of the group, not the Group ID.

It will return a JSON of the members of that group in the following format:

{
     "Users" : [
   			{
				UserName:  <SSO Identity Store User Name>,
				DisplayName: <SSO Identity Store Display Name>,
				Email: <Primary Email>
			},
		...
		],
    "Count"  : <The total number of users in the group>
}
The function returns a 502 error if the group provided is invalid
