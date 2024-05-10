# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Author: xiaodong.li
@Time: 5/6/2024 2:23 PM
@Description: Description
@File: refresh_incremental_sql.py
"""
import os
import shutil
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from common_utils.handle_git import git_add_safe, git_clone_with_credentials, is_latest, git_pull, \
    get_git_directory_structure
from migration.core.incremental_sql import filter_by_pattern, copy_file


class LocalGitRepository:
    prefix = "Git-Repository-"

    def __init__(self):
        self.dir_path = None
        self.need_clone = None
        self.latest = False

    def init(self, is_rm=False):
        git_repositories = self.query()
        # 确认系统临时目录中是否存在GIT_PREFIX文件夹
        if len(git_repositories) == 0:
            self.need_clone = True
            self.dir_path = tempfile.mkdtemp(prefix=self.prefix)
        elif len(git_repositories) == 1:
            self.dir_path = git_repositories[0]
            if is_rm is True:
                self.need_clone = True
                os.system(f"rmdir /s /q {self.dir_path}")
            else:
                self.need_clone = False
        else:
            for git_repository in git_repositories:
                shutil.rmtree(git_repository)
            self.dir_path = tempfile.mkdtemp(prefix=self.prefix)
            self.need_clone = True

    def query(self):
        temp_dir = tempfile.gettempdir()
        git_repositories = []
        for root, dirs, files in os.walk(temp_dir):
            for dir_name in dirs:
                if dir_name.startswith(self.prefix):
                    git_repositories.append(os.path.join(root, dir_name))
        return git_repositories


def load_local_git_repository(url, user, pwd, branch_name, incremental_sql_dir, is_rm=False):
    r = LocalGitRepository()
    r.init(is_rm)
    git_add_safe(r.dir_path)
    if r.need_clone is True:
        git_clone_with_credentials(url, user, pwd, r.dir_path, branch_name)
    try:
        r.latest = is_latest(r.dir_path, branch_name)
    except Exception as e:
        print(e)
        return load_local_git_repository(url, user, pwd, branch_name, incremental_sql_dir, True)
    return r


def refresh_git_incremental_file(url, user, pwd, branch_name, incremental_sql_dir):
    r: LocalGitRepository = load_local_git_repository(url, user, pwd, branch_name, incremental_sql_dir)
    if r.dir_path is not None and (r.latest is False or r.need_clone):
        git_pull_and_copy_incremental_sql(r.dir_path, branch_name, incremental_sql_dir)


def git_pull_and_copy_incremental_sql(local_git_repository_dir, branch_name, incremental_sql_dir):
    git_pull(local_git_repository_dir, branch_name)
    items = get_git_directory_structure(local_git_repository_dir)
    f_result = filter_by_pattern(items)
    copy_file(incremental_sql_dir, local_git_repository_dir, f_result)
