
from datetime import timedelta
from importlib import reload
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, TransactionTestCase
from django.utils import timezone
import requests_mock


# Create your tests here.
from feeds.models import Source, Subscription, Post
from feeds.utils_internal import (
    fix_relative,
    hash_body,
)
from feeds.utils import (
    read_feed,
    get_subscription_list_for_user,
    get_unread_subscription_list_for_user
)

from feeds import utils
from feeds import utils_internal


User = get_user_model()

TEST_FILES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
BASE_URL = 'http://feed.com/'


class NullOutput(object):

    # little class to stop the tests filling the console window
    def write(self, strin: str):
        pass


class UtilsTest(TestCase):

    def test_fix_relative(self):

        url = "https://example.com/rss.xml"
        html = "<a href='/'><img src='/image.jpg'></a>"

        html = fix_relative(html, url)

        self.assertEqual(html, "<a href='https://example.com/'><img src='https://example.com/image.jpg'></a>")


class BaseTest(TransactionTestCase):

    def _populate_mock(self, mock, test_file, status, content_type, etag=None, headers=None, url=BASE_URL, is_cloudflare=False):

        content = open(os.path.join(TEST_FILES_FOLDER, test_file), "rb").read()

        ret_headers = {"Content-Type": content_type, "etag": "an-etag"}
        if headers is not None:
            ret_headers = {**ret_headers, **headers}

        if is_cloudflare:
            ret_headers["Server"] = "Some cloudflare thing"
            mock.register_uri('GET', url, status_code=status, content=content, headers=ret_headers)
        else:
            if etag is None:
                mock.register_uri('GET', url, status_code=status, content=content, headers=ret_headers)
            else:
                mock.register_uri('GET', url, request_headers={'If-None-Match': etag}, status_code=status, content=content, headers=ret_headers)


