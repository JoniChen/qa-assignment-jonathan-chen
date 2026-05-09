import requests
from utils.conftest import load_config


def test_get_posts():
    config = load_config()
    url = f"{config['api']['base_url']}/posts"
    
    # Make GET request
    response = requests.get(url)
    # Verify response code
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    # Parse JSON response
    posts = response.json()
    
    # Verify it's a list
    assert isinstance(posts, list), f"Expected list, got {type(posts)}"
    
    # Verify length is 100
    assert len(posts) == 100, f"Expected 100 posts, got {len(posts)}"
    
    # Validate schema of first item
    if posts:
        first_post = posts[0]
        
        # Check required keys
        required_keys = ['userId', 'id', 'title', 'body']
        for key in required_keys:
            assert key in first_post, f"Missing key '{key}' in post"
        
        # Check types
        assert isinstance(first_post['userId'], int), f"userId should be int, got {type(first_post['userId'])}"
        assert isinstance(first_post['id'], int), f"id should be int, got {type(first_post['id'])}"
        assert isinstance(first_post['title'], str), f"title should be str, got {type(first_post['title'])}"
        assert isinstance(first_post['body'], str), f"body should be str, got {type(first_post['body'])}"
        
        # Check reasonable values
        assert first_post['userId'] > 0, "userId should be positive"
        assert first_post['id'] > 0, "id should be positive"
        assert len(first_post['title']) > 0, "title should not be empty"
        assert len(first_post['body']) > 0, "body should not be empty"


def test_get_post_by_id():
    config = load_config()
    base_url = config['api']['base_url']

    # Valid post ID should return 200
    valid_response = requests.get(f"{base_url}/posts/1")
    assert valid_response.status_code == 200, f"Expected 200 for existing post, got {valid_response.status_code}"

    post = valid_response.json()
    assert post['id'] == 1
    assert 'userId' in post
    assert 'title' in post
    assert 'body' in post

    # Non-existent post ID should return 404
    invalid_response = requests.get(f"{base_url}/posts/99999")
    assert invalid_response.status_code == 404, f"Expected 404 for non-existent post, got {invalid_response.status_code}"


def test_create_post():
    config = load_config()
    base_url = config['api']['base_url']
    payload = config['api']['create_post_payload']

    response = requests.post(f"{base_url}/posts", json=payload)
    assert response.status_code == 201, f"Expected 201 for created post, got {response.status_code}"

    created_post = response.json()

    # The API should echo the payload fields
    assert created_post['title'] == payload['title']
    assert created_post['body'] == payload['body']
    assert created_post['userId'] == payload['userId']

    # And include a generated id
    assert 'id' in created_post, "Expected generated id in response"
    assert isinstance(created_post['id'], int), "Generated id should be an integer"
    assert created_post['id'] > 0, "Generated id should be positive"


def test_update_post():
    config = load_config()
    base_url = config['api']['base_url']
    update_payload = config['api']['update_post_payload']
    
    response = requests.put(f"{base_url}/posts/1", json=update_payload)
    assert response.status_code == 200, f"Expected 200 for updated post, got {response.status_code}"
    
    updated_post = response.json()
    
    # Verify the update is reflected in response
    assert updated_post['title'] == update_payload['title']
    assert updated_post['body'] == update_payload['body']
    assert updated_post['userId'] == update_payload['userId']
    
    # Check response shape includes id
    assert 'id' in updated_post, "Expected id in updated post"
    assert isinstance(updated_post['id'], int), "id should be an integer"


def test_delete_post():
    config = load_config()
    base_url = config['api']['base_url']
    
    response = requests.delete(f"{base_url}/posts/1")
    
    # JSONPlaceholder returns 200 for successful delete
    assert response.status_code in [200, 204], f"Expected 200 or 204 for deleted post, got {response.status_code}"
    
    # Verify response shape
    deleted_post = response.json()
    
    # The response should still have the post structure or be empty
    if deleted_post:
        assert 'id' in deleted_post or isinstance(deleted_post, dict), "Response should be a valid JSON object"
