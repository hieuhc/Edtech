"""
author: Hieu Huynh Feb 8th, 2016.
Extract the feed items from json log files
"""
import csv
import json
from EdTech import Constant
import pandas as pd
import datetime
from collections import Counter

class FeedItem:
    def __init__(self):
        print('-Start init FeedItem')

    def feed_extraction(self, file_name_in, file_name_out=None):
        """
        :return: feedItemId, currentSpaceId, space_1, feedItemActorId, feedItemActorType, feedItemVerbId
        [object] isAnnouncement, commentThreadId, commentCount, contentType, id, name, topics.name, topics.id
        """
        feed_temp_file = 'feed_temp.csv'
        data_feed = json.load(open(file_name_in))
        data_feed_extract = csv.writer(open(feed_temp_file, 'w', encoding='utf8'), delimiter=',',
                                       lineterminator='\n')
        data_feed_extract.writerow(['feedItemId', 'currentSpaceId', 'space_1', 'feedItemActorId', 'feedItemActorType',
                                    'feedItemVerbId', 'object.isAnnouncement', 'object.commentThreadId',
                                    'object.commentsCount',
                                    'object.contentType', 'object.id', 'object.name', 'object.topics.name',
                                    'object.topics.id'])
        data_feed_rows = []
        for item in data_feed:
            if item['event'] == 'Viewed feedItem':
                item_properties = item['properties']
                feed_row_value = [
                    item_properties['feedItemId'], item_properties['currentSpaceId'],
                    Constant.ID_COURSE_DICT[item_properties['currentSpaceId']],
                    item_properties['feedItemActorId'], item_properties['feedItemActorType'],
                    item_properties['feedItemVerbId']]
                # add object attributes
                object_attribute = ['isAnnouncement', 'commentThreadId', 'commentsCount', 'contentType', 'id', 'name']
                feed_desc = item_properties['feedItemDescription']
                for obj_att in object_attribute:
                    if obj_att in feed_desc['object']:
                        feed_row_value.append(feed_desc['object'][obj_att])
                    else:
                        feed_row_value.append('')
                #  add topic names and topic ids
                topics_name, topics_id = [], []
                if 'topics' in feed_desc['object']:
                    for obj_topic_item in feed_desc['object']['topics']:
                        topics_name.append(obj_topic_item['name'])
                        topics_id.append(obj_topic_item['id'])
                else:
                    print('- topics not in object: %d' % item_properties['time'])
                feed_row_value.append('||'.join(topics_name))
                feed_row_value.append('||'.join(topics_id))
                data_feed_rows.append(feed_row_value)

        for data_feed_row in data_feed_rows:
            data_feed_extract.writerow(data_feed_row)
        data_feed = pd.read_csv(feed_temp_file, encoding='utf8')
        item_feed_set = set(data_feed.feedItemId.values)
        item_count_dict = {}
        for row_idx in range(data_feed.shape[0]):
            feed_crr = data_feed.feedItemId[row_idx]
            count_crr = data_feed.ix[row_idx, 'object.commentsCount']
            if feed_crr not in item_count_dict:
                item_count_dict[feed_crr] = (row_idx, count_crr)
            elif count_crr > item_count_dict[feed_crr][1]:
                item_count_dict[feed_crr] = (row_idx, count_crr)
        for item in item_feed_set:
            print(item)
        assert len(item_feed_set) == len(item_count_dict), 'item feed set and item count dict len different, %d-%d' % \
                                                           (len(item_feed_set), len(item_count_dict))
        print(len(item_feed_set))
        print(len(item_count_dict))
        row_keep = [item_count_dict[item][0] for item in item_count_dict]
        print(len(row_keep))
        data_feed = pd.DataFrame(data_feed.ix[row_keep, :].values, columns=data_feed.columns)
        print(data_feed.shape)
        if file_name_out is not None:
            data_feed.to_csv(file_name_out, header=True, index=False)
        return data_feed

    def feed_update(self, feed_base_file, json_file, feed_base_out):
        feed_base = pd.read_csv(feed_base_file, encoding='utf8')
        feed_base_count_dict = {feed_base.feedItemId[row_idx]: feed_base.ix[row_idx, 'object.commentsCount']
                                for row_idx in range(feed_base.shape[0])}
        feed_update = self.feed_extraction(json_file)
        feed_update_row = []
        for row_idx in range(feed_update.shape[0]):
            feed_crr = feed_update.feedItemId[row_idx]
            count_crr = feed_update.ix[row_idx, 'object.commentsCount']
            if (feed_crr in feed_base_count_dict) and (count_crr > feed_base_count_dict[feed_crr]):
                feed_base_count_dict[feed_crr] = count_crr
            else:
                feed_update_row.append(row_idx)

        for row_idx in range(feed_base.shape[0]):
            feed_crr = feed_base.feedItemId[row_idx]
            if feed_crr in feed_base_count_dict:
                feed_base.ix[row_idx, 'object.commentsCount'] = feed_base_count_dict[feed_crr]

        print(feed_base.shape), print(len(feed_update_row))
        feed_base = pd.concat([feed_base, feed_update.ix[feed_update_row, :]], axis=0, ignore_index=True)
        print(feed_base.shape)
        feed_base.to_csv(feed_base_out, header=True, index=False)

    def feed_view_extraction(self, data_file, feed_view_file_name, init):
        data = pd.read_csv(data_file, encoding='utf8')
        if init:
            feed_view_file = csv.writer(open(feed_view_file_name, 'w', encoding='utf8'), delimiter=',',
                                        lineterminator='\n')
        else:
            feed_view_file = csv.writer(open(feed_view_file_name, 'a', encoding='utf8'), delimiter=',',
                                        lineterminator='\n')
        feed_view_file.writerow(['viewerId', 'feedItemId', 'time_1'])
        for row_idx in range(data.shape[0]):
            if data.event_1[row_idx] == 'Viewed feedItem':
                feed_view_file.writerow([data.distinct_id[row_idx], data.feedItemId[row_idx], data.time_1[row_idx]])


    def feed_view_count(self, feed_file, feed_view_file, date_start, date_end):
        feed_view = pd.read_csv(feed_view_file, encoding='utf8')
        feed_view['date'] = feed_view.time_1.map(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())
        feed_view_r = feed_view[(feed_view.date >= date_start) & (feed_view.date <= date_end)].feedItemId.values
        feed_view_r_dict = Counter(feed_view_r)
        feed_base = pd.read_csv(feed_file, encoding='utf8')
        feed_view_count = [feed_view_r_dict[feed_id] for feed_id in feed_base.feedItemId.values]
        print(feed_view_count)
        feed_base['feed count w. ' + str(date_end)] = feed_view_count
        feed_base.to_csv(feed_file, header=True, index=False)


if __name__ == '__main__':
    feed_obj = FeedItem()
    # feed_obj.feed_extraction('data/json_data/anonymous-student-events.json', 'data/data/feed.csv')
    # print('- Start feed update')
    # feed_obj.feed_update('data/data/feed.csv', 'data/json_data/anonymous-student-events_16.2.1.json',
    #                      'data/data/feed.csv')
    # feed_obj.feed_update('data/data/feed.csv', 'data/json_data/anonymous-student-events_16.2.8.json',
    #                      'data/data/feed.csv')
    # print('- Start feed view extraction')
    # feed_obj.feed_view_extraction('data/data/student.csv', 'data/data/feed_view.csv',
    #                               init=True)
    # print('- Start creating feed view count')
    feed_obj.feed_view_count('data/data/feed.csv', 'data/data/feed_view.csv',datetime.date(2016, 1, 25), datetime.date(2016, 1, 31))
    feed_obj.feed_view_count('data/data/feed.csv', 'data/data/feed_view.csv',datetime.date(2016, 2, 1), datetime.date(2016, 2, 7))