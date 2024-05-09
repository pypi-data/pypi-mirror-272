import json
import os
from typing import Optional, Callable

from ceotr_git_manager import GitUser, GitRepoGitlab
from ceotr_git_manager.GitRepo import logger


class MetaFileDownloader:
    """Class to handle the downloading of metadata files from a GitLab repository."""
    def __init__(self, username: str, access_token: str, repo_path: str = 'ceotr-public/meta_json_files',
                 branch: str = 'master'):
        """Initialize with user credentials and target repository details."""
        self.user = GitUser(username=username, access_token=access_token)
        self.repo = GitRepoGitlab(git_user=self.user, repo_path=repo_path, branch=branch)
        logger.info("Initialized GitLabFileDownloader for repository %s on branch %s", repo_path, branch)

    def download_file_by_relative_path(self, relative_path: str, output_dir: str,
                                       progress_callback: Optional[Callable[[int, int], None]] = None) -> None:
        """Download a file from GitLab repository by its relative path."""
        try:
            file_contents = self.repo.get_file_contents(relative_path)
            output_path = os.path.join(output_dir, relative_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            write_mode = 'w' if isinstance(file_contents, str) else 'wb'
            content_to_write = file_contents

            if relative_path.endswith('.json') and isinstance(file_contents, bytes):
                data = json.loads(file_contents.decode('utf-8'))
                content_to_write = json.dumps(data, indent=4).encode('utf-8')  # json beautifier

            with open(output_path, write_mode) as file:
                file.write(content_to_write)
                logger.info(f"Successfully saved {output_path}")

            if progress_callback:
                progress_callback(1, 1)
        except OSError as os_error:
            logger.error(f"File operation failed for {relative_path}: {os_error}")
            raise
        except Exception as e:
            logger.error(f"Failed to download {relative_path}: {e}")
            raise


def progress_update(current, total):
    """Prints the current progress of file downloads."""
    print(f"Download progress: {current}/{total} files")
