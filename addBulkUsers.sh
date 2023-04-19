#! /bin/sh

a=0

while [ $a -lt 300 ]
do
	myUserName="user"$a
	myEmailsValue="Value="$myUserName"@gmail.com,Type=work,Primary=true"
	echo $myUserName
	echo $myEmailsValue
	a=`expr $a + 1`
	aws identitystore create-user --identity-store-id d-906791034d --user-name $myUserName --display-name $myUserName --name "Formatted=string,FamilyName=robot,GivenName=mister,MiddleName=a,HonorificPrefix=none,HonorificSuffix=none" --emails $myEmailsValue
done

