def test_health(client):
    # Act
    response = client.get("/health")

    # Verify
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
