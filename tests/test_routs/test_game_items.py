import pytest
from fastapi import status


class TestGetGameItem:

    @pytest.mark.asyncio
    async def test_get_game_items_without_authorization(
            self,
            async_client,
    ):
        """
        Tests report is returned only for the authenticated user.
        """
        response = await async_client.get('/items_manager/items/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers['WWW-Authenticate'] == 'Bearer'

    @pytest.mark.asyncio
    async def test_get_game_item_by_id_without_authorization(
            self,
            async_client,
            get_game_items,
    ):
        """
        Tests report is returned only for the authenticated user.
        """
        response = await async_client.get('/items_manager/items/1/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers['WWW-Authenticate'] == 'Bearer'

    @pytest.mark.asyncio
    async def test_get_game_items(
            self,
            async_client,
            normal_user_token_headers,
            get_game_items
    ):
        """
        Tests report is returned only for the authenticated user.
        """
        response = await async_client.get(
            url='/items_manager/items/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'}
        )
        game_item = response.json()[0]
        assert response.status_code == status.HTTP_200_OK
        assert get_game_items['name'] == game_item['name']
        assert get_game_items['description'] == game_item['description']
        assert get_game_items['quantity'] == game_item['quantity']
        assert get_game_items['price'] == game_item['price']
        assert get_game_items['category_id'] == game_item['category_id']

    @pytest.mark.asyncio
    async def test_get_game_item_by_id(
            self,
            async_client,
            normal_user_token_headers,
            get_game_items
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        response = await async_client.get(
            url='/items_manager/items/1/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'}
        )
        game_item = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert get_game_items['name'] == game_item['name']
        assert get_game_items['description'] == game_item['description']
        assert get_game_items['quantity'] == game_item['quantity']
        assert get_game_items['price'] == game_item['price']
        assert get_game_items['category_id'] == game_item['category_id']


class TestPostGameItem:

    @pytest.mark.asyncio
    async def test_create_game_item_without_authorization(
            self,
            async_client,
    ):
        """
        Tests report is returned only for the authenticated user.
        """
        response = await async_client.post('/items_manager/items/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers['WWW-Authenticate'] == 'Bearer'

    @pytest.mark.asyncio
    async def test_create_game_item(
            self,
            async_client,
            normal_user_token_headers,
            create_game_item
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        response = await async_client.post(
            url='/items_manager/items/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
            json=create_game_item
        )
        game_item = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert create_game_item['name'] == game_item['name']
        assert create_game_item['description'] == game_item['description']
        assert create_game_item['quantity'] == game_item['quantity']
        assert create_game_item['price'] == game_item['price']
        assert create_game_item['category_id'] == game_item['category_id']

    @pytest.mark.asyncio
    async def test_create_game_item_failed_name_409(
            self,
            async_client,
            normal_user_token_headers,
            create_game_item
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        await async_client.post(
            url='/items_manager/items/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
            json=create_game_item
        )
        response = await async_client.post(
            url='/items_manager/items/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
            json=create_game_item
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_create_game_item_failed_name_422(
            self,
            async_client,
            normal_user_token_headers,
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        response = await async_client.post(
            url='/items_manager/items/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestPatchGameItem:

    @pytest.mark.asyncio
    async def test_update_game_item_without_authorization(
            self,
            async_client,
            update_game_item
    ):
        """
        Tests report is returned only for the authenticated user.
        """
        response = await async_client.patch('/items_manager/items/1/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers['WWW-Authenticate'] == 'Bearer'

    @pytest.mark.asyncio
    async def test_update_game_item(
            self,
            async_client,
            normal_user_token_headers,
            update_game_item
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        response = await async_client.patch(
            url='/items_manager/items/1/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
            json=update_game_item
        )
        game_item = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert update_game_item['name'] == game_item['name']
        assert update_game_item['description'] == game_item['description']
        assert update_game_item['quantity'] == game_item['quantity']
        assert update_game_item['price'] == game_item['price']
        assert update_game_item['category_id'] == game_item['category_id']

    @pytest.mark.asyncio
    async def test_update_game_item_failed_name_404(
            self,
            async_client,
            normal_user_token_headers,
            update_game_item,
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        response = await async_client.patch(
            url='/items_manager/items/3/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
            json=update_game_item
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_update_game_item_failed_name_409(
            self,
            async_client,
            normal_user_token_headers,
            update_game_item_failed_name
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        response = await async_client.patch(
            url='/items_manager/items/1/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
            json=update_game_item_failed_name
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.asyncio
    async def test_update_game_item_failed_422(
            self,
            async_client,
            normal_user_token_headers,
            update_game_item,
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        response = await async_client.patch(
            url='/items_manager/items/1/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteGameItem:

    @pytest.mark.asyncio
    async def test_delete_game_item_without_authorization(
            self,
            async_client,
            get_game_items
    ):
        """
        Tests report is returned only for the authenticated user.
        """
        response = await async_client.delete('/items_manager/items/1/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.headers['WWW-Authenticate'] == 'Bearer'

    @pytest.mark.asyncio
    async def test_delete_game_item(
            self,
            async_client,
            normal_user_token_headers,
            get_game_items
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        response = await async_client.delete(
            url='/items_manager/items/1/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.asyncio
    async def test_delete_game_item_failed_404(
            self,
            async_client,
            normal_user_token_headers,
            create_game_item
    ):
        """
        Tests report returns correct data that equals to the predefined one.
        """
        response = await async_client.delete(
            url='/items_manager/items/3/',
            headers={'Authorization': f'Bearer {normal_user_token_headers.access_token}'},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
