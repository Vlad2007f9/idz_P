import pytest
import httpx
import json
from unittest.mock import AsyncMock, Mock

from structures.idz_3_1 import check_resource

@pytest.mark.asyncio
async def test_timeout():
    
    url = "https://httpbin.org/delay/1"

    mock_client = Mock(spec=httpx.AsyncClient)
    mock_client.get = AsyncMock()

    mock_client.get.side_effect = httpx.TimeoutException("Mocked timeout error")

    result = await check_resource(mock_client, "Test_Server", url)

    result is not None

    mock_client.get.assert_called_with(url)


@pytest.mark.asyncio
async def test_side_effects():

    url = "https://httpbin.org/delay/1"

    mock_client = Mock(spec=httpx.AsyncClient)
    mock_client.get = AsyncMock()

    resp_503 = Mock(spec=httpx.Response)
    resp_503.status_code = 503

    resp_200 = Mock(spec=httpx.Response)
    resp_200.status_code = 200
    resp_200.json = Mock(return_value={"status": "good"})

    mock_client.get.side_effect = [resp_503, resp_503, resp_200]

    result = await check_resource(mock_client, "Test_Server", url)
    
    assert result is not None


@pytest.mark.asyncio
async def test_corrupted():

    url = "https://httpbin.org/delay/1"

    mock_client = Mock(spec=httpx.AsyncClient)
    mock_client.get = AsyncMock()


    resp_bad = Mock(spec=httpx.Response)
    resp_bad.status_code = 200

    resp_bad.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)

    mock_client.get.return_value = resp_bad

    result = await check_resource(mock_client, "Test_Server", url)
    assert result is not None