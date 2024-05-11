from collections import defaultdict
import logging

import openai

from riddlesolver.constants import SUMMARY_PROMPT_TEMPLATE
from riddlesolver.utils import format_date, handle_error, calculate_days_between_dates

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def generate_commit_summary(batched_commits, config, output_file=None):
    """
    Generates a summary of commits within the specified date range.

    Args:
        batched_commits (list): A list mapping authors to branches and their corresponding commits.
        config (dict): The configuration dictionary.
        output_file (str): The path to the output file.
    """
    if not batched_commits or len(batched_commits) == 0:
        logger.warning("No commits found within the specified date range.")
        return

    logger.info("=" * 50)

    summary = generate_summary(batched_commits, config)

    if output_file:
        save_summary_to_file(summary, output_file)

    logger.info("=" * 50)
    logger.info("Summary generation complete.")
    return summary


def group_commits_by_author_and_branch(commits, branch_names):
    """
    Groups commits by author and branch.

    Args:
        commits (list): The list of commits.
        branch_names (list): The list of branch names.

    Returns:
        dict: A dictionary mapping authors to branches and their corresponding commits.
    """
    commit_batches = defaultdict(lambda: defaultdict(list))
    for commit in commits:
        author = commit.author.email if hasattr(commit, 'author') else commit['commit']['author']['email']
        for branch_name in branch_names:
            if branch_name == commit.branch if hasattr(commit, 'branch') else True:
                commit_batches[author][branch_name].append(commit)
    return commit_batches


def generate_summary(commit_batches, config):
    """
    Generates a summary of commit batches.

    Args:
        commit_batches (list): A list mapping authors to branches and their corresponding commits.
        config (config): The configuration dictionary.

    Returns:
        str: The generated summary.
    """

    summary = []
    for idx, commit_object in enumerate(commit_batches):
        branch_name = commit_object['branch']
        author = commit_object['author']
        start_date = commit_object['start_date']
        end_date = commit_object['end_date']
        commit_messages = commit_object['commit_messages']
        commit_messages = [message['messages'] for message in commit_messages]
        duration = max(1, calculate_days_between_dates(start_date, end_date))
        openai_summary = get_openai_summary(commit_messages, branch_name, config)
        if openai_summary:
            batch_summary = [
                f"Author: {author}",
                f"Branch: {branch_name}",
                f"Period: {format_date(start_date)} to {format_date(end_date)} ({duration} day(s))",
                f"Summary of {len(commit_messages)} commits:",
                openai_summary,
            ]
            summary_result = "\n".join(batch_summary)
            summary.append(summary_result)
            logger.info(f"Generated summary for author: {author}, branch: {branch_name}")
        else:
            summary_result = f"Failed to generate summary for author: {author}, branch: {branch_name}"
            summary.append(summary_result)
            logger.warning(f"Failed to generate summary for author: {author}, branch: {branch_name}")

        # print summary result to the console
        logger.info(summary_result)

        if idx < len(commit_batches) - 1:
            # separator between different batches
            summary.append("-" * 50)
            logger.info("-" * 50)

    return "\n".join(summary)


def get_openai_summary(commit_messages, branch_name, config):
    """
    Generates a summary of commit messages using the OpenAI API.

    Args:
        commit_messages (list): The list of commit messages.
        branch_name (str): The branch name.
        config (configparser.ConfigParser): The configuration object.

    Returns:
        str: The generated summary.
    """
    model = config.get("openai", "model")
    openai_api_key = config.get("openai", "api_key")
    base_url = config.get("openai", "base_url")

    client = openai.Client(api_key=openai_api_key, base_url=base_url)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": SUMMARY_PROMPT_TEMPLATE.format(branch_name=branch_name, commit_messages=commit_messages)
            }]
        )
        if response.choices:
            summary = response.choices[0].message.content.strip()
            logger.info(f"Generated summary using OpenAI API: {summary}")
            return summary
        else:
            logger.warning("OpenAI API returned an empty response.")
            return None
    except openai.RateLimitError:
        logger.error("OpenAI API request exceeded rate limit.")
        return None
    except openai.AuthenticationError:
        logger.error("OpenAI API authentication failed. Please check your API key.")
        return None
    except openai.APIError as e:
        logger.error(f"OpenAI API Error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return None


def save_summary_to_file(summary, output_file):
    """
    Saves the summary to a file.

    Args:
        summary (str): The summary to save.
        output_file (str): The path to the output file.
    """
    try:
        with open(output_file, "w") as file:
            file.write(summary)
        logger.info(f"Summary saved to {output_file}")
    except IOError as e:
        logger.error(f"Error saving summary to file: {str(e)}")
        handle_error(e)