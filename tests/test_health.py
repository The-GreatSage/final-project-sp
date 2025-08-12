def test_health(client):
    """Test the health endpoint returns 'ok'."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}