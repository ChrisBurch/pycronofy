class Pages:
    """
        Get paged data from Cronofy.
        Optionally iterate through all data (automatically fetching pages) or manually list and paginate.

        Example data: {'pages': {u'current': 1, u'next_page': u'https://api.cronofy.com/v1/events/pages/[blah blah]', u'total': 2},}
    """

    def __init__(self, client, data, data_type, automatic_pagination=True):
        """
        :param CronofyClient client: CronofyClient (for fetching subsequent pages)
        :param dict data: Dictionary containing json response from cronofy.
        :param string data_type: Type of paged data being retrieved (eg: 'events')
        :param bool automatic_pagination: Default True. During iteration automatically move to the next page.
        """
        self.client = client
        self.current = data['pages']['current']
        self.total = data['pages']['total']
        self.next_page_url = None
        if 'next_page' in data['pages']:
            self.next_page_url = data['pages']['next_page']
        self.data_type = data_type
        self.data = data
        self.index = 0
        self.length = len(self.data[data_type])
        self.automatic_pagination = automatic_pagination

    def __iter__(self):
        """Function as an interator"""
        return self

    def data(self):
        """Get the raw json data of the response
        :return: Dictionary containing response data.
        :rtype: ``dict``
        """
        return self.data

    def fetch_next_page(self):
        """Retrieves the next page of data and refreshes Pages instance."""
        result = self.client._get(url=self.next_page_url)
        self.__init__(self.client, result, self.data_type, self.automatic_pagination)

    def list(self):
        """Return the current json data as a list.
        """
        return self.data[self.data_type]

    def next(self):
        """Python 2 backwards compatibility"""
        return self.__next__()

    def __next__(self):
        """Iterate to the next item in the data set.
        By default fetch the next page if one exists.

        :return: The next item in the data set.
        :rtype: ``dict``
        """
        if self.index < self.length:
            self.index += 1
            return self.data[self.data_type][self.index-1]
        else:
            if self.automatic_pagination and (self.current < self.total):
                self.fetch_next_page()
                return self.__next__()
            else:
                raise StopIteration()
