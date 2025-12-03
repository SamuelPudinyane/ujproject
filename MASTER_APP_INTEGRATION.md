# Master Application Integration Guide

## Overview
This social media application is designed as a sub-application that integrates with a master authentication system. Users authenticate through the master application and are then granted access to this sub-application.

## Integration Methods

### 1. Setting User Session

When a user from the master application accesses this sub-app, call the session endpoint:

```python
# Master App Python Example
import requests

def set_user_session_in_subapp(user_data, subapp_url):
    endpoint = f"{subapp_url}/set_user_session"
    
    payload = {
        "user_id": user_data["id"],
        "email": user_data["email"],
        "first_name": user_data["first_name"],
        "last_name": user_data["last_name"],
        "occupation": user_data.get("occupation", ""),
        "bio": user_data.get("bio", "")
    }
    
    response = requests.post(endpoint, json=payload)
    return response.json()

# Usage
user_data = {
    "id": 123,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
}

result = set_user_session_in_subapp(user_data, "http://localhost:9000")
```

### 2. JavaScript Integration

```javascript
// Master App JavaScript Example
async function setUserSessionInSubApp(userData, subappUrl) {
    const endpoint = `${subappUrl}/set_user_session`;
    
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userData.id,
                email: userData.email,
                first_name: userData.firstName,
                last_name: userData.lastName,
                occupation: userData.occupation || '',
                bio: userData.bio || ''
            })
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error setting user session:', error);
        return { error: 'Failed to set user session' };
    }
}

// Usage
const userData = {
    id: 123,
    email: 'user@example.com',
    firstName: 'John',
    lastName: 'Doe'
};

setUserSessionInSubApp(userData, 'http://localhost:9000')
    .then(result => {
        if (result.success) {
            // Redirect user to sub-app
            window.location.href = 'http://localhost:9000/post';
        }
    });
```

## API Endpoints

### POST /set_user_session
Set user session data from master application.

**Request Body:**
```json
{
    "user_id": 123,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "occupation": "Developer",
    "bio": "Software Developer"
}
```

**Response:**
```json
{
    "success": true,
    "message": "User session set successfully"
}
```

### GET /clear_session
Clear user session when user logs out from master application.

**Response:**
```json
{
    "success": true,
    "message": "Session cleared"
}
```

### GET /api/app_info
Get sub-application information.

**Response:**
```json
{
    "app_name": "Social Media Sub-Application",
    "version": "1.0.0",
    "status": "active",
    "features": [...],
    "endpoints": {...}
}
```

### GET /api/health
Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-10-28T...",
    "session_active": true
}
```

## Integration Flow

1. **User Authentication**: User logs into master application
2. **Session Setup**: Master app calls `/set_user_session` with user data
3. **Redirect**: Master app redirects user to sub-app (`/post` route)
4. **Sub-app Access**: User can now use all sub-app features
5. **Logout**: Master app calls `/clear_session` when user logs out

## Default Behavior

If no user session is set by the master application:
- Sub-app creates a default guest user session
- User ID defaults to 1
- Email defaults to "guest@example.com"
- User can still access all features with limited profile information

## Security Considerations

1. **Shared Secret**: Consider implementing a shared secret key between master and sub-app
2. **Session Validation**: Implement session validation tokens
3. **HTTPS**: Use HTTPS for all communication between applications
4. **CORS**: Configure proper CORS settings if needed

## Error Handling

The sub-application gracefully handles missing user sessions by creating default user data, ensuring the application remains functional even if the master application integration fails.

## Testing Integration

Use the health check endpoint to verify the sub-application is running:

```bash
curl http://localhost:9000/api/health
```

Test session setting:

```bash
curl -X POST http://localhost:9000/set_user_session \
  -H "Content-Type: application/json" \
  -d '{"user_id": 123, "email": "test@example.com", "first_name": "Test", "last_name": "User"}'
```