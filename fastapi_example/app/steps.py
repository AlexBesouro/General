# Step 1: Create User by asking for username and password
# Step 2: Store the user in the database with hashed password
# Step 3: Create Login endpoint to authenticate user and return JWT token (oauth2.create_access_token(data={"user_id": str(user.id)}))
#         To create JWT token: we use user ID (in my case UUID) as payload data in the token
#         Token will be in str format
# Step 4: Create a dependency that will be used in protected routes to get the current user from the token
#         (get_current_user(token: str = Depends(oauth2_scheme))) - this function will decode the token and return user id from payload
#         Deepends(oauth2_scheme) - will extract the token from the request of protected route
#         Inside get_current_user we call verify_access_token to decode the token and get user id from payload to verify if id is equal to #         any existing user id in the database. verify_access_token(token, credential_exeptions) will return an object of TokenData schema  #         with id attribute if token is valid else it will raise HTTPException
# Step 5: Use get_current_user as a dependency in protected routes to get the current user based on the token provided inside header of the #         request
# Note: OAuth2PasswordBearer is used to extract token from the request header, it expects the token to be sent in the "Authorization" header with the "Bearer" scheme.
