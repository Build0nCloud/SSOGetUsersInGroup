import json
import boto3

print('Loading function')
client = boto3.client('identitystore')
myIdentityStore = 'd-906791034d'
print(boto3.__version__)


def lambda_handler(event, context):
    myUserDict=dict()
    returnDict=dict()
    rList=list()
    print("Received event: " + json.dumps(event, indent=2))
    
#    myQueryString = "Administrators"
    queryStrings = event["queryStringParameters"]
    myQueryString = queryStrings["q"]
    
#-----------------------------------    
# Get GroupID from group Display name    
#-----------------------------------

    response = client.list_groups(
    IdentityStoreId= myIdentityStore,
    Filters=[
        {
            'AttributePath': 'DisplayName',
            'AttributeValue': myQueryString
        },
    ]
    )
    print(response)
    if len(response["Groups"]) == 0 :
        print("ERRORERRORERROR")
        RESTresponse = {
        "statusCode": 502,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "body": "Group is empty or does not exist",
        "isBase64Encoded": False
        }
        
        return RESTresponse
    r1 = response["Groups"][0]
    myGroupId = r1["GroupId"]
    
#---------------------------------------------
# Get Members of Group
#---------------------------------------------

    response = client.list_group_memberships(
        IdentityStoreId= myIdentityStore, 
        GroupId= myGroupId
    )
#---------------------------------------------
# Get email value for user and return
#---------------------------------------------
    myList = response["GroupMemberships"]
#    index=int(0)
    for i in myList:

        response = client.describe_user(
            IdentityStoreId=myIdentityStore,
            UserId=i["MemberId"]["UserId"]
        )
        
#Get Primary Email Value
        myEmail = response["Emails"]
        for x in myEmail:
            if str(x["Primary"]) == "True" :
                primaryEmail = x["Value"]
        
        
# Create response
        myUserDict = {
            "UserName" : response["UserName"],
            "DisplayName" : response["DisplayName"],
            "Email" : primaryEmail
        }
        rList.append(myUserDict)

        
#
    returnDict = {
            "Users" : rList
    }
    returnBody = json.dumps(returnDict)
    
    RESTresponse = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "body": returnBody,
        "isBase64Encoded": False
    }
        
    return RESTresponse
    #raise Exception('Something went wrong')