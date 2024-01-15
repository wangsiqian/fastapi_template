from httpx import AsyncClient


async def test_list_examples(client: AsyncClient):
    response = await client.get('/v1/examples/')
    assert response.status_code == 200

    json_result = response.json()
    assert len(json_result['data']) == 0

    # 创建
    response = await client.post(
        '/v1/examples/', json={
            'first_name': 'test',
            'last_name': 'test'
        }
    )
    assert response.status_code == 200

    response = await client.post(
        '/v1/examples/', json={
            'first_name': 'test2',
            'last_name': 'test2'
        }
    )
    assert response.status_code == 200

    response = await client.get('/v1/examples/')
    assert response.status_code == 200

    json_result = response.json()
    assert len(json_result['data']) == 2
