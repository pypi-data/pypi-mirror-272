import os
import subprocess
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from gitignore_parser import parse_gitignore  # type: ignore
from httpx import AsyncClient
from rapidfuzz import process

from exponent.core.remote_execution.kernel import Kernel
from exponent.core.remote_execution.types import (
    CodeExecutionRequest,
    CodeExecutionResponse,
    CreateChatResponse,
    GetFileContentsRequest,
    GetFileContentsResponse,
    GetMatchingFilesRequest,
    GetMatchingFilesResponse,
    ListFilesRequest,
    ListFilesResponse,
    RemoteExecutionRequest,
    RemoteExecutionRequestData,
    RemoteExecutionResponse,
    StartChatRequest,
    StartChatResponse,
)


class RemoteExecutionClientSession:
    def __init__(self, api_client: AsyncClient, kernel: Kernel):
        self.api_client = api_client
        self.kernel = kernel


class RemoteExecutionClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        working_directory: str,
        session: RemoteExecutionClientSession,
    ):
        self.headers = {"API-KEY": api_key}
        self.base_url = base_url
        self.working_directory = working_directory
        self.api_client = session.api_client
        self.kernel = session.kernel

    async def get_execution_requests(
        self, chat_uuid: str
    ) -> list[RemoteExecutionRequest[Any]]:
        response = await self.api_client.get(
            f"{self.base_url}/api/remote_execution/{chat_uuid}/requests",
            headers=self.headers,
        )
        return [
            RemoteExecutionRequestData.deserialize_raw(result)
            for result in response.json()
        ]

    async def post_execution_result(
        self, chat_uuid: str, execution_response: RemoteExecutionResponse
    ) -> None:
        await self.api_client.post(
            f"{self.base_url}/api/remote_execution/{chat_uuid}/result",
            headers=self.headers,
            content=execution_response.serialize(),
        )

    async def create_chat(self) -> CreateChatResponse:
        response = await self.api_client.post(
            f"{self.base_url}/api/remote_execution/create_chat",
            headers=self.headers,
        )
        return CreateChatResponse(**response.json())

    async def start_chat(self, chat_uuid: str, prompt: str) -> StartChatResponse:
        response = await self.api_client.post(
            f"{self.base_url}/api/remote_execution/create_chat",
            headers=self.headers,
            json=StartChatRequest(chat_uuid=chat_uuid, prompt=prompt).model_dump(),
        )
        return StartChatResponse(**response.json())

    def handle_request(
        self, request: RemoteExecutionRequest[Any]
    ) -> RemoteExecutionResponse:
        if isinstance(request, CodeExecutionRequest):
            return self.execute_code(request)
        elif isinstance(request, ListFilesRequest):
            return self.list_files(request)
        else:
            raise ValueError(f"Unknown request type: {request.message_type()}")

    def execute_code(
        self, code_execution_request: CodeExecutionRequest
    ) -> CodeExecutionResponse:
        try:
            if code_execution_request.language == "python":
                return CodeExecutionResponse(
                    content=self.kernel.execute_code(code_execution_request.content),
                    correlation_id=code_execution_request.correlation_id,
                )
            elif code_execution_request.language == "shell":
                try:
                    shell_output = subprocess.check_output(
                        code_execution_request.content,
                        shell=True,
                        stderr=subprocess.STDOUT,
                        text=True,
                    )
                except subprocess.CalledProcessError as e:
                    shell_output = e.output

                code_execution_result = CodeExecutionResponse(
                    content=shell_output,
                    correlation_id=code_execution_request.correlation_id,
                )
                return code_execution_result
            else:
                raise ValueError(
                    f"Unsupported language: {code_execution_request.language}"
                )
        except Exception as e:
            return CodeExecutionResponse(
                content="An error occurred while executing the code: " + str(e),
                correlation_id=code_execution_request.correlation_id,
            )

    def list_files(self, list_files_request: ListFilesRequest) -> ListFilesResponse:
        filenames = os.listdir(list_files_request.directory)
        return ListFilesResponse(
            filenames=filenames,
            correlation_id=list_files_request.correlation_id,
        )

    def get_file_contents(
        self, get_file_contents_request: GetFileContentsRequest
    ) -> GetFileContentsResponse:
        file_path = os.path.join(
            self.working_directory, get_file_contents_request.file_path
        )
        with open(file_path) as f:
            return GetFileContentsResponse(
                content=f.read(),
                file_path=get_file_contents_request.file_path,
                correlation_id=get_file_contents_request.correlation_id,
            )

    def get_matching_files(
        self, search_term: GetMatchingFilesRequest
    ) -> GetMatchingFilesResponse:
        MAX_MATCHING_FILES = 10

        # Read .gitignore file if it exists
        gitignore_path = os.path.join(self.working_directory, ".gitignore")
        gitignore = (
            parse_gitignore(gitignore_path) if os.path.exists(gitignore_path) else None
        )

        # Find all files in the working directory and subdirectories
        all_files = []
        for root, _, files in os.walk(self.working_directory):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.working_directory)

                # Ignore files that are in .gitignore
                if gitignore and gitignore(file_path):
                    continue

                all_files.append(relative_path)

        # Use rapidfuzz to find the best matching files
        matching_files = process.extract(
            search_term.search_term,
            all_files,
            limit=MAX_MATCHING_FILES,
            score_cutoff=80,
        )

        file_paths: list[str] = [file for file, _, _ in matching_files]

        return GetMatchingFilesResponse(
            file_paths=file_paths, correlation_id=search_term.correlation_id
        )

    @staticmethod
    @asynccontextmanager
    async def session(
        api_key: str, base_url: str, working_directory: str
    ) -> AsyncGenerator["RemoteExecutionClient", None]:
        session = RemoteExecutionClientSession(AsyncClient(), Kernel())
        try:
            yield RemoteExecutionClient(api_key, base_url, working_directory, session)
        except Exception as e:
            await session.api_client.aclose()
            session.kernel.close()
            raise e
