import sys

import praw
import requests
import tqdm
from group_remote.group_remote import GroupsRemote
# from profile_local.comprehensive_profile import ComprehensiveProfileLocal
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger
from python_sdk_remote.utilities import our_get_env

from .ProfileRedditConstants import (
    PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME
)

REDDIT_CLIENT_ID = our_get_env('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = our_get_env('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = our_get_env('REDDIT_USERNAME')

GROUP_PROFILE_RELATIONSHIP_TYPE_ID = 1

object_to_insert = {
    'component_id': PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': PROFILE_REDDIT_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'yoav.e@circ.zone'
}

logger = Logger.create_logger(object=object_to_insert)


# TODO: get meaningful data from Reddit API
class Reddit(praw.Reddit):

    def __init__(self, is_test_data: bool = False):
        logger.start()
        # TODO Let's add API-Management Indirect around it.
        super().__init__(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=f"random_names (by u/{REDDIT_USERNAME})"
        )
        self.is_test_data = is_test_data
        # self.comprehensive_profile_local = ComprehensiveProfileLocal()
        logger.end()

    def get_reddit_users_by_subreddit(self, subreddit, user_count: int) -> list[dict]:
        logger.start(object={'subreddit': subreddit.name, 'user_count': user_count})
        reddit_users_in_profile_json = []

        # TODO: when 'group' section is ready in ComprehensiveProfilesLocal, delete this line and
        #  add 'group' to reddit_users.append
        group_id = self._create_group_if_not_exists(subreddit.name)
        iteration = 0

        with tqdm.tqdm(total=user_count, desc="Getting users", file=sys.stdout) as pbar:
            for submission in subreddit.new(limit=None):
                if len(reddit_users_in_profile_json) >= user_count:
                    return reddit_users_in_profile_json
                for comment in submission.comments.list():
                    logger.info("Reddit user comment, iteration: " + str(iteration))
                    if len(reddit_users_in_profile_json) >= user_count:
                        return reddit_users_in_profile_json
                    if comment.author.name == 'AutoModerator':
                        continue
                    # TODO: get contact / useful info from comment.author
                    reddit_user_json = {
                        'profile': {
                            'name': str(comment.author.name),
                            'name_approved': True,
                            'lang_code': "en",
                            'visibility_id': True,
                            'is_approved': True,
                            'profile_type_id': 1,
                            'stars': 2,
                            'last_dialog_workflow_state_id': 1,
                            'comments': str(comment.author.comments),
                            'submissions': str(comment.author.submissions),
                            'created_utc': str(comment.author.created_utc),
                            'has_verified_email': str(comment.author.has_verified_email),
                            'is_employee': str(comment.author.is_employee),
                            'is_mod': str(comment.author.is_mod),
                            'is_gold': str(comment.author.is_gold),
                            'link_karma': str(comment.author.link_karma)
                        },

                        'storage': {
                            "url": str(comment.author.icon_img),
                            "filename": f'{comment.author.name}.jpg',
                            "file_type": "Profile Image",
                            "file_extension": "jpg"
                        },

                        'reaction': {
                            'value': str(comment.author.comment_karma),
                            'image': None,
                            'title': 'comment karma',
                            'description': None
                        },
                        'group': {
                            'group_id': group_id,
                            'lang_code': "en",
                            'parent_group_id': None,
                            'is_interest': False,
                            'image': None,
                        },
                        'group_profile': {
                            'group_id': group_id,
                            'relationship_type_id': GROUP_PROFILE_RELATIONSHIP_TYPE_ID
                        },
                        'is_test_data': self.is_test_data
                    }
                    reddit_users_in_profile_json.append(reddit_user_json)
                    logger.info("Reddit user data: " + str(reddit_user_json))
                    iteration += 1

                    pbar.update(1)
        logger.end(object={'reddit_users_in_profile_json': reddit_users_in_profile_json})
        return reddit_users_in_profile_json

    # TODO: when 'group' section is ready in ComprehensiveProfilesLocal, delete this private method
    def _create_group_if_not_exists(self, group_name: str):
        logger.start(object={'group_name': group_name})

        groups_remote_object = GroupsRemote()
        group_response = groups_remote_object.get_group_response_by_group_name(group_name)
        if group_response.status_code == requests.codes.no_content:
            group_response = groups_remote_object.create_group(group_name)
        if group_response.status_code != requests.codes.ok:
            raise Exception(f"Failed to create group: {group_name} with status code: {group_response.status_code}."
                            f" Response: {group_response.text}. Url: {group_response.url}")
        group_json = group_response.json()
        group_id = int(group_json['data'][0]['id'])
        logger.end(object={'group_id': group_id})
        return group_id