@requests_mock.Mocker()
class SubscriptionsTest(BaseTest):

    def test_single_user(self, mock):

        self._populate_mock(mock, status=200, test_file="rss_xhtml_body.xml", content_type="application/rss+xml")

        ls = timezone.now()
        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
        src.save()

        # Read the feed once to get the 1 post  and the etag
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.unread_count, 1)

        self.assertEqual(len(src.get_unread_posts()), 1)

        src.mark_read()

        src.refresh_from_db()

        self.assertEqual(src.unread_count, 0)

        self.assertEqual(len(src.get_unread_posts()), 0)

    def test_subscriber_count(self, mock):

        ls = timezone.now()
        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
        src.save()
        src.refresh_from_db()
        # If we don't use Subscriptions then the default is 1
        self.assertEqual(src.subscriber_count, 1)

        # First subscriber keeps num_subs at 1
        user = User(email='x@example.com')
        user.save()
        sub = Subscription(user=user, source=src)
        sub.save()
        src.refresh_from_db()
        self.assertEqual(src.subscriber_count, 1)

        # Second subscriber ups it to 2
        user2 = User(email='y@example.com')
        user2.save()
        sub2 = Subscription(user=user2, source=src)
        sub2.save()
        src.refresh_from_db()
        self.assertEqual(src.subscriber_count, 2)

        # deleting Subscriptions drops the subscriber count
        sub.delete()
        src.refresh_from_db()
        self.assertEqual(src.subscriber_count, 1)

        # all the way down to none
        sub2.delete()
        src.refresh_from_db()
        self.assertEqual(src.subscriber_count, 0)

    def test_basic_subscription(self, mock):

        self._populate_mock(mock, status=200, test_file="rss_xhtml_body.xml", content_type="application/rss+xml")

        ls = timezone.now()
        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
        src.save()

        user = User(email='x@example.com')
        user.save()

        read_feed(src, output=NullOutput())

        sub = Subscription(user=user, source=src)
        sub.save()
        sub.refresh_from_db()

        self.assertEqual(src.unread_count, 1)

        sub.mark_read()

        sub.refresh_from_db()

        self.assertEqual(sub.unread_count, 0)

    def test_get_subscription_list_1(self, mock):

        user = User(email='x@example.com')
        user.save()

        for i in range(5):
            ls = timezone.now()
            src = Source(name="test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.max_index = 1
            src.save()

            sub = Subscription(user=user, source=src)
            sub.save()

        sub_list = get_subscription_list_for_user(user)

        self.assertEqual(len(sub_list), 5)

    def test_get_subscription_list_2(self, mock):

        user = User(email='x@example.com')
        user.save()

        for i in range(5):
            ls = timezone.now()
            src = Source(name="test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.max_index = 1
            src.save()

            sub = Subscription(user=user, source=src)
            sub.save()

        folder = Subscription(user=user, source=None, name="Folder")
        folder.save()

        for i in range(5):
            ls = timezone.now()
            src = Source(name="folder_test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.max_index = 1
            src.save()

            sub = Subscription(user=user, source=src, parent=folder)
            sub.save()

        all_subs_and_folder = Subscription.objects.filter(user=user).count()

        sub_list = get_subscription_list_for_user(user)

        self.assertEqual(all_subs_and_folder, 11)
        self.assertEqual(len(sub_list), 6)

    def test_basic_subscription_read(self, mock):

        user = User(email='x@example.com')
        user.save()

        for i in range(5):
            ls = timezone.now()
            src = Source(name="test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.max_index = 1
            src.last_read
            src.save()

            sub = Subscription(user=user, source=src)
            sub.save()

        folder = Subscription(user=user, source=None, name="Folder")
        folder.save()

        for i in range(5):
            ls = timezone.now()
            src = Source(name="folder_test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.max_index = 1
            src.save()

            # make the posts get created earlier as they increase in index to check the ordering below
            p = Post(source=src, title=f"post{i}", created=timezone.now() - timedelta(days=i), index=1, guid=f"src-{src.id}-post-{i}")
            p.save()

            sub = Subscription(user=user, source=src, parent=folder)
            src.last_read = 0
            sub.save()

        all_subs_and_folder = Subscription.objects.filter(user=user).count()

        sub_list = get_unread_subscription_list_for_user(user)

        self.assertEqual(all_subs_and_folder, 11)
        self.assertEqual(len(sub_list), 6)

        for s in sub_list:
            if s.source is None:
                self.assertEqual(s.unread_count, 5)

                self.assertEqual(len(s.get_unread_posts()), 5)

                i = 5
                for p in s.get_unread_posts():
                    i -= 1
                    self.assertEqual(p.title, f"post{i}")

    def test_nested_subscription_read(self, mock):

        user = User(email='x@example.com')
        user.save()

        pcount = 0

        for i in range(3):
            ls = timezone.now()
            src = Source(name="test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.save()

            for j in range(3):
                p = Post(source=src, title="post", created=timezone.now())
                p.save()

            sub = Subscription(user=user, source=src)
            sub.save()

        folder = Subscription(user=user, source=None, name="Folder")
        folder.save()

        for i in range(3):
            ls = timezone.now()
            src = Source(name="folder1_test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.save()

            for j in range(3):
                p = Post(source=src, title=f"post-{pcount}", created=timezone.now()-timedelta(days=pcount))
                p.save()
                pcount += 1

            sub = Subscription(user=user, source=src, parent=folder)
            sub.name = f"Sub-1-{i}"
            sub.save()

        folder2 = Subscription(user=user, source=None, name="AFolder2", parent=folder)
        folder2.save()

        for i in range(3):
            ls = timezone.now()
            src = Source(name="folder2_test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.save()

            for j in range(3):
                p = Post(source=src, title=f"post-{pcount}", created=timezone.now()-timedelta(days=pcount))
                p.save()
                pcount += 1

            sub = Subscription(user=user, source=src, parent=folder2)
            sub.save()

        all_subs_and_folder = Subscription.objects.filter(user=user).count()

        sub_list = get_unread_subscription_list_for_user(user)

        self.assertEqual(all_subs_and_folder, 11)
        self.assertEqual(len(sub_list), 4)

        for s in sub_list:
            if s.source is None:
                self.assertEqual(s.unread_count, 18)
                self.assertEqual(len(s.get_unread_posts()), 18)
                last = None
                for p in s.get_unread_posts():
                    if last:
                        self.assertGreater(p.created, last.created)
                    last = p

        (posts, paginator) = folder.get_paginated_posts(1, posts_per_page=10)
        self.assertEqual(len(posts), 10)
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(posts[0].subscription.name, "Sub-1-0")

        (posts, paginator) = folder.get_paginated_posts(2, posts_per_page=10)
        self.assertEqual(len(posts), 8)

    def test_get_unread(self, mock):

        self._populate_mock(mock, status=200, test_file="rss_xhtml_body.xml", content_type="application/rss+xml")

        ls = timezone.now()
        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
        src.save()

        # Read the feed once to get the 1 post  and the etag
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(len(src.get_unread_posts()), 1)
        src.mark_read()
        src.refresh_from_db()
        self.assertEqual(len(src.get_unread_posts()), 0)

    def test_get_unread_count_for_single_folder(self, mock):

        user = User(email='x@example.com')
        user.save()

        for i in range(3):
            ls = timezone.now()
            src = Source(name="test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.max_index = 1
            src.save()

            sub = Subscription(user=user, source=src)
            sub.save()

        folder = Subscription(user=user, source=None, name="Folder")
        folder.save()

        for i in range(3):
            ls = timezone.now()
            src = Source(name="folder1_test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.max_index = 1
            src.save()

            sub = Subscription(user=user, source=src, parent=folder)
            sub.save()

        folder2 = Subscription(user=user, source=None, name="AFolder2", parent=folder)
        folder2.save()

        for i in range(3):
            ls = timezone.now()
            src = Source(name="folder2_test{i}".format(i=i), feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
            src.max_index = 1
            src.save()

            sub = Subscription(user=user, source=src, parent=folder2)
            sub.save()

        folder.refresh_from_db()
        all_subs_and_folder = Subscription.objects.filter(user=user).count()

        self.assertEqual(all_subs_and_folder, 11)
        self.assertEqual(folder.unread_count, 6)


@requests_mock.Mocker()
class XMLFeedsTest(BaseTest):

    def test_simple_xml(self, mock):

        self._populate_mock(mock, status=200, test_file="rss_xhtml_body.xml", content_type="application/rss+xml")

        ls = timezone.now()
        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
        src.save()

        # Read the feed once to get the 1 post  and the etag
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        self.assertEqual(src.posts.count(), 1)  # got the one post
        self.assertEqual(src.interval, 60)
        self.assertEqual(src.etag, "an-etag")
        self.assertNotEqual(src.last_success, ls)
        self.assertNotEqual(src.last_change, ls)

    def test_podcast(self, mock):

        self._populate_mock(mock, status=200, test_file="podcast.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        # Read the feed once to get the 1 post  and the etag
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.description, 'SU: Three nerds discussing tech, Apple, programming, and loosely related matters.')

        self.assertEqual(src.posts.all()[0].enclosures.count(), 1)

        enc = src.posts.all()[0].enclosures.all()[0]

        self.assertEqual(enc.href, "http://traffic.libsyn.com/atpfm/atp238.mp3")

    def test_mastodon(self, mock):

        self._populate_mock(mock, status=200, test_file="mastodon.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.description, 'Public posts from @xurble@toot.community')

        self.assertEqual(src.posts.all()[0].enclosures.count(), 1)

    def test_youtube_embed(self, mock):

        self._populate_mock(mock, status=200, test_file="youtube.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        post = src.posts.all()[0]

        self.assertTrue("iframe" in post.body)


    def test_media_content(self, mock):

        self._populate_mock(mock, status=200, test_file="media_content.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        post = src.posts.all()[0]
        self.assertEqual(post.enclosures.count(), 1)

        self.assertEqual(post.body, "<p>New job, new Mac.</p>")

        enc = post.enclosures.all()[0]

        self.assertEqual(enc.href, "https://static.toot.community/media_attachments/files/111/981/336/553/711/283/original/d83ded1af64141ba.jpeg")
        self.assertEqual(enc.description, "This is the alt text.")

    def test_keep_old_enclosure(self, mock):

        settings.FEEDS_KEEP_OLD_ENCLOSURES = True

        # to pick up the settings change
        reload(utils)
        reload(utils_internal)

        self._populate_mock(mock, status=200, test_file="media_content.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())

        self._populate_mock(mock, status=200, test_file="media_content_changed.xml", content_type="application/rss+xml")

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        post = src.posts.all()[0]
        self.assertEqual(post.enclosures.count(), 2)

        self.assertEqual(post.current_enclosures.count(), 1)
        self.assertEqual(post.old_enclosures.count(), 1)

        enc = post.current_enclosures.all()[0]

        self.assertEqual(enc.href, "https://static.toot.community/media_attachments/files/111/981/336/553/711/283/original/d83ded1af64141ba_new.jpeg")

    def test_save_json(self, mock):

        settings.FEEDS_SAVE_JSON = True

        # to pick up the settings change
        reload(utils)
        reload(utils_internal)

        self._populate_mock(mock, status=200, test_file="media_content.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()
        self.assertEqual(src.json["feed"]["link"], "https://toot.community/@xurble")

        post = src.posts.all()[0]
        self.assertEqual(post.json["summary"], post.body)

    def test_sanitize_1(self, mock):

        """
            Make sure feedparser's sanitization is running
        """

        self._populate_mock(mock, status=200, test_file="rss_xhtml_body.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        # Read the feed once to get the 1 post  and the etag
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        p = src.posts.all()[0]

        self.assertFalse("<script>" in p.body)

    def test_sanitize_2(self, mock):
        """
            Another test that the sanitization is going on.  This time we have
            stolen a test case from the feedparser libarary
        """

        self._populate_mock(mock, status=200, test_file="sanitizer_bad_comment.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        # read the feed to update the name
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        self.assertEqual(src.name, "safe")

    def test_sanitize_attrs(self, mock):

        self._populate_mock(mock, status=200, test_file="sanitizer_img_attrs.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        # read the feed to update the name
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)

        body = src.posts.all()[0].body

        self.assertTrue("<img" in body)
        self.assertFalse("align=" in body)
        self.assertFalse("hspace=" in body)
        self.assertTrue("class=" in body)
        self.assertFalse("style=" in body)

    def test_sanitize_style(self, mock):

        self._populate_mock(mock, status=200, test_file="sanitizer_style.xml", content_type="application/rss+xml")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        # read the feed to update the name
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)

        body = src.posts.all()[0].body

        print (body)

        self.assertTrue("<img" in body)
        self.assertFalse("align=" in body)
        self.assertFalse("hspace=" in body)
        self.assertTrue("class=" in body)
        self.assertFalse("style=" in body)


    def create_source(self, mock, test_name, test_fn):
        self._populate_mock(mock, status=200,
                            test_file=test_fn,
                            content_type="application/rss+xml")
        src = Source(name=test_name, feed_url=BASE_URL, interval=0)
        src.save()
        # read the feed to update the name
        read_feed(src, output=NullOutput())
        src.refresh_from_db()
        self.assertEqual(src.status_code, 200)
        return src

    def test_catch_long_guid_short_url(self, mock):
        test_name = "long guid short url"
        src = self.create_source(mock, test_name, "long_guid_tests.xml")
        # post with long guid should have hash guid
        p = src.posts.get(title=test_name)
        self.assertEqual(p.guid, p.link)

    def test_catch_long_guid_long_url(self, mock):
        test_name = "long guid long url"
        src = self.create_source(mock, test_name, "long_guid_tests.xml")
        # post with long guid should have hash guid
        p = src.posts.get(title=test_name)
        self.assertEqual(p.guid, hash_body(p.body))


@requests_mock.Mocker()
class JSONFeedTest(BaseTest):

    def test_simple_json(self, mock):

        self._populate_mock(mock, status=200, test_file="json_simple_two_entry.json", content_type="application/json")

        ls = timezone.now()

        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls, last_change=ls)
        src.save()

        # Read the feed once to get the 1 post  and the etag
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        self.assertEqual(src.posts.count(), 2)  # got the one post
        self.assertEqual(src.interval, 60)
        self.assertEqual(src.etag, "an-etag")
        self.assertNotEqual(src.last_success, ls)
        self.assertNotEqual(src.last_change, ls)

    def test_save_json(self, mock):

        settings.FEEDS_SAVE_JSON = True

        # to pick up the settings change
        reload(utils)
        reload(utils_internal)

        self._populate_mock(mock, status=200, test_file="json_simple_two_entry.json", content_type="application/json")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()
        self.assertEqual(src.json["title"], src.name)

        post = src.posts.all()[0]
        self.assertEqual(post.json["url"], post.link)

    def test_sanitize_1(self, mock):

        self._populate_mock(mock, status=200, test_file="json_simple_two_entry.json", content_type="application/json")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        # Read the feed once to get the 1 post  and the etag
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        p = src.posts.all()[0]

        self.assertFalse("<script>" in p.body)

    def test_sanitize_2(self, mock):
        """
            Another test that the sanitization is going on.  This time we have
            stolen a test case from the feedparser libarary
        """

        self._populate_mock(mock, status=200, test_file="sanitizer_bad_comment.json", content_type="application/json")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        # read the feed to update the name
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        self.assertEqual(src.name, "safe")

    def test_podcast(self, mock):

        self._populate_mock(mock, status=200, test_file="podcast.json", content_type="application/json")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        # read the feed to update the name
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)

        post = src.posts.all()[0]

        self.assertEqual(post.enclosures.count(), 1)


@requests_mock.Mocker()
class HTTPStuffTest(BaseTest):

    def test_etags(self, mock):

        self._populate_mock(mock, status=200, test_file="rss_xhtml_body.xml", content_type="application/xml+rss")
        self._populate_mock(mock, status=304, test_file="empty_file.txt", content_type="application/xml+rss", etag="an-etag")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        # Read the feed once to get the 1 post  and the etag
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        self.assertEqual(src.posts.count(), 1)  # got the one post
        self.assertEqual(src.interval, 60)
        self.assertEqual(src.etag, "an-etag")

        # Read the feed again to get a 304 and a small increment to the interval
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.posts.count(), 1)  # should have no more
        self.assertEqual(src.status_code, 304)
        self.assertEqual(src.interval, 70)
        self.assertTrue(src.live)

    def test_not_a_feed(self, mock):

        self._populate_mock(mock, status=200, test_file="spurious_text_file.txt", content_type="text/plain")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)  # it returned a page, but not a  feed
        self.assertEqual(src.posts.count(), 0)  # can't have got any
        self.assertEqual(src.interval, 120)
        self.assertTrue(src.live)

    def test_permission_denied(self, mock):

        self._populate_mock(mock, status=403, test_file="empty_file.txt", content_type="text/plain")

        ls = timezone.now()

        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 403)  # it returned a page, but not a  feed
        self.assertEqual(src.posts.count(), 0)  # can't have got any
        self.assertFalse(src.live)

    def test_cloudflared_standard(self, mock):

        settings.FEEDS_DRIPFEED_KEY = "Key"

        # to pick up the settings change
        reload(utils)

        self._populate_mock(mock, status=403, test_file="empty_file.txt", content_type="text/plain", is_cloudflare=True)

        mock.register_uri('PUT', "https://dripfeed.app/api/v1/feeds/", content=b"""{"feed": {"uuid": "aa48333e-c40d-47ac-8a46-a13352dd8505", "name": "Elephant", "source_url": "http://feed.com/", "status_code": 200, "last_polled": "2024-03-17T18:48:19Z", "next_poll": "2024-03-25T03:06:08.991Z", "content_type": "text/plain", "etag": "06b06eb5", "error_code": "not-feed", "last_result": "Server response was not a feed", "dripfeed_url": "https://dripfeed.app/feed/aa48333e-c40d-47ac-8a46-a13352dd8505/", "live": true}, "detail": "OK"}""")

        ls = timezone.now()

        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 403)  # it returned a page, but not a  feed
        self.assertEqual(src.posts.count(), 0)  # can't have got any
        self.assertTrue(src.live)
        self.assertTrue(src.is_cloudflare)
        self.assertEqual(src.alt_url, "https://dripfeed.app/feed/aa48333e-c40d-47ac-8a46-a13352dd8505/")

    def test_cloudflared_already_dripfed(self, mock):

        settings.FEEDS_DRIPFEED_KEY = "Key"

        # to pick up the settings change
        reload(utils)

        self._populate_mock(mock, status=403, test_file="empty_file.txt", content_type="text/plain", is_cloudflare=True)

        mock.register_uri('PUT', "https://dripfeed.app/api/v1/feeds/", status_code=400, content=b"""{"detail": "Already subscribed to this feed."}""")
        mock.register_uri('GET', "https://dripfeed.app/api/v1/feeds/", content=b"""{"feeds": [{"uuid": "aa48333e-c40d-47ac-8a46-a13352dd8505", "name": "Elephant", "source_url": "http://feed.com/", "status_code": 200, "last_polled": "2024-03-17T18:48:19Z", "next_poll": "2024-03-25T03:06:08.991Z", "content_type": "text/plain", "etag": "06b06eb5", "error_code": "not-feed", "last_result": "Server response was not a feed", "dripfeed_url": "https://dripfeed.app/feed/aa48333e-c40d-47ac-8a46-a13352dd8505/", "live": true}], "detail": "OK"}""")

        ls = timezone.now()

        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 403)  # it returned a page, but not a  feed
        self.assertEqual(src.posts.count(), 0)  # can't have got any
        self.assertTrue(src.live)
        self.assertTrue(src.is_cloudflare)
        self.assertEqual(src.alt_url, "https://dripfeed.app/feed/aa48333e-c40d-47ac-8a46-a13352dd8505/")

    def test_cloudflared_cant_dripfeed(self, mock):

        settings.FEEDS_DRIPFEED_KEY = "Key"

        # to pick up the settings change
        reload(utils)

        self._populate_mock(mock, status=403, test_file="empty_file.txt", content_type="text/plain", is_cloudflare=True)

        mock.register_uri('PUT', "https://dripfeed.app/api/v1/feeds/", status_code=403, content=b"""{"detail": "Maximum number of feeds reached."}""")

        ls = timezone.now()

        src = Source(name="test1", feed_url=BASE_URL, interval=0, last_success=ls)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 403)  # it returned a page, but not a  feed
        self.assertEqual(src.posts.count(), 0)  # can't have got any
        self.assertTrue(src.live)
        self.assertTrue(src.is_cloudflare)
        self.assertIsNone(src.alt_url)
        self.assertEqual(src.last_result, "Failed add to Dripfeed: Maximum number of feeds reached.")

    def test_feed_gone(self, mock):

        self._populate_mock(mock, status=410, test_file="empty_file.txt", content_type="text/plain")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 410)  # it returned a page, but not a  feed
        self.assertEqual(src.posts.count(), 0)  # can't have got any
        self.assertFalse(src.live)

    def test_feed_not_found(self, mock):

        self._populate_mock(mock, status=404, test_file="empty_file.txt", content_type="text/plain")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 404)  # it returned a page, but not a  feed
        self.assertEqual(src.posts.count(), 0)  # can't have got any
        self.assertTrue(src.live)
        self.assertEqual(src.interval, 120)

    def test_temp_redirect(self, mock):

        new_url = "http://new.feed.com/"
        self._populate_mock(mock, status=302, test_file="empty_file.txt", content_type="text/plain", headers={"Location": new_url})
        self._populate_mock(mock, status=200, test_file="rss_xhtml_body.xml", content_type="application/xml+rss",  url=new_url)

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        self.assertIsNone(src.last_302_start)

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        self.assertEqual(src.last_302_url, new_url)  # this is where  went
        self.assertIsNotNone(src.last_302_start)
        self.assertEqual(src.posts.count(), 1)  # after following redirect will have 1 post
        self.assertEqual(src.interval, 60)
        self.assertTrue(src.live)

        # do it all again -  shouldn't change
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)  # it returned a page, but not a  feed
        self.assertEqual(src.last_302_url, new_url)  # this is where  went
        self.assertIsNotNone(src.last_302_start)
        self.assertEqual(src.posts.count(), 1)  # after following redirect will have 1 post
        self.assertEqual(src.interval, 80)
        self.assertTrue(src.live)

        # now we test making it permaent
        src.last_302_start = timezone.now() - timedelta(days=365)
        src.save()
        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        self.assertEqual(src.last_302_url, ' ')
        self.assertIsNone(src.last_302_start)
        self.assertEqual(src.posts.count(), 1)
        self.assertEqual(src.interval, 100)
        self.assertEqual(src.feed_url, new_url)
        self.assertTrue(src.live)

    def test_perm_redirect(self, mock):

        new_url = "http://new.feed.com/"
        self._populate_mock(mock, status=301, test_file="empty_file.txt", content_type="text/plain", headers={"Location": new_url})
        self._populate_mock(mock, status=200, test_file="rss_xhtml_body.xml", content_type="application/xml+rss",  url=new_url)

        src = Source(name="test1", feed_url=BASE_URL, interval=60)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 301)
        self.assertEqual(src.interval, 60)
        self.assertEqual(src.feed_url, new_url)

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 200)
        self.assertEqual(src.posts.count(), 1)
        self.assertEqual(src.interval, 60)
        self.assertTrue(src.live)

    def test_server_error_1(self, mock):

        self._populate_mock(mock, status=500, test_file="empty_file.txt", content_type="text/plain")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 500)  # error
        self.assertEqual(src.posts.count(), 0)  # can't have got any
        self.assertTrue(src.live)
        self.assertEqual(src.interval, 120)

    def test_server_error_2(self, mock):

        self._populate_mock(mock, status=503, test_file="empty_file.txt", content_type="text/plain")

        src = Source(name="test1", feed_url=BASE_URL, interval=0)
        src.save()

        read_feed(src, output=NullOutput())
        src.refresh_from_db()

        self.assertEqual(src.status_code, 503)  # error!
        self.assertEqual(src.posts.count(), 0)  # can't have got any
        self.assertTrue(src.live)
        self.assertEqual(src.interval, 120)
