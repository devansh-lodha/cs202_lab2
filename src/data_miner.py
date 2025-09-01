# src/data_miner.py
"""Module for mining bug-fixing commits from a Git repository."""
import os
import logging
import re
import sys
from typing import Optional
import pandas as pd
from pydriller import Repository
from tqdm.auto import tqdm
from src.config_loader import config

def mine_repository(limit: Optional[int] = None) -> pd.DataFrame:
    """
    Mines the configured Git repository for bug-fixing commits, extracting
    metadata, diffs, and the full source code before and after the change.
    """
    repo_url = config['io']['repo_url']
    local_path = config['io']['local_repo_path']
    cols = config['columns']
    logging.info(f"Starting repository mining for {repo_url}")
    
    BUG_KEYWORDS = [
        "fixed", "bug", "fixes", "fix", "crash", "solves", "resolves", "issue",
        "regression", "fail", "npe", "except", "broken", "error", "hang",
        "leak", "overflow", "avoid", "workaround", "break", "stop"
    ]
    BUG_REGEX = re.compile(
        r'.*((solv(ed|es|e|ing))|(fix(s|es|ing|ed)?)|((error|bug|issue)(s)?)).*',
        re.IGNORECASE
    )
    
    clone_dir = os.path.dirname(local_path)
    os.makedirs(clone_dir, exist_ok=True)
    
    repo_miner = Repository(repo_url, clone_repo_to=clone_dir)
    bug_data = []
    commits_processed = 0
    
    for commit in tqdm(repo_miner.traverse_commits(), desc="Mining Commits"):
        if limit and commits_processed >= limit: break
        is_bug_fix = (any(k in commit.msg.lower() for k in BUG_KEYWORDS) or bool(BUG_REGEX.match(commit.msg)))
        if is_bug_fix:
            commit_had_py_file = False
            for mod in commit.modified_files:
                if mod.diff and mod.new_path and mod.new_path.endswith('.py'):
                    bug_data.append({
                        cols['hash']: commit.hash,
                        cols['message']: commit.msg,
                        cols['filename']: mod.new_path,
                        cols['diff']: mod.diff,
                        cols['source_before']: mod.source_code_before,
                        cols['source_current']: mod.source_code
                    })
                    commit_had_py_file = True
            if commit_had_py_file: commits_processed += 1
            
    if not bug_data:
        logging.error("No bug-fixing commits found. Exiting.")
        sys.exit()
        
    df = pd.DataFrame(bug_data)
    logging.info(f"Mining complete. Found {len(df)} files in {commits_processed} commits.")
    return df