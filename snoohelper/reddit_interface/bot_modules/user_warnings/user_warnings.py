import snoohelper.utils.utils as utils
from snoohelper.reddit_interface.database_models import UserModel
import time


class UserWarnings:

    def __init__(self, webhook, comment_threshold, submission_threshold, ban_threshold):
        self.webhook = webhook
        self.comment_threshold = comment_threshold
        self.submission_threshold = submission_threshold
        self.ban_threshold = ban_threshold
        self.last_warned = dict()

    def check_user(self, user, thing):
        message = utils.SlackResponse()
        send = False
        attachment = None

        if user.comment_removals > self.comment_threshold:
            attachment = message.add_attachment(title="Warning regarding user /u/" + user.username,
                                    title_link="https://reddit.com/u/" + user.username,
                                    color='#3AA3E3',
                                    text="User has had %s> comments removed. Please check profile history." %
                                    str(self.comment_threshold))
            send = True

        if user.submission_removals > self.submission_threshold:
            attachment = message.add_attachment(title="Warning regarding user /u/" + user.username,
                                                 title_link="https://reddit.com/u/" + user.username,
                                                 color='#3AA3E3',
                                                 text="User has had %s> submissions removed. Please check profile"
                                                      " history." %
                                                      str(self.submission_threshold))
            send = True

        if user.bans > self.ban_threshold:
            attachment = message.add_attachment(title="Warning regarding user /u/" + user.username,
                                                 title_link="https://reddit.com/u/" + user.username,
                                                 color='#3AA3E3',
                                                 text="User has been banned %s> times. Please check profile history." %
                                                      str(self.ban_threshold))
            send = True

        if not user.warnings_muted and send and time.time() - self.last_warned[user.username] > 86400:
            attachment.add_button("Verify", value="verify", style='good')
            attachment.add_button("Track", value="track_" + user.username)
            attachment.add_button("Botban", value="botban_" + user.username, style='danger')
            attachment.add_button("Mute warnings for this user", value="mutewarnings_" + user.username, style='danger')
            self.last_warned[user.username] = time.time()
            self.webhook.send_message(message)

        if user.tracked:
            message = utils.SlackResponse("New post by user /u/" + user.username)

            try:
                title = thing.submission.title
            except AttributeError:
                title = thing.title
            attachment = message.add_attachment(title=title, title_link=thing.permalink, text=thing.body,
                                                color='#3AA3E3')
            attachment.add_button("Verify", value="verify", style='good')
            attachment.add_button("Untrack", value="untrack_" + user.username)
            attachment.add_button("Botban", value="botban_" + user.username, style='danger')
            self.webhook.send_message(message)

    @staticmethod
    def mute_user_warnings(user):
        user = UserModel.get(UserModel.username == user)
        user.warnings_muted = True
        user.save()
