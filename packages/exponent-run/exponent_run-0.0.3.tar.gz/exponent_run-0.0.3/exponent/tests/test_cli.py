from unittest import mock
from unittest.mock import mock_open

from click.testing import CliRunner

from exponent.cli import login
from exponent.core.remote_execution.client import RemoteExecutionClient
from exponent.core.remote_execution.kernel import Kernel
from exponent.core.remote_execution.types import (
    GetFileContentsRequest,
    GetFileContentsResponse,
    GetMatchingFilesRequest,
    GetMatchingFilesResponse,
    ListFilesRequest,
    ListFilesResponse,
)


async def test_exponent_login(cli_runner: CliRunner) -> None:
    with mock.patch("builtins.open", new_callable=mock_open):
        result = cli_runner.invoke(
            login, ["--key", "123456"], env={"EXPONENT_API_KEY": "123456"}
        )
        assert result.exit_code == 0
        assert "Saving API Key" in result.output


@mock.patch(
    "exponent.core.remote_execution.client.RemoteExecutionClient.get_execution_requests"
)
async def test_list_files(
    get_execution_requests: mock.Mock,
    default_temporary_directory: str,
) -> None:
    get_execution_requests.return_value = [
        ListFilesRequest(correlation_id="123456", directory=default_temporary_directory)
    ]

    async with RemoteExecutionClient.session(
        api_key="123456",
        base_url="https://example.com",
        working_directory=default_temporary_directory,
    ) as client:
        requests = await client.get_execution_requests(chat_uuid="123456")

        assert len(requests) == 1
        request = requests[0]
        assert isinstance(request, ListFilesRequest)
        assert request == ListFilesRequest(
            correlation_id="123456", directory=default_temporary_directory
        )

        response = client.list_files(request)
        assert response == ListFilesResponse(
            correlation_id="123456", filenames=["test1.py", "test2.py"]
        )


@mock.patch(
    "exponent.core.remote_execution.client.RemoteExecutionClient.get_execution_requests"
)
async def test_get_file_contents(
    get_execution_requests: mock.Mock,
    default_temporary_directory: str,
) -> None:
    get_execution_requests.return_value = [
        GetFileContentsRequest(correlation_id="123456", file_path="test1.py")
    ]

    async with RemoteExecutionClient.session(
        api_key="123456",
        base_url="https://example.com",
        working_directory=default_temporary_directory,
    ) as client:
        requests = await client.get_execution_requests(chat_uuid="123456")
        assert len(requests) == 1

        request = requests[0]
        assert isinstance(request, GetFileContentsRequest)
        assert request == GetFileContentsRequest(
            correlation_id="123456", file_path="test1.py"
        )

        response = client.get_file_contents(request)
        assert response == GetFileContentsResponse(
            correlation_id="123456",
            file_path="test1.py",
            content="print('Hello, world!')",
        )


@mock.patch(
    "exponent.core.remote_execution.client.RemoteExecutionClient.get_execution_requests"
)
async def test_get_matching_files(
    get_execution_requests: mock.Mock,
    default_temporary_directory: str,
) -> None:
    get_execution_requests.return_value = [
        GetMatchingFilesRequest(correlation_id="123456", search_term="tes"),
        GetMatchingFilesRequest(correlation_id="123456", search_term="test1"),
    ]

    async with RemoteExecutionClient.session(
        api_key="123456",
        base_url="https://example.com",
        working_directory=default_temporary_directory,
    ) as client:
        EXPECTED_REQUESTS_COUNT = 2
        requests = await client.get_execution_requests(chat_uuid="123456")
        assert len(requests) == EXPECTED_REQUESTS_COUNT

        request1 = requests[0]
        assert isinstance(request1, GetMatchingFilesRequest)
        assert request1 == GetMatchingFilesRequest(
            correlation_id="123456", search_term="tes"
        )
        response1 = client.get_matching_files(request1)
        assert response1 == GetMatchingFilesResponse(
            correlation_id="123456", file_paths=["test1.py", "test2.py"]
        )

        request2 = requests[1]
        assert isinstance(request2, GetMatchingFilesRequest)
        assert request2 == GetMatchingFilesRequest(
            correlation_id="123456", search_term="test1"
        )
        response2 = client.get_matching_files(request2)
        assert response2 == GetMatchingFilesResponse(
            correlation_id="123456", file_paths=["test1.py", "test2.py"]
        )


@mock.patch(
    "exponent.core.remote_execution.client.RemoteExecutionClient.get_execution_requests"
)
async def test_get_matching_files_nested(
    get_execution_requests: mock.Mock,
    temporary_directory: str,
) -> None:
    # Setup test directory to look like this:
    # /folder
    #   /subfolder
    #     test1.py
    #     test2.py
    # /main
    #   core.java
    # random.tsx
    # .env
    # .gitignore (contains .env ignored)

    # Test queries for:
    # .env
    # random
    # test1
    # test2
    # .tsx
    # mjava
    import os

    # Create the necessary files and folders in the temporary directory
    os.makedirs(os.path.join(temporary_directory, "folder", "subfolder"))
    os.makedirs(os.path.join(temporary_directory, "main"))

    with open(
        os.path.join(temporary_directory, "folder", "subfolder", "test1.py"),
        "w",
    ) as f:
        f.write("# test1.py")

    with open(
        os.path.join(temporary_directory, "folder", "subfolder", "test2.py"),
        "w",
    ) as f:
        f.write("# test2.py")

    with open(os.path.join(temporary_directory, "main", "core.java"), "w") as f:
        f.write("// core.java")

    with open(os.path.join(temporary_directory, "random.tsx"), "w") as f:
        f.write("// random.tsx")

    with open(os.path.join(temporary_directory, ".env"), "w") as f:
        f.write("SECRET_KEY=123456")

    with open(os.path.join(temporary_directory, ".gitignore"), "w") as f:
        f.write(".env")

    # Test queries for various search terms
    test_cases = [
        # ("tes", ["folder/subfolder/test1.py", "folder/subfolder/test2.py"]),
        ("random", ["random.tsx"]),
        (".env", []),
        ("core", ["main/core.java"]),
        (".tsx", ["random.tsx"]),
        ("java", ["main/core.java"]),
        ("nonexistent", []),
        ("folder", ["folder/subfolder/test1.py", "folder/subfolder/test2.py"]),
        ("subfolder", ["folder/subfolder/test1.py", "folder/subfolder/test2.py"]),
        ("test1", ["folder/subfolder/test1.py"]),
        ("test2", ["folder/subfolder/test2.py"]),
    ]

    async with RemoteExecutionClient.session(
        api_key="123456",
        base_url="https://example.com",
        working_directory=temporary_directory,
    ) as client:
        for search_term, expected_files in test_cases:
            get_execution_requests.return_value = [
                GetMatchingFilesRequest(
                    correlation_id="123456", search_term=search_term
                )
            ]
            requests = await client.get_execution_requests(chat_uuid="123456")
            assert len(requests) == 1

            request = requests[0]
            assert isinstance(request, GetMatchingFilesRequest)
            assert request == GetMatchingFilesRequest(
                correlation_id="123456", search_term=search_term
            )

            response = client.get_matching_files(request)
            assert response == GetMatchingFilesResponse(
                correlation_id="123456", file_paths=expected_files
            )


async def test_python_kernel() -> None:
    kernel = Kernel()
    result = kernel.execute_code("print('Hello, world!')")
    assert result == "Hello, world!\n"
